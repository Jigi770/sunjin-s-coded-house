import streamlit as st

st.set_page_config(page_title="FOR HIM - Men's Beauty AI Demo", layout="wide")

DEMO_HTML = """
<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FOR HIM — Men's Beauty AI Demo</title>
<style>
  :root{
    --bg:#f6f5f2;
    --surface:#ffffff;
    --ink:#1c1c1a;
    --ink-soft:#71706a;
    --line:#e6e4de;
    --accent:#54634a;
    --accent-soft:#e7ecdf;
    --dark:#1a1a18;
    --dark-soft:#2a2a26;
    --gold:#c9a86a;
    --gold-soft:#3a3630;
    --bad:#c1666b;
    --mid:#c98a3c;
    --good:#54634a;
    --radius-lg:20px;
    --radius:14px;
    --radius-sm:9px;
    --shadow: 0 14px 34px rgba(20,20,18,0.07);
    --maxw: 1120px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Pretendard","Segoe UI","Noto Sans KR",sans-serif;
    background:var(--bg);
    color:var(--ink);
    line-height:1.55;
    -webkit-font-smoothing:antialiased;
    overflow-x:hidden;
  }
  a{color:inherit;text-decoration:none;}
  button{font-family:inherit;cursor:pointer;}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px;}
  section{padding:88px 0;}
  .eyebrow{
    display:inline-flex;align-items:center;gap:8px;
    font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--accent);font-weight:700;margin-bottom:14px;
  }
  .eyebrow.on-dark{color:var(--gold);}
  h1,h2,h3{margin:0;font-weight:700;letter-spacing:-0.02em;}
  h2{font-size:clamp(24px,3.4vw,34px);}
  .sub{color:var(--ink-soft);font-size:16px;margin-top:10px;max-width:560px;}
  .sub.on-dark{color:#c9c8c1;}

  /* ---------- NAV ---------- */
  .nav{
    position:sticky;top:0;z-index:50;
    background:rgba(246,245,242,0.86);backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);
  }
  .nav .wrap{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;}
  .brand{display:flex;flex-direction:column;line-height:1.1;}
  .brand b{font-size:19px;letter-spacing:-.02em;}
  .brand span{font-size:10.5px;letter-spacing:.16em;color:var(--ink-soft);text-transform:uppercase;margin-top:2px;}
  .nav-links{display:flex;gap:28px;font-size:14.5px;font-weight:600;color:var(--ink-soft);}
  .nav-links a:hover{color:var(--ink);}
  .btn{
    display:inline-flex;align-items:center;justify-content:center;gap:8px;
    padding:12px 22px;border-radius:999px;border:none;font-weight:700;font-size:14.5px;
    transition:transform .15s ease, opacity .15s ease;
  }
  .btn:active{transform:scale(.97);}
  .btn-dark{background:var(--dark);color:#f6f5f2;}
  .btn-dark:hover{opacity:.88;}
  .btn-gold{background:var(--gold);color:#1a1a18;}
  .btn-gold:hover{opacity:.9;}
  .btn-outline{background:transparent;border:1.5px solid var(--line);color:var(--ink);}
  .btn-outline:hover{border-color:var(--ink);}
  .btn-sm{padding:9px 16px;font-size:13px;}
  .btn[disabled]{opacity:.45;cursor:not-allowed;}

  /* ---------- HERO ---------- */
  .hero{
    background:radial-gradient(120% 140% at 15% 0%, #232320 0%, var(--dark) 55%, var(--dark) 100%);
    color:#f6f5f2;padding:110px 0 90px;
  }
  .hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;}
  .hero h1{font-size:clamp(32px,4.6vw,52px);line-height:1.18;}
  .hero h1 em{font-style:normal;color:var(--gold);}
  .hero .sub{max-width:480px;}
  .hero-cta{display:flex;align-items:center;gap:16px;margin-top:32px;flex-wrap:wrap;}
  .hero-note{font-size:13px;color:#a9a89f;}
  .trust-row{display:flex;gap:18px;margin-top:34px;flex-wrap:wrap;font-size:13px;color:#c9c8c1;}
  .trust-row span{display:flex;align-items:center;gap:6px;}
  .dot{width:4px;height:4px;border-radius:50%;background:var(--gold);}
  .hero-visual{
    position:relative;background:var(--dark-soft);border:1px solid #3a3934;
    border-radius:var(--radius-lg);padding:26px;
  }
  .hero-visual .face{
    aspect-ratio:1/1;border-radius:16px;
    background:linear-gradient(160deg,#3a3934,#232320);
    display:flex;align-items:center;justify-content:center;color:#7a7970;
    border:1px dashed #4a4940;
  }
  .hero-visual .cap{margin-top:14px;font-size:12.5px;color:#9c9b92;text-align:center;}

  /* ---------- CHIPS ---------- */
  .chip{
    display:inline-flex;align-items:center;gap:7px;
    padding:11px 18px;border-radius:999px;border:1.5px solid var(--line);
    background:var(--surface);font-size:14px;font-weight:600;color:var(--ink-soft);
    transition:all .15s ease;
  }
  .chip:hover{border-color:#c8c6bd;}
  .chip.active{background:var(--accent);border-color:var(--accent);color:#fff;}
  .chip-check{width:14px;height:14px;flex:none;}

  /* ---------- ANALYSIS ---------- */
  .analysis-card{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);
    padding:40px;box-shadow:var(--shadow);margin-top:36px;
  }
  .picker-label{font-weight:700;font-size:15px;margin-bottom:16px;}
  .chip-row{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px;}
  .hint{font-size:13px;color:var(--bad);min-height:18px;margin-bottom:14px;}

  .loading{display:none;align-items:center;gap:14px;padding:20px 0;color:var(--ink-soft);font-weight:600;}
  .loading.show{display:flex;}
  .spinner{width:22px;height:22px;border-radius:50%;border:3px solid var(--line);border-top-color:var(--accent);animation:spin .8s linear infinite;}
  @keyframes spin{to{transform:rotate(360deg);}}

  .result{display:none;margin-top:8px;animation:fade .5s ease;}
  .result.show{display:block;}
  @keyframes fade{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
  .result-grid{display:grid;grid-template-columns:220px 1fr;gap:40px;align-items:center;padding-top:16px;border-top:1px solid var(--line);}
  .ring{
    width:180px;height:180px;border-radius:50%;margin:0 auto;
    display:flex;align-items:center;justify-content:center;position:relative;
  }
  .ring::after{
    content:"";position:absolute;inset:14px;background:var(--surface);border-radius:50%;
  }
  .ring-inner{position:relative;z-index:1;text-align:center;}
  .ring-inner b{font-size:34px;display:block;line-height:1;}
  .ring-inner span{font-size:12px;color:var(--ink-soft);}
  .metric{margin-bottom:14px;}
  .metric-top{display:flex;justify-content:space-between;font-size:13.5px;font-weight:600;margin-bottom:6px;}
  .metric-track{height:8px;border-radius:999px;background:var(--accent-soft);overflow:hidden;}
  .metric-fill{height:100%;border-radius:999px;width:0%;transition:width 1s cubic-bezier(.2,.8,.2,1);}
  .fill-good{background:var(--good);}
  .fill-mid{background:var(--mid);}
  .fill-bad{background:var(--bad);}
  .summary{margin-top:26px;padding:20px 22px;background:var(--accent-soft);border-radius:var(--radius);font-size:14.5px;color:#3c4636;}
  .result-actions{margin-top:24px;display:flex;gap:12px;flex-wrap:wrap;}

  /* ---------- RECOMMEND ---------- */
  .recommend{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
  .rec-head{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:20px;}
  .switch-wrap{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--ink-soft);}
  .switch{width:42px;height:24px;border-radius:999px;background:var(--line);position:relative;transition:.2s;flex:none;}
  .switch::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.2);}
  .switch.on{background:var(--accent);}
  .switch.on::after{left:21px;}
  .placeholder-note{
    margin-top:30px;padding:16px 20px;border:1px dashed var(--line);border-radius:var(--radius);
    color:var(--ink-soft);font-size:13.5px;background:var(--bg);
  }
  .routine-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:30px;}
  .routine-grid.one{grid-template-columns:1fr;max-width:360px;}
  .p-card{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);padding:22px;}
  .p-step{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700;}
  .p-name{font-size:16px;font-weight:700;margin-top:10px;}
  .p-reason{font-size:13px;color:var(--ink-soft);margin-top:8px;}
  .p-tag{display:inline-block;margin-top:14px;font-size:11.5px;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-weight:700;}

  /* ---------- COMMUNITY ---------- */
  .filter-row{display:flex;gap:10px;flex-wrap:wrap;margin:30px 0 26px;}
  .filter-chip{padding:8px 16px;border-radius:999px;border:1.5px solid var(--line);font-size:13.5px;font-weight:600;color:var(--ink-soft);background:var(--surface);}
  .filter-chip.active{background:var(--dark);border-color:var(--dark);color:#fff;}
  .post-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;}
  .post{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;}
  .post-top{display:flex;align-items:center;gap:10px;}
  .avatar{width:34px;height:34px;border-radius:50%;background:var(--dark);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex:none;}
  .post-meta b{font-size:14px;display:block;}
  .post-meta span{font-size:12px;color:var(--ink-soft);}
  .post-tag{margin-left:auto;font-size:11px;font-weight:700;color:var(--accent);background:var(--accent-soft);padding:4px 10px;border-radius:999px;}
  .post-body{font-size:14px;color:#3a3a36;margin:14px 0 16px;}
  .post-stats{display:flex;gap:16px;font-size:12.5px;color:var(--ink-soft);}
  .post-stats span{display:flex;align-items:center;gap:5px;}
  .icon{width:15px;height:15px;}
  .toast{
    position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(120%);
    background:var(--dark);color:#fff;padding:13px 22px;border-radius:999px;font-size:13.5px;font-weight:600;
    box-shadow:var(--shadow);transition:transform .25s ease;z-index:100;
  }
  .toast.show{transform:translateX(-50%) translateY(0);}

  footer{padding:46px 0;text-align:center;color:var(--ink-soft);font-size:12.5px;background:var(--dark);}
  footer b{color:#f6f5f2;font-size:15px;display:block;margin-bottom:6px;}
  footer .fine{margin-top:10px;color:#7d7c75;}

  @media (max-width:860px){
    section{padding:60px 0;}
    .nav-links{display:none;}
    .hero .wrap{grid-template-columns:1fr;}
    .hero{padding:70px 0 56px;text-align:left;}
    .result-grid{grid-template-columns:1fr;text-align:center;}
    .routine-grid{grid-template-columns:1fr 1fr;}
    .routine-grid.one{max-width:none;}
    .post-grid{grid-template-columns:1fr;}
    .analysis-card{padding:26px;}
    .rec-head{flex-direction:column;align-items:flex-start;}
  }
  @media (max-width:480px){
    .routine-grid{grid-template-columns:1fr;}
    .wrap{padding:0 18px;}
  }
</style>
</head>
<body>

<div class="nav">
  <div class="wrap">
    <div class="brand"><b>FOR HIM</b><span>Men's Skincare Lab</span></div>
    <div class="nav-links">
      <a href="#analysis">피부분석</a>
      <a href="#recommend">제품추천</a>
      <a href="#community">커뮤니티</a>
    </div>
    <a href="#analysis" class="btn btn-dark btn-sm">분석 시작</a>
  </div>
</div>

<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow on-dark">MEN'S BEAUTY, SIMPLIFIED</div>
      <h1>피부 관리, <em>어렵게</em><br/>생각하지 마세요</h1>
      <p class="sub on-dark">복잡한 성분 이름도, 매장에서의 어색한 상담도 필요 없어요. 지금 신경 쓰이는 부분만 골라도 AI가 상태를 확인해드려요.</p>
      <div class="hero-cta">
        <a href="#analysis" class="btn btn-gold">30초 만에 피부 확인하기</a>
        <span class="hero-note">화장품, 처음이어도 괜찮아요</span>
      </div>
      <div class="trust-row">
        <span>버튼 선택만으로 분석</span><span class="dot"></span>
        <span>어려운 성분 설명 없이</span><span class="dot"></span>
        <span>매장 방문 없이 시작</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="face">영상 분석 화면 (데모)</div>
      <div class="cap">실제 서비스에서는 이 영역에서 카메라 분석이 진행돼요</div>
    </div>
  </div>
</section>

<section id="analysis">
  <div class="wrap">
    <div class="eyebrow">SKIN ANALYSIS AI</div>
    <h2>피부 영상 분석 AI</h2>
    <p class="sub">카메라 앞에 서지 않아도 괜찮아요. 이 데모에서는 지금 느끼는 고민을 선택하면 실제 분석처럼 결과를 보여드려요.</p>

    <div class="analysis-card">
      <div class="picker-label">지금 가장 신경 쓰이는 부분을 선택해주세요 (복수 선택 가능)</div>
      <div class="chip-row" id="chipRow">
        <button class="chip" data-key="scar">파인 흉터</button>
        <button class="chip" data-key="pore">넓은 모공</button>
        <button class="chip" data-key="oil">피지·유분</button>
        <button class="chip" data-key="acne">화농성 여드름</button>
      </div>
      <div class="hint" id="hint"></div>
      <button class="btn btn-dark" id="analyzeBtn">AI 분석 시작하기</button>

      <div class="loading" id="loading">
        <div class="spinner"></div>
        <span>AI가 피부 상태를 분석하고 있어요...</span>
      </div>

      <div class="result" id="result">
        <div class="result-grid">
          <div class="ring" id="ring">
            <div class="ring-inner"><b id="scoreNum">0</b><span>종합 스코어</span></div>
          </div>
          <div id="metrics"></div>
        </div>
        <div class="summary" id="summary"></div>
        <div class="result-actions">
          <a href="#recommend" class="btn btn-dark btn-sm" id="toRecommend">맞춤 제품 추천 받기</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="recommend" class="recommend">
  <div class="wrap">
    <div class="rec-head">
      <div>
        <div class="eyebrow">PRODUCT RECOMMEND AI</div>
        <h2>제품 추천 AI</h2>
        <p class="sub">성분표를 몰라도 괜찮아요. 지금 상태에 필요한 것만 알려드릴게요.</p>
      </div>
      <div class="switch-wrap">
        <span>귀찮은 날엔 올인원으로</span>
        <div class="switch" id="allInOneSwitch"></div>
      </div>
    </div>

    <div class="placeholder-note" id="recNote">먼저 위에서 피부 분석을 해보면 더 정확한 루틴을 추천해드려요. 지금은 기본 루틴을 보여드리고 있어요.</div>
    <div class="routine-grid" id="routineGrid"></div>
  </div>
</section>

<section id="community">
  <div class="wrap">
    <div class="eyebrow">COMMUNITY</div>
    <h2>커뮤니티</h2>
    <p class="sub">같은 고민, 같은 눈높이에서 편하게 물어보세요.</p>

    <div class="filter-row" id="filterRow">
      <button class="filter-chip active" data-tag="all">전체</button>
      <button class="filter-chip" data-tag="모공">모공</button>
      <button class="filter-chip" data-tag="트러블">트러블</button>
      <button class="filter-chip" data-tag="유분">유분</button>
      <button class="filter-chip" data-tag="왕초보질문">왕초보질문</button>
      <button class="btn btn-outline btn-sm" id="writeBtn" style="margin-left:auto;">글 남기기</button>
    </div>

    <div class="post-grid" id="postGrid"></div>
  </div>
</section>

<footer>
  <div class="wrap">
    <b>FOR HIM — Men's Beauty, Simplified.</b>
    복잡한 과정 없이, 자연스럽게 시작하는 남성 스킨케어
    <div class="fine">본 화면은 데모이며 모든 분석·추천 결과는 예시 데이터입니다.</div>
  </div>
</footer>

<div class="toast" id="toast"></div>

<script>
(function(){
  const CHECK_SVG = '<svg class="chip-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M4 12l5 5L20 7"/></svg>';
  const HEART_SVG = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.35-9.5-8.5C.5 8.5 2.5 5 6 5c2 0 3.5 1 6 3.5C14.5 6 16 5 18 5c3.5 0 5.5 3.5 3.5 7.5C19 16.65 12 21 12 21z"/></svg>';
  const CHAT_SVG = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5H3l2.7-3.6A8.4 8.4 0 1 1 21 11.5z"/></svg>';

  const CONCERNS = {
    scar:{label:'파인 흉터'},
    pore:{label:'넓은 모공'},
    oil:{label:'피지·유분'},
    acne:{label:'화농성 여드름'}
  };
  const state = { concerns:new Set(), analyzed:false, allInOne:false };

  /* ---------------- concern chips ---------------- */
  const chipRow = document.getElementById('chipRow');
  chipRow.querySelectorAll('.chip').forEach(chip=>{
    chip.addEventListener('click', ()=>{
      const key = chip.dataset.key;
      if(state.concerns.has(key)){
        state.concerns.delete(key); chip.classList.remove('active'); chip.innerHTML = CONCERNS[key].label;
      } else {
        state.concerns.add(key); chip.classList.add('active'); chip.innerHTML = CHECK_SVG + CONCERNS[key].label;
      }
      document.getElementById('hint').textContent='';
    });
  });

  /* ---------------- analysis ---------------- */
  const loadingEl = document.getElementById('loading');
  const resultEl = document.getElementById('result');
  const hintEl = document.getElementById('hint');

  function band(score){ return score>=70?'good':score>=50?'mid':'bad'; }

  function computeMetrics(){
    const base = { 수분:74, 유분조절:76, 모공:78, 트러블:80, 탄력:75 };
    if(state.concerns.has('scar')){ base.탄력-=20; base.트러블-=8; }
    if(state.concerns.has('pore')){ base.모공-=35; }
    if(state.concerns.has('oil')){ base.유분조절-=32; base.수분-=8; }
    if(state.concerns.has('acne')){ base.트러블-=35; base.유분조절-=10; }
    Object.keys(base).forEach(k=> base[k]=Math.max(15, Math.min(95, base[k])) );
    return base;
  }

  document.getElementById('analyzeBtn').addEventListener('click', ()=>{
    if(state.concerns.size===0){
      hintEl.textContent = '최소 1개 이상의 고민을 선택해주세요.';
      return;
    }
    resultEl.classList.remove('show');
    loadingEl.classList.add('show');

    setTimeout(()=>{
      loadingEl.classList.remove('show');
      renderResult(computeMetrics());
      resultEl.classList.add('show');
      state.analyzed = true;
      renderRoutine();
    }, 1400);
  });

  function renderResult(metrics){
    const values = Object.values(metrics);
    const overall = Math.round(values.reduce((a,b)=>a+b,0)/values.length);
    document.getElementById('scoreNum').textContent = overall;
    document.getElementById('ring').style.background =
      `conic-gradient(var(--gold) ${overall}%, var(--line) ${overall}% 100%)`;

    const metricsEl = document.getElementById('metrics');
    metricsEl.innerHTML = '';
    Object.entries(metrics).forEach(([label, score])=>{
      const b = band(score);
      const row = document.createElement('div');
      row.className='metric';
      row.innerHTML = `
        <div class="metric-top"><span>${label}</span><span>${score}</span></div>
        <div class="metric-track"><div class="metric-fill fill-${b}" style="width:0%"></div></div>`;
      metricsEl.appendChild(row);
      requestAnimationFrame(()=>{ row.querySelector('.metric-fill').style.width = score+'%'; });
    });

    const labels = [...state.concerns].map(k=>CONCERNS[k].label);
    const listText = labels.length ? labels.join(', ') : '특별한 고민';
    const tone = overall>=70 ? '전반적으로 관리가 잘 되고 있어요. 지금 루틴을 유지하면서 조금만 보완해볼까요?'
               : overall>=50 ? '조금만 신경 쓰면 확실히 달라질 수 있는 단계예요.'
               : '지금부터 관리를 시작하기 좋은 시점이에요. 무리하지 않고 기본부터 잡아볼게요.';
    document.getElementById('summary').textContent =
      `${listText} 고민을 중심으로 분석했어요. 종합 스코어는 ${overall}점이에요. ${tone}`;
  }

  /* ---------------- recommend ---------------- */
  const routineGrid = document.getElementById('routineGrid');
  const recNote = document.getElementById('recNote');
  const allInOneSwitch = document.getElementById('allInOneSwitch');

  allInOneSwitch.addEventListener('click', ()=>{
    state.allInOne = !state.allInOne;
    allInOneSwitch.classList.toggle('on', state.allInOne);
    renderRoutine();
  });

  document.getElementById('toRecommend').addEventListener('click', ()=>{
    setTimeout(renderRoutine, 50);
  });

  function pick(cond, yes, no){ return cond ? yes : no; }

  function getSteps(){
    const c = state.concerns;
    return [
      { step:'클렌징', name:'포어 클린 폼', tag:'저자극',
        reason: pick(c.has('oil')||c.has('acne'),
          '피지와 트러블 원인까지 부담 없이 씻어내는 약산성 폼이에요.',
          '하루 노폐물과 유분을 순하게 씻어내요.') },
      { step:'토너 · 세럼', name: pick(c.has('pore'),'포어 타이트닝 토너','데일리 수분 세럼'), tag: pick(c.has('scar'),'브라이트닝','수분 진정'),
        reason: pick(c.has('pore'), '넓어진 모공을 조여주는 데 집중한 토너예요.',
              pick(c.has('scar'), '흉터 자국과 피부결을 매끈하게 정돈해줘요.', '수분을 채우고 다음 단계를 잘 흡수하게 해줘요.')) },
      { step:'로션', name: pick(c.has('oil'),'라이트 젤 로션','데일리 수분 로션'), tag:'산뜻 마무리',
        reason: pick(c.has('oil'), '유분 걱정 없이 촉촉함만 가볍게 남겨요.', '하루종일 당김 없이 편안하게 유지해줘요.') },
      { step:'선크림', name:'데일리 선크림', tag:'필수',
        reason:'자외선 차단은 선택이 아니라 관리의 기본이에요.' }
    ];
  }

  function renderRoutine(){
    const steps = state.allInOne
      ? [{ step:'올인원', name:'올데이 올인원 크림', tag:'귀찮음 제로',
           reason:'클렌징 후 이거 하나면 끝. 귀찮은 날에도 이것만 발라도 충분해요.' }]
      : getSteps();

    routineGrid.classList.toggle('one', state.allInOne);
    routineGrid.innerHTML = steps.map(s=>`
      <div class="p-card">
        <div class="p-step">${s.step}</div>
        <div class="p-name">${s.name}</div>
        <div class="p-reason">${s.reason}</div>
        <div class="p-tag">${s.tag}</div>
      </div>`).join('');

    recNote.style.display = state.analyzed ? 'none' : 'block';
  }
  renderRoutine();

  /* ---------------- community ---------------- */
  const POSTS = [
    {name:'코딩하는곰', time:'3시간 전', tag:'모공', body:'모공 넓은 거 때문에 파운데이션도 안 바르는데 클렌징만 잘해도 좀 나아지나요?', likes:12, comments:4},
    {name:'야근장인', time:'5시간 전', tag:'트러블', body:'턱쪽에 화농성 여드름이 계속 나는데 저만 이런가요... 뭐부터 해보면 좋을지 궁금해요.', likes:21, comments:9},
    {name:'초보루틴', time:'1일 전', tag:'왕초보질문', body:'스킨케어 뭐부터 사야하는지 진짜 모르겠어요. 올인원 제품 하나로 시작해도 될까요?', likes:34, comments:15},
    {name:'T존건조', time:'1일 전', tag:'유분', body:'T존은 번들거리는데 볼은 당기는 복합성 피부, 다들 어떻게 관리하세요?', likes:8, comments:3},
    {name:'무던한직장인', time:'2일 전', tag:'모공', body:'매장 가서 상담받는 게 너무 부담스러워서 대충 쓰고 있었는데 여기서 정보 얻어가요.', likes:40, comments:6},
    {name:'출근전5분', time:'3일 전', tag:'트러블', body:'아침에 시간 없어서 스킵하는 날 많은데 최소한 뭐는 꼭 발라야 할까요?', likes:17, comments:7}
  ];

  const postGrid = document.getElementById('postGrid');
  function renderPosts(filter){
    const list = filter==='all' ? POSTS : POSTS.filter(p=>p.tag===filter);
    postGrid.innerHTML = list.map(p=>`
      <div class="post">
        <div class="post-top">
          <div class="avatar">${p.name[0]}</div>
          <div class="post-meta"><b>${p.name}</b><span>${p.time}</span></div>
          <div class="post-tag">#${p.tag}</div>
        </div>
        <div class="post-body">${p.body}</div>
        <div class="post-stats">
          <span>${HEART_SVG}${p.likes}</span>
          <span>${CHAT_SVG}${p.comments}</span>
        </div>
      </div>`).join('');
  }
  renderPosts('all');

  document.getElementById('filterRow').querySelectorAll('.filter-chip').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      document.querySelectorAll('.filter-chip').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      renderPosts(btn.dataset.tag);
    });
  });

  const toast = document.getElementById('toast');
  document.getElementById('writeBtn').addEventListener('click', ()=>{
    toast.textContent = '데모 버전에서는 글쓰기가 비활성화되어 있어요.';
    toast.classList.add('show');
    setTimeout(()=>toast.classList.remove('show'), 2200);
  });

})();
</script>
</body>
</html>
"""

st.iframe(DEMO_HTML, height="content", width="stretch")
