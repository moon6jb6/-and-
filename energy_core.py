# -*- coding: utf-8 -*-
"""能源经济分析体系 —— 装载、校验与数据构造。

把 energy_meta.py（域/层/证据/数据集/模型）与 energy_questions.py（研究问题总表）
合成一份供 HTML / SVG 使用的 DATA 字典，并执行完整性断言。

同时桥接原 137 对象碳核算框架（framework_core），使其成为「05 能源与碳排放」的子模块。
"""
import io
import json

from energy_meta import (VERSION, BUILT, LAYERS4, DOMAINS, EVIDENCE_TIERS,
                         DATASETS, MODELS)
from energy_questions import QUESTIONS
from energy_anchors import (ANCHORS, ANCHOR_ISSUES, ANCHOR_GAPS,
                            ANCHOR_TRAPS, ANCHOR_SUMMARY, validate as validate_anchors)
from data_tasks import (TASKS, SUMMARY as TASK_SUMMARY, STANDARDS, LEVELS,
                        STATUS_META as TASK_STATUS, SCHEMA_FIELDS, CORE_TABLES,
                        ROADMAP)

STATUS_META = {
    "可算": ("可算", "#34d399", "指标算式明确，所需数据已有公开来源"),
    "部分可算": ("部分可算", "#fbbf24", "算式明确，关键数据缺失或口径需自行编纂"),
    "缺关键数据": ("缺关键数据", "#fb7185", "数据源不公开或不存在，当前无法出可靠数值"),
}


