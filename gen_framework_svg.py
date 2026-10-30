# -*- coding: utf-8 -*-
"""生成《城市碳核算与政策分析框架》总图 SVG (137 行 / 26 一级模块 / 8 层)。"""
import io
from framework_core import (VERSION, BUILT, KEY_FIGURES, IDENTITIES, build_data)

_DATA = build_data()

# ---------------- 画布与排版参数 ----------------
W = 2000
MARGIN = 70
CARD_X = 196
CARD_W = W - CARD_X - MARGIN
PAD = 34
INNER_X = CARD_X + PAD
INNER_W = CARD_W - 2 * PAD

CHIP_FS = 17
CHIP_PX = 13
CHIP_PY = 8
CHIP_GAP = 9
LINE_GAP = 9
CHIP_H = 36
NUM_FS = 13
SUB_FS = 17
SUB_LABEL_H = 24
SUB_MT = 16
HEAD_H = 74
RAIL_CX = 120
RAIL_BADGE = 62

# ---------------- 配色 ----------------
BG0, BG1, BG2 = "#070d1a", "#0d1730", "#101c36"
CARD_FILL_A, CARD_FILL_B = "#131f3a", "#0e1830"
TXT_MAIN = "#e8eefb"
TXT_DIM = "#8ba0c2"
TXT_CHIP = "#d7e3f8"

