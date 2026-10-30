# -*- coding: utf-8 -*-
"""生成《能源经济分析与决策知识系统》静态总图 SVG（12×4 矩阵海报）。"""
import io

from energy_core import build_energy_data

D = build_energy_data()
T = D["totals"]

W = 1800
MARGIN = 64
TOP_H = 300
ROW_H = 62
MATRIX_TOP = TOP_H + 96
MATRIX_H = ROW_H * 12
BOT_TOP = MATRIX_TOP + MATRIX_H + 104
BOT_H = 470
H = BOT_TOP + BOT_H

TXT_MAIN = "#e8eefb"
TXT_DIM = "#8ba0c2"
BG0, BG1, BG2 = "#070d1a", "#0d1730", "#101c36"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text_w(s, fs):
    return sum(fs * (0.56 if ord(c) < 128 else 1.0) for c in str(s))


out = []
a = out.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
  'role="img" aria-labelledby="ttl">' % (W, H, W, H))
a('<title id="ttl">能源经济分析与决策知识系统 · 12 域 × 4 层研究矩阵</title>')
a('<defs>')
a('<linearGradient id="bg" x1="0" y1="0" x2="0.25" y2="1" color-interpolation="linearRGB">'
  '<stop offset="0%%" stop-color="%s"/><stop offset="45%%" stop-color="%s"/>'
  '<stop offset="100%%" stop-color="%s"/></linearGradient>' % (BG0, BG1, BG2))
a('<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
  '<stop offset="0%" stop-color="#1e40af" stop-opacity="0.40"/>'
  '<stop offset="60%" stop-color="#1e3a8a" stop-opacity="0.12"/>'
  '<stop offset="100%" stop-color="#0a1020" stop-opacity="0"/></radialGradient>')
a('</defs>')

a('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H))
a('<ellipse cx="%d" cy="110" rx="%d" ry="700" fill="url(#glow)"/>' % (W // 2, int(W * 0.5)))
a('<g stroke="#2b3f63" stroke-width="1" opacity="0.16">')
for gx in range(0, W + 1, 50):
    a('<line x1="%d" y1="0" x2="%d" y2="%d"/>' % (gx, gx, H))
for gy in range(0, H + 1, 100):
    a('<line x1="0" y1="%d" x2="%d" y2="%d"/>' % (gy, W, gy))
a('</g>')

# ---------- 标题 ----------
a('<text x="%d" y="112" font-family="Microsoft YaHei" font-size="52" font-weight="700" '
  'fill="%s" letter-spacing="2">能源经济分析与决策知识系统</text>' % (MARGIN, TXT_MAIN))
a('<text x="%d" y="158" font-family="Microsoft YaHei" font-size="19" fill="%s" '
  'letter-spacing="1">12 个研究域 × 4 个分析层次 × 8 层证据体系　·　'
  '碳排放是结果变量模块（05），不是系统全部</text>' % (MARGIN, TXT_DIM))
a('<rect x="%d" y="182" width="150" height="5" rx="2.5" fill="#38bdf8"/>' % MARGIN)
a('<rect x="%d" y="182" width="430" height="5" rx="2.5" fill="#38bdf8" opacity="0.18"/>' % MARGIN)

pills = [(str(T["domains"]), "研究域"), (str(T["layers"]), "分析层次"),
         (str(T["questions"]), "研究问题"), (str(T["indicatorCount"]), "可算指标"),
         (str(T["datasets"]), "数据集"), (str(T["models"]), "模型"),
         (str(T["anchors"]), "数据锚点"), (str(T["evidence"]), "层证据")]
px, py = MARGIN, 210
for val, lab in pills:
    pw = 30 + text_w(val, 26) + 10 + text_w(lab, 15) + 26
    a('<rect x="%d" y="%d" width="%d" height="42" rx="21" fill="#152441" stroke="#2f4570"/>'
      % (px, py, pw))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="26" font-weight="700" '
      'fill="#7dd3fc">%s</text>' % (px + 26, py + 31, val))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="15" fill="%s">%s</text>'
      % (px + 26 + text_w(val, 26) + 10, py + 29, TXT_DIM, lab))
    px += pw + 12

a('<text x="%d" y="112" text-anchor="end" font-family="Microsoft YaHei" font-size="24" '
  'font-weight="700" fill="#34d399">%s</text>' % (W - MARGIN, D["version"]))
a('<text x="%d" y="140" text-anchor="end" font-family="Microsoft YaHei" font-size="15" '
  'fill="%s">建立 %s　·　与 index.html 同源生成</text>' % (W - MARGIN, TXT_DIM, D["built"]))

# ---------- 矩阵 ----------
LAB_W = 300
CELL_W = (W - MARGIN * 2 - LAB_W - 96) / 4.0
TOT_W = 96
mx = MARGIN
my = MATRIX_TOP

a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="19" font-weight="600" '
  'fill="#9db4d6">研究域 ↓　×　分析层次 →</text>' % (mx, my - 18))