def build_energy_data(with_carbon=True):
    dom_ids = [d[0] for d in DOMAINS]
    layer_ids = [l[0] for l in LAYERS4]
    ev_ids = [e[0] for e in EVIDENCE_TIERS]
    ds_ids = [d[0] for d in DATASETS]
    md_ids = [m[0] for m in MODELS]

    # ---------- 基本完整性 ----------
    assert len(DOMAINS) == 12, len(DOMAINS)
    assert len(LAYERS4) == 4, len(LAYERS4)
    assert len(EVIDENCE_TIERS) == 8, len(EVIDENCE_TIERS)
    assert len(set(ds_ids)) == len(ds_ids), "数据集编号重复"
    assert len(set(md_ids)) == len(md_ids), "模型编号重复"
    assert len(set(q["id"] for q in QUESTIONS)) == len(QUESTIONS), "问题编号重复"

    # ---------- 每条问题的字段完整性 ----------
    for q in QUESTIONS:
        assert q["dom"] in dom_ids, "未知域: %s (%s)" % (q["dom"], q["id"])
        assert q["layer"] in layer_ids, "未知层: %s (%s)" % (q["layer"], q["id"])
        assert q["ind"], "问题无指标: %s" % q["id"]
        for t in q["ind"]:
            assert len(t) == 3, "指标须为(名称,单位,算式): %s" % q["id"]
            assert t[2].strip(), "指标算式为空: %s / %s" % (q["id"], t[0])
        assert q["data"], "问题无数据源: %s" % q["id"]
        for d in q["data"]:
            assert d in ds_ids, "未知数据集: %s (%s)" % (d, q["id"])
        assert q["model"], "问题无模型: %s" % q["id"]
        for m in q["model"]:
            assert m in md_ids, "未知模型: %s (%s)" % (m, q["id"])
        assert q["ev"], "问题无证据层次: %s" % q["id"]
        for e in q["ev"]:
            assert e in ev_ids, "未知证据层: %s (%s)" % (e, q["id"])

    # ---------- 12×4 矩阵必须无空格 ----------
    matrix = {}
    for d in dom_ids:
        matrix[d] = {l: [] for l in layer_ids}
    for q in QUESTIONS:
        matrix[q["dom"]][q["layer"]].append(q["id"])
    empty_cells = [(d, l) for d in dom_ids for l in layer_ids if not matrix[d][l]]
    assert not empty_cells, "12×4 矩阵存在空单元格: %s" % empty_cells

    # ---------- 每层至少 8 条（保证层不是摆设） ----------
    for l in layer_ids:
        n = sum(len(matrix[d][l]) for d in dom_ids)
        assert n >= 8, "层 %s 只有 %d 条问题" % (l, n)

    # ---------- 每条问题至少挂 1 个统计类证据，2 个以上视为充分 ----------
    weak = [q["id"] for q in QUESTIONS if "E1" not in q["ev"] and "E2" not in q["ev"]]
    # 不强制：情景与因果类问题可以只挂 E3/E4/E8

    # ---------- 统计 ----------
    from collections import Counter
    st = Counter(q["status"] for q in QUESTIONS)
    ev_use = Counter(e for q in QUESTIONS for e in q["ev"])
    md_use = Counter(m for q in QUESTIONS for m in q["model"])
    ds_use = Counter(d for q in QUESTIONS for d in q["data"])

    doms = []
    for d in DOMAINS:
        no, name, sub, accent, first = d
        qs = [q for q in QUESTIONS if q["dom"] == no]
        doms.append({
            "no": no, "name": name, "sub": sub, "accent": accent, "first": first,
            "cells": {l: matrix[no][l] for l in layer_ids},
            "counts": {"total": len(qs),
                       **{l: len(matrix[no][l]) for l in layer_ids}},
            "byStatus": {k: sum(1 for q in qs if q["status"] == k)
                         for k in STATUS_META},
            "layerFirst": next(l[4] for l in LAYERS4 if l[0] == "L1"),
        })

    layers = [{"id": l[0], "name": l[1], "sub": l[2], "accent": l[3], "first": l[4],
               "count": sum(len(matrix[d][l[0]]) for d in dom_ids)}
              for l in LAYERS4]

    data = {
        "system": "能源经济分析与决策知识系统",
        "version": VERSION,
        "built": BUILT,
        "layers": layers,
        "domains": doms,
        "questions": QUESTIONS,
        "anchors": [{"id": a[0], "dom": a[1], "name": a[2], "val": a[3],
                     "unit": a[4], "year": a[5], "scope": a[6], "status": a[7],
                     "src": a[8], "url": a[9]} for a in ANCHORS],
        "anchorIssues": ANCHOR_ISSUES,
        "anchorGaps": [{"id": g[0], "item": g[1], "why": g[2], "next": g[3]}
                       for g in ANCHOR_GAPS],
        "anchorTraps": [{"t": t[0], "d": t[1]} for t in ANCHOR_TRAPS],
        "anchorSummary": ANCHOR_SUMMARY,
        "tasks": TASKS,
        "taskSummary": TASK_SUMMARY,
        "taskStandards": [{"name": s[0], "key": s[1], "levels": s[2], "def": s[3]}
                          for s in STANDARDS],
        "taskLevels": [{"id": l[0], "name": l[1], "accent": l[2], "def": l[3]}
                       for l in LEVELS],
        "taskStatus": {k: {"label": v[0], "accent": v[1], "def": v[2]}
                       for k, v in TASK_STATUS.items()},
        "schemaFields": [{"key": f[0], "type": f[1], "def": f[2], "req": f[3]}
                         for f in SCHEMA_FIELDS],
        "coreTables": CORE_TABLES,
        "roadmap": [{"stage": r[0], "name": r[1], "work": r[2], "out": r[3]}
                    for r in ROADMAP],
        "evidence": [{"id": e[0], "name": e[1], "accent": e[2],
                      "ask": e[3], "rules": e[4], "usedBy": ev_use.get(e[0], 0)}
                     for e in EVIDENCE_TIERS],
        "datasets": [{"id": d[0], "name": d[1], "org": d[2], "freq": d[3],
                      "cover": d[4], "caveat": d[5],
                      "url": d[6] if len(d) > 6 else "",
                      "urlKind": d[7] if len(d) > 7 else "none",
                      "urlNote": d[8] if len(d) > 8 else "",
                      "usedBy": ds_use.get(d[0], 0)}
                     for d in DATASETS],
        "models": [{"id": m[0], "name": m[1], "kind": m[2], "use": m[3],
                    "formula": m[4], "limit": m[5], "usedBy": md_use.get(m[0], 0)}
                   for m in MODELS],
        "statusMeta": STATUS_META,
        "matrix": matrix,
        "totals": {
            "domains": 12, "layers": 4, "questions": len(QUESTIONS),
            "datasets": len(DATASETS), "models": len(MODELS),
            "evidence": len(EVIDENCE_TIERS),
            "byStatus": dict(st),
            "indicatorCount": sum(len(q["ind"]) for q in QUESTIONS),
            "cells": 48,
            "weakEvidence": weak,
            "anchors": len(ANCHORS),
            "anchorStatus": dict(validate_anchors()),
            "tasks": TASK_SUMMARY["total"],
            "taskStatus": TASK_SUMMARY["byStatus"],
        },
    }

    # ---------- 桥接碳核算子模块 ----------
    if with_carbon:
        try:
            from framework_core import build_data as build_carbon
            cd = build_carbon()
            data["carbon"] = {
                "version": cd["version"], "built": cd["built"],
                "totals": cd["totals"],
                "layers": [{"no": l["no"], "name": l["name"],
                            "mods": len(l["mods"]),
                            "items": sum(len(m["chips"]) for m in l["mods"])}
                           for l in cd["layers"]],
            }
            assert data["carbon"]["totals"]["items"] == 137
        except Exception as exc:      # 缺 carbon 模块时降级，不阻断主流程
            data["carbon"] = {"error": str(exc)}

    return data


if __name__ == "__main__":
    D = build_energy_data()
    t = D["totals"]
    print("系统: %s  %s / %s" % (D["system"], D["version"], D["built"]))
    print("规模: %d 域 × %d 层 = %d 单元格 / %d 条研究问题 / %d 个指标"
          % (t["domains"], t["layers"], t["cells"], t["questions"], t["indicatorCount"]))
    print("资源: %d 个数据集 / %d 个模型 / %d 层证据"
          % (t["datasets"], t["models"], t["evidence"]))
    print("状态:", t["byStatus"])
    print("\n12×4 矩阵（数字为该单元格问题数）:")
    hdr = "     " + "  ".join("%-6s" % l["name"] for l in D["layers"])
    print(hdr)
    for d in D["domains"]:
        row = "  ".join("%-6d" % d["counts"][l["id"]] for l in D["layers"])
        print("%s %-10s %s | 合计 %d" % (d["no"], d["name"], row, d["counts"]["total"]))
    if "totals" in D.get("carbon", {}):
        c = D["carbon"]["totals"]
        print("\n碳核算子模块: %d 对象 / %d 模块 / %d 参数 / %d 缺口"
              % (c["items"], c["mods"], c["params"], c["gaps"]))