# ---------------- 数据：8 层 ----------------
# (层号, 层名, 副标题, 强调色, 分组, 右上角公式/原则注释)
BANDS = [
    ("01", "边界", "确定统计什么、什么时候", "#94a3b8", [
        ("空间边界", [("1", "行政区划"), ("2", "时间边界")]),
    ]),
    ("02", "能源输入", "进入城市边界的能源与含碳物料", "#fbbf24", [
        ("能源输入 3–10", [("3", "煤炭"), ("4", "石油及成品油"), ("5", "天然气"),
                        ("6", "电力与热力"), ("7", "可再生能源"), ("8", "非能源含碳原料"),
                        ("9", "外部产品"), ("10", "外部废弃物")]),
    ]),
    ("03", "能源转换", "从一次能源到可用能，含开采与输配", "#fb923c", [
        ("能源转换 11–18", [("11", "煤炭开采"), ("12", "油气开采与储运"), ("13", "炼油与焦化"),
                         ("14", "燃煤电厂"), ("15", "燃气电厂"), ("16", "热电联产"),
                         ("17", "锅炉与工业供热"), ("18", "输配电与储能")]),
    ]),
    ("04", "排放源", "九类活动的直接排放与逸散", "#fb7185", [
        ("工业排放 19–24", [("19", "钢铁"), ("20", "水泥"), ("21", "石灰与玻璃"),
                         ("22", "化工"), ("23", "有色金属"), ("24", "其他制造业")]),
        ("工业能源 25–26", [("25", "工业电力消费"), ("26", "余热与副产气")]),
        ("建筑能源 27–28", [("27", "居民建筑"), ("28", "商业与公共建筑")]),
        ("交通能源 29–31", [("29", "道路交通"), ("30", "铁路交通"), ("31", "航空与水运")]),
        ("农业排放 32–34", [("32", "稻田"), ("33", "化肥与农田土壤"), ("34", "畜牧业")]),
        ("土地与生态 35–38", [("35", "森林"), ("36", "草地、农田与湿地"),
                          ("37", "城市绿地"), ("38", "土地利用变化")]),
        ("逸散排放 39–40", [("39", "煤矿甲烷"), ("40", "油气系统")]),
        ("工业气体 41", [("41", "制冷剂与含氟气体")]),
        ("废弃物 42–44", [("42", "垃圾焚烧"), ("43", "垃圾填埋"), ("44", "污水处理")]),
    ]),
    ("05", "碳流", "碳在城市系统内的去向与存留", "#c084fc", [
        ("碳流 45–56", [("45", "大气排放"), ("46", "生态系统吸收"), ("47", "产品碳储存"),
                     ("48", "废弃物与废水碳"), ("49", "跨设施转移"), ("50", "跨区域转移"),
                     ("51", "地质封存"), ("52", "碳矿化"), ("53", "碳利用"),
                     ("54", "水泥碳化"), ("55", "生物源碳"), ("56", "碳库存变化")]),
    ]),
    ("06", "城市清单", "把碳流汇总成可考核的账", "#22d3ee", [
        ("城市清单 57–65", [("57", "直接排放总量"), ("58", "间接排放"), ("59", "消费端隐含排放"),
                         ("60", "生产端排放"), ("61", "净排放"), ("62", "设施排放占比"),
                         ("63", "行业排放占比"), ("64", "能源关联排放占比"),
                         ("65", "减排与移除贡献")]),
    ]),
    ("07", "政策工具", "总量、市场、信用与移除的完整链条", "#34d399", [
        ("碳预算 66", [("66", "国家与行业碳预算")]),
        ("总量控制 67–75", [("67", "全国碳市场覆盖范围"), ("68", "市场配额总量"),
                         ("69", "强度控制"), ("70", "总量控制"), ("71", "强度向总量转型"),
                         ("72", "配额分配"), ("73", "配额收紧"), ("74", "配额盈缺与清缴"),
                         ("75", "控制效果评估")]),
        ("碳市场 76–78", [("76", "全国碳排放权交易"), ("77", "碳价格"), ("78", "配额市场稳定性")]),
        ("碳信用 79–90", [("79", "CCER项目资格"), ("80", "额外性"), ("81", "基准线"),
                       ("82", "项目减排量"), ("83", "泄漏"), ("84", "持久性与逆转"),
                       ("85", "测量不确定性"), ("86", "重复计算与重复签发"),
                       ("87", "核证与登记"), ("88", "抵消资格与比例"),
                       ("89", "信用注销"), ("90", "信用质量评价")]),
        ("碳移除 91–104", [("91", "移除路径分类"), ("92", "大气来源证明"), ("93", "总移除量"),
                        ("94", "生命周期排放"), ("95", "净移除量"), ("96", "储存期限"),
                        ("97", "逆转监测"), ("98", "项目确权"), ("99", "方法学适用性"),
                        ("100", "第三方核查"), ("101", "项目登记与信用签发"),
                        ("102", "信用交易与注销"), ("103", "单位净移除成本"),
                        ("104", "技术扩散与规模化")]),
        ("碳税 105–107", [("105", "税基与税率"), ("106", "税收与排放响应"), ("107", "分配效应")]),
        ("碳交易 108–110", [("108", "企业履约成本"), ("109", "碳价传导"),
                         ("110", "市场覆盖与竞争")]),
        ("自愿碳市场 111–112", [("111", "CCER项目收入"), ("112", "其他碳信用标准")]),
    ]),
    ("08", "分析与数据", "驱动因素、核算质量与情景推演", "#60a5fa", [
        ("能源经济 113–123", [("113", "能源价格"), ("114", "能源强度"), ("115", "碳强度"),
                           ("116", "减排成本"), ("117", "产业结构"),
                           ("118", "企业投资与融资"), ("119", "财政与补贴"),
                           ("120", "绿色金融"), ("121", "居民消费"),
                           ("122", "产业链隐含碳"), ("123", "政策因果效应")]),
        ("MRV 与质量 124–128", [("124", "活动数据"), ("125", "排放因子"), ("126", "实测与估算"),
                             ("127", "误差与不确定性"), ("128", "重复计算检查")]),
        ("数据体系 129–132", [("129", "设施数据库"), ("130", "能源数据库"),
                          ("131", "碳流数据库"), ("132", "经济政策数据库")]),
        ("情景模拟 133–137", [("133", "能源替代"), ("134", "工业技术改造"),
                          ("135", "碳价与总量政策"), ("136", "碳移除规模化"),
                          ("137", "综合政策组合")]),
    ]),
]


BAND_NOTES = {
    "01": u"核算边界 = 行政区划 × 日历年",
    "02": u"排放 = 实物量 × 低位热值 × 含碳量 × 氧化率 × 44/12",
    "03": u"总排放与排放强度须分列：EF = (CC×OX×44/12) ÷ η",
    "04": u"燃烧排放与工业过程排放必须分列",
    "05": u"C_in − C_out + C_gen − C_cons − ΔS = 0",
    "06": u"4 条电力因子序列，禁跨序列拼接",
    "07": u"先减排、后移除；抵消设比例上限",
    "08": u"Kaya + LMDI 分解；DID 防交错处理偏误",
}


