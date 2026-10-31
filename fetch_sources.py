# -*- coding: utf-8 -*-
"""数据源归档器。

把知识体系与数据锚点引用到的所有来源页面/文件下载到本地，并生成可校验的清单。

设计要点
- 一源一文件：文件名 = 编号__机构_标题摘要.扩展名，编号与 ANCHORS / SOURCES 一致
- 记录 SHA256、字节数、HTTP 状态、抓取时间、原 URL
- 失败也记录，并写明失败原因（403 / 404 / 需要登录 / 超时）——失败清单本身是资产
- 不覆盖已存在且哈希一致的文件，可反复运行

用法：
    python fetch_sources.py            # 抓取全部
    python fetch_sources.py --only S1,S2,A-01
    python fetch_sources.py --check    # 只校验已有文件，不发起请求
"""
import hashlib
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from energy_anchors import ANCHORS          # noqa: E402
from energy_meta import DATASETS             # noqa: E402
from framework_core import SOURCES          # noqa: E402

# 站点屏蔽自动抓取时的可用替代档案（同为官方源，仅宿主不同）
ARCHIVE_EXTRA = [
    {"id": "X-01", "org": "IPCC", "title": "2006 年指南 第1卷 第3章 不确定性（PDF 原文）",
     "url": "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/1_Volume1/V1_3_Ch3_Uncertainties.pdf"},
    {"id": "X-02", "org": "IPCC", "title": "2006 年指南 第2卷 第2章 固定源燃烧（PDF 原文）",
     "url": "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf"},
    {"id": "X-03", "org": "IPCC", "title": "2019 年修订版 第2卷 第2章 固定源燃烧（PDF 原文）",
     "url": "https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/2_Volume2/19R_V2_2_Ch02_Stationary_Combustion.pdf"},
]

DATA_DIR = "data"
MANIFEST_JSON = os.path.join(DATA_DIR, "manifest.json")
MANIFEST_MD = os.path.join(DATA_DIR, "MANIFEST.md")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# 机构 → 目录名（便于按来源归类）
ORG_DIR = {
    "生态环境部": "mee",
    "国家统计局": "stats",
    "国家能源局": "nea",
    "海关总署": "customs",
    "国家发展改革委": "ndrc",
    "国务院办公厅": "gov",
    "中共中央、国务院": "gov",
    "IPCC": "ipcc",
    "Global Carbon Project": "gcp",
    "欧盟委员会": "eu",
    "IRENA/中电联": "irena",
    "商务部 WTO/FTA 咨询网": "mofcom",
    "中国能源报": "media",
    "中国煤炭工业协会": "media",
    "中国能源新闻网": "media",
    "证券时报": "media",
    "国务院新闻办": "gov",
    "中国政府网": "gov",
}


def slug(s, n=48):
    s = re.sub(r"[\\/:*?\"<>|\s]+", "_", str(s))
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:n]


def org_key(org):
    for k, v in ORG_DIR.items():
        if k in str(org):
            return v
    return "other"


def ext_for(url, ctype):
    u = url.lower().split("?")[0]
    for e in (".pdf", ".xlsx", ".xls", ".csv", ".zip", ".json", ".jpg", ".png"):
        if u.endswith(e):
            return e
    if "pdf" in (ctype or ""):
        return ".pdf"
    if "json" in (ctype or ""):
        return ".json"
    if "image" in (ctype or ""):
        return ".jpg"
    return ".htm"


