# -*- coding: utf-8 -*-
"""生成《能源经济发展原理与运行机制知识体系》主页面。

定位：解释为主体。首屏是知识目录与阅读区，数据/指标/模型/任务降为支撑材料。
"""
import io
import json
import os

from knowledge_core import build_knowledge_data
from energy_core import build_energy_data

# 网址索引（由 fetch_sources.py 生成）
URL_INDEX = {"total": 0, "archived": 0, "failed": 0, "entries": []}
if os.path.exists(os.path.join("data", "url-index.json")):
    URL_INDEX = json.load(io.open(os.path.join("data", "url-index.json"), encoding="utf-8"))

KD = build_knowledge_data()
ED = build_energy_data()

DATA = {
    "k": KD,
    "tools": {
        "questions": ED["questions"],
        "datasets": ED["datasets"],
        "models": ED["models"],
        "anchors": ED["anchors"],
        "evidence": ED["evidence"],
        "tasks": ED["tasks"],
        "taskSummary": ED["taskSummary"],
        "taskStatus": ED["taskStatus"],
        "taskLevels": ED["taskLevels"],
        "taskStandards": ED["taskStandards"],
        "schemaFields": ED["schemaFields"],
        "coreTables": ED["coreTables"],
        "roadmap": ED["roadmap"],
        "anchorSummary": ED["anchorSummary"],
        "anchorIssues": ED["anchorIssues"],
        "anchorGaps": ED["anchorGaps"],
        "anchorTraps": ED["anchorTraps"],
        "carbon": ED["carbon"],
    },
    "urlIndex": URL_INDEX,
}
DATA_JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))
_t = KD["totals"]
print("核对通过: %d 部分 / %d 模块 / %d 段解释｜支撑 %d 问 / %d 锚点 / %d 数据集 / %d 模型 / %d 任务"
      % (_t["parts"], _t["modules"], _t["sectionCount"], _t["questions"],
         _t["anchors"], _t["datasets"], _t["models"], len(ED["tasks"])))

HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>能源经济发展原理与运行机制</title>
<style>
  :root{
    --bg:#070d1a; --bg2:#0b1426; --card:#111d35; --card2:#0d1729;
    --line:#22344f; --txt:#e9eefb; --dim:#8ba0c2; --dim2:#5e7ba0;
    --accent:#38bdf8;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:radial-gradient(1000px 520px at 50% -140px,rgba(30,64,175,.30),transparent 70%),
       linear-gradient(170deg,var(--bg),var(--bg2) 55%,#0a1222);
       color:var(--txt);font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;
       line-height:1.7;min-height:100vh;padding-bottom:70px}
  /* ---------- 顶栏 ---------- */
  header{padding:30px 26px 0;max-width:1620px;margin:0 auto}
  h1{font-size:29px;letter-spacing:1.2px;font-weight:700}
  .sub{color:var(--dim);font-size:14px;margin-top:8px;line-height:1.75;max-width:900px}
  .pills{display:flex;gap:9px;flex-wrap:wrap;margin-top:15px}
  .pill{background:#132340;border:1px solid var(--line);border-radius:20px;padding:5px 14px;
        font-size:12.5px;color:var(--dim);display:flex;gap:6px;align-items:center}
  .pill b{color:#7dd3fc;font-size:15px;font-weight:700}
  /* ---------- 主导航 ---------- */
  .tabs{max-width:1620px;margin:18px auto 0;padding:0 26px;display:flex;gap:7px;flex-wrap:wrap;
        border-bottom:1px solid var(--line);padding-bottom:0}
  .tab{cursor:pointer;background:none;border:none;border-bottom:2px solid transparent;
       color:var(--dim);padding:11px 15px;font-size:14px;font-family:inherit;transition:.15s}
  .tab:hover{color:#c9d8ef}
  .tab.on{color:#7dd3fc;border-bottom-color:#38bdf8}
  .tab.mgr{color:#5e7ba0;font-size:13px}
  .tab.mgr.on{color:#8ba0c2;border-bottom-color:#3f5c8f}
  .view[hidden]{display:none}
  /* ---------- 阅读布局 ---------- */
  .reader{max-width:1620px;margin:0 auto;padding:24px 26px 0;
          display:grid;grid-template-columns:286px minmax(0,1fr);gap:34px;align-items:start}
  @media(max-width:1080px){.reader{grid-template-columns:1fr;gap:18px}}
  .toc{position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto;padding-right:6px}
  .toc::-webkit-scrollbar{width:7px}
  .toc::-webkit-scrollbar-thumb{background:#26375a;border-radius:4px}
  .toc-part{margin-bottom:16px}
  .toc-ph{font-size:11.5px;letter-spacing:1.1px;color:var(--dim2);margin-bottom:6px;
          display:flex;align-items:center;gap:6px}
  .toc-ph i{width:6px;height:6px;border-radius:50%;display:inline-block}
  .toc-item{display:block;width:100%;text-align:left;background:none;border:none;cursor:pointer;
            color:#b6c7e0;font-size:13.5px;font-family:inherit;padding:6px 9px;border-radius:7px;
            transition:.13s;line-height:1.5}
  .toc-item:hover{background:rgba(255,255,255,.045);color:#e9eefb}
  .toc-item.on{background:#17305a;color:#7dd3fc;font-weight:600}
  .toc-item span{opacity:.5;font-size:11.5px;margin-right:6px;font-family:Consolas,monospace}
  /* ---------- 文章 ---------- */
  article{min-width:0}
  .mh{margin-bottom:26px}
  .mbadge{display:inline-flex;gap:7px;align-items:center;font-size:12px;color:var(--dim);
          border:1px solid var(--line);border-radius:20px;padding:3px 11px;margin-bottom:10px}
  .mh h2{font-size:26px;font-weight:700;letter-spacing:.5px}
  .mh .msub{font-size:15px;color:var(--dim);margin-top:6px}
  .sec8{margin:0 0 30px}
  .sec8-h{display:flex;align-items:baseline;gap:10px;margin-bottom:10px;
          padding-bottom:7px;border-bottom:1px solid var(--line)}
  .sec8-n{font-family:Consolas,monospace;font-size:12.5px;color:#5e7ba0;flex:0 0 auto}
  .sec8-t{font-size:17px;font-weight:700;color:#cfe0f5}
  .sec8-w{font-size:12px;color:#5e7ba0;margin-left:auto;text-align:right}
  @media(max-width:720px){.sec8-w{display:none}}
  .defs{display:grid;gap:11px}
  .def{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
       border-radius:11px;padding:12px 15px}
  .def dt{font-size:14px;font-weight:700;color:#a5d7f5;margin-bottom:4px}
  .def dd{font-size:14px;color:#c8d7ee;line-height:1.78}
  .firstbox{background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.28);
            border-left:4px solid #38bdf8;border-radius:11px;padding:15px 18px;
            font-size:15px;line-height:1.9;color:#dfe9fa}
  .mech{display:grid;gap:0}
  .mech-row{display:grid;grid-template-columns:150px 1fr;gap:14px;padding:11px 0;
            border-bottom:1px dashed rgba(255,255,255,.08)}
  .mech-row:last-child{border-bottom:none}
  .mech-k{font-size:13.5px;font-weight:700;color:#b9a2f0}
  .mech-v{font-size:14px;color:#c8d7ee;line-height:1.78}
  @media(max-width:720px){.mech-row{grid-template-columns:1fr;gap:3px}}
  .tl{position:relative;padding-left:22px}
  .tl::before{content:"";position:absolute;left:5px;top:6px;bottom:6px;width:1.5px;
              background:linear-gradient(#3f5c8f,rgba(63,92,143,.15))}
  .tl-item{position:relative;padding:0 0 15px}
  .tl-item::before{content:"";position:absolute;left:-21px;top:7px;width:8px;height:8px;
                   border-radius:50%;background:#22d3ee;box-shadow:0 0 0 3px rgba(34,211,238,.16)}
  .tl-t{font-size:13.5px;font-weight:700;color:#7dd3fc}
  .tl-d{font-size:14px;color:#c8d7ee;line-height:1.78}
  table.st{width:100%;border-collapse:collapse;font-size:13.5px}
  table.st th,table.st td{border-bottom:1px solid rgba(255,255,255,.08);padding:9px 10px;
        text-align:left;vertical-align:top;line-height:1.7}
  table.st th{color:#8ba0c2;font-weight:600;font-size:12px;background:rgba(255,255,255,.03)}
  table.st tr:last-child td{border-bottom:none}
  .st-val{color:#e9eefb}
  .st-src{font-size:11.5px;color:#6d86ab;white-space:nowrap}
  .st-src a{color:#7dd3fc;text-decoration:none}
  .tens{display:grid;gap:11px}
  .ten{background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.25);
       border-left:4px solid #fbbf24;border-radius:11px;padding:12px 15px}
  .ten b{display:block;font-size:14px;color:#fcd34d;margin-bottom:4px}
  .ten span{font-size:14px;color:#d6c9a8;line-height:1.78}
  .mths{display:grid;gap:9px}
  .mth{background:rgba(34,211,238,.05);border:1px solid rgba(34,211,238,.2);
       border-radius:10px;padding:11px 14px}
  .mth b{font-size:13.5px;color:#67e8f9}
  .mth span{font-size:13.5px;color:#bcd6e6;line-height:1.75}
  .futbox{background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.26);
          border-left:4px solid #34d399;border-radius:11px;padding:15px 18px;
          font-size:15px;line-height:1.9;color:#d9f2e6}
  .modfoot{margin-top:34px;padding-top:18px;border-top:1px solid var(--line);
           display:grid;gap:14px}
  .mf-t{font-size:12px;letter-spacing:1px;color:var(--dim2);margin-bottom:6px}
  .chips{display:flex;gap:7px;flex-wrap:wrap}
  .chipx{font-size:12px;padding:3px 10px;border-radius:7px;border:1px solid currentColor;
         text-decoration:none;cursor:default}
  .guide{display:grid;gap:7px}
  .guide a,.guide div{font-size:13px;color:#b6c7e0;text-decoration:none;padding:6px 10px;
        background:rgba(255,255,255,.035);border-radius:8px;line-height:1.6}
  .guide a:hover{background:rgba(125,211,252,.12);color:#e9eefb}
  .guide .qid{font-family:Consolas,monospace;font-size:11px;color:#5e7ba0;margin-right:7px}
  /* ---------- 首页导语 ---------- */
  .intro{max-width:860px}
  .intro h2{font-size:23px;margin-bottom:12px}
  .intro p{font-size:15px;color:#c8d7ee;line-height:1.95;margin-bottom:14px}
  .intro .q{color:#a5d7f5;font-weight:600}
  .partcards{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));margin-top:24px}
  .pc{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
      border-left:3px solid currentColor;border-radius:12px;padding:15px 17px;cursor:pointer;
      transition:.15s;text-align:left;font-family:inherit}
  .pc:hover{transform:translateY(-2px);box-shadow:0 12px 28px -16px #000}
  .pc h3{font-size:16px;font-weight:700;margin-bottom:4px;color:#e9eefb}
  .pc .pcs{font-size:12.5px;color:var(--dim);margin-bottom:8px}
  .pc ul{list-style:none;display:grid;gap:3px}
  .pc li{font-size:12.5px;color:#a9bfdc}
  .pc li b{color:#7dd3fc;font-family:Consolas,monospace;font-size:11px;margin-right:5px}
  /* ---------- 工具区 ---------- */
  .wrap1{max-width:1620px;margin:0 auto;padding:24px 26px 0}
  .card{background:linear-gradient(150deg,var(--card),var(--card2));border:1px solid var(--line);
        border-radius:14px;padding:17px 19px;margin-bottom:14px}
  .card h2{font-size:17px;margin-bottom:6px}
  .card .lead{font-size:13.5px;color:var(--dim);line-height:1.8;margin-bottom:12px}
  table.tbl{width:100%;border-collapse:collapse;font-size:13px}
  table.tbl th,table.tbl td{border-bottom:1px solid rgba(255,255,255,.08);padding:8px 9px;
        text-align:left;vertical-align:top;line-height:1.65}
  table.tbl th{color:#8ba0c2;font-weight:600;font-size:12px;background:rgba(255,255,255,.03)}
  table.tbl tr:last-child td{border-bottom:none}
  table.tbl td.num{font-variant-numeric:tabular-nums;color:#a5e3ff}
  .formula{font-family:Consolas,monospace;font-size:12px;line-height:1.7;background:#0a1424;
           border:1px solid var(--line);border-radius:9px;padding:9px 11px;color:#a5e3ff;
           white-space:pre-wrap}
  .sub-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
  .stab{cursor:pointer;background:#0f1c33;border:1px solid var(--line);color:var(--dim);
        border-radius:8px;padding:7px 13px;font-size:13px;font-family:inherit}
  .stab.on{color:#7dd3fc;border-color:#3f5c8f;background:#16274a}
  .warn{font-size:13px;color:#fbbf24;background:rgba(251,191,36,.07);
        border:1px solid rgba(251,191,36,.26);border-radius:9px;padding:10px 12px;
        line-height:1.75;margin-top:10px}
  .tagx{font-size:11.5px;padding:2px 8px;border-radius:6px;background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.13);color:#a9bfdc}
  .mgrbar{background:rgba(251,113,133,.08);border:1px solid rgba(251,113,133,.3);
          border-radius:10px;padding:12px 15px;font-size:13px;color:#fda4af;line-height:1.75;
          margin-bottom:14px}
  .tools{display:flex;gap:8px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
  .search{flex:1;min-width:200px;background:#101c34;border:1px solid var(--line);border-radius:9px;
          padding:8px 12px;color:var(--txt);font-size:13px;font-family:inherit;outline:none}
  .fsel{background:#101c34;border:1px solid var(--line);border-radius:8px;padding:7px 10px;
        color:var(--dim);font-size:12.5px;font-family:inherit}
</style>
</head>
<body>

<header>
  <h1>能源经济发展原理与运行机制</h1>
  <div class="sub">
    这个系统只做一件事：<b>解释能源经济如何运行</b>。它不收集数据，也不管理项目——
    数据、指标、模型与任务都在后面作为<b>支撑材料</b>存在，服务于解释。
  </div>
  <div class="pills">
    <div class="pill"><b id="s-parts">0</b>个部分</div>
    <div class="pill"><b id="s-mods">0</b>个知识模块</div>
    <div class="pill"><b id="s-secs">0</b>段解释</div>
    <div class="pill" style="opacity:.72"><b id="s-q">0</b>研究问题</div>
    <div class="pill" style="opacity:.72"><b id="s-a">0</b>数据锚点</div>
    <div class="pill" style="opacity:.72"><b id="s-ds">0</b>数据集</div>
    <div class="pill" style="opacity:.72"><b id="s-md">0</b>模型</div>
    <div class="pill" style="border-color:#3f5c8f"><b style="color:#34d399" id="s-ver">v5</b><span id="s-built"></span></div>
  </div>
</header>

<div class="tabs" id="tabs">
  <button class="tab on" data-v="know">知识体系</button>
  <button class="tab" data-v="carbon">专题 · 碳核算</button>
  <button class="tab" data-v="ref">支撑材料</button>
  <button class="tab mgr" data-v="proj">项目与数据任务 · 内部</button>
</div>

<!-- ============ 知识体系 ============ -->
<div class="view reader" id="view-know">
  <nav class="toc" id="toc"></nav>
  <article id="article"></article>
</div>

<!-- ============ 专题 · 碳核算 ============ -->
<div class="view wrap1" id="view-carbon" hidden>
  <main id="mCarbon"></main>
</div>

<!-- ============ 支撑材料 ============ -->
<div class="view wrap1" id="view-ref" hidden>
  <div class="sub-tabs" id="refTabs">
    <button class="stab on" data-r="ind">指标字典</button>
    <button class="stab" data-r="data">数据资源库</button>
    <button class="stab" data-r="model">方法库</button>
    <button class="stab" data-r="evid">证据与来源</button>
    <button class="stab" data-r="url">网址索引</button>
  </div>
  <main id="mRef"></main>
</div>

<!-- ============ 项目与数据任务 ============ -->
<div class="view wrap1" id="view-proj" hidden>
  <main id="mProj"></main>
</div>

<script>
const DATA = __DATA__;
const K = DATA.k, T = DATA.tools;
const PARTS = {}; K.parts.forEach(p=>PARTS[p.id]=p);
const MODS = {}; K.modules.forEach(m=>MODS[m.id]=m);

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
/* 支持 **强调** 行内标记（先转义再替换，避免注入） */
function fmt(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<b style="color:#7dd3fc">$1</b>');}

/* ================= 目录 ================= */
function drawTOC(){
  document.getElementById('toc').innerHTML = K.parts.map(p=>`
    <div class="toc-part">
      <div class="toc-ph"><i style="background:${p.accent}"></i>${esc(p.name)}</div>
      ${p.modules.map(m=>`<button class="toc-item" data-m="${m.id}">
        <span>${m.id}</span>${esc(m.title)}</button>`).join('')}
    </div>`).join('');
  document.getElementById('toc').addEventListener('click', e=>{
    const b = e.target.closest('.toc-item');
    if(!b) return;
    renderModule(b.dataset.m);
  });
}

/* ================= 首页导语 ================= */
function drawIntro(){
  document.getElementById('article').innerHTML = `
    <div class="intro">
      <h2>这个系统想解释什么</h2>
      <p>能源经济研究的困难不在于缺数据，而在于<span class="q">数字之间没有解释链</span>。
      「2025 年风光装机首超火电」是一个事实，但它不等于「新能源已经主导供给」——
      因为利用小时差 3–5 倍。而「利用率下降」也不等于「新能源没发展好」——
      因为那说明装机跑在了消纳能力前面。</p>
      <p>所以这个系统按五组递进的问题组织：<span class="q">是什么 → 为什么 → 有什么问题 →
      怎么研究 → 会怎么变</span>。每个模块都用同一套八段结构展开，
      从「基本概念」走到「政策与未来」，确保读者能沿着一条完整的解释链读下去，
      而不是在一堆指标之间跳转。</p>
      <p style="color:#8ba0c2;font-size:13.5px">数据、指标、模型、任务都在「支撑材料」与「项目与数据任务」里。
      它们服务于解释，不构成解释本身。</p>
      <div class="partcards">
        ${K.parts.map(p=>`<button class="pc" data-p="${p.id}" style="color:${p.accent}">
          <h3>${p.id}　${esc(p.name)}</h3>
          <div class="pcs">${esc(p.sub)}　·　${p.count} 个模块</div>
          <ul>${p.modules.map(m=>`<li><b>${m.id}</b>${esc(m.title)}</li>`).join('')}</ul>
        </button>`).join('')}
      </div>
    </div>`;
  document.getElementById('article').addEventListener('click', e=>{
    const b = e.target.closest('.pc');
    if(b){ renderModule(PARTS[b.dataset.p].modules[0].id); }
  });
}

/* ================= 模块阅读 ================= */
function renderModule(mid){
  const m = MODS[mid], p = PARTS[m.part];
  document.querySelectorAll('.toc-item').forEach(x=>x.classList.toggle('on', x.dataset.m===mid));

  const S = K.sectionNames;
  const sec = (i, body)=>({i, body});

  const concepts = `<div class="defs">${m.concepts.map(c=>
    `<dl class="def"><dt>${esc(c.t)}</dt><dd>${fmt(c.d)}</dd></dl>`).join('')}</div>`;
  const first = `<div class="firstbox">${fmt(m.first)}</div>`;
  const mech = `<div class="mech">${m.mechanism.map(x=>
    `<div class="mech-row"><div class="mech-k">${esc(x.t)}</div>
     <div class="mech-v">${fmt(x.d)}</div></div>`).join('')}</div>`;
  const hist = `<div class="tl">${m.history.map(x=>
    `<div class="tl-item"><div class="tl-t">${esc(x.t)}</div>
     <div class="tl-d">${fmt(x.d)}</div></div>`).join('')}</div>`;
  const status = `<table class="st">
    <tr><th style="width:26%">指标</th><th style="width:52%">数值 / 说明</th><th>来源</th></tr>
    ${m.status.map(s=>`<tr><td style="color:#a5d7f5">${esc(s.name)}</td>
      <td class="st-val">${esc(s.val)}</td>
      <td class="st-src">${s.src
        ? (s.srcUrl ? `<a href="${s.srcUrl}" target="_blank" rel="noopener">${esc(s.src)}</a>` : esc(s.src))
        : '—'}</td></tr>`).join('')}
    </table>
    <div style="font-size:12px;color:#5e7ba0;margin-top:9px">
      数据口径与完整来源见「支撑材料 → 证据与来源」。同一个指标换口径结论可能相反，引用前请核对口径。</div>`;
  const tens = `<div class="tens">${m.tension.map(x=>
    `<div class="ten"><b>${esc(x.t)}</b><span>${fmt(x.d)}</span></div>`).join('')}</div>`;
  const mths = `<div class="mths">${m.methods.map(x=>
    `<div class="mth"><b>${esc(x.t)}</b><br><span>${fmt(x.d)}</span></div>`).join('')}</div>`;
  const fut = `<div class="futbox">${fmt(m.future)}</div>`;

  const bodies = [concepts, first, mech, hist, status, tens, mths, fut];

  document.getElementById('article').innerHTML = `
    <div class="mh">
      <div class="mbadge" style="color:${p.accent};border-color:${p.accent}55">
        ${p.id}　${esc(p.name)}　·　${esc(p.sub)}</div>
      <h2>${m.id}　${esc(m.title)}</h2>
      <div class="msub">${esc(m.sub)}</div>
    </div>
    ${S.map((s,i)=>`
      <section class="sec8">
        <div class="sec8-h">
          <span class="sec8-n">${String(i+1).padStart(2,'0')}</span>
          <span class="sec8-t">${esc(s.name)}</span>
          <span class="sec8-w">${esc(s.why)}</span>
        </div>
        ${bodies[i]}
      </section>`).join('')}
    <div class="modfoot">
      <div>
        <div class="mf-t">对应研究域（12 域体系）</div>
        <div class="chips">${m.domains.map(d=>
          `<span class="chipx" style="color:${d.accent}">${d.no} ${esc(d.name)}</span>`).join('')}</div>
      </div>
      <div>
        <div class="mf-t">本模块的引导问题（可展开指标与数据需求）</div>
        <div class="guide">${m.questions.map(q=>
          `<a href="#ref"><span class="qid">${q.id}</span>${esc(q.q)}</a>`).join('')}</div>
      </div>
    </div>`;
  window.scrollTo({top:0, behavior:'smooth'});
}

/* ================= 专题 · 碳核算 ================= */
function drawCarbon(){
  const c = T.carbon || {};
  const tt = c.totals || {};
  document.getElementById('mCarbon').innerHTML = `
    <div class="card" style="border-left:3px solid #c084fc">
      <h2>专题 · 碳排放核算</h2>
      <div class="lead">
        碳核算是本知识体系中的<b>一个专题</b>，不是全部。它的定位见 K08（碳排放）：解释「从燃料里的碳
        到大气里的碳」这条链，以及为什么同一份排放可以算出三个不同的数（生产端 / 消费端 / 属地）。
        完整核算对象、参数台账与证据链在独立页面里。
      </div>
      <table class="tbl">
        <tr><th style="width:30%">维度</th><th style="width:16%">数量</th><th>说明</th></tr>
        <tr><td>核算对象</td><td class="num">${tt.items||137}</td><td>8 层结构下的逐条核算对象</td></tr>
        <tr><td>一级模块</td><td class="num">${tt.mods||26}</td><td>双轴标定（M 方法成熟度 / D 数据完备度）</td></tr>
        <tr><td>参数条目</td><td class="num">${tt.params||87}</td><td>${tt.paramsBound||63} 条已绑定文号级来源、${tt.paramsUnbound||24} 条仅模块级</td></tr>
        <tr><td>待补缺口</td><td class="num">${tt.gaps||63}</td><td>已按四标准分类，见「项目与数据任务」</td></tr>
      </table>
      <div style="margin-top:15px">
        <a href="carbon.html" style="display:inline-block;background:#17305a;border:1px solid #3f5c8f;
           color:#7dd3fc;border-radius:10px;padding:10px 18px;text-decoration:none;font-size:13.5px">
          打开完整碳核算地图 →</a>
        <a href="framework-map.svg" style="display:inline-block;background:#12203c;border:1px solid #2f4570;
           color:#9db4d6;border-radius:10px;padding:10px 18px;text-decoration:none;font-size:13.5px;margin-left:8px">
          静态矢量总图 →</a>
      </div>
    </div>
    <div class="card">
      <h2>为什么碳核算不能单独成为体系</h2>
      <div class="lead">
        排放是能源经济的结果变量。只做核算，能回答「排了多少」，但回答不了
        「为什么增长」（需要 K02 需求与 K12 分解）、「价格怎么形成」（K03）、
        「谁承担成本」（K11 与 K15）、「未来怎么变」（K16）。
        这正是本系统把碳核算降为专题的理由。
      </div>
    </div>`;
}

/* ================= 支撑材料 ================= */
let refView = 'ind';
function drawRef(){
  const box = document.getElementById('mRef');
  if(refView==='ind'){
    const qs = T.questions;
    box.innerHTML = `
      <div class="card">
        <h2>指标字典（${qs.length} 条研究问题 / ${qs.reduce((a,q)=>a+q.ind.length,0)} 个指标）</h2>
        <div class="lead">这里是指标与算式的查询入口，不是阅读入口。每条指标都带算式，
        供研究时检索；要理解它为什么存在，请回到对应的知识模块。</div>
        <div class="tools">
          <input class="search" id="qi" placeholder="搜索指标 / 算式 / 问题，例如：LCOE、脱钩、MRIO…">
        </div>
        <table class="tbl" id="tblInd">
          <tr><th style="width:7%">编号</th><th style="width:30%">研究问题</th>
              <th style="width:22%">指标</th><th>算式</th></tr>
          ${qs.map(q=>q.ind.map((i,k)=>`<tr class="indrow">
            <td class="num" style="white-space:nowrap">${k===0?q.id:''}</td>
            <td style="font-size:12.5px">${k===0?esc(q.q):''}</td>
            <td style="color:#a5d7f5;font-size:12.5px">${esc(i[0])}<span style="color:#6d86ab">（${esc(i[1])}）</span></td>
            <td class="formula" style="font-size:11.5px">${esc(i[2])}</td></tr>`).join('')).join('')}
        </table>
      </div>`;
    const inp = document.getElementById('qi');
    inp.addEventListener('input', ()=>{
      const kw = inp.value.trim().toLowerCase();
      document.querySelectorAll('#tblInd .indrow').forEach(tr=>{
        tr.style.display = (!kw || tr.textContent.toLowerCase().includes(kw)) ? '' : 'none';
      });
    });
  } else if(refView==='data'){
    box.innerHTML = `
      <div class="card">
        <h2>数据资源库（${T.datasets.length} 个数据集）</h2>
        <div class="lead">每条登记发布机构、频率、覆盖与<b>已知口径局限</b>。
        能源经济研究里最常见的错误不是算错，而是把两个不同口径的数放在一起比。</div>
        <table class="tbl">
          <tr><th style="width:5%">编号</th><th style="width:19%">名称</th><th style="width:14%">发布机构</th>
              <th style="width:6%">频率</th><th style="width:9%">覆盖</th><th>口径 / 已知局限</th></tr>
          ${T.datasets.map(d=>`<tr><td class="num">${d.id}</td>
            <td><b>${esc(d.name)}</b></td><td style="font-size:12.5px">${esc(d.org)}</td>
            <td style="font-size:12.5px">${esc(d.freq)}</td>
            <td style="font-size:12.5px">${esc(d.cover)}</td>
            <td style="font-size:12.5px;color:#a9bfdc">${esc(d.caveat)}</td></tr>`).join('')}
        </table>
      </div>`;
  } else if(refView==='model'){
    box.innerHTML = `
      <div class="card">
        <h2>方法库（${T.models.length} 个模型）</h2>
        <div class="lead">每个模型登记数学形式与<b>适用限度</b>。选模型的原则是先定用途再选族：
        解释用简约模型，预测用结构模型，评估用反事实模型——用错族比算错参数更致命。
        要理解模型背后的逻辑，请读 K12–K14。</div>
        <table class="tbl">
          <tr><th style="width:6%">编号</th><th style="width:16%">名称</th><th style="width:7%">类别</th>
              <th style="width:19%">适用问题</th><th>数学形式 / 适用限度</th></tr>
          ${T.models.map(m=>`<tr><td class="num">${m.id}</td>
            <td><b>${esc(m.name)}</b></td><td style="color:#a78bfa;font-size:12.5px">${esc(m.kind)}</td>
            <td style="font-size:12.5px">${esc(m.use)}</td>
            <td><div class="formula" style="font-size:11.5px">${esc(m.formula)}</div>
              <div style="font-size:11.5px;color:#fbbf24;margin-top:5px">限度：${esc(m.limit)}</div></td></tr>`).join('')}
        </table>
      </div>`;
  } else if(refView==='url'){
    const U = DATA.urlIndex;
    const okU = U.entries.filter(e=>e.localFile);
    const noU = U.entries.filter(e=>!e.localFile);
    const grp = {};
    okU.forEach(e=>{ (grp[e.kind]=grp[e.kind]||[]).push(e); });
    box.innerHTML = `
      <div class="card" style="border-left:3px solid #34d399">
        <h2>网址索引（${U.total} 条：已归档 ${U.archived} · 未获取 ${U.failed}）</h2>
        <div class="lead">
          这是全部引用来源的<b>可点击索引</b>。左列点开即达原文；右列是已下载到本仓库的副本，
          点击可直接打开（离线可读）。归档器 <code>fetch_sources.py</code> 会记录每个文件的 SHA256，
          可校验内容未被篡改。
        </div>
        <div class="warn">未获取的 ${U.failed} 条不是遗漏，而是站点屏蔽自动抓取或本来就没有公开入口
          （如 IEA / IRENA / EI 返回 403、海关总署返回 412、气象消纳中心无公开入口）。
          这些条目保留原 URL，供人工打开。</div>
      </div>
      ${Object.keys(grp).map(k=>`
        <div class="card">
          <h2>${esc(k)}（${grp[k].length}）</h2>
          <table class="tbl">
            <tr><th style="width:8%">编号</th><th style="width:16%">机构</th>
                <th>原文链接</th><th style="width:26%">本地归档副本</th></tr>
            ${grp[k].map(e=>`<tr>
              <td class="num" style="white-space:nowrap">${esc(e.id)}${e.alias&&e.alias.length?'<div style="font-size:10.5px;color:#6d86ab">'+e.alias.map(esc).join('<br>')+'</div>':''}</td>
              <td style="font-size:12px">${esc(e.org)}</td>
              <td style="font-size:12.5px"><a href="${e.url}" target="_blank" rel="noopener"
                  style="color:#7dd3fc">${esc(e.title||e.url)}</a>
                <div style="font-size:11px;color:#6d86ab">${(()=>{try{return new URL(e.url).hostname}catch(x){return ''}})()}</div></td>
              <td style="font-size:11.5px"><a href="data/${e.localFile}" target="_blank" rel="noopener"
                  style="color:#34d399">${esc(e.localFile.split('/').pop())}</a>
                <div style="color:#6d86ab">${(e.bytes/1024).toFixed(0)} KB</div></td></tr>`).join('')}
          </table>
        </div>`).join('')}
      <div class="card">
        <h2>未获取（${noU.length}）</h2>
        <div class="lead">保留原 URL 与失败原因。这些是最需要人工补的 ${noU.length} 条。</div>
        <table class="tbl">
          <tr><th style="width:8%">编号</th><th style="width:18%">机构</th>
              <th style="width:28%">原因</th><th>原文链接</th></tr>
          ${noU.map(e=>`<tr><td class="num">${esc(e.id)}</td>
            <td style="font-size:12px">${esc(e.org)}</td>
            <td style="font-size:12px;color:#fb7185">${esc(e.error||'—')}</td>
            <td style="font-size:12px">${e.url?`<a href="${e.url}" target="_blank" rel="noopener" style="color:#7dd3fc">${esc(e.url.slice(0,70))}</a>`:'<span style="color:#6d86ab">无公开入口</span>'}</td></tr>`).join('')}
        </table>
      </div>`;
  } else {
    const A = T.anchors;
    box.innerHTML = `
      <div class="card" style="border-left:3px solid #a78bfa">
        <h2>还要看分析视图？</h2>
        <div class="lead">本页「支撑材料」是查询用的精简版。完整的 12×4 分析矩阵、
        107 条研究问题的筛选器、数据锚点台账与四标准任务表在独立分析页里。</div>
        <a href="explorer.html" style="display:inline-block;background:#17305a;border:1px solid #3f5c8f;
           color:#7dd3fc;border-radius:10px;padding:10px 18px;text-decoration:none;font-size:13.5px">
          打开完整分析视图 →</a>
      </div>
      <div class="card">
        <h2>证据与来源（${A.length} 条数据锚点）</h2>
        <div class="lead">知识模块「当前发展状态」里的每个数值，都应能在本表找到对应行与来源链接。
        标注「部分核实 / 计算值」的条目，其可信度低于一手官方数据。</div>
        <table class="tbl">
          <tr><th style="width:5%">编号</th><th style="width:14%">指标</th><th style="width:16%">数值</th>
              <th style="width:6%">年份</th><th style="width:22%">口径说明</th>
              <th style="width:8%">状态</th><th>来源</th></tr>
          ${A.map(a=>`<tr><td class="num">${a.id}</td><td>${esc(a.name)}</td>
            <td style="color:#e9eefb"><b>${esc(a.val)}</b> <span style="color:#6d86ab;font-size:11.5px">${esc(a.unit)}</span></td>
            <td style="font-size:12px">${esc(a.year)}</td>
            <td style="font-size:11.5px;color:#8ba0c2">${esc(a.scope)}</td>
            <td style="font-size:11.5px;color:${a.status==='已核实'?'#34d399':a.status==='部分核实'?'#fbbf24':'#a78bfa'}">${a.status}</td>
            <td style="font-size:11.5px;color:#6d86ab">${esc(a.src)}
              ${a.url?`<div><a href="${a.url}" target="_blank" rel="noopener" style="color:#7dd3fc">原文</a></div>`:''}</td></tr>`).join('')}
        </table>
      </div>
      <div class="card">
        <h2>五个必须先说清的口径陷阱</h2>
        <ul style="list-style:none;display:grid;gap:10px">
          ${T.anchorTraps.map(t=>`<li style="font-size:13px;color:#c8d7ee;line-height:1.8">
            <b style="color:#fbbf24">${esc(t.t)}</b><br><span style="color:#a9bfdc">${esc(t.d)}</span></li>`).join('')}
        </ul>
      </div>`;
  }
}
document.getElementById('refTabs').addEventListener('click', e=>{
  const b = e.target.closest('.stab'); if(!b) return;
  document.querySelectorAll('.stab').forEach(x=>x.classList.toggle('on', x===b));
  refView = b.dataset.r; drawRef();
});

/* ================= 项目与数据任务 ================= */
function drawProj(){
  const TT = T.tasks, S = T.taskSummary, TS = T.taskStatus;
  document.getElementById('mProj').innerHTML = `
    <div class="mgrbar">
      <b>这是内部管理页面，不是知识内容。</b>
      放在这里是为了让数据采集工作有据可查，但读者理解能源经济不需要先读它。
      110 项任务的分类与状态属于项目执行信息；知识解释请看「知识体系」。
    </div>
    <div class="card">
      <h2>数据补充任务总表（${TT.length} 项）</h2>
      <div class="lead">每项按四标准标定：存在性 / 可取得性 / 可计算性 / 可追溯性。
      其中「可获取未取」= 公开可得但还没采；「不可得」= 无公开来源或政策未定。</div>
      <table class="tbl">
        <tr><th style="width:22%">状态</th><th style="width:10%">条数</th><th>含义</th></tr>
        ${Object.keys(TS).map(k=>`<tr><td style="color:${TS[k].accent}">${k}</td>
          <td class="num">${S.byStatus[k]||0}</td>
          <td style="font-size:12.5px">${esc(TS[k].def)}</td></tr>`).join('')}
      </table>
    </div>
    <div class="card">
      <h2>任务清单（${TT.length} 项）</h2>
      <table class="tbl">
        <tr><th style="width:5%">编号</th><th style="width:9%">分类</th><th style="width:26%">指标 / 缺口</th>
            <th style="width:13%">主来源</th><th style="width:13%">替代来源</th>
            <th style="width:11%">四标准</th><th style="width:5%">层</th><th>状态</th></tr>
        ${TT.map(t=>`<tr>
          <td class="num">${t.id}</td>
          <td style="font-size:11.5px;color:#8ba0c2">${esc(t.catName)}</td>
          <td style="font-size:12.5px">${esc(t.name)}</td>
          <td style="font-size:11.5px;color:#a9bfdc">${esc(t.primary)}</td>
          <td style="font-size:11.5px;color:#6d86ab">${esc(t.alt)}</td>
          <td style="font-size:11px;color:#8ba0c2">${t.exist}/${t.access}<br>${t.compute}/${t.trace}</td>
          <td style="font-size:11.5px;color:${(T.taskLevels.find(l=>l.id===t.level)||{}).accent||'#8ba0c2'}">${t.level}</td>
          <td style="font-size:11.5px;color:${TS[t.status].accent};white-space:nowrap">${t.status}</td></tr>`).join('')}
      </table>
    </div>
    <div class="card">
      <h2>六阶段执行顺序</h2>
      <table class="tbl">
        <tr><th style="width:10%">阶段</th><th style="width:20%">工作</th><th style="width:20%">交付</th><th>说明</th></tr>
        ${T.roadmap.map(r=>`<tr><td style="color:#7dd3fc;white-space:nowrap">${esc(r.stage)}</td>
          <td><b>${esc(r.name)}</b></td>
          <td style="font-size:12.5px;color:#a5e3ff">${esc(r.out)}</td>
          <td style="font-size:12.5px;color:#a9bfdc">${esc(r.work)}</td></tr>`).join('')}
      </table>
    </div>`;
}

/* ================= Tab ================= */
const VIEWS = {know:'view-know', carbon:'view-carbon', ref:'view-ref', proj:'view-proj'};
document.getElementById('tabs').addEventListener('click', e=>{
  const b = e.target.closest('.tab'); if(!b) return;
  const v = b.dataset.v;
  Object.keys(VIEWS).forEach(k=>{
    const el = document.getElementById(VIEWS[k]);
    if(el) el.hidden = (k!==v);
  });
  document.querySelectorAll('#tabs .tab').forEach(x=>x.classList.toggle('on', x.dataset.v===v));
  try{ history.replaceState(null,'','#'+v); }catch(err){}
  window.scrollTo({top:0});
});

/* ================= 启动 ================= */
document.getElementById('s-parts').textContent = K.totals.parts;
document.getElementById('s-mods').textContent = K.totals.modules;
document.getElementById('s-secs').textContent = K.totals.sectionCount;
document.getElementById('s-q').textContent = K.totals.questions;
document.getElementById('s-a').textContent = K.totals.anchors;
document.getElementById('s-ds').textContent = K.totals.datasets;
document.getElementById('s-md').textContent = K.totals.models;
document.getElementById('s-ver').textContent = K.version;
document.getElementById('s-built').textContent = ' · ' + K.built;

drawTOC(); drawIntro(); drawCarbon(); drawRef(); drawProj();

// 支撑材料里的引导问题链接：跳到指标字典
document.addEventListener('click', e=>{
  const a = e.target.closest('.guide a');
  if(a){ document.querySelector('.tab[data-v="ref"]').click(); }
});

(function deepLink(){
  const h = (location.hash||'').replace('#','');
  // 支撑材料子页深链接：#ref/url #ref/data #ref/model #ref/evid #ref/ind
  if(h.indexOf('ref/')===0){
    const sub = h.slice(4);
    const tb = document.querySelector('#tabs .tab[data-v="ref"]');
    if(tb) tb.click();
    const sb = document.querySelector('.stab[data-r="'+sub+'"]');
    if(sb) sb.click();
    return;
  }
  // 模块深链接：#K01 ~ #K16
  if(/^K\d\d$/.test(h) && MODS[h]){
    renderModule(h);
    return;
  }
  if(h && VIEWS[h] && h!=='know'){
    const b = document.querySelector(`#tabs .tab[data-v="${h}"]`);
    if(b) b.click();
  }
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", DATA_JSON)
path = "能源经济知识体系.html"
io.open(path, "w", encoding="utf-8", newline="\n").write(out)
print("已生成 %s  (%.1f KB)" % (path, len(out.encode("utf-8")) / 1024.0))