# ---------------- 文本宽度估算 ----------------
def char_w(ch, fs):
    return fs * (0.56 if ord(ch) < 128 else 1.0)


def text_w(s, fs):
    return sum(char_w(c, fs) for c in s)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------- 布局预计算 ----------------
COL_GAP = 46
BAND_COLS = {"04": 2}   # 第 04 层子组多且短，改双栏填充版面


def pack_rows(chips, avail_w):
    """把 chips 打包成若干行；每项携带 (num,name,num_w,txt_w,chip_w,offset_x)。"""
    rows, cur, cur_w = [], [], 0.0
    for num, name in chips:
        nw = text_w(num, NUM_FS)
        tw = text_w(name, CHIP_FS)
        cw = CHIP_PX * 2 + nw + 7 + tw
        if cur and cur_w + CHIP_GAP + cw > avail_w:
            rows.append(cur)
            cur, cur_w = [], 0.0
        if cur:
            cur_w += CHIP_GAP
        cur.append((num, name, nw, tw, cw, cur_w))
        cur_w += cw
    if cur:
        rows.append(cur)
    return rows


def group_h(rows):
    if not rows:
        return SUB_LABEL_H
    return SUB_LABEL_H + len(rows) * CHIP_H + (len(rows) - 1) * LINE_GAP


def build_blocks(groups, cols):
    """返回 (blocks, content_height)。block = (dy, dx, label, rows, avail_w)。"""
    blocks = []
    y = 0.0
    if cols <= 1:
        for gi, (label, chips) in enumerate(groups):
            if gi > 0:
                y += SUB_MT
            rows = pack_rows(chips, INNER_W)
            blocks.append((y, 0, label, rows, INNER_W))
            y += group_h(rows)
        return blocks, y

    cell_w = (INNER_W - COL_GAP * (cols - 1)) / float(cols)
    for i in range(0, len(groups), cols):
        if i > 0:
            y += SUB_MT
        row_groups = groups[i:i + cols]
        row_h = 0.0
        for j, (label, chips) in enumerate(row_groups):
            rows = pack_rows(chips, cell_w)
            blocks.append((y, j * (cell_w + COL_GAP), label, rows, cell_w))
            row_h = max(row_h, group_h(rows))
        y += row_h
    return blocks, y


laid = []
for no, name, sub, accent, groups in BANDS:
    note = BAND_NOTES.get(no)
    cols = BAND_COLS.get(no, 1)
    blocks, ch = build_blocks(groups, cols)
    card_h = int(round(PAD + HEAD_H + ch + PAD))
    laid.append((no, name, sub, accent, blocks, card_h, ch, note, cols))

# ---- 完整性断言 ----
seen = []
n_groups = 0
for _b in laid:
    for _dy, _dx, _label, _rowlist, _aw in _b[4]:
        n_groups += 1
        for _row in _rowlist:
            for _item in _row:
                seen.append(int(_item[0]))
assert len(seen) == 137, "chip count = %d, expect 137" % len(seen)
assert sorted(seen) == list(range(1, 138)), "row numbers are not exactly 1..137"
assert n_groups == 26, "一级模块数 = %d, expect 26 (原表一级模块数)" % n_groups

_overflow = []
for _b in laid:
    for _dy, _dx, _label, _rowlist, _aw in _b[4]:
        for _row in _rowlist:
            for _item in _row:
                if _item[5] + _item[4] > _aw + 0.5:
                    _overflow.append((_b[0], _item[1], round(_item[5] + _item[4], 1), round(_aw, 1)))
assert not _overflow, "chip 溢出栏宽: %s" % _overflow[:5]
print("核对通过：137 个核算对象 / 26 个一级模块 / %d 层 / 无溢出" % len(laid))

TOP_H = 300
BAND_GAP = 40
FOOT_H = 500
total_h = int(round(TOP_H + sum(b[5] for b in laid) + BAND_GAP * len(laid) + FOOT_H))

# ---------------- 组装 SVG ----------------
out = []
a = out.append

a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
  'width="%d" height="%d" role="img" aria-labelledby="ttl">' % (W, total_h, W, total_h))
