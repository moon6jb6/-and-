# -*- coding: utf-8 -*-
"""
MISSING_DATA_SPEC —— 碳核算框架缺失数据补齐任务单
=================================================================
用途：把本文件交给另一个 AI / 检索代理，要求其按 FILL_RULES 填充
      MISSING_DATA 中每个条目的 value / quote / url / as_of / confidence。

对应文档：《能源—碳—经济核算框架：数据支撑手册》第五部分「待核清单」
对应表格：《城市碳核算与政策分析框架》137 行总表
生成日期：2026-02

-----------------------------------------------------------------
FILL_RULES（把这整段也给对方）
-----------------------------------------------------------------
1. 【只填能逐字引用的】
   value 必须能在 quote 字段里逐字对应到信息源。找不到原文就留 None。
2. 【找不到就说找不到】
   无法取得一手来源时，将 status 设为 "not_found"，并在 notes 说明卡在哪里。
   ★ 严禁估算、严禁"根据经验推断"、严禁给一个"看起来合理"的数。
3. 【禁止用二手解读代替原文】
   新闻报道、券商研报、博客、AI 摘要都不能作为 fill 依据。
   source_priority="primary" 的条目必须来自标准/法规/政府公告原文。
4. 【必须回答三件事】
   数值是什么？出处是哪份文件的哪张表/哪一条？该数据对应哪一年？
5. 【单位必须与 unit 字段一致】
   若原文用不同单位，换算后在 notes 写明换算过程。
6. 【区分"没有数据"与"数据不公开"】
   数据不公开 → status="restricted"，并说明申请渠道。
   确实没发布 → status="not_found"。
7. 【多值条目】
   values 字段用于分省/分行业/分气体的字典型数据，一个 key 一个值。
8. 【填写完成后自检】
   运行本文件 `python missing_data_spec.py`，
   它会校验必填字段是否齐全，并打印覆盖率。
-----------------------------------------------------------------
"""