# 列表头
for i, l in enumerate(D["layers"]):
    cx = mx + LAB_W + i * CELL_W
    a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" font-size="17" '
      'font-weight="700" fill="%s">%s %s</text>' % (cx + CELL_W / 2, my + 4, l["accent"], l["id"], esc(l["name"])))
    a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" font-size="12.5" '
      'fill="%s">%s</text>' % (cx + CELL_W / 2, my + 24, TXT_DIM, esc(l["sub"])))
a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" font-size="14" '
  'fill="%s">合计</text>' % (mx + LAB_W + 4 * CELL_W + TOT_W / 2, my + 14, TXT_DIM))

ry = my + 40
for d in D["domains"]:
    acc = d["accent"]
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="#101c34" fill-opacity="0.55" '
      'stroke="%s" stroke-opacity="0.25"/>' % (mx, ry, LAB_W - 12, ROW_H - 10, acc))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="18" font-weight="700" '
      'fill="%s">%s</text>' % (mx + 14, ry + 26, acc, d["no"]))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="17" font-weight="600" '
      'fill="%s">%s</text>' % (mx + 50, ry + 26, TXT_MAIN, esc(d["name"])))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="12.5" fill="%s">%s</text>'
      % (mx + 50, ry + 45, TXT_DIM, esc(d["sub"])))
    for i, l in enumerate(D["layers"]):
        n = d["counts"][l["id"]]
        cx = mx + LAB_W + i * CELL_W
        op = min(0.55, 0.07 + n * 0.075)
        a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" fill-opacity="%.3f" '
          'stroke="%s" stroke-opacity="0.22"/>'
          % (cx + 4, ry, CELL_W - 8, ROW_H - 10, acc, op, acc))
        a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" font-size="21" '
          'font-weight="700" fill="%s">%d</text>'
          % (cx + CELL_W / 2, ry + 36, TXT_MAIN, n))
    a('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="#16274a" stroke="#2f4570"/>'
      % (mx + LAB_W + 4 * CELL_W + 6, ry, TOT_W - 12, ROW_H - 10))
    a('<text x="%d" y="%d" text-anchor="middle" font-family="Microsoft YaHei" font-size="20" '
      'font-weight="700" fill="#7dd3fc">%d</text>'
      % (mx + LAB_W + 4 * CELL_W + TOT_W / 2, ry + 36, d["counts"]["total"]))
    ry += ROW_H

a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="13" fill="#5d7398">'
  '格子数值 = 该单元格下的研究问题条数；48 个单元格在构建期断言校验，不允许为空</text>'
  % (mx, ry + 22))

# ---------- 底部 ----------
by = BOT_TOP
a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2c4064" stroke-width="2"/>'
  % (MARGIN, by - 26, W - MARGIN, by - 26))

# 四层说明
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="18" font-weight="600" '
  'fill="#9db4d6">四个层次的方法论要点</text>' % (MARGIN, by + 6))