a('<title id="ttl">城市碳核算与政策分析框架 · 137 项总图</title>')
a('<defs>')

a('<linearGradient id="bg" x1="0" y1="0" x2="0.25" y2="1" color-interpolation="linearRGB">'
  '<stop offset="0%%" stop-color="%s"/><stop offset="42%%" stop-color="%s"/>'
  '<stop offset="100%%" stop-color="%s"/></linearGradient>' % (BG0, BG1, BG2))

a('<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5" color-interpolation="linearRGB">'
  '<stop offset="0%" stop-color="#1e40af" stop-opacity="0.42"/>'
  '<stop offset="55%" stop-color="#1e3a8a" stop-opacity="0.14"/>'
  '<stop offset="100%" stop-color="#0a1020" stop-opacity="0"/></radialGradient>')

for _b in laid:
    no = _b[0]
    gid = "card" + no
    a('<linearGradient id="%s" x1="0" y1="0" x2="0.18" y2="1" color-interpolation="linearRGB">'
      '<stop offset="0%%" stop-color="%s"/><stop offset="100%%" stop-color="%s"/></linearGradient>'
      % (gid, CARD_FILL_A, CARD_FILL_B))

a('<filter id="sh" x="-12%" y="-12%" width="130%" height="130%" '
  'color-interpolation-filters="linearRGB">'
  '<feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b"/>'
  '<feOffset in="b" dx="0" dy="6" result="o"/>'
  '<feFlood flood-color="#050a16" flood-opacity="0.55" result="c"/>'
  '<feComposite in="c" in2="o" operator="in" result="s"/>'
  '<feMerge><feMergeNode in="s"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

a('<filter id="grain" color-interpolation-filters="linearRGB">'
  '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>'
  '<feColorMatrix type="saturate" values="0"/>'
  '<feBlend in="SourceGraphic" mode="soft-light"/></filter>')

a('</defs>')

# ---------- 背景 ----------
a('<g id="background">')
a('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, total_h))
a('<ellipse cx="%d" cy="120" rx="%d" ry="760" fill="url(#glow)"/>' % (W // 2, int(W * 0.52)))
# 细网格
a('<g stroke="#2b3f63" stroke-width="1" opacity="0.20">')
step = 50
for gx in range(0, W + 1, step):
    a('<line x1="%d" y1="0" x2="%d" y2="%d"/>' % (gx, gx, total_h))
for gy in range(0, total_h + 1, step * 2):
    a('<line x1="0" y1="%d" x2="%d" y2="%d"/>' % (gy, W, gy))
a('</g>')
a('<rect width="%d" height="%d" filter="url(#grain)" opacity="0.055"/>' % (W, total_h))
a('</g>')

# ---------- 标题 ----------
a('<g id="title">')
a('<text x="%d" y="118" font-family="Microsoft YaHei" font-size="58" font-weight="700" '
  'fill="%s" letter-spacing="2">城市碳核算与政策分析框架</text>' % (MARGIN, TXT_MAIN))
a('<text x="%d" y="168" font-family="Microsoft YaHei" font-size="21" fill="%s" '
  'letter-spacing="1">ENERGY · CARBON · ECONOMY　全链条核算与政策分析总图</text>'
  % (MARGIN, TXT_DIM))
# 强调线
a('<rect x="%d" y="196" width="150" height="5" rx="2.5" fill="#38bdf8"/>' % MARGIN)
a('<rect x="%d" y="196" width="420" height="5" rx="2.5" fill="#38bdf8" opacity="0.18"/>'
  % MARGIN)

# 统计胶囊
pills = [("137", "行核算对象"), ("26", "一级模块"), ("8", "层结构"),
         (str(_DATA["totals"]["params"]), "条参数"),
         (str(_DATA["totals"]["gaps"]), "项待补缺口")]
px = MARGIN
py = 224
for val, lab in pills:
    pw = 34 + text_w(val, 30) + 12 + text_w(lab, 16) + 30
    a('<rect x="%d" y="%d" width="%d" height="46" rx="23" fill="#152441" '
      'stroke="#2f4570" stroke-width="1"/>' % (px, py, pw))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="30" font-weight="700" '
      'fill="#7dd3fc">%s</text>' % (px + 30, py + 34, val))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="16" fill="%s">%s</text>'
      % (px + 30 + text_w(val, 30) + 12, py + 32, TXT_DIM, lab))
    px += pw + 16

# 右上角流向提示
a('<text x="%d" y="118" text-anchor="end" font-family="Microsoft YaHei" font-size="24" '
  'font-weight="700" fill="#34d399">%s</text>' % (W - MARGIN, VERSION))
a('<text x="%d" y="146" text-anchor="end" font-family="Microsoft YaHei" font-size="15" '
  'fill="%s">建立 %s　·　与 index.html 同源生成</text>' % (W - MARGIN, TXT_DIM, BUILT))
a('<text x="%d" y="250" text-anchor="end" font-family="Microsoft YaHei" font-size="17" '
  'fill="%s">输入 → 转换 → 排放 → 碳流 → 清单 → 政策 → 分析</text>'
  % (W - MARGIN, TXT_DIM))
a('</g>')

# ---------- 主体 ----------
a('<g id="midground">')
y = TOP_H
rail_segs = []
for idx, (no, name, sub, accent, blocks, card_h, ch, note, cols) in enumerate(laid):
    gid = "card" + no
    # 卡片
    a('<g filter="url(#sh)"><rect x="%d" y="%d" width="%d" height="%d" rx="20" '
      'fill="url(#%s)" stroke="%s" stroke-opacity="0.28" stroke-width="1.2"/></g>'
      % (CARD_X, y, CARD_W, card_h, gid, accent))
    # 顶部内侧高光（五区光照的 specular）
    a('<rect x="%d" y="%d" width="%d" height="1.5" rx="0.75" fill="%s" opacity="0.45"/>'
      % (CARD_X + 24, y + 1.5, CARD_W - 48, accent))
    # 左侧强调条
    a('<rect x="%d" y="%d" width="6" height="%d" rx="3" fill="%s" opacity="0.9"/>'
      % (CARD_X, y + 18, card_h - 36, accent))
    # 轨道徽标
    by = y + 30
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="16" fill="%s" fill-opacity="0.14" '
      'stroke="%s" stroke-opacity="0.55" stroke-width="1.5"/>'
      % (RAIL_CX - RAIL_BADGE // 2, by, RAIL_BADGE, RAIL_BADGE, accent, accent))
    a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" '
      'font-size="26" font-weight="700" fill="%s">%s</text>'
      % (RAIL_CX, by + 42, accent, no))
    rail_segs.append((by, by + RAIL_BADGE, accent))

    # 层标题
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="31" font-weight="700" '
      'fill="%s">%s</text>' % (INNER_X, y + PAD + 30, TXT_MAIN, esc(name)))
    nw = text_w(name, 31)
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="17" fill="%s">%s</text>'
      % (INNER_X + nw + 20, y + PAD + 30, TXT_DIM, esc(sub)))

    # 右上角公式 / 原则
    if note:
        nx = INNER_X + INNER_W
        a('<text x="%d" y="%d" text-anchor="end" font-family="Microsoft YaHei" '
          'font-size="16" font-weight="500" fill="%s" fill-opacity="0.95">%s</text>'
          % (nx, y + PAD + 29, accent, esc(note)))
        d = 8
        a('<circle cx="%d" cy="%d" r="3.5" fill="%s" fill-opacity="0.9"/>'
          % (nx - text_w(note, 16) - 18, y + PAD + 24, accent))

    base_y = y + PAD + HEAD_H
    for bidx, (bdy, bdx, label, rowlist, avail) in enumerate(blocks):
        cy = base_y + bdy
        bx = INNER_X + bdx
        # 单栏时画子组分隔线
        if cols == 1 and bdy > 0:
            a('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
              'stroke-opacity="0.13" stroke-width="1" stroke-dasharray="4 7"/>'
              % (INNER_X, cy - SUB_MT / 2.0, INNER_X + INNER_W, cy - SUB_MT / 2.0, accent))
        a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="%d" '
          'font-weight="600" fill="%s" fill-opacity="0.92">%s</text>'
          % (bx, cy + 17, SUB_FS, accent, esc(label)))
        cy += SUB_LABEL_H
        for ri, row in enumerate(rowlist):
            for (num, nm, numw, tw, cw, off) in row:
                cx = bx + off
                a('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="9" fill="%s" '
                  'fill-opacity="0.10" stroke="%s" stroke-opacity="0.38" stroke-width="1"/>'
                  % (cx, cy, cw, CHIP_H, accent, accent))
                a('<text x="%.1f" y="%d" font-family="Microsoft YaHei" font-size="%d" '
                  'fill="%s" fill-opacity="0.85">%s</text>'
                  % (cx + CHIP_PX, cy + 23, NUM_FS, accent, num))
                a('<text x="%.1f" y="%d" font-family="Microsoft YaHei" font-size="%d" '
                  'fill="%s">%s</text>'
                  % (cx + CHIP_PX + numw + 7, cy + 24, CHIP_FS, TXT_CHIP, esc(nm)))
            cy += CHIP_H
            if ri < len(rowlist) - 1:
                cy += LINE_GAP
    y += card_h + BAND_GAP