# ================================================================
# 第一部分：待填数据
# ================================================================
MISSING_DATA = {

    # ---------------- G1 温室气体特征参数 ----------------
    "GWP_AR6_FGAS": {
        "category": "温室气体参数",
        "row_refs": [41, 45, 127],
        "item": "IPCC AR6 各含氟气体 GWP100 精确值",
        "question": ("IPCC AR6 WG1 第7章表7.15 中，以下气体的 GWP100 精确值分别是多少："
                     "SF6、NF3、CF4、C2F6、HFC-23、HFC-32、HFC-125、HFC-134a、"
                     "HFC-143a、HFC-152a、PFC-14、PFC-116？"),
        "unit": "无量纲（CO2=1）",
        "source_hint": "IPCC AR6 WG1 Chapter 7, Table 7.15 (Radiative efficiencies and GWP values)",
        "source_priority": "primary",
        "granularity": "气体",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "GWP_AR6_CH4_SPLIT": {
        "category": "温室气体参数",
        "row_refs": [39, 40, 45, 127],
        "item": "AR6 甲烷 GWP100 三分类官方表述",
        "question": ("AR6 对化石源 CH4、非化石源 CH4、未区分来源 CH4 的 GWP100 分别是多少？"
                     "请给出 IPCC 原文中对这三者的定义措辞。"),
        "unit": "无量纲",
        "source_hint": "IPCC AR6 WG1 Table 7.15 及脚注",
        "source_priority": "primary",
        "granularity": "气体",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "GWP_AR6_GWP20": {
        "category": "温室气体参数",
        "row_refs": [45, 65, 136],
        "item": "AR6 GWP20 值（用于短期气候效益评估）",
        "question": ("AR6 中 CH4（三种分类）、N2O、SF6、CF4 的 GWP20 分别是多少？"
                     "做短期气候效益评估时必须用 GWP20 并声明。"),
        "unit": "无量纲",
        "source_hint": "IPCC AR6 WG1 Table 7.15",
        "source_priority": "primary",
        "granularity": "气体",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "GWP_AR5_FGAS": {
        "category": "温室气体参数",
        "row_refs": [41, 45],
        "item": "AR5 含氟气体 GWP100（历史序列一致性）",
        "question": ("AR5 中 SF6、NF3、CF4、C2F6 的 GWP100 分别是多少？"
                     "需要它是因为历史清单可能按 AR5 编制，重算时要做版本对照。"),
        "unit": "无量纲",
        "source_hint": "IPCC AR5 WG1 Chapter 8, Table 8.7",
        "source_priority": "primary",
        "granularity": "气体",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    # ---------------- G2 燃料与能源排放因子 ----------------
    "EF_FUEL_PROVINCIAL": {
        "category": "能源排放因子",
        "row_refs": [3, 4, 5, 13],
        "item": "中国官方分品种燃料排放因子（本地化值）",
        "question": ("《省级温室气体清单编制指南（试行）》能源活动章节中，"
                     "原煤、洗精煤、其他洗煤、焦炭、原油、汽油、煤油、柴油、燃料油、"
                     "液化石油气、天然气、焦炉煤气的【低位发热量】【单位热值含碳量】"
                     "【碳氧化率】分别是多少？请逐项给出，并注明表号。"),
        "unit": "低位发热量 GJ/t 或 GJ/10^3m3；含碳量 tC/TJ；氧化率 无量纲",
        "source_hint": "《省级温室气体清单编制指南（试行）》（国家发改委应对气候变化司）能源活动部分",
        "source_priority": "primary",
        "granularity": "燃料品种",
        "value": None,
        "values": {
            "原煤": {"NCV": None, "CC": None, "OX": None},
            "洗精煤": {"NCV": None, "CC": None, "OX": None},
            "焦炭": {"NCV": None, "CC": None, "OX": None},
            "原油": {"NCV": None, "CC": None, "OX": None},
            "汽油": {"NCV": None, "CC": None, "OX": None},
            "柴油": {"NCV": None, "CC": None, "OX": None},
            "燃料油": {"NCV": None, "CC": None, "OX": None},
            "液化石油气": {"NCV": None, "CC": None, "OX": None},
            "天然气": {"NCV": None, "CC": None, "OX": None},
            "焦炉煤气": {"NCV": None, "CC": None, "OX": None},
        },
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "EF_HEAT": {
        "category": "能源排放因子",
        "row_refs": [6, 16, 17, 58],
        "item": "热力排放因子",
        "question": ("外购热力的 CO2 排放因子，中国是否有官方发布值？"
                     "若无，地方/行业常用值是多少（tCO2/GJ）？请给出处。"),
        "unit": "tCO2/GJ",
        "source_hint": "GB/T 32151 系列行业核算指南；地方碳市场核算指南；地方供热统计",
        "source_priority": "primary",
        "granularity": "全国/地方",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    # ---------------- G3 工业过程排放因子 ----------------
    "EF_CEMENT_CLINKER": {
        "category": "工业过程因子",
        "row_refs": [20, 54],
        "item": "水泥熟料工艺排放因子（中国官方）",
        "question": ("水泥熟料碳酸盐分解的 CO2 排放因子，中国官方核算指南取多少"
                     "（tCO2/t 熟料）？是固定缺省值还是按实测 CaO 含量计算？"
                     "水泥碳化（使用期+废弃期）吸收量的官方估算方法是什么？"),
        "unit": "tCO2/t 熟料",
        "source_hint": "《水泥行业温室气体排放核算与报告要求》GB/T 32151.x；全国碳市场水泥行业核算指南",
        "source_priority": "primary",
        "granularity": "行业",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "EF_STEEL": {
        "category": "工业过程因子",
        "row_refs": [19],
        "item": "钢铁各工序排放因子与吨钢排放",
        "question": ("钢铁长流程各工序（焦化、烧结、球团、炼铁、炼钢、轧钢）的"
                     "单位产品 CO2 排放因子，中国官方指南取多少？"
                     "吨粗钢（BF-BOF / EAF）的行业典型排放强度范围是多少？"),
        "unit": "tCO2/t 产品",
        "source_hint": "GB/T 32151 钢铁行业；《钢铁行业温室气体排放核算方法与报告指南》；中钢协年度报告",
        "source_priority": "primary",
        "granularity": "工序",
        "value": None,
        "values": {"焦化": None, "烧结": None, "球团": None,
                   "炼铁": None, "炼钢": None, "轧钢": None,
                   "吨粗钢_BF_BOF": None, "吨粗钢_EAF": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "EF_ALUMINIUM": {
        "category": "工业过程因子",
        "row_refs": [23, 41],
        "item": "电解铝排放因子与阳极效应含氟气体",
        "question": ("电解铝吨铝 CO2 排放因子；阳极效应产生 CF4 和 C2F6 的"
                     "排放因子（kg/t 铝）官方取值是多少？中国铝行业平均阳极效应系数？"),
        "unit": "tCO2/t 铝；kg CF4/t 铝；kg C2F6/t 铝",
        "source_hint": "GB/T 32151 有色金属行业；全国碳市场铝冶炼行业核算指南（2025年扩围）",
        "source_priority": "primary",
        "granularity": "行业",
        "value": None,
        "values": {"tCO2_per_t_Al": None, "CF4_kg_per_t": None,
                   "C2F6_kg_per_t": None, "阳极效应系数": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "EF_OTHER_PROCESS": {
        "category": "工业过程因子",
        "row_refs": [21, 22, 23],
        "item": "框架缺失的工业过程品种排放因子",
        "question": ("以下品种的工艺排放因子分别是多少：石灰、玻璃（碳酸钠分解）、"
                     "纯碱、电石、硝酸（N2O）、己二酸（N2O）、黄磷、多晶硅、铁合金、炭黑？"
                     "请给出中国官方指南或行业标准取值。"),
        "unit": "tCO2（或 tCO2e）/t 产品",
        "source_hint": "GB/T 32151 系列；《工业其他行业企业温室气体排放核算方法与报告指南》",
        "source_priority": "primary",
        "granularity": "产品",
        "value": None,
        "values": {"石灰": None, "玻璃": None, "纯碱": None, "电石": None,
                   "硝酸_N2O": None, "己二酸_N2O": None, "黄磷": None,
                   "多晶硅": None, "铁合金": None, "炭黑": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G4 碳市场基准与规则 ----------------
    "ETS_BENCHMARKS": {
        "category": "碳市场规则",
        "row_refs": [69, 72, 73],
        "item": "各行业配额分配基准值",
        "question": ("全国碳市场发电、钢铁、水泥、铝冶炼四个行业的"
                     "【排放强度基准值】分别是多少（各自的单位是什么）？"
                     "2024年度与2025年度方案是否不同？"),
        "unit": "按行业定（如 tCO2/MWh、tCO2/t 产品）",
        "source_hint": ("生态环境部《2024、2025年度全国碳排放权交易市场钢铁、水泥、铝冶炼行业"
                        "配额总量和分配方案》；发电行业年度配额方案"),
        "source_priority": "primary",
        "granularity": "行业",
        "value": None,
        "values": {"发电": None, "钢铁": None, "水泥": None, "铝冶炼": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "ETS_ALLOCATION_RULES": {
        "category": "碳市场规则",
        "row_refs": [72, 74],
        "item": "配额有偿分配比例与结转规则",
        "question": ("目前有偿分配的具体比例是否已公布？各行业差异化比例是多少？"
                     "配额跨期结转（banking）的具体规则、限制比例和有效期限是什么？"),
        "unit": "%；规则条文",
        "source_hint": "《关于推进绿色低碳转型 加强全国碳市场建设的意见》；年度配额方案；配额结转规定",
        "source_priority": "primary",
        "granularity": "制度",
        "value": None,
        "values": {"有偿分配比例": None, "结转规则": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G5 农业排放因子 ----------------
    "EF_AGRICULTURE": {
        "category": "农业排放因子",
        "row_refs": [32, 33, 34],
        "item": "中国农业 CH4 / N2O 排放因子",
        "question": ("（1）稻田 CH4 排放因子的中国官方取值（分区域/分水分管理），"
                     "单位 kg CH4/ha/日 或 kg CH4/ha/季？"
                     "（2）反刍动物肠道发酵 CH4 排放因子（分牛/羊，中国分区）？"
                     "（3）畜禽粪污管理 CH4 与 N2O 排放因子？"
                     "（4）农田 N2O 直接排放因子 EF1 与间接排放系数（挥发、淋洗）中国官方值？"),
        "unit": "kg CH4/ha/季；kg CH4/头/年；kg N2O-N/kg N",
        "source_hint": "《省级温室气体清单编制指南（试行）》农业活动部分；IPCC 2006 第4卷 第10/11章",
        "source_priority": "primary",
        "granularity": "区域/畜种",
        "value": None,
        "values": {"稻田CH4": None, "肠道发酵_牛": None, "肠道发酵_羊": None,
                   "粪污管理_CH4": None, "粪污管理_N2O": None,
                   "农田N2O_EF1": None, "N2O挥发系数": None, "N2O淋洗系数": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "EF_CROP_RESIDUE_BURNING": {
        "category": "农业排放因子",
        "row_refs": [32, 33],
        "item": "秸秆露天焚烧排放（框架缺项）",
        "question": ("秸秆露天焚烧的 CH4、N2O、黑碳排放因子，中国取值多少？"
                     "秸秆焚烧比例（焚烧量占秸秆产量比例）官方或权威估计是多少？"),
        "unit": "g/kg 秸秆；%",
        "source_hint": "IPCC 2006 第4卷 第2章；《省级清单指南》；农业农村部秸秆综合利用相关统计",
        "source_priority": "primary",
        "granularity": "全国/区域",
        "value": None,
        "values": {"CH4": None, "N2O": None, "黑碳": None, "焚烧比例": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G6 废弃物 ----------------
    "EF_WASTE": {
        "category": "废弃物排放因子",
        "row_refs": [42, 43, 44],
        "item": "废弃物处理 CH4 / N2O 参数",
        "question": ("（1）生活垃圾填埋的 DOC、DOCf、F、氧化因子、CH4 收集率中国取值？"
                     "（2）生活垃圾焚烧的化石碳比例（%，中国实测）与焚烧排放因子？"
                     "（3）城镇污水 CH4 与 N2O 排放因子（按 BOD/COD、按氮负荷）？"
                     "（4）餐厨垃圾、堆肥、露天焚烧的排放因子？"),
        "unit": "多种（见 notes）",
        "source_hint": "《省级温室气体清单指南》废弃物部分；IPCC 2006 第5卷；住建部城乡建设统计年鉴",
        "source_priority": "primary",
        "granularity": "处理方式",
        "value": None,
        "values": {"DOC": None, "DOCf": None, "F": None, "氧化因子": None,
                   "CH4收集率": None, "垃圾焚烧化石碳比例": None,
                   "污水CH4因子": None, "污水N2O因子": None,
                   "堆肥CH4": None, "堆肥N2O": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G7 逸散排放 ----------------
    "EF_FUGITIVE": {
        "category": "逸散排放因子",
        "row_refs": [39, 40, 12, 11],
        "item": "煤矿与油气系统甲烷逸散因子",
        "question": ("（1）井工煤矿 CH4 排放因子（m3 CH4/t 煤）按瓦斯等级分档的取值？"
                     "（2）油气系统逸散排放因子（按井口、储罐、管道、压缩站的设备计数法参数）？"
                     "（3）火炬燃烧效率与放空排放因子？"),
        "unit": "m3 CH4/t 煤；kg CH4/设备/年；无量纲",
        "source_hint": "《省级温室气体清单指南》逃逸排放部分；IPCC 2006 第2卷；中国煤矿瓦斯抽采利用统计",
        "source_priority": "primary",
        "granularity": "设施类型",
        "value": None,
        "values": {"煤矿CH4_高瓦斯": None, "煤矿CH4_低瓦斯": None,
                   "油气逸散_井口": None, "储罐": None, "管道": None,
                   "火炬效率": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "EF_REFRIGERANT": {
        "category": "逸散排放因子",
        "row_refs": [28, 41],
        "item": "制冷剂充注量与泄漏率",
        "question": ("分行业（家用空调、商用空调、冷库、汽车空调）的"
                     "制冷剂初始充注量（kg/台）和年泄漏率（%）是多少？"
                     "回收率与报废释放比例？"),
        "unit": "kg/台；%/年",
        "source_hint": "IPCC 2006 第3卷第7章；中国家电/制冷行业统计；《蒙特利尔议定书》基加利修正案履约报告",
        "source_priority": "primary",
        "granularity": "设备类型",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    # ---------------- G8 土地、森林与蓝碳 ----------------
    "CARBON_DENSITY_LULUCF": {
        "category": "土地利用碳参数",
        "row_refs": [35, 36, 37, 38, 46, 56],
        "item": "森林/草地/农田/湿地碳密度与生物量参数",
        "question": ("（1）分树种的生物量扩展因子 BEF、含碳率、根茎比？"
                     "（2）六大土地利用类型的植被与土壤碳密度（tC/ha）中国取值？"
                     "（3）森林蓄积量—生物量转换参数？"),
        "unit": "tC/ha；无量纲",
        "source_hint": "《省级温室气体清单指南》土地利用变化与林业部分；全国森林资源清查；IPCC 2006 第4卷",
        "source_priority": "primary",
        "granularity": "树种/地类",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "BLUE_CARBON": {
        "category": "蓝碳参数",
        "row_refs": [36, 46],
        "item": "滨海湿地碳汇参数（框架缺项，政策关键）",
        "question": ("（1）盐沼、海草床、红树林的植被与土壤碳密度（tC/ha）？"
                     "（2）碳埋藏速率（tC/ha/年）？"
                     "（3）CCER 盐沼/海草床/红树林方法学中的基准线与默认参数取值？"),
        "unit": "tC/ha；tC/ha/年",
        "source_hint": ("生态环境部《温室气体自愿减排项目方法学：滨海盐沼植被修复》、"
                        "《海草床植被修复》、《红树林营造》；自然资源部海洋碳汇相关标准"),
        "source_priority": "primary",
        "granularity": "生态系统类型",
        "value": None,
        "values": {"盐沼_碳密度": None, "盐沼_埋藏速率": None,
                   "海草床_碳密度": None, "海草床_埋藏速率": None,
                   "红树林_碳密度": None, "红树林_埋藏速率": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G9 活动数据 ----------------
    "CITY_ENERGY_BALANCE": {
        "category": "活动数据",
        "row_refs": [2, 3, 4, 5, 6, 130],
        "item": "城市级能源平衡表（多数城市不存在）",
        "question": ("中国是否有官方发布的【城市级】能源平衡表？"
                     "若无，用省级平衡表向下拆分或自下而上编制的标准方法是哪个文件规定的？"
                     "地级市能源消费数据在《中国城市统计年鉴》中的字段口径是什么？"),
        "unit": "万tce / 实物量",
        "source_hint": "《中国能源统计年鉴》能源平衡表；《中国城市统计年鉴》；省级统计年鉴",
        "source_priority": "primary",
        "granularity": "城市",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "ACTIVITY_TRANSPORT": {
        "category": "活动数据",
        "row_refs": [29, 30, 31],
        "item": "交通活动数据（框架关键缺项）",
        "question": ("（1）中国分车型年均行驶里程（VKT，km/年）官方或权威估计？"
                     "（2）非道路移动机械保有量与年工作小时？"
                     "（3）港口船舶靠泊排放的核算方法与活动数据来源？"
                     "（4）航空 LTO 循环次数与起降排放因子？"
                     "（5）城市轨道交通能耗强度（kWh/人公里）？"),
        "unit": "km/年；台；次；kWh/人km",
        "source_hint": "交通运输部统计公报；《中国交通年鉴》；民航局统计；港口统计年鉴；IPCC 2006 第3卷",
        "source_priority": "primary",
        "granularity": "车/船/机类型",
        "value": None,
        "values": {"VKT_汽油车": None, "VKT_柴油车": None, "VKT_电动车": None,
                   "非道路机械保有量": None, "非道路年工作小时": None,
                   "船舶排放因子": None, "航空LTO因子": None,
                   "地铁能耗强度": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "ACTIVITY_INDUSTRY_CITY": {
        "category": "活动数据",
        "row_refs": [19, 20, 21, 22, 23, 24],
        "item": "城市级工业产品产量",
        "question": ("地级市层面的粗钢、水泥熟料、电解铝、合成氨、电石等"
                     "主要高耗能产品产量，官方统计口径在哪里获取？"
                     "分企业数据是否可通过排污许可平台获得？"),
        "unit": "万t",
        "source_hint": "《中国城市统计年鉴》；各省统计年鉴；全国排污许可证管理信息平台",
        "source_priority": "primary",
        "granularity": "城市/产品",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "ACTIVITY_MISSING_SECTORS": {
        "category": "活动数据",
        "row_refs": [25, 28, 29],
        "item": "框架缺失行业的活动数据",
        "question": ("（1）中国数据中心总能耗与分区域分布（亿kWh，近年）？"
                     "（2）分气候区公共建筑单位面积能耗强度（kWh/m2/年）？"
                     "（3）半导体/显示面板行业 NF3、CF4 使用量？"),
        "unit": "亿kWh；kWh/m2；t",
        "source_hint": "国家能源局/工信部数据中心相关文件；《中国建筑节能年度发展研究报告》；行业协会统计",
        "source_priority": "primary",
        "granularity": "行业/区域",
        "value": None,
        "values": {"数据中心能耗": None, "公共建筑EUI_严寒": None,
                   "公共建筑EUI_夏热冬冷": None, "NF3使用量": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G10 政策与制度参数 ----------------
    "CBAM_PARAMS": {
        "category": "政策参数",
        "row_refs": [110, 122],
        "item": "CBAM 实施细则参数（框架缺项，出口城市关键）",
        "question": ("（1）CBAM 覆盖六大类产品的【默认排放值】分别是多少？"
                     "（2）2026–2034 年免费配额递减系数（CBAM factor）的时间表？"
                     "（3）间接排放是否计入、从哪一年开始计入？"
                     "（4）中国碳市场已付碳价如何抵扣（抵扣计算规则）？"),
        "unit": "tCO2e/t 产品；%；规则条文",
        "source_hint": ("Regulation (EU) 2023/956（CBAM 基础条例）及其实施条例/"
                        "Implementing Regulation；欧盟委员会 CBAM 官方页面"),
        "source_priority": "primary",
        "granularity": "产品类别",
        "value": None,
        "values": {"水泥默认值": None, "钢铁默认值": None, "铝默认值": None,
                   "化肥默认值": None, "氢默认值": None,
                   "免费配额递减时间表": None, "间接排放规则": None,
                   "中国碳价抵扣规则": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "CCER_PARAMS": {
        "category": "政策参数",
        "row_refs": [79, 88, 89],
        "item": "CCER 抵消比例与各方法学默认参数",
        "question": ("（1）重点排放单位可使用 CCER 抵消其配额清缴的比例上限是多少（%），"
                     "历年规则是否变化？"
                     "（2）各 CCER 方法学的基准线排放因子与默认参数取值？"
                     "（3）2025年12项方法学的正式文本编号与发布文号？"),
        "unit": "%；参数值；文号",
        "source_hint": "全国碳市场年度履约通知；生态环境部发布的方法学正式文本",
        "source_priority": "primary",
        "granularity": "制度/方法学",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "GREEN_CERTIFICATE_RULES": {
        "category": "政策参数",
        "row_refs": [6, 58],
        "item": "绿证（GEC）与间接排放扣减规则（口径关键）",
        "question": ("（1）绿证核发与核销的官方规则文件是什么？"
                     "（2）企业核算间接排放时，绿证能否扣减、扣减多少、是否需要核销？"
                     "（3）与电力二氧化碳排放因子公告中"
                     "『不包括市场化交易的非化石能源电量』口径如何衔接？"),
        "unit": "规则条文；%",
        "source_hint": ("《关于做好可再生能源绿色电力证书全覆盖工作促进可再生能源电力消费的通知》；"
                        "电力二氧化碳排放因子公告；全国碳市场相关规则"),
        "source_priority": "primary",
        "granularity": "制度",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "TAX_PARAMS": {
        "category": "政策参数",
        "row_refs": [105, 106],
        "item": "现行相关税种税率（中国无碳税）",
        "question": ("（1）环境保护税的税目与税率（大气污染物、水污染物、固体废物）？"
                     "（2）成品油消费税税率（汽油、柴油）？"
                     "（3）资源税中煤炭、原油、天然气的税率？"
                     "（4）若做碳税情景，学界常用的税率假设区间是多少（需注明文献）？"),
        "unit": "元/吨；元/升；%",
        "source_hint": "《环境保护税法》；《消费税暂行条例》；《资源税法》；碳税情景需引学术文献",
        "source_priority": "primary",
        "granularity": "税种",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    "DUAL_CONTROL_RULES": {
        "category": "政策参数",
        "row_refs": [71],
        "item": "能耗双控转向碳排放双控的具体指标",
        "question": ("《加快构建碳排放双控制度体系工作方案》中，"
                     "碳排放双控的具体指标体系是什么？"
                     "『新增可再生能源消费不纳入能耗总量控制』的具体规则？"
                     "原料用能如何扣除？"),
        "unit": "规则条文；%",
        "source_hint": "《加快构建碳排放双控制度体系工作方案》（国务院办公厅）；相关配套文件",
        "source_priority": "primary",
        "granularity": "制度",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },

    # ---------------- G11 经济参数 ----------------
    "SCC_CHINA": {
        "category": "经济参数",
        "row_refs": [116, 119, 136],
        "item": "碳的社会成本 SCC",
        "question": ("中国官方或权威学术估计的碳的社会成本（元/tCO2）是多少？"
                     "用的贴现率与时间跨度是什么？国际参照（如美国 IWG/EPA）最新值是多少？"),
        "unit": "元/tCO2；USD/tCO2",
        "source_hint": "国内核心期刊（经济研究/中国工业经济等）SCC 估计；美国 EPA/IWG SCC 报告",
        "source_priority": "academic",
        "granularity": "全国",
        "value": None,
        "values": {"中国SCC": None, "贴现率": None, "国际参照": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "ELASTICITIES": {
        "category": "经济参数",
        "row_refs": [106, 113, 114, 134],
        "item": "能源需求弹性与回弹效应（框架缺项）",
        "question": ("（1）中国能源需求价格弹性（分部门：工业、居民、交通）的可靠估计？"
                     "（2）能源回弹效应（rebound effect）的中国实证估计值？"
                     "（3）能源需求收入弹性？"),
        "unit": "无量纲",
        "source_hint": "国内核心期刊实证研究；需注明样本期与识别方法",
        "source_priority": "academic",
        "granularity": "部门",
        "value": None,
        "values": {"工业价格弹性": None, "居民价格弹性": None,
                   "交通价格弹性": None, "回弹效应": None, "收入弹性": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "COBENEFIT": {
        "category": "经济参数",
        "row_refs": [116, 119, 133],
        "item": "减污降碳协同效益（框架最大经济缺口）",
        "question": ("（1）CO2 减排与 PM2.5/SO2/NOx 减排的协同系数（每吨 CO2 减排协同减少多少污染物）？"
                     "（2）健康效益货币化价值（VSL，统计生命价值，中国取值）？"
                     "（3）每吨污染物减排的健康损失避免价值？"),
        "unit": "kg 污染物/tCO2；元/人；元/t 污染物",
        "source_hint": "中国环境规划院相关研究；生态环境部《减污降碳协同增效实施方案》；VSL 中国实证文献",
        "source_priority": "academic",
        "granularity": "全国/区域",
        "value": None,
        "values": {"协同系数_PM25": None, "协同系数_SO2": None,
                   "协同系数_NOx": None, "VSL": None, "健康效益价值": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "TECH_COST_PARAMS": {
        "category": "经济参数",
        "row_refs": [116, 118, 134, 136],
        "item": "技术成本与学习率",
        "question": ("（1）光伏、风电、储能、电解槽、CCUS、DACCS 的单位投资成本与学习率？"
                     "（2）中国各技术边际减排成本（元/tCO2）区间？"
                     "（3）CCUS 全链条成本（捕集+运输+封存）分行业取值？"),
        "unit": "元/kW；元/tCO2；%",
        "source_hint": "IRENA/BNEF 年度报告；中国电力企业联合会；CCUS 行业协会；国内核心期刊",
        "source_priority": "industry",
        "granularity": "技术",
        "value": None,
        "values": {"光伏学习率": None, "风电学习率": None, "储能成本": None,
                   "电解槽成本": None, "CCUS成本": None, "DACCS成本": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "CARBON_PASS_THROUGH": {
        "category": "经济参数",
        "row_refs": [109, 110],
        "item": "碳价传导率与就业冲击",
        "question": ("（1）碳价向产品价格的传导率（pass-through rate）中国实证估计？"
                     "（2）碳市场/碳税对就业的影响系数（分行业）？"
                     "（3）能源贫困的界定指标与中国发生率？"),
        "unit": "%；人/万tCO2；%",
        "source_hint": "国内核心期刊实证研究；需注明样本期与方法",
        "source_priority": "academic",
        "granularity": "行业/区域",
        "value": None,
        "values": {"传导率": None, "就业冲击系数": None, "能源贫困率": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    # ---------------- G12 模型与预算参数 ----------------
    "CARBON_BUDGET": {
        "category": "模型参数",
        "row_refs": [66, 61],
        "item": "剩余碳预算与 TCRE",
        "question": ("（1）IPCC AR6 给出的 1.5℃ 与 2℃ 剩余碳预算（从哪一年起算、多少 GtCO2）？"
                     "（2）TCRE 取值区间（℃/1000GtCO2）？"
                     "（3）中国实现碳中和对应的累计排放上限估计？"),
        "unit": "GtCO2；℃/1000GtCO2",
        "source_hint": "IPCC AR6 WG1 SPM / Chapter 5；中国碳中和路径研究",
        "source_priority": "primary",
        "granularity": "全球/国家",
        "value": None,
        "values": {"剩余碳预算_1.5C": None, "剩余碳预算_2C": None, "TCRE": None},
        "quote": None, "url": None, "as_of": None, "confidence": None,
        "status": None, "notes": None,
    },

    "PRODUCT_CARBON_STORAGE": {
        "category": "模型参数",
        "row_refs": [47, 53, 56],
        "item": "产品碳储存与释放",
        "question": ("塑料、木材、化工品中碳的储存期限（半衰期）与最终释放比例？"
                     "IPCC 废弃物卷中关于产品碳储存的核算规则？"),
        "unit": "年；%",
        "source_hint": "IPCC 2006 第5卷（废弃物）产品碳储存相关章节；生命周期评价文献",
        "source_priority": "primary",
        "granularity": "产品类别",
        "value": None, "values": None, "quote": None, "url": None,
        "as_of": None, "confidence": None, "status": None, "notes": None,
    },
}


# ================================================================
# 第二部分：已核实（勿重复检索）
# ================================================================
ALREADY_VERIFIED = {
    "_说明": "以下数据已取得官方一手来源并交叉校验，对方无需再查。若对方发现错误请指出。",
    "GWP_AR6_CH4_N2O": {
        "CH4_化石源_GWP100": 29.8,
        "CH4_非化石源_GWP100": 27.0,
        "CH4_未区分_GWP100": 27.9,
        "N2O_GWP100": 273,
        "status": "已核实，来源 IPCC AR6",
    },
    "ELECTRICITY_CO2_FACTOR_2022": {
        "全国": 0.5366,
        "全国_不含市场化交易非化石电量": 0.5856,
        "全国_化石能源电力": 0.8325,
        "华北": 0.6776, "东北": 0.5564, "华东": 0.5617, "华中": 0.5395,
        "西北": 0.5857, "南方": 0.3869, "西南": 0.2268,
        "省级": {
            "北京": 0.5580, "天津": 0.7041, "河北": 0.7252, "山西": 0.7096,
            "内蒙古": 0.6849, "辽宁": 0.5626, "吉林": 0.4932, "黑龙江": 0.5368,
            "上海": 0.5849, "江苏": 0.5978, "浙江": 0.5153, "安徽": 0.6782,
            "福建": 0.4092, "江西": 0.5752, "山东": 0.6410, "河南": 0.6058,
            "湖北": 0.4364, "湖南": 0.4900, "广东": 0.4403, "广西": 0.4044,
            "海南": 0.4184, "重庆": 0.5227, "四川": 0.1404, "贵州": 0.4989,
            "云南": 0.1073, "陕西": 0.6558, "甘肃": 0.4772, "青海": 0.1567,
            "宁夏": 0.6423, "新疆": 0.6231,
        },
        "unit": "kgCO2/kWh",
        "source": "公告 2024年 第33号",
    },
    "ELECTRICITY_FOOTPRINT_FACTOR": {
        "2023_全国平均": 0.6205,
        "2024_全国平均": 0.5777,
        "2023_输配电_不含线损": 0.0036,
        "2024_输配电_不含线损": 0.0046,
        "unit": "kgCO2e/kWh",
        "source": "公告 2025年 第19号",
    },
    "CARBON_MARKET_2025": {
        "纳管企业": 3378, "发电": 2087, "钢铁": 232, "水泥": 962, "铝冶炼": 97,
        "交易日": 243,
        "累计成交量_亿吨": 8.65, "累计成交额_亿元": 576.63,
        "2025成交量_亿吨": 2.35, "2025成交额_亿元": 146.30,
        "2025年底收盘价_元每吨": 74.63, "2025均价_元每吨": 62.36,
        "2024清缴总量_亿吨": 81.94, "清缴完成率_百分比": 99.99,
        "source": "生态环境部 2026-01-01",
    },
    "CCER_2025": {
        "已登记项目": 33, "已登记减排量_万吨": 1776.37,
        "累计成交量_万吨": 921.94, "累计成交额_亿元": 6.50,
        "全年均价_元每吨": 70.76, "累计开户": 6106, "新增方法学": 12,
        "source": "生态环境部 2026-01-01",
    },
}


# ================================================================
# 第三部分：自检与摘要
# ================================================================
REQUIRED_FIELDS = ["category", "row_refs", "item", "question", "unit",
                   "source_hint", "source_priority", "granularity",
                   "value", "values", "quote", "url", "as_of",
                   "confidence", "status", "notes"]

VALID_STATUS = {None, "filled", "partial", "not_found", "restricted"}


def validate():
    """校验条目结构完整性；返回 (ok, problems)。"""
    problems = []
    for key, spec in MISSING_DATA.items():
        missing = [f for f in REQUIRED_FIELDS if f not in spec]
        if missing:
            problems.append("%s: 缺字段 %s" % (key, missing))
        if spec.get("status") not in VALID_STATUS:
            problems.append("%s: status 非法 -> %r" % (key, spec.get("status")))
        if spec.get("status") == "filled":
            if spec.get("value") is None and not spec.get("values"):
                problems.append("%s: 标了 filled 却没有 value/values" % key)
            if not spec.get("quote") or not spec.get("url"):
                problems.append("%s: 标了 filled 但缺 quote 或 url" % key)
            if not spec.get("as_of"):
                problems.append("%s: 标了 filled 但缺 as_of（数据年份）" % key)
    return (len(problems) == 0, problems)


def summary():
    total = len(MISSING_DATA)
    done = sum(1 for s in MISSING_DATA.values() if s.get("status") == "filled")
    partial = sum(1 for s in MISSING_DATA.values() if s.get("status") == "partial")
    nf = sum(1 for s in MISSING_DATA.values() if s.get("status") == "not_found")
    restricted = sum(1 for s in MISSING_DATA.values() if s.get("status") == "restricted")
    todo = total - done - partial - nf - restricted

    print("=" * 68)
    print("  缺失数据补齐任务单 —— 进度")
    print("=" * 68)
    print("  总条目          : %d" % total)
    print("  已填(filled)    : %d" % done)
    print("  部分(partial)   : %d" % partial)
    print("  未找到(not_found): %d" % nf)
    print("  不公开(restricted): %d" % restricted)
    print("  待办            : %d" % todo)
    print("  覆盖率          : %.1f%%" % (100.0 * done / total if total else 0))
    print("=" * 68)

    print("\n按类别统计：")
    cats = {}
    for spec in MISSING_DATA.values():
        cats.setdefault(spec["category"], [0, 0])
        cats[spec["category"]][0] += 1
        if spec.get("status") == "filled":
            cats[spec["category"]][1] += 1
    for cat in sorted(cats):
        t, d = cats[cat]
        print("  %-18s %2d 条 (已填 %d)" % (cat, t, d))

    print("\n涉及的行号覆盖：")
    rows = set()
    for spec in MISSING_DATA.values():
        rows.update(spec["row_refs"])
    print("  共 %d 个不同行号，范围 %d-%d" % (len(rows), min(rows), max(rows)))
    uncovered = sorted(set(range(1, 138)) - rows)
    print("  未涉及补充的其余行号数：%d（这些行不属于缺失数据类，"
          "或已在 ALREADY_VERIFIED 中给出）" % len(uncovered))


if __name__ == "__main__":
    summary()
    print("\n结构校验：")
    ok, probs = validate()
    if ok:
        print("  PASS —— 所有 %d 个条目字段完整，status 合法" % len(MISSING_DATA))
    else:
        print("  FAIL —— 发现 %d 个问题：" % len(probs))
        for p in probs[:30]:
            print("    - %s" % p)
