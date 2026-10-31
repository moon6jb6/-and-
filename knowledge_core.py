# -*- coding: utf-8 -*-
"""知识体系装配与校验。

把 knowledge_p12 / knowledge_p345 的 16 个知识模块，与 energy_questions（研究问题）、
energy_anchors（数据锚点）、energy_meta（数据集/模型/证据）交叉校验后，
组装成「以解释为主体」的 DATA 字典。

设计原则：知识模块是主体，数据/指标/模型/任务只作为支撑材料被引用，不出现在主视图首屏。
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_p12 import MODULES_P12
from knowledge_p345 import MODULES_P345
from energy_questions import QUESTIONS
from energy_anchors import ANCHORS
from energy_meta import DATASETS, MODELS, EVIDENCE_TIERS, DOMAINS

VERSION = "v5"
BUILT = "2026-10-31"

PARTS = [
    ("P1", "能源经济的基本事实", "目前是什么状态", "#38bdf8",
     "先把状态描述清楚。事实部分不做解释，只回答「多少、在哪、怎么变」。"
     "描述的价值取决于口径是否锁定——同一指标换一个口径，结论可以完全相反。"),
    ("P2", "能源经济的运行机制", "为什么这样运行", "#a78bfa",
     "从状态走向机制。机制必须能回答「通过什么渠道、在多长时间内、以多大规模」起作用，"
     "否则只是把相关性换个说法。这一部分是整个体系的理论核心。"),
    ("P3", "能源经济的核心问题", "面临什么问题", "#fbbf24",
     "问题不是「哪里不好」，而是「约束在哪里相互冲突」。"
     "每一个核心问题都是一组无法同时满足的约束，因此不存在纯技术解。"),
    ("P4", "能源经济的分析方法", "如何科学地研究", "#22d3ee",
     "方法回答的不是「怎么算」，而是「凭什么让人相信」。"
     "每种方法都有其成立条件，用错方法的后果比算错数字更严重。"),
    ("P5", "能源经济的政策与未来", "未来如何变化、政策如何调整", "#34d399",
     "情景不是预测。每个未来判断都由一组假设推出，"
     "因此结论的可信度上限等于假设的合理性，报告结论必须同时报告假设。"),
]

SECTION_NAMES = [
    ("concepts", "基本概念", "解释研究对象是什么"),
    ("first", "第一性原理", "解释其底层逻辑"),
    ("mechanism", "运行机制", "解释变量之间如何相互作用"),
    ("history", "发展历程", "解释它是如何形成和演变的"),
    ("status", "当前发展状态", "用真实数据说明现实情况"),
    ("tension", "核心矛盾", "解释目前存在什么问题"),
    ("methods", "分析方法", "解释学界如何研究这个问题"),
    ("future", "政策与未来", "解释可能的发展方向"),
]


def build_knowledge_data():
    modules = MODULES_P12 + MODULES_P345

    part_ids = [p[0] for p in PARTS]
    q_ids = {q["id"] for q in QUESTIONS}
    a_ids = {a[0] for a in ANCHORS}
    dom_ids = {d[0] for d in DOMAINS}

    assert len(modules) == 16, "知识模块数 = %d" % len(modules)
    assert len({m["id"] for m in modules}) == 16, "模块编号重复"

    for m in modules:
        assert m["part"] in part_ids, "未知部分: %s" % m["part"]
        # 八段结构完整性
        assert len(m["concepts"]) >= 2, "%s 基本概念不足" % m["id"]
        assert m["first"].strip(), "%s 缺第一性原理" % m["id"]
        assert len(m["mechanism"]) >= 3, "%s 运行机制不足" % m["id"]
        assert len(m["history"]) >= 3, "%s 发展历程不足" % m["id"]
        assert len(m["status"]) >= 2, "%s 当前状态不足" % m["id"]
        assert len(m["tension"]) >= 2, "%s 核心矛盾不足" % m["id"]
        assert len(m["methods"]) >= 3, "%s 分析方法不足" % m["id"]
        assert m["future"].strip(), "%s 缺政策与未来" % m["id"]
        # 交叉引用必须真实存在
        for d in m["domains"]:
            assert d in dom_ids, "%s 引用未知研究域 %s" % (m["id"], d)
        for q in m["questions"]:
            assert q in q_ids, "%s 引用未知研究问题 %s" % (m["id"], q)
        for s in m["status"]:
            if s[2] is not None:
                assert s[2] in a_ids, "%s 引用未知锚点 %s" % (m["id"], s[2])

    # 每部分至少 2 个模块
    for p in part_ids:
        n = sum(1 for m in modules if m["part"] == p)
        assert n >= 2, "部分 %s 只有 %d 个模块" % (p, n)

    parts_out = []
    for p in PARTS:
        no, name, sub, accent, lead = p
        ms = [{"id": m["id"], "title": m["title"], "sub": m["sub"]}
              for m in modules if m["part"] == no]
        parts_out.append({"id": no, "name": name, "sub": sub, "accent": accent,
                          "lead": lead, "modules": ms, "count": len(ms)})

    anchor_index = {a[0]: a for a in ANCHORS}
    dom_index = {d[0]: d for d in DOMAINS}
    q_index = {q["id"]: q for q in QUESTIONS}

    mods_out = []
    for m in modules:
        mods_out.append({
            "id": m["id"], "part": m["part"], "title": m["title"], "sub": m["sub"],
            "concepts": [{"t": c[0], "d": c[1]} for c in m["concepts"]],
            "first": m["first"],
            "mechanism": [{"t": c[0], "d": c[1]} for c in m["mechanism"]],
            "history": [{"t": c[0], "d": c[1]} for c in m["history"]],
            "status": [{"name": s[0], "val": s[1],
                        "src": s[2] if s[2] else "",
                        "srcTitle": (anchor_index[s[2]][2] if s[2] else ""),
                        "srcUrl": (anchor_index[s[2]][9] if s[2] else "")}
                       for s in m["status"]],
            "tension": [{"t": c[0], "d": c[1]} for c in m["tension"]],
            "methods": [{"t": c[0], "d": c[1]} for c in m["methods"]],
            "future": m["future"],
            "domains": [{"no": d, "name": dom_index[d][1],
                         "accent": dom_index[d][3]} for d in m["domains"]],
            "questions": [{"id": q, "q": q_index[q]["q"],
                           "layer": q_index[q]["layer"],
                           "status": q_index[q]["status"]} for q in m["questions"]],
        })

    return {
        "system": "能源经济发展原理与运行机制知识体系",
        "version": VERSION,
        "built": BUILT,
        "parts": parts_out,
        "modules": mods_out,
        "sectionNames": [{"key": s[0], "name": s[1], "why": s[2]} for s in SECTION_NAMES],
        "totals": {
            "parts": len(PARTS), "modules": len(mods_out),
            "sections": len(SECTION_NAMES),
            "sectionCount": len(mods_out) * len(SECTION_NAMES),
            "questions": len(QUESTIONS),
            "anchors": len(ANCHORS),
            "datasets": len(DATASETS), "models": len(MODELS),
            "evidence": len(EVIDENCE_TIERS),
            "domains": len(DOMAINS),
        },
    }


if __name__ == "__main__":
    D = build_knowledge_data()
    t = D["totals"]
    print("系统: %s  %s / %s" % (D["system"], D["version"], D["built"]))
    print("%d 个部分 / %d 个知识模块 / %d 段结构 = %d 段解释"
          % (t["parts"], t["modules"], t["sections"], t["sectionCount"]))
    print("支撑材料: %d 研究问题 / %d 数据锚点 / %d 数据集 / %d 模型 / %d 层证据"
          % (t["questions"], t["anchors"], t["datasets"], t["models"], t["evidence"]))
    print()
    for p in D["parts"]:
        print("%s %s（%d）" % (p["id"], p["name"], p["count"]))
        for m in p["modules"]:
            print("    %s %s —— %s" % (m["id"], m["title"], m["sub"]))