a('</g>')

# ---------- 轨道连线 ----------
a('<g id="rail"><g stroke="#2c4064" stroke-width="3" stroke-linecap="round">')
for i in range(len(rail_segs) - 1):
    a('<line x1="%d" y1="%d" x2="%d" y2="%d"/>'
      % (RAIL_CX, rail_segs[i][1], RAIL_CX, rail_segs[i + 1][0]))
a('</g></g>')

# ---------- 底部：四条核心恒等式 ----------
fy = y + 14
a('<g id="footer">')
a('<rect x="%d" y="%d" width="%d" height="2" rx="1" fill="#2c4064"/>'
  % (MARGIN, fy, W - MARGIN * 2))
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="19" font-weight="600" '
  'fill="#9db4d6">四条核心恒等式（框架内所有数字的对账依据）</text>'
  % (MARGIN, fy + 46))

_ID_COL = ["#c084fc", "#22d3ee", "#34d399", "#fbbf24"]
ident = [(k, v, _ID_COL[i % len(_ID_COL)]) for i, (k, v) in enumerate(IDENTITIES)]
iy = fy + 76
for k, v, col in ident:
    a('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (MARGIN + 5, iy + 8, col))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="17" font-weight="600" '
      'fill="%s">%s</text>' % (MARGIN + 22, iy + 14, col, k))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="17" fill="%s">%s</text>'
      % (MARGIN + 22 + text_w(k, 17) + 22, iy + 14, TXT_DIM, v))
    iy += 40

