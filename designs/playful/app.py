import streamlit as st
import streamlit.components.v1 as components

# FOR HIM — Design A: "PLAY" (game-like, cute, MZ vibe)
# Mobile-only, no-scroll platform. Each screen fills one phone viewport;
# navigation happens through a bottom tab bar (no page scrolling).
st.set_page_config(page_title="FOR HIM · PLAY", layout="centered",
                   initial_sidebar_state="collapsed")

# Strip all Streamlit chrome so the phone app fills the screen edge-to-edge.
st.markdown("""
<style>
  #MainMenu, header, footer {visibility:hidden;}
  [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {display:none !important;}
  [data-testid="stAppViewContainer"] {background:#0d0b1a;}
  .block-container, [data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"]
    {padding:0 !important; margin:0 !important; max-width:100% !important;}
  .stApp {overflow:hidden;}
  .stApp iframe {height:100dvh !important; width:100vw !important; border:none !important; display:block;}
  html, body {margin:0; padding:0; overflow:hidden;}
</style>
""", unsafe_allow_html=True)

HTML = r"""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<style>
  *{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
  :root{
    --grape:#7a3cff; --pink:#ff5fa2; --peach:#ffb15c; --lime:#38e5b0; --sky:#4cc9ff;
    --ink:#20143f; --paper:#fff;
  }
  html,body{height:100%;font-family:-apple-system,"Apple SD Gothic Neo","Malgun Gothic","Segoe UI",sans-serif;}
  body{
    display:flex;align-items:center;justify-content:center;min-height:100dvh;
    background:radial-gradient(120% 90% at 20% 0%,#8b57ff 0%,#6a2ff0 40%,#3a1a9e 100%);
    color:var(--ink);overflow:hidden;
  }
  .phone{
    position:relative;width:min(430px,100vw);height:min(880px,100dvh);
    background:linear-gradient(180deg,#fef4ff 0%,#f3ecff 100%);
    display:flex;flex-direction:column;overflow:hidden;
    box-shadow:0 30px 80px rgba(40,10,90,.45);
  }
  @media(min-width:460px){ .phone{border-radius:38px;border:8px solid #1b1030;height:min(880px,96dvh);} }

  /* ---- top bar ---- */
  .top{padding:16px 18px 10px;display:flex;align-items:center;gap:10px;flex-shrink:0;}
  .lvl{display:flex;align-items:center;gap:7px;background:#fff;border-radius:999px;padding:5px 12px 5px 6px;
    box-shadow:0 4px 0 #e4d3ff;font-weight:900;font-size:13px;}
  .lvl .ring{width:26px;height:26px;border-radius:50%;background:conic-gradient(var(--grape) 68%,#eadcff 0);
    display:grid;place-items:center;font-size:10px;color:var(--grape);}
  .lvl .ring b{background:#fff;width:18px;height:18px;border-radius:50%;display:grid;place-items:center;}
  .coins{margin-left:auto;display:flex;gap:7px;}
  .pill{background:#fff;border-radius:999px;padding:6px 11px;font-weight:900;font-size:13px;display:flex;
    align-items:center;gap:5px;box-shadow:0 4px 0 #e4d3ff;}
  .pill.flame{color:#ff7a2f;} .pill.coin{color:#f0a500;}

  /* ---- screen area ---- */
  .stage{flex:1;position:relative;overflow:hidden;}
  .screen{position:absolute;inset:0;padding:6px 18px 14px;display:flex;flex-direction:column;gap:12px;
    opacity:0;transform:translateY(14px) scale(.98);pointer-events:none;transition:.32s cubic-bezier(.2,.9,.3,1.3);overflow:hidden;}
  .screen.on{opacity:1;transform:none;pointer-events:auto;}
  .h1{font-size:23px;font-weight:900;line-height:1.15;letter-spacing:-.5px;}
  .h1 em{font-style:normal;color:var(--grape);}
  .sub{font-size:12.5px;color:#8a7bb0;font-weight:700;margin-top:-4px;}

  /* mascot */
  .buddy{width:132px;height:132px;margin:2px auto 0;position:relative;animation:bob 2.4s ease-in-out infinite;}
  @keyframes bob{50%{transform:translateY(-9px) rotate(-3deg);}}
  .buddy svg{filter:drop-shadow(0 12px 18px rgba(122,60,255,.35));}

  /* score gauge */
  .gauge{width:190px;height:190px;margin:0 auto;border-radius:50%;
    background:conic-gradient(var(--lime) 0 72%,#e9ddff 72% 100%);
    display:grid;place-items:center;box-shadow:0 14px 0 #e4d3ff, inset 0 0 0 10px #fff;}
  .gauge .in{width:132px;height:132px;background:#fff;border-radius:50%;display:grid;place-items:center;text-align:center;}
  .gauge .in b{font-size:46px;font-weight:900;color:var(--grape);line-height:1;}
  .gauge .in span{font-size:11px;font-weight:800;color:#a99;letter-spacing:1px;}

  .card{background:#fff;border-radius:22px;padding:15px 16px;box-shadow:0 8px 0 #eadcff;}
  .card.grape{background:linear-gradient(135deg,#7a3cff,#b06bff);color:#fff;box-shadow:0 8px 0 #4d1fb0;}
  .card-t{font-weight:900;font-size:15px;display:flex;align-items:center;gap:8px;}
  .card-d{font-size:12px;font-weight:700;opacity:.8;margin-top:3px;}

  .missions{display:flex;flex-direction:column;gap:9px;}
  .mission{display:flex;align-items:center;gap:11px;background:#fff;border-radius:18px;padding:11px 13px;
    box-shadow:0 5px 0 #eadcff;font-weight:800;font-size:13.5px;}
  .mchk{width:26px;height:26px;border-radius:9px;background:#f0e8ff;display:grid;place-items:center;flex-shrink:0;
    font-size:14px;color:transparent;transition:.2s;}
  .mission.done .mchk{background:var(--lime);color:#fff;}
  .mission.done{color:#b3a9c9;text-decoration:line-through;}
  .mxp{margin-left:auto;font-size:11px;font-weight:900;color:var(--peach);background:#fff5e6;
    padding:4px 9px;border-radius:999px;flex-shrink:0;}

  .xpbar{height:16px;background:#e9ddff;border-radius:999px;overflow:hidden;box-shadow:inset 0 2px 4px rgba(0,0,0,.08);}
  .xpbar>i{display:block;height:100%;width:68%;border-radius:999px;
    background:linear-gradient(90deg,var(--pink),var(--peach));}

  .cta{border:none;font-family:inherit;font-weight:900;font-size:17px;color:#fff;border-radius:20px;padding:16px;
    background:linear-gradient(135deg,var(--pink),var(--grape));box-shadow:0 8px 0 #5a1fb0;cursor:pointer;
    transition:.12s;display:flex;align-items:center;justify-content:center;gap:8px;}
  .cta:active{transform:translateY(5px);box-shadow:0 3px 0 #5a1fb0;}
  .cta.lime{background:linear-gradient(135deg,var(--lime),var(--sky));box-shadow:0 8px 0 #1c9c7a;}

  .chips{display:flex;gap:8px;flex-wrap:wrap;}
  .chip{background:#fff;border-radius:999px;padding:9px 15px;font-weight:800;font-size:13px;
    box-shadow:0 5px 0 #eadcff;cursor:pointer;transition:.12s;border:2px solid transparent;}
  .chip.sel{background:var(--grape);color:#fff;box-shadow:0 5px 0 #4d1fb0;}

  /* products */
  .prods{display:flex;flex-direction:column;gap:10px;overflow:hidden;}
  .prod{display:flex;align-items:center;gap:12px;background:#fff;border-radius:20px;padding:11px;box-shadow:0 6px 0 #eadcff;}
  .pface{width:52px;height:52px;border-radius:16px;flex-shrink:0;display:grid;place-items:center;font-size:26px;}
  .prod b{font-size:14px;font-weight:900;} .prod small{font-size:11.5px;color:#9a8fb5;font-weight:700;display:block;}
  .match{margin-left:auto;font-size:11px;font-weight:900;color:#fff;background:var(--lime);border-radius:999px;padding:5px 9px;flex-shrink:0;}

  /* community feed */
  .feed{display:flex;flex-direction:column;gap:10px;overflow:hidden;}
  .post{background:#fff;border-radius:20px;padding:13px 15px;box-shadow:0 6px 0 #eadcff;}
  .post .ph{display:flex;align-items:center;gap:8px;font-weight:900;font-size:12.5px;}
  .ava{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-size:15px;color:#fff;}
  .post p{font-size:13px;font-weight:700;color:#5c5175;margin-top:7px;line-height:1.45;}
  .post .rx{display:flex;gap:14px;margin-top:9px;font-size:12px;font-weight:800;color:#b0a5c8;}

  /* my */
  .badges{display:flex;gap:10px;justify-content:center;}
  .badge{width:64px;height:64px;border-radius:20px;display:grid;place-items:center;font-size:30px;
    background:#fff;box-shadow:0 6px 0 #eadcff;}
  .badge.lock{filter:grayscale(1);opacity:.45;}
  .statrow{display:flex;gap:10px;}
  .stat{flex:1;background:#fff;border-radius:18px;padding:13px;text-align:center;box-shadow:0 6px 0 #eadcff;}
  .stat b{font-size:22px;font-weight:900;color:var(--grape);display:block;}
  .stat span{font-size:11px;font-weight:800;color:#a99bc0;}

  /* bottom nav */
  .nav{flex-shrink:0;display:flex;justify-content:space-around;align-items:flex-end;padding:8px 10px 14px;
    background:#fff;border-top:2px solid #f0e8ff;position:relative;}
  .nb{border:none;background:none;font-family:inherit;display:flex;flex-direction:column;align-items:center;gap:2px;
    font-size:10px;font-weight:900;color:#c3b8dd;cursor:pointer;flex:1;padding:4px 0;transition:.15s;}
  .nb .ic{font-size:21px;transition:.2s;}
  .nb.on{color:var(--grape);} .nb.on .ic{transform:translateY(-3px) scale(1.18);}
  .nb.scan{margin-top:-30px;}
  .nb.scan .ic{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,var(--pink),var(--grape));
    color:#fff;display:grid;place-items:center;box-shadow:0 8px 0 #5a1fb0;font-size:26px;}
  .nb.scan.on .ic{transform:none;}

  .center{margin:auto 0;text-align:center;}
  .scanning .buddy{animation:spin 1s linear infinite;}
  @keyframes spin{to{transform:rotate(360deg);}}
  .toast{position:absolute;left:50%;bottom:96px;transform:translateX(-50%) translateY(20px);opacity:0;
    background:var(--ink);color:#fff;font-weight:800;font-size:12.5px;padding:10px 16px;border-radius:999px;
    transition:.3s;pointer-events:none;white-space:nowrap;z-index:40;}
  .toast.on{opacity:1;transform:translateX(-50%);}
</style>

<div class="phone">
  <div class="top">
    <div class="lvl"><div class="ring"><b>7</b></div>Lv.7 뷰티러너</div>
    <div class="coins">
      <div class="pill flame">🔥 12</div>
      <div class="pill coin">🪙 340</div>
    </div>
  </div>

  <div class="stage" id="stage">

    <!-- HOME -->
    <section class="screen on" data-screen="home">
      <div class="h1">민준님, <em>피부 퀘스트</em> 가자! 🚀</div>
      <div class="gauge"><div class="in"><b>72</b><span>SKIN LV</span></div></div>
      <div class="card grape">
        <div class="card-t">⚡ 다음 레벨까지</div>
        <div class="xpbar" style="margin-top:10px;background:rgba(255,255,255,.25)"><i></i></div>
        <div class="card-d" style="margin-top:8px;opacity:.95">320 / 500 XP · 미션 깨고 레벨업!</div>
      </div>
      <div class="missions">
        <div class="mission done"><span class="mchk">✔</span>오늘 물 2L 마시기<span class="mxp">+20</span></div>
        <div class="mission"><span class="mchk">✔</span>피부 스캔하기<span class="mxp">+50</span></div>
        <div class="mission"><span class="mchk">✔</span>루틴 인증샷 올리기<span class="mxp">+30</span></div>
      </div>
    </section>

    <!-- SCAN -->
    <section class="screen" data-screen="scan" id="scanScreen">
      <div class="h1">얼굴 <em>스캔</em>하고<br/>피부 레벨 올리기 📸</div>
      <div class="center">
        <div class="buddy" id="buddy">
          <svg width="132" height="132" viewBox="0 0 132 132">
            <ellipse cx="66" cy="74" rx="52" ry="48" fill="#7a3cff"/>
            <ellipse cx="66" cy="70" rx="44" ry="40" fill="#a06bff"/>
            <circle cx="50" cy="66" r="9" fill="#fff"/><circle cx="82" cy="66" r="9" fill="#fff"/>
            <circle cx="52" cy="68" r="4.5" fill="#20143f"/><circle cx="84" cy="68" r="4.5" fill="#20143f"/>
            <path d="M56 84 q10 9 20 0" stroke="#20143f" stroke-width="4" fill="none" stroke-linecap="round"/>
            <circle cx="40" cy="80" r="6" fill="#ff8fbf" opacity=".7"/><circle cx="92" cy="80" r="6" fill="#ff8fbf" opacity=".7"/>
            <path d="M66 20 l5 10 11 1 -8 8 2 11 -10 -6 -10 6 2 -11 -8 -8 11 -1z" fill="#ffd84c"/>
          </svg>
        </div>
        <div class="sub" id="scanMsg" style="margin-top:10px;font-size:13.5px;">버디가 얼굴을 분석할 준비 완료!</div>
      </div>
      <button class="cta" id="scanBtn">📷 스캔 시작 <span style="opacity:.85">+50 XP</span></button>
    </section>

    <!-- RECOMMEND -->
    <section class="screen" data-screen="reco">
      <div class="h1"><em>딱 맞는</em> 아이템 🛍️</div>
      <div class="chips">
        <div class="chip sel">전체</div><div class="chip">모공</div><div class="chip">트러블</div><div class="chip">유분</div>
      </div>
      <div class="prods">
        <div class="prod"><div class="pface" style="background:#ffe4ef">🧴</div><div><b>레드 블레미쉬 토너</b><small>진정 · 트러블 케어</small></div><div class="match">96%</div></div>
        <div class="prod"><div class="pface" style="background:#e4f7ff">☀️</div><div><b>마데카소사이드 선세럼</b><small>자외선 · 보습</small></div><div class="match">91%</div></div>
        <div class="prod"><div class="pface" style="background:#eafbe4">💧</div><div><b>6펩타이드 세럼</b><small>탄력 · 결</small></div><div class="match">88%</div></div>
        <div class="prod"><div class="pface" style="background:#fff2df">🌿</div><div><b>시카 데일리 크림</b><small>보습 · 장벽</small></div><div class="match">84%</div></div>
      </div>
    </section>

    <!-- COMMUNITY -->
    <section class="screen" data-screen="comm">
      <div class="h1"><em>피부 친구들</em> 💬</div>
      <div class="feed">
        <div class="post"><div class="ph"><div class="ava" style="background:#ff5fa2">J</div>준코 · 2분 전</div>
          <p>모공 토너 3주째 쓰는데 진짜 결 좋아짐 ㄷㄷ 같이 인증하실 분 🙌</p>
          <div class="rx">❤️ 24<span>💬 8</span><span>🔖</span></div></div>
        <div class="post"><div class="ph"><div class="ava" style="background:#4cc9ff">S</div>수현 · 15분 전</div>
          <p>턱 트러블 진정 루틴 공유함! 스캔 점수 62 → 74 올림 🔥</p>
          <div class="rx">❤️ 51<span>💬 19</span><span>🔖</span></div></div>
        <div class="post"><div class="ph"><div class="ava" style="background:#38e5b0">M</div>민지 · 1시간 전</div>
          <p>선세럼 매치율 91% 떠서 바로 질렀는데 만족 👍</p>
          <div class="rx">❤️ 12<span>💬 3</span><span>🔖</span></div></div>
      </div>
    </section>

    <!-- MY -->
    <section class="screen" data-screen="my">
      <div class="center" style="margin:6px 0;">
        <div class="buddy" style="width:96px;height:96px;animation:none;">
          <svg width="96" height="96" viewBox="0 0 132 132"><ellipse cx="66" cy="74" rx="52" ry="48" fill="#7a3cff"/><ellipse cx="66" cy="70" rx="44" ry="40" fill="#a06bff"/><circle cx="50" cy="66" r="9" fill="#fff"/><circle cx="82" cy="66" r="9" fill="#fff"/><circle cx="52" cy="68" r="4.5" fill="#20143f"/><circle cx="84" cy="68" r="4.5" fill="#20143f"/><path d="M56 84 q10 9 20 0" stroke="#20143f" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
        </div>
        <div class="h1" style="margin-top:6px;">민준 <em>Lv.7</em></div>
        <div class="sub">뷰티러너 · 연속 12일 🔥</div>
      </div>
      <div class="statrow">
        <div class="stat"><b>18</b><span>스캔</span></div>
        <div class="stat"><b>7</b><span>루틴</span></div>
        <div class="stat"><b>340</b><span>코인</span></div>
      </div>
      <div class="card"><div class="card-t">🏆 획득 배지</div>
        <div class="badges" style="margin-top:12px;">
          <div class="badge">🥇</div><div class="badge">💧</div><div class="badge">🔥</div><div class="badge lock">🔒</div>
        </div>
      </div>
      <button class="cta lime">🎁 오늘의 출석 보상 받기</button>
    </section>

  </div>

  <div class="toast" id="toast"></div>

  <nav class="nav" id="nav">
    <button class="nb on" data-go="home"><span class="ic">🏠</span>홈</button>
    <button class="nb" data-go="reco"><span class="ic">🛍️</span>추천</button>
    <button class="nb scan" data-go="scan"><span class="ic">📷</span></button>
    <button class="nb" data-go="comm"><span class="ic">💬</span>친구</button>
    <button class="nb" data-go="my"><span class="ic">😎</span>마이</button>
  </nav>
</div>

<script>
(function(){
  var screens = document.querySelectorAll('.screen');
  var nbs = document.querySelectorAll('.nb');
  function go(name){
    screens.forEach(function(s){ s.classList.toggle('on', s.dataset.screen===name); });
    nbs.forEach(function(b){ b.classList.toggle('on', b.dataset.go===name); });
  }
  nbs.forEach(function(b){ b.addEventListener('click', function(){ go(b.dataset.go); }); });

  var toast = document.getElementById('toast');
  function pop(msg){ toast.textContent=msg; toast.classList.add('on'); setTimeout(function(){ toast.classList.remove('on'); },1800); }

  document.querySelectorAll('.mission').forEach(function(m){
    m.addEventListener('click', function(){ if(!m.classList.contains('done')){ m.classList.add('done'); pop('미션 완료! +XP 🎉'); } });
  });
  document.querySelectorAll('.chip').forEach(function(c){
    c.addEventListener('click', function(){ document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('sel');}); c.classList.add('sel'); });
  });

  var scanBtn = document.getElementById('scanBtn');
  var scanScreen = document.getElementById('scanScreen');
  var scanMsg = document.getElementById('scanMsg');
  scanBtn.addEventListener('click', function(){
    scanScreen.classList.add('scanning');
    scanMsg.textContent = '버디가 분석 중... 🔍';
    scanBtn.style.opacity=.6; scanBtn.style.pointerEvents='none';
    setTimeout(function(){
      scanScreen.classList.remove('scanning');
      scanMsg.textContent = '완료! 스킨 레벨 +2 올랐어요 ✨';
      scanBtn.style.opacity=1; scanBtn.style.pointerEvents='auto';
      pop('스캔 완료! +50 XP 🪙');
      setTimeout(function(){ go('reco'); }, 900);
    }, 1800);
  });
})();
</script>
"""

components.html(HTML, height=900, scrolling=False)
