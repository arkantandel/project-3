<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AWS Data Pipeline — Arkan Tandel</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#0a0c10;--bg2:#111318;--bg3:#1a1d24;--bg4:#22262f;
  --border:#2a2e38;--border2:#3a3f4d;
  --text:#e8eaf0;--text2:#9ca3b0;--text3:#5a6070;
  --green:#22c55e;--green2:#16a34a;--green3:#0d4f2a;
  --blue:#3b82f6;--blue2:#1d4ed8;--blue3:#0d2a6b;
  --orange:#f97316;--orange2:#ea6c0a;--orange3:#5a2a06;
  --purple:#a855f7;--purple2:#7c3aed;--purple3:#3b1a6b;
  --cyan:#06b6d4;--cyan2:#0891b2;--cyan3:#083344;
  --red:#ef4444;--yellow:#eab308;
  --r:8px;--r2:12px;--r3:16px;
}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;overflow-x:hidden;line-height:1.6;}
/* HERO */
.hero{position:relative;padding:70px 40px 60px;text-align:center;overflow:hidden;border-bottom:1px solid var(--border);}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:40px 40px;opacity:0.3;}
.hero-glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:300px;background:radial-gradient(ellipse,rgba(59,130,246,0.12) 0%,transparent 70%);pointer-events:none;}
.hero-content{position:relative;z-index:1;}
.badge-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:24px;}
.badge{padding:4px 12px;border-radius:20px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;border:1px solid;letter-spacing:0.5px;}
.badge-blue{background:var(--blue3);border-color:var(--blue);color:var(--blue);}
.badge-green{background:var(--green3);border-color:var(--green);color:var(--green);}
.badge-orange{background:var(--orange3);border-color:var(--orange);color:var(--orange);}
.badge-purple{background:var(--purple3);border-color:var(--purple);color:var(--purple);}
.badge-cyan{background:var(--cyan3);border-color:var(--cyan);color:var(--cyan);}
h1{font-size:clamp(28px,5vw,52px);font-weight:700;line-height:1.1;margin-bottom:12px;}
h1 span{background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:16px;color:var(--text2);margin-bottom:8px;}
.hero-meta{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text3);margin-top:16px;}
.hero-meta span{color:var(--green);margin:0 4px;}
/* NAV */
.toc{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 40px;display:flex;gap:0;overflow-x:auto;position:sticky;top:0;z-index:100;}
.toc a{padding:14px 18px;font-size:13px;color:var(--text2);text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent;transition:all .2s;font-weight:500;}
.toc a:hover,.toc a.active{color:var(--blue);border-bottom-color:var(--blue);}
/* SECTIONS */
.section{padding:60px 40px;border-bottom:1px solid var(--border);max-width:1100px;margin:0 auto;}
.section-label{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--blue);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.section-title{font-size:28px;font-weight:700;margin-bottom:8px;}
.section-desc{color:var(--text2);font-size:15px;margin-bottom:36px;max-width:600px;}
/* PIPELINE DIAGRAM */
#diagram{padding:60px 40px;border-bottom:1px solid var(--border);}
.pipeline-wrap{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r3);padding:40px 20px;overflow:hidden;position:relative;}
svg.pipeline{width:100%;max-width:900px;display:block;margin:0 auto;}
/* STEPS */
.steps{display:flex;flex-direction:column;gap:0;}
.step{display:flex;gap:24px;position:relative;}
.step:not(:last-child)::after{content:'';position:absolute;left:19px;top:52px;bottom:0;width:2px;background:linear-gradient(var(--border2),var(--border));}
.step-num{width:40px;height:40px;border-radius:50%;background:var(--bg3);border:2px solid var(--border2);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--blue);flex-shrink:0;margin-top:6px;position:relative;z-index:1;transition:all .3s;}
.step:hover .step-num{background:var(--blue3);border-color:var(--blue);}
.step-body{padding:6px 0 40px;}
.step-title{font-size:18px;font-weight:600;margin-bottom:6px;display:flex;align-items:center;gap:10px;}
.step-title .icon{font-size:18px;}
.step-desc{color:var(--text2);font-size:14px;margin-bottom:16px;line-height:1.7;}
.code-block{background:var(--bg);border:1px solid var(--border);border-radius:var(--r);padding:16px 20px;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.8;position:relative;overflow:auto;}
.code-block .comment{color:var(--text3);}
.code-block .cmd{color:var(--green);}
.code-block .flag{color:var(--cyan);}
.code-block .val{color:var(--orange);}
.code-block .kw{color:var(--purple);}
.code-block .str{color:var(--yellow);}
.copy-btn{position:absolute;top:10px;right:10px;background:var(--bg3);border:1px solid var(--border2);color:var(--text2);padding:4px 10px;border-radius:6px;font-size:11px;cursor:pointer;font-family:'JetBrains Mono',monospace;transition:all .2s;}
.copy-btn:hover{background:var(--border2);color:var(--text);}
.tip-box{background:var(--blue3);border:1px solid var(--blue2);border-left:3px solid var(--blue);border-radius:var(--r);padding:12px 16px;font-size:13px;color:#bfdbfe;margin-top:12px;}
.tip-box strong{color:var(--blue);display:block;margin-bottom:2px;font-size:12px;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:1px;}
/* FILES */
.file-tree{background:var(--bg);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;}
.file-tree-header{background:var(--bg3);padding:10px 16px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text3);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;}
.dot{width:12px;height:12px;border-radius:50%;}
.file-item{display:flex;gap:12px;padding:10px 20px;border-bottom:1px solid var(--border);align-items:flex-start;cursor:pointer;transition:background .15s;}
.file-item:hover{background:var(--bg3);}
.file-item:last-child{border-bottom:none;}
.file-icon{font-family:'JetBrains Mono',monospace;font-size:12px;padding:2px 8px;border-radius:4px;flex-shrink:0;margin-top:2px;}
.fi-py{background:#1e3a5f;color:#60a5fa;}
.fi-docker{background:#0d3b5e;color:#38bdf8;}
.fi-txt{background:#1a2e1a;color:#4ade80;}
.fi-csv{background:#2d2006;color:#facc15;}
.fi-md{background:#2a1a4a;color:#c084fc;}
.file-name{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;margin-bottom:2px;}
.file-desc{font-size:13px;color:var(--text2);}
/* SERVICES TABLE */
.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;}
.service-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:20px;transition:all .2s;cursor:default;}
.service-card:hover{border-color:var(--border2);transform:translateY(-2px);}
.service-icon{font-size:24px;margin-bottom:12px;}
.service-name{font-size:14px;font-weight:600;margin-bottom:4px;}
.service-role{font-size:13px;color:var(--text2);line-height:1.5;}
/* OUTPUT */
.terminal{background:#0a0e0a;border:1px solid #1a2e1a;border-radius:var(--r2);overflow:hidden;}
.terminal-bar{background:#111811;padding:10px 16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid #1a2e1a;}
.terminal-title{font-family:'JetBrains Mono',monospace;font-size:11px;color:#4b5563;}
.terminal-body{padding:20px 24px;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:2;}
.t-prompt{color:#4ade80;}
.t-cmd{color:#e2e8f0;}
.t-out-ok{color:#22c55e;display:flex;align-items:center;gap:8px;}
.t-out-warn{color:#f59e0b;}
.t-cursor{display:inline-block;width:8px;height:14px;background:#22c55e;animation:blink 1s step-end infinite;vertical-align:middle;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
/* CHALLENGES */
.challenges{display:flex;flex-direction:column;gap:12px;}
.challenge{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:18px 20px;display:flex;gap:16px;align-items:flex-start;}
.ch-num{width:28px;height:28px;border-radius:50%;background:var(--orange3);border:1px solid var(--orange);color:var(--orange);font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:600;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.ch-title{font-size:14px;font-weight:600;margin-bottom:4px;}
.ch-sol{font-size:13px;color:var(--text2);}
.ch-sol strong{color:var(--green);font-weight:500;}
/* FOOTER */
.footer{background:var(--bg2);border-top:1px solid var(--border);padding:30px 40px;text-align:center;}
.footer-name{font-size:15px;font-weight:600;margin-bottom:4px;}
.footer-sub{font-size:13px;color:var(--text3);}
/* ANIMATIONS */
@keyframes flowDash{to{stroke-dashoffset:-40;}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
@keyframes slideIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.animate-in{animation:slideIn .5s ease forwards;}
.flow-arrow{stroke-dasharray:8 4;animation:flowDash 1.2s linear infinite;}
.flow-arrow-slow{stroke-dasharray:8 4;animation:flowDash 2s linear infinite;}
.pulse-dot{animation:pulse 2s ease-in-out infinite;}
/* SCROLLBAR */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
</style>
</head>
<body>

<!-- HERO -->
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-glow"></div>
  <div class="hero-content">
    <div class="badge-row">
      <span class="badge badge-blue">Python 3.9</span>
      <span class="badge badge-cyan">Docker</span>
      <span class="badge badge-orange">AWS S3</span>
      <span class="badge badge-green">Amazon RDS</span>
      <span class="badge badge-purple">AWS Glue</span>
    </div>
    <h1>AWS Data Ingestion<br/><span>Pipeline</span></h1>
    <div class="hero-sub">S3 → RDS (MySQL) with Glue Fallback · Dockerized Python App</div>
    <div class="hero-meta">
      Author <span>Arkan Tandel</span> · Batch <span>28 July</span> · MCA · Fortune Cloud Technologies
    </div>
  </div>
</div>

<!-- NAV -->
<nav class="toc">
  <a href="#overview" class="active">Overview</a>
  <a href="#diagram">Architecture</a>
  <a href="#structure">Files</a>
  <a href="#services">Services</a>
  <a href="#steps">Setup Guide</a>
  <a href="#output">Output</a>
  <a href="#challenges">Challenges</a>
</nav>

<!-- OVERVIEW -->
<div id="overview" class="section">
  <div class="section-label">01 · Overview</div>
  <div class="section-title">What this project does</div>
  <div class="section-desc">A fault-tolerant cloud data pipeline that runs end-to-end inside Docker.</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;">
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:20px;">
      <div style="font-size:22px;margin-bottom:10px;">📥</div>
      <div style="font-size:14px;font-weight:600;margin-bottom:4px;">Read from S3</div>
      <div style="font-size:13px;color:var(--text2);">CSV file is fetched from an Amazon S3 bucket using boto3 and loaded into a pandas DataFrame.</div>
    </div>
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:20px;">
      <div style="font-size:22px;margin-bottom:10px;">📤</div>
      <div style="font-size:14px;font-weight:600;margin-bottom:4px;">Insert into RDS</div>
      <div style="font-size:13px;color:var(--text2);">Data is pushed into Amazon RDS (MySQL) using SQLAlchemy + PyMySQL as the primary destination.</div>
    </div>
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:20px;">
      <div style="font-size:22px;margin-bottom:10px;">⚡</div>
      <div style="font-size:14px;font-weight:600;margin-bottom:4px;">Glue Fallback</div>
      <div style="font-size:13px;color:var(--text2);">If RDS fails, the app automatically creates an external table in AWS Glue Data Catalog pointing to S3.</div>
    </div>
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:20px;">
      <div style="font-size:22px;margin-bottom:10px;">🐳</div>
      <div style="font-size:14px;font-weight:600;margin-bottom:4px;">Dockerized</div>
      <div style="font-size:13px;color:var(--text2);">Entire app packaged in Docker. Runs consistently on any environment — EC2, local, CI/CD.</div>
    </div>
  </div>
</div>

<!-- ARCHITECTURE DIAGRAM -->
<div id="diagram" style="padding:60px 40px;border-bottom:1px solid var(--border);">
  <div style="max-width:1100px;margin:0 auto;">
    <div class="section-label">02 · Architecture</div>
    <div class="section-title">How data flows through the pipeline</div>
    <div class="section-desc">Watch the live data flow — the diagram shows both primary path (green) and fallback path (orange).</div>
    <div class="pipeline-wrap">
      <svg class="pipeline" viewBox="0 0 860 460" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrowG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M2 1L8 5L2 9" fill="none" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
          <marker id="arrowO" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M2 1L8 5L2 9" fill="none" stroke="#f97316" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
          <marker id="arrowR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M2 1L8 5L2 9" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>

        <!-- ── CSV FILE ── -->
        <rect x="30" y="180" width="100" height="60" rx="8" fill="#1a2e1a" stroke="#22c55e" stroke-width="1"/>
        <text x="80" y="206" text-anchor="middle" fill="#4ade80" font-family="JetBrains Mono" font-size="10" font-weight="600">sample_data</text>
        <text x="80" y="222" text-anchor="middle" fill="#4ade80" font-family="JetBrains Mono" font-size="10">.csv</text>
        <text x="80" y="256" text-anchor="middle" fill="#6b7280" font-family="Space Grotesk" font-size="10">Source file</text>

        <!-- CSV → S3 arrow -->
        <line x1="130" y1="210" x2="168" y2="210" stroke="#22c55e" stroke-width="1.5" class="flow-arrow" marker-end="url(#arrowG)"/>
        <text x="149" y="204" text-anchor="middle" fill="#16a34a" font-family="JetBrains Mono" font-size="9">upload</text>

        <!-- ── S3 BUCKET ── -->
        <rect x="170" y="150" width="130" height="120" rx="10" fill="#0d2a6b" stroke="#3b82f6" stroke-width="1.5"/>
        <text x="235" y="180" text-anchor="middle" fill="#60a5fa" font-family="JetBrains Mono" font-size="11" font-weight="600">Amazon S3</text>
        <rect x="185" y="190" width="100" height="28" rx="4" fill="#1e3a8a" stroke="#2563eb" stroke-width="0.5"/>
        <text x="235" y="208" text-anchor="middle" fill="#93c5fd" font-family="JetBrains Mono" font-size="9">data-pipeline-bucket</text>
        <text x="235" y="284" text-anchor="middle" fill="#6b7280" font-family="Space Grotesk" font-size="10">Object storage</text>

        <!-- S3 → Docker arrow -->
        <line x1="300" y1="210" x2="348" y2="210" stroke="#22c55e" stroke-width="1.5" class="flow-arrow" marker-end="url(#arrowG)"/>
        <text x="324" y="204" text-anchor="middle" fill="#16a34a" font-family="JetBrains Mono" font-size="9">boto3</text>

        <!-- ── DOCKER CONTAINER ── -->
        <rect x="350" y="100" width="190" height="220" rx="12" fill="#0c1220" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6 3"/>
        <text x="445" y="130" text-anchor="middle" fill="#7dd3fc" font-family="JetBrains Mono" font-size="11" font-weight="600">Docker Container</text>
        <!-- app.py box inside -->
        <rect x="368" y="142" width="154" height="70" rx="6" fill="#0d2a3d" stroke="#0891b2" stroke-width="1"/>
        <text x="445" y="162" text-anchor="middle" fill="#38bdf8" font-family="JetBrains Mono" font-size="10" font-weight="600">app.py</text>
        <text x="445" y="178" text-anchor="middle" fill="#6ba5bf" font-family="JetBrains Mono" font-size="9">read_from_s3()</text>
        <text x="445" y="193" text-anchor="middle" fill="#6ba5bf" font-family="JetBrains Mono" font-size="9">upload_to_rds()</text>
        <text x="445" y="208" text-anchor="middle" fill="#6ba5bf" font-family="JetBrains Mono" font-size="9">fallback_to_glue()</text>
        <!-- Python version badge -->
        <rect x="368" y="226" width="70" height="22" rx="4" fill="#1e1a3a" stroke="#7c3aed" stroke-width="0.5"/>
        <text x="403" y="240" text-anchor="middle" fill="#a78bfa" font-family="JetBrains Mono" font-size="9">Python 3.9</text>
        <rect x="452" y="226" width="70" height="22" rx="4" fill="#1a2e1a" stroke="#16a34a" stroke-width="0.5"/>
        <text x="487" y="240" text-anchor="middle" fill="#4ade80" font-family="JetBrains Mono" font-size="9">boto3+pandas</text>
        <text x="445" y="332" text-anchor="middle" fill="#6b7280" font-family="Space Grotesk" font-size="10">Containerized app</text>

        <!-- ── PRIMARY PATH: Docker → RDS ── -->
        <line x1="540" y1="185" x2="588" y2="185" stroke="#22c55e" stroke-width="2" class="flow-arrow" marker-end="url(#arrowG)"/>
        <text x="564" y="178" text-anchor="middle" fill="#16a34a" font-family="JetBrains Mono" font-size="9">SUCCESS</text>

        <!-- ── RDS ── -->
        <rect x="590" y="130" width="140" height="110" rx="10" fill="#0d4f2a" stroke="#22c55e" stroke-width="1.5"/>
        <text x="660" y="160" text-anchor="middle" fill="#4ade80" font-family="JetBrains Mono" font-size="11" font-weight="600">Amazon RDS</text>
        <text x="660" y="176" text-anchor="middle" fill="#16a34a" font-family="JetBrains Mono" font-size="9">MySQL</text>
        <rect x="608" y="186" width="104" height="38" rx="4" fill="#0a3d1e" stroke="#15803d" stroke-width="0.5"/>
        <text x="660" y="201" text-anchor="middle" fill="#86efac" font-family="JetBrains Mono" font-size="9">DB: testdb</text>
        <text x="660" y="215" text-anchor="middle" fill="#86efac" font-family="JetBrains Mono" font-size="9">Table: mytable</text>
        <!-- Pulse dot on RDS -->
        <circle cx="726" cy="140" r="5" fill="#22c55e" class="pulse-dot"/>
        <text x="660" y="258" text-anchor="middle" fill="#6b7280" font-family="Space Grotesk" font-size="10">Primary database</text>

        <!-- ── FAILURE PATH label ── -->
        <text x="445" y="295" text-anchor="middle" fill="#ef4444" font-family="JetBrains Mono" font-size="9" font-weight="600">if RDS fails →</text>

        <!-- Docker → Glue (fallback path) -->
        <path d="M445 320 L445 370 L630 370" fill="none" stroke="#f97316" stroke-width="1.5" stroke-dasharray="6 3" class="flow-arrow-slow" marker-end="url(#arrowO)"/>

        <!-- ── AWS GLUE ── -->
        <rect x="630" y="340" width="160" height="90" rx="10" fill="#5a2a06" stroke="#f97316" stroke-width="1.5" stroke-dasharray="5 3"/>
        <text x="710" y="368" text-anchor="middle" fill="#fdba74" font-family="JetBrains Mono" font-size="11" font-weight="600">AWS Glue</text>
        <text x="710" y="384" text-anchor="middle" fill="#f97316" font-family="JetBrains Mono" font-size="9">Data Catalog</text>
        <rect x="648" y="392" width="124" height="26" rx="4" fill="#451a03" stroke="#b45309" stroke-width="0.5"/>
        <text x="710" y="408" text-anchor="middle" fill="#fcd34d" font-family="JetBrains Mono" font-size="9">EXTERNAL_TABLE → S3</text>
        <text x="710" y="448" text-anchor="middle" fill="#6b7280" font-family="Space Grotesk" font-size="10">Fallback catalog</text>

        <!-- LEGEND -->
        <line x1="30" y1="420" x2="60" y2="420" stroke="#22c55e" stroke-width="2" class="flow-arrow" marker-end="url(#arrowG)"/>
        <text x="68" y="424" fill="#6b7280" font-family="Space Grotesk" font-size="11">Primary path</text>
        <line x1="160" y1="420" x2="190" y2="420" stroke="#f97316" stroke-width="1.5" stroke-dasharray="5 3" class="flow-arrow-slow" marker-end="url(#arrowO)"/>
        <text x="198" y="424" fill="#6b7280" font-family="Space Grotesk" font-size="11">Fallback path</text>
      </svg>

      <!-- Toggle buttons -->
      <div style="display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap;">
        <button onclick="setPath('both')" id="btn-both" style="padding:8px 20px;border-radius:20px;border:1px solid var(--green);background:var(--green3);color:var(--green);font-size:13px;cursor:pointer;font-family:'Space Grotesk',sans-serif;font-weight:500;">Both Paths</button>
        <button onclick="setPath('primary')" id="btn-primary" style="padding:8px 20px;border-radius:20px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:13px;cursor:pointer;font-family:'Space Grotesk',sans-serif;font-weight:500;">Primary Only (RDS)</button>
        <button onclick="setPath('fallback')" id="btn-fallback" style="padding:8px 20px;border-radius:20px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:13px;cursor:pointer;font-family:'Space Grotesk',sans-serif;font-weight:500;">Fallback Only (Glue)</button>
      </div>
    </div>
  </div>
</div>

<!-- PROJECT STRUCTURE -->
<div id="structure" class="section">
  <div class="section-label">03 · Project Structure</div>
  <div class="section-title">Repository files</div>
  <div class="section-desc">Click any file to see what it contains.</div>
  <div class="file-tree">
    <div class="file-tree-header">
      <div class="dot" style="background:#ef4444;"></div>
      <div class="dot" style="background:#f59e0b;"></div>
      <div class="dot" style="background:#22c55e;"></div>
      <span style="margin-left:8px;">aws-pipeline/</span>
    </div>
    <div class="file-item" onclick="toggleCode('code-app')">
      <div class="file-icon fi-py">.py</div>
      <div>
        <div class="file-name">app.py</div>
        <div class="file-desc">Main Python script — reads S3, inserts into RDS, falls back to Glue</div>
      </div>
    </div>
    <div class="code-block" id="code-app" style="display:none;border-radius:0;border-left:none;border-right:none;border-top:none;">
<span class="comment"># ── IMPORTS ──────────────────────────────────────────</span>
<span class="kw">import</span> os, boto3, pandas <span class="kw">as</span> pd
<span class="kw">from</span> sqlalchemy <span class="kw">import</span> create_engine
<span class="kw">from</span> botocore.exceptions <span class="kw">import</span> ClientError

<span class="comment"># ── ENV VARIABLES ────────────────────────────────────</span>
S3_BUCKET  = os.getenv(<span class="str">"S3_BUCKET"</span>)
RDS_HOST   = os.getenv(<span class="str">"RDS_HOST"</span>)
GLUE_DB    = os.getenv(<span class="str">"GLUE_DB"</span>)

<span class="comment"># ── FUNCTIONS ────────────────────────────────────────</span>
<span class="kw">def</span> <span class="cmd">read_from_s3</span>():
    s3  = boto3.client(<span class="str">"s3"</span>)
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    <span class="kw">return</span> pd.read_csv(obj[<span class="str">"Body"</span>])

<span class="kw">def</span> <span class="cmd">upload_to_rds</span>(df):
    engine = create_engine(<span class="str">f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}/{RDS_DB}"</span>)
    df.to_sql(RDS_TABLE, con=engine, if_exists=<span class="str">"replace"</span>, index=<span class="val">False</span>)

<span class="kw">def</span> <span class="cmd">fallback_to_glue</span>():
    glue = boto3.client(<span class="str">"glue"</span>)
    glue.create_table(DatabaseName=GLUE_DB, TableInput={...})

<span class="kw">def</span> <span class="cmd">main</span>():
    <span class="kw">try</span>:
        df = read_from_s3()
        upload_to_rds(df)         <span class="comment"># ✅ Primary path</span>
    <span class="kw">except</span> Exception:
        fallback_to_glue()        <span class="comment"># ⚡ Fallback</span></div>
    <div class="file-item" onclick="toggleCode('code-docker')">
      <div class="file-icon fi-docker">🐳</div>
      <div>
        <div class="file-name">Dockerfile</div>
        <div class="file-desc">Container config — Python 3.9 base with all dependencies</div>
      </div>
    </div>
    <div class="code-block" id="code-docker" style="display:none;border-radius:0;border-left:none;border-right:none;border-top:none;">
<span class="kw">FROM</span> <span class="val">python:3.9</span>

<span class="kw">WORKDIR</span> <span class="str">/app</span>

<span class="kw">COPY</span> requirements.txt <span class="str">.</span>
<span class="kw">RUN</span>  <span class="cmd">pip install</span> <span class="flag">-r</span> requirements.txt

<span class="kw">COPY</span> app.py <span class="str">.</span>

<span class="kw">CMD</span> [<span class="str">"python"</span>, <span class="str">"app.py"</span>]</div>
    <div class="file-item" onclick="toggleCode('code-req')">
      <div class="file-icon fi-txt">.txt</div>
      <div>
        <div class="file-name">requirements.txt</div>
        <div class="file-desc">All Python library dependencies</div>
      </div>
    </div>
    <div class="code-block" id="code-req" style="display:none;border-radius:0;border-left:none;border-right:none;border-top:none;">
<span class="cmd">boto3</span>
<span class="cmd">pandas</span>
<span class="cmd">sqlalchemy</span>
<span class="cmd">pymysql</span>
<span class="cmd">cryptography</span></div>
    <div class="file-item" onclick="toggleCode('code-csv')">
      <div class="file-icon fi-csv">.csv</div>
      <div>
        <div class="file-name">sample_data.csv</div>
        <div class="file-desc">Test dataset uploaded to S3 to verify the pipeline</div>
      </div>
    </div>
    <div class="code-block" id="code-csv" style="display:none;border-radius:0;border-left:none;border-right:none;border-top:none;">
<span class="str">id,name,age</span>
<span class="val">1,Arkan,22</span>
<span class="val">2,Rahul,25</span>
<span class="val">3,Amit,28</span></div>
    <div class="file-item" onclick="toggleCode('code-md')">
      <div class="file-icon fi-md">.md</div>
      <div>
        <div class="file-name">README.md</div>
        <div class="file-desc">Project documentation — this file you are reading right now</div>
      </div>
    </div>
  </div>
</div>

<!-- SERVICES -->
<div id="services" class="section">
  <div class="section-label">04 · AWS Services</div>
  <div class="section-title">Cloud services used</div>
  <div class="section-desc">Five services working together to build the pipeline.</div>
  <div class="services-grid">
    <div class="service-card" style="border-top:2px solid var(--orange);">
      <div class="service-icon">📦</div>
      <div class="service-name">Amazon S3</div>
      <div class="service-role">Stores source CSV file. Read with <code style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--cyan);">boto3.get_object()</code>. Acts as the data lake.</div>
    </div>
    <div class="service-card" style="border-top:2px solid var(--green);">
      <div class="service-icon">🗄️</div>
      <div class="service-name">Amazon RDS (MySQL)</div>
      <div class="service-role">Primary database destination. Data inserted using SQLAlchemy + PyMySQL engine.</div>
    </div>
    <div class="service-card" style="border-top:2px solid var(--orange);">
      <div class="service-icon">🔗</div>
      <div class="service-name">AWS Glue</div>
      <div class="service-role">Fallback — creates an external table in Glue Data Catalog if RDS is unavailable.</div>
    </div>
    <div class="service-card" style="border-top:2px solid var(--cyan);">
      <div class="service-icon">💻</div>
      <div class="service-name">Amazon EC2</div>
      <div class="service-role">Ubuntu server where Docker container is built and run. us-east-1 region.</div>
    </div>
    <div class="service-card" style="border-top:2px solid var(--blue);">
      <div class="service-icon">🐳</div>
      <div class="service-name">Docker</div>
      <div class="service-role">Packages app + all dependencies into a portable container image for consistent deployment.</div>
    </div>
  </div>
</div>

<!-- STEP BY STEP GUIDE -->
<div id="steps" class="section">
  <div class="section-label">05 · Setup Guide</div>
  <div class="section-title">Step-by-step project creation</div>
  <div class="section-desc">Follow each step exactly to recreate this project from scratch.</div>

  <div class="steps">

    <div class="step">
      <div class="step-num">01</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">📦</span> Create S3 Bucket &amp; Upload CSV</div>
        <div class="step-desc">Log in to AWS Console → S3 → Create Bucket. Then upload your sample CSV file to be used as the data source.</div>
        <div class="code-block">
<span class="comment"># AWS Console → S3 → Create Bucket</span>
<span class="flag">Bucket Name :</span> <span class="val">my--data-pipeline-bucket</span>
<span class="flag">Region      :</span> <span class="val">us-east-1</span>
<span class="flag">Access      :</span> <span class="val">Private</span>

<span class="comment"># Upload sample_data.csv to the bucket</span>
<span class="comment"># File contents:</span>
<span class="str">id,name,age</span>
<span class="str">1,Arkan,22</span>
<span class="str">2,Rahul,25</span>
<span class="str">3,Amit,28</span>
        </div>
        <div class="tip-box"><strong>Why?</strong> S3 is our data source. The Python app reads this CSV using boto3.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">02</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">🗄️</span> Launch RDS MySQL Instance</div>
        <div class="step-desc">Create a free-tier MySQL database on RDS. This is the primary destination for ingested data.</div>
        <div class="code-block">
<span class="comment"># AWS Console → RDS → Create Database</span>
<span class="flag">Engine      :</span> <span class="val">MySQL</span>
<span class="flag">Template    :</span> <span class="val">Free Tier</span>
<span class="flag">DB Name     :</span> <span class="val">testdb</span>
<span class="flag">Username    :</span> <span class="val">admin</span>
<span class="flag">Password    :</span> <span class="val">your-secure-password</span>
<span class="flag">Public      :</span> <span class="val">Yes</span> <span class="comment">(for EC2 access)</span>

<span class="comment"># Note down the endpoint URL — needed later</span>
<span class="comment"># Example: database-1.cwda4ouui41q.us-east-1.rds.amazonaws.com</span>
        </div>
        <div class="tip-box"><strong>Why?</strong> RDS is the primary path. All CSV rows will be written to a table here.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">03</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">🔗</span> Create AWS Glue Database</div>
        <div class="step-desc">Set up the Glue Data Catalog database. This is only used if RDS fails.</div>
        <div class="code-block">
<span class="comment"># AWS Console → AWS Glue → Databases → Add Database</span>
<span class="flag">Name   :</span> <span class="val">my_glue_db</span>
<span class="flag">Region :</span> <span class="val">us-east-1</span>
        </div>
        <div class="tip-box"><strong>Why?</strong> The app creates an external table in Glue automatically if RDS is unavailable — acting as a fallback catalog.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">04</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">💻</span> Launch EC2 Ubuntu Instance</div>
        <div class="step-desc">Spin up an EC2 Ubuntu server. This is where Docker will run the container.</div>
        <div class="code-block">
<span class="comment"># AWS Console → EC2 → Launch Instance</span>
<span class="flag">OS     :</span> <span class="val">Ubuntu 22.04 LTS</span>
<span class="flag">Type   :</span> <span class="val">t2.micro</span> <span class="comment">(Free Tier)</span>
<span class="flag">Storage:</span> <span class="val">8 GB</span>
<span class="flag">Key    :</span> <span class="val">Create new .pem key → download it</span>

<span class="comment"># SSH into the instance</span>
<span class="cmd">ssh</span> <span class="flag">-i</span> <span class="val">your-key.pem</span> ubuntu@<span class="val">your-ec2-public-ip</span>
        </div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">05</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">🐳</span> Install Docker on EC2</div>
        <div class="step-desc">Install Docker engine on the Ubuntu server so we can build and run the container.</div>
        <div class="code-block">
<span class="cmd">sudo apt update</span>
<span class="cmd">sudo apt install</span> docker.io <span class="flag">-y</span>
<span class="cmd">sudo usermod</span> <span class="flag">-aG</span> docker ubuntu
<span class="cmd">newgrp</span> docker
<span class="cmd">docker</span> <span class="flag">--version</span>
<span class="comment"># → Docker version 24.x.x</span>
        </div>
        <div class="tip-box"><strong>Why?</strong> Docker isolates the app from the host OS. Our Python app + all dependencies run in one portable image.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">06</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">📁</span> Create Project Files</div>
        <div class="step-desc">Create the project directory and all required files on EC2.</div>
        <div class="code-block">
<span class="cmd">mkdir</span> aws-pipeline &amp;&amp; <span class="cmd">cd</span> aws-pipeline

<span class="comment"># Create all files</span>
<span class="cmd">nano</span> app.py
<span class="cmd">nano</span> Dockerfile
<span class="cmd">nano</span> requirements.txt
<span class="cmd">nano</span> sample_data.csv

<span class="comment"># OR clone from GitHub</span>
<span class="cmd">git clone</span> https://github.com/arkantandel/project-3.git
<span class="cmd">cd</span> project-3
        </div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">07</div>
      <div class="step-body">
        <div class="step-title"><span class="icon">🔨</span> Build the Docker Image</div>
        <div class="step-desc">Build the Docker image. This pulls Python 3.9, installs all libraries, and copies app.py.</div>
        <div class="code-block">
<span class="cmd">docker build</span> <span class="flag">-t</span> <span class="val">data-pipeline</span> <span class="str">.</span>

<span class="comment"># What happens during build:</span>
<span class="comment"># [1/3] FROM python:3.9        ← pulls base image</span>
<span class="comment"># [2/3] RUN pip install -r ... ← installs boto3, pandas, etc</span>
<span class="comment"># [3/3] COPY app.py .          ← adds your script</span>
<span class="comment"># → Image "data-pipeline" ready ✅</span>
        </div>
        <div class="tip-box"><strong>Why?</strong> The build packages everything so the same image runs identically anywhere — EC2, local machine, or CI/CD.</div>
      </div>
    </div>

    <div class="step" style="padding-bottom:0;">
      <div class="step-num">08</div>
      <div class="step-body" style="padding-bottom:0;">
        <div class="step-title"><span class="icon">🚀</span> Run the Docker Container</div>
        <div class="step-desc">Run the container with all AWS credentials and config passed as environment variables. No secrets hardcoded.</div>
        <div class="code-block">
<span class="cmd">docker run</span> \
  <span class="flag">-e</span> <span class="val">AWS_ACCESS_KEY_ID</span>=YOUR_KEY \
  <span class="flag">-e</span> <span class="val">AWS_SECRET_ACCESS_KEY</span>=YOUR_SECRET \
  <span class="flag">-e</span> <span class="val">AWS_DEFAULT_REGION</span>=us-east-1 \
  <span class="flag">-e</span> <span class="val">S3_BUCKET</span>=my--data-pipeline-bucket \
  <span class="flag">-e</span> <span class="val">S3_KEY</span>=data.csv \
  <span class="flag">-e</span> <span class="val">RDS_HOST</span>=your-rds-endpoint.rds.amazonaws.com \
  <span class="flag">-e</span> <span class="val">RDS_USER</span>=admin \
  <span class="flag">-e</span> <span class="val">RDS_PASSWORD</span>=your-password \
  <span class="flag">-e</span> <span class="val">RDS_DB</span>=testdb \
  <span class="flag">-e</span> <span class="val">RDS_TABLE</span>=mytable \
  <span class="flag">-e</span> <span class="val">GLUE_DB</span>=my_glue_db \
  <span class="flag">-e</span> <span class="val">GLUE_TABLE</span>=my_glue_table \
  <span class="flag">-e</span> <span class="val">GLUE_S3_PATH</span>=s3://my--data-pipeline-bucket/ \
  data-pipeline
        </div>
        <div class="tip-box"><strong>Security note:</strong> Using -e env vars means credentials stay outside the image. Never hardcode AWS keys in app.py or Dockerfile.</div>
      </div>
    </div>

  </div>
</div>

<!-- OUTPUT -->
<div id="output" class="section">
  <div class="section-label">06 · Output</div>
  <div class="section-title">Execution result</div>
  <div class="section-desc">Container ran on AWS EC2 Ubuntu instance. Terminal output below.</div>
  <div class="terminal">
    <div class="terminal-bar">
      <div class="dot" style="background:#ef4444;"></div>
      <div class="dot" style="background:#f59e0b;"></div>
      <div class="dot" style="background:#22c55e;"></div>
      <span class="terminal-title" style="margin-left:8px;">ubuntu@ip-172-31-30-219:~/aws-pipeline</span>
    </div>
    <div class="terminal-body" id="terminal-body">
      <div><span class="t-prompt">ubuntu@ip-172-31-30-219</span><span style="color:#6b7280;">:~/aws-pipeline$</span> <span class="t-cmd" id="typed-cmd"></span><span class="t-cursor" id="cursor1"></span></div>
      <div id="output-lines" style="display:none;">
        <div style="color:#6b7280;font-size:11px;line-height:1.6;">PythonDeprecationWarning: Boto3 will no longer support<br/>Python 3.9 starting April 29, 2026...</div>
        <div class="t-out-ok"><span style="color:#22c55e;font-size:14px;">✅</span> Data read from S3</div>
        <div class="t-out-ok"><span style="color:#22c55e;font-size:14px;">✅</span> Data inserted into RDS</div>
        <div style="margin-top:8px;"><span class="t-prompt">ubuntu@ip-172-31-30-219</span><span style="color:#6b7280;">:~/aws-pipeline$</span> <span class="t-cursor"></span></div>
      </div>
    </div>
  </div>
  <button onclick="replayTerminal()" style="margin-top:14px;padding:8px 20px;border-radius:20px;border:1px solid var(--border2);background:var(--bg3);color:var(--text2);font-size:13px;cursor:pointer;font-family:'Space Grotesk',sans-serif;">Replay animation</button>
</div>

<!-- CHALLENGES -->
<div id="challenges" class="section">
  <div class="section-label">07 · Challenges</div>
  <div class="section-title">Challenges &amp; solutions</div>
  <div class="section-desc">Real problems faced during development and how they were fixed.</div>
  <div class="challenges">
    <div class="challenge">
      <div class="ch-num">1</div>
      <div>
        <div class="ch-title">Passing AWS credentials securely into Docker</div>
        <div class="ch-sol"><strong>Solved:</strong> Used <code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);">-e</code> env vars at <code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);">docker run</code> time. Nothing is stored inside the image — credentials stay out of version control completely.</div>
      </div>
    </div>
    <div class="challenge">
      <div class="ch-num">2</div>
      <div>
        <div class="ch-title">RDS not accepting connections from Docker container</div>
        <div class="ch-sol"><strong>Solved:</strong> Opened inbound port 3306 in the RDS Security Group for the EC2 instance's IP address. Also ensured Public Accessibility was enabled.</div>
      </div>
    </div>
    <div class="challenge">
      <div class="ch-num">3</div>
      <div>
        <div class="ch-title">Glue fallback triggering even when RDS worked</div>
        <div class="ch-sol"><strong>Solved:</strong> Wrapped RDS logic in a clean <code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);">try/except</code> block. Glue is only called if an exception is raised — not on success.</div>
      </div>
    </div>
    <div class="challenge">
      <div class="ch-num">4</div>
      <div>
        <div class="ch-title">Dependency issues inside the container</div>
        <div class="ch-sol"><strong>Solved:</strong> Listed all packages in <code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);">requirements.txt</code> and installed via <code style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);">pip install -r</code> in Dockerfile. This locks versions and ensures consistent builds.</div>
      </div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<div class="footer">
  <div class="footer-name">Arkan Tandel</div>
  <div class="footer-sub">28 July Batch · MCA Internship · Fortune Cloud Technologies · 2026</div>
</div>

<script>
// ── FILE TOGGLE ──
function toggleCode(id){
  const el=document.getElementById(id);
  el.style.display=el.style.display==='none'?'block':'none';
}

// ── DIAGRAM PATH TOGGLE ──
function setPath(path){
  const btns=['btn-both','btn-primary','btn-fallback'];
  btns.forEach(b=>{
    const el=document.getElementById(b);
    el.style.background='var(--bg3)';
    el.style.borderColor='var(--border2)';
    el.style.color='var(--text2)';
  });
  const active=document.getElementById('btn-'+path);
  if(path==='both'){active.style.background='var(--green3)';active.style.borderColor='var(--green)';active.style.color='var(--green)';}
  else if(path==='primary'){active.style.background='var(--blue3)';active.style.borderColor='var(--blue)';active.style.color='var(--blue)';}
  else{active.style.background='var(--orange3)';active.style.borderColor='var(--orange)';active.style.color='var(--orange)';}
}

// ── TERMINAL ANIMATION ──
const fullCmd='docker run -e AWS_ACCESS_KEY_ID=... -e S3_BUCKET=my--data-pipeline-bucket data-pipeline';
let typingDone=false;
function typeCmd(){
  const el=document.getElementById('typed-cmd');
  const cur=document.getElementById('cursor1');
  el.textContent='';
  document.getElementById('output-lines').style.display='none';
  typingDone=false;
  let i=0;
  const iv=setInterval(()=>{
    if(i<fullCmd.length){
      el.textContent+=fullCmd[i++];
    } else {
      clearInterval(iv);
      cur.style.display='none';
      setTimeout(()=>{
        document.getElementById('output-lines').style.display='block';
        typingDone=true;
      },400);
    }
  },22);
}
function replayTerminal(){typeCmd();}
setTimeout(typeCmd,800);

// ── NAV ACTIVE STATE ──
const sections=document.querySelectorAll('[id]');
const navLinks=document.querySelectorAll('.toc a');
window.addEventListener('scroll',()=>{
  let current='';
  sections.forEach(s=>{if(window.scrollY>=s.offsetTop-120)current=s.id;});
  navLinks.forEach(a=>{
    a.classList.remove('active');
    if(a.getAttribute('href')==='#'+current)a.classList.add('active');
  });
});
</script>
</body>
</html>