def collect_targets():
    """汇总去重后的抓取目标。"""
    seen = {}
    out = []
    # 1) 证据链（framework_core.SOURCES）：S 系列
    for sid, x in SOURCES.items():
        u = x.get("url") or ""
        if not u.startswith("http"):
            continue
        if u in seen:
            continue
        seen[u] = True
        out.append({"id": sid, "org": x.get("org", ""), "title": x.get("doc", ""),
                    "url": u, "kind": "证据链"})
    # 2) 数据锚点：A/B/C/D/E/F 系列
    for a in ANCHORS:
        u = a[9]
        if not u.startswith("http"):
            continue
        if u in seen:
            # 同一 URL 被多个锚点引用时，登记别名
            for t in out:
                if t["url"] == u:
                    t.setdefault("alias", []).append(a[0])
            continue
        seen[u] = True
        out.append({"id": a[0], "org": a[8], "title": a[2], "url": u,
                    "kind": "数据锚点", "alias": []})
    # 3) 数据集入口（D 系列）
    for d in DATASETS:
        u = d[6] if len(d) > 6 else ""
        if not u.startswith("http"):
            out.append({"id": d[0], "org": d[2], "title": d[1], "url": "",
                        "kind": "数据集入口", "alias": [], "skip": True,
                        "skipReason": (d[8] if len(d) > 8 else "无公开入口")})
            continue
        if u in seen:
            for t in out:
                if t["url"] == u:
                    t.setdefault("alias", []).append(d[0])
            continue
        seen[u] = True
        out.append({"id": d[0], "org": d[2], "title": d[1], "url": u,
                    "kind": "数据集入口", "alias": []})
    # 4) 补充档案：站点屏蔽的原始文件的可用替代（同源不同宿主）
    for e in ARCHIVE_EXTRA:
        if e["url"] in seen:
            continue
        seen[e["url"]] = True
        out.append(dict(e, kind="补充档案", alias=[]))
    return out


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def main():
    args = sys.argv[1:]
    only = None
    check = "--check" in args
    for a in args:
        if a.startswith("--only"):
            only = set(x.strip() for x in a.split("=", 1)[1].split(","))

    os.makedirs(DATA_DIR, exist_ok=True)
    # 关闭系统代理（当前环境代理不稳，直连可用）
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        os.environ.pop(k, None)
    urllib.request.install_opener(
        urllib.request.build_opener(urllib.request.ProxyHandler({})))

    targets = collect_targets()
    if only:
        targets = [t for t in targets if t["id"] in only]
    print("抓取目标：%d 个唯一 URL" % len(targets))

    records = []
    prev = {}
    if os.path.exists(MANIFEST_JSON):
        for r in json.load(io.open(MANIFEST_JSON, encoding="utf-8")):
            prev[r["id"]] = r
    if check:
        records = list(prev.values())
        print("仅校验模式：已加载清单 %d 条" % len(records))
    else:
        # 保留本次未处理的历史记录（--only 或 --include 时不清空清单）
        if only:
            records = [r for k, r in prev.items() if k not in only]
        for i, t in enumerate(targets, 1):
            d = os.path.join(DATA_DIR, org_key(t["org"]))
            os.makedirs(d, exist_ok=True)
            rec = {"id": t["id"], "kind": t["kind"], "org": t["org"],
                   "title": t["title"], "url": t["url"],
                   "alias": t.get("alias", []), "fetched_at": None,
                   "status": None, "bytes": None, "sha256": None,
                   "file": None, "error": None}
            if t.get("skip"):
                rec["error"] = "无公开入口：" + t.get("skipReason", "")
                print("[%2d/%d] -- %-6s %s" % (i, len(targets), t["id"], rec["error"][:60]))
                records.append(rec)
                continue
            try:
                st, ctype, body = fetch(t["url"])
                ext = ext_for(t["url"], ctype)
                fn = "%s__%s%s" % (t["id"], slug(t["org"]), ext)
                fp = os.path.join(d, fn)
                # 已存在且一致则跳过写盘
                h = hashlib.sha256(body).hexdigest()
                if os.path.exists(fp):
                    old = hashlib.sha256(open(fp, "rb").read()).hexdigest()
                    if old == h:
                        print("[%2d/%d] = %-6s 已存在且一致  %s" % (i, len(targets), t["id"], fn))
                        rec.update(status=st, bytes=len(body), sha256=h,
                                   file=os.path.relpath(fp, DATA_DIR).replace("\\", "/"),
                                   fetched_at=time.strftime("%Y-%m-%dT%H:%M:%S"))
                        records.append(rec)
                        continue
                with open(fp, "wb") as f:
                    f.write(body)
                rec.update(status=st, bytes=len(body), sha256=h,
                           file=os.path.relpath(fp, DATA_DIR).replace("\\", "/"),
                           fetched_at=time.strftime("%Y-%m-%dT%H:%M:%S"))
                print("[%2d/%d] OK %-6s %6.0f KB  %s" % (i, len(targets), t["id"], len(body) / 1024.0, fn))
            except urllib.error.HTTPError as e:
                rec["status"] = e.code
                rec["error"] = "HTTP %d" % e.code
                print("[%2d/%d] !! %-6s HTTP %d  %s" % (i, len(targets), t["id"], e.code, t["url"][:60]))
            except Exception as e:
                rec["error"] = type(e).__name__ + ": " + str(e)[:80]
                print("[%2d/%d] !! %-6s %s" % (i, len(targets), t["id"], rec["error"][:70]))
            records.append(rec)
            time.sleep(0.8)   # 礼貌间隔

    # ---- 校验已有文件 ----
    for r in records:
        if r.get("file"):
            fp = os.path.join(DATA_DIR, r["file"])
            if os.path.exists(fp):
                r["exists"] = True
                r["size_on_disk"] = os.path.getsize(fp)
                r["hash_ok"] = (hashlib.sha256(open(fp, "rb").read()).hexdigest()
                                == r.get("sha256"))
            else:
                r["exists"] = False

    json.dump(records, io.open(MANIFEST_JSON, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)

    ok = [r for r in records if r.get("file")]
    fail = [r for r in records if not r.get("file")]
    tot_kb = sum((r.get("bytes") or 0) for r in ok) / 1024.0

    lines = [
        "# 数据源归档清单", "",
        "**生成时间**：%s  " % time.strftime("%Y-%m-%d %H:%M:%S"),
        "**成功归档**：%d 个  ·  **失败**：%d 个  ·  **合计**：%.1f MB" % (len(ok), len(fail), tot_kb / 1024.0),
        "", "> 本清单由 `fetch_sources.py` 自动生成。每个文件的 SHA256 可用于校验内容未被篡改。",
        "> 失败条目保留原 URL 与失败原因——**失败清单本身是资产**，说明哪些来源需要人工获取。", "",
        "## 一、已归档（%d）" % len(ok), "",
        "| 编号 | 类型 | 机构 | 文件 | 大小 | SHA256 |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(ok, key=lambda x: x["id"]):
        lines.append("| %s | %s | %s | `%s` | %.0f KB | `%s…` |"
                     % (r["id"], r["kind"], r["org"], r["file"],
                        (r.get("bytes") or 0) / 1024.0, (r.get("sha256") or "")[:12]))
    lines += ["", "## 二、未获取（%d）" % len(fail), "",
              "| 编号 | 机构 | 原因 | 原 URL |", "|---|---|---|---|"]
    for r in sorted(fail, key=lambda x: x["id"]):
        u = r["url"]
        lines.append("| %s | %s | %s | %s |"
                     % (r["id"], r["org"], r.get("error") or "未抓取",
                        (u[:90] + "…") if len(u) > 90 else u))
    io.open(MANIFEST_MD, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

    print("\n" + "=" * 60)
    print("成功 %d / 失败 %d  ·  合计 %.2f MB" % (len(ok), len(fail), tot_kb / 1024.0))
    print("清单：%s" % MANIFEST_MD)
    if fail:
        print("\n失败明细：")
        for r in fail:
            print("  %-6s %s" % (r["id"], (r.get("error") or "")[:70]))


def build_index():
    """生成可点击的网址索引（Markdown + JSON）。"""
    recs = json.load(io.open(MANIFEST_JSON, encoding="utf-8")) if os.path.exists(MANIFEST_JSON) else []
    ok = sorted([r for r in recs if r.get("file")], key=lambda x: (x["kind"], x["id"]))
    fail = sorted([r for r in recs if not r.get("file")], key=lambda x: (x["kind"], x["id"]))

    # JSON：机器可读，供程序直接引用
    idx = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "total": len(recs), "archived": len(ok), "failed": len(fail),
           "entries": [{"id": r["id"], "kind": r["kind"], "org": r["org"],
                        "title": r["title"], "url": r["url"],
                        "alias": r.get("alias", []),
                        "localFile": r.get("file"),
                        "bytes": r.get("bytes"), "sha256": r.get("sha256"),
                        "fetchedAt": r.get("fetched_at"),
                        "error": r.get("error")} for r in ok + fail]}
    io.open(os.path.join(DATA_DIR, "url-index.json"), "w", encoding="utf-8",
            newline="\n").write(json.dumps(idx, ensure_ascii=False, indent=1))

    def row(r):
        al = (" ／ " + "、".join(r["alias"])) if r.get("alias") else ""
        loc = ("`%s`" % r["file"]) if r.get("file") else "—"
        return "| **%s**%s | %s | [%s](%s) | %s |" % (
            r["id"], al, r["org"], (r["title"] or "打开")[:34], r["url"], loc)

    L = ["# 数据源网址索引", "",
         "**生成时间**：%s  " % idx["generated"],
         "**总计** %d 条：已归档 **%d** · 未获取 **%d**" % (idx["total"], idx["archived"], idx["failed"]),
         "",
         "> 本文件是全部引用来源的**可点击索引**。点开链接即达原文；「本地文件」列指向已归档副本（在 `data/` 下）。",
         "> 编号与 `energy_anchors.py`（A–F 系列）、`framework_core.py`（S 系列）、`energy_meta.py`（D 系列）一一对应。", ""]

    for kind in ("证据链", "数据锚点", "数据集入口", "补充档案"):
        grp = [r for r in ok if r["kind"] == kind]
        if not grp:
            continue
        L += ["## 已归档 · %s（%d）" % (kind, len(grp)), "",
              "| 编号 | 机构 | 原文链接 | 本地文件 |", "|---|---|---|---|"]
        L += [row(r) for r in grp]
        L.append("")

    if fail:
        L += ["## 未获取（%d）" % len(fail), "",
              "| 编号 | 机构 | 原因 | 原文链接 |", "|---|---|---|---|"]
        for r in fail:
            L.append("| **%s** | %s | %s | %s |" % (
                r["id"], r["org"], r.get("error") or "—",
                ("[%s](%s)" % (r["url"][:60], r["url"])) if r.get("url") else "无公开入口"))
        L.append("")

    io.open(os.path.join(DATA_DIR, "INDEX.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(L) + "\n")
    print("网址索引：%s（%d 条，已归档 %d）" % (os.path.join(DATA_DIR, "INDEX.md"), len(recs), len(ok)))


if __name__ == "__main__":
    if "--index" in sys.argv:
        build_index()
    else:
        main()
        build_index()
