# -*- coding: utf-8 -*-
"""生成《城市碳核算与政策分析框架》交互地图 HTML（v3）。

数据来自 framework_core.py（单一事实源）。静态 SVG 总图由 gen_framework_svg.py
从同一模块生成，因此网页与静态图永远同源、不会出现内容不一致。
"""
import io, json
from framework_core import build_data, VERSION, BUILT

DATA = build_data()
DATA_JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))
t = DATA["totals"]
print("核对通过: 137 条 / 26 模块 / 8 层 / 参数 %d 条 / 缺口 %d 项 / 状态 %s"
      % (t["params"], t["gaps"], t["byStatus"]))


# ============================================================
# 六、HTML 模板
# ============================================================
HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>城市碳核算与政策分析框架 · 交互地图</title>
<style>
  :root{
    --bg:#080e1c; --bg2:#0d1730; --card:#121f3a; --card2:#0e1830;
    --line:#26375a; --txt:#e8eefb; --dim:#8ba0c2; --dim2:#5e7ba0;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    background:radial-gradient(900px 500px at 50% -100px,rgba(30,64,175,.35),transparent 70%),
               linear-gradient(160deg,var(--bg),var(--bg2) 60%,#101c36);
    color:var(--txt);
    font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;
    min-height:100vh; padding-bottom:60px;
  }
  /* ---------- 顶栏 ---------- */
  header{padding:26px 22px 0;max-width:1720px;margin:0 auto}
  h1{font-size:30px;letter-spacing:1px;font-weight:700}
  .sub{color:var(--dim);font-size:14px;margin-top:6px;letter-spacing:.5px}
  .stats{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}
  .pill{background:#152441;border:1px solid var(--line);border-radius:20px;
        padding:6px 15px;font-size:13px;color:var(--dim);display:flex;gap:7px;align-items:center}
  .pill b{color:#7dd3fc;font-size:16px;font-weight:700}
  /* ---------- 层按钮 ---------- */
  nav{max-width:1720px;margin:16px auto 0;padding:0 22px;
      display:flex;gap:9px;flex-wrap:wrap;position:sticky;top:0;z-index:30;
      background:linear-gradient(#080e1c 72%,rgba(8,14,28,0));padding-top:12px;padding-bottom:14px}
  .lbtn{cursor:pointer;border:1px solid var(--line);background:#101c34;color:var(--txt);
        border-radius:11px;padding:9px 15px;font-size:14px;font-family:inherit;
        display:flex;gap:9px;align-items:center;transition:.15s;white-space:nowrap}
  .lbtn:hover{border-color:#3f5c8f;transform:translateY(-1px)}
  .lbtn .no{font-size:12px;font-weight:700;opacity:.9}
  .lbtn.on{background:#1a2c4e;border-color:currentColor;box-shadow:0 0 0 1px currentColor inset}
  /* ---------- 布局 ---------- */
  .wrap{max-width:1720px;margin:0 auto;padding:0 22px;
        display:grid;grid-template-columns:minmax(0,1fr) 452px;gap:20px;align-items:start}
  @media(max-width:1180px){.wrap{grid-template-columns:1fr}}
  /* ---------- 图 ---------- */
  .layer{margin-bottom:16px}
  .lhead{display:flex;align-items:center;gap:12px;padding:10px 4px 10px}
  .lno{width:44px;height:44px;flex:0 0 44px;border-radius:13px;display:grid;place-items:center;
       font-weight:700;font-size:19px;border:1.5px solid currentColor;background:rgba(255,255,255,.045)}
  .lname{font-size:20px;font-weight:700}
  .lsub{font-size:13px;color:var(--dim);margin-left:2px}
  .mods{display:grid;gap:10px;
        grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
  .mods.one{grid-template-columns:1fr}
  .layer{scroll-margin-top:88px}
  .mod{background:linear-gradient(150deg,var(--card),var(--card2));
       border:1px solid var(--line);border-left:3px solid currentColor;
       border-radius:14px;padding:13px 14px;cursor:pointer;transition:.15s;text-align:left;
       font-family:inherit;color:var(--txt);width:100%}
  .mod:hover{border-color:#3f5c8f;border-left-color:currentColor;transform:translateY(-2px);
             box-shadow:0 10px 24px -12px #000}
  .mod.on{background:#17305a;box-shadow:0 0 0 1.5px currentColor inset}
  .mod-h{display:flex;align-items:center;gap:8px;margin-bottom:3px}
  .mod-h h3{font-size:16px;font-weight:700;flex:1}
  .rng{font-size:11.5px;color:var(--dim);font-variant-numeric:tabular-nums}
  .dot{width:8px;height:8px;border-radius:50%;flex:0 0 8px}
  .chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
  .chip{font-size:12px;padding:3px 7px;border-radius:7px;cursor:pointer;
        background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
        color:#c9d8ef;font-family:inherit;transition:.12s}
  .chip:hover,.chip:focus-visible{background:rgba(125,211,252,.18);border-color:#7dd3fc;color:#fff;outline:none}
  .mod:focus-visible,.lbtn:focus-visible{outline:2px solid #7dd3fc;outline-offset:2px}
  .chip b{opacity:.55;font-weight:400;margin-right:3px;font-variant-numeric:tabular-nums}
  /* ---------- 右栏 ---------- */
  aside{position:sticky;top:82px;max-height:calc(100vh - 100px);overflow:auto;
        background:linear-gradient(165deg,#13203c,#0d172c);border:1px solid var(--line);
        border-radius:18px;padding:18px}
  aside::-webkit-scrollbar{width:8px}
  aside::-webkit-scrollbar-thumb{background:#2b4067;border-radius:4px}
  .p-kicker{font-size:11.5px;letter-spacing:1.4px;color:var(--dim);text-transform:uppercase}
  .p-title{font-size:22px;font-weight:700;margin:5px 0 3px}
  .p-meta{font-size:12.5px;color:var(--dim);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  .tag{font-size:11.5px;padding:2.5px 9px;border-radius:20px;border:1px solid currentColor}
  .sec{margin-top:16px;border-top:1px solid var(--line);padding-top:13px}
  .sec-t{font-size:12px;letter-spacing:1px;color:var(--dim);margin-bottom:8px;
         display:flex;align-items:center;gap:7px}
  .sec-t::before{content:"";width:3px;height:12px;border-radius:2px;background:currentColor}
  .first{font-size:14.5px;line-height:1.78;color:#dfe9fa;
         background:rgba(125,211,252,.07);border:1px solid rgba(125,211,252,.22);
         border-radius:11px;padding:12px 13px}
  .formula{font-family:Consolas,"Courier New",monospace;font-size:13.5px;line-height:1.7;
           background:#0a1424;border:1px solid var(--line);border-radius:10px;
           padding:11px 13px;color:#a5e3ff;white-space:pre-wrap;word-break:break-word}
  ul.li{list-style:none;display:grid;gap:7px}
  ul.li li{font-size:13px;line-height:1.62;color:#c8d7ee;padding-left:18px;position:relative}
  ul.li li::before{content:"▸";position:absolute;left:2px;opacity:.65}
  ul.li.gap li::before{content:"○";color:#fbbf24}
  .spec{font-family:Consolas,monospace;font-size:11.5px;color:#fbbf24;opacity:.95}
  ul.src li::before{content:"\2197";color:#38bdf8}
  ul.src a{color:#7dd3fc;text-decoration:none;border-bottom:1px dotted rgba(125,211,252,.4)}
  ul.src a:hover{color:#bae6fd}
  ul.src .org{font-size:11.5px;color:#6d86ab;margin-top:2px;display:block}
  .unit-row{display:flex;gap:10px;font-size:12.5px;padding:6px 0;border-bottom:1px dashed rgba(255,255,255,.07)}
  .unit-row b{color:#9fc3ee;flex:0 0 118px;font-weight:600}
  .unit-row span{color:#b9cbe6;line-height:1.55}
  .unit-row em{color:#5f7599;font-style:normal;flex:0 0 92px}
  .empty{font-size:13px;color:#5f7599;font-style:italic}
  .ov-row{display:flex;justify-content:space-between;font-size:13px;padding:6px 0;
          border-bottom:1px dashed rgba(255,255,255,.07)}
  .ov-row span:last-child{font-variant-numeric:tabular-nums;color:#9fc3ee}
  .bar{height:7px;border-radius:4px;background:#1b2b49;overflow:hidden;margin-top:8px;display:flex}
  .bar i{display:block;height:100%}
  .legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;font-size:12px;color:var(--dim)}
  .legend i{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:5px}
  .hint{font-size:12px;color:#5f7599;line-height:1.7;margin-top:14px}
  /* ---------- 搜索 ---------- */
  .tools{display:flex;gap:9px;align-items:center;margin:0 0 14px;flex-wrap:wrap}
  .search{flex:1;min-width:200px;background:#101c34;border:1px solid var(--line);
          border-radius:10px;padding:9px 13px;color:var(--txt);font-size:13.5px;
          font-family:inherit;outline:none}
  .search:focus{border-color:#3f5c8f}
  .fbtn{cursor:pointer;background:#101c34;border:1px solid var(--line);color:var(--dim);
        border-radius:9px;padding:8px 12px;font-size:12.5px;font-family:inherit}
  .fbtn.on{color:#7dd3fc;border-color:#3f5c8f;background:#16274a}
  .hidden{display:none !important}
  /* ---------- 视图切换 ---------- */
  .view[hidden]{display:none}
  .tabs{max-width:1720px;margin:14px auto 0;padding:0 22px;display:flex;gap:8px;flex-wrap:wrap}
  .tab{cursor:pointer;border:1px solid var(--line);background:#0e1830;color:var(--dim);
       border-radius:10px;padding:9px 16px;font-size:13.5px;font-family:inherit;transition:.15s}
  .tab:hover{border-color:#3f5c8f;color:#c9d8ef}
  .tab.on{background:#17305a;color:#7dd3fc;border-color:#3f5c8f;box-shadow:0 0 0 1px #3f5c8f inset}
  .card{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
        border-radius:14px;padding:16px 18px;margin-bottom:14px}
  .card h2{font-size:17px;margin-bottom:5px}
  .card .lead{font-size:13px;color:var(--dim);line-height:1.72;margin-bottom:11px}
  table.tbl{width:100%;border-collapse:collapse;font-size:13px}
  table.tbl th,table.tbl td{border-bottom:1px solid rgba(255,255,255,.08);padding:8px 9px;
        text-align:left;vertical-align:top;line-height:1.6}
  table.tbl th{color:#8ba0c2;font-weight:600;font-size:12px;letter-spacing:.4px;background:rgba(255,255,255,.03)}
  table.tbl td.num{font-variant-numeric:tabular-nums;text-align:right;color:#a5e3ff;white-space:nowrap}
  table.tbl tr:last-child td{border-bottom:none}
  .md{display:inline-flex;gap:5px;flex-wrap:wrap}
  .md i{font-style:normal;font-size:10.5px;padding:1.5px 6px;border-radius:6px;
        border:1px solid currentColor;opacity:.9;white-space:nowrap}
  .calc input{width:118px;background:#0a1424;border:1px solid var(--line);border-radius:7px;
              padding:6px 9px;color:#a5e3ff;font-family:Consolas,monospace;font-size:13px}
  .calc .row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:8px 0;font-size:13px}
  .calc .out{font-family:Consolas,monospace;font-size:14.5px;color:#34d399;margin-top:6px;line-height:1.8}
  .mt{font-size:12px;color:#6d86ab;margin-top:9px;line-height:1.68}
  .warn{font-size:12.5px;color:#fbbf24;background:rgba(251,191,36,.08);
        border:1px solid rgba(251,191,36,.28);border-radius:9px;padding:9px 11px;line-height:1.7;margin-top:9px}
</style>
</head>
<body>

<header>
  <h1>城市碳核算与政策分析框架</h1>
  <div class="sub">ENERGY · CARBON · ECONOMY　点击任意层 / 模块 / 条目，查看第一性原理与最新进展</div>
  <div class="stats">
    <div class="pill"><b>137</b>核算对象</div>
    <div class="pill"><b>26</b>一级模块</div>
    <div class="pill"><b>8</b>层结构</div>
    <div class="pill"><b id="s-ver">0</b>条参数（附来源）</div>
    <div class="pill"><b id="s-gap">0</b>项待补缺口</div>
    <div class="pill" style="border-color:#3f5c8f"><b id="s-ver2" style="color:#34d399">v3</b><span id="s-built"></span></div>
  </div>
</header>

<nav id="nav"></nav>

<div class="tabs" id="tabs">
  <button class="tab on" data-v="map">框架地图</button>
  <button class="tab" data-v="method">研究方法层 · 6 类</button>
  <button class="tab" data-v="data">数据序列 · 电力因子</button>
  <button class="tab" data-v="params">参数证据台账</button>
  <button class="tab" data-v="policy">2026 政策台账</button>
  <button class="tab" data-v="axes">双轴状态与恒等式</button>
</div>

<div class="wrap view" id="view-map">
  <main>
    <div class="tools">
      <input class="search" id="q" placeholder="搜索条目 / 模块名，例如：电力、CCER、稻田…">
      <button class="fbtn on" data-f="all">全部</button>
      <button class="fbtn" data-f="verified">已核实</button>
      <button class="fbtn" data-f="partial">部分可用</button>
      <button class="fbtn" data-f="pending">待补参数</button>
    </div>
    <div id="map"></div>
  </main>
  <aside id="panel"></aside>
</div>

<div class="wrap view" id="view-method" hidden style="grid-template-columns:1fr">
  <main id="mMethod"></main>
</div>
<div class="wrap view" id="view-data" hidden style="grid-template-columns:1fr">
  <main id="mData"></main>
</div>
<div class="wrap view" id="view-params" hidden style="grid-template-columns:1fr">
  <main id="mParams"></main>
</div>
<div class="wrap view" id="view-policy" hidden style="grid-template-columns:1fr">
  <main id="mPolicy"></main>
</div>
<div class="wrap view" id="view-axes" hidden style="grid-template-columns:1fr">
  <main id="mAxes"></main>
</div>

<script>
const DATA = __DATA__;
const SM = DATA.statusMeta;

/* ---------- 渲染主图 ---------- */
const navEl = document.getElementById('nav');
const mapEl = document.getElementById('map');

function layerBtn(l){
  return `<button class="lbtn" data-layer="${l.no}" style="color:${l.accent}">
      <span class="no">${l.no}</span><span style="color:var(--txt)">${l.name}</span>
    </button>`;
}
navEl.innerHTML = DATA.layers.map(layerBtn).join('');

let modIndex = [];
let html = '';
DATA.layers.forEach(l=>{
  html += `<section class="layer" data-layer="${l.no}" style="color:${l.accent}">
    <div class="lhead">
      <div class="lno" style="color:${l.accent}">${l.no}</div>
      <div>
        <div class="lname" style="color:var(--txt)">${l.name}
          <span class="lsub">${l.sub}</span></div>
      </div>
    </div>
    <div class="mods${l.mods.length===1?' one':''}">`;
  l.mods.forEach(m=>{
    const idx = modIndex.length;
    modIndex.push({layer:l, mod:m, idx});
    const st = SM[m.status];
    html += `<div class="mod" role="button" tabindex="0" data-idx="${idx}" style="color:${l.accent}">
      <div class="mod-h">
        <span class="dot" style="background:${st[1]}"></span>
        <h3>${m.name}</h3>
        <span class="rng">${m.rows}</span>
      </div>
      <div class="chips">` +
      m.chips.map(c=>`<span class="chip" role="button" tabindex="0" data-idx="${idx}" data-n="${c.n}"><b>${c.n}</b>${c.t}</span>`).join('') +
      `</div></div>`;
  });
  html += `</div></section>`;
});
mapEl.innerHTML = html;

/* ---------- 面板 ---------- */
const panel = document.getElementById('panel');

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function srcBlock(m){
  if(!m.srcs || !m.srcs.length) return '';
  const items = m.srcs.map(id=>{
    const x = DATA.sources[id];
    if(!x) return '';
    const tail = `<span class="org">${esc(x.org)} · ${esc(x.date)}` +
      (x.verify ? ` · <b style="color:#fbbf24">${esc(x.verify)}</b>` : '') + `</span>`;
    return x.url
      ? `<li><a href="${x.url}" target="_blank" rel="noopener">${esc(x.doc)}</a>${tail}</li>`
      : `<li><span style="color:#c8d7ee">${esc(x.doc)}</span>${tail}</li>`;
  }).join('');
  return `<div class="sec" style="color:#38bdf8">
      <div class="sec-t">证据链 · 模块级 ${m.srcs.length} 条来源</div>
      <ul class="li src">${items}</ul>
      <div class="hint" style="margin-top:8px">说明：此处为模块级绑定，用于定位该模块的整体依据；
      逐参数级登记见「参数证据台账」视图（含来源编号 / 年份 / 单位 / 适用范围）。</div>
    </div>`;
}

function overview(){
  const t = DATA.totals;
  let cnt = {verified:0, partial:0, pending:0};
  DATA.layers.forEach(l=>l.mods.forEach(m=>cnt[m.status]++));
  const rows = DATA.layers.map(l=>{
    const v = l.mods.filter(m=>m.status==='verified').length;
    return `<div class="ov-row"><span style="color:${l.accent}">${l.no} ${l.name}</span>
      <span>${l.mods.length} 模块 · 已核实 ${v}</span></div>`;
  }).join('');
  panel.innerHTML = `
    <div class="p-kicker">OVERVIEW</div>
    <div class="p-title">总览</div>
    <div class="p-meta">点击左侧任意层、模块或条目查看详情</div>

    <div class="sec" style="color:#7dd3fc">
      <div class="sec-t">数据进度</div>
      <div class="bar">
        <i style="width:${cnt.verified/t.mods*100}%;background:${SM.verified[1]}"></i>
        <i style="width:${cnt.partial/t.mods*100}%;background:${SM.partial[1]}"></i>
        <i style="width:${cnt.pending/t.mods*100}%;background:${SM.pending[1]}"></i>
      </div>
      <div class="legend">
        <span><i style="background:${SM.verified[1]}"></i>已核实 ${cnt.verified}</span>
        <span><i style="background:${SM.partial[1]}"></i>部分可用 ${cnt.partial}</span>
        <span><i style="background:${SM.pending[1]}"></i>待补参数 ${cnt.pending}</span>
      </div>
    </div>

    <div class="sec" style="color:#a78bfa">
      <div class="sec-t">规模</div>
      <div class="ov-row"><span>核算对象</span><span>${t.items} 条</span></div>
      <div class="ov-row"><span>一级模块</span><span>${t.mods} 个</span></div>
      <div class="ov-row"><span>结构层次</span><span>${t.layers} 层</span></div>
      <div class="ov-row"><span>已核实参数</span><span>${t.params} 条</span></div>
      <div class="ov-row"><span>待补缺口</span><span>${t.gaps} 项</span></div>
      <div class="ov-row"><span>数据版本</span><span>${DATA.version} · ${DATA.built}</span></div>
    </div>

    <div class="sec" style="color:#34d399">
      <div class="sec-t">各层完成度</div>
      ${rows}
    </div>

    <div class="sec" style="color:#fbbf24">
      <div class="sec-t">四条对账恒等式</div>
      <ul class="li">
        ${DATA.identities.map(x=>`<li><b>${esc(x[0])}</b>：<span class="spec" style="color:#a5e3ff">${esc(x[1])}</span></li>`).join('')}
      </ul>
    </div>

    <div class="sec" style="color:#f472b6">
      <div class="sec-t">状态口径已改：双轴替代单一标签</div>
      <div class="hint" style="margin-top:0">
        v2 的单一「已核实 / 部分可用 / 待补参数」出现 15/26 个模块与缺口清单自相矛盾
        （如「已核实」仍列缺口、「待补」却无缺口清单）。v3 改为两轴独立标定：
        <b>方法成熟度 M</b>（公式是否明确、是否有标准方法学）与
        <b>数据完备度 D</b>（参数是否齐全可出数），三色状态由 (M, D, 缺口数) 派生，
        并加硬断言：D&lt;4 必须有缺口清单，D=4 必须有来源。详见「双轴状态」页。
      </div>
    </div>

    <div class="sec" style="color:#38bdf8">
      <div class="sec-t">单位与量纲（审计要求）</div>
      ${DATA.units.map(u=>`<div class="unit-row"><em>${esc(u.k)}</em><b>${esc(u.a)}</b><span>${esc(u.b)}</span></div>`).join('')}
    </div>

    <div class="sec" style="color:#fbbf24">
      <div class="sec-t">已核实参数的定义边界</div>
      <div class="hint" style="margin-top:0">
        「已核实」= 该表述可追溯到政府公告/统计公报原文并已逐字比对；
        <b>不等于</b>该参数适用于任意城市、任意年份。适用条件见各模块「口径限定」条目。
      </div>
    </div>

    <div class="sec" style="color:#a78bfa">
      <div class="sec-t">配套文件（可下载）</div>
      <ul class="li src">
        <li><a href="manual.md" target="_blank" rel="noopener">数据支撑手册</a>
          <span class="org">参数、公式、来源与待核清单</span></li>
        <li><a href="parameters.xlsx" target="_blank" rel="noopener">碳核算参数表</a>
          <span class="org">8 个工作表，可载入模型</span></li>
        <li><a href="missing_data_spec.py" target="_blank" rel="noopener">缺失数据任务单</a>
          <span class="org">35 条 / 172 个数据点，含自检脚本</span></li>
        <li><a href="audit-response-round2.md" target="_blank" rel="noopener">第二轮审计响应</a>
          <span class="org">2026 政策核实、α 方向修正、状态体系重构</span></li>
        <li><a href="audit-response-round1.md" target="_blank" rel="noopener">第一轮审计响应</a>
          <span class="org">逐条核实记录与修正说明</span></li>
        <li><a href="framework-map.svg" target="_blank" rel="noopener">静态矢量总图</a>
          <span class="org">2000 × 3890 SVG，与页面同源生成</span></li>
        <li><a href="framework_core.py" target="_blank" rel="noopener">单一事实源</a>
          <span class="org">全部数据 + 双轴标定 + 生成期断言，可本地复现</span></li>
      </ul>
    </div>`;
}

function renderLayer(l){
  const first = l.first;
  const mods = l.mods.map(m=>{
    const st = SM[m.status];
    return `<div class="ov-row"><span>${esc(m.name)}</span>
      <span style="color:${st[1]}">${st[0]} · ${m.chips.length} 条</span></div>`;
  }).join('');
  panel.innerHTML = `
    <div class="p-kicker" style="color:${l.accent}">LAYER ${l.no}</div>
    <div class="p-title">${esc(l.name)}</div>
    <div class="p-meta"><span class="tag" style="color:${l.accent}">${l.mods.length} 个模块</span>
      <span>${l.mods.reduce((a,m)=>a+m.chips.length,0)} 条核算对象</span></div>
    <div class="sec" style="color:${l.accent}">
      <div class="sec-t">第一性原理</div>
      <div class="first">${esc(first)}</div>
    </div>
    <div class="sec" style="color:#7dd3fc">
      <div class="sec-t">本层模块进度</div>${mods}
    </div>`;
}

function renderModule(idx){
  const {layer:l, mod:m} = modIndex[idx];
  const st = SM[m.status];
  const ver = m.verified.length ? `<ul class="li">` +
      m.verified.map(v=>`<li>${esc(v)}</li>`).join('') + `</ul>`
      : `<div class="empty">暂无已核实参数</div>`;
  const gap = m.gaps.length ? `<ul class="li gap">` +
      m.gaps.map(g=>`<li>${esc(g.t)} <span class="spec">[${g.id}]</span></li>`).join('') + `</ul>`
      : `<div class="empty">本模块无待补缺口</div>`;
  panel.innerHTML = `
    <div class="p-kicker" style="color:${l.accent}">${l.no} ${l.name}</div>
    <div class="p-title">${esc(m.name)}</div>
    <div class="p-meta">
      <span>对应总表第 ${m.rows} 行</span>
      <span class="tag" style="color:${st[1]}">${st[0]}</span>
      <span>${m.chips.length} 条</span>
      <span class="md" style="color:#7dd3fc"><i>M${m.M}</i><i style="color:#a78bfa">D${m.D}</i></span>
    </div>

    <div class="sec" style="color:#7dd3fc">
      <div class="sec-t">第一性原理</div>
      <div class="first">${esc(m.first)}</div>
    </div>

    <div class="sec" style="color:#a78bfa">
      <div class="sec-t">核心核算式</div>
      <div class="formula">${esc(m.formula)}</div>
    </div>

    <div class="sec" style="color:#34d399">
      <div class="sec-t">最新进展 · 已核实 ${m.verified.length} 条</div>
      ${ver}
    </div>

    <div class="sec" style="color:#fbbf24">
      <div class="sec-t">待补缺口 ${m.gaps.length} 项</div>
      ${gap}
    </div>

    ${srcBlock(m)}

    <div class="hint">状态说明：${st[2]}<br>
      待补项编号对应 missing_data_spec.py 中的条目 key。</div>`;
}

function renderItem(idx, n){
  const {layer:l, mod:m} = modIndex[idx];
  const chip = m.chips.find(c=>c.n===n);
  if(!chip) return;
  const st = SM[m.status];
  const gap = m.gaps.length
    ? `<ul class="li gap">` + m.gaps.map(g=>`<li>${esc(g.t)} <span class="spec">[${g.id}]</span></li>`).join('') + `</ul>`
    : `<div class="empty">本模块无待补缺口</div>`;
  panel.innerHTML = `
    <div class="p-kicker" style="color:${l.accent}">第 ${n} 项 · ${l.no} ${l.name}</div>
    <div class="p-title">${esc(chip.t)}</div>
    <div class="p-meta">
      <span>所属模块：${esc(m.name)}（第 ${m.rows} 行）</span>
      <span class="tag" style="color:${st[1]}">${st[0]}</span>
    </div>

    <div class="sec" style="color:#7dd3fc">
      <div class="sec-t">第一性原理（模块级）</div>
      <div class="first">${esc(m.first)}</div>
    </div>

    <div class="sec" style="color:#a78bfa">
      <div class="sec-t">本条核算式</div>
      <div class="formula">${esc(m.formula)}</div>
    </div>

    <div class="sec" style="color:#34d399">
      <div class="sec-t">模块内已核实参数</div>
      ${m.verified.length ? `<ul class="li">`+m.verified.map(v=>`<li>${esc(v)}</li>`).join('')+`</ul>`
                          : `<div class="empty">暂无</div>`}
    </div>

    <div class="sec" style="color:#fbbf24">
      <div class="sec-t">阻断本条的待补数据</div>
      ${gap}
    </div>

    ${srcBlock(m)}`;
}

/* ---------- 交互 ---------- */
let cur = {type:'overview', idx:null, n:null};

function setOn(el, cls){
  document.querySelectorAll('.'+cls).forEach(x=>x.classList.remove('on'));
  if(el) el.classList.add('on');
}

mapEl.addEventListener('click', e=>{
  const chip = e.target.closest('.chip');
  if(chip){
    e.stopPropagation();
    const idx = +chip.dataset.idx, n = chip.dataset.n;
    cur = {type:'item', idx, n};
    setOn(chip.closest('.mod'), 'on');
    renderItem(idx, n);
    return;
  }
  const mod = e.target.closest('.mod');
  if(mod){
    const idx = +mod.dataset.idx;
    cur = {type:'mod', idx};
    setOn(mod, 'on');
    renderModule(idx);
  }
});

mapEl.addEventListener('keydown', e=>{
  if(e.key!=='Enter' && e.key!==' ') return;
  const el = e.target.closest('.chip') || e.target.closest('.mod');
  if(!el) return;
  e.preventDefault();
  if(el.classList.contains('chip')){
    cur = {type:'item', idx:+el.dataset.idx, n:el.dataset.n};
    setOn(el.closest('.mod'), 'on');
    renderItem(+el.dataset.idx, el.dataset.n);
  } else {
    cur = {type:'mod', idx:+el.dataset.idx};
    setOn(el, 'on');
    renderModule(+el.dataset.idx);
  }
});

navEl.addEventListener('click', e=>{
  const b = e.target.closest('.lbtn');
  if(!b) return;
  const no = b.dataset.layer;
  const l = DATA.layers.find(x=>x.no===no);
  setOn(b, 'on');
  document.querySelectorAll('.mod').forEach(x=>x.classList.remove('on'));
  cur = {type:'layer', no};
  renderLayer(l);
  const sec = document.querySelector(`.layer[data-layer="${no}"]`);
  if(sec){
    const top = sec.getBoundingClientRect().top + (window.pageYOffset || 0) - 76;
    window.scrollTo(0, Math.max(0, top));
  }
});

/* ---------- 搜索 / 过滤 ---------- */
const q = document.getElementById('q');
let filter = 'all';

function applyFilter(){
  const kw = q.value.trim().toLowerCase();
  document.querySelectorAll('.mod').forEach(modEl=>{
    const idx = +modEl.dataset.idx;
    const m = modIndex[idx].mod;
    const hitKw = !kw || m.name.toLowerCase().includes(kw) ||
      m.chips.some(c=>c.t.toLowerCase().includes(kw) || c.n===kw);
    const hitF = filter==='all' || m.status===filter;
    modEl.classList.toggle('hidden', !(hitKw && hitF));
    if(hitKw && kw){
      modEl.querySelectorAll('.chip').forEach(ch=>{
        const t = ch.textContent.toLowerCase();
        ch.style.opacity = t.includes(kw) ? '1' : '.32';
      });
    } else {
      modEl.querySelectorAll('.chip').forEach(ch=>ch.style.opacity='1');
    }
  });
  document.querySelectorAll('.layer').forEach(sec=>{
    const any = sec.querySelectorAll('.mod:not(.hidden)').length > 0;
    sec.classList.toggle('hidden', !any);
  });
}
q.addEventListener('input', applyFilter);
document.querySelectorAll('.fbtn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); filter = b.dataset.f; applyFilter();
  });
});

/* ============================================================
   研究方法层
   ============================================================ */
const mMethod = document.getElementById('mMethod');
function drawMethods(){
  mMethod.innerHTML = `
    <div class="card" style="border-left:3px solid #a78bfa">
      <h2>研究方法层 · 6 类方法</h2>
      <div class="lead">这 6 类方法<b>不新增核算对象</b>，而是叠加在既有 137 个对象之上——
      把「统计」升级为「归因、因果与成本」。之所以不把它们塞进 8 层框架，
      是因为它们不是第 9 层数据，而是作用在既有数据上的运算。</div>
    </div>` +
    DATA.methods.map(x=>`
      <div class="card">
        <h2>${esc(x.name)}
          <span style="font-size:12px;color:#6d86ab;font-weight:400">${esc(x.en)}</span></h2>
        <div class="lead">${esc(x.use)}</div>
        <div class="formula">${esc(x.formula)}</div>
        <div class="sec" style="color:#7dd3fc"><div class="sec-t">数据需求</div>
          <ul class="li">${x.needs.map(s=>`<li>${esc(s)}</li>`).join('')}</ul></div>
        <div class="sec" style="color:#34d399"><div class="sec-t">作用到的核算对象</div>
          <div class="md" style="gap:6px">${x.maps.map(s=>`<i style="color:#a5e3ff">${esc(s)}</i>`).join('')}</div></div>
        <div class="sec" style="color:#fbbf24"><div class="sec-t">适用限度</div>
          <div class="warn">${esc(x.limit)}</div></div>
        <div class="mt">代表文献：${x.refs.map(esc).join(' ｜ ')}<br>
          <span style="color:#fbbf24">注：以上为方法学原始出处，本轮<b>未</b>逐条核验卷期与页码；正式引用前须补 DOI 与页码。</span></div>
      </div>`).join('');
}

/* ============================================================
   数据序列 · 电力排放因子
   ============================================================ */
const mData = document.getElementById('mData');
function drawData(){
  mData.innerHTML = `
    <div class="card" style="border-left:3px solid #22d3ee">
      <h2>电力排放因子：${DATA.elec.length} 条独立序列，禁止跨序列拼接</h2>
      <div class="lead">v2 的实质问题不是数字错，而是把不同口径的因子并列在同一张表里，
      读者会默认它们构成一条时间序列。下面按「序列」拆开，每条序列单独记录年份 / 区域 / 单位 / 适用场景。</div>
      ${DATA.elec.map(s=>`
        <div class="sec" style="color:#22d3ee">
          <div class="sec-t">${esc(s.name)}
            <span class="spec" style="color:#6d86ab">[${esc(s.id)}]</span></div>
          <table class="tbl">
            <tr><th style="width:24%">年份 / 区域</th><th style="width:18%">数值</th><th>单位</th></tr>
            ${s.values.map(v=>`<tr><td>${esc(v[0])}</td><td class="num">${esc(v[1])}</td><td>${esc(s.unit)}</td></tr>`).join('')}
          </table>
          <div class="mt"><b style="color:#9fc3ee">适用场景</b>：${esc(s.scope)}<br>
            <b style="color:#9fc3ee">使用规则</b>：${esc(s.rule)}<br>
            <b style="color:#9fc3ee">说明</b>：${esc(s.note)}<br>
            <b style="color:#9fc3ee">来源</b>：${s.srcs.map(id=>(DATA.sources[id]||{}).doc||id).map(esc).join('；')}</div>
        </div>`).join('')}
    </div>
    <div class="card">
      <h2>三种最常见的误用</h2>
      <div class="warn" style="color:#fb7185;background:rgba(251,113,133,.08);border-color:rgba(251,113,133,.3)">
        ① 用 0.5777（碳足迹 kgCO₂e/kWh）算清单范围二的 CO₂ 排放——
        量纲与口径双错：碳足迹含生命周期非 CO₂ 温室气体，清单范围二只算 CO₂。<br>
        ② 用 0.5306（清单 kgCO₂/kWh）算产品碳足迹——漏掉燃料开采、运输、输配环节。<br>
        ③ 把 2022→2023→2024 三个不同口径的数排成一条序列算「年均降幅」——分母不同，降幅无意义。
      </div>
    </div>`;
}

/* ============================================================
   参数证据台账（逐参数级）
   ============================================================ */
const mParams = document.getElementById('mParams');
function drawParams(){
  const t = DATA.totals;
  const rows = DATA.params.map(p=>{
    const s = p.bound ? (DATA.sources[p.src]||{}) : null;
    return `<tr>
      <td style="color:#6d86ab">${p.layer}</td>
      <td>${esc(p.mod)}</td>
      <td>${esc(p.t)}</td>
      <td>${p.bound
        ? `<span style="color:#34d399">${esc(p.src)}</span>`
        : `<span style="color:#fb7185">—</span>`}</td>
      <td>${p.bound ? esc(p.year) : '—'}</td>
      <td>${p.bound ? esc(p.unit) : '—'}</td>
      <td style="font-size:12px;color:#8ba0c2">${esc(p.scope)}</td>
    </tr>`;
  }).join('');
  mParams.innerHTML = `
    <div class="card" style="border-left:3px solid #34d399">
      <h2>参数证据台账：把「模块级」拆到「参数级」</h2>
      <div class="lead">
        上一轮你指出：<b>「62 条是项目的核实状态统计，不能直接等同于 62 条都已经具备可复现的学术证据链」</b>——成立。
        现在每条参数单独登记来源编号 / 数据年份 / 单位 / 适用范围四项字段，
        并如实区分「已绑定文号」与「仅模块级」。
      </div>
      <table class="tbl">
        <tr><th style="width:32%">指标</th><th style="width:18%">数量</th><th>说明</th></tr>
        <tr><td>参数总条目</td><td class="num">${t.params}</td><td>所有模块「最新进展·已核实」列表的条目总数</td></tr>
        <tr><td style="color:#34d399">已绑定文号级来源</td><td class="num" style="color:#34d399">${t.paramsBound}</td>
            <td>可指向具体文件（含文号/公告号）且登记了年份、单位与适用范围</td></tr>
        <tr><td style="color:#fb7185">仅模块级</td><td class="num" style="color:#fb7185">${t.paramsUnbound}</td>
            <td>${esc(DATA.unboundNote)}</td></tr>
        <tr><td>待补缺口</td><td class="num">${t.gaps}</td><td>数据缺口，编号对应 missing_data_spec.py</td></tr>
      </table>
      <div class="warn">
        <b>口径说明</b>：本表的「已绑定文号」只保证该条<b>可追溯到文件</b>，不保证已核对页码。
        页码级核验（page-level citation）仍需逐条打开原文比对，属下一步工作。
        因此 ${t.paramsBound} 条也<b>不等于</b> ${t.paramsBound} 条已完成学术级引用审查。
      </div>
    </div>

    <div class="card">
      <h2>逐条台账（${t.params} 条）</h2>
      <table class="tbl">
        <tr><th style="width:5%">层</th><th style="width:12%">模块</th><th style="width:34%">参数表述</th>
            <th style="width:7%">来源</th><th style="width:7%">年份</th>
            <th style="width:12%">单位</th><th>适用范围</th></tr>
        ${rows}
      </table>
    </div>

    <div class="card">
      <h2>来源编号索引（${Object.keys(DATA.sources).length} 条）</h2>
      <table class="tbl">
        <tr><th style="width:6%">编号</th><th style="width:14%">发布机构</th><th style="width:37%">文件</th>
            <th style="width:11%">日期</th><th>链接</th></tr>
        ${Object.keys(DATA.sources).map(id=>{const x=DATA.sources[id];
          return `<tr><td class="num" style="text-align:left">${id}</td><td>${esc(x.org)}</td>
            <td>${esc(x.doc)}</td><td>${esc(x.date)}</td>
            <td>${x.url?`<a href="${x.url}" target="_blank" rel="noopener" style="color:#7dd3fc">原文</a>`
                       :'<span style="color:#fbbf24">未取得</span>'}</td></tr>`;
        }).join('')}
      </table>
    </div>`;
}

/* ============================================================
   2026 政策台账 · 碳市场配额 + CCER 方法学
   ============================================================ */
const mPolicy = document.getElementById('mPolicy');
function drawPolicy(){
  const e = DATA.ets;
  mPolicy.innerHTML = `
    <div class="card" style="border-left:3px solid #34d399">
      <h2>2026 年全国碳市场配额方法（四行业）</h2>
      <div class="lead">方法截至 ${esc(e.asof)}。发电用<b>强度基准法</b>，钢铁/水泥/铝冶炼用<b>强度系数法</b>——
      两者都叫「强度」，但不是同一个公式，不可互换代入。</div>
      <table class="tbl">
        <tr><th style="width:8%">行业</th><th style="width:18%">配额方法</th>
            <th style="width:22%">公式</th><th>变量与说明</th></tr>
        ${e.rows.map(r=>`<tr><td><b>${esc(r.ind)}</b></td><td>${esc(r.method)}</td>
          <td class="num" style="text-align:left;white-space:pre-wrap">${esc(r.formula)}</td>
          <td>${esc(r.vars)}<div class="mt">${esc(r.note)}</div></td></tr>`).join('')}
      </table>
      <div class="sec" style="color:#34d399"><div class="sec-t">α 取值表（偏离度 X 分段）</div>
        <table class="tbl">
          <tr><th style="width:26%">偏离度区间</th><th style="width:22%">α 取值</th><th>含义</th></tr>
          ${(e.alpha||[]).map(r=>`<tr><td class="num" style="text-align:left">${esc(r[0])}</td>
            <td class="num" style="text-align:left;color:#a5e3ff">${esc(r[1])}</td>
            <td>${esc(r[2])}</td></tr>`).join('')}
        </table>
        <div class="mt">X = (BP − I) ÷ BP；BP 行业平衡值（使行业配额总量＝应清缴总量时的工序碳排放强度），I 企业主要工序吨产品碳排放量。</div>
      </div>

      <div class="sec" style="color:#34d399"><div class="sec-t">共同规则</div>
        <ul class="li">${e.common.map(s=>`<li>${esc(s)}</li>`).join('')}</ul></div>
      <div class="warn">${esc(e.caveat)}</div>
    </div>

    <div class="card">
      <h2>配额计算器　A = E × (1 + α)</h2>
      <div class="lead">输入经核查排放量 E、系数 α 与碳价，得到核发配额、盈缺与履约成本。
      注意 α 的方向：<b style="color:#34d399">α > 0 是奖励先进（A > E，盈余）</b>，
      <b style="color:#fb7185">α < 0 是收紧落后（A < E，缺口）</b>。</div>
      <div class="calc">
        <div class="row"><label>E 经核查排放（tCO₂）</label>
          <input id="cE" type="number" value="1000000" step="10000"></div>
        <div class="row"><label>α 碳排放强度系数</label>
          <input id="cA" type="number" value="-0.02" step="0.01"></div>
        <div class="row"><label>碳价（元/tCO₂）</label>
          <input id="cP" type="number" value="62.36" step="0.01"></div>
        <div class="out" id="cOut"></div>
      </div>
      <div class="mt">对照：发电属基准法 A = Q_e × B_e × F_f + Q_h × B_h，必须先有发电量/供热量与基准值，
        不能套用本计算器。</div>
    </div>

    <div class="card">
      <h2>CCER 方法学版本台账</h2>
      <div class="lead">方法学不是「一个类别」，而是有版本、有权属规则、有计入期管理的法律文本。
      造林碳汇与红树林营造均已于 2026-10-10 更新至 V02。</div>
      <table class="tbl">
        <tr><th style="width:13%">编号</th><th style="width:11%">名称</th><th style="width:7%">版本</th>
            <th style="width:10%">日期</th><th style="width:15%">状态</th><th>关键变更</th></tr>
        ${DATA.ccer.ledger.map(r=>`<tr>
          <td class="num" style="text-align:left">${esc(r.code)}</td><td>${esc(r.name)}</td>
          <td>${esc(r.ver)}</td><td>${esc(r.date)}</td>
          <td style="color:${r.status==='现行'?'#34d399':(r.status.indexOf('未生效')>=0?'#fbbf24':'#8ba0c2')}">${esc(r.status)}</td>
          <td><ul class="li">${r.changes.map(c=>`<li>${esc(c)}</li>`).join('')}</ul></td></tr>`).join('')}
      </table>
      <div class="sec" style="color:#fbbf24"><div class="sec-t">版本与权属管理规则</div>
        <ul class="li gap">${DATA.ccer.rules.map(s=>`<li>${esc(s)}</li>`).join('')}</ul></div>
      <div class="warn">本页政策条目已取得原文链接与文号（S15–S18 均可在「双轴状态」页证据链清单中点击原文），
        其中配额方案的公式、基准值与 α 取值表已与国环规气候〔2026〕1号 PDF 正文逐字比对。
        仍未取得的是各行业「行业平衡值 BP」全表与有偿分配的分年比例安排。</div>
    </div>`;
  const cE=document.getElementById('cE'), cA=document.getElementById('cA'),
        cP=document.getElementById('cP'), cOut=document.getElementById('cOut');
  function calc(){
    const E=+cE.value, a=+cA.value, p=+cP.value;
    const A=E*(1+a), g=E-A, cost=g*p;
    const f=n=>Math.abs(n).toLocaleString('zh-CN',{maximumFractionDigits:1});
    cOut.innerHTML = `核发配额 A = ${f(A)} tCO₂　（α = ${a}）<br>` +
      (g>0 ? `缺口 E − A = ${f(g)} tCO₂ → 需购入，履约成本 ≈ ${f(cost)} 元`
           : `盈余 E − A = −${f(g)} tCO₂ → 可出售，理论收益 ≈ ${f(-cost)} 元`);
  }
  [cE,cA,cP].forEach(x=>x.addEventListener('input', calc));
  calc();
}

/* ============================================================
   双轴状态 / 恒等式 / 单位 / 证据链
   ============================================================ */
const mAxes = document.getElementById('mAxes');
function drawAxes(){
  const M = DATA.axes.M, D = DATA.axes.D;
  const rows = [];
  DATA.layers.forEach(l=>l.mods.forEach(m=>rows.push({l,m})));
  mAxes.innerHTML = `
    <div class="card" style="border-left:3px solid #f472b6">
      <h2>双轴状态体系：为什么弃用单一「已核实」标签</h2>
      <div class="lead">v2 用单一 status 标注 26 个模块，结果 <b>15 个模块</b>与缺口清单自相矛盾：
      「已核实」却仍列缺口 2 个；「待补参数」却没有任何缺口清单 1 个；「部分可用」却无缺口 1 个；
      另有 11 个「待补」模块同时列着已核实参数。根因是把「方法是否成熟」与「数据是否齐备」压成了一个变量。</div>
      <table class="tbl">
        <tr><th style="width:50%">方法成熟度 M（公式是否明确、有无标准方法学）</th>
            <th>数据完备度 D（参数是否齐全、能否出数）</th></tr>
        <tr><td>${M.map(x=>`<div style="margin:3px 0"><b style="color:#7dd3fc">${esc(x.code)}</b> ${esc(x.t)}</div>`).join('')}</td>
            <td>${D.map(x=>`<div style="margin:3px 0"><b style="color:#a78bfa">${esc(x.code)}</b> ${esc(x.t)}</div>`).join('')}</td></tr>
      </table>
      <div class="mt">派生规则：M≥3 且 D≥4 且缺口=0 → 已核实；D≤2 → 待补参数；其余 → 部分可用。<br>
        生成时执行的硬断言：<b>D&lt;4 ⟹ 至少 1 项缺口</b>；<b>已核实 ⟹ 缺口数 = 0</b>；<b>模块必须双轴标定</b>。不满足即构建失败。</div>
    </div>

    <div class="card">
      <h2>26 个模块的双轴标定</h2>
      <table class="tbl">
        <tr><th style="width:6%">层</th><th style="width:13%">模块</th><th style="width:8%">行</th>
            <th style="width:6%">M</th><th style="width:6%">D</th><th style="width:10%">状态</th>
            <th style="width:7%">参数</th><th style="width:7%">缺口</th><th>主要阻断项</th></tr>
        ${rows.map(o=>{const l=o.l,m=o.m;const st=SM[m.status];
          return `<tr><td style="color:${l.accent}">${l.no}</td><td>${esc(m.name)}</td>
            <td class="num">${esc(m.rows)}</td><td class="num">M${m.M}</td><td class="num">D${m.D}</td>
            <td style="color:${st[1]}">${st[0]}</td>
            <td class="num">${m.verified.length}</td><td class="num">${m.gaps.length}</td>
            <td style="font-size:12px;color:#8ba0c2">${m.gaps.map(g=>esc(g.t)).join('；')||'—'}</td></tr>`;
        }).join('')}
      </table>
    </div>

    <div class="card">
      <h2>四条对账恒等式</h2>
      <table class="tbl"><tr><th style="width:26%">恒等式</th><th>表达式</th></tr>
        ${DATA.identities.map(x=>`<tr><td>${esc(x[0])}</td>
          <td class="num" style="text-align:left;white-space:pre-wrap">${esc(x[1])}</td></tr>`).join('')}
      </table>
    </div>

    <div class="card">
      <h2>单位与量纲</h2>
      <table class="tbl"><tr><th style="width:10%">类</th><th style="width:28%">易混量</th><th>换算与说明</th></tr>
        ${DATA.units.map(u=>`<tr><td>${esc(u.k)}</td><td>${esc(u.a)}</td><td>${esc(u.b)}</td></tr>`).join('')}
      </table>
    </div>

    <div class="card">
      <h2>证据链清单（${Object.keys(DATA.sources).length} 条）</h2>
      <div class="lead">标注「未取得」的条目只有文件名与日期，没有原文链接——这些条目<b>不计入</b>已核实。</div>
      <table class="tbl">
        <tr><th style="width:6%">编号</th><th style="width:13%">发布机构</th><th style="width:34%">文件</th>
            <th style="width:11%">日期</th><th>链接 / 状态</th></tr>
        ${Object.keys(DATA.sources).map(id=>{const x=DATA.sources[id];
          return `<tr><td class="num" style="text-align:left">${id}</td><td>${esc(x.org)}</td>
            <td>${esc(x.doc)}</td><td>${esc(x.date)}</td>
            <td>${x.url?`<a href="${x.url}" target="_blank" rel="noopener" style="color:#7dd3fc">原文</a>`
                       :'<span style="color:#fbbf24">未取得</span>'}
            ${x.verify?`<div class="mt" style="color:#fbbf24">${esc(x.verify)}</div>`:''}</td></tr>`;
        }).join('')}
      </table>
    </div>

    <div class="card">
      <h2>本轮仍未完成的事项</h2>
      <ul class="li gap">
        <li>页码级引用核验：87 条参数已登记 src / year / unit / scope 四项（63 条绑定文号、24 条仅模块级），仍缺 page 字段与逐条原文比对记录</li>
        <li>城市级实证验证：未选定城市，未做一次完整核算并与成熟数据库交叉核对</li>
        <li>误差传播：已有公式与分布要求，但未真正跑出蒙特卡洛区间</li>
        <li>MRIO 消费端：只给出模型与数据需求，未接入实际投入产出表</li>
        <li>2026 政策原件：S15–S18 已取得原文链接与文号；仍缺各行业「行业平衡值 BP」全表与有偿分配分年比例</li>
      </ul>
    </div>`;
}

/* ============================================================
   Tab 切换
   ============================================================ */
const VIEWS = {map:'view-map', method:'view-method', data:'view-data',
               params:'view-params', policy:'view-policy', axes:'view-axes'};
document.getElementById('tabs').addEventListener('click', ev=>{
  const b = ev.target.closest('.tab');
  if(!b) return;
  const v = b.dataset.v;
  Object.keys(VIEWS).forEach(k=>{
    const el = document.getElementById(VIEWS[k]);
    if(el) el.hidden = (k!==v);
  });
  document.querySelectorAll('#tabs .tab').forEach(x=>x.classList.toggle('on', x.dataset.v===v));
  document.getElementById('nav').style.display = (v==='map') ? '' : 'none';
  try{ history.replaceState(null,'','#'+v); }catch(e){}
  window.scrollTo(0,0);
});

/* 深链接：#method / #data / #policy / #axes 直接打开对应视图 */
(function deepLink(){
  const h = (location.hash||'').replace('#','');
  if(h && VIEWS[h] && h!=='map'){
    const btn = document.querySelector(`#tabs .tab[data-v="${h}"]`);
    if(btn) btn.click();
  }
})();

/* ---------- 启动 ---------- */
document.getElementById('s-ver').textContent = DATA.totals.params;
document.getElementById('s-gap').textContent = DATA.totals.gaps;
document.getElementById('s-ver2').textContent = DATA.version;
document.getElementById('s-built').textContent = ' · ' + DATA.built;
drawMethods(); drawData(); drawParams(); drawPolicy(); drawAxes();
overview();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", DATA_JSON)
path = "碳核算框架_交互地图.html"
io.open(path, "w", encoding="utf-8", newline="\n").write(out)
print("已生成 %s  (%.1f KB)" % (path, len(out.encode("utf-8")) / 1024.0))