# 数据锚点：与 index.html 逐字一致
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="14" font-weight="600" '
  'fill="#7dd3fc">%s 数据锚点（与 index.html 同源，逐字一致）</text>'
  % (MARGIN, iy + 26, VERSION))
a('<text x="%d" y="%d" font-family="Consolas,Microsoft YaHei" font-size="14" fill="#9db4d6">%s</text>'
  % (MARGIN, iy + 50, esc("  ·  ".join(KEY_FIGURES))))
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="13" fill="#5d7398">'
  '电力因子分四条序列（清单 / 市场 / 化石电源 / 碳足迹），年份与单位不同即不可拼接；'
  '2026 四行业配额：发电 A = Q_e×B_e×F_f + Q_h×B_h，钢铁水泥铝 A = E×(1+α)</text>'
  % (MARGIN, iy + 76))

a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="15" fill="#5d7398">'
  '数据支撑见《碳核算框架_数据支撑手册.md》与《碳核算参数表.xlsx》｜'
  '待补数据见 missing_data_spec.py｜证据链见 index.html「双轴状态」页｜'
  '编号与 137 行总表一一对应</text>'
  % (MARGIN, iy + 110))
a('</g>')

a('</svg>')

_svg = "\n".join(out)
_missing = [k for k in KEY_FIGURES if k not in _svg]
assert not _missing, "SVG 缺少与 HTML 共享的关键数字: %s" % _missing

for _fn in ("draft.svg", "城市碳核算与政策分析框架_总图.svg"):
    with io.open(_fn, "w", encoding="utf-8", newline="\n") as _f:
        _f.write(_svg)

print("OK  viewBox=0 0 %d %d   (%.2f MB)" % (W, total_h, len(_svg) / 1024 / 1024))
print("一致性断言通过：%d 个关键数字与 index.html 同源" % len(KEY_FIGURES))
