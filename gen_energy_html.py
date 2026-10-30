# -*- coding: utf-8 -*-
"""生成《能源经济分析与决策知识系统》交互页面（单文件、离线可用）。

数据来自 energy_core.py（12 域 × 4 层 × 107 问）；碳排放部分桥接 framework_core.py。
"""
import io
import json

from energy_core import build_energy_data

DATA = build_energy_data()
DATA_JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))
_t = DATA["totals"]
print("核对通过: %d 域 / %d 层 / %d 单元 / %d 问 / %d 指标 / %d 数据集 / %d 模型 / 状态 %s"
      % (_t["domains"], _t["layers"], _t["cells"], _t["questions"],
         _t["indicatorCount"], _t["datasets"], _t["models"], _t["byStatus"]))

HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>能源经济分析与决策知识系统</title>
<style>
  :root{
    --bg:#070d1a; --bg2:#0d1730; --card:#121f3a; --card2:#0e1830;
    --line:#26375a; --txt:#e8eefb; --dim:#8ba0c2; --dim2:#5e7ba0;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:radial-gradient(900px 500px at 50% -100px,rgba(30,64,175,.35),transparent 70%),
       linear-gradient(160deg,var(--bg),var(--bg2) 60%,#101c36);
       color:var(--txt);font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;
       min-height:100vh;padding-bottom:60px}
  header{padding:26px 22px 0;max-width:1780px;margin:0 auto}
  h1{font-size:30px;letter-spacing:1px;font-weight:700}
  .sub{color:var(--dim);font-size:14px;margin-top:7px;letter-spacing:.4px;line-height:1.65}
  .stats{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}
  .pill{background:#152441;border:1px solid var(--line);border-radius:20px;
        padding:6px 15px;font-size:13px;color:var(--dim);display:flex;gap:7px;align-items:center}
  .pill b{color:#7dd3fc;font-size:16px;font-weight:700}
  .tabs{max-width:1780px;margin:16px auto 0;padding:0 22px;display:flex;gap:8px;flex-wrap:wrap}
  .tab{cursor:pointer;border:1px solid var(--line);background:#0e1830;color:var(--dim);
       border-radius:10px;padding:9px 16px;font-size:13.5px;font-family:inherit;transition:.15s}
  .tab:hover{border-color:#3f5c8f;color:#c9d8ef}
  .tab.on{background:#17305a;color:#7dd3fc;border-color:#3f5c8f;box-shadow:0 0 0 1px #3f5c8f inset}
  .wrap{max-width:1780px;margin:16px auto 0;padding:0 22px;
        display:grid;grid-template-columns:minmax(0,1fr) 470px;gap:20px;align-items:start}
  .wrap.one{grid-template-columns:1fr}
  .view[hidden]{display:none}
  @media(max-width:1200px){.wrap{grid-template-columns:1fr}}
  .card{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
        border-radius:14px;padding:16px 18px;margin-bottom:14px}
  .card h2{font-size:17px;margin-bottom:6px}
  .card .lead{font-size:13px;color:var(--dim);line-height:1.75;margin-bottom:11px}
  table.tbl{width:100%;border-collapse:collapse;font-size:13px}
  table.tbl th,table.tbl td{border-bottom:1px solid rgba(255,255,255,.08);
        padding:8px 9px;text-align:left;vertical-align:top;line-height:1.6}
  table.tbl th{color:#8ba0c2;font-weight:600;font-size:12px;letter-spacing:.4px;background:rgba(255,255,255,.03)}
  table.tbl td.num{font-variant-numeric:tabular-nums;color:#a5e3ff}
  table.tbl tr:last-child td{border-bottom:none}
  /* 矩阵 */
  .mtx{width:100%;border-collapse:separate;border-spacing:6px}
  .mtx th{font-size:12px;color:#8ba0c2;font-weight:600;padding:6px 4px;text-align:center}
  .mtx th.dh{text-align:left;padding-left:8px}
  .mtx td.dc{font-size:13px;padding:8px 10px;border-radius:9px;
             background:rgba(255,255,255,.035);white-space:nowrap}
  .mtx td.cell{text-align:center;border-radius:9px;padding:14px 6px;cursor:pointer;
               font-size:15px;font-weight:700;font-variant-numeric:tabular-nums;
               transition:.13s;border:1px solid transparent}
  .mtx td.cell:hover{transform:translateY(-2px);border-color:#7dd3fc}
  .mtx td.cell small{display:block;font-size:10px;font-weight:400;color:#8ba0c2;margin-top:2px}
  /* 问题卡 */
  .qcard{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
         border-left:3px solid currentColor;border-radius:12px;padding:12px 14px;margin-bottom:10px;
         cursor:pointer;transition:.14s}
  .qcard:hover{border-color:#3f5c8f;transform:translateY(-1px);box-shadow:0 10px 24px -14px #000}
  .qcard.on{background:#17305a;box-shadow:0 0 0 1.5px currentColor inset}
  .qh{display:flex;gap:9px;align-items:center;margin-bottom:5px;flex-wrap:wrap}
  .qid{font-family:Consolas,monospace;font-size:11.5px;color:#6d86ab}
  .qdom{font-size:12px;font-weight:600}
  .qly{font-size:10.5px;padding:1.5px 7px;border-radius:6px;border:1px solid currentColor;opacity:.9}
  .qst{font-size:10.5px;padding:1.5px 7px;border-radius:6px}
  .qtext{font-size:13.5px;line-height:1.72;color:#dfe9fa}
  .qmeta{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
  .tagx{font-size:10.5px;padding:2px 7px;border-radius:6px;background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.13);color:#a9bfdc;font-family:Consolas,monospace}
  /* 面板 */
  aside{position:sticky;top:14px;max-height:calc(100vh - 30px);overflow:auto;
        background:linear-gradient(165deg,#13203c,#0d172c);border:1px solid var(--line);
        border-radius:18px;padding:18px}
  aside::-webkit-scrollbar{width:8px}
  aside::-webkit-scrollbar-thumb{background:#2b4067;border-radius:4px}
  .p-kicker{font-size:11.5px;letter-spacing:1.4px;color:var(--dim);text-transform:uppercase}
  .p-title{font-size:20px;font-weight:700;margin:6px 0 4px;line-height:1.45}
  .p-meta{font-size:12.5px;color:var(--dim);display:flex;gap:9px;flex-wrap:wrap;align-items:center}
  .sec{margin-top:15px;border-top:1px solid var(--line);padding-top:12px}
  .sec-t{font-size:12px;letter-spacing:1px;color:var(--dim);margin-bottom:8px;
         display:flex;align-items:center;gap:7px}
  .sec-t::before{content:"";width:3px;height:12px;border-radius:2px;background:currentColor}
  .first{font-size:14px;line-height:1.8;color:#dfe9fa;background:rgba(125,211,252,.07);
         border:1px solid rgba(125,211,252,.22);border-radius:11px;padding:12px 13px}
  .formula{font-family:Consolas,"Courier New",monospace;font-size:12.5px;line-height:1.75;
           background:#0a1424;border:1px solid var(--line);border-radius:10px;padding:11px 13px;
           color:#a5e3ff;white-space:pre-wrap;word-break:break-word}
  ul.li{list-style:none;display:grid;gap:7px}
  ul.li li{font-size:13px;line-height:1.65;color:#c8d7ee;padding-left:18px;position:relative}
  ul.li li::before{content:"▸";position:absolute;left:2px;opacity:.65}
  .empty{font-size:13px;color:#5f7599;font-style:italic}
  .hint{font-size:12px;color:#5f7599;line-height:1.72;margin-top:12px}
  .warn{font-size:12.5px;color:#fbbf24;background:rgba(251,191,36,.08);
        border:1px solid rgba(251,191,36,.28);border-radius:9px;padding:9px 11px;line-height:1.72;margin-top:9px}
  .tools{display:flex;gap:8px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
  .search{flex:1;min-width:200px;background:#101c34;border:1px solid var(--line);border-radius:10px;
          padding:9px 13px;color:var(--txt);font-size:13.5px;font-family:inherit;outline:none}
  .search:focus{border-color:#3f5c8f}
  .fbtn{cursor:pointer;background:#101c34;border:1px solid var(--line);color:var(--dim);
        border-radius:9px;padding:7px 11px;font-size:12.5px;font-family:inherit;white-space:nowrap}
  .fbtn.on{color:#7dd3fc;border-color:#3f5c8f;background:#16274a}
  .fsel{background:#101c34;border:1px solid var(--line);border-radius:9px;padding:7px 10px;
        color:var(--dim);font-size:12.5px;font-family:inherit}
  .grid2{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
  .layerbar{display:flex;height:12px;border-radius:6px;overflow:hidden;background:#1b2b49;margin-top:8px}
  .layerbar i{display:block;height:100%}
  .lg{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:var(--dim)}
  .lg i{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:5px}
</style>
</head>
<body>

<header>
  <h1>能源经济分析与决策知识系统</h1>
  <div class="sub">
    FRAMEWORK&nbsp;v4&nbsp;·&nbsp;12 个研究域 × 4 个分析层次 × 8 层证据体系<br>
    碳排放是本系统的一个结果变量模块（05），不是系统的全部；供给、需求、价格、产业、宏观、安全、技术、政策、区域、国际、情景共同构成解释链条。
  </div>
  <div class="stats">
    <div class="pill"><b id="s-dom">0</b>研究域</div>
    <div class="pill"><b id="s-ly">0</b>分析层次</div>
    <div class="pill"><b id="s-q">0</b>条研究问题</div>
    <div class="pill"><b id="s-ind">0</b>个可算指标</div>
    <div class="pill"><b id="s-ds">0</b>个数据集</div>
    <div class="pill"><b id="s-md">0</b>个模型</div>
    <div class="pill" style="border-color:#3f5c8f"><b id="s-ver" style="color:#34d399">v4</b><span id="s-built"></span></div>
  </div>
</header>

<div class="tabs" id="tabs">
  <button class="tab on" data-v="matrix">分析矩阵 · 12×4</button>
  <button class="tab" data-v="qs">研究问题总表</button>
  <button class="tab" data-v="dom">分域详解</button>
  <button class="tab" data-v="models">模型库</button>
  <button class="tab" data-v="data">数据源字典</button>
  <button class="tab" data-v="evid">证据体系</button>
  <button class="tab" data-v="carbon">碳核算子模块</button>
</div>

<div class="wrap one view" id="view-matrix">
  <main id="mMatrix"></main>
</div>

<div class="wrap view" id="view-qs" hidden>
  <main>
    <div class="tools">
      <input class="search" id="q" placeholder="搜索问题 / 指标 / 算式，例如：脱钩、LCOE、MRIO、反弹效应…">
      <select class="fsel" id="fDom"><option value="all">全部域</option></select>
      <select class="fsel" id="fLy"><option value="all">全部层次</option></select>
      <button class="fbtn on" data-f="all">全部状态</button>
      <button class="fbtn" data-f="可算">可算</button>
      <button class="fbtn" data-f="部分可算">部分可算</button>
      <button class="fbtn" data-f="缺关键数据">缺关键数据</button>
    </div>
    <div id="qlist"></div>
  </main>
  <aside id="panel2"></aside>
</div>

<div class="wrap view" id="view-dom" hidden style="grid-template-columns:1fr">
  <main id="mDom"></main>
</div>
<div class="wrap view" id="view-models" hidden style="grid-template-columns:1fr">
  <main id="mModels"></main>
</div>
<div class="wrap view" id="view-data" hidden style="grid-template-columns:1fr">
  <main id="mData"></main>
</div>
<div class="wrap view" id="view-evid" hidden style="grid-template-columns:1fr">
  <main id="mEvid"></main>
</div>
<div class="wrap view" id="view-carbon" hidden style="grid-template-columns:1fr">
  <main id="mCarbon"></main>
</div>

<script>
const DATA = __DATA__;
const SM = DATA.statusMeta;
const LY = {}; DATA.layers.forEach(l=>LY[l.id]=l);
const DOM = {}; DATA.domains.forEach(d=>DOM[d.no]=d);

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function lyName(id){return (LY[id]||{}).name||id;}
function domName(no){return (DOM[no]||{}).name||no;}
function domAccent(no){return (DOM[no]||{}).accent||'#7dd3fc';}

/* ================= 矩阵视图 ================= */
function drawMatrix(){
  const t = DATA.totals;
  const rows = DATA.domains.map(d=>{
    const cells = DATA.layers.map(l=>{
      const n = d.counts[l.id];
      const shade = Math.min(0.62, 0.08 + n*0.075);
      return `<td class="cell" data-dom="${d.no}" data-ly="${l.id}"
        style="background:${d.accent}${Math.round(shade*255).toString(16).padStart(2,'0')};
               color:${n>=4?'#fff':'#dfe9fa'}">${n}<small>${n===0?'空':'问题'}</small></td>`;
    }).join('');
    return `<tr><td class="dc" style="color:${d.accent}">${d.no} ${esc(d.name)}
      <small style="display:block;color:#6d86ab;font-size:11px">${esc(d.sub)}</small></td>${cells}
      <td class="num" style="text-align:center">${d.counts.total}</td></tr>`;
  }).join('');

  const st = t.byStatus;
  const total = t.questions;
  const bars = Object.keys(SM).map(k=>{
    const n = st[k]||0;
    return `<i title="${SM[k][0]} ${n}" style="width:${n/total*100}%;background:${SM[k][1]}"></i>`;
  }).join('');
  const legend = Object.keys(SM).map(k=>{
    const n = st[k]||0;
    return `<span><i style="background:${SM[k][1]}"></i>${SM[k][0]} ${n}（${(n/total*100).toFixed(0)}%）</span>`;
  }).join('');

  const lyRows = DATA.layers.map(l=>`
    <tr><td style="color:${l.accent};font-weight:700">${l.id}</td>
      <td>${esc(l.name)}<div style="font-size:11.5px;color:#6d86ab">${esc(l.sub)}</div></td>
      <td class="num" style="text-align:center">${l.count}</td>
      <td style="font-size:12.5px;color:#a9bfdc">${esc(l.first)}</td></tr>`).join('');

  document.getElementById('mMatrix').innerHTML = `
    <div class="card">
      <h2>12 个研究域 × 4 个分析层次</h2>
      <div class="lead">矩阵里每一个格子都是一个必须回答的问题集合。格子的数值是该单元格的问题条数——
      数字小不代表不重要，而是代表这一层还没被拆细。点击任意单元格可直接筛选问题。</div>
      <table class="mtx">
        <tr><th class="dh">研究域 \ 层次</th>
          ${DATA.layers.map(l=>`<th style="color:${l.accent}">${esc(l.name)}<br>
            <span style="font-weight:400;color:#6d86ab">${esc(l.sub)}</span></th>`).join('')}
          <th>合计</th></tr>
        ${rows}
      </table>
      <div class="lg">
        <span style="color:#8ba0c2">颜色深度 = 该单元格问题条数（越深越多）</span>
      </div>
    </div>

    <div class="card">
      <h2>四个层次各自回答什么</h2>
      <table class="tbl">
        <tr><th style="width:7%">层</th><th style="width:20%">名称 / 追问</th>
            <th style="width:8%">问题数</th><th>这一层的方法论要点</th></tr>
        ${lyRows}
      </table>
      <div class="warn">层次之间不是并列关系而是递进关系：没有 L1 的口径锁定，L2 的机制解释就会在不同边界之间漂移；
      没有 L3 的反事实构造，L4 的情景推演就缺乏可信的基线。</div>
    </div>

    <div class="card">
      <h2>可执行状态分布</h2>
      <div class="lead">「可算」= 算式明确且数据有公开来源；「部分可算」= 算式明确但关键数据缺失或口径需自行编纂；
      「缺关键数据」= 数据源不公开或不存在。三者合计 ${total} 条。</div>
      <div class="layerbar">${bars}</div>
      <div class="lg">${legend}</div>
      <div class="hint">诚实说明：目前只有 ${(st['可算']/total*100).toFixed(0)}% 的问题可以立刻算出数。
      其余不是框架缺陷，而是数据可得性的真实约束——把它们标出来，比假装都能算更有用。</div>
    </div>

    <div class="card">
      <h2>规模</h2>
      <table class="tbl">
        <tr><th style="width:34%">维度</th><th style="width:14%">数量</th><th>说明</th></tr>
        <tr><td>研究域</td><td class="num">${t.domains}</td><td>从能源供给到未来预测的完整链条</td></tr>
        <tr><td>分析层次</td><td class="num">${t.layers}</td><td>事实描述 / 机制解释 / 影响评估 / 未来判断</td></tr>
        <tr><td>矩阵单元格</td><td class="num">${t.cells}</td><td>12 × 4，全部有内容（构建期断言校验）</td></tr>
        <tr><td>研究问题</td><td class="num">${t.questions}</td><td>每条均登记指标、数据、模型、证据层次</td></tr>
        <tr><td>可计算指标</td><td class="num">${t.indicatorCount}</td><td>每个指标都带算式，平均每题 ${(t.indicatorCount/t.questions).toFixed(1)} 个</td></tr>
        <tr><td>数据集</td><td class="num">${t.datasets}</td><td>含口径与已知局限说明</td></tr>
        <tr><td>分析模型</td><td class="num">${t.models}</td><td>含数学形式与适用限度</td></tr>
        <tr><td>证据层次</td><td class="num">${t.evidence}</td><td>统计 / 核算 / 模型 / 因果 / 空间 / 不确定 / 国际 / 情景</td></tr>
      </table>
    </div>`;
}

/* ================= 问题总表 ================= */
function qCard(q){
  const st = SM[q.status];
  const inds = q.ind.map(i=>`<span class="tagx">${esc(i[0])}</span>`).join('');
  return `<div class="qcard" data-id="${q.id}" style="color:${domAccent(q.dom)}">
    <div class="qh">
      <span class="qid">${q.id}</span>
      <span class="qdom" style="color:${domAccent(q.dom)}">${esc(domName(q.dom))}</span>
      <span class="qly" style="color:${LY[q.layer].accent}">${esc(lyName(q.layer))}</span>
      <span class="qst" style="color:${st[1]};background:${st[1]}1f">${st[0]}</span>
    </div>
    <div class="qtext">${esc(q.q)}</div>
    <div class="qmeta">${inds}</div>
  </div>`;
}

let curQ = null;
function drawQList(){
  const box = document.getElementById('qlist');
  box.innerHTML = DATA.questions.map(qCard).join('');
  box.querySelectorAll('.qcard').forEach(el=>{
    el.addEventListener('click', ()=>{
      box.querySelectorAll('.qcard').forEach(x=>x.classList.remove('on'));
      el.classList.add('on');
      showQ(el.dataset.id);
    });
  });
}

function showQ(id){
  const q = DATA.questions.find(x=>x.id===id);
  if(!q) return;
  curQ = id;
  const st = SM[q.status];
  const ind = q.ind.map(i=>`<li><b style="color:#a5e3ff">${esc(i[0])}</b>
    <span style="color:#6d86ab">（${esc(i[1])}）</span><br>
    <span style="font-family:Consolas,monospace;font-size:12px;color:#8fd6ff">${esc(i[2])}</span></li>`).join('');
  const ds = q.data.map(d=>{
    const x = DATA.datasets.find(y=>y.id===d)||{};
    return `<div class="ov" style="margin-bottom:8px">
      <div style="font-size:13px;color:#c8d7ee"><b style="color:#7dd3fc">${d}</b> ${esc(x.name||'')}</div>
      <div style="font-size:11.5px;color:#6d86ab;line-height:1.6">${esc(x.org||'')} · ${esc(x.freq||'')} · ${esc(x.cover||'')}</div>
      <div style="font-size:11.5px;color:#8ba0c2;line-height:1.6">口径/局限：${esc(x.caveat||'')}</div></div>`;
  }).join('');
  const md = q.model.map(m=>{
    const x = DATA.models.find(y=>y.id===m)||{};
    return `<div style="margin-bottom:9px">
      <div style="font-size:13px;color:#c8d7ee"><b style="color:#a78bfa">${m}</b> ${esc(x.name||'')}
        <span style="font-size:11px;color:#6d86ab">[${esc(x.kind||'')}]</span></div>
      <div class="formula" style="margin-top:5px;font-size:11.5px">${esc(x.formula||'')}</div>
      <div style="font-size:11.5px;color:#8ba0c2;line-height:1.6;margin-top:4px">限度：${esc(x.limit||'')}</div>
    </div>`;
  }).join('');
  const ev = q.ev.map(e=>{
    const x = DATA.evidence.find(y=>y.id===e)||{};
    return `<span class="tagx" style="color:${x.accent};border-color:${x.accent}55">${e} ${esc(x.name||'')}</span>`;
  }).join(' ');

  document.getElementById('panel2').innerHTML = `
    <div class="p-kicker" style="color:${domAccent(q.dom)}">${q.id} · ${esc(domName(q.dom))} · ${esc(lyName(q.layer))}</div>
    <div class="p-title">${esc(q.q)}</div>
    <div class="p-meta">
      <span class="tagx" style="color:${st[1]};border-color:${st[1]}55">${st[0]}</span>
      <span>${st[2]}</span>
    </div>

    <div class="sec" style="color:#22d3ee">
      <div class="sec-t">可计算指标与算式（${q.ind.length}）</div>
      <ul class="li">${ind}</ul>
    </div>

    <div class="sec" style="color:#7dd3fc">
      <div class="sec-t">所需数据集（${q.data.length}）</div>
      ${ds}
    </div>

    <div class="sec" style="color:#a78bfa">
      <div class="sec-t">适用模型（${q.model.length}）</div>
      ${md}
    </div>

    <div class="sec" style="color:#34d399">
      <div class="sec-t">证据层次</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap">${ev}</div>
      <div class="hint">证据层次回答的不是「用什么数据」，而是「凭什么让人相信这个结论」。
      同一问题若只挂 E1（统计），只能做描述；要支撑因果陈述必须挂 E4。</div>
    </div>`;
}

/* ================= 分域详解 ================= */
function drawDomains(){
  document.getElementById('mDom').innerHTML = DATA.domains.map(d=>{
    const cellRows = DATA.layers.map(l=>{
      const ids = d.cells[l.id];
      return `<tr><td style="color:${l.accent};white-space:nowrap">${l.id} ${esc(l.name)}</td>
        <td>${ids.map(id=>{
          const q = DATA.questions.find(x=>x.id===id);
          return `<div style="margin:3px 0"><span class="qid">${id}</span>
            <span style="font-size:12.5px;color:#c8d7ee">${esc(q.q)}</span></div>`;
        }).join('')||'<span class="empty">待补</span>'}</td></tr>`;
    }).join('');
    const st = Object.keys(SM).map(k=>{
      const n = d.byStatus[k]||0;
      return n? `<span class="tagx" style="color:${SM[k][1]};border-color:${SM[k][1]}55">${SM[k][0]} ${n}</span>`:'';
    }).join(' ');
    return `<div class="card" style="border-left:3px solid ${d.accent}">
      <h2 style="color:${d.accent}">${d.no} ${esc(d.name)}
        <span style="font-size:12px;color:#6d86ab;font-weight:400">${esc(d.sub)}</span></h2>
      <div class="lead">${esc(d.first)}</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">${st}</div>
      <table class="tbl"><tr><th style="width:16%">层次</th><th>对应研究问题</th></tr>${cellRows}</table>
    </div>`;
  }).join('');
}

/* ================= 模型库 ================= */
function drawModels(){
  document.getElementById('mModels').innerHTML = `
    <div class="card" style="border-left:3px solid #a78bfa">
      <h2>模型库（${DATA.models.length} 个）</h2>
      <div class="lead">每个模型登记数学形式与适用限度。选模型的原则是「先定用途，再选族」：
      解释用简约模型，预测用结构模型，评估用反事实模型——用错族比算错参数更致命。</div>
    </div>
    <div class="card">
      <table class="tbl">
        <tr><th style="width:6%">编号</th><th style="width:16%">名称</th><th style="width:7%">类别</th>
            <th style="width:20%">适用问题</th><th>数学形式 / 要点</th></tr>
        ${DATA.models.map(m=>`<tr>
          <td class="num">${m.id}</td>
          <td><b>${esc(m.name)}</b><div style="font-size:11px;color:#6d86ab">被 ${m.usedBy} 条问题引用</div></td>
          <td style="color:#a78bfa">${esc(m.kind)}</td>
          <td style="font-size:12.5px">${esc(m.use)}
            <div style="font-size:11.5px;color:#fbbf24;margin-top:4px">限度：${esc(m.limit)}</div></td>
          <td><div class="formula" style="font-size:11.5px">${esc(m.formula)}</div></td></tr>`).join('')}
      </table>
    </div>`;
}

/* ================= 数据源字典 ================= */
function drawData(){
  document.getElementById('mData').innerHTML = `
    <div class="card" style="border-left:3px solid #22d3ee">
      <h2>数据源字典（${DATA.datasets.length} 个）</h2>
      <div class="lead">每条登记发布机构、频率、覆盖范围与<b>已知口径局限</b>。
      能源经济研究里最常见的错误不是算错，而是把两个不同口径的数放在一起比。</div>
    </div>
    <div class="card">
      <table class="tbl">
        <tr><th style="width:5%">编号</th><th style="width:19%">名称</th><th style="width:15%">发布机构</th>
            <th style="width:6%">频率</th><th style="width:9%">覆盖</th><th>口径 / 已知局限</th></tr>
        ${DATA.datasets.map(d=>`<tr>
          <td class="num">${d.id}</td><td><b>${esc(d.name)}</b>
            <div style="font-size:11px;color:#6d86ab">被 ${d.usedBy} 条问题引用</div></td>
          <td style="font-size:12.5px">${esc(d.org)}</td>
          <td style="font-size:12.5px">${esc(d.freq)}</td>
          <td style="font-size:12.5px">${esc(d.cover)}</td>
          <td style="font-size:12.5px;color:#a9bfdc">${esc(d.caveat)}</td></tr>`).join('')}
      </table>
    </div>`;
}

/* ================= 证据体系 ================= */
function drawEvid(){
  document.getElementById('mEvid').innerHTML = `
    <div class="card" style="border-left:3px solid #34d399">
      <h2>八层证据体系：凭什么得出结论</h2>
      <div class="lead">前十二个域回答「研究什么」，这一层回答「<b>凭什么让人相信</b>」。
      这是原框架最薄弱的部分——有数据不等于有证据，有模型不等于有结论。</div>
    </div>` +
    DATA.evidence.map(e=>`
      <div class="card" style="border-left:3px solid ${e.accent}">
        <h2 style="color:${e.accent}">${e.id} ${esc(e.name)}
          <span style="font-size:12px;color:#6d86ab;font-weight:400">被 ${e.usedBy} 条问题引用</span></h2>
        <div class="lead">${esc(e.ask)}</div>
        <ul class="li">${e.rules.map(r=>`<li>${esc(r)}</li>`).join('')}</ul>
      </div>`).join('');
}

/* ================= 碳核算子模块 ================= */
function drawCarbon(){
  const c = DATA.carbon||{};
  if(c.error){
    document.getElementById('mCarbon').innerHTML =
      `<div class="card"><h2>碳核算子模块</h2><div class="warn">未接入：${esc(c.error)}</div></div>`;
    return;
  }
  const t = c.totals;
  document.getElementById('mCarbon').innerHTML = `
    <div class="card" style="border-left:3px solid #c084fc">
      <h2>碳核算子模块（原框架，现为「05 能源与碳排放」的下位模块）</h2>
      <div class="lead">原 137 对象碳核算框架并未废弃，而是被<b>降为第五域的实现层</b>。
      它回答的是「排了多少」，而第五域的上位问题还包括「为什么增长」「生产端与消费端差多少」
      「跨区域怎么转移」「强度下降是否等于总量下降」——这四问在子模块里没有，现在补在了 05 域。</div>
      <table class="tbl">
        <tr><th style="width:34%">维度</th><th style="width:16%">数量</th><th>说明</th></tr>
        <tr><td>核算对象</td><td class="num">${t.items}</td><td>8 层结构下的逐条核算对象</td></tr>
        <tr><td>一级模块</td><td class="num">${t.mods}</td><td>双轴标定（M 方法成熟度 / D 数据完备度）</td></tr>
        <tr><td>参数条目</td><td class="num">${t.params}</td><td>其中 ${t.paramsBound} 条已绑定文号级来源、${t.paramsUnbound} 条仅模块级</td></tr>
        <tr><td>待补缺口</td><td class="num">${t.gaps}</td><td>编号对应 missing_data_spec.py</td></tr>
        <tr><td>版本</td><td class="num">${esc(c.version)}</td><td>建立于 ${esc(c.built)}</td></tr>
      </table>
      <div style="margin-top:14px">
        <a href="carbon.html" style="display:inline-block;background:#17305a;border:1px solid #3f5c8f;
           color:#7dd3fc;border-radius:10px;padding:10px 18px;text-decoration:none;font-size:13.5px">
          打开完整碳核算交互地图 →</a>
        <a href="framework-map.svg" style="display:inline-block;background:#12203c;border:1px solid #2f4570;
           color:#9db4d6;border-radius:10px;padding:10px 18px;text-decoration:none;font-size:13.5px;margin-left:8px">
          静态矢量总图 SVG →</a>
      </div>
    </div>

    <div class="card">
      <h2>子模块的 8 层结构</h2>
      <table class="tbl">
        <tr><th style="width:8%">层</th><th style="width:20%">名称</th>
            <th style="width:12%">模块数</th><th style="width:12%">对象数</th></tr>
        ${(c.layers||[]).map(l=>`<tr><td class="num">${l.no}</td><td>${esc(l.name)}</td>
          <td class="num">${l.mods}</td><td class="num">${l.items}</td></tr>`).join('')}
      </table>
    </div>

    <div class="card">
      <h2>本系统仍未完成的事项</h2>
      <ul class="li">
        <li>城市级实证验证：12 域中涉及城市层面的问题（10 域多数）尚无一次完整跑通</li>
        <li>页码级引用：碳子模块 87 条参数已绑定文号，但未逐条核到原文页码</li>
        <li>MRIO 消费端：05-03 / 05-04 需要区域间投入产出表，未接入实际数据</li>
        <li>误差传播：E6 的方法论规则已写，蒙特卡洛未在任一问题上实跑</li>
        <li>宏观模型：06 域多数 L3 问题需要 CGE/DSGE，参数校准未做</li>
        <li>国际比较：E7 的 PPP 与热值口径统一尚未落地到具体指标</li>
      </ul>
    </div>`;
}

/* ================= 交互 ================= */
function applyFilter(){
  const kw = (document.getElementById('q').value||'').trim().toLowerCase();
  const fd = document.getElementById('fDom').value;
  const fl = document.getElementById('fLy').value;
  document.querySelectorAll('#qlist .qcard').forEach(el=>{
    const q = DATA.questions.find(x=>x.id===el.dataset.id);
    const hitKw = !kw || q.q.toLowerCase().includes(kw) ||
      q.ind.some(i=>(i[0]+i[2]).toLowerCase().includes(kw)) ||
      q.id.includes(kw);
    const hitD = fd==='all' || q.dom===fd;
    const hitL = fl==='all' || q.layer===fl;
    const hitS = filter==='all' || q.status===filter;
    el.style.display = (hitKw&&hitD&&hitL&&hitS) ? '' : 'none';
  });
}
let filter='all';

/* ================= Tab ================= */
const VIEWS = {matrix:'view-matrix', qs:'view-qs', dom:'view-dom',
               models:'view-models', data:'view-data', evid:'view-evid', carbon:'view-carbon'};
document.getElementById('tabs').addEventListener('click', ev=>{
  const b = ev.target.closest('.tab'); if(!b) return;
  const v = b.dataset.v;
  Object.keys(VIEWS).forEach(k=>{
    const el = document.getElementById(VIEWS[k]);
    if(el) el.hidden = (k!==v);
  });
  document.querySelectorAll('#tabs .tab').forEach(x=>x.classList.toggle('on', x.dataset.v===v));
  try{ history.replaceState(null,'','#'+v); }catch(e){}
  window.scrollTo(0,0);
});

/* ================= 启动 ================= */
document.getElementById('s-dom').textContent = DATA.totals.domains;
document.getElementById('s-ly').textContent = DATA.totals.layers;
document.getElementById('s-q').textContent = DATA.totals.questions;
document.getElementById('s-ind').textContent = DATA.totals.indicatorCount;
document.getElementById('s-ds').textContent = DATA.totals.datasets;
document.getElementById('s-md').textContent = DATA.totals.models;
document.getElementById('s-ver').textContent = DATA.version;
document.getElementById('s-built').textContent = ' · ' + DATA.built;

drawMatrix(); drawQList(); drawDomains(); drawModels(); drawData(); drawEvid(); drawCarbon();

// 矩阵单元格点击 → 跳到问题总表并筛选
document.getElementById('mMatrix').addEventListener('click', ev=>{
  const cell = ev.target.closest('.cell'); if(!cell) return;
  document.getElementById('fDom').value = cell.dataset.dom;
  document.getElementById('fLy').value = cell.dataset.ly;
  document.querySelector('#tabs .tab[data-v="qs"]').click();
  applyFilter();
});

// 筛选器初始化
const fDom = document.getElementById('fDom');
DATA.domains.forEach(d=>{
  const o = document.createElement('option');
  o.value = d.no; o.textContent = d.no + ' ' + d.name; fDom.appendChild(o);
});
const fLy = document.getElementById('fLy');
DATA.layers.forEach(l=>{
  const o = document.createElement('option');
  o.value = l.id; o.textContent = l.id + ' ' + l.name; fLy.appendChild(o);
});
fDom.addEventListener('change', applyFilter);
fLy.addEventListener('change', applyFilter);
document.getElementById('q').addEventListener('input', applyFilter);
document.querySelectorAll('.fbtn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('on'));
    b.classList.add('on'); filter = b.dataset.f; applyFilter();
  });
});

// 默认展示第一问
if(DATA.questions.length) showQ(DATA.questions[0].id);

// 深链接
(function deepLink(){
  const h = (location.hash||'').replace('#','');
  if(h && VIEWS[h] && h!=='matrix'){
    const btn = document.querySelector(`#tabs .tab[data-v="${h}"]`);
    if(btn) btn.click();
  }
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", DATA_JSON)
path = "能源经济分析系统.html"
io.open(path, "w", encoding="utf-8", newline="\n").write(out)
print("已生成 %s  (%.1f KB)" % (path, len(out.encode("utf-8")) / 1024.0))