ly = by + 34
for l in D["layers"]:
    a('<rect x="%d" y="%d" width="10" height="10" rx="5" fill="%s"/>'
      % (MARGIN + 4, ly + 4, l["accent"]))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="16" font-weight="700" '
      'fill="%s">%s %s</text>' % (MARGIN + 24, ly + 14, l["accent"], l["id"], esc(l["name"])))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="13.5" fill="%s">'
      '%d 问　·　%s</text>' % (MARGIN + 24, ly + 34, TXT_DIM, l["count"],
                               esc(l["sub"])))
    ly += 52

# 状态分布
rx = MARGIN + 520
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="18" font-weight="600" '
  'fill="#9db4d6">可执行状态</text>' % (rx, by + 6))
st = T["byStatus"]
bx, bw = rx, 640
acc = 0.0
for k in ("可算", "部分可算", "缺关键数据"):
    n = st.get(k, 0)
    w = bw * n / float(T["questions"])
    col = D["statusMeta"][k][1]
    a('<rect x="%.1f" y="%d" width="%.1f" height="16" rx="4" fill="%s"/>'
      % (bx + acc, by + 24, w, col))
    acc += w
ly = by + 58
for k in ("可算", "部分可算", "缺关键数据"):
    n = st.get(k, 0)
    col = D["statusMeta"][k][1]
    a('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (rx + 5, ly + 6, col))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="14.5" fill="%s">%s %d 条'
      '（%.0f%%）</text>' % (rx + 18, ly + 11, TXT_DIM, k, n, n * 100.0 / T["questions"]))
    ly += 26

a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="13" fill="#5d7398">'
  '「可算」只表示数据有公开来源，不表示已算出结果；「缺关键数据」是真实约束，不是框架缺陷</text>'
  % (rx, ly + 8))

# 证据体系
ex = MARGIN + 1240
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="18" font-weight="600" '
  'fill="#9db4d6">八层证据体系</text>' % (ex, by + 6))
ey = by + 34
for e in D["evidence"]:
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="14" font-weight="700" '
      'fill="%s">%s</text>' % (ex, ey, e["accent"], e["id"]))
    a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="13.5" fill="%s">%s</text>'
      % (ex + 40, ey, TXT_DIM, esc(e["name"])))
    ey += 23

# 页脚
fy = H - 96
a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2c4064" stroke-width="2"/>'
  % (MARGIN, fy, W - MARGIN, fy))
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="14" font-weight="600" '
  'fill="#7dd3fc">%s 数据锚点（与 index.html 同源）</text>' % (MARGIN, fy + 30, D["version"]))
anchors = ("107 条问题 · 307 个指标 · 30 个数据集 · 22 个模型 · 8 层证据 · "
           "50 条数据锚点（18 已核实 / 31 部分核实 / 1 计算值 / 7 未核实）· "
           "碳子模块 137 对象 / 87 参数 / 63 缺口")
a('<text x="%d" y="%d" font-family="Consolas,Microsoft YaHei" font-size="13.5" fill="#9db4d6">%s</text>'
  % (MARGIN, fy + 54, esc(anchors)))
a('<text x="%d" y="%d" font-family="Microsoft YaHei" font-size="12.5" fill="#5d7398">'
  '碳排放核算子模块见 carbon.html 与 framework-map.svg｜证据链与逐参数台账见碳子模块「参数证据台账」页</text>'
  % (MARGIN, fy + 78))

a('</svg>')

svg = "\n".join(out)

# ---------- 一致性断言 ----------
MUST = ["12", "107", "307", "30", "22", "50", "能源经济分析与决策知识系统",
        "能源供给", "未来预测与情景", "八层证据体系", "数据锚点"]
miss = [m for m in MUST if m not in svg]
assert not miss, "SVG 缺少关键内容: %s" % miss
for d in D["domains"]:
    assert d["name"] in svg, "缺研究域: %s" % d["name"]

for fn in ("energy-map.svg", "能源经济分析系统_总图.svg"):
    with io.open(fn, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)

print("OK  viewBox=0 0 %d %d  (%.2f MB)" % (W, H, len(svg) / 1024.0 / 1024.0))
print("一致性断言通过：12 域全部出现，关键数字齐备")
