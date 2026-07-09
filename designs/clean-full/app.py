import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# FOR HIM — CLEAN (full): the minimal "clean" design system carrying the real
# product-matching engine, survey/camera analysis, recommendations, per-account
# records and Google (OIDC) login. Mobile-only, no page scroll: a phone shell
# with a bottom tab bar; each screen fills one viewport.
st.set_page_config(page_title="FOR HIM · CLEAN", layout="centered",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
  #MainMenu, header, footer {visibility:hidden;}
  [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {display:none !important;}
  [data-testid="stAppViewContainer"] {background:#0e0e0d;}
  .block-container, [data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"]
    {padding:0 !important; margin:0 !important; max-width:100% !important;}
  .stApp {overflow:hidden;}
  .stApp iframe {height:100dvh !important; width:100vw !important; border:none !important; display:block;}
  html, body {margin:0; padding:0; overflow:hidden;}
</style>
""", unsafe_allow_html=True)


def _secret(key: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(key, default))
    except Exception:
        return default


def _auth_configured() -> bool:
    try:
        return "auth" in st.secrets
    except Exception:
        return False


# --- real Google OIDC login (runs at the Python layer; iframe can't do OAuth) ---
auth_on = _auth_configured()
logged_in = False
user_email = ""
user_name = ""
app_url = ""
if auth_on:
    try:
        app_url = str(st.secrets["auth"].get("redirect_uri", ""))
        if app_url.endswith("/oauth2callback"):
            app_url = app_url[: -len("/oauth2callback")]
        app_url = app_url.rstrip("/")
    except Exception:
        app_url = ""
    try:
        if st.user.is_logged_in:
            logged_in = True
            user_email = getattr(st.user, "email", "") or ""
            user_name = getattr(st.user, "name", "") or ""
    except Exception:
        pass
    try:
        qp = st.query_params
    except Exception:
        qp = {}
    try:
        if not logged_in and qp.get("login") == "google":
            st.login()
        elif logged_in and qp.get("logout") == "1":
            st.logout()
        elif logged_in and "login" in qp:
            del st.query_params["login"]
    except Exception:
        pass

supabase_url = _secret("SUPABASE_URL")
supabase_key = _secret("SUPABASE_ANON_KEY")

logo_uri = ""
try:
    logo_path = Path(__file__).parent.parent.parent / "로고.png"
    logo_uri = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")
except Exception:
    logo_uri = ""

HTML = r"""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<style>
  *{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
  :root{ --ink:#17130f; --paper:#f6f3ee; --card:#fffdf9; --line:#e3ddd3; --mute:#9a9186; --accent:#2f5d4b; --accent2:#c9a86a; }
  html,body{height:100%;font-family:-apple-system,"Apple SD Gothic Neo","Helvetica Neue","Segoe UI",sans-serif;}
  body{display:flex;align-items:center;justify-content:center;min-height:100dvh;background:#0e0e0d;color:var(--ink);overflow:hidden;}
  .phone{position:relative;width:min(430px,100vw);height:min(900px,100dvh);background:var(--paper);
    display:flex;flex-direction:column;overflow:hidden;}
  @media(min-width:460px){ .phone{border-radius:34px;border:1px solid #262421;height:min(900px,96dvh);box-shadow:0 30px 90px rgba(0,0,0,.5);} }
  button{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit;}
  .ey{font-size:10.5px;font-weight:800;letter-spacing:2.5px;color:var(--mute);text-transform:uppercase;}
  .h1{font-size:26px;font-weight:800;line-height:1.2;letter-spacing:-.6px;}
  .h1 .thin{font-weight:300;} .h1 em{font-style:normal;color:var(--accent);}
  .lead{font-size:13px;color:#6b6459;line-height:1.6;font-weight:500;}
  .mute{color:var(--mute);}

  /* screen system */
  .stage{flex:1;position:relative;overflow:hidden;}
  .screen{position:absolute;inset:0;padding:22px 22px 16px;display:flex;flex-direction:column;gap:16px;
    opacity:0;transform:translateY(10px);pointer-events:none;transition:.4s cubic-bezier(.2,.8,.2,1);overflow:hidden;}
  .screen.on{opacity:1;transform:none;pointer-events:auto;}
  .grow{flex:1;min-height:0;}
  .bottomstick{margin-top:auto;}

  /* buttons */
  .btn{font-weight:700;font-size:15px;color:var(--paper);background:var(--ink);border-radius:14px;padding:16px;letter-spacing:.3px;transition:.15s;width:100%;}
  .btn:active{transform:scale(.985);opacity:.92;}
  .btn.accent{background:var(--accent);}
  .btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--ink);}
  .btn.sm{padding:12px;font-size:13.5px;border-radius:12px;}

  /* top bar (in-app) */
  .appbar{display:flex;align-items:center;padding:18px 22px 6px;flex-shrink:0;}
  .brand{font-size:15px;font-weight:800;letter-spacing:3px;} .brand span{color:var(--accent);}
  .appbar .r{margin-left:auto;width:34px;height:34px;border-radius:50%;background:#eceae4;display:grid;place-items:center;font-size:13px;font-weight:800;color:var(--accent);}

  /* score ring + metrics */
  .scorewrap{display:flex;align-items:center;gap:20px;}
  .ring{position:relative;width:118px;height:118px;flex-shrink:0;}
  .ring svg{transform:rotate(-90deg);}
  .ring .val{position:absolute;inset:0;display:grid;place-items:center;text-align:center;}
  .ring .val b{font-size:36px;font-weight:300;line-height:1;} .ring .val span{font-size:10px;letter-spacing:2px;color:var(--mute);}
  .metrics{flex:1;display:flex;flex-direction:column;gap:9px;}
  .metric span{display:flex;justify-content:space-between;font-size:12px;font-weight:600;margin-bottom:5px;}
  .metric span i{font-style:normal;color:var(--mute);}
  .track{height:3px;background:var(--line);border-radius:2px;overflow:hidden;}
  .track>i{display:block;height:100%;background:var(--accent);transition:width .8s cubic-bezier(.2,.8,.2,1);}

  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;}
  .hr{height:1px;background:var(--line);}

  /* chips (survey) */
  .chips{display:flex;flex-wrap:wrap;gap:8px;}
  .chip{font-size:13.5px;font-weight:700;color:var(--ink);padding:11px 16px;border-radius:12px;border:1px solid var(--line);background:var(--card);transition:.15s;}
  .chip.sel{background:var(--ink);color:var(--paper);border-color:var(--ink);}

  /* pills / tabs */
  .tabs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;flex-shrink:0;} .tabs::-webkit-scrollbar{display:none;}
  .tab{flex:0 0 auto;font-size:12.5px;font-weight:700;color:var(--mute);padding:8px 14px;border-radius:999px;border:1px solid var(--line);transition:.15s;white-space:nowrap;}
  .tab.sel{background:var(--ink);color:var(--paper);border-color:var(--ink);}

  /* product rows */
  .rows{display:flex;flex-direction:column;}
  .prow{display:flex;align-items:center;gap:12px;padding:13px 0;border-bottom:1px solid var(--line);text-decoration:none;color:inherit;}
  .prow:last-child{border-bottom:none;}
  .prow .rk{font-size:11px;font-weight:800;color:var(--mute);width:20px;flex-shrink:0;}
  .pth{width:44px;height:44px;border-radius:12px;flex-shrink:0;object-fit:cover;background:#eceae4;}
  .pbody{min-width:0;} .pbody b{font-size:13.5px;font-weight:700;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .pbody small{font-size:11px;color:var(--mute);}
  .pmatch{margin-left:auto;font-size:12px;font-weight:800;color:var(--accent);flex-shrink:0;}

  /* rows generic */
  .lrow{display:flex;align-items:center;gap:14px;padding:15px 0;border-bottom:1px solid var(--line);}
  .lrow:last-child{border-bottom:none;} .lrow .body b{font-size:14px;font-weight:700;display:block;} .lrow .body small{font-size:11.5px;color:var(--mute);}
  .lrow .arw{margin-left:auto;color:var(--mute);}

  /* camera */
  .cam{margin:auto 0;display:flex;flex-direction:column;align-items:center;gap:16px;}
  .camframe{width:210px;height:210px;border-radius:50%;overflow:hidden;position:relative;background:#111;border:1px solid var(--line);}
  .camframe video{width:100%;height:100%;object-fit:cover;}
  .camring{position:absolute;inset:0;border-radius:50%;border:2px dashed var(--accent);opacity:.55;}
  .scanning .camring{animation:rot 1.3s linear infinite;} @keyframes rot{to{transform:rotate(360deg);}}
  .cambar{width:180px;height:3px;background:var(--line);border-radius:2px;overflow:hidden;}
  .cambar>i{display:block;height:100%;width:0;background:var(--accent);transition:width .3s linear;}

  /* choice buttons */
  .choice{display:flex;flex-direction:column;gap:12px;}
  .cbtn{text-align:left;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:17px 18px;transition:.15s;}
  .cbtn:active{transform:scale(.99);} .cbtn.primary{background:var(--ink);color:var(--paper);border-color:var(--ink);}
  .cbtn b{font-size:15px;font-weight:700;display:block;} .cbtn small{font-size:12px;opacity:.75;}

  /* community */
  .feed{display:flex;flex-direction:column;}
  .post{padding:14px 0;border-bottom:1px solid var(--line);}
  .post .ph{display:flex;align-items:center;gap:9px;}
  .ava{width:30px;height:30px;border-radius:50%;background:#e6e3db;display:grid;place-items:center;font-weight:800;font-size:12px;color:var(--accent);}
  .post .ph b{font-size:12.5px;font-weight:700;} .post .ph time{font-size:11px;color:var(--mute);margin-left:auto;}
  .post .tt{font-size:14px;font-weight:700;margin-top:8px;} .post p{font-size:12.5px;color:#4d473e;line-height:1.5;margin-top:4px;}
  .post .rx{display:flex;gap:16px;margin-top:8px;font-size:11.5px;color:var(--mute);font-weight:600;}

  /* pager */
  .pager{display:flex;align-items:center;justify-content:center;gap:16px;font-size:12px;font-weight:700;color:var(--mute);}
  .pager button{color:var(--ink);font-weight:800;padding:6px 10px;} .pager button[disabled]{opacity:.3;}

  /* stat line */
  .statline{display:flex;text-align:center;}
  .statline>div{flex:1;padding:6px 0;border-right:1px solid var(--line);} .statline>div:last-child{border-right:none;}
  .statline b{font-size:24px;font-weight:300;display:block;} .statline span{font-size:10px;letter-spacing:1.5px;color:var(--mute);text-transform:uppercase;}
  .profile{display:flex;align-items:center;gap:16px;}
  .pav{width:60px;height:60px;border-radius:50%;background:var(--accent);color:var(--paper);display:grid;place-items:center;font-size:22px;font-weight:300;}

  /* consent */
  .cons{display:flex;flex-direction:column;gap:2px;}
  .cons label{display:flex;align-items:center;gap:11px;padding:14px 0;border-bottom:1px solid var(--line);font-size:13px;font-weight:600;}
  .cons .all{font-weight:800;font-size:14px;border-bottom:1px solid var(--line);}
  .cbox{width:22px;height:22px;border-radius:7px;border:1.5px solid var(--line);flex-shrink:0;display:grid;place-items:center;color:transparent;font-size:12px;transition:.15s;}
  .cons input{display:none;} .cons input:checked + .cbox{background:var(--accent);border-color:var(--accent);color:#fff;}
  .tag{font-size:10px;font-weight:800;padding:2px 7px;border-radius:6px;background:#eceae4;color:var(--mute);}
  .tag.req{background:var(--accent);color:#fff;}

  .field{display:flex;flex-direction:column;gap:6px;}
  .field label{font-size:12px;font-weight:700;color:var(--mute);}
  .field input{font-family:inherit;font-size:15px;padding:13px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--ink);}
  .field input:focus{outline:none;border-color:var(--accent);}

  /* splash */
  .splash{position:absolute;inset:0;z-index:60;background:var(--ink);display:grid;place-items:center;transition:opacity .5s;}
  .splash.gone{opacity:0;pointer-events:none;}
  .splash img{width:120px;filter:invert(1) brightness(1.6);opacity:.95;}
  .splash .fallback{color:var(--paper);font-size:22px;font-weight:800;letter-spacing:6px;}

  /* bottom nav */
  .nav{flex-shrink:0;display:none;justify-content:space-around;padding:11px 8px calc(13px + env(safe-area-inset-bottom));background:var(--paper);border-top:1px solid var(--line);}
  .nav.on{display:flex;}
  .nb{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:9.5px;font-weight:700;letter-spacing:.5px;color:var(--mute);flex:1;text-transform:uppercase;transition:.15s;}
  .nb.sel{color:var(--ink);} .nb svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.6;}

  .toast{position:absolute;left:50%;bottom:92px;transform:translateX(-50%) translateY(16px);opacity:0;background:var(--ink);color:var(--paper);font-weight:600;font-size:12.5px;padding:11px 18px;border-radius:12px;transition:.3s;pointer-events:none;white-space:nowrap;z-index:70;}
  .toast.on{opacity:1;transform:translateX(-50%);}
  .back{position:absolute;top:18px;left:18px;font-size:13px;font-weight:700;color:var(--mute);z-index:5;}
</style>

<div class="phone">
  <!-- splash -->
  <div class="splash" id="splash"><img src="__LOGO__" alt="FOR HIM" onerror="this.style.display='none';this.insertAdjacentHTML('afterend','<div class=fallback>FOR HIM</div>')"/></div>

  <div class="stage" id="stage">

    <!-- AUTH / membership entry -->
    <section class="screen" data-s="auth">
      <div class="ey">Membership</div>
      <div class="h1">내 피부, <span class="thin">기록해서<br/>관리해요.</span></div>
      <div class="lead">가입하면 분석 결과와 추천을 저장하고, 피부 변화를 계속 추적할 수 있어요.</div>
      <div class="rows" style="margin-top:4px;">
        <div class="lrow"><div class="body"><b>피부 기록 저장</b><small>분석 결과를 계정에 보관</small></div></div>
        <div class="lrow"><div class="body"><b>추천 이력 관리</b><small>받은 제품 추천을 한눈에</small></div></div>
        <div class="lrow"><div class="body"><b>변화 추적</b><small>이전 대비 피부 점수 비교</small></div></div>
      </div>
      <div class="bottomstick" style="display:flex;flex-direction:column;gap:10px;">
        <button class="btn" id="googleBtn">Google로 시작하기</button>
        <button class="btn ghost" id="skipBtn">회원가입 없이 둘러보기</button>
      </div>
    </section>

    <!-- CONSENT -->
    <section class="screen" data-s="consent">
      <div class="back" data-go="auth">‹ 뒤로</div>
      <div style="margin-top:18px;"><div class="ey">Agreement</div><div class="h1" style="margin-top:6px;">약관에 <span class="thin">동의해주세요.</span></div></div>
      <div class="lead">피부 데이터를 안전하게 관리하기 위해 아래 항목 동의가 필요해요.</div>
      <div class="cons" id="consList">
        <label class="all"><input type="checkbox" id="cAll"/><span class="cbox">✓</span>약관 전체 동의</label>
        <label><input type="checkbox" class="cchk" data-req="1"/><span class="cbox">✓</span><span class="tag req">필수</span>서비스 이용약관 및 개인정보 수집·이용</label>
        <label><input type="checkbox" class="cchk" data-req="0"/><span class="cbox">✓</span><span class="tag">선택</span>마케팅 정보 수신 동의</label>
      </div>
      <div class="lead" id="consHint" style="color:#b0453c;min-height:16px;"></div>
      <div class="bottomstick" style="display:flex;gap:10px;">
        <button class="btn ghost" id="consReq">필수만 동의</button>
        <button class="btn accent" id="consOk">동의하고 시작</button>
      </div>
    </section>

    <!-- PROFILE -->
    <section class="screen" data-s="profile">
      <div style="margin-top:8px;"><div class="ey">Profile</div><div class="h1" style="margin-top:6px;">프로필을 <span class="thin">설정해주세요.</span></div></div>
      <div class="field"><label>이메일</label><input type="email" id="pfEmail" readonly/></div>
      <div class="field"><label>나이</label><input type="number" id="pfAge" min="1" max="120" placeholder="나이"/></div>
      <div class="field"><label>닉네임</label><input type="text" id="pfNick" maxlength="12" placeholder="사용할 닉네임"/></div>
      <div class="lead" id="pfHint" style="color:#b0453c;min-height:16px;"></div>
      <button class="btn bottomstick" id="pfOk">시작하기</button>
    </section>

    <!-- START CHOICE -->
    <section class="screen" data-s="start">
      <div class="grow" style="display:flex;flex-direction:column;justify-content:center;gap:8px;">
        <div class="ey" style="text-align:center;">Welcome</div>
        <div class="h1" id="startTitle" style="text-align:center;">가입 완료 🎉</div>
        <div class="lead" style="text-align:center;margin-bottom:8px;">어떤 방식으로 피부를 확인해볼까요?</div>
        <div class="choice">
          <button class="cbtn primary" data-scan="cam"><b>영상 촬영으로 스캔하기</b><small>카메라로 얼굴을 비추면 AI가 바로 분석해요</small></button>
          <button class="cbtn" data-scan="survey"><b>설문으로 진단하기</b><small>카메라 없이 고민을 선택해 결과를 확인해요</small></button>
        </div>
      </div>
      <button class="btn ghost sm bottomstick" data-tab="my">내 피부 관리 페이지로 가기</button>
    </section>

    <!-- ======= MAIN APP (bottom nav) ======= -->

    <!-- HOME -->
    <section class="screen" data-s="home" data-nav>
      <div class="appbar" style="padding:0;"><div class="brand">FOR <span>HIM</span></div><div class="r" id="homeAv">MJ</div></div>
      <div><div class="ey">Today's skin</div><div class="h1" id="homeHello" style="margin-top:6px;">좋은 하루예요.</div></div>
      <div class="scorewrap" id="homeScore">
        <div class="ring"><svg width="118" height="118"><circle cx="59" cy="59" r="53" stroke="#e3ddd3" stroke-width="3" fill="none"/><circle id="homeArc" cx="59" cy="59" r="53" stroke="#2f5d4b" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="333" stroke-dashoffset="333"/></svg><div class="val"><b id="homeScoreN">–</b><span>SCORE</span></div></div>
        <div class="metrics" id="homeMetrics"></div>
      </div>
      <div class="lead" id="homeMsg">아직 분석 기록이 없어요. 오늘의 피부 스캔으로 시작해볼까요?</div>
      <button class="btn bottomstick" data-tab="scan">오늘의 피부 스캔</button>
    </section>

    <!-- SCAN / ANALYSIS -->
    <section class="screen" data-s="scan" data-nav>
      <div><div class="ey">Analysis</div><div class="h1" style="margin-top:6px;">피부 <span class="thin">진단.</span></div></div>
      <!-- entry: choose method -->
      <div class="choice" id="scanEntry" style="margin-top:6px;">
        <button class="cbtn primary" data-scan="cam"><b>영상 촬영으로 스캔</b><small>카메라로 얼굴 분석</small></button>
        <button class="cbtn" data-scan="survey"><b>설문으로 진단</b><small>고민을 선택해 결과 확인</small></button>
      </div>
    </section>

    <!-- CAMERA -->
    <section class="screen" data-s="cam" id="camScreen">
      <div class="back" data-tab="scan">‹ 뒤로</div>
      <div style="margin-top:18px;"><div class="ey">Camera scan</div><div class="h1" style="margin-top:6px;">얼굴을 <span class="thin">비춰주세요.</span></div></div>
      <div class="cam">
        <div class="camframe"><video id="camVideo" autoplay playsinline muted></video><div class="camring"></div></div>
        <div class="lead" id="camMsg" style="text-align:center;max-width:230px;">준비되면 스캔을 시작하세요. 5초간 천천히 고개를 움직여주세요.</div>
        <div class="cambar"><i id="camFill"></i></div>
      </div>
      <button class="btn accent bottomstick" id="camStart">스캔 시작</button>
    </section>

    <!-- SURVEY -->
    <section class="screen" data-s="survey">
      <div class="back" data-tab="scan">‹ 뒤로</div>
      <div style="margin-top:18px;"><div class="ey">Survey</div><div class="h1" style="margin-top:6px;">지금 <span class="thin">가장 신경 쓰이는</span> 곳은?</div></div>
      <div class="lead">복수 선택할 수 있어요.</div>
      <div class="chips" id="chips">
        <button class="chip" data-k="scar">파인 흉터</button>
        <button class="chip" data-k="pore">넓은 모공</button>
        <button class="chip" data-k="oil">피지·유분</button>
        <button class="chip" data-k="acne">화농성 여드름</button>
      </div>
      <div class="lead" id="svHint" style="color:#b0453c;min-height:16px;"></div>
      <button class="btn accent bottomstick" id="svGo">AI 분석 시작</button>
    </section>

    <!-- RESULT -->
    <section class="screen" data-s="result">
      <div><div class="ey">Result</div><div class="h1" style="margin-top:6px;">피부 <span class="thin">리포트.</span></div></div>
      <div class="scorewrap">
        <div class="ring"><svg width="118" height="118"><circle cx="59" cy="59" r="53" stroke="#e3ddd3" stroke-width="3" fill="none"/><circle id="rsArc" cx="59" cy="59" r="53" stroke="#2f5d4b" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="333" stroke-dashoffset="333"/></svg><div class="val"><b id="rsScore">–</b><span>SCORE</span></div></div>
        <div class="metrics" id="rsMetrics"></div>
      </div>
      <div class="lead" id="rsSummary"></div>
      <button class="btn bottomstick" data-tab="reco">맞춤 제품 추천 받기</button>
    </section>

    <!-- RECOMMEND -->
    <section class="screen" data-s="reco" data-nav>
      <div><div class="ey">Curated</div><div class="h1" style="margin-top:6px;">추천 <span class="thin">루틴.</span></div></div>
      <div class="tabs" id="tierTabs"></div>
      <div class="lead" id="tierDesc" style="min-height:34px;"></div>
      <div class="rows grow" id="tierRows"></div>
    </section>

    <!-- COMMUNITY -->
    <section class="screen" data-s="comm" data-nav>
      <div style="display:flex;align-items:center;"><div><div class="ey">Community</div><div class="h1" style="margin-top:6px;">함께 <span class="thin">기록해요.</span></div></div>
        <button class="btn sm" id="cmWrite" style="width:auto;margin-left:auto;padding:9px 14px;">글쓰기</button></div>
      <div class="tabs" id="cmCats"></div>
      <div class="feed grow" id="cmFeed"></div>
      <div class="pager" id="cmPager"></div>
    </section>

    <!-- COMMUNITY WRITE -->
    <section class="screen" data-s="cwrite">
      <div class="back" data-tab="comm">‹ 뒤로</div>
      <div style="margin-top:18px;"><div class="ey">New post</div><div class="h1" style="margin-top:6px;">새 글 <span class="thin">남기기.</span></div></div>
      <div class="field"><label>제목</label><input type="text" id="cwTitle" maxlength="40" placeholder="제목"/></div>
      <div class="field grow"><label>내용</label><textarea id="cwBody" placeholder="같은 고민을 가진 분들에게 편하게 이야기해보세요" style="flex:1;font-family:inherit;font-size:14px;padding:13px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);resize:none;"></textarea></div>
      <button class="btn accent bottomstick" id="cwOk">등록하기</button>
    </section>

    <!-- MY -->
    <section class="screen" data-s="my" data-nav>
      <div class="ey">Profile</div>
      <div class="profile"><div class="pav" id="myAv">M</div><div><div class="h1" id="myName" style="font-size:21px;">회원</div><div class="lead" id="myMeta" style="margin-top:2px;"></div></div></div>
      <div class="statline"><div><b id="stA">0</b><span>Scans</span></div><div><b id="stR">0</b><span>Routines</span></div><div><b id="stT">–</b><span>Trend</span></div></div>
      <div class="hr"></div>
      <div class="tabs" id="myTabs"><button class="tab sel" data-mt="analyses">분석 내역</button><button class="tab" data-mt="recommends">추천 이력</button></div>
      <div class="rows grow" id="myList"></div>
      <button class="btn ghost sm bottomstick" id="logoutBtn">로그아웃</button>
    </section>

  </div>

  <div class="toast" id="toast"></div>

  <nav class="nav" id="nav">
    <button class="nb" data-tab="home"><svg viewBox="0 0 24 24"><path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg>Home</button>
    <button class="nb" data-tab="scan"><svg viewBox="0 0 24 24"><path d="M4 8V5a1 1 0 0 1 1-1h3M20 8V5a1 1 0 0 0-1-1h-3M4 16v3a1 1 0 0 0 1 1h3M20 16v3a1 1 0 0 1-1 1h-3"/><circle cx="12" cy="12" r="3.2"/></svg>Scan</button>
    <button class="nb" data-tab="reco"><svg viewBox="0 0 24 24"><path d="M6 7h12l-1 13H7z"/><path d="M9 7a3 3 0 0 1 6 0"/></svg>Shop</button>
    <button class="nb" data-tab="comm"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/></svg>Feed</button>
    <button class="nb" data-tab="my"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/></svg>My</button>
  </nav>
</div>

<script>
(function(){
  var W = window;
  var state = { concerns:new Set(), age:29, nickname:'', email:'', analyzed:false };
  var CONCERN_LABEL = { scar:'파인 흉터', pore:'넓은 모공', oil:'피지·유분', acne:'화농성 여드름' };

  /* ---------- product catalog + real matching engine (ported) ---------- */
  var PIMG = {
    cosrx:'https://dn5hzapyfrpio.cloudfront.net/product/a97/a97c0080-1b38-11f0-a461-e9e3e4353caa.jpeg?w=200',
    toriden:'https://dn5hzapyfrpio.cloudfront.net/product/302/3029f520-5fed-11f1-94d9-bb4c387ac818.jpeg?w=200',
    anua:'https://dn5hzapyfrpio.cloudfront.net/product/18f/18f9d910-e811-11ef-b7ff-9d94b272a52e.jpeg?w=200',
    mediheal:'https://dn5hzapyfrpio.cloudfront.net/product/bf9/bf9d94f0-77ef-11f0-ba45-05d1d2abb09d.jpeg?w=200',
    ahc:'https://dn5hzapyfrpio.cloudfront.net/product/417/417b9320-49b2-11f1-ab05-f74f22f2eff9.jpeg?w=200',
    goodal:'https://dn5hzapyfrpio.cloudfront.net/product/6f3/6f3891e0-c8cb-11f0-b07b-5b53b651bab0.jpeg?w=200',
    jsm:'https://dn5hzapyfrpio.cloudfront.net/product/5f6/5f61dd30-7850-11ee-b842-db65e1eeb438.jpeg?w=200',
    hera:'https://dn5hzapyfrpio.cloudfront.net/product/fe1/fe18aa80-ebc8-11ee-8b0a-6d2974cceb54.jpeg?w=200',
    clioCushion:'https://dn5hzapyfrpio.cloudfront.net/product/a88/a88ee6f0-846b-11f0-b021-b5dec3c00b35.jpeg?w=200',
    lumir:'https://dn5hzapyfrpio.cloudfront.net/product/629/629e9f90-47ff-11ef-9c5c-759480f80bcd.jpeg?w=200',
    peripera:'https://dn5hzapyfrpio.cloudfront.net/product/d34/d3475980-92e5-11f0-9444-11e570e33be4.jpeg?w=200',
    clioEye:'https://dn5hzapyfrpio.cloudfront.net/product/9cb/9cbc3980-4242-11ee-88cc-5d4011facace.jpeg?w=200',
    physiogel:'https://dn5hzapyfrpio.cloudfront.net/product/b1f/b1fc6de0-b9f2-11f0-97cf-eb8f804ad159.jpeg?w=200',
    drg:'https://dn5hzapyfrpio.cloudfront.net/product/c67/c671e760-8bd2-11ed-a6ae-7f4a9ccf8e92.jpeg?w=200',
    medicubeMist:'https://dn5hzapyfrpio.cloudfront.net/product/adb/adbe3440-984e-11f0-9b5e-4999a7af4d26.jpeg?w=200'
  };
  var ALL_TAGS = ['pore','oil','acne','scar','elastic','texture','spot','blemish','tone','blackhead','darkcircle','shave','ingrown','dull','dryness','redness','pigment','flake','wrinkle','cover'];
  var PRODUCTS = [
    {id:'cosrx',brand:'코스알엑스',name:'더 6 펩타이드 스킨 부스터 세럼',img:PIMG.cosrx,color:'#8b6f47',cats:['serum'],pop:96,tag:'결·컨디션 개선',aff:{pore:2,texture:3,acne:2,blemish:2,pigment:2,dull:2,spot:1,scar:1}},
    {id:'toriden',brand:'토리든',name:'다이브인 저분자 히알루론산 세럼',img:PIMG.toriden,color:'#5c7a8b',cats:['serum'],pop:94,tag:'저분자 수분 진정',aff:{dryness:3,texture:2,redness:2,flake:2,darkcircle:1}},
    {id:'anua',brand:'아누아',name:'PDRN 히알루론산 캡슐 100 세럼',img:PIMG.anua,color:'#7a8b5c',cats:['serum'],pop:90,tag:'PDRN 재생 케어',aff:{scar:3,pigment:2,elastic:2,tone:2,darkcircle:1,spot:2}},
    {id:'anuaTuner',brand:'아누아',name:'어성초 77 토너',color:'#7a8b5c',cats:['toner'],pop:82,tag:'모공·진정 토너',aff:{pore:3,oil:2,acne:2,ingrown:2,flake:2,texture:2,blackhead:2}},
    {id:'mediheal',brand:'메디힐',name:'마데카소사이드 수분 선세럼',img:PIMG.mediheal,color:'#6b8b6f',cats:['sun'],pop:85,tag:'저자극 선케어',aff:{oil:2,redness:2,acne:2}},
    {id:'ahc',brand:'AHC',name:'마스터즈 에어 리치 선스틱',img:PIMG.ahc,color:'#4a7a9b',cats:['sun'],pop:88,tag:'산뜻한 선스틱',aff:{oil:2,dull:1}},
    {id:'goodalSun',brand:'구달',name:'맑은 어성초 진정 수분 선크림',img:PIMG.goodal,color:'#7a9b6f',cats:['sun'],pop:80,tag:'민감성 선크림',aff:{oil:2,redness:2,acne:2}},
    {id:'goodalVitaC',brand:'구달',name:'청귤 비타C 잡티 세럼',color:'#c9915c',cats:['serum'],pop:87,tag:'비타민C 브라이트닝',aff:{spot:3,pigment:3,tone:2,dull:2,blemish:2}},
    {id:'jsm',brand:'정샘물',name:'에센셜 스킨 누더 쿠션',img:PIMG.jsm,color:'#c9915c',cats:['cushion'],pop:89,tag:'자연스러운 피부 보정',aff:{cover:3,tone:2,dull:1}},
    {id:'hera',brand:'헤라',name:'블랙 쿠션 파운데이션',img:PIMG.hera,color:'#9b7a4a',cats:['cushion'],pop:84,tag:'커버 + 지속력',aff:{cover:3,tone:2,scar:1}},
    {id:'clioCushion',brand:'클리오',name:'킬커버 파운웨어 쿠션',img:PIMG.clioCushion,color:'#b58b5c',cats:['cushion'],pop:83,tag:'모공 커버',aff:{cover:3,pore:1,tone:2}},
    {id:'lumir',brand:'루미르',name:'라이트 온 아이즈 섀도우 팔레트',img:PIMG.lumir,color:'#9b6f8b',cats:['eye'],pop:72,tag:'퍼스널컬러 팔레트',aff:{}},
    {id:'peripera',brand:'페리페라',name:'올테이크 무드 팔레트',img:PIMG.peripera,color:'#c15c5c',cats:['eye'],pop:78,tag:'데일리 아이 컬러',aff:{}},
    {id:'clioEye',brand:'클리오',name:'프로 아이 팔레트 에어',img:PIMG.clioEye,color:'#a85c6f',cats:['eye'],pop:76,tag:'데일리 섀도우',aff:{}},
    {id:'medicubeAger',brand:'메디큐브',name:'AGE-R 부스터 프로',color:'#5c6f8b',cats:['device'],pop:79,tag:'리프팅 디바이스',aff:{elastic:3,wrinkle:2,dull:1}},
    {id:'vflab',brand:'브이플랩',name:'브이토닝 디바이스',color:'#6f5c8b',cats:['device'],pop:70,tag:'얼굴 라인 관리',aff:{elastic:2}},
    {id:'wellbeing',brand:'웰빙시크릿',name:'4D 페이스 마사지기',color:'#5c8b7a',cats:['device'],pop:68,tag:'붓기 케어',aff:{darkcircle:2,elastic:1}},
    {id:'estraCream',brand:'에스트라',name:'아토베리어365 크림',color:'#6b7a8b',cats:['cream'],pop:86,tag:'장벽 강화 크림',aff:{dryness:3,redness:2,elastic:2,flake:2}},
    {id:'origins',brand:'오리진스',name:'메가 버섯 퍼스트 에센스',color:'#8b7a5c',cats:['serum'],pop:74,tag:'탄력 영양 에센스',aff:{elastic:2,dull:2,texture:2}},
    {id:'medicubeMist',brand:'메디큐브',name:'PDRN 핑크 콜라겐 젤리 미스트 세럼',img:PIMG.medicubeMist,color:'#a86f7a',cats:['serum'],pop:81,tag:'PDRN 재생 미스트',aff:{elastic:2,darkcircle:2,dryness:2,dull:1,scar:1}},
    {id:'esnature',brand:'에스네이처',name:'아쿠아 스쿠알란 수분크림',color:'#6b8b8b',cats:['cream'],pop:77,tag:'수분 진정 크림',aff:{dryness:3,redness:1,flake:1}},
    {id:'drg',brand:'닥터지',name:'레드 블레미쉬 클리어 수딩 토너',img:PIMG.drg,color:'#a85c5c',cats:['toner'],pop:88,tag:'트러블 진정 토너',aff:{acne:3,blemish:2,redness:3,shave:2}},
    {id:'roundlabMadeca',brand:'라운드랩',name:'마데카 크림',color:'#5c8b6f',cats:['cream'],pop:85,tag:'재생 진정 크림',aff:{redness:2,acne:2,shave:2,ingrown:2,elastic:1}},
    {id:'cosrxBHA',brand:'코스알엑스',name:'BHA 블랙헤드 파워 리퀴드',color:'#8b6f47',cats:['toner'],pop:84,tag:'모공 각질 케어',aff:{blackhead:3,pore:2,flake:2,ingrown:2,texture:2}},
    {id:'innisfree',brand:'이니스프리',name:'그린티 클렌징폼',color:'#5c8b6f',cats:['cleanser'],pop:75,tag:'산뜻한 세안',aff:{blackhead:2,oil:2}},
    {id:'estraCleanser',brand:'에스트라',name:'아토베리어365 클렌징폼',color:'#6b7a8b',cats:['cleanser'],pop:76,tag:'저자극 클렌징',aff:{dryness:2,redness:1}},
    {id:'roundlabBirch',brand:'라운드랩',name:'자작나무 수분크림',color:'#5c8b6f',cats:['cream'],pop:80,tag:'수분 진정',aff:{dryness:2,ingrown:1,redness:1}},
    {id:'physiogel',brand:'피지오겔',name:'데일리 모이스쳐 테라피 에센스 인 토너',img:PIMG.physiogel,color:'#a86f6f',cats:['toner'],pop:78,tag:'저자극 수분 토너',aff:{dryness:2,redness:2,shave:2,darkcircle:1,flake:2}}
  ];
  function buildProfile(){
    var c = state.concerns, age = state.age||29, sev = {}, BASE=0.32;
    ALL_TAGS.forEach(function(t){ sev[t]=BASE; });
    function bump(t,v){ sev[t]=Math.min(1,Math.max(sev[t],v)); }
    if(c.has('oil')){ bump('oil',.95);bump('blackhead',.7);bump('shave',.55);bump('dull',.5);bump('acne',.55); }
    if(c.has('pore')){ bump('pore',.95);bump('blackhead',.7);bump('texture',.65);bump('flake',.5); }
    if(c.has('acne')){ bump('acne',.95);bump('blemish',.75);bump('redness',.65);bump('ingrown',.55);bump('shave',.6); }
    if(c.has('scar')){ bump('scar',.95);bump('pigment',.8);bump('spot',.6);bump('tone',.6);bump('texture',.55); }
    if(age>=30){ bump('elastic',.6);bump('wrinkle',.6);bump('darkcircle',.5);bump('dull',.5);bump('dryness',.5); }
    if(age>=40){ bump('elastic',.85);bump('wrinkle',.85);bump('pigment',.6); }
    return { sev:sev };
  }
  function scoreProduct(p,pr){ var s=0; for(var t in p.aff){ s+=p.aff[t]*(pr.sev[t]||0); } s+=(p.pop||70)*0.012; return s; }
  function recommendFrom(pool,N,focal){
    var pr=buildProfile();
    var scored=pool.map(function(p){ return {p:p,s:scoreProduct(p,pr)+(focal?(p.aff[focal]||0)*1.7:0)}; });
    var max=scored.reduce(function(m,x){ return Math.max(m,x.s); },0.0001);
    scored.sort(function(a,b){ return b.s-a.s; });
    return scored.slice(0,N).map(function(x,i){ var o=Object.assign({},x.p); o.rank=i+1; o.match=Math.round(72+27*(x.s/max)); return o; });
  }
  function recommendForCat(cat,N){ return recommendFrom(PRODUCTS.filter(function(p){ return p.cats.indexOf(cat)>=0; }),N,null); }

  var TIERS=[
    {key:'t1',label:'세럼',cat:'serum',desc:'클렌징·스킨·세럼으로 여드름을 억제하고 전반적인 피부 컨디션을 개선해요.'},
    {key:'t2',label:'선크림',cat:'sun',desc:'기초에 이어 피부 타입에 맞는 선케어로 노화·주름까지 예방해요.'},
    {key:'t3',label:'쿠션',cat:'cushion',desc:'기초·선케어에 이어 간단한 색조로 피부 보정 효과를 더해요.'},
    {key:'t4',label:'아이',cat:'eye',desc:'퍼스널 컬러에 맞는 섀도우로 나만의 개성을 표현해요.'},
    {key:'t5',label:'디바이스',cat:'device',desc:'뷰티 디바이스로 얼굴형과 붓기까지 관리해요.'}
  ];

  /* ---------- diagnosis metrics (ported) ---------- */
  function computeMetrics(){
    var b={수분:74,유분조절:76,모공:78,트러블:80,탄력:75}, c=state.concerns;
    if(c.has('scar')){ b.탄력-=20; b.트러블-=8; }
    if(c.has('pore')){ b.모공-=35; }
    if(c.has('oil')){ b.유분조절-=32; b.수분-=8; }
    if(c.has('acne')){ b.트러블-=35; b.유분조절-=10; }
    Object.keys(b).forEach(function(k){ b[k]=Math.max(15,Math.min(95,b[k])); });
    return b;
  }

  /* ---------- per-account records ---------- */
  var MEMBER_KEY='forhimc_member', REC_PREFIX='forhimc_rec_', GUEST_KEY='forhimc_rec_guest';
  var member=null; try{ member=JSON.parse(localStorage.getItem(MEMBER_KEY)||'null'); }catch(e){}
  function isMember(){ return !!(member && member.loggedIn); }
  function memberId(){ if(!member) return ''; return (member.email?member.email.toLowerCase():'m:'+(member.nickname||''))||'m'; }
  function recKey(){ return isMember()?(REC_PREFIX+memberId()):GUEST_KEY; }
  function emptyRec(){ return {analyses:[],recommends:[]}; }
  function readRec(k){ try{ var r=JSON.parse(localStorage.getItem(k)||'null'); if(r) return r; }catch(e){} return null; }
  var records=readRec(recKey())||emptyRec();
  function saveRec(){ try{ localStorage.setItem(recKey(),JSON.stringify(records)); }catch(e){} }
  function refreshRec(){ records=readRec(recKey())||emptyRec(); }
  function mergeGuest(){
    var g=readRec(GUEST_KEY), a=readRec(REC_PREFIX+memberId())||emptyRec();
    if(g){ ['analyses','recommends'].forEach(function(cat){ var have=new Set((a[cat]||[]).map(function(x){return x.id;})); (g[cat]||[]).forEach(function(x){ if(!have.has(x.id)) a[cat].push(x); }); a[cat].sort(function(x,y){return y.date-x.date;}); }); try{ localStorage.removeItem(GUEST_KEY); }catch(e){} }
    records=a; try{ localStorage.setItem(REC_PREFIX+memberId(),JSON.stringify(a)); }catch(e){}
  }
  function labels(){ return Array.from(state.concerns).map(function(k){ return CONCERN_LABEL[k]; }); }
  function recordAnalysis(overall){
    var cs=labels(); var rec={id:'a'+Date.now(),date:Date.now(),score:overall,
      type: state.concerns.has('oil')?'지성':(state.concerns.has('pore')||state.concerns.has('scar'))?'복합성':'중성',
      summary:(cs.join('·')||'전반')+' 중심 분석, 종합 '+overall+'점'};
    if(records.analyses[0]&&Date.now()-records.analyses[0].date<60000) records.analyses[0]=rec; else records.analyses.unshift(rec);
    saveRec();
  }
  function recordRecommend(){
    var cs=labels(); var rec={id:'r'+Date.now(),date:Date.now(),title:(cs.join('·')||'맞춤')+' 루틴 추천',summary:'AI 매칭 기반 단계별 추천'};
    if(records.recommends[0]&&Date.now()-records.recommends[0].date<60000) records.recommends[0]=rec; else records.recommends.unshift(rec);
    saveRec();
  }
  function fmtDate(ts){ var d=new Date(ts),p=function(n){return String(n).padStart(2,'0');}; return d.getFullYear()+'.'+p(d.getMonth()+1)+'.'+p(d.getDate()); }

  /* ---------- screens / nav ---------- */
  var screens=document.querySelectorAll('.screen'), nbs=document.querySelectorAll('.nb'), navBar=document.getElementById('nav');
  function show(name){
    var el=null;
    screens.forEach(function(s){ var on=s.dataset.s===name; s.classList.toggle('on',on); if(on) el=s; });
    var isTab = el && el.hasAttribute('data-nav');
    navBar.classList.toggle('on', !!isTab);
    nbs.forEach(function(b){ b.classList.toggle('sel', b.dataset.tab===name); });
  }
  document.querySelectorAll('[data-tab]').forEach(function(b){ b.addEventListener('click', function(){ go(b.dataset.tab); }); });
  document.querySelectorAll('[data-go]').forEach(function(b){ b.addEventListener('click', function(){ show(b.dataset.go); }); });
  function go(name){ // tab entries with side effects
    if(name==='reco'){ recordRecommend(); renderTiers(); }
    if(name==='home') renderHome();
    if(name==='my') renderMy();
    if(name==='comm') renderFeed();
    show(name);
  }

  var toast=document.getElementById('toast');
  function pop(m){ toast.textContent=m; toast.classList.add('on'); setTimeout(function(){ toast.classList.remove('on'); },1800); }

  /* ---------- ring helper ---------- */
  function setRing(arcId,numId,score){
    var C=333, off=C*(1-score/100);
    var arc=document.getElementById(arcId); if(arc) arc.style.strokeDashoffset=off;
    var n=document.getElementById(numId); if(n) n.textContent=score;
  }
  function renderMetrics(el,metrics){
    el.innerHTML=Object.keys(metrics).map(function(k){
      return '<div class="metric"><span>'+k+' <i>'+metrics[k]+'</i></span><div class="track"><i style="width:0%"></i></div></div>';
    }).join('');
    requestAnimationFrame(function(){ var fills=el.querySelectorAll('.track>i'), vals=Object.values(metrics); fills.forEach(function(f,i){ f.style.width=vals[i]+'%'; }); });
  }

  /* ---------- home ---------- */
  function renderHome(){
    var name=(member&&member.nickname)||state.nickname||'회원';
    document.getElementById('homeHello').innerHTML='좋은 하루예요, <span class="thin">'+name+'님.</span>';
    document.getElementById('homeAv').textContent=name.charAt(0)||'M';
    var last=records.analyses[0];
    if(last){
      var m=computeMetrics(); setRing('homeArc','homeScoreN',last.score);
      renderMetrics(document.getElementById('homeMetrics'),m);
      document.getElementById('homeMsg').textContent=fmtDate(last.date)+' · '+last.summary;
    } else {
      setRing('homeArc','homeScoreN',0); document.getElementById('homeScoreN').textContent='–';
      document.getElementById('homeMetrics').innerHTML='';
      document.getElementById('homeMsg').textContent='아직 분석 기록이 없어요. 오늘의 피부 스캔으로 시작해볼까요?';
    }
  }

  /* ---------- survey ---------- */
  document.querySelectorAll('#chips .chip').forEach(function(c){
    c.addEventListener('click', function(){ var k=c.dataset.k; if(state.concerns.has(k)){ state.concerns.delete(k); c.classList.remove('sel'); } else { state.concerns.add(k); c.classList.add('sel'); } document.getElementById('svHint').textContent=''; });
  });
  document.getElementById('svGo').addEventListener('click', function(){
    if(state.concerns.size===0){ document.getElementById('svHint').textContent='최소 1개 이상 선택해주세요.'; return; }
    runAnalysis();
  });

  /* ---------- camera ---------- */
  var camStream=null;
  function openCam(){
    show('cam'); var v=document.getElementById('camVideo');
    if(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia){
      navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false}).then(function(s){ camStream=s; v.srcObject=s; }).catch(function(){});
    }
  }
  function stopCam(){ if(camStream){ camStream.getTracks().forEach(function(t){t.stop();}); camStream=null; } }
  document.getElementById('camStart').addEventListener('click', function(){
    var sc=document.getElementById('camScreen'); sc.classList.add('scanning');
    document.getElementById('camMsg').textContent='피부 상태를 분석하고 있어요…';
    var f=document.getElementById('camFill'), p=0;
    var iv=setInterval(function(){ p+=10; f.style.width=p+'%'; if(p>=100){ clearInterval(iv); sc.classList.remove('scanning'); stopCam();
      if(state.concerns.size===0){ ['scar','pore','oil','acne'].forEach(function(k){ state.concerns.add(k); }); syncChips(); }
      runAnalysis(); } }, 200);
  });
  function syncChips(){ document.querySelectorAll('#chips .chip').forEach(function(c){ c.classList.toggle('sel', state.concerns.has(c.dataset.k)); }); }

  /* ---------- run analysis -> result ---------- */
  function runAnalysis(){
    var m=computeMetrics(); var vals=Object.values(m); var overall=Math.round(vals.reduce(function(a,b){return a+b;},0)/vals.length);
    setRing('rsArc','rsScore',overall); renderMetrics(document.getElementById('rsMetrics'),m);
    var lab=labels(); var listText=lab.length?lab.join(', '):'특별한 고민';
    var tone=overall>=70?'전반적으로 관리가 잘 되고 있어요. 지금 루틴을 유지하면서 조금만 보완해볼까요?':overall>=50?'조금만 신경 쓰면 확실히 달라질 수 있는 단계예요.':'지금부터 관리를 시작하기 좋은 시점이에요.';
    document.getElementById('rsSummary').textContent=listText+' 고민을 중심으로 분석했어요. 종합 스코어는 '+overall+'점이에요. '+tone;
    state.analyzed=true; recordAnalysis(overall);
    show('result');
  }

  /* ---------- recommend ---------- */
  var activeTier='t1';
  function renderTiers(){
    document.getElementById('tierTabs').innerHTML=TIERS.map(function(t){ return '<button class="tab'+(t.key===activeTier?' sel':'')+'" data-tier="'+t.key+'">'+t.label+'</button>'; }).join('');
    document.querySelectorAll('#tierTabs .tab').forEach(function(b){ b.addEventListener('click', function(){ activeTier=b.dataset.tier; renderTiers(); }); });
    var tier=TIERS.filter(function(t){return t.key===activeTier;})[0];
    document.getElementById('tierDesc').textContent=tier.desc;
    var list=recommendForCat(tier.cat,3);
    document.getElementById('tierRows').innerHTML=list.map(function(p){
      var q=encodeURIComponent(p.brand+' '+p.name);
      var thumb=p.img?('<img class="pth" src="'+p.img+'" onerror="this.style.background=\''+p.color+'\';this.removeAttribute(\'src\')"/>'):('<div class="pth" style="background:'+p.color+'"></div>');
      return '<a class="prow" target="_blank" rel="noopener" href="https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query='+q+'">'+
        '<span class="rk">'+p.rank+'</span>'+thumb+'<div class="pbody"><b>'+p.name+'</b><small>'+p.brand+' · '+p.tag+'</small></div>'+
        (p.match?'<span class="pmatch">'+p.match+'%</span>':'')+'</a>';
    }).join('');
  }

  /* ---------- community (localStorage; Supabase sync planned next) ---------- */
  var CM_CATS=[{k:'all',l:'전체'},{k:'pore',l:'모공'},{k:'oil',l:'유분'},{k:'acne',l:'트러블'},{k:'scar',l:'흉터'},{k:'sensitive',l:'민감성'}];
  var CM_KEY='forhimc_posts', cmCat='all', cmPage=0, PER=4;
  function cmSeed(){ var n=Date.now(),D=3600000; return [
    {id:'p1',cat:'pore',author:'준코',title:'모공 토너 3주 후기',body:'결이 확실히 정돈됐어요. 같은 고민 있으신 분들과 기록 공유하고 싶어요.',date:n-2*60000,likes:24,comments:8},
    {id:'p2',cat:'acne',author:'수현',title:'턱 트러블 진정 루틴',body:'스캔 점수 62 → 74 로 올랐어요. 진정+유분 관리 위주로 했습니다.',date:n-15*60000,likes:51,comments:19},
    {id:'p3',cat:'oil',author:'민지',title:'선세럼 매치율 91%',body:'추천 매치율 보고 구매했는데 발림성 좋네요.',date:n-D,likes:12,comments:3},
    {id:'p4',cat:'scar',author:'도윤',title:'흉터 자국 PDRN 세럼',body:'재생 세럼 두 달째. 붉은 자국이 옅어지는 느낌이에요.',date:n-2*D,likes:33,comments:6},
    {id:'p5',cat:'sensitive',author:'하준',title:'면도 후 진정 팁',body:'면도 직후 시카 크림 얇게. 트러블이 확 줄었어요.',date:n-5*D,likes:18,comments:4}
  ]; }
  function cmLoad(){ try{ var r=JSON.parse(localStorage.getItem(CM_KEY)||'null'); if(r) return r; }catch(e){} var s=cmSeed(); cmSave(s); return s; }
  function cmSave(list){ try{ localStorage.setItem(CM_KEY,JSON.stringify(list)); }catch(e){} }
  var cmPosts=cmLoad();
  function cmAgo(ts){ var d=Date.now()-ts,m=60000,h=3600000,dd=86400000; if(d<m)return '방금 전'; if(d<h)return Math.floor(d/m)+'분 전'; if(d<dd)return Math.floor(d/h)+'시간 전'; return Math.floor(d/dd)+'일 전'; }
  function renderFeed(){
    document.getElementById('cmCats').innerHTML=CM_CATS.map(function(c){ return '<button class="tab'+(c.k===cmCat?' sel':'')+'" data-cat="'+c.k+'">'+c.l+'</button>'; }).join('');
    document.querySelectorAll('#cmCats .tab').forEach(function(b){ b.addEventListener('click', function(){ cmCat=b.dataset.cat; cmPage=0; renderFeed(); }); });
    var list=cmPosts.filter(function(p){ return cmCat==='all'||p.cat===cmCat; }).sort(function(a,b){ return b.date-a.date; });
    var pages=Math.max(1,Math.ceil(list.length/PER)); if(cmPage>=pages) cmPage=0;
    var slice=list.slice(cmPage*PER,cmPage*PER+PER);
    document.getElementById('cmFeed').innerHTML=slice.length?slice.map(function(p){
      return '<div class="post"><div class="ph"><div class="ava">'+esc(p.author.charAt(0))+'</div><b>'+esc(p.author)+'</b><time>'+cmAgo(p.date)+'</time></div>'+
        '<div class="tt">'+esc(p.title)+'</div><p>'+esc(p.body)+'</p><div class="rx"><span>♡ '+p.likes+'</span><span>댓글 '+p.comments+'</span></div></div>';
    }).join(''):'<div class="lead" style="text-align:center;padding:30px 0;">아직 글이 없어요.</div>';
    document.getElementById('cmPager').innerHTML= pages>1 ?
      '<button id="cmPrev"'+(cmPage===0?' disabled':'')+'>‹ 이전</button><span>'+(cmPage+1)+' / '+pages+'</span><button id="cmNext"'+(cmPage>=pages-1?' disabled':'')+'>다음 ›</button>' : '';
    var pv=document.getElementById('cmPrev'), nx=document.getElementById('cmNext');
    if(pv) pv.addEventListener('click', function(){ if(cmPage>0){ cmPage--; renderFeed(); } });
    if(nx) nx.addEventListener('click', function(){ if(cmPage<pages-1){ cmPage++; renderFeed(); } });
  }
  document.getElementById('cmWrite').addEventListener('click', function(){ document.getElementById('cwTitle').value=''; document.getElementById('cwBody').value=''; show('cwrite'); });
  document.getElementById('cwOk').addEventListener('click', function(){
    var t=document.getElementById('cwTitle').value.trim(), b=document.getElementById('cwBody').value.trim();
    if(!t||!b){ pop('제목과 내용을 입력해주세요.'); return; }
    cmPosts.unshift({id:'p'+Date.now(),cat:(cmCat==='all'?'pore':cmCat),author:(member&&member.nickname)||state.nickname||'익명',title:t,body:b,date:Date.now(),likes:0,comments:0});
    cmSave(cmPosts); cmCat='all'; cmPage=0; pop('글이 등록되었어요.'); go('comm');
  });
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }

  /* ---------- my page ---------- */
  var myTab='analyses';
  function renderMy(){
    var name=(member&&member.nickname)||state.nickname||'회원';
    document.getElementById('myName').textContent=name;
    document.getElementById('myAv').textContent=name.charAt(0)||'M';
    document.getElementById('myMeta').textContent=(member&&member.email?member.email:'게스트')+(member&&member.age?' · '+member.age+'세':'');
    document.getElementById('stA').textContent=records.analyses.length;
    document.getElementById('stR').textContent=records.recommends.length;
    var trend='–'; if(records.analyses.length>=2){ var d=records.analyses[0].score-records.analyses[records.analyses.length-1].score; trend=(d>=0?'+':'')+d; }
    document.getElementById('stT').textContent=trend;
    document.querySelectorAll('#myTabs .tab').forEach(function(b){ b.classList.toggle('sel', b.dataset.mt===myTab); });
    var list=records[myTab]||[];
    document.getElementById('myList').innerHTML=list.length?list.map(function(r){
      var title=myTab==='analyses'?(r.type+' · 종합 '+r.score+'점'):r.title;
      return '<div class="lrow"><div class="body"><b>'+esc(title)+'</b><small>'+fmtDate(r.date)+' · '+esc(r.summary)+'</small></div></div>';
    }).join(''):'<div class="lead" style="text-align:center;padding:30px 0;">아직 기록이 없어요.</div>';
  }
  document.querySelectorAll('#myTabs .tab').forEach(function(b){ b.addEventListener('click', function(){ myTab=b.dataset.mt; renderMy(); }); });
  document.getElementById('logoutBtn').addEventListener('click', function(){
    member=null; try{ localStorage.removeItem(MEMBER_KEY); localStorage.removeItem('forhimc_pending'); }catch(e){}
    refreshRec(); pop('로그아웃했어요.'); show('auth');
  });

  /* ---------- scan-method choice buttons (start screen + scan tab) ---------- */
  document.querySelectorAll('[data-scan]').forEach(function(b){ b.addEventListener('click', function(){ if(b.dataset.scan==='cam') openCam(); else { syncChips(); show('survey'); } }); });

  /* ---------- membership flow ---------- */
  function beginSignup(email,name){
    document.getElementById('pfEmail').value=email||'';
    document.getElementById('pfAge').value='';
    document.getElementById('pfNick').value=name||'';
    document.getElementById('pfHint').textContent='';
    // reset consent
    document.getElementById('cAll').checked=false;
    document.querySelectorAll('#consList .cchk').forEach(function(c){ c.checked=false; });
    document.getElementById('consHint').textContent='';
    show('consent');
  }
  document.getElementById('skipBtn').addEventListener('click', function(){ go('home'); });
  document.getElementById('googleBtn').addEventListener('click', function(){
    if(W.USER_LOGGED_IN==='1'){ beginSignup(W.USER_EMAIL||'', W.USER_NAME||''); return; }
    if(W.AUTH_ON==='1' && W.APP_URL){
      try{ localStorage.setItem('forhimc_pending','1'); }catch(e){}
      pop('구글 로그인 창을 여는 중…');
      var url=W.APP_URL+(W.APP_URL.indexOf('?')>=0?'&':'?')+'login=google';
      try{ var a=document.createElement('a'); a.href=url; a.target='_top'; a.rel='opener'; document.body.appendChild(a); a.click(); a.remove(); }catch(e){}
      setTimeout(function(){ try{ W.top.location.href=url; }catch(e){ try{ W.open(url,'_blank'); }catch(e2){} } },150);
      return;
    }
    // no auth configured (local/demo) → simulate a Google account
    beginSignup('minjun.kim@gmail.com','Minjun');
  });
  // consent
  document.getElementById('cAll').addEventListener('change', function(e){ document.querySelectorAll('#consList .cchk').forEach(function(c){ c.checked=e.target.checked; }); });
  document.querySelectorAll('#consList .cchk').forEach(function(c){ c.addEventListener('change', function(){ var all=[].slice.call(document.querySelectorAll('#consList .cchk')); document.getElementById('cAll').checked=all.every(function(x){return x.checked;}); }); });
  function consentGo(){
    var chks=[].slice.call(document.querySelectorAll('#consList .cchk'));
    if(!chks.filter(function(c){return c.dataset.req==='1';}).every(function(c){return c.checked;})){ document.getElementById('consHint').textContent='필수 항목에 동의해주세요.'; return; }
    show('profile');
  }
  document.getElementById('consOk').addEventListener('click', consentGo);
  document.getElementById('consReq').addEventListener('click', function(){ document.querySelectorAll('#consList .cchk').forEach(function(c){ c.checked=(c.dataset.req==='1'); }); document.getElementById('cAll').checked=false; consentGo(); });
  // profile submit
  document.getElementById('pfOk').addEventListener('click', function(){
    var nick=document.getElementById('pfNick').value.trim(), age=parseInt(document.getElementById('pfAge').value,10), email=document.getElementById('pfEmail').value.trim();
    var hint=document.getElementById('pfHint');
    if(!nick){ hint.textContent='닉네임을 입력해주세요.'; return; }
    if(!age||age<1||age>120){ hint.textContent='나이를 올바르게 입력해주세요.'; return; }
    state.nickname=nick; state.age=age; state.email=email;
    member={loggedIn:true,provider:'google',nickname:nick,email:email,age:age,joinedAt:Date.now()};
    try{ localStorage.setItem(MEMBER_KEY,JSON.stringify(member)); }catch(e){}
    mergeGuest();
    document.getElementById('startTitle').innerHTML=nick+'님, <span class="thin">가입 완료 🎉</span>';
    show('start');
  });

  /* ---------- splash + routing ---------- */
  function pending(){ try{ return localStorage.getItem('forhimc_pending')==='1'; }catch(e){ return false; } }
  function clearPending(){ try{ localStorage.removeItem('forhimc_pending'); }catch(e){} }
  function routeAfterSplash(){
    document.getElementById('splash').classList.add('gone');
    if(W.USER_LOGGED_IN==='1'){
      var email=W.USER_EMAIL||'';
      if(isMember() && member.provider==='google' && (member.email||'')===email){ clearPending(); refreshRec(); go('home'); return; }
      if(pending()){ clearPending(); beginSignup(email, W.USER_NAME||''); return; }
    }
    show('auth');
  }
  // if a saved google member but the real session is gone, drop it
  if(W.AUTH_ON==='1' && W.USER_LOGGED_IN!=='1' && isMember() && member.provider==='google'){ member=null; try{ localStorage.removeItem(MEMBER_KEY); }catch(e){} refreshRec(); }
  setTimeout(routeAfterSplash, 1600);
})();
</script>
"""

HTML = HTML.replace("__LOGO__", logo_uri)
HEAD = (
    "<script>window.AUTH_ON=%s;window.USER_LOGGED_IN=%s;window.USER_EMAIL=%s;"
    "window.USER_NAME=%s;window.APP_URL=%s;window.SB_URL=%s;window.SB_KEY=%s;</script>"
) % (
    json.dumps("1" if auth_on else ""),
    json.dumps("1" if logged_in else ""),
    json.dumps(user_email),
    json.dumps(user_name),
    json.dumps(app_url),
    json.dumps(supabase_url),
    json.dumps(supabase_key),
)

components.html(HEAD + HTML, height=900, scrolling=False)
