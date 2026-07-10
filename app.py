import base64
import json
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="FOR HIM - Men's Beauty AI Demo", layout="wide")

logo_path = Path(__file__).parent / "로고.png"
logo_data_uri = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")


def _img_data_uri(name: str) -> str:
    """Encode a local PNG as a data URI; empty string if the file is missing."""
    try:
        p = Path(__file__).parent / name
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    except Exception:
        return ""


# Real analysis faces used on the detailed diagnosis page (by member gender).
# ASCII filenames so the deploy platform loads them reliably.
face_male_uri = _img_data_uri("face_male.png")
face_female_uri = _img_data_uri("face_female.png")


def _look_imgs() -> dict:
    """스타일 피드 카드별 완성 촬영 이미지(look_<카드id>.png)가 있으면 로드.

    예: look_f4.png 를 폴더에 넣으면 '면접 신뢰 룩' 카드가 SVG 착장 합성 대신
    해당 실사 이미지를 사용한다. 파일이 없으면 빈 dict → 합성 방식 폴백.
    """
    out = {}
    for p in Path(__file__).parent.glob("look_*.png"):
        uri = _img_data_uri(p.name)
        if uri:
            out[p.stem.replace("look_", "")] = uri
    return out


look_imgs = _look_imgs()


def _prod_imgs() -> dict:
    """제품 카드용 실제 상품 이미지(prod_<제품id>.png|jpg|webp)가 있으면 로드.

    예: prod_anuaTuner.png 를 폴더에 넣으면 '어성초 77 토너' 카드가 SVG
    플레이스홀더 대신 그 실물 사진을 사용한다. 공식 이미지 확보 시 파일만
    추가하면 코드 수정 없이 카드에 반영된다.
    """
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    out = {}
    for p in Path(__file__).parent.glob("prod_*.*"):
        m = mime.get(p.suffix.lower())
        if not m:
            continue
        try:
            out[p.stem.replace("prod_", "")] = f"data:{m};base64," + base64.b64encode(p.read_bytes()).decode("ascii")
        except Exception:
            pass
    return out


prod_imgs = _prod_imgs()

# ---- 올리브영 랭킹 데이터 ----
# fetch_oy_ranking.py 배치를 주기 실행(1일 1회 권장)하면 oy_ranking.json 이 갱신된다.
# 파일이 없거나 읽기 실패 시 아래 시드 스냅샷을 쓴다(공개된 올리브영 베스트/어워즈
# 정보를 참고해 수동 구성한 데이터 — 실계약/공식 데이터 확보 시 교체).
# segmented=True 가 되면(연령·성별 세분화 랭킹 확보 시) 뱃지 문구가
# "30대 男 구매 1위" 형태로 자동 고도화된다.
OY_RANKING_SEED = {
    "updatedAt": "2026-07-10",
    "source": "seed(올리브영 공개 베스트/어워즈 정보 기반 수동 구성)",
    "segmented": False,
    "entries": [
        {"matchId": "anuaTuner",     "cat": "toner",      "rank": 1, "brand": "아누아",   "name": "어성초 77 토너"},
        {"matchId": "toriden",       "cat": "serum",      "rank": 1, "brand": "토리든",   "name": "다이브인 저분자 히알루론산 세럼"},
        {"matchId": "illiyoonLotion","cat": "lotion",     "rank": 1, "brand": "일리윤",   "name": "세라마이드 아토 로션"},
        {"matchId": "estraCream",    "cat": "cream",      "rank": 1, "brand": "에스트라", "name": "아토베리어365 크림"},
        {"matchId": "estraCleanser", "cat": "cleanser",   "rank": 1, "brand": "에스트라", "name": "아토베리어365 클렌징폼"},
        {"matchId": "ahc",           "cat": "sun",        "rank": 1, "brand": "AHC",      "name": "마스터즈 에어 리치 선스틱"},
        {"matchId": "clioCushion",   "cat": "cushion",    "rank": 1, "brand": "클리오",   "name": "킬커버 파운웨어 쿠션"},
        {"matchId": "clioBrow",      "cat": "brow",       "rank": 1, "brand": "클리오",   "name": "킬브로우 오토 하드 브로우 펜슬"},
        {"matchId": "clioEye",       "cat": "eye",        "rank": 1, "brand": "클리오",   "name": "프로 아이 팔레트 에어"},
        {"matchId": "foretPerfume",  "cat": "perfume",    "rank": 1, "brand": "포레",     "name": "우디 머스크 오 드 퍼퓸"},
        {"matchId": "ceraveBody",    "cat": "bodylotion", "rank": 1, "brand": "세라비",   "name": "모이스처라이징 바디 크림"},
        {"matchId": "scholFoot",     "cat": "foot",       "rank": 1, "brand": "닥터숄",   "name": "벨벳 스무스 풋 크림"},
        {"matchId": "niveaDeo",      "cat": "deo",        "rank": 1, "brand": "니베아",   "name": "프레시 액티브 데오 롤온"},
        {"matchId": "medicubeAger",  "cat": "device",     "rank": 1, "brand": "메디큐브", "name": "AGE-R 부스터 프로"},
    ],
}


def _load_oy_ranking() -> dict:
    """배치가 만든 oy_ranking.json을 우선 사용, 없으면 시드 폴백."""
    try:
        p = Path(__file__).parent / "oy_ranking.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("entries"):
                return data
    except Exception:
        pass
    return OY_RANKING_SEED


oy_ranking = _load_oy_ranking()
# 데이터 갱신 시점 확인용 로그(서버 콘솔) — 관리자용 표시는 사이드바 캡션 참조
print(f"[oy_ranking] updatedAt={oy_ranking.get('updatedAt')} source={oy_ranking.get('source')} entries={len(oy_ranking.get('entries', []))}")

DEMO_HTML = """
<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FOR HIM — Men's Beauty AI Demo</title>
<script>window.SB_URL="__SUPABASE_URL__";window.SB_KEY="__SUPABASE_KEY__";window.AUTH_ON=__AUTH_ON__;window.USER_LOGGED_IN=__USER_LOGGED_IN__;window.USER_EMAIL=__USER_EMAIL__;window.USER_NAME=__USER_NAME__;window.APP_URL=__APP_URL__;window.FACE_MALE="__FACE_MALE__";window.FACE_FEMALE="__FACE_FEMALE__";window.OY_RANKING=__OY_RANKING__;window.LOOK_IMGS=__LOOK_IMGS__;window.PROD_IMGS=__PROD_IMGS__;</script>
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
  html{-webkit-text-size-adjust:100%;text-size-adjust:100%;}
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
  /* 화면 너비와 상관없이 한 줄 유지(줄바꿈 방지). 좁으면 폰트 축소 후 가로 스크롤로 대응. */
  .single-line-text{
    white-space:nowrap;max-width:100%;overflow-x:auto;
    font-size:clamp(12px,1.5vw,16px);
    -webkit-overflow-scrolling:touch;scrollbar-width:none;
  }
  .single-line-text::-webkit-scrollbar{display:none;}
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
  .nav-links a.active{color:var(--ink);text-decoration:underline;text-underline-offset:7px;text-decoration-color:var(--gold);text-decoration-thickness:2px;}
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

  /* ---------- REWARD MISSIONS ---------- */
  .reward-card{background:var(--dark-soft);border:1px solid #3a3934;border-radius:var(--radius-lg);padding:20px 22px;margin-top:28px;}
  .reward-head{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:14px;}
  .reward-title{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:800;color:#f6f5f2;}
  .reward-title .rw-ic{width:18px;height:18px;color:var(--gold);}
  .reward-balance{font-size:13px;color:#c9c8c1;font-weight:700;}
  .reward-balance b{color:var(--gold);font-size:17px;margin:0 2px;}
  .reward-missions{display:flex;gap:12px;flex-wrap:wrap;}
  .reward-mission{position:relative;flex:1 1 220px;min-width:200px;}
  .rw-btn{
    display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;
    padding:14px 16px;border-radius:14px;border:1.5px solid #3a3934;background:#201f1c;color:#f6f5f2;
    font-family:inherit;font-size:14px;font-weight:700;cursor:pointer;text-align:left;
    transition:border-color .15s ease,transform .12s ease;
  }
  .rw-btn:hover{border-color:var(--gold);}
  .rw-btn:active{transform:scale(.99);}
  .rw-btn .rw-p{flex:none;color:var(--gold);font-weight:800;font-size:13.5px;}
  .rw-btn.done{background:#26251f;border-color:#33322d;color:#8f8e86;cursor:default;}
  .rw-btn.done .rw-p{color:#8f8e86;}
  .rw-tip{
    position:absolute;left:50%;bottom:calc(100% + 9px);transform:translateX(-50%);white-space:nowrap;
    background:#1a1a18;color:#f6f5f2;font-size:11.5px;font-weight:600;padding:7px 11px;border-radius:9px;
    opacity:0;pointer-events:none;transition:opacity .15s ease;box-shadow:0 8px 20px rgba(0,0,0,.4);z-index:8;
  }
  .rw-tip::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:5px solid transparent;border-top-color:#1a1a18;}
  .reward-mission:hover .rw-tip{opacity:1;}

  /* 리워드 미션(좌) + 사용처 패널(우) */
  .reward-body{display:grid;grid-template-columns:1.5fr 1fr;gap:22px;align-items:start;}
  .reward-col{min-width:0;}
  .reward-use{border-left:1px solid #3a3934;padding-left:22px;}
  .reward-use-head{font-size:13px;font-weight:800;color:#f6f5f2;margin-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
  .reward-use-head span{font-size:11px;font-weight:700;color:var(--gold);background:var(--gold-soft);padding:3px 9px;border-radius:999px;}
  .use-card{
    display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;border:1.5px solid #3a3934;
    background:#201f1c;margin-bottom:10px;transition:border-color .15s ease,transform .12s ease;position:relative;
  }
  .use-card:last-child{margin-bottom:0;}
  .use-card:hover{border-color:var(--gold);transform:translateY(-1px);}
  .use-ic{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex:none;}
  .use-txt{flex:1;min-width:0;}
  .use-txt b{display:block;font-size:14px;font-weight:700;color:#f6f5f2;}
  .use-txt span{display:block;font-size:11px;color:#a9a89f;margin-top:2px;}
  .use-go{font-size:11px;font-weight:700;color:#8f8e86;flex:none;transition:color .15s ease;}
  .use-card:hover .use-go{color:var(--gold);}
  @media (max-width:860px){
    .reward-missions{flex-direction:column;} .reward-mission{flex:1 1 auto;}
    .reward-body{grid-template-columns:1fr;}
    .reward-use{border-left:none;padding-left:0;border-top:1px solid #3a3934;padding-top:18px;}
  }

  /* ---------- REWARDS PAGE (독립 탭) ---------- */
  .rewards-page{
    background:radial-gradient(120% 140% at 15% 0%, #232320 0%, var(--dark) 55%, var(--dark) 100%);
    color:#f6f5f2;
  }
  .rewards-page .reward-card{margin-top:30px;}

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

  /* ---------- APP STEPS ---------- */
  section.app-step{display:none;padding:0;}
  section.app-step.active{display:block;animation:fade .4s ease;}
  .app-step .wrap{padding-top:28px;padding-bottom:24px;}
  .step-nav{
    display:flex;justify-content:space-between;align-items:center;gap:12px;
    margin-top:26px;padding-top:18px;border-top:1px solid var(--line);
  }
  .step-nav.on-dark{border-top-color:#3a3934;}
  .step-progress{display:flex;gap:6px;}
  .step-dot{width:6px;height:6px;border-radius:50%;background:var(--line);transition:all .2s ease;}
  .step-dot.active{background:var(--accent);width:18px;border-radius:999px;}
  .step-nav.on-dark .step-dot{background:#4a4940;}
  .step-nav.on-dark .step-dot.active{background:var(--gold);}
  .step-nav-btn{visibility:visible;}
  .step-nav-btn[disabled]{visibility:hidden;}

  /* ---------- RECOMMEND ---------- */
  .recommend{background:var(--surface);}
  .tier-tabs{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px;}
  .tier-tab{
    padding:9px 16px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);
    color:var(--ink-soft);font-size:13px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;
  }
  .tier-tab.active{background:var(--dark);border-color:var(--dark);color:#fff;}
  .tier-desc{margin-top:14px;padding:13px 18px;background:var(--accent-soft);border-radius:var(--radius);font-size:13px;color:#3c4636;line-height:1.5;}
  .tier-cat-label{margin-top:16px;font-size:12px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;}

  .prod-row{display:flex;gap:16px;margin-top:12px;overflow-x:auto;padding-bottom:6px;}
  .prod-card{
    flex:0 0 240px;background:var(--bg);border:2px solid var(--line);border-radius:var(--radius-lg);
    padding:20px;text-align:center;position:relative;display:block;text-decoration:none;color:inherit;
    transition:transform .15s ease,box-shadow .15s ease;cursor:pointer;
  }
  .prod-card:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(20,20,18,.08);}
  .prod-card.reco{border-color:var(--gold);background:linear-gradient(180deg,#fdf8ee,var(--bg));}
  .prod-cart-btn{
    margin-top:14px;padding:9px 0;border-radius:999px;background:var(--dark);color:#fff;
    font-size:11.5px;font-weight:700;
  }
  .prod-card.reco .prod-cart-btn{background:var(--gold);color:#1a1a18;}
  /* 배지: 왼쪽 상단 랭킹(올리브영 랭킹 데이터 기반) · 오른쪽 상단 '추천'(내 피부 매칭)
     문구가 길어져도 한 줄 유지(nowrap) + 폰트 90% 축소, 위치·색·형태는 기존 그대로 */
  .prod-rank{
    position:absolute;top:12px;left:12px;font-size:9.5px;font-weight:800;padding:3px 9px;border-radius:999px;
    background:var(--dark);color:#fff;z-index:1;white-space:nowrap;
    max-width:calc(100% - 72px);overflow:hidden;text-overflow:ellipsis;
  }
  .prod-reco{
    position:absolute;top:12px;right:12px;font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;
    background:var(--gold);color:#1a1a18;z-index:1;
  }
  .prod-icon{width:58px;height:72px;border-radius:11px 11px 5px 5px;margin:14px auto 12px;position:relative;}
  .prod-icon::before{content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:24px;height:10px;border-radius:3px;background:rgba(0,0,0,.28);}
  .prod-photo{
    width:100%;height:150px;border-radius:12px;margin:0 auto 12px;background:#fff;
    display:flex;align-items:center;justify-content:center;overflow:hidden;
  }
  .prod-photo img{width:100%;height:100%;object-fit:contain;padding:8px;}
  /* 이미지 없는 제품: 카테고리 형태 일러스트로 동일한 카드 비율 유지 */
  .prod-photo-ph{background:linear-gradient(165deg,#fbf9f5,#f0ebe2);}
  .prod-photo-ph svg{width:72px;height:120px;}
  .prod-brand{font-size:11.5px;font-weight:700;color:var(--ink-soft);}
  .prod-name{font-size:13.5px;font-weight:700;color:var(--ink);margin-top:4px;line-height:1.35;min-height:36px;}
  .prod-tag{display:inline-block;margin-top:8px;font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent);}
  .prod-tags{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;margin-top:8px;}
  .prod-tags .prod-tag{margin-top:0;}
  .prod-match{font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;background:#eef1e7;color:#54634a;}
  .prod-card.reco .prod-match{background:#f6ecd6;color:#9a7b3f;}
  /* 단계 안의 라인별(토너/앰플/로션/크림 등) 구분 */
  .tier-lines{margin-top:6px;}
  .tier-line{margin-top:22px;}
  .tier-line:first-child{margin-top:14px;}
  .tier-line-label{
    display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;color:var(--ink);
    margin-bottom:10px;
  }
  .tier-line-label::before{content:'';width:4px;height:14px;border-radius:2px;background:var(--accent);flex:none;}
  .tier-line-sub{font-size:11px;font-weight:700;color:var(--ink-soft);}

  /* ---------- EXTRA CONCERNS ---------- */
  .extra-tabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;margin-top:20px;}
  .extra-tab{
    flex:0 0 auto;padding:9px 15px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);
    color:var(--ink-soft);font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;white-space:nowrap;transition:all .15s ease;
  }
  .extra-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;}

  /* ---------- STYLE GUIDE (TPO) ---------- */
  .tpo-tabs{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px;}
  .tpo-tab{
    display:flex;align-items:center;gap:7px;padding:10px 16px;border-radius:999px;border:1.5px solid var(--line);
    background:var(--bg);color:var(--ink-soft);font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;
  }
  .tpo-tab .tpo-emoji{font-size:15px;}
  .tpo-tab.active{background:var(--dark);border-color:var(--dark);color:#fff;}

  .tpo-combo{
    margin-top:18px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);
    box-shadow:var(--shadow);overflow:hidden;
  }
  .tpo-combo-head{
    background:linear-gradient(135deg,#232320,var(--dark));color:#f6f5f2;padding:20px 22px;
    display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
  }
  .tpo-combo-head .tc-badge{font-size:11.5px;font-weight:800;letter-spacing:.12em;color:var(--gold);text-transform:uppercase;}
  .tpo-combo-head .tc-title{font-size:19px;font-weight:800;letter-spacing:-.02em;margin-top:4px;}
  .tpo-impression{display:flex;gap:6px;flex-wrap:wrap;}
  .tpo-impression span{font-size:11.5px;font-weight:700;padding:5px 11px;border-radius:999px;background:var(--gold-soft);color:var(--gold);}

  /* ---------- WEATHER WIDGET (검정 카드 헤더) ---------- */
  .wx-meta{font-size:13px;color:#c9c8c1;margin-top:6px;}
  .wx-copy{font-size:13px;color:var(--gold);margin-top:9px;font-weight:600;}
  .wx-refresh{
    flex:none;display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;
    border:1.5px solid #3a3934;background:#201f1c;color:#c9c8c1;font-size:12px;font-weight:700;
    font-family:inherit;cursor:pointer;transition:border-color .15s ease,color .15s ease;
  }
  .wx-refresh:hover{border-color:var(--gold);color:var(--gold);}
  .wx-refresh[disabled]{opacity:.5;cursor:wait;}
  .wx-reco{flex-basis:100%;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px;}
  .wx-reco-item{background:rgba(255,255,255,.05);border:1px solid #3a3934;border-radius:10px;padding:9px 11px;}
  .wx-reco-item b{display:block;font-size:10.5px;font-weight:800;color:var(--gold);letter-spacing:.06em;margin-bottom:3px;}
  .wx-reco-item span{font-size:12px;color:#e6e4de;line-height:1.45;}
  .wx-note{flex-basis:100%;font-size:11.5px;color:#c98a3c;margin-top:6px;}
  .wx-loading .tc-title,.wx-loading .wx-meta{animation:wxpulse 1.2s ease-in-out infinite;}
  @keyframes wxpulse{0%,100%{opacity:1;}50%{opacity:.45;}}
  @media (max-width:700px){ .wx-reco{grid-template-columns:1fr 1fr;} }
  /* 상황(TPO) 타이틀은 헤더 대신 본문 첫 줄로 이동 */
  .tpo-situ{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;background:var(--bg);}
  .tpo-situ .tpo-situ-title{font-size:15px;font-weight:800;color:var(--ink);}
  .tpo-situ .tpo-impression span{background:var(--accent-soft);color:var(--accent);}
  .tpo-combo-body{display:grid;grid-template-columns:repeat(2,1fr);gap:0;}
  .tpo-slot{padding:18px 22px;border-top:1px solid var(--line);border-right:1px solid var(--line);}
  .tpo-slot:nth-child(2n){border-right:none;}
  .tpo-slot-label{display:flex;align-items:center;gap:7px;font-size:11.5px;font-weight:800;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;margin-bottom:9px;}
  .tpo-slot-label svg{width:15px;height:15px;color:var(--accent);}
  .tpo-slot-main{font-size:15px;font-weight:700;color:var(--ink);line-height:1.4;}
  .tpo-slot-sub{font-size:12.5px;color:var(--ink-soft);line-height:1.55;margin-top:5px;}
  .tpo-slot-list{margin:6px 0 0;padding:0;list-style:none;}
  .tpo-slot-list li{position:relative;padding-left:15px;font-size:13px;color:#4a4944;line-height:1.6;margin-top:4px;}
  .tpo-slot-list li::before{content:'';position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:var(--accent);}
  .tpo-slot.full{grid-column:1/-1;border-right:none;}
  @media (max-width:560px){ .tpo-combo-body{grid-template-columns:1fr;} .tpo-slot{border-right:none;} }

  /* ---------- STYLE FEED ---------- */
  .style-feed-head{margin-top:34px;}
  .style-feed-title{font-size:17px;font-weight:800;letter-spacing:-.02em;color:var(--ink);}
  .style-feed-sub{font-size:13px;color:var(--ink-soft);margin-top:3px;}
  .style-feed{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px;}
  .feed-card{
    position:relative;border-radius:var(--radius);overflow:hidden;border:1px solid var(--line);background:var(--bg);
    cursor:pointer;transition:transform .15s ease,box-shadow .15s ease;
  }
  .feed-card:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(20,20,18,.10);}
  .feed-photo{position:relative;width:100%;aspect-ratio:4/5;overflow:hidden;background:#e7e4dd;}
  .feed-photo img{width:100%;height:100%;object-fit:cover;display:block;}
  /* 컨셉 착장 합성: 카드별 옷 종류·색으로 룩 분위기를 구분 (실사 에셋이 있으면 미사용)
     blend 레이어는 사진과 곱해져(multiply) 원본 옷의 주름·음영이 원단 위로 비친다 */
  .feed-outfit{position:absolute;left:0;bottom:0;width:100%;height:46%;z-index:1;pointer-events:none;}
  .feed-outfit.blend{mix-blend-mode:multiply;}
  .feed-outfit.top{filter:drop-shadow(0 .5px 1.5px rgba(0,0,0,.18));}
  .feed-style-line{
    font-size:10.5px;color:var(--ink-soft);margin-top:7px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  }
  .feed-situation{
    position:absolute;top:10px;left:10px;font-size:11px;font-weight:800;padding:5px 11px;border-radius:999px;
    background:rgba(26,26,24,.78);color:#fff;backdrop-filter:blur(4px);z-index:2;
  }
  .feed-tag{
    position:absolute;transform:translate(-50%,-50%);z-index:2;width:20px;height:20px;border-radius:50%;
    background:#fff;border:2px solid var(--dark);color:var(--dark);font-size:11px;font-weight:800;
    display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.35);
  }
  .feed-tag::after{content:'';position:absolute;inset:-6px;border-radius:50%;border:1.5px solid rgba(255,255,255,.6);animation:tagpulse 2s ease-in-out infinite;}
  @keyframes tagpulse{0%,100%{transform:scale(1);opacity:.7;}50%{transform:scale(1.25);opacity:0;}}
  .feed-foot{padding:11px 12px;}
  .feed-look-title{font-size:13px;font-weight:700;color:var(--ink);line-height:1.35;}
  .feed-keys{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px;}
  .feed-keys span{font-size:10px;font-weight:700;color:var(--ink-soft);background:var(--surface);border:1px solid var(--line);padding:2px 7px;border-radius:999px;}
  @media (max-width:760px){ .style-feed{grid-template-columns:1fr 1fr;} }
  @media (max-width:440px){ .style-feed{grid-template-columns:1fr 1fr;gap:10px;} }

  /* ---------- STYLE DETAIL MODAL ----------
     iframe(높이=문서 전체) 환경에서도 스크롤 이동 없이 클릭한 위치에 바로 뜨도록,
     하단 고정 시트 대신 클릭 좌표 기준으로 배치되는 모달을 쓴다. */
  .sheet{position:fixed;inset:0;z-index:220;}
  .sheet[hidden]{display:none;}
  .sheet-backdrop{position:absolute;inset:0;background:rgba(20,20,18,.55);animation:fade .25s ease;}
  .sheet-card{
    position:absolute;left:50%;transform:translateX(-50%);width:min(560px, calc(100% - 32px));
    max-height:640px;overflow-y:auto;background:var(--surface);
    border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.32);animation:sheetPop .28s cubic-bezier(.2,.8,.2,1);
  }
  @keyframes sheetPop{from{opacity:0;transform:translateX(-50%) translateY(14px);}to{opacity:1;transform:translateX(-50%) translateY(0);}}
  .sheet-actions{display:flex;gap:10px;margin-top:20px;}
  .sheet-actions .btn{flex:1;}
  .sheet-grip{width:40px;height:4px;border-radius:999px;background:var(--line);margin:10px auto 0;}
  .sheet-photo{position:relative;width:100%;aspect-ratio:16/10;overflow:hidden;}
  .sheet-photo img{width:100%;height:100%;object-fit:cover;object-position:center 28%;}
  .sheet-close{position:absolute;top:12px;right:12px;width:34px;height:34px;border-radius:50%;border:none;cursor:pointer;background:rgba(26,26,24,.7);color:#fff;font-size:20px;line-height:1;z-index:3;}
  .sheet-body{padding:20px 22px 26px;}
  .sheet-situation{font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);}
  .sheet-title{font-size:20px;font-weight:800;letter-spacing:-.02em;color:var(--ink);margin-top:4px;}
  .sheet-keys{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;}
  .sheet-keys span{font-size:11.5px;font-weight:700;padding:5px 11px;border-radius:999px;background:var(--accent-soft);color:var(--accent);}
  .sheet-sec{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);}
  .sheet-sec-label{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:800;color:var(--ink);margin-bottom:9px;}
  .sheet-sec-label svg{width:16px;height:16px;color:var(--accent);}
  .sheet-skin{font-size:13.5px;color:#4a4944;line-height:1.65;}
  .sheet-prod{display:flex;align-items:center;gap:11px;padding:9px 0;border-bottom:1px solid var(--line);}
  .sheet-prod:last-child{border-bottom:none;}
  .sheet-prod-no{width:22px;height:22px;border-radius:50%;background:var(--dark);color:#fff;font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;}
  .sheet-prod-txt b{font-size:13.5px;color:var(--ink);}
  .sheet-prod-txt span{font-size:11.5px;color:var(--ink-soft);margin-left:6px;}
  .sheet-two{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
  .sheet-mini-main{font-size:14px;font-weight:700;color:var(--ink);}
  .sheet-mini-sub{font-size:12px;color:var(--ink-soft);margin-top:4px;line-height:1.5;}
  @media (max-width:440px){ .sheet-two{grid-template-columns:1fr;} }

  /* 준비 순서(이미지 번호와 동일) 단계 리스트 */
  .sheet-step{padding:10px 0;border-bottom:1px solid var(--line);}
  .sheet-step:last-of-type{border-bottom:none;}
  .sheet-step-head{display:flex;align-items:center;gap:9px;flex-wrap:wrap;}
  .sheet-step-name{font-size:13.5px;font-weight:800;color:var(--ink);}
  .sheet-step-sub{font-size:11.5px;color:var(--ink-soft);}
  .sheet-step-items{margin-top:7px;padding-left:31px;}
  .sheet-step-item{position:relative;padding-left:13px;font-size:13px;color:#4a4944;line-height:1.6;}
  .sheet-step-item::before{content:'';position:absolute;left:0;top:9px;width:4px;height:4px;border-radius:50%;background:var(--accent);}
  /* 추가 추천 열기/닫기 */
  .sheet-more-btn{
    display:flex;align-items:center;justify-content:center;gap:7px;width:100%;margin-top:12px;
    padding:11px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);
    color:var(--ink-soft);font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;
    transition:border-color .15s ease,color .15s ease;
  }
  .sheet-more-btn:hover{border-color:var(--ink);color:var(--ink);}
  .sheet-more-btn svg{width:14px;height:14px;transition:transform .2s ease;}
  .sheet-more-btn.open svg{transform:rotate(180deg);}
  .sheet-extra{display:none;margin-top:6px;}
  .sheet-extra.open{display:block;animation:fade .3s ease;}
  .sheet-extra-group{margin-top:12px;}
  .sheet-extra-label{font-size:11.5px;font-weight:800;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;}

  /* ---------- COMMUNITY ---------- */
  .avatar{width:30px;height:30px;border-radius:50%;background:var(--dark);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex:none;}
  .icon{width:13px;height:13px;}
  .cm-view[hidden]{display:none;}

  /* toolbar: search + write */
  .cm-toolbar{display:flex;gap:12px;align-items:center;margin:22px 0 14px;flex-wrap:wrap;}
  .cm-search{
    flex:1 1 240px;display:flex;align-items:center;gap:9px;padding:11px 16px;border-radius:999px;
    border:1.5px solid var(--line);background:var(--surface);transition:border-color .15s ease;
  }
  .cm-search:focus-within{border-color:var(--accent);}
  .cm-search svg{width:17px;height:17px;color:var(--ink-soft);flex:none;}
  .cm-search input{border:none;outline:none;background:none;font-family:inherit;font-size:14px;color:var(--ink);width:100%;}
  .cm-write-btn{flex:none;display:inline-flex;align-items:center;gap:7px;}
  .cm-write-btn svg{width:15px;height:15px;}

  /* category tabs */
  .cm-cats{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;margin-bottom:16px;}
  .cm-cat{
    flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;
    border:1.5px solid var(--line);background:var(--surface);color:var(--ink-soft);font-size:12.5px;font-weight:700;
    font-family:inherit;cursor:pointer;white-space:nowrap;transition:all .15s ease;
  }
  .cm-cat:hover{border-color:#c8c6bd;}
  .cm-cat.active{background:var(--dark);border-color:var(--dark);color:#fff;}
  .cm-cat .cm-cat-dot{width:7px;height:7px;border-radius:50%;flex:none;}
  .cm-cat.fav.active{background:var(--gold);border-color:var(--gold);color:#1a1a18;}

  /* post list */
  .cm-list{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  .cm-card{
    position:relative;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:16px 16px 14px;cursor:pointer;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease;
    display:flex;flex-direction:column;
  }
  .cm-card:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(20,20,18,.07);border-color:#d8d6cc;}
  .cm-card-top{display:flex;align-items:center;gap:8px;margin-bottom:9px;}
  .cm-cat-chip{font-size:10.5px;font-weight:800;color:var(--accent);background:var(--accent-soft);padding:4px 10px;border-radius:999px;}
  .cm-fav{
    margin-left:auto;background:none;border:none;padding:2px;cursor:pointer;color:var(--line);
    display:inline-flex;transition:transform .15s ease,color .15s ease;flex:none;
  }
  .cm-fav svg{width:19px;height:19px;}
  .cm-fav:hover{transform:scale(1.12);color:#d9c48f;}
  .cm-fav.on{color:var(--gold);}
  .cm-card-title{font-size:14.5px;font-weight:700;color:var(--ink);line-height:1.4;margin-bottom:6px;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
  .cm-card-body{font-size:12.5px;color:#4a4944;line-height:1.55;margin-bottom:12px;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
  .cm-card-thumb{width:100%;height:120px;border-radius:10px;object-fit:cover;margin-bottom:12px;border:1px solid var(--line);}
  .cm-card-foot{display:flex;align-items:center;gap:8px;margin-top:auto;}
  .cm-card-foot .avatar{width:24px;height:24px;font-size:10.5px;}
  .cm-author{font-size:11.5px;font-weight:700;color:var(--ink);}
  .cm-time{font-size:10px;color:var(--ink-soft);}
  .cm-card-stats{margin-left:auto;display:flex;gap:10px;font-size:11px;color:var(--ink-soft);}
  .cm-card-stats span{display:flex;align-items:center;gap:4px;}
  .cm-skintags{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;}
  .cm-skintag{font-size:9.5px;font-weight:700;color:var(--ink-soft);background:var(--bg);border:1px solid var(--line);padding:2px 8px;border-radius:999px;}
  .cm-empty{text-align:center;color:var(--ink-soft);font-size:13.5px;padding:44px 0;}

  /* 콘텐츠 유형 배지 */
  .cm-type-badge{font-size:10px;font-weight:800;padding:3px 8px;border-radius:999px;color:#fff;}
  .cm-type-badge.vote{background:#c15c8a;}
  .cm-type-badge.ba{background:#5c7a9b;}

  /* 투표(남좋메/여좋메) */
  .cm-vote{display:flex;flex-direction:column;gap:8px;margin:6px 0 12px;}
  .cm-vote-opt{
    position:relative;display:flex;align-items:center;justify-content:space-between;gap:8px;
    width:100%;padding:11px 14px;border-radius:11px;border:1.5px solid var(--line);background:var(--bg);
    font-family:inherit;font-size:13px;font-weight:700;color:var(--ink);cursor:pointer;overflow:hidden;transition:border-color .15s ease;
  }
  .cm-vote-opt:not([disabled]):hover{border-color:var(--accent);}
  .cm-vote-opt[disabled]{cursor:default;}
  .cm-vote-fill{position:absolute;left:0;top:0;bottom:0;background:var(--accent-soft);transition:width .5s cubic-bezier(.2,.8,.2,1);z-index:0;}
  .cm-vote-opt.mine .cm-vote-fill{background:#dbe6cf;}
  .cm-vote-opt.mine{border-color:var(--accent);}
  .cm-vote-label,.cm-vote-pct{position:relative;z-index:1;}
  .cm-vote-pct{color:var(--accent);font-weight:800;}
  .cm-vote-total{font-size:11.5px;color:var(--ink-soft);font-weight:600;text-align:right;}

  /* 비포·애프터 */
  .cm-ba{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:6px 0 12px;}
  .cm-ba-col{position:relative;border-radius:11px;overflow:hidden;background:#ece8e0;aspect-ratio:4/5;}
  .cm-ba.big .cm-ba-col{aspect-ratio:1/1;}
  .cm-ba-img{width:100%;height:100%;object-fit:cover;display:block;}
  .cm-ba-img.before{filter:grayscale(0.85) brightness(0.92) contrast(0.95);}
  .cm-ba-tag{position:absolute;top:8px;left:8px;z-index:2;font-size:10px;font-weight:800;letter-spacing:.05em;padding:3px 8px;border-radius:999px;background:rgba(26,26,24,.72);color:#fff;}
  .cm-ba-tag.after{background:var(--accent);}
  .cm-ba-ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:var(--ink-soft);font-size:12px;}

  /* 사용 제품 · 변화 포인트 */
  .cm-extra{margin:14px 0 0;padding-top:14px;border-top:1px solid var(--line);}
  .cm-extra-label{font-size:11.5px;font-weight:800;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;margin-bottom:9px;}
  .cm-prod-list{display:flex;flex-direction:column;gap:7px;}
  .cm-prod-item{display:flex;align-items:center;gap:9px;font-size:13.5px;font-weight:600;color:var(--ink);}
  .cm-prod-no{width:20px;height:20px;border-radius:50%;background:var(--dark);color:#fff;font-size:10.5px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;}
  .cm-change{font-size:13.5px;color:#4a4944;line-height:1.65;background:var(--accent-soft);padding:12px 14px;border-radius:11px;}

  /* 작성 폼: 콘텐츠 유형 선택 */
  .cm-type-seg{display:flex;gap:8px;flex-wrap:wrap;}
  .cm-type-btn{
    flex:1 1 auto;padding:10px 12px;border-radius:11px;border:1.5px solid var(--line);background:var(--bg);
    color:var(--ink-soft);font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;white-space:nowrap;
  }
  .cm-type-btn:hover{border-color:#c8c6bd;}
  .cm-type-btn.on{background:var(--dark);border-color:var(--dark);color:#fff;}

  /* detail view */
  .cm-back{
    display:inline-flex;align-items:center;gap:6px;padding:8px 14px 8px 10px;border-radius:999px;
    border:1.5px solid var(--line);background:var(--surface);color:var(--ink-soft);font-size:13px;font-weight:700;
    font-family:inherit;cursor:pointer;margin:20px 0 16px;transition:border-color .15s ease,color .15s ease;
  }
  .cm-back:hover{border-color:var(--ink);color:var(--ink);}
  .cm-back svg{width:16px;height:16px;}
  .cm-detail-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:26px;box-shadow:var(--shadow);}
  .cm-detail-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
  .cm-detail-actions{margin-left:auto;display:flex;gap:8px;}
  .cm-icon-btn{
    display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:999px;border:1.5px solid var(--line);
    background:var(--surface);color:var(--ink-soft);font-size:12px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;
  }
  .cm-icon-btn:hover{border-color:var(--ink);color:var(--ink);}
  .cm-icon-btn svg{width:14px;height:14px;}
  .cm-icon-btn.on{border-color:var(--gold);color:var(--gold);background:var(--gold-soft);}
  .cm-detail-title{font-size:clamp(19px,2.6vw,24px);font-weight:700;letter-spacing:-.02em;color:var(--ink);margin:14px 0 10px;line-height:1.35;}
  .cm-detail-meta{display:flex;align-items:center;gap:9px;padding-bottom:16px;border-bottom:1px solid var(--line);}
  .cm-detail-photo{width:100%;max-height:420px;object-fit:cover;border-radius:14px;margin:18px 0;border:1px solid var(--line);}
  .cm-detail-body{font-size:14.5px;color:#3a3a36;line-height:1.75;margin:18px 0 6px;white-space:pre-wrap;}
  .cm-comments{margin-top:24px;padding-top:20px;border-top:1px solid var(--line);}
  .cm-comments-title{font-size:13px;font-weight:800;color:var(--ink);margin-bottom:14px;}
  .cm-comment{display:flex;gap:10px;padding:12px 0;border-bottom:1px solid var(--line);}
  .cm-comment:last-of-type{border-bottom:none;}
  .cm-comment-main b{font-size:12.5px;color:var(--ink);}
  .cm-comment-main .cm-time{margin-left:6px;}
  .cm-comment-main p{margin:5px 0 0;font-size:13px;color:#4a4944;line-height:1.55;}
  .cm-comment-form{display:flex;gap:8px;margin-top:14px;}
  .cm-comment-form input{
    flex:1;padding:11px 15px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);
    font-family:inherit;font-size:13.5px;color:var(--ink);
  }
  .cm-comment-form input:focus{outline:none;border-color:var(--accent);}

  /* write / edit form */
  .cm-form{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:26px;box-shadow:var(--shadow);margin-top:8px;}
  .cm-form-title{font-size:18px;font-weight:700;color:var(--ink);margin-bottom:20px;letter-spacing:-.02em;}
  .cm-field{margin-bottom:18px;}
  .cm-field label{display:block;font-size:12.5px;font-weight:800;color:var(--ink);margin-bottom:9px;}
  .cm-field select,.cm-field input[type=text],.cm-field textarea{
    width:100%;padding:12px 15px;border-radius:12px;border:1.5px solid var(--line);background:var(--bg);
    font-family:inherit;font-size:14px;color:var(--ink);
  }
  .cm-field select:focus,.cm-field input:focus,.cm-field textarea:focus{outline:none;border-color:var(--accent);}
  .cm-field textarea{min-height:150px;resize:vertical;line-height:1.6;}
  .cm-photo-drop{
    display:flex;align-items:center;gap:12px;padding:16px;border-radius:12px;border:1.5px dashed var(--line);
    background:var(--bg);cursor:pointer;transition:border-color .15s ease;
  }
  .cm-photo-drop:hover{border-color:var(--accent);}
  .cm-photo-drop svg{width:22px;height:22px;color:var(--ink-soft);flex:none;}
  .cm-photo-drop span{font-size:13px;color:var(--ink-soft);}
  .cm-photo-preview{position:relative;margin-top:12px;display:none;}
  .cm-photo-preview.show{display:block;}
  .cm-photo-preview img{width:100%;max-height:260px;object-fit:cover;border-radius:12px;border:1px solid var(--line);}
  .cm-photo-remove{
    position:absolute;top:8px;right:8px;width:28px;height:28px;border-radius:50%;border:none;cursor:pointer;
    background:rgba(26,26,24,.75);color:#fff;font-size:15px;display:flex;align-items:center;justify-content:center;
  }
  .cm-form-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:8px;}
  .cm-form-hint{font-size:12px;color:var(--bad);min-height:16px;margin-bottom:8px;}

  /* auth control + modal */
  .cm-auth{display:flex;align-items:center;gap:8px;flex:none;}
  .cm-auth:empty{display:none;}
  .cm-auth-name{font-size:12.5px;font-weight:700;color:var(--ink);}
  .cm-auth-btn{
    padding:9px 15px;border-radius:999px;border:1.5px solid var(--line);background:var(--surface);
    color:var(--ink-soft);font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;
  }
  .cm-auth-btn:hover{border-color:var(--ink);color:var(--ink);}
  .cm-modal{position:fixed;inset:0;z-index:200;background:rgba(20,20,18,.55);display:flex;align-items:center;justify-content:center;padding:20px;}
  .cm-modal[hidden]{display:none;}
  .cm-modal-card{
    width:100%;max-width:360px;background:var(--surface);border-radius:var(--radius-lg);padding:28px;
    box-shadow:0 24px 60px rgba(0,0,0,.32);position:relative;
  }
  .cm-modal-close{position:absolute;top:12px;right:14px;width:32px;height:32px;border:none;background:none;font-size:24px;color:var(--ink-soft);cursor:pointer;line-height:1;}
  .cm-modal-title{font-size:20px;font-weight:700;color:var(--ink);letter-spacing:-.02em;}
  .cm-modal-sub{font-size:12.5px;color:var(--ink-soft);margin:7px 0 20px;}
  .cm-auth-toggle{width:100%;margin-top:12px;background:none;border:none;color:var(--ink-soft);font-size:12.5px;font-weight:600;font-family:inherit;cursor:pointer;}
  .cm-auth-toggle:hover{color:var(--ink);}

  @media (max-width:860px){
    .cm-list{grid-template-columns:1fr 1fr;}
  }
  @media (max-width:560px){
    .cm-list{grid-template-columns:1fr;}
    .cm-detail-card,.cm-form{padding:20px;}
  }
  .toast{
    position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(120%);
    background:var(--dark);color:#fff;padding:13px 22px;border-radius:999px;font-size:13.5px;font-weight:600;
    box-shadow:var(--shadow);transition:transform .25s ease;z-index:100;
  }
  .toast.show{transform:translateX(-50%) translateY(0);}

  footer{padding:0;text-align:center;color:var(--ink-soft);font-size:11.5px;background:none;margin-top:18px;}
  footer .fine{color:#a6a49c;}

  @media (max-width:860px){
    .hero .wrap{grid-template-columns:1fr;}
    .hero{text-align:left;}
    .result-grid{grid-template-columns:1fr;text-align:center;}
    .post-grid{grid-template-columns:1fr;}
    .analysis-card{padding:22px;}
  }
  @media (max-width:480px){
    .wrap{padding:0 18px;}
  }

  /* ---------- ONBOARDING SCREENS ---------- */
  .screen{width:100%;min-height:700px;display:flex;align-items:center;justify-content:center;}
  .screen.hidden{display:none;}

  .splash{background:#2c2d2d;opacity:1;transition:opacity .8s ease;}
  .splash.fade-out{opacity:0;pointer-events:none;}
  .splash-logo{
    width:min(380px,70vw);border-radius:14px;overflow:hidden;
    filter:blur(26px);opacity:0;
    transition:filter 1.3s ease, opacity 1.3s ease;
  }
  .splash-logo img{display:block;width:100%;height:auto;}
  .splash-logo.sharp{filter:blur(0);opacity:1;}

  .intro{
    background:radial-gradient(120% 140% at 15% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);
    opacity:0;transition:opacity .5s ease;padding:24px;
  }
  .intro.visible{opacity:1;}
  .intro-card{width:100%;max-width:620px;color:#f6f5f2;}
  .intro-card h1{font-size:20px;line-height:1.4;margin-top:14px;font-weight:700;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;}
  .intro-card h1 em{font-style:normal;color:var(--gold);}
  .intro-card .sub{white-space:nowrap;font-size:11px;line-height:1.75;max-width:none;overflow:hidden;}
  @media (min-width:700px){
    .intro-card h1{font-size:25px;}
    .intro-card .sub{font-size:13.5px;}
  }
  .field-row{margin-top:22px;}
  .field-row label{display:block;font-size:13px;font-weight:700;color:#c9c8c1;margin-bottom:8px;}
  .field-row input{
    width:100%;padding:13px 16px;border-radius:12px;border:1.5px solid #3a3934;
    background:#201f1c;color:#f6f5f2;font-size:15px;font-family:inherit;
  }
  .field-row input::placeholder{color:#6f6e67;}
  .field-row input:focus{outline:none;border-color:var(--gold);}
  .intro-card .hint{margin-top:12px;}
  .intro-card .btn{margin-top:26px;width:100%;padding:14px;font-size:15px;}
  .intro-recall{
    display:flex;align-items:center;justify-content:center;gap:6px;width:100%;margin-top:14px;
    background:none;border:none;color:#c9c8c1;font-size:12.5px;font-weight:600;font-family:inherit;
    cursor:pointer;padding:6px;
  }
  .intro-recall:hover{color:#f6f5f2;}

  .camera{
    background:radial-gradient(120% 140% at 85% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);
    opacity:0;transition:opacity .5s ease;padding:24px;
  }
  .camera.visible{opacity:1;}
  .camera-card{width:100%;max-width:420px;color:#f6f5f2;text-align:center;}
  .cam-title{font-size:clamp(22px,3.6vw,28px);margin-top:14px;font-weight:700;letter-spacing:-.02em;}
  .cam-frame-outer{position:relative;margin:30px auto 0;width:min(260px,64vw);aspect-ratio:1/1;}
  .cam-frame{
    position:absolute;inset:0;border-radius:50%;overflow:hidden;background:#000;
  }
  .cam-frame video{width:100%;height:100%;object-fit:cover;transform:scaleX(-1);border-radius:50%;}
  .cam-scanline{position:absolute;pointer-events:none;}
  .cam-scanline.dir-h{
    left:8%;right:8%;height:3px;top:15%;
    background:linear-gradient(90deg, transparent, rgba(201,168,106,.95), transparent);
    box-shadow:0 0 14px 3px rgba(201,168,106,.75);
  }
  .cam-scanline.dir-v{
    top:12%;bottom:12%;width:3px;left:15%;
    background:linear-gradient(180deg, transparent, rgba(201,168,106,.95), transparent);
    box-shadow:0 0 14px 3px rgba(201,168,106,.75);
  }
  @keyframes scan-down{ 0%,100%{ top:15%; opacity:.25; } 50%{ top:82%; opacity:1; } }
  @keyframes scan-up{ 0%,100%{ top:82%; opacity:.25; } 50%{ top:15%; opacity:1; } }
  @keyframes scan-right{ 0%,100%{ left:12%; opacity:.25; } 50%{ left:78%; opacity:1; } }
  @keyframes scan-left{ 0%,100%{ left:78%; opacity:.25; } 50%{ left:12%; opacity:1; } }
  .cam-ring{
    position:absolute;inset:-9px;width:calc(100% + 18px);height:calc(100% + 18px);
    animation:cam-ring-spin 7s linear infinite;pointer-events:none;
  }
  .cam-ring circle{fill:none;stroke:var(--gold);stroke-width:2.5;stroke-dasharray:3 7;opacity:.8;}
  @keyframes cam-ring-spin{ to{ transform:rotate(360deg); } }
  .cam-arrow{
    position:absolute;font-size:24px;color:var(--gold);text-shadow:0 2px 8px rgba(0,0,0,.6);
    transition:top .4s ease,left .4s ease,right .4s ease,bottom .4s ease,transform .4s ease,opacity .3s ease;
    pointer-events:none;
  }
  .cam-arrow.dir-center{top:50%;left:50%;right:auto;bottom:auto;transform:translate(-50%,-50%);font-size:20px;opacity:.9;}
  .cam-arrow.dir-right{top:50%;left:auto;right:-16px;bottom:auto;transform:translateY(-50%);}
  .cam-arrow.dir-left{top:50%;right:auto;left:-16px;bottom:auto;transform:translateY(-50%);}
  .cam-arrow.dir-up{left:50%;top:-16px;right:auto;bottom:auto;transform:translateX(-50%);}
  .cam-arrow.dir-down{left:50%;bottom:-16px;top:auto;right:auto;transform:translateX(-50%);}
  .cam-progress{margin-top:26px;height:6px;border-radius:999px;background:#3a3934;overflow:hidden;}
  .cam-progress-fill{height:100%;width:0%;background:var(--gold);border-radius:999px;}
  .cam-steps{margin-top:14px;font-size:14px;color:#c9c8c1;font-weight:600;min-height:20px;}
  .cam-fallback{margin-top:18px;font-size:13px;color:#9c9b92;}
  .cam-fallback .btn{margin-top:10px;}

  @media (max-width:520px){
    .cam-frame-outer{width:min(220px,60vw);}
  }

  /* ---------- ANALYSIS LOADING (bridge) ---------- */
  .loadscreen{
    background:radial-gradient(120% 140% at 50% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);
    opacity:0;transition:opacity .5s ease;padding:24px;
  }
  .loadscreen.visible{opacity:1;}
  .load-card{width:100%;max-width:420px;color:#f6f5f2;text-align:center;}
  .load-orb{position:relative;width:128px;height:128px;margin:8px auto 30px;}
  .load-orb .orb-core{
    position:absolute;inset:36px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%, #efdcad, var(--gold) 58%, #8a6a3a);
    box-shadow:0 0 28px 6px rgba(201,168,106,.42);animation:orb-pulse 1.8s ease-in-out infinite;
  }
  .load-orb svg{position:absolute;inset:0;width:100%;height:100%;animation:cam-ring-spin 3.6s linear infinite;}
  .load-orb svg circle{fill:none;stroke:var(--gold);stroke-width:2;stroke-dasharray:4 8;opacity:.7;}
  .load-orb svg.ring2{animation-duration:5.6s;animation-direction:reverse;}
  .load-orb svg.ring2 circle{stroke:#7d7a70;stroke-dasharray:2 10;opacity:.5;}
  @keyframes orb-pulse{0%,100%{transform:scale(.92);opacity:.85;}50%{transform:scale(1.06);opacity:1;}}
  .load-title{font-size:clamp(19px,3.4vw,23px);font-weight:700;letter-spacing:-.02em;min-height:31px;transition:opacity .35s ease;}
  .load-sub{font-size:13px;color:#a9a89f;margin-top:10px;line-height:1.65;}
  .load-bar{margin-top:26px;height:6px;border-radius:999px;background:#33322d;overflow:hidden;}
  .load-bar-fill{height:100%;width:0%;background:linear-gradient(90deg,var(--gold),#efdcad);border-radius:999px;transition:width .55s ease;}
  .load-phase{margin-top:12px;font-size:11.5px;color:#8f8e86;letter-spacing:.03em;min-height:16px;}

  /* ---------- SKIN SURVEY ---------- */
  .survey{
    background:radial-gradient(120% 140% at 15% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);
    opacity:0;transition:opacity .5s ease;padding:24px;
  }
  .survey.visible{opacity:1;}
  .survey-card{width:100%;max-width:440px;color:#f6f5f2;}
  .sv-top{display:flex;align-items:center;gap:12px;margin-bottom:22px;}
  .sv-back{background:none;border:none;color:#c9c8c1;cursor:pointer;padding:4px;display:inline-flex;font-family:inherit;flex:none;transition:opacity .15s ease;}
  .sv-back svg{width:20px;height:20px;}
  .sv-back:hover{color:#f6f5f2;}
  .sv-back[disabled]{opacity:0;pointer-events:none;}
  .sv-progress{flex:1;height:6px;border-radius:999px;background:#33322d;overflow:hidden;}
  .sv-progress-fill{height:100%;width:0%;background:var(--gold);border-radius:999px;transition:width .35s ease;}
  .sv-count{font-size:12px;color:#a9a89f;font-weight:700;flex:none;min-width:40px;text-align:right;}
  .sv-eyebrow{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700;}
  .sv-q{font-size:clamp(20px,3.6vw,25px);font-weight:700;letter-spacing:-.02em;line-height:1.35;margin-top:10px;min-height:34px;}
  .sv-opts{margin-top:22px;display:flex;flex-direction:column;gap:10px;animation:fade .3s ease;}
  .sv-opts.grid{flex-direction:row;flex-wrap:wrap;}
  .sv-opt{
    display:flex;align-items:center;gap:12px;width:100%;text-align:left;padding:15px 18px;border-radius:14px;
    border:1.5px solid #3a3934;background:#201f1c;color:#f6f5f2;font-family:inherit;cursor:pointer;
    transition:border-color .15s ease,background .15s ease,transform .12s ease;
  }
  .sv-opt:hover{border-color:var(--gold);}
  .sv-opt:active{transform:scale(.98);}
  .sv-opt.on{border-color:var(--gold);background:#2a2820;}
  .sv-opt-txt{flex:1;}
  .sv-opt-txt b{display:block;font-size:15px;font-weight:700;}
  .sv-opt-txt span{display:block;font-size:11.5px;color:#a9a89f;margin-top:3px;}
  .sv-opt-check{width:22px;height:22px;border-radius:50%;border:1.5px solid #4a4940;flex:none;position:relative;transition:all .15s ease;}
  .sv-opt.on .sv-opt-check{background:var(--gold);border-color:var(--gold);}
  .sv-opt.on .sv-opt-check::after{content:'';position:absolute;left:7px;top:3px;width:5px;height:10px;border:solid #1a1a18;border-width:0 2px 2px 0;transform:rotate(45deg);}
  .sv-opts.grid .sv-opt{flex:1 1 calc(50% - 5px);justify-content:center;text-align:center;padding:15px 12px;}
  .sv-opts.grid .sv-opt-txt b{font-size:14.5px;}
  .sv-opts.grid .sv-opt-check{display:none;}
  .sv-next{
    width:100%;margin-top:6px;padding:14px;border-radius:14px;border:none;background:var(--gold);
    color:#1a1a18;font-size:15px;font-weight:700;font-family:inherit;cursor:pointer;transition:opacity .15s ease;
  }
  .sv-next:hover{opacity:.9;}
  .sv-next[disabled]{opacity:.4;cursor:not-allowed;}
  .sv-opts.grid .sv-next{flex:1 1 100%;}

  /* ---------- DIAGNOSIS RESULT (report dashboard) ---------- */
  .diagnosis{
    background:linear-gradient(180deg,#fbf8f4,#f3ede4);opacity:0;transition:opacity .5s ease;padding:18px 24px;
    --db-brown:#8a6a52; --db-brown-soft:#efe4d8; --db-line:#e6dccd;
  }
  .diagnosis.visible{opacity:1;}
  .diag-card{width:100%;max-width:1180px;}
  .diag-back{
    display:inline-flex;align-items:center;gap:6px;padding:8px 14px 8px 10px;border-radius:999px;
    border:1.5px solid var(--db-line);background:#fff;color:#8a8072;font-size:13px;font-weight:700;
    font-family:inherit;cursor:pointer;margin-bottom:10px;transition:border-color .15s ease,color .15s ease;
  }
  .diag-back:hover{border-color:var(--db-brown);color:var(--db-brown);}
  .diag-back svg{width:16px;height:16px;}
  .diag-title{font-size:clamp(18px,3vw,22px);margin-top:2px;font-weight:700;letter-spacing:-.02em;color:#2b241d;}
  .diag-face-title,.diag-summary-title{font-size:12px;font-weight:700;letter-spacing:.06em;color:#a89a86;text-transform:uppercase;margin-bottom:10px;}

  .diag-report{
    display:grid;grid-template-columns:1fr 1.25fr 1fr;grid-template-areas:"info face score";gap:16px;
    align-items:stretch;
  }
  .diag-info-panel,.diag-face-panel,.diag-scorelist{
    background:#fffdfa;border:1px solid var(--db-line);border-radius:20px;padding:18px;
    box-shadow:0 10px 28px rgba(120,96,68,.06);
  }
  .diag-info-panel{grid-area:info;}
  /* 얼굴 칸은 세로 중앙 정렬 → 항목별 점수 칸과 아래 라인(카드 높이)이 맞도록 stretch */
  .diag-face-panel{grid-area:face;text-align:center;display:flex;flex-direction:column;justify-content:center;}
  .diag-scorelist{grid-area:score;}

  .diag-score-hero{display:flex;align-items:baseline;gap:6px;margin-top:10px;}
  .diag-score-hero b{font-size:44px;font-weight:800;color:var(--db-brown);letter-spacing:-.02em;line-height:1;}
  .diag-score-hero span{font-size:14px;color:#a89a86;font-weight:700;}
  .diag-score-tag{
    display:inline-block;margin-top:10px;font-size:11.5px;font-weight:700;color:var(--db-brown);
    background:var(--db-brown-soft);padding:5px 12px;border-radius:999px;
  }
  .diag-sentence{
    margin-top:12px;font-size:13px;color:#5c5346;line-height:1.6;padding-top:12px;border-top:1px solid var(--db-line);
  }
  .diag-userinfo{margin-top:12px;padding-top:12px;border-top:1px solid var(--db-line);}
  .diag-userinfo div{display:flex;justify-content:space-between;padding:4px 0;font-size:13px;}
  .diag-userinfo span{color:#a89a86;}
  .diag-userinfo b{color:#2b241d;font-weight:700;}
  .diag-survey{margin-top:12px;padding-top:12px;border-top:1px solid var(--db-line);}
  .diag-survey-flag{
    display:flex;align-items:center;gap:7px;font-size:12.5px;font-weight:700;color:#3c6b4a;
    background:#e4efe4;border-radius:10px;padding:9px 12px;margin-bottom:12px;line-height:1.4;
  }
  .diag-survey-flag::before{content:'✓';font-weight:800;color:#4a8a5f;}
  .diag-survey-title{font-size:11px;font-weight:700;letter-spacing:.06em;color:#a89a86;text-transform:uppercase;margin-bottom:9px;}
  .diag-survey-tags{display:flex;flex-wrap:wrap;gap:6px;}
  .diag-survey-tags span{font-size:11.5px;font-weight:700;color:var(--db-brown);background:var(--db-brown-soft);padding:5px 11px;border-radius:999px;}
  .diag-survey-empty{font-size:12.5px;color:#5c5346;line-height:1.6;}
  #diagCta{margin-top:14px;width:100%;padding:13px;font-size:15px;background:var(--db-brown);}
  #diagCta:hover{opacity:.9;}

  /* 이미지가 카드의 중심 정보로 보이도록 크게, 패널 여백은 축소 */
  .diag-face-panel{padding:18px 16px !important;}
  .face-map{position:relative;width:100%;max-width:360px;aspect-ratio:1/1;margin:4px auto 0;}
  .face-model{
    position:absolute;inset:0;z-index:0;border-radius:22px;overflow:hidden;background:#f2e8d9;
    box-shadow:inset 0 0 0 1px #ece2d2, 0 8px 20px rgba(120,96,68,.10);
  }
  /* 얼굴 중심 확대 크롭: 상반신 비중을 줄이고 얼굴이 프레임을 채우게 (145% 줌) */
  .face-model img{position:absolute;width:145%;height:145%;left:-22.5%;top:-8%;object-fit:cover;display:block;}
  .face-model svg{position:absolute;inset:0;width:100%;height:100%;display:block;}
  /* 피부 분석 맵 오버레이: 라인 기반 영역 구분 + 고민별 반투명 하이라이트 + 부위 점 표시 */
  .face-overlay{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none;}
  .face-overlay .fz{opacity:0;transition:opacity .6s ease;}
  .face-overlay .fz.on{opacity:1;}
  .face-overlay .fz-base{opacity:.55;}
  .fz-line{fill:none;stroke-width:.7;stroke-dasharray:2 1.6;stroke-linecap:round;}
  .fz-fill{stroke-width:.8;stroke-dasharray:2.4 1.8;stroke-linejoin:round;}
  .fz-dot{stroke:none;}
  .fz-label{
    font-size:3.4px;font-weight:800;letter-spacing:.02em;
    paint-order:stroke;stroke:#fff;stroke-width:.9px;stroke-linejoin:round;
  }
  /* 여성 사진은 얼굴이 더 위쪽 → 오버레이 전체 보정(145% 줌 반영) */
  .face-map.gf .face-overlay{transform:translateY(-4.6%);}
  .face-legend{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:14px;}
  .legend-item{
    display:flex;align-items:center;gap:5px;font-size:10.5px;font-weight:700;color:#b9b6ab;
    padding:4px 9px;border-radius:999px;background:var(--bg);border:1px solid var(--line);transition:all .2s ease;
  }
  .legend-item.active{color:var(--ink);background:var(--accent-soft);border-color:transparent;}
  .legend-dot{width:8px;height:8px;border-radius:50%;flex:none;}
  .legend-dot.oil{background:#c98a3c;}
  .legend-dot.pore{background:#c86e46;}
  .legend-dot.scar{background:#965a96;}
  .legend-dot.acne{background:#c13c3c;}
  .legend-dot.redness{background:#c1666b;}

  .score-row{
    display:flex;align-items:center;justify-content:space-between;padding:8.5px 0;
    border-bottom:1px solid var(--db-line);
  }
  .score-row:last-child{border-bottom:none;}
  .score-row.overall{padding-bottom:16px;margin-bottom:6px;border-bottom:1.5px solid var(--db-line);}
  .score-row.overall .score-row-label{font-size:14px;font-weight:700;color:#2b241d;}
  .score-row.overall .score-row-value{font-size:22px;color:var(--db-brown);}
  .score-row-label{font-size:13.5px;font-weight:600;color:#4a4436;display:flex;align-items:center;gap:8px;}
  .score-row-dot{width:7px;height:7px;border-radius:50%;flex:none;}
  .score-row-dot.good{background:#6f9b7a;}
  .score-row-dot.mid{background:#c98a3c;}
  .score-row-dot.bad{background:#c1666b;}
  .score-row-right{display:flex;align-items:center;gap:6px;}
  .score-row-value{font-size:15px;font-weight:700;color:#2b241d;}
  .score-row-chev{width:14px;height:14px;color:#c3b8a5;}

  /* ---------- CONCERN TABS (vertical sidebar) ---------- */
  .diag-tabsblock{
    margin-top:14px;background:#fffdfa;border:1px solid var(--db-line);border-radius:20px;padding:18px;
    box-shadow:0 10px 28px rgba(120,96,68,.06);
  }
  .diag-tabs-layout{display:grid;grid-template-columns:190px 1fr;gap:20px;margin-top:12px;align-items:start;}
  .diag-tabs{display:flex;flex-direction:column;gap:8px;}
  .diag-tab{
    display:flex;align-items:center;gap:8px;padding:12px 16px;border-radius:14px;border:1.5px solid var(--line);
    background:var(--bg);color:var(--ink-soft);font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;
    transition:all .15s ease;text-align:left;width:100%;
  }
  .diag-tab .tab-dot{width:7px;height:7px;border-radius:50%;flex:none;}
  .diag-tab.active{background:var(--dark);border-color:var(--dark);color:#fff;}
  .diag-panel{display:none;}
  .diag-panel.active{display:block;animation:fade .4s ease;}
  .panel-head{display:flex;align-items:center;justify-content:space-between;}
  .panel-title{font-size:15.5px;font-weight:700;color:var(--ink);}
  .panel-badge{font-size:11.5px;font-weight:700;padding:4px 11px;border-radius:999px;}
  .panel-badge.good{background:var(--accent-soft);color:var(--accent);}
  .panel-badge.mid{background:#fbe9d2;color:var(--mid);}
  .panel-badge.bad{background:#f7dede;color:var(--bad);}
  .panel-score-track{height:7px;border-radius:999px;background:var(--bg);margin-top:10px;overflow:hidden;}
  .panel-score-fill{height:100%;border-radius:999px;}
  .panel-desc{margin-top:12px;font-size:13px;color:#4a4944;line-height:1.6;}
  .panel-tips{margin-top:10px;}
  .panel-tips-title{font-size:11.5px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;}
  .panel-tips ul{margin:8px 0 0;padding:0;list-style:none;}
  .panel-tips li{position:relative;padding-left:16px;font-size:13px;color:#4a4944;line-height:1.6;margin-top:6px;}
  .panel-tips li::before{content:'';position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:var(--accent);}

  @media (max-width:1023px){
    .diag-report{grid-template-columns:1fr 1fr;grid-template-areas:"face face" "info score";}
  }
  @media (max-width:760px){
    .diag-tabs-layout{grid-template-columns:1fr;}
    .diag-tabs{flex-direction:row;overflow-x:auto;}
    .diag-tab{width:auto;white-space:nowrap;}
  }
  @media (max-width:640px){
    .diag-report{grid-template-columns:1fr;grid-template-areas:"face" "info" "score";gap:16px;}
    .diag-info-panel,.diag-face-panel,.diag-scorelist{padding:20px;border-radius:18px;}
    .face-map{margin-top:6px;}
    .diag-tabsblock{padding:20px;border-radius:18px;}
  }

  /* ---------- RESULT CHOICE ---------- */
  .choice{background:var(--bg);opacity:0;transition:opacity .4s ease;padding:24px;}
  .choice.visible{opacity:1;}
  .choice-card{width:100%;max-width:400px;text-align:center;}
  .choice-badge{
    width:54px;height:54px;border-radius:50%;background:var(--accent-soft);color:var(--accent);
    display:flex;align-items:center;justify-content:center;margin:0 auto 16px;
  }
  .choice-title{font-size:21px;font-weight:700;letter-spacing:-.02em;color:var(--ink);}
  .choice-sub{margin-top:7px;color:var(--ink-soft);font-size:13.5px;}
  .choice-btn{
    display:block;width:100%;text-align:left;margin-top:14px;padding:16px 18px;border-radius:16px;
    border:1.5px solid var(--line);background:var(--surface);cursor:pointer;
    transition:transform .15s ease,border-color .15s ease;font-family:inherit;
  }
  .choice-btn:active{transform:scale(.98);}
  .choice-btn:hover{border-color:#c8c6bd;}
  .choice-btn-title{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:700;color:var(--ink);}
  .choice-btn-desc{display:block;margin-top:5px;font-size:12px;color:var(--ink-soft);margin-left:29px;}
  .choice-btn-primary{background:var(--dark);border-color:var(--dark);}
  .choice-btn-primary .choice-btn-title{color:#fff;}
  .choice-btn-primary .choice-btn-desc{color:#c9c8c1;}
  .choice-icon{width:19px;height:19px;flex:none;}

  /* ---------- SIMPLE RESULT ---------- */
  .simple{background:var(--bg);opacity:0;transition:opacity .4s ease;padding:14px;}
  .simple.visible{opacity:1;}
  .simple-card{
    width:100%;max-width:340px;background:var(--surface);border-radius:22px;overflow:hidden;
    box-shadow:var(--shadow);border:1px solid var(--line);
  }
  .simple-header{position:relative;background:linear-gradient(135deg,#e57b73,#d9564f);color:#fff;padding:16px 18px 18px;}
  .simple-date{font-size:11px;opacity:.85;font-weight:600;}
  .simple-title{font-size:15px;font-weight:700;margin-top:5px;line-height:1.4;max-width:68%;}
  .simple-header-icon{position:absolute;right:12px;top:12px;width:42px;height:42px;}
  .simple-body{padding:14px 18px 2px;}
  .simple-score-row{display:flex;justify-content:space-between;align-items:flex-start;}
  .simple-score-label{font-size:12.5px;font-weight:700;color:var(--ink);}
  .simple-cmp{display:flex;gap:12px;}
  .simple-cmp div{text-align:center;}
  .simple-cmp span{display:block;font-size:9px;color:var(--ink-soft);}
  .simple-cmp b{font-size:12.5px;color:var(--ink);}
  .simple-score-main{margin-top:4px;display:flex;align-items:baseline;gap:4px;}
  .simple-score-main b{font-size:30px;font-weight:800;color:var(--ink);letter-spacing:-.02em;}
  .simple-score-main span{font-size:11.5px;color:var(--ink-soft);}
  .simple-tier{font-size:11px;color:var(--ink-soft);margin-top:1px;}
  .simple-survey{margin-top:9px;display:flex;flex-wrap:wrap;gap:5px;}
  .simple-survey .ss-flag{width:100%;font-size:11px;font-weight:700;color:#3c6b4a;background:#e4efe4;border-radius:8px;padding:6px 10px;display:flex;align-items:center;gap:6px;}
  .simple-survey .ss-flag::before{content:'✓';font-weight:800;}
  .simple-survey .ss-tag{font-size:10px;font-weight:700;color:var(--accent);background:var(--accent-soft);padding:3px 8px;border-radius:999px;}
  .radar-holder{margin-top:2px;}
  .radar-wrap{position:relative;width:100%;max-width:250px;margin:0 auto;}
  .radar-svg{width:100%;height:auto;display:block;}
  .radar-ring{fill:none;stroke:var(--line);stroke-width:1;}
  .radar-axis{stroke:var(--line);stroke-width:1;}
  .radar-shape{fill:rgba(217,86,79,.25);stroke:#d9564f;stroke-width:1.6;}
  .radar-dot{fill:#d9564f;}
  .radar-label{position:absolute;transform:translate(-50%,-50%);text-align:center;width:60px;line-height:1.2;}
  .radar-label b{display:block;font-size:9px;font-weight:700;color:var(--ink);}
  .radar-label .radar-pct{display:block;font-size:8.5px;color:var(--ink-soft);}
  .radar-badge{display:inline-block;font-size:7.5px;font-weight:700;padding:1px 5px;border-radius:999px;margin-bottom:1px;}
  .radar-badge.good{background:var(--accent-soft);color:var(--accent);}
  .radar-badge.mid{background:#fbe9d2;color:var(--mid);}
  .radar-badge.bad{background:#f7dede;color:var(--bad);}
  .simple-actions{display:flex;gap:8px;padding:12px 18px 16px;}
  .simple-actions .btn{flex:1;padding:10px;font-size:12.5px;}
  #screenSimple{min-height:600px;}

  /* ---------- INTRO MEMBER CTA ---------- */
  .intro-member{margin-top:20px;}
  .intro-member-or{display:flex;align-items:center;gap:12px;color:#6f6e67;font-size:11.5px;margin-bottom:14px;}
  .intro-member-or::before,.intro-member-or::after{content:'';height:1px;background:#3a3934;flex:1;}
  .intro-member-btn{
    display:flex;align-items:center;gap:12px;width:100%;text-align:left;padding:15px 18px;border-radius:14px;
    border:1.5px solid #3a3934;background:#201f1c;color:#f6f5f2;font-family:inherit;cursor:pointer;transition:border-color .15s ease;
  }
  .intro-member-btn:hover{border-color:var(--gold);}
  .intro-member-txt{flex:1;}
  .intro-member-txt b{display:block;font-size:14px;font-weight:700;}
  .intro-member-txt span{display:block;font-size:11.5px;color:#a9a89f;margin-top:3px;}
  .intro-member-btn svg{width:18px;height:18px;color:var(--gold);flex:none;}

  /* ---------- AUTH (social login) ---------- */
  .auth{background:radial-gradient(120% 140% at 15% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);opacity:0;transition:opacity .5s ease;padding:24px;}
  .auth.visible{opacity:1;}
  .auth-card{width:100%;max-width:420px;color:#f6f5f2;}
  .auth-back,.consent-card .auth-back{
    display:inline-flex;align-items:center;gap:4px;background:none;border:none;color:#c9c8c1;font-size:13px;font-weight:600;
    font-family:inherit;cursor:pointer;padding:0;margin-bottom:22px;
  }
  .auth-back svg{width:16px;height:16px;}
  .auth-back:hover{color:#f6f5f2;}
  .auth-title{font-size:26px;font-weight:700;letter-spacing:-.02em;line-height:1.3;}
  .auth-title em{font-style:normal;color:var(--gold);}
  .auth-sub{font-size:13.5px;color:#c9c8c1;margin-top:10px;line-height:1.6;}
  .auth-benefits{display:flex;flex-direction:column;gap:10px;margin:24px 0;}
  .auth-benefit{display:flex;align-items:center;gap:13px;padding:13px 15px;border-radius:12px;background:#201f1c;border:1px solid #33322d;}
  .auth-benefit svg{width:22px;height:22px;color:var(--gold);flex:none;}
  .auth-benefit b{display:block;font-size:13.5px;font-weight:700;}
  .auth-benefit span{display:block;font-size:11.5px;color:#a9a89f;margin-top:2px;}
  .social-btns{display:flex;flex-direction:column;gap:10px;margin-top:8px;}
  .social-btn{
    display:flex;align-items:center;gap:12px;width:100%;padding:14px 18px;border-radius:12px;
    border:1.5px solid #3a3934;background:#26251f;color:#f6f5f2;font-family:inherit;font-size:14.5px;font-weight:700;
    cursor:pointer;transition:border-color .15s ease,transform .12s ease;
  }
  .social-btn:hover{border-color:#6f6e67;}
  .social-btn:active{transform:scale(.99);}
  .social-ic{width:26px;height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;flex:none;}
  .auth-skip{width:100%;margin-top:18px;background:none;border:none;color:#a9a89f;font-size:12.5px;font-weight:600;font-family:inherit;cursor:pointer;}
  .auth-skip:hover{color:#f6f5f2;}

  /* ---------- CONSENT ---------- */
  .consent{background:radial-gradient(120% 140% at 85% 0%, #232320 0%, var(--dark) 60%, var(--dark) 100%);opacity:0;transition:opacity .5s ease;padding:24px;}
  .consent.visible{opacity:1;}
  .consent-card{width:100%;max-width:460px;color:#f6f5f2;}
  .consent-title{font-size:22px;font-weight:700;letter-spacing:-.02em;}
  .consent-sub{font-size:13px;color:#c9c8c1;margin-top:8px;line-height:1.6;}
  .consent-all{display:flex;align-items:center;gap:11px;margin:22px 0 12px;padding:15px 16px;border-radius:12px;background:#26251f;border:1.5px solid var(--gold);cursor:pointer;font-size:15px;}
  .consent-list{display:flex;flex-direction:column;}
  .consent-item{border-top:1px solid #33322d;padding:14px 2px;}
  .consent-item label{display:flex;align-items:center;gap:11px;cursor:pointer;}
  .consent-label{flex:1;font-size:13.5px;color:#e8e7e0;}
  .consent-tag{font-style:normal;font-size:10.5px;font-weight:800;padding:2px 7px;border-radius:999px;margin-right:6px;}
  .consent-tag.req{background:var(--gold-soft);color:var(--gold);}
  .consent-tag.opt{background:#33322d;color:#a9a89f;}
  .consent-all input,.consent-item input{position:absolute;opacity:0;width:0;height:0;}
  .consent-check{width:22px;height:22px;border-radius:7px;border:1.5px solid #4a4940;flex:none;position:relative;transition:all .15s ease;}
  .consent-check::after{content:'';position:absolute;left:7px;top:3px;width:5px;height:10px;border:solid #1a1a18;border-width:0 2px 2px 0;transform:rotate(45deg) scale(0);transition:transform .15s ease;}
  .consent-all input:checked ~ .consent-check,.consent-item input:checked + .consent-check{background:var(--gold);border-color:var(--gold);}
  .consent-all input:checked ~ .consent-check::after,.consent-item input:checked + .consent-check::after{transform:rotate(45deg) scale(1);}
  .consent-more{margin-left:33px;margin-top:6px;background:none;border:none;color:#8f8e86;font-size:11.5px;font-family:inherit;cursor:pointer;text-decoration:underline;}
  .consent-detail{display:none;margin:8px 0 0 33px;font-size:12px;color:#a9a89f;line-height:1.6;padding:10px 12px;background:#201f1c;border-radius:9px;}
  .consent-detail.show{display:block;}
  .consent-hint{min-height:18px;font-size:12.5px;color:#e0a3a3;margin:14px 0 4px;}
  .consent-actions{display:flex;gap:10px;margin-top:6px;}
  .consent-actions .btn{flex:1;padding:14px;font-size:14.5px;}
  .consent-actions .btn-outline{border-color:#4a4940;color:#e8e7e0;}
  #screenProfile .field-row label{display:flex;align-items:center;gap:8px;}
  .prof-badge{font-style:normal;font-size:10px;font-weight:800;padding:2px 8px;border-radius:999px;background:var(--gold-soft);color:var(--gold);}
  #screenProfile input[readonly]{opacity:.75;cursor:default;}
  #screenProfile .btn-gold{margin-top:8px;}
  .prof-gender{display:flex;gap:8px;}
  .prof-gender-btn{
    flex:1;padding:12px 8px;border-radius:12px;border:1.5px solid #3a3934;background:#201f1c;
    color:#c9c8c1;font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;transition:all .15s ease;
  }
  .prof-gender-btn:hover{border-color:#6f6e67;}
  .prof-gender-btn.on{background:var(--gold);border-color:var(--gold);color:#1a1a18;}

  /* ---------- MY PAGE ---------- */
  .mypage{background:linear-gradient(180deg,#fbf8f4,#f3ede4);opacity:0;transition:opacity .5s ease;padding:32px 24px;}
  .mypage.visible{opacity:1;}
  .mypage-card{width:100%;max-width:720px;}
  .mp-head{display:flex;align-items:center;gap:14px;}
  .mp-user{display:flex;align-items:center;gap:12px;flex:1;}
  .mp-avatar{width:48px;height:48px;border-radius:50%;background:var(--dark);color:#fff;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:800;flex:none;}
  .mp-name{font-size:18px;font-weight:800;color:#2b241d;letter-spacing:-.02em;}
  .mp-provider{font-size:12px;color:#a89a86;font-weight:600;margin-top:2px;}
  .mp-head-actions{display:flex;align-items:center;gap:8px;}
  .mp-ghost{background:none;border:none;color:#a89a86;font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;}
  .mp-ghost:hover{color:#2b241d;}
  .mp-hello{margin:18px 0 16px;font-size:13.5px;color:#5c5346;line-height:1.6;}
  .mp-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
  .mp-stat{background:#fffdfa;border:1px solid #e6dccd;border-radius:16px;padding:18px;text-align:center;}
  .mp-stat b{display:block;font-size:26px;font-weight:800;color:var(--db-brown,#8a6a52);line-height:1;}
  .mp-stat span{display:block;font-size:11.5px;color:#a89a86;font-weight:700;margin-top:6px;}
  .mp-cta-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:18px 0 22px;}
  .mp-recall{display:inline-flex;align-items:center;gap:6px;background:none;border:none;color:#8a6a52;font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;}
  .mp-recall svg{width:14px;height:14px;}
  .mp-recall:hover{text-decoration:underline;}
  .mp-tabs{display:flex;gap:8px;border-bottom:1px solid #e6dccd;margin-bottom:16px;overflow-x:auto;}
  .mp-tab{padding:11px 4px;margin-right:12px;background:none;border:none;border-bottom:2px solid transparent;color:#a89a86;font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;white-space:nowrap;transition:all .15s ease;}
  .mp-tab.active{color:#2b241d;border-bottom-color:var(--db-brown,#8a6a52);}
  .mp-panels{display:flex;flex-direction:column;gap:12px;}
  .mp-record{background:#fffdfa;border:1px solid #e6dccd;border-radius:14px;padding:16px 18px;transition:box-shadow .15s ease;}
  .mp-record:hover{box-shadow:0 8px 20px rgba(120,96,68,.08);}
  .mp-record-top{display:flex;align-items:center;gap:10px;}
  .mp-record-date{font-size:11.5px;color:#a89a86;font-weight:700;}
  .mp-record-badge{margin-left:auto;font-size:11px;font-weight:800;color:var(--db-brown,#8a6a52);background:#efe4d8;padding:3px 10px;border-radius:999px;}
  .mp-record-title{font-size:14.5px;font-weight:700;color:#2b241d;margin-top:7px;}
  .mp-record-sum{font-size:12.5px;color:#5c5346;line-height:1.55;margin-top:5px;}
  .mp-empty{text-align:center;color:#a89a86;font-size:13px;padding:40px 0;}

  @media (max-width:560px){
    .mp-head{flex-wrap:wrap;}
    .auth-title{font-size:23px;}
  }
</style>
</head>
<body>

<div class="screen splash" id="screenSplash">
  <div class="splash-logo" id="splashLogo">
    <img src="__LOGO_SRC__" alt="MEN ARE COOL" />
  </div>
</div>

<div class="screen intro hidden" id="screenIntro">
  <div class="intro-card">
    <div class="eyebrow on-dark">MEN'S BEAUTY, SIMPLIFIED</div>
    <h1>피부 관리, <em>어렵게</em> 생각하지 마세요</h1>
    <p class="sub on-dark">복잡한 성분 이름도, 매장에서의 어색한 상담도 필요 없어요.<br/>카메라로 얼굴을 몇 초만 비춰주시면 AI가 피부 상태를 확인해드려요.</p>
    <div class="field-row">
      <label>닉네임</label>
      <input type="text" id="nickInput" placeholder="닉네임을 입력해주세요" maxlength="12" />
    </div>
    <div class="field-row">
      <label>나이</label>
      <input type="number" id="ageInput" placeholder="나이를 입력해주세요" min="1" max="120" />
    </div>
    <div class="hint" id="introHint"></div>
    <button class="btn btn-gold" id="introConfirm">확인</button>
    <button type="button" class="intro-recall" id="introRecall" style="display:none;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 2.6-6.36M3 4v5h5"/></svg>
      최근 분석 결과 다시 보기
    </button>

    <div class="intro-member">
      <div class="intro-member-or"><span>또는</span></div>
      <button type="button" class="intro-member-btn" id="introMember">
        <div class="intro-member-txt">
          <b>회원가입하고 내 피부 기록 저장하기</b>
          <span>피부 기록 저장 · 추천 이력 관리 · 변화 추적</span>
        </div>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 6l6 6-6 6"/></svg>
      </button>
    </div>
  </div>
</div>

<div class="screen camera hidden" id="screenCamera">
  <div class="camera-card">
    <div class="eyebrow on-dark">SKIN ANALYSIS AI</div>
    <h2 class="cam-title">지금부터 얼굴을 촬영할게요</h2>
    <p class="sub on-dark" id="camSub">잠시 후 안내에 따라 고개를 움직여주세요</p>
    <div class="cam-frame-outer">
      <div class="cam-frame">
        <video id="camVideo" autoplay playsinline muted></video>
        <div class="cam-scanline dir-h" id="camScanline"></div>
      </div>
      <svg class="cam-ring" viewBox="0 0 200 200"><circle cx="100" cy="100" r="97"/></svg>
      <div class="cam-arrow" id="camArrow"></div>
    </div>
    <div class="cam-progress"><div class="cam-progress-fill" id="camProgressFill"></div></div>
    <div class="cam-steps" id="camSteps"></div>
    <div class="cam-fallback" id="camFallback" style="display:none;">
      카메라를 사용할 수 없어요.<br/>
      <button class="btn btn-outline btn-sm" id="camSkip">카메라 없이 계속하기</button>
    </div>
  </div>
</div>

<div class="screen loadscreen hidden" id="screenLoading">
  <div class="load-card">
    <div class="eyebrow on-dark">SKIN ANALYSIS AI</div>
    <div class="load-orb">
      <svg viewBox="0 0 132 132"><circle cx="66" cy="66" r="63"/></svg>
      <svg class="ring2" viewBox="0 0 132 132"><circle cx="66" cy="66" r="52"/></svg>
      <div class="orb-core"></div>
    </div>
    <div class="load-title" id="loadTitle">얼굴 영상을 분석하고 있어요</div>
    <p class="load-sub">촬영된 영상에서 피부 상태를 정밀하게 읽어내고 있어요.<br/>잠시만 기다려 주세요.</p>
    <div class="load-bar"><div class="load-bar-fill" id="loadBarFill"></div></div>
    <div class="load-phase" id="loadPhase">피부 이미지 정합 중…</div>
  </div>
</div>

<div class="screen survey hidden" id="screenSurvey">
  <div class="survey-card">
    <div class="sv-top">
      <button type="button" class="sv-back" id="svBack" disabled aria-label="이전 질문">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <div class="sv-progress"><div class="sv-progress-fill" id="svProgress"></div></div>
      <div class="sv-count" id="svCount">1 / 9</div>
    </div>
    <div class="sv-eyebrow">SKIN SURVEY</div>
    <div class="sv-q" id="svQuestion">-</div>
    <div class="sv-opts" id="svOpts"></div>
  </div>
</div>

<div class="screen choice hidden" id="screenChoice">
  <div class="choice-card">
    <div class="choice-badge">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 12l5 5L20 7"/></svg>
    </div>
    <div class="choice-title">피부 진단이 완료되었어요</div>
    <p class="choice-sub">원하는 방식으로 결과를 확인해보세요</p>

    <button type="button" class="choice-btn choice-btn-primary" id="goSimple">
      <div class="choice-btn-title">
        <svg class="choice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg>
        간단한 피부 결과 확인하기
      </div>
      <span class="choice-btn-desc">핵심 결과만 빠르게 확인</span>
    </button>

    <button type="button" class="choice-btn" id="goDetailed">
      <div class="choice-btn-title">
        <svg class="choice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>
        상세한 피부 결과 확인하기
      </div>
      <span class="choice-btn-desc">항목별 분석과 자세한 설명 확인</span>
    </button>
  </div>
</div>

<div class="screen simple hidden" id="screenSimple">
  <div class="simple-card">
    <div class="simple-header">
      <div class="simple-date" id="simpleDate">-</div>
      <div class="simple-title" id="simpleNameTitle">고객님의 피부 분석 리포트</div>
      <svg class="simple-header-icon" viewBox="0 0 48 48" fill="none">
        <rect x="10" y="6" width="28" height="36" rx="3" fill="#fff" opacity=".92"/>
        <path d="M16 16h16M16 24h16M16 32h10" stroke="#d9564f" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="14" cy="16" r="2" fill="#d9564f"/>
        <circle cx="14" cy="24" r="2" fill="#d9564f"/>
        <circle cx="14" cy="32" r="2" fill="#d9564f"/>
      </svg>
    </div>

    <div class="simple-body">
      <div class="simple-score-row">
        <div class="simple-score-label">피부 점수</div>
        <div class="simple-cmp">
          <div><span>전체</span><b id="cmpAll">-</b></div>
          <div><span id="cmpAgeLabel">동일 연령대</span><b id="cmpAge">-</b></div>
        </div>
      </div>
      <div class="simple-score-main"><b id="simpleScore">-</b><span>점 / 100</span></div>
      <div class="simple-tier" id="simpleTier">-</div>
      <div class="simple-survey" id="simpleSurveyNote"></div>

      <div class="radar-holder" id="radarHolder"></div>
    </div>

    <div class="simple-actions">
      <button type="button" class="btn btn-outline btn-sm" id="simpleBack">뒤로가기</button>
      <button type="button" class="btn btn-dark" id="simpleToRecommend">제품 추천</button>
    </div>
  </div>
</div>

<div class="screen diagnosis hidden" id="screenDiagnosis">
  <div class="diag-card">
    <button type="button" class="diag-back" id="diagBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg>
      결과 선택으로
    </button>

    <div class="diag-report">
      <div class="diag-info-panel">
        <div class="eyebrow" style="color:#8a6a52;">SKIN ANALYSIS REPORT</div>
        <h2 class="diag-title">피부 진단 결과예요</h2>
        <div class="diag-score-hero"><b id="diagScoreBig">-</b><span>/ 100</span></div>
        <div class="diag-score-tag" id="diagPriorityTag">우선 관리 · -</div>
        <p class="diag-sentence" id="diagSentence"></p>
        <div class="diag-userinfo">
          <div><span>닉네임</span><b id="diagUserNick">-</b></div>
          <div><span>피부 나이</span><b id="diagAge">-</b></div>
          <div><span>피부 타입</span><b id="diagType">-</b></div>
          <div><span>분석 일시</span><b id="diagDate">-</b></div>
        </div>
        <div class="diag-survey" id="diagSurveyNote"></div>
        <button class="btn btn-gold" id="diagCta">나에게 맞는 제품 찾기</button>
      </div>

      <div class="diag-face-panel">
        <div class="diag-face-title">관리가 필요한 부위</div>
        <div class="face-map">
          <div class="face-model" id="faceModel"></div>
          <svg class="face-overlay" id="faceOverlay" viewBox="0 0 100 100" aria-hidden="true">
            <!-- 좌표는 145% 줌 크롭 기준 얼굴 특징점(눈 35 · 코끝 50 · 입 58 · 턱 66)에 맞춤.
                 viewBox 0-100 = %기반이라 카드 크기가 바뀌어도 비율 그대로 따라간다 -->
            <!-- 기본 영역 구분 라인(항상 표시): T존 / U존 -->
            <g class="fz-base">
              <path class="fz-line" stroke="#b9ad99" d="M34 14 Q50 11.5 66 14 Q67 19.5 66 25 Q57 23.5 55.5 26 L55.5 46 Q55.5 50.5 50 50.5 Q44.5 50.5 44.5 46 L44.5 26 Q43 23.5 34 25 Q33 19.5 34 14 Z"/>
              <path class="fz-line" stroke="#b9ad99" d="M28 44 Q28.5 62 50 67.5 Q71.5 62 72 44"/>
              <text class="fz-label" fill="#a89a86" x="68" y="16">T존</text>
              <text class="fz-label" fill="#a89a86" x="74" y="42">U존</text>
            </g>
            <!-- 유분 → 이마·코 T존 -->
            <g class="fz" data-zone="oil">
              <path class="fz-fill" fill="rgba(201,138,60,.16)" stroke="#c98a3c" d="M34 14 Q50 11.5 66 14 Q67 19.5 66 25 Q57 23.5 55.5 26 L55.5 46 Q55.5 50.5 50 50.5 Q44.5 50.5 44.5 46 L44.5 26 Q43 23.5 34 25 Q33 19.5 34 14 Z"/>
              <circle class="fz-dot" fill="#c98a3c" cx="45" cy="18.5" r=".9"/><circle class="fz-dot" fill="#c98a3c" cx="55" cy="18" r=".9"/><circle class="fz-dot" fill="#c98a3c" cx="50" cy="42" r=".9"/>
              <text class="fz-label" fill="#c98a3c" x="13" y="15">유분 · T존</text>
            </g>
            <!-- 모공 → 양볼 -->
            <g class="fz" data-zone="pore">
              <ellipse class="fz-fill" fill="rgba(200,110,70,.14)" stroke="#c86e46" cx="33.5" cy="49.5" rx="7" ry="5"/>
              <ellipse class="fz-fill" fill="rgba(200,110,70,.14)" stroke="#c86e46" cx="66.5" cy="49.5" rx="7" ry="5"/>
              <circle class="fz-dot" fill="#c86e46" cx="31.5" cy="48.5" r=".8"/><circle class="fz-dot" fill="#c86e46" cx="35.5" cy="51" r=".8"/>
              <circle class="fz-dot" fill="#c86e46" cx="64.5" cy="50.7" r=".8"/><circle class="fz-dot" fill="#c86e46" cx="68.5" cy="48.5" r=".8"/>
              <text class="fz-label" fill="#c86e46" x="9" y="42">모공 · 볼</text>
            </g>
            <!-- 붉은기 → 볼 안쪽·코 -->
            <g class="fz" data-zone="redness">
              <ellipse class="fz-fill" fill="rgba(193,102,107,.16)" stroke="#c1666b" cx="42.5" cy="52" rx="4.4" ry="3"/>
              <ellipse class="fz-fill" fill="rgba(193,102,107,.16)" stroke="#c1666b" cx="57.5" cy="52" rx="4.4" ry="3"/>
              <ellipse class="fz-fill" fill="rgba(193,102,107,.16)" stroke="#c1666b" cx="50" cy="47" rx="3.2" ry="2.4"/>
              <text class="fz-label" fill="#c1666b" x="64" y="61.5">붉은기</text>
            </g>
            <!-- 흉터·색소 → 국소 부위(오른볼) -->
            <g class="fz" data-zone="scar">
              <circle class="fz-fill" fill="rgba(150,90,150,.14)" stroke="#965a96" cx="65" cy="48" r="3.2"/>
              <circle class="fz-dot" fill="#965a96" cx="65" cy="48" r=".9"/>
              <circle class="fz-fill" fill="rgba(150,90,150,.14)" stroke="#965a96" cx="61" cy="52.5" r="2.2"/>
              <circle class="fz-dot" fill="#965a96" cx="61" cy="52.5" r=".7"/>
              <text class="fz-label" fill="#965a96" x="72" y="36">흉터 · 국소</text>
            </g>
            <!-- 여드름 → 턱·볼 -->
            <g class="fz" data-zone="acne">
              <ellipse class="fz-fill" fill="rgba(193,60,60,.13)" stroke="#c13c3c" cx="50" cy="65" rx="7.5" ry="3.8"/>
              <circle class="fz-dot" fill="#c13c3c" cx="47" cy="64" r="1"/><circle class="fz-dot" fill="#c13c3c" cx="53" cy="65.8" r=".9"/><circle class="fz-dot" fill="#c13c3c" cx="50" cy="67" r=".8"/>
              <circle class="fz-dot" fill="#c13c3c" cx="34.5" cy="54.5" r=".9"/>
              <text class="fz-label" fill="#c13c3c" x="31" y="74.5">여드름 · 턱·볼</text>
            </g>
          </svg>
        </div>
        <div class="face-legend" id="faceLegend">
          <span class="legend-item" data-concern="oil"><span class="legend-dot oil"></span>유분 · T존(이마·코)</span>
          <span class="legend-item" data-concern="pore"><span class="legend-dot pore"></span>모공 · 볼</span>
          <span class="legend-item" data-concern="redness"><span class="legend-dot redness"></span>붉은기 · 볼·코</span>
          <span class="legend-item" data-concern="scar"><span class="legend-dot scar"></span>흉터·색소 · 국소</span>
          <span class="legend-item" data-concern="acne"><span class="legend-dot acne"></span>여드름 · 턱·볼</span>
        </div>
      </div>

      <div class="diag-scorelist">
        <div class="diag-summary-title">항목별 점수</div>
        <div id="diagScoreRows"></div>
      </div>
    </div>

    <div class="diag-tabsblock">
      <div class="diag-concerns-head">
        <span>고민별 자세히 보기</span>
      </div>
      <div class="diag-tabs-layout">
        <div class="diag-tabs" id="diagTabs"></div>
        <div id="diagPanels"></div>
      </div>
    </div>
  </div>
</div>

<div class="screen auth hidden" id="screenAuth">
  <div class="auth-card">
    <button type="button" class="auth-back" id="authBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg> 뒤로
    </button>
    <div class="eyebrow on-dark">MEMBERSHIP</div>
    <h1 class="auth-title">내 피부, <em>기록</em>해서 관리해요</h1>
    <p class="auth-sub">가입하면 분석 결과와 추천을 저장하고, 피부 변화를 계속 추적할 수 있어요.</p>
    <div class="auth-benefits">
      <div class="auth-benefit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/></svg>
        <div><b>피부 기록 저장</b><span>분석 결과를 계정에 보관</span></div>
      </div>
      <div class="auth-benefit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        <div><b>추천 이력 관리</b><span>받은 제품 추천을 한눈에</span></div>
      </div>
      <div class="auth-benefit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8M14 7h7v7"/></svg>
        <div><b>변화 추적</b><span>이전 대비 피부 점수 비교</span></div>
      </div>
    </div>
    <div class="social-btns">
      <button type="button" class="social-btn" data-provider="google">
        <span class="social-ic" style="background:#fff;color:#4285F4;border:1px solid #e6e4de;">G</span>구글로 시작하기
      </button>
    </div>
    <button type="button" class="auth-skip" id="authSkip">회원가입 없이 둘러보기</button>
  </div>
</div>

<div class="screen consent hidden" id="screenConsent">
  <div class="consent-card">
    <button type="button" class="auth-back" id="consentBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg> 뒤로
    </button>
    <h1 class="consent-title">약관에 동의해주세요</h1>
    <p class="consent-sub">피부 데이터를 안전하게 관리하기 위해 아래 항목 동의가 필요해요.</p>

    <label class="consent-all">
      <input type="checkbox" id="consentAll" />
      <span class="consent-check"></span>
      <b>약관 전체 동의</b>
    </label>

    <div class="consent-list" id="consentList">
      <div class="consent-item">
        <label>
          <input type="checkbox" class="consent-chk" data-req="1" />
          <span class="consent-check"></span>
          <span class="consent-label"><i class="consent-tag req">필수</i> 서비스 이용약관 및 개인정보 수집·이용 동의</span>
        </label>
        <button type="button" class="consent-more">자세히</button>
        <div class="consent-detail">서비스 제공을 위해 최소한의 정보(이메일·나이·닉네임)만 수집하고, 피부 분석·상담 이력을 계정에 저장해 변화 추적에 사용합니다. 촬영 이미지는 분석에만 쓰이며 데모에서는 저장되지 않고, 목적 달성 후 지체 없이 파기합니다.</div>
      </div>
      <div class="consent-item">
        <label>
          <input type="checkbox" class="consent-chk" data-req="0" />
          <span class="consent-check"></span>
          <span class="consent-label"><i class="consent-tag opt">선택</i> 마케팅 정보 수신 동의</span>
        </label>
        <button type="button" class="consent-more">자세히</button>
        <div class="consent-detail">신제품·이벤트·맞춤 추천 소식을 받아볼 수 있습니다. 동의하지 않아도 서비스 이용에는 제한이 없어요.</div>
      </div>
    </div>

    <div class="consent-hint" id="consentHint"></div>
    <div class="consent-actions">
      <button type="button" class="btn btn-outline" id="consentReqOnly">필수만 동의</button>
      <button type="button" class="btn btn-gold" id="consentSubmit">동의하고 시작하기</button>
    </div>
  </div>
</div>

<div class="screen consent hidden" id="screenProfile">
  <div class="consent-card">
    <button type="button" class="auth-back" id="profBack">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg> 뒤로
    </button>
    <h1 class="consent-title">프로필을 설정해주세요</h1>
    <p class="consent-sub" id="profProvider">계정에서 정보를 가져왔어요</p>
    <div class="field-row">
      <label>이메일 <i class="prof-badge">계정 연동</i></label>
      <input type="email" id="profEmail" readonly />
    </div>
    <div class="field-row">
      <label>나이 <i class="prof-badge">계정 연동</i></label>
      <input type="number" id="profAge" min="1" max="120" placeholder="나이" />
    </div>
    <div class="field-row">
      <label>성별 <i class="prof-badge">비교 기준</i></label>
      <div class="prof-gender" id="profGender">
        <button type="button" class="prof-gender-btn" data-gender="male">남성</button>
        <button type="button" class="prof-gender-btn" data-gender="female">여성</button>
        <button type="button" class="prof-gender-btn" data-gender="">밝히지 않음</button>
      </div>
    </div>
    <div class="field-row">
      <label>닉네임</label>
      <input type="text" id="profNick" maxlength="12" placeholder="사용할 닉네임을 입력해주세요" />
    </div>
    <div class="consent-hint" id="profHint"></div>
    <button type="button" class="btn btn-gold" id="profSubmit" style="width:100%;padding:14px;">시작하기</button>
  </div>
</div>

<div class="screen mypage hidden" id="screenMyPage">
  <div class="mypage-card">
    <div class="mp-head">
      <div class="mp-user">
        <div class="mp-avatar" id="mpAvatar">회</div>
        <div>
          <div class="mp-name" id="mpName">회원님</div>
          <div class="mp-provider" id="mpProvider">로그인</div>
        </div>
      </div>
      <div class="mp-head-actions">
        <button type="button" class="mp-ghost" id="mpLogout">로그아웃</button>
        <button type="button" class="btn btn-dark btn-sm" id="mpHome">홈으로</button>
      </div>
    </div>

    <div class="mp-hello">내 피부 관리 페이지예요. 그동안의 기록을 한곳에서 확인해보세요.</div>

    <div class="mp-stats">
      <div class="mp-stat"><b id="mpCountA">0</b><span>피부 분석</span></div>
      <div class="mp-stat"><b id="mpCountR">0</b><span>추천 이력</span></div>
      <div class="mp-stat"><b id="mpCountC">0</b><span>상담 내역</span></div>
    </div>

    <div class="mp-cta-row">
      <button type="button" class="btn btn-gold btn-sm" id="mpStart">새 피부 분석 시작</button>
      <button type="button" class="mp-recall" id="mpRecall">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 2.6-6.36M3 4v5h5"/></svg>
        최근 분석 결과 다시 보기
      </button>
    </div>

    <div class="mp-tabs">
      <button type="button" class="mp-tab active" data-mp="analyses">피부 분석 내역</button>
      <button type="button" class="mp-tab" data-mp="recommends">추천 이력</button>
      <button type="button" class="mp-tab" data-mp="consults">상담 내역</button>
    </div>
    <div class="mp-panels" id="mpPanels"></div>
  </div>
</div>

<div class="screen choice hidden" id="screenStartChoice">
  <div class="choice-card">
    <div class="choice-badge">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 12l5 5L20 7"/></svg>
    </div>
    <div class="choice-title" id="startChoiceTitle">가입이 완료되었어요</div>
    <p class="choice-sub">어떤 방식으로 피부를 확인해볼까요?</p>

    <button type="button" class="choice-btn choice-btn-primary" id="startCamera">
      <div class="choice-btn-title">
        <svg class="choice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        영상 촬영으로 스캔하기
      </div>
      <span class="choice-btn-desc">카메라로 얼굴을 비추면 AI가 바로 분석해요</span>
    </button>

    <button type="button" class="choice-btn" id="startSurvey">
      <div class="choice-btn-title">
        <svg class="choice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        설문으로 진단하기
      </div>
      <span class="choice-btn-desc">카메라 없이 고민을 선택해 결과를 확인해요</span>
    </button>

    <button type="button" class="mp-recall" id="startToMypage" style="margin:14px auto 0;display:flex;">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>
      내 피부 관리 페이지로 가기
    </button>
  </div>
</div>

<div id="screenApp" class="app-screen" style="display:none;">
<div class="nav">
  <div class="wrap">
    <div class="brand"><b>FOR HIM</b><span>Men's Skincare Lab</span></div>
    <div class="nav-links">
      <a href="#" data-step="analysis">피부분석</a>
      <a href="#" data-step="recommend">제품추천</a>
      <a href="#" data-step="style">스타일</a>
      <a href="#" data-step="community">커뮤니티</a>
      <a href="#" data-step="rewards">리워드</a>
    </div>
    <button type="button" class="btn btn-outline btn-sm" id="navRecall" style="display:none;">최근 결과 다시 보기</button>
    <button type="button" class="btn btn-outline btn-sm" id="navMember">로그인</button>
    <button type="button" class="btn btn-dark btn-sm" data-step="analysis">분석 시작</button>
  </div>
</div>

<section class="hero app-step active" id="stepHero">
  <div class="wrap">
    <div>
      <div class="eyebrow on-dark">MEN'S BEAUTY, SIMPLIFIED</div>
      <h1><span id="heroGreet"></span>피부 관리, <em>어렵게</em><br/>생각하지 마세요</h1>
      <p class="sub on-dark">복잡한 성분 이름도, 매장에서의 어색한 상담도 필요 없어요. 지금 신경 쓰이는 부분만 골라도 AI가 상태를 확인해드려요.</p>
      <div class="hero-cta">
        <button type="button" class="btn btn-gold" data-step="analysis">30초 만에 피부 확인하기</button>
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
    <div class="step-nav on-dark" style="grid-column:1/-1;">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" disabled>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-gold btn-sm step-nav-btn" data-step-next>다음</button>
    </div>
  </div>
</section>

<section id="analysis" class="app-step">
  <div class="wrap">
    <div class="eyebrow">SKIN ANALYSIS AI</div>
    <h2>피부 영상 분석 AI</h2>
    <p class="sub single-line-text">카메라 앞에 서지 않아도 괜찮아요. 이 데모에서는 지금 느끼는 고민을 선택하면 실제 분석처럼 결과를 보여드려요.</p>

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
          <button type="button" class="btn btn-dark btn-sm" id="toRecommend" data-step="recommend">맞춤 제품 추천 받기</button>
        </div>
      </div>
    </div>
    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-next>다음</button>
    </div>
  </div>
</section>

<section id="recommend" class="recommend app-step">
  <div class="wrap">
    <div class="eyebrow">PRODUCT RECOMMEND AI</div>
    <h2>제품 추천 AI</h2>
    <p class="sub single-line-text">관리 단계를 선택하면, 단계 안에서 라인·카테고리별로 AI가 매칭한 추천 제품을 보여드려요.</p>

    <div class="tier-tabs" id="tierTabs"></div>
    <div class="tier-desc" id="tierDesc"></div>
    <div class="tier-lines" id="tierProdRow"></div>

    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-next>상황별 스타일 추천 →</button>
    </div>
  </div>
</section>

<section id="style" class="app-step">
  <div class="wrap">
    <div class="eyebrow">STYLE GUIDE AI</div>
    <h2>상황별 스타일, 딱 정해드려요</h2>
    <p class="sub">피부 상태에 맞춰 화장품부터 옷·헤어까지. 오늘 어디 가는지만 고르면 조합을 정해드려요.</p>

    <div class="tpo-tabs" id="tpoTabs"></div>
    <div class="tpo-combo">
      <div class="tpo-combo-head" id="wxHead">
        <div class="wx-main">
          <div class="tc-badge">오늘의 날씨</div>
          <div class="tc-title" id="wxTitle">날씨 불러오는 중…</div>
          <div class="wx-meta" id="wxMeta"></div>
          <div class="wx-copy" id="wxCopy"></div>
        </div>
        <button type="button" class="wx-refresh" id="wxRefresh">↻ 새로고침</button>
        <div class="wx-reco" id="wxReco"></div>
        <div class="wx-note" id="wxNote" hidden></div>
      </div>
      <div class="tpo-combo-body" id="tpoComboBody"></div>
    </div>

    <div class="style-feed-head">
      <div>
        <div class="style-feed-title">스타일 피드</div>
        <div class="style-feed-sub">사진 속 스타일에 쓰인 아이템을 확인해보세요</div>
      </div>
    </div>
    <div class="style-feed" id="styleFeed"></div>

    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-next>다음</button>
    </div>
  </div>
</section>

<div class="sheet" id="styleSheet" hidden>
  <div class="sheet-backdrop" id="sheetBackdrop"></div>
  <div class="sheet-card" id="sheetCard"></div>
</div>

<section id="extra" class="app-step">
  <div class="wrap">
    <div class="eyebrow">MORE CONCERNS</div>
    <h2>더 필요한 케어가 있나요?</h2>
    <p class="sub">관심있는 고민을 선택하면 맞춤 제품을 추가로 추천해드려요.</p>

    <div class="extra-tabs" id="extraTabs"></div>
    <div class="prod-row" id="extraProdRow"></div>

    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-next>다음</button>
    </div>
  </div>
</section>

<section id="community" class="app-step">
  <div class="wrap">
    <div class="eyebrow">COMMUNITY</div>
    <h2>커뮤니티</h2>
    <p class="sub">같은 고민, 같은 눈높이에서 편하게 물어보세요.</p>

    <div class="cm-view" id="cmViewList">
      <div class="cm-toolbar">
        <label class="cm-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
          <input type="text" id="cmSearch" placeholder="궁금한 키워드로 검색해보세요" />
        </label>
        <div class="cm-auth" id="cmAuth"></div>
        <button type="button" class="btn btn-dark btn-sm cm-write-btn" id="cmWriteBtn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>
          글 남기기
        </button>
      </div>
      <div class="cm-cats" id="cmCats"></div>
      <div class="cm-list" id="cmList"></div>
      <div class="cm-empty" id="cmEmpty" hidden>조건에 맞는 글이 아직 없어요. 첫 글을 남겨보세요!</div>
    </div>

    <div class="cm-view" id="cmViewDetail" hidden>
      <button type="button" class="cm-back" id="cmDetailBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg>
        목록으로
      </button>
      <div class="cm-detail-card" id="cmDetailCard"></div>
    </div>

    <div class="cm-view" id="cmViewWrite" hidden>
      <button type="button" class="cm-back" id="cmWriteBack">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M15 18l-6-6 6-6"/></svg>
        목록으로
      </button>
      <div class="cm-form">
        <div class="cm-form-title" id="cmFormTitle">새 글 남기기</div>
        <div class="cm-field">
          <label>콘텐츠 유형</label>
          <div class="cm-type-seg" id="cmFormType">
            <button type="button" class="cm-type-btn on" data-type="normal">일반 글</button>
            <button type="button" class="cm-type-btn" data-type="vote">투표형 (남좋메/여좋메)</button>
            <button type="button" class="cm-type-btn" data-type="ba">비포·애프터</button>
          </div>
        </div>
        <div class="cm-field">
          <label>카테고리</label>
          <select id="cmFormCat"></select>
        </div>
        <div class="cm-field">
          <label>제목</label>
          <input type="text" id="cmFormTitleInput" maxlength="60" placeholder="제목을 입력해주세요" />
        </div>
        <div class="cm-field" id="cmFormVoteFields" hidden>
          <label>투표 선택지 (2개)</label>
          <input type="text" id="cmFormOpt1" maxlength="30" placeholder="선택지 1 (예: 가볍게 톤업만)" style="margin-bottom:8px;" />
          <input type="text" id="cmFormOpt2" maxlength="30" placeholder="선택지 2 (예: 확실하게 커버)" />
        </div>
        <div class="cm-field">
          <label>내용</label>
          <textarea id="cmFormBody" placeholder="같은 고민을 가진 분들에게 편하게 이야기해보세요"></textarea>
        </div>
        <div class="cm-field" id="cmFormBaFields" hidden>
          <label>사용 제품 (줄바꿈으로 구분)</label>
          <textarea id="cmFormProducts" placeholder="예)&#10;닥터지 레드 블레미쉬 토너&#10;라운드랩 마데카 크림" style="min-height:80px;margin-bottom:12px;"></textarea>
          <label>변화 포인트</label>
          <input type="text" id="cmFormChange" maxlength="80" placeholder="예: 붉은기가 가라앉고 톤이 밝아졌어요" />
        </div>
        <div class="cm-field">
          <label>사진 첨부 (선택)</label>
          <label class="cm-photo-drop" for="cmFormPhoto">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            <span>사진을 선택하세요 (JPG·PNG)</span>
          </label>
          <input type="file" id="cmFormPhoto" accept="image/*" hidden />
          <div class="cm-photo-preview" id="cmPhotoPreview">
            <img id="cmPhotoImg" alt="첨부 미리보기" />
            <button type="button" class="cm-photo-remove" id="cmPhotoRemove" aria-label="사진 삭제">×</button>
          </div>
        </div>
        <div class="cm-form-hint" id="cmFormHint"></div>
        <div class="cm-form-actions">
          <button type="button" class="btn btn-outline btn-sm" id="cmFormCancel">취소</button>
          <button type="button" class="btn btn-dark btn-sm" id="cmFormSubmit">등록하기</button>
        </div>
      </div>
    </div>

    <div class="cm-modal" id="cmAuthModal" hidden>
      <div class="cm-modal-card">
        <button type="button" class="cm-modal-close" id="cmAuthClose" aria-label="닫기">×</button>
        <div class="cm-modal-title" id="cmAuthTitle">로그인</div>
        <p class="cm-modal-sub">글쓰기·댓글을 남기려면 로그인이 필요해요.</p>
        <div class="cm-field"><label>이메일</label><input type="email" id="cmAuthEmail" placeholder="you@example.com" /></div>
        <div class="cm-field"><label>비밀번호</label><input type="password" id="cmAuthPw" placeholder="6자 이상" /></div>
        <div class="cm-form-hint" id="cmAuthHint"></div>
        <button type="button" class="btn btn-dark" id="cmAuthSubmit" style="width:100%;padding:13px;">로그인</button>
        <button type="button" class="cm-auth-toggle" id="cmAuthToggle">계정이 없으신가요? 회원가입</button>
      </div>
    </div>

    <footer>
      <div class="fine">본 화면은 데모이며 모든 분석·추천 결과는 예시 데이터입니다.</div>
    </footer>
    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-loop>처음으로</button>
    </div>
  </div>
</section>

<section id="rewards" class="app-step rewards-page">
  <div class="wrap">
    <div class="eyebrow on-dark">REWARDS</div>
    <h2>리워드</h2>
    <p class="sub on-dark">미션으로 포인트를 모으고, 제휴 서비스에서 바로 사용하세요.</p>
    <div class="reward-card">
      <div class="reward-body">
        <div class="reward-col">
          <div class="reward-head">
            <div class="reward-title">
              <svg class="rw-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12v9H4v-9M2 7h20v5H2zM12 22V7M12 7C12 7 12 2 8.5 2 5 2 5 7 12 7zM12 7s0-5 3.5-5S19 7 12 7z"/></svg>
              리워드 미션
            </div>
            <div class="reward-balance">내 포인트 <b id="rewardTotal">0</b>P</div>
          </div>
          <div class="reward-missions" id="rewardMissions"></div>
        </div>
        <div class="reward-use">
          <div class="reward-use-head">리워드 사용처 <span>여기서 바로 사용 가능</span></div>
          <a class="use-card" href="https://tinder.com" target="_blank" rel="noopener noreferrer">
            <div class="use-ic" style="background:#3a2530;color:#fe3c72;">🔥</div>
            <div class="use-txt"><b>틴더</b><span>포인트 사용 가능</span></div>
            <div class="use-go">사이트로 이동 →</div>
          </a>
          <a class="use-card" href="https://map.naver.com/p/search/%ED%98%BC%EC%88%A0%EC%A7%91" target="_blank" rel="noopener noreferrer">
            <div class="use-ic" style="background:#233022;color:#5ac467;">🍶</div>
            <div class="use-txt"><b>혼술집</b><span>제휴 혜택 확인</span></div>
            <div class="use-go">네이버 맵에서 보기 →</div>
          </a>
          <a class="use-card" href="https://www.oliveyoung.co.kr" target="_blank" rel="noopener noreferrer">
            <div class="use-ic" style="background:#2f2a20;color:#f5c04a;">🛍️</div>
            <div class="use-txt"><b>올리브영</b><span>적립 포인트로 이용</span></div>
            <div class="use-go">추천 상품 보러가기 →</div>
          </a>
        </div>
      </div>
    </div>
    <div class="step-nav on-dark">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-gold btn-sm step-nav-btn" data-step-loop>처음으로</button>
    </div>
  </div>
</section>

<div class="toast" id="toast"></div>
</div>

<script>
(function(){
  window.appState = { concerns:new Set(), analyzed:false, allInOne:false, age:29, nickname:'', gender:'', survey:{} };
  const state = window.appState;

  const splash = document.getElementById('screenSplash');
  const splashLogo = document.getElementById('splashLogo');
  const intro = document.getElementById('screenIntro');
  const camera = document.getElementById('screenCamera');
  const choice = document.getElementById('screenChoice');
  const simpleResult = document.getElementById('screenSimple');
  const diagnosis = document.getElementById('screenDiagnosis');
  const loadScreen = document.getElementById('screenLoading');
  const surveyScreen = document.getElementById('screenSurvey');
  const appScreen = document.getElementById('screenApp');
  let nickname = '';
  let enteredAge = 29;

  /* ---------------- 0) last-result recall ---------------- */
  const RECALL_KEY = 'forhim_last_result_v3';

  function saveLastResult(){
    try {
      localStorage.setItem(RECALL_KEY, JSON.stringify({
        nickname: nickname, age: enteredAge, concerns: Array.from(state.concerns), savedAt: Date.now()
      }));
    } catch(e){}
  }

  function loadLastResult(){
    try {
      const raw = localStorage.getItem(RECALL_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch(e){ return null; }
  }

  function viewLastResult(){
    const saved = loadLastResult();
    if(!saved) return;
    nickname = saved.nickname || '고객';
    enteredAge = saved.age || 29;
    state.age = enteredAge;
    state.nickname = nickname;
    state.concerns = new Set(saved.concerns && saved.concerns.length ? saved.concerns : ['scar','pore','oil','acne']);

    /* 이력·선택 화면을 거치지 않고, 상단 탭이 있는 메인 앱의 분석 결과 화면으로 바로 진입.
       enterAppStep이 멤버 화면을 모두 닫고 앱을 열며, showAnalysisResult가
       저장된 최근 분석 상태를 결과 UI로 즉시 렌더링한다. */
    enterAppStep('analysis');
    if(window.showAnalysisResult){ window.showAnalysisResult(); }
  }

  function initRecallEntryPoints(){
    const saved = loadLastResult();
    if(!saved) return;
    const introLink = document.getElementById('introRecall');
    const navLink = document.getElementById('navRecall');
    if(introLink) introLink.style.display = 'flex';
    if(navLink) navLink.style.display = 'inline-flex';
  }
  document.getElementById('introRecall').addEventListener('click', viewLastResult);
  document.getElementById('navRecall').addEventListener('click', viewLastResult);
  initRecallEntryPoints();

  /* ---------------- membership + records (dummy social login) ---------------- */
  const MEMBER_KEY = 'forhim_member';
  /* Records are stored per-account so a new member starts empty and their own
     history keeps accumulating. Guests write to a shared bucket that is merged
     into the account on sign-up, so a just-finished analysis carries over. */
  /* v3: 이전 버전에 쌓인 더미/샘플·중복 기록을 무시하고 새 버킷부터 실제 기록만 저장 */
  const RECORDS_PREFIX = 'forhim_records_v3_';
  const GUEST_RECORDS_KEY = 'forhim_records_guest_v3';
  const screenAuth = document.getElementById('screenAuth');
  const screenConsent = document.getElementById('screenConsent');
  const screenProfile = document.getElementById('screenProfile');
  const screenMyPage = document.getElementById('screenMyPage');
  const screenStartChoice = document.getElementById('screenStartChoice');
  const CONCERN_LABEL = { scar:'흉터', pore:'모공', oil:'유분', acne:'여드름' };
  /* 계정 연동 시 제공사에서 받아오는 정보(데모: 시뮬레이션). 실제 OAuth 연동 시
     이메일은 세션에서, 나이는 제공사 동의 범위에 따라 채워집니다. */
  const PROVIDER_SAMPLE = {
    kakao:  { email:'minjun.kim@kakao.com',  age:28, name:'김민준', gender:'male' },
    google: { email:'minjun.kim@gmail.com',  age:31, name:'Minjun', gender:'male' },
    naver:  { email:'minjun.kim@naver.com',  age:26, name:'민준',   gender:'male' }
  };
  let authOrigin = 'intro';
  let pendingProvider = null;
  let pendingMarketing = false;
  let linkedAccount = null;
  let mpTab = 'analyses';

  /* Start/stop the real Google OAuth. OAuth can't run inside the sandboxed
     iframe, so we navigate the top window back to the app with a flag that the
     Python layer reads (?login=google / ?logout=1). */
  function topGo(flag){
    const base = window.APP_URL || '';
    if(!base){ memberToast('로그인 설정을 확인해주세요. (secrets [auth] 확인)'); return; }
    const url = base + (base.indexOf('?')>=0?'&':'?') + flag;
    /* Navigate the whole tab (not the iframe) so OAuth runs at the top level.
       A real anchor click with target="_top" during a user gesture is the most
       reliable way through the sandbox; scripted nav is a fallback that only
       fires if the anchor click didn't already tear this page down. */
    try{
      const a = document.createElement('a');
      a.href = url; a.target = '_top'; a.rel = 'opener';
      document.body.appendChild(a); a.click(); a.remove();
    }catch(e){}
    setTimeout(function(){
      try{ window.top.location.href = url; }
      catch(e){ try{ window.open(url, '_blank'); }catch(e2){} }
    }, 150);
  }
  function startGoogleLogin(){
    /* Already authenticated with Google (session lingers across reloads): no
       OAuth needed — continue the signup right here in the iframe. */
    if(window.USER_LOGGED_IN === '1'){ beginGoogleSignup(); return; }
    /* Not logged in: real OAuth needs top-level navigation, which the Streamlit
       component iframe blocks — so it falls back to opening a new tab. Use
       localStorage (shared across tabs) so the login tab continues to consent. */
    try{ localStorage.setItem('forhim_signup_pending', '1'); }catch(e){}
    memberToast('구글 로그인 창을 여는 중이에요…');
    topGo('login=google');
  }

  function loadMember(){ try{ return JSON.parse(localStorage.getItem(MEMBER_KEY) || 'null'); }catch(e){ return null; } }
  function saveMember(m){ member = m; try{ if(m) localStorage.setItem(MEMBER_KEY, JSON.stringify(m)); else localStorage.removeItem(MEMBER_KEY); }catch(e){} }
  function isMember(){ return !!(member && member.loggedIn); }
  let member = loadMember();
  /* 로그인 회원 정보를 분석 상태에 반영(비교 기준·얼굴 모델 성별에 사용). */
  if(member){
    if(member.gender) state.gender = member.gender;
    if(member.age){ enteredAge = member.age; state.age = member.age; }
  }

  function emptyRecords(){ return { analyses:[], recommends:[], consults:[] }; }
  /* Stable per-account id: email when available, else provider+nickname. */
  function memberId(m){
    m = m || member;
    if(!m) return '';
    return (m.email ? String(m.email).toLowerCase() : (m.provider||'') + ':' + (m.nickname||'')) || 'member';
  }
  function currentRecordsKey(){ return isMember() ? (RECORDS_PREFIX + memberId()) : GUEST_RECORDS_KEY; }
  function readRecords(key){ try{ const r = JSON.parse(localStorage.getItem(key) || 'null'); if(r) return r; }catch(e){} return null; }
  function loadRecords(){ return readRecords(currentRecordsKey()) || emptyRecords(); }
  function saveRecords(r){ records = r; try{ localStorage.setItem(currentRecordsKey(), JSON.stringify(r)); }catch(e){} }
  /* Point `records` at the active bucket (account when logged in, else guest). */
  function refreshRecordsForMember(){ records = loadRecords(); }
  /* On sign-up, fold any guest-session history into the account and clear it. */
  function mergeGuestIntoMember(){
    const guest = readRecords(GUEST_RECORDS_KEY);
    const acct = readRecords(RECORDS_PREFIX + memberId()) || emptyRecords();
    if(guest){
      ['analyses','recommends','consults'].forEach(function(cat){
        const have = new Set((acct[cat]||[]).map(function(x){ return x.id; }));
        (guest[cat]||[]).forEach(function(x){ if(!have.has(x.id)){ acct[cat].push(x); } });
        acct[cat].sort(function(a,b){ return b.date - a.date; });
      });
      try{ localStorage.removeItem(GUEST_RECORDS_KEY); }catch(e){}
    }
    records = acct;
    try{ localStorage.setItem(RECORDS_PREFIX + memberId(), JSON.stringify(acct)); }catch(e){}
  }
  /* 이전 버전(v2 등)에 쌓인 더미/중복 기록을 localStorage에서 실제로 제거 */
  (function purgeLegacyRecords(){
    try{
      const kill = [];
      for(let i=0;i<localStorage.length;i++){
        const k = localStorage.key(i);
        if(!k) continue;
        if(k.indexOf('forhim_records_v2_')===0 || k==='forhim_records_guest' || k==='forhim_last_result'){ kill.push(k); }
      }
      kill.forEach(function(k){ localStorage.removeItem(k); });
    }catch(e){}
  })();
  let records = null;
  records = loadRecords();

  function mpEsc(s){ return String(s==null?'':s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function fmtDate(ts){ const d = new Date(ts); const p = n=>String(n).padStart(2,'0'); return d.getFullYear()+'.'+p(d.getMonth()+1)+'.'+p(d.getDate()); }
  function providerLabel(p){ return p==='kakao'?'카카오':p==='google'?'구글':p==='naver'?'네이버':'회원'; }
  function concernLabel(k){ return CONCERN_LABEL[k] || k; }

  function recordAnalysis(){
    const metrics = computeDiagnosis();
    const overall = Math.round(metrics.reduce((a,m)=>a+m.score,0)/metrics.length*10);
    const worst = metrics.reduce((a,b)=> a.score<b.score?a:b);
    const type = state.concerns.has('oil') ? '지성' : (state.concerns.has('pore')||state.concerns.has('scar')) ? '복합성' : '중성';
    const cs = Array.from(state.concerns).sort();
    const sig = type + '|' + overall + '|' + cs.join(',');   /* 동일 분석 판별용 서명 */
    const rec = { id:'a'+Date.now(), date:Date.now(), score:overall, type:type, top:worst.label, sig:sig,
      summary:(cs.map(concernLabel).join('·')||'전반') + ' 중심 분석, 종합 ' + overall + '점' };
    /* 같은 결과를 반복 완료하거나 짧은 시간 내 재저장되면 새 기록을 쌓지 않고 최신 것만 갱신
       → 탭 이동/새로고침/최근 결과 다시 보기 등으로 중복 누적되지 않음 */
    const latest = records.analyses[0];
    if(latest && (latest.sig === sig || Date.now() - latest.date < 60000)){ records.analyses[0] = rec; }
    else { records.analyses.unshift(rec); }
    saveRecords(records);
  }
  function recordRecommend(){
    const cs = Array.from(state.concerns);
    const rec = { id:'r'+Date.now(), date:Date.now(), title:(cs.map(concernLabel).join('·')||'맞춤') + ' 루틴 추천',
      summary:'AI 매칭 기반 단계별 추천', items:['1단계 스킨케어','2단계 선케어','3단계 베이스 메이크업','4단계 아이 메이크업','5단계 퍼퓸&바디'] };
    if(records.recommends[0] && Date.now()-records.recommends[0].date < 60000){ records.recommends[0] = rec; }
    else { records.recommends.unshift(rec); }
    saveRecords(records);
  }
  /* Exposed so the survey/analysis step (a separate IIFE) can log history too. */
  window.recordRecommend = recordRecommend;
  window.persistAnalysis = function(){ saveLastResult(); recordAnalysis(); };

  const MEMBER_SCREENS = [splash, intro, camera, loadScreen, surveyScreen, choice, simpleResult, diagnosis, screenAuth, screenConsent, screenProfile, screenMyPage, screenStartChoice];
  function showMemberScreen(el){
    MEMBER_SCREENS.forEach(s=>{ s.classList.add('hidden'); s.classList.remove('visible'); });
    appScreen.style.display = 'none';
    el.classList.remove('hidden'); requestAnimationFrame(()=> el.classList.add('visible'));
    window.scrollTo(0,0);
  }
  function backToApp(){
    MEMBER_SCREENS.forEach(s=>{ s.classList.add('hidden'); s.classList.remove('visible'); });
    appScreen.style.display = 'block';
    if(window.showAppStep){ window.showAppStep('hero'); }
    window.scrollTo(0,0);
  }
  /* Enter the main app at a specific step (e.g. the survey/analysis step). */
  function enterAppStep(step){
    MEMBER_SCREENS.forEach(s=>{ s.classList.add('hidden'); s.classList.remove('visible'); });
    appScreen.style.display = 'block';
    if(window.showAppStep){ window.showAppStep(step || 'hero'); }
    window.scrollTo(0,0);
  }
  /* Post-signup fork: shoot a video scan or take the concern survey. */
  function showStartChoice(){
    const t = document.getElementById('startChoiceTitle');
    if(t){ t.textContent = ((member && member.nickname) || nickname || '회원') + '님, 가입이 완료되었어요'; }
    showMemberScreen(screenStartChoice);
  }
  function goCamera(){
    if(!nickname){ nickname = (member && member.nickname) || '회원'; }
    state.nickname = nickname; state.age = enteredAge;
    showMemberScreen(camera);
    startCamera();
  }

  function showAuth(origin){
    authOrigin = origin || 'intro';
    if(isMember()){ showMyPage(); return; }
    /* "뒤로" only makes sense when we opened auth from inside the app; on the
       entry screen (after splash) there is nothing to go back to. */
    const back = document.getElementById('authBack');
    if(back) back.style.display = (authOrigin === 'app') ? '' : 'none';
    showMemberScreen(screenAuth);
  }
  function backFromAuth(){ if(authOrigin==='app'){ backToApp(); } else { showMemberScreen(intro); } }
  function doSocial(provider){
    pendingProvider = provider;
    linkedAccount = Object.assign({ provider:provider }, PROVIDER_SAMPLE[provider] || PROVIDER_SAMPLE.kakao);
    showConsent();
  }
  function showConsent(){
    setAllConsent(false);
    const hint = document.getElementById('consentHint'); if(hint) hint.textContent = '';
    showMemberScreen(screenConsent);
  }

  function setAllConsent(v){
    document.querySelectorAll('#consentList .consent-chk').forEach(c=>{ c.checked = v; });
    document.getElementById('consentAll').checked = v;
  }
  function setConsentReqOnly(){
    document.querySelectorAll('#consentList .consent-chk').forEach(c=>{ c.checked = (c.dataset.req==='1'); });
    syncConsentAll();
  }
  function syncConsentAll(){
    const chks = [].slice.call(document.querySelectorAll('#consentList .consent-chk'));
    document.getElementById('consentAll').checked = chks.every(c=>c.checked);
    document.getElementById('consentHint').textContent = '';
  }
  function consentSubmit(){
    const chks = [].slice.call(document.querySelectorAll('#consentList .consent-chk'));
    const reqOk = chks.filter(c=>c.dataset.req==='1').every(c=>c.checked);
    if(!reqOk){ document.getElementById('consentHint').textContent = '필수 항목에 동의해주세요.'; return; }
    pendingMarketing = chks.some(c=>c.dataset.req==='0' && c.checked);
    showProfile();
  }

  /* 성별 선택 UI (프로필). 기본값은 계정 정보 → 없으면 미선택. */
  let pendingGender = '';
  function setProfileGender(g){
    pendingGender = g;
    document.querySelectorAll('#profGender .prof-gender-btn').forEach(b=>{
      b.classList.toggle('on', b.dataset.gender === g);
    });
  }
  document.querySelectorAll('#profGender .prof-gender-btn').forEach(b=>{
    b.addEventListener('click', ()=> setProfileGender(b.dataset.gender));
  });

  function showProfile(){
    const acc = linkedAccount || PROVIDER_SAMPLE.kakao;
    document.getElementById('profProvider').textContent = providerLabel(pendingProvider) + ' 계정에서 정보를 가져왔어요';
    document.getElementById('profEmail').value = acc.email || '';
    document.getElementById('profAge').value = acc.age || '';
    document.getElementById('profNick').value = acc.name || nickname || '';
    document.getElementById('profHint').textContent = '';
    setProfileGender(acc.gender || '');
    showMemberScreen(screenProfile);
  }
  function profileSubmit(){
    const nick = document.getElementById('profNick').value.trim();
    const age = parseInt(document.getElementById('profAge').value, 10);
    const email = document.getElementById('profEmail').value.trim();
    const hint = document.getElementById('profHint');
    if(!nick){ hint.textContent = '닉네임을 입력해주세요.'; return; }
    if(!age || age < 1 || age > 120){ hint.textContent = '나이를 올바르게 입력해주세요.'; return; }
    nickname = nick; enteredAge = age; state.nickname = nick; state.age = age; state.gender = pendingGender;
    saveMember({ loggedIn:true, provider:pendingProvider||'kakao', nickname:nick, email:email, age:age, gender:pendingGender,
      joinedAt:Date.now(), agreements:{ required:true, marketing:!!pendingMarketing } });
    /* Load this account's history and fold in anything done as a guest, so the
       flow continues seamlessly and future records keep accumulating here. */
    mergeGuestIntoMember();
    updateMemberUI();
    if(window.awardPoints){ window.awardPoints('signup'); }   /* 회원가입 500P */
    showStartChoice();
  }

  /* 리워드 '회원가입' 미션 진입점: 이미 회원이면 마이페이지, 아니면 로그인 */
  window.rewardGoSignup = function(){ showAuth('intro'); };

  function memberToast(msg){ const t = document.getElementById('toast'); if(!t) return; t.textContent = msg; t.classList.add('show'); setTimeout(()=> t.classList.remove('show'), 2400); }
  function beginGoogleSignup(){
    pendingProvider = 'google';
    pendingMarketing = false;
    linkedAccount = { provider:'google', email:(window.USER_EMAIL||''), name:(window.USER_NAME||''), age:'' };
    showConsent();
  }
  function logout(){
    /* Log out of the app locally. (The underlying Streamlit Google session can't
       be cleared from the sandboxed iframe; it simply appears logged out here,
       and the membership screen lets the user start again.) */
    saveMember(null); refreshRecordsForMember(); updateMemberUI();
    try{ localStorage.removeItem('forhim_signup_pending'); }catch(e){}
    memberToast('로그아웃했어요.');
    showAuth('intro');
  }
  function updateMemberUI(){ const nav = document.getElementById('navMember'); if(nav){ nav.textContent = isMember() ? '마이페이지' : '로그인'; } }
  /* Keep the stored member in sync with the real Google session: if Google
     logged out (session gone) but we still have a saved google member, drop it. */
  function syncRealSession(){
    if(window.AUTH_ON==='1' && window.USER_LOGGED_IN!=='1' && isMember() && member.provider==='google'){
      saveMember(null); refreshRecordsForMember(); updateMemberUI();
    }
  }
  const SIGNUP_PENDING_KEY = 'forhim_signup_pending';
  /* localStorage (not sessionStorage) so a login that completes in a new tab —
     the only way through the iframe's top-navigation block — still continues
     the signup, since sessionStorage is per-tab but localStorage is per-origin. */
  function signupPending(){ try{ return localStorage.getItem(SIGNUP_PENDING_KEY) === '1'; }catch(e){ return false; } }
  function clearSignupPending(){ try{ localStorage.removeItem(SIGNUP_PENDING_KEY); }catch(e){} }

  /* Decide where to land after the splash. The logo always plays first; we only
     jump into the Google signup (consent) when the user just clicked the login
     button (a pending flag survives the OAuth redirect). A lingering Google
     session on a plain reload falls through to the membership entry screen. */
  function routeAfterSplash(){
    splash.classList.add('hidden');
    if(window.USER_LOGGED_IN === '1'){
      const email = (window.USER_EMAIL||'');
      const pending = signupPending();
      if(isMember() && member.provider === 'google' && (member.email||'') === email){
        clearSignupPending();
        refreshRecordsForMember(); updateMemberUI(); showMyPage(); return;
      }
      if(pending){
        clearSignupPending();
        beginGoogleSignup(); return;
      }
      /* logged in but not mid-signup → show membership entry as usual */
    }
    showAuth('intro');
  }

  function showMyPage(){ renderMyPage(); showMemberScreen(screenMyPage); }
  function mpCard(date, title, summary, badge){
    return '<div class="mp-record"><div class="mp-record-top"><span class="mp-record-date">'+date+'</span>'+
      (badge?'<span class="mp-record-badge">'+mpEsc(badge)+'</span>':'')+'</div>'+
      '<div class="mp-record-title">'+mpEsc(title)+'</div>'+
      '<div class="mp-record-sum">'+mpEsc(summary)+'</div></div>';
  }
  function mpEmpty(msg){ return '<div class="mp-empty">'+msg+'</div>'; }
  function renderMyPanels(){
    const el = document.getElementById('mpPanels');
    let html = '';
    if(mpTab==='analyses'){
      html = records.analyses.length ? records.analyses.map(a=> mpCard(fmtDate(a.date), a.type+' · '+a.top+' 집중', a.summary, a.score+'점')).join('') : mpEmpty('아직 분석 기록이 없어요.');
    } else if(mpTab==='recommends'){
      html = records.recommends.length ? records.recommends.map(r=> mpCard(fmtDate(r.date), r.title, r.summary+' · '+r.items.join(', '), '')).join('') : mpEmpty('아직 추천 이력이 없어요.');
    } else {
      html = records.consults.length ? records.consults.map(s=> mpCard(fmtDate(s.date), s.title, s.summary, s.status||'')).join('') : mpEmpty('아직 상담 내역이 없어요.');
    }
    el.innerHTML = html;
  }
  function renderMyPage(){
    const name = (member && member.nickname) || nickname || '회원';
    document.getElementById('mpName').textContent = name + '님';
    document.getElementById('mpAvatar').textContent = (name[0] || '회');
    const mEmail = (member && member.email) || '';
    const mAge = (member && member.age) || enteredAge;
    document.getElementById('mpProvider').textContent =
      providerLabel(member && member.provider) + ' 로그인' + (mEmail ? ' · ' + mEmail : '') + (mAge ? ' · ' + mAge + '세' : '');
    document.getElementById('mpCountA').textContent = records.analyses.length;
    document.getElementById('mpCountR').textContent = records.recommends.length;
    document.getElementById('mpCountC').textContent = records.consults.length;
    document.getElementById('mpRecall').style.display = loadLastResult() ? 'inline-flex' : 'none';
    renderMyPanels();
  }

  /* wiring */
  document.getElementById('introMember').addEventListener('click', ()=> showAuth('intro'));
  document.getElementById('navMember').addEventListener('click', ()=>{ if(isMember()) showMyPage(); else showAuth('app'); });
  document.getElementById('authBack').addEventListener('click', backFromAuth);
  document.getElementById('authSkip').addEventListener('click', ()=>{ if(authOrigin==='app') backToApp(); else showMemberScreen(intro); });
  document.querySelectorAll('#screenAuth .social-btn').forEach(b=> b.addEventListener('click', ()=>{
    if(b.dataset.provider==='google' && window.AUTH_ON==='1'){
      startGoogleLogin();
      return;
    }
    doSocial(b.dataset.provider);
  }));
  document.getElementById('consentBack').addEventListener('click', ()=> showMemberScreen(screenAuth));
  document.getElementById('profBack').addEventListener('click', ()=> showMemberScreen(screenConsent));
  document.getElementById('profSubmit').addEventListener('click', profileSubmit);
  document.getElementById('startCamera').addEventListener('click', goCamera);
  document.getElementById('startSurvey').addEventListener('click', ()=> enterAppStep('analysis'));
  document.getElementById('startToMypage').addEventListener('click', showMyPage);
  document.getElementById('consentSubmit').addEventListener('click', consentSubmit);
  document.getElementById('consentReqOnly').addEventListener('click', ()=>{ setConsentReqOnly(); consentSubmit(); });
  document.getElementById('consentAll').addEventListener('change', (e)=> setAllConsent(e.target.checked));
  document.querySelectorAll('#consentList .consent-chk').forEach(c=> c.addEventListener('change', syncConsentAll));
  document.querySelectorAll('#consentList .consent-more').forEach(m=> m.addEventListener('click', ()=>{
    const d = m.parentElement.querySelector('.consent-detail');
    d.classList.toggle('show'); m.textContent = d.classList.contains('show') ? '닫기' : '자세히';
  }));
  document.getElementById('mpLogout').addEventListener('click', logout);
  document.getElementById('mpHome').addEventListener('click', backToApp);
  document.getElementById('mpStart').addEventListener('click', goCamera);
  document.getElementById('mpRecall').addEventListener('click', ()=>{ if(loadLastResult()) viewLastResult(); else goCamera(); });
  document.querySelectorAll('#screenMyPage .mp-tab').forEach(t=> t.addEventListener('click', ()=>{
    document.querySelectorAll('#screenMyPage .mp-tab').forEach(x=> x.classList.remove('active'));
    t.classList.add('active'); mpTab = t.dataset.mp; renderMyPanels();
  }));
  syncRealSession();
  updateMemberUI();

  /* ---------------- 1) splash ---------------- */
  /* The logo always plays; routeAfterSplash decides the first screen. */
  setTimeout(()=> splashLogo.classList.add('sharp'), 150);
  setTimeout(()=> splashLogo.classList.remove('sharp'), 2400);
  setTimeout(()=> splash.classList.add('fade-out'), 2900);
  setTimeout(routeAfterSplash, 3700);

  /* ---------------- 2) intro form ---------------- */
  const nickInput = document.getElementById('nickInput');
  const ageInput = document.getElementById('ageInput');
  const introHint = document.getElementById('introHint');

  document.getElementById('introConfirm').addEventListener('click', ()=>{
    const nick = nickInput.value.trim();
    const age = ageInput.value.trim();
    if(!nick || !age){
      introHint.textContent = '닉네임과 나이를 모두 입력해주세요.';
      return;
    }
    if(Number(age) <= 0 || Number(age) > 120){
      introHint.textContent = '나이를 올바르게 입력해주세요.';
      return;
    }
    nickname = nick;
    enteredAge = Number(age);
    state.age = enteredAge;
    state.nickname = nickname;
    intro.classList.remove('visible');
    setTimeout(()=>{
      intro.classList.add('hidden');
      camera.classList.remove('hidden');
      requestAnimationFrame(()=> camera.classList.add('visible'));
      startCamera();
    }, 550);
  });

  /* ---------------- 3) camera capture ---------------- */
  const camVideo = document.getElementById('camVideo');
  const camArrow = document.getElementById('camArrow');
  const camScanline = document.getElementById('camScanline');
  const camSub = document.getElementById('camSub');
  const camProgressFill = document.getElementById('camProgressFill');
  const camSteps = document.getElementById('camSteps');
  const camFallback = document.getElementById('camFallback');

  const DIRECTIONS = [
    { label:'정면을 바라봐주세요', arrow:'●', dir:'center' },
    { label:'고개를 오른쪽으로 천천히 돌려주세요', arrow:'→', dir:'right' },
    { label:'고개를 왼쪽으로 천천히 돌려주세요', arrow:'←', dir:'left' },
    { label:'고개를 위로 들어주세요', arrow:'↑', dir:'up' },
    { label:'고개를 아래로 내려주세요', arrow:'↓', dir:'down' }
  ];
  let stream = null;

  function startCamera(){
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
      navigator.mediaDevices.getUserMedia({ video:{ facingMode:'user' }, audio:false })
        .then(s=>{ stream = s; camVideo.srcObject = s; runSteps(); })
        .catch(showFallback);
    } else {
      showFallback();
    }
  }

  function showFallback(){
    camFallback.style.display = 'block';
    camSub.textContent = '카메라 권한을 확인해주세요';
  }

  document.getElementById('camSkip').addEventListener('click', finishCamera);

  function setScanDirection(dir){
    camScanline.style.animation = 'none';
    camScanline.classList.remove('dir-h','dir-v');
    void camScanline.offsetWidth;
    if(dir === 'up'){ camScanline.classList.add('dir-h'); camScanline.style.animation = 'scan-up 1.7s ease-in-out infinite'; }
    else if(dir === 'down'){ camScanline.classList.add('dir-h'); camScanline.style.animation = 'scan-down 1.7s ease-in-out infinite'; }
    else if(dir === 'right'){ camScanline.classList.add('dir-v'); camScanline.style.animation = 'scan-right 1.7s ease-in-out infinite'; }
    else if(dir === 'left'){ camScanline.classList.add('dir-v'); camScanline.style.animation = 'scan-left 1.7s ease-in-out infinite'; }
    else { camScanline.classList.add('dir-h'); camScanline.style.animation = 'scan-down 2.4s ease-in-out infinite'; }
  }

  function runSteps(){
    let i = 0;
    function step(){
      if(i >= DIRECTIONS.length){ finishCamera(); return; }
      const d = DIRECTIONS[i];
      camSub.textContent = d.label;
      camArrow.textContent = d.arrow;
      camArrow.className = 'cam-arrow dir-' + d.dir;
      setScanDirection(d.dir);
      camSteps.textContent = (i+1) + ' / ' + DIRECTIONS.length;
      camProgressFill.style.transition = 'none';
      camProgressFill.style.width = '0%';
      requestAnimationFrame(()=>{
        camProgressFill.style.transition = 'width 2.9s linear';
        camProgressFill.style.width = '100%';
      });
      i++;
      /* 방향별 안내를 각 1초씩 더 길게 유지해 인식 흐름을 안정적으로 느끼게 함 */
      setTimeout(step, 3000);
    }
    step();
  }

  function finishCamera(){
    if(stream){ stream.getTracks().forEach(t=>t.stop()); }
    camSub.textContent = '촬영이 완료됐어요. 분석을 준비할게요...';
    camArrow.className = 'cam-arrow dir-center';
    camArrow.textContent = '✓';
    camSteps.textContent = '';
    if(state.concerns.size === 0){
      ['scar','pore','oil','acne'].forEach(k=> state.concerns.add(k));
    }
    /* 스캔 직후 바로 결과로 넘기지 않고 로딩 브릿지 → 설문 단계로 이어짐 */
    setTimeout(showLoading, 1200);
  }

  /* ---- 분석 로딩 브릿지 (스캔 → 설문 사이) ---- */
  const LOAD_PHASES = [
    { title:'얼굴 영상을 분석하고 있어요', phase:'피부 이미지를 정합하는 중…' },
    { title:'모공과 피부결을 정밀 스캔 중이에요', phase:'T존·볼 영역을 분석하는 중…' },
    { title:'유분·트러블 분포를 확인하고 있어요', phase:'분석 결과를 정리하는 중…' }
  ];

  function showLoading(){
    camera.classList.remove('visible');
    setTimeout(()=>{
      camera.classList.add('hidden');
      loadScreen.classList.remove('hidden');
      requestAnimationFrame(()=> loadScreen.classList.add('visible'));
      runLoading();
    }, 550);
  }

  function runLoading(){
    const fill = document.getElementById('loadBarFill');
    const title = document.getElementById('loadTitle');
    const phase = document.getElementById('loadPhase');
    let i = 0;
    fill.style.width = '0%';
    function tick(){
      if(i >= LOAD_PHASES.length){ setTimeout(showSurvey, 500); return; }
      const p = LOAD_PHASES[i];
      title.style.opacity = '0';
      setTimeout(()=>{ title.textContent = p.title; title.style.opacity = '1'; }, 200);
      phase.textContent = p.phase;
      fill.style.width = Math.round((i+1)/LOAD_PHASES.length*100) + '%';
      i++;
      setTimeout(tick, 900);
    }
    tick();
  }

  /* ---- 추가 피부 설문 (체감 상태 반영) ---- */
  const SURVEY = [
    { key:'sensitive', q:'평소 피부가 예민한 편인가요?', opts:[
        {v:'high', t:'예민해요', s:'화장품·환경에 쉽게 반응해요'},
        {v:'mid', t:'보통이에요', s:'가끔 반응하는 정도'},
        {v:'low', t:'둔감한 편이에요', s:'거의 반응 없어요'} ]},
    { key:'atopy', q:'아토피나 피부염을 겪은 적 있나요?', opts:[
        {v:'yes', t:'있어요', s:'현재 또는 최근에'},
        {v:'past', t:'예전에요', s:'지금은 괜찮아요'},
        {v:'no', t:'없어요', s:'경험이 없어요'} ]},
    { key:'oil', q:'유분·피지는 어느 정도인가요?', opts:[
        {v:'high', t:'많아요', s:'금방 번들거려요'},
        {v:'mid', t:'보통이에요', s:'T존 위주로 나요'},
        {v:'low', t:'적어요', s:'건조한 편이에요'} ]},
    { key:'dryness', q:'세안 후 피부가 당기고 건조한가요?', opts:[
        {v:'high', t:'심해요', s:'바로 당기고 갈라져요'},
        {v:'mid', t:'조금요', s:'금방 괜찮아져요'},
        {v:'low', t:'없어요', s:'촉촉함이 유지돼요'} ]},
    { key:'trouble', q:'트러블(여드름)은 얼마나 자주 올라오나요?', opts:[
        {v:'high', t:'자주요', s:'거의 항상 있어요'},
        {v:'mid', t:'가끔요', s:'컨디션에 따라'},
        {v:'low', t:'거의 없어요', s:'드물게 올라와요'} ]},
    { key:'redness', q:'붉어짐이나 자극 반응이 잘 생기나요?', opts:[
        {v:'high', t:'잘 생겨요', s:'쉽게 붉어지고 따가워요'},
        {v:'mid', t:'가끔요', s:'특정 상황에서만'},
        {v:'low', t:'거의 없어요', s:'안정적인 편이에요'} ]},
    { key:'focus', q:'가장 신경 쓰이는 피부 고민은?', opts:[
        {v:'trouble', t:'트러블·여드름'},
        {v:'pore', t:'모공·피지'},
        {v:'pigment', t:'색소·잡티'},
        {v:'aging', t:'주름·탄력'},
        {v:'dry', t:'건조·거칢'} ]},
    { key:'goal', q:'원하는 관리 방식은? (복수 선택)', multi:true, opts:[
        {v:'soothe', t:'진정·저자극'},
        {v:'hydrate', t:'수분·보습'},
        {v:'bright', t:'미백·톤업'},
        {v:'pore', t:'모공·피지 조절'},
        {v:'firm', t:'탄력·안티에이징'} ]},
    { key:'current', q:'지금 하고 있는 관리는?', opts:[
        {v:'none', t:'거의 안 해요'},
        {v:'basic', t:'기초만 발라요'},
        {v:'multi', t:'여러 단계 챙겨요'} ]}
  ];
  let svIndex = 0;
  const svQEl = document.getElementById('svQuestion');
  const svOptsEl = document.getElementById('svOpts');
  const svCountEl = document.getElementById('svCount');
  const svProgEl = document.getElementById('svProgress');
  const svBackBtn = document.getElementById('svBack');

  function showSurvey(){
    loadScreen.classList.remove('visible');
    setTimeout(()=>{
      loadScreen.classList.add('hidden');
      surveyScreen.classList.remove('hidden');
      requestAnimationFrame(()=> surveyScreen.classList.add('visible'));
      svIndex = 0;
      state.survey = {};
      renderSurvey();
    }, 500);
  }

  function renderSurvey(){
    const item = SURVEY[svIndex];
    svCountEl.textContent = (svIndex+1) + ' / ' + SURVEY.length;
    svProgEl.style.width = Math.round(svIndex / SURVEY.length * 100) + '%';
    svBackBtn.disabled = svIndex === 0;
    svQEl.textContent = item.q;
    const isGrid = item.opts.every(o=> !o.s);
    const multi = !!item.multi;
    const selected = multi
      ? (Array.isArray(state.survey[item.key]) ? state.survey[item.key] : [])
      : state.survey[item.key];
    svOptsEl.className = 'sv-opts' + (isGrid ? ' grid' : '');
    const optsHtml = item.opts.map(o=>{
      const chosen = multi ? (selected.indexOf(o.v) >= 0) : (selected === o.v);
      return '<button type="button" class="sv-opt' + (chosen?' on':'') + '" data-v="' + o.v + '">' +
        '<span class="sv-opt-txt"><b>' + o.t + '</b>' + (o.s ? '<span>'+o.s+'</span>' : '') + '</span>' +
        '<span class="sv-opt-check"></span>' +
      '</button>';
    }).join('');
    /* 복수 선택 문항은 자동 넘김 대신 '다음' 버튼으로 진행 */
    const nextBtn = multi
      ? '<button type="button" class="sv-next" id="svNext"' + (selected.length ? '' : ' disabled') + '>다음</button>'
      : '';
    svOptsEl.innerHTML = optsHtml + nextBtn;

    svOptsEl.querySelectorAll('.sv-opt').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        if(multi){
          const arr = Array.isArray(state.survey[item.key]) ? state.survey[item.key] : [];
          const v = btn.dataset.v;
          const i = arr.indexOf(v);
          if(i >= 0){ arr.splice(i,1); btn.classList.remove('on'); }
          else { arr.push(v); btn.classList.add('on'); }
          state.survey[item.key] = arr;
          const nb = document.getElementById('svNext');
          if(nb) nb.disabled = arr.length === 0;
        } else {
          state.survey[item.key] = btn.dataset.v;
          svOptsEl.querySelectorAll('.sv-opt').forEach(b=> b.classList.remove('on'));
          btn.classList.add('on');
          setTimeout(nextSurvey, 240);
        }
      });
    });
    const nb = document.getElementById('svNext');
    if(nb) nb.addEventListener('click', ()=>{ if(!nb.disabled) nextSurvey(); });
  }

  function nextSurvey(){
    if(svIndex < SURVEY.length - 1){ svIndex++; renderSurvey(); }
    else { finishSurvey(); }
  }

  svBackBtn.addEventListener('click', ()=>{ if(svIndex > 0){ svIndex--; renderSurvey(); } });

  function finishSurvey(){
    svProgEl.style.width = '100%';
    if(state.concerns.size === 0){
      ['scar','pore','oil','acne'].forEach(k=> state.concerns.add(k));
    }
    /* 영상 분석 + 설문을 함께 반영한 결과를 저장/기록 */
    saveLastResult();
    recordAnalysis();
    if(window.awardPoints){ window.awardPoints('scan'); }   /* 피부 검사 1500P */
    surveyScreen.classList.remove('visible');
    setTimeout(()=>{
      surveyScreen.classList.add('hidden');
      choice.classList.remove('hidden');
      requestAnimationFrame(()=> choice.classList.add('visible'));
    }, 500);
  }

  /* 설문 기반 보정 포인트 / 저자극·진정 모드 판정 (결과·추천 공용) */
  function surveyCorrectionNote(){
    const sv = state.survey || {};
    const pts = [];
    if(sv.sensitive === 'high') pts.push('예민 피부 반영');
    if(sv.atopy === 'yes') pts.push('아토피·피부염 이력 반영');
    if(sv.redness === 'high') pts.push('붉어짐·자극 민감 반영');
    if(sv.dryness === 'high') pts.push('세안 후 건조 보정');
    if(sv.oil === 'high') pts.push('과잉 유분 보정');
    if(sv.trouble === 'high') pts.push('잦은 트러블 보정');
    return pts;
  }
  /* goal은 단일 문자열 또는 복수 선택 배열일 수 있음 */
  function goalHas(sv, v){ const g = sv && sv.goal; return Array.isArray(g) ? g.indexOf(v) >= 0 : g === v; }
  function isSoothingMode(){
    const sv = state.survey || {};
    return sv.sensitive === 'high' || sv.atopy === 'yes' || sv.redness === 'high' || goalHas(sv, 'soothe');
  }
  window.isSoothingMode = isSoothingMode;

  function switchScreen(from, to, delay){
    from.classList.remove('visible');
    setTimeout(()=>{
      from.classList.add('hidden');
      to.classList.remove('hidden');
      requestAnimationFrame(()=> to.classList.add('visible'));
    }, delay || 400);
  }

  document.getElementById('goSimple').addEventListener('click', ()=>{
    renderSimpleResult();
    switchScreen(choice, simpleResult);
    if(window.awardPoints){ window.awardPoints('result'); }   /* 결과 확인 300P */
  });
  document.getElementById('goDetailed').addEventListener('click', ()=>{
    renderDiagnosis();
    switchScreen(choice, diagnosis);
    if(window.awardPoints){ window.awardPoints('result'); }   /* 결과 확인 300P */
  });
  document.getElementById('simpleBack').addEventListener('click', ()=>{
    switchScreen(simpleResult, choice);
  });
  document.getElementById('simpleToRecommend').addEventListener('click', enterApp);

  /* ---------------- 4) diagnosis result ---------------- */
  function clamp10(v){ return Math.max(0.5, Math.min(10, Math.round(v*10)/10)); }

  /* ---- 로그인 회원 정보 기반 비교 기준 라벨 (고정 "20대 남성" 대체) ---- */
  function ageBandLabel(age){
    if(!age || age < 1) return '';
    if(age < 20) return '10대';
    if(age < 30) return '20대';
    if(age < 40) return '30대';
    return '40대 이상';
  }
  function genderWord(g){ return g === 'male' ? '남성' : g === 'female' ? '여성' : ''; }
  function currentGender(){ return (member && member.gender) || state.gender || ''; }
  function peerLabel(){
    const g = genderWord(currentGender());
    const band = ageBandLabel((member && member.age) || state.age || enteredAge);
    if(band && g) return band + ' ' + g;   /* 예: 20대 남성 / 30대 여성 */
    if(band) return band;                   /* 성별 없음 → 동일 연령대 기준 */
    if(g) return g;                          /* 나이 없음 → 성별 기준 */
    return '전체 사용자';                    /* 정보 없음 → 전체 기준 */
  }

  /* ---- 성별에 따라 달라지는 정돈된 얼굴 모델(SVG). 문제 부위 하이라이트는 별도 오버레이 유지 ---- */
  function faceSVG(kind){
    const female = kind === 'female';
    const skinTop = female ? '#fbe3d3' : '#f3d8c2';
    const skinMid = female ? '#f6d2bd' : '#ecc7a9';
    const skinBot = female ? '#eec4aa' : '#dfb595';
    const hairCol = female ? '#4a3327' : '#2f251f';
    const hairHi  = female ? '#6a4c3b' : '#453529';
    const lip     = female ? '#d98784' : '#c48978';
    const cloth   = female ? '#d9cfc4' : '#c9bfb4';
    const browW   = female ? 2.8 : 4;

    const hairBack = female
      ? '<path d="M34 96 C24 54 52 22 92 22 C132 22 160 54 150 96 L156 178 C150 150 146 132 138 120 C142 152 140 180 136 200 L48 200 C44 180 42 152 46 120 C38 132 34 150 28 178 Z" fill="'+hairCol+'"/>'
      : '';
    const hairFront = female
      ? '<path d="M40 94 C36 50 60 26 92 26 C124 26 148 50 144 94 C140 74 132 62 118 57 C120 66 120 74 117 80 C104 62 80 62 67 80 C64 74 64 66 66 57 C52 62 44 74 40 94 Z" fill="'+hairCol+'"/>'
        + '<path d="M92 26 C74 26 62 40 60 56 C72 44 84 42 92 42 Z" fill="'+hairHi+'" opacity=".5"/>'
      : '<path d="M42 98 C36 52 60 28 92 28 C124 28 148 52 142 98 C138 76 132 62 120 56 C124 64 124 72 121 79 C118 66 108 58 92 58 C76 58 66 66 63 79 C60 72 60 64 64 56 C52 62 46 78 42 98 Z" fill="'+hairCol+'"/>'
        + '<path d="M64 56 C74 48 84 46 92 46 C100 46 110 48 120 56 C108 52 96 51 92 51 C88 51 76 52 64 56 Z" fill="'+hairHi+'" opacity=".45"/>';
    const lashes = female
      ? '<path d="M60 108 q11 -6 22 0" stroke="#5a4038" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
        + '<path d="M102 108 q11 -6 22 0" stroke="#5a4038" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
      : '';
    const stubble = kind === 'male'
      ? '<path d="M60 158 C70 186 114 186 124 158 C120 178 108 192 92 192 C76 192 64 178 60 158 Z" fill="#c9a889" opacity=".2"/>'
      : '';
    const lipTop = female ? 9 : 6;
    const lipBot = female ? 5 : 3;

    return '<svg viewBox="0 0 184 224" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
      + '<defs>'
      +   '<linearGradient id="fmSkin" x1="0" y1="0" x2="0" y2="1">'
      +     '<stop offset="0" stop-color="'+skinTop+'"/><stop offset=".55" stop-color="'+skinMid+'"/><stop offset="1" stop-color="'+skinBot+'"/>'
      +   '</linearGradient>'
      +   '<radialGradient id="fmCheek" cx="0.5" cy="0.5" r="0.5">'
      +     '<stop offset="0" stop-color="#e8a184" stop-opacity=".45"/><stop offset="1" stop-color="#e8a184" stop-opacity="0"/>'
      +   '</radialGradient>'
      + '</defs>'
      + '<path d="M26 224 C28 196 56 182 92 182 C128 182 156 196 158 224 Z" fill="'+cloth+'"/>'
      + '<path d="M92 176 c-9 0 -16 3 -16 3 l0 12 q16 9 32 0 l0 -12 s-7 -3 -16 -3z" fill="url(#fmSkin)"/>'
      + hairBack
      + '<ellipse cx="48" cy="120" rx="8" ry="12" fill="url(#fmSkin)"/>'
      + '<ellipse cx="136" cy="120" rx="8" ry="12" fill="url(#fmSkin)"/>'
      + '<path d="M46 104 C46 64 66 40 92 40 C118 40 138 64 138 104 C138 146 120 186 92 190 C64 186 46 146 46 104 Z" fill="url(#fmSkin)"/>'
      + '<ellipse cx="66" cy="132" rx="15" ry="12" fill="url(#fmCheek)"/>'
      + '<ellipse cx="118" cy="132" rx="15" ry="12" fill="url(#fmCheek)"/>'
      + stubble
      + hairFront
      + '<path d="M60 100 q11 -6 22 -1" stroke="#5a4238" stroke-width="'+browW+'" fill="none" stroke-linecap="round"/>'
      + '<path d="M102 99 q11 -5 22 1" stroke="#5a4238" stroke-width="'+browW+'" fill="none" stroke-linecap="round"/>'
      + '<ellipse cx="71" cy="112" rx="7" ry="4" fill="#fff"/><circle cx="71" cy="112" r="2.7" fill="#3a2c24"/>'
      + '<ellipse cx="113" cy="112" rx="7" ry="4" fill="#fff"/><circle cx="113" cy="112" r="2.7" fill="#3a2c24"/>'
      + lashes
      + '<path d="M92 116 L87 140 q5 4 10 0" stroke="#d3a17d" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<path d="M79 160 q13 '+lipTop+' 26 0 q-13 '+lipBot+' -26 0 Z" fill="'+lip+'"/>'
      + '<path d="M79 160 q13 3 26 0" stroke="#b06b63" stroke-width="1.1" fill="none" opacity=".55"/>'
      + '</svg>';
  }
  function renderFaceModel(){
    const g = currentGender();
    const el = document.getElementById('faceModel');
    if(!el) return;
    const male = window.FACE_MALE || '';
    const female = window.FACE_FEMALE || '';
    /* 성별에 맞는 실제 분석 사진 사용. 여성=여자.png, 그 외(남성·미선택)=남자.png */
    const src = g === 'female' ? (female || male) : (male || female);
    /* 여성 사진은 얼굴 위치가 달라 하이라이트 좌표를 .gf 로 보정 */
    const map = el.closest('.face-map') || el.parentElement;
    if(map) map.classList.toggle('gf', g === 'female');
    if(src){
      el.innerHTML = '<img src="' + src + '" alt="AI 피부 분석 얼굴" />';
    } else {
      /* 사진이 없으면 벡터 모델로 폴백 */
      el.innerHTML = faceSVG(g === 'female' ? 'female' : g === 'male' ? 'male' : 'neutral');
    }
  }

  function computeDiagnosis(){
    const c = state.concerns;
    /* 영상 분석 점수에 설문(체감 상태) 보정을 더한다. */
    const sv = state.survey || {};
    const sens = (sv.sensitive === 'high') || (sv.atopy === 'yes');
    return [
      { key:'wrinkle', label:'주름', score: clamp10(8.2 - Math.max(0, enteredAge-25)*0.12 - ((sv.focus==='aging'||goalHas(sv,'firm'))?0.6:0)) },
      { key:'pigment', label:'색소침착', score: clamp10(7.6 - (c.has('scar')?3.4:0) - (sv.focus==='pigment'?0.8:0)) },
      { key:'redness', label:'붉은기', score: clamp10(8.6 - (c.has('acne')?2.2:0) - (c.has('oil')?0.8:0) - (sens?1.8:0) - (sv.redness==='high'?1.2:0)) },
      { key:'pore', label:'모공', score: clamp10(8.0 - (c.has('pore')?5.2:0) - (sv.oil==='high'?0.8:0)) },
      { key:'oil', label:'피지', score: clamp10(7.6 - (c.has('oil')?4.0:0) - (c.has('acne')?1.4:0) - (sv.oil==='high'?1.4:0) + (sv.oil==='low'?0.8:0)) },
      { key:'trouble', label:'트러블', score: clamp10(8.6 - (c.has('acne')?5.0:0) - (c.has('oil')?0.8:0) - (sv.trouble==='high'?1.6:0) + (sv.trouble==='low'?0.6:0)) }
    ];
  }

  function renderDiagnosis(){
    const metrics = computeDiagnosis();
    const overall = metrics.reduce((a,m)=>a+m.score,0) / metrics.length;
    const skinAge = Math.max(18, Math.round(enteredAge + (8-overall)*1.4));
    const worst = metrics.reduce((a,b)=> a.score<b.score?a:b);
    const best = metrics.reduce((a,b)=> a.score>b.score?a:b);
    const skinType = state.concerns.has('oil') ? '지성'
      : (state.concerns.has('pore') || state.concerns.has('scar')) ? '복합성' : '중성';

    document.getElementById('diagAge').innerHTML = skinAge + '<i> 세</i>';
    document.getElementById('diagScoreBig').textContent = Math.round(overall*10);
    document.getElementById('diagPriorityTag').textContent = '우선 관리 · ' + worst.label;
    document.getElementById('diagType').textContent = skinType;
    document.getElementById('diagUserNick').textContent = nickname || '고객';
    document.getElementById('diagDate').textContent = formatToday();

    renderFaceModel();

    document.getElementById('diagSentence').textContent =
      '좋습니다! 당신의 피부 점수는 ' + overall.toFixed(1) + '입니다. 우선 ' + best.label +
      ' 은(는) 관리가 잘 되어 있어요. ' + worst.label + ' 은(는) 좀 더 관리가 필요해요.';

    /* 영상 분석 + 설문 보정 포인트 표시 */
    const noteEl = document.getElementById('diagSurveyNote');
    if(noteEl){
      const pts = surveyCorrectionNote();
      let html = '';
      if(isSoothingMode()){
        html += '<div class="diag-survey-flag">민감·자극 반응이 높아 저자극·진정 중심으로 추천을 조정했어요</div>';
      }
      html += '<div class="diag-survey-title">영상 분석 + 설문 보정 포인트</div>';
      html += pts.length
        ? '<div class="diag-survey-tags">' + pts.map(p=>'<span>'+p+'</span>').join('') + '</div>'
        : '<div class="diag-survey-empty">체감 상태가 안정적이라 영상 분석 결과를 그대로 반영했어요.</div>';
      noteEl.innerHTML = html;
    }

    document.getElementById('diagScoreRows').innerHTML =
      '<div class="score-row overall"><div class="score-row-label">종합</div>' +
        '<div class="score-row-right"><span class="score-row-value">' + Math.round(overall*10) + '</span></div></div>' +
      metrics.map(m=>{
        const band = m.score>=7 ? 'good' : m.score>=4 ? 'mid' : 'bad';
        return '<div class="score-row">' +
          '<div class="score-row-label"><span class="score-row-dot ' + band + '"></span>' + m.label + '</div>' +
          '<div class="score-row-right"><span class="score-row-value">' + Math.round(m.score*10) + '</span>' +
          '<svg class="score-row-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 6l6 6-6 6"/></svg></div>' +
        '</div>';
      }).join('');

    /* 고민 종류 → 얼굴 부위 하이라이트. 범례 칩과 오버레이는 같은 data-concern 키·색으로 연결 */
    const sv = state.survey || {};
    const zoneOn = {
      oil:     state.concerns.has('oil'),
      pore:    state.concerns.has('pore'),
      scar:    state.concerns.has('scar'),
      acne:    state.concerns.has('acne'),
      redness: sv.redness === 'high' || sv.sensitive === 'high' || state.concerns.has('acne')
    };
    document.querySelectorAll('#faceOverlay .fz').forEach(z=>{
      z.classList.toggle('on', !!zoneOn[z.dataset.zone]);
    });
    document.querySelectorAll('.legend-item').forEach(el=>{
      el.classList.toggle('active', !!zoneOn[el.dataset.concern]);
    });

    document.getElementById('diagCta').textContent = '나에게 맞는 제품 찾기';

    renderConcernTabs(metrics);
  }
  window.renderDiagnosis = renderDiagnosis;   /* 데모/테스트 하니스 진입점 */

  /* ---------------- concern detail tabs ---------------- */
  const CONCERN_DETAIL = {
    pore: {
      label:'모공', metricKey:'pore', tag:'pore',
      desc:{
        bad:'모공이 눈에 띄게 넓어져 있어요. 피지와 노폐물이 쌓이기 쉬운 상태라 꾸준한 관리가 필요해요.',
        mid:'모공이 약간 넓어진 편이에요. 지금부터 관리하면 눈에 띄게 좋아질 수 있어요.',
        good:'모공 상태가 양호해요. 지금 루틴을 유지해주세요.'
      },
      tips:['이중세안으로 모공 속 노폐물을 자주 제거해주세요.','뜨거운 물 세안은 피하고 미온수를 사용하세요.','주 1~2회 각질 케어로 모공을 정돈해주세요.']
    },
    oil: {
      label:'유분', metricKey:'oil', tag:'oil',
      desc:{
        bad:'T존을 중심으로 유분이 많이 분비되고 있어요. 번들거림과 트러블로 이어지기 쉬운 상태예요.',
        mid:'유분이 약간 많은 편이에요. 가벼운 제형으로 관리하면 균형을 잡을 수 있어요.',
        good:'유분·수분 밸런스가 좋은 편이에요. 지금 루틴을 유지해주세요.'
      },
      tips:['하루 2회, 약산성 클렌저로 과도한 유분만 부드럽게 제거해주세요.','무거운 크림 대신 가벼운 젤 타입 제형을 사용해보세요.','오후에 유분이 심하면 블로팅 페이퍼로 가볍게 눌러주세요.']
    },
    acne: {
      label:'여드름', metricKey:'trouble', tag:'acne',
      desc:{
        bad:'염증성 트러블이 반복되고 있어요. 자극을 줄이고 원인균 관리가 필요한 상태예요.',
        mid:'가끔 트러블이 올라오는 편이에요. 초기에 진정시켜주면 흉터로 남는 걸 줄일 수 있어요.',
        good:'트러블이 잘 관리되고 있어요. 지금 상태를 유지해주세요.'
      },
      tips:['손으로 만지거나 짜지 말고 진정 성분으로 케어해주세요.','베개 커버, 마스크 등 피부에 닿는 물건을 자주 세척해주세요.','트러블 부위엔 저자극 스팟 제품을 사용해보세요.']
    },
    scar: {
      label:'흉터', metricKey:'pigment', tag:'scar',
      desc:{
        bad:'흉터·색소 자국이 두드러져 피부결이 고르지 않은 상태예요. 꾸준한 진정·재생 관리가 필요해요.',
        mid:'옅은 자국이 남아있어요. 꾸준히 관리하면 결이 점점 매끈해질 수 있어요.',
        good:'흉터·색소 부담이 적은 편이에요. 지금 루틴을 유지해주세요.'
      },
      tips:['자외선 차단제를 매일 발라 색소 자국이 짙어지는 걸 막아주세요.','브라이트닝 성분(나이아신아마이드 등)을 꾸준히 사용해보세요.','새로 생긴 트러블은 짜지 않아야 흉터로 남지 않아요.']
    }
  };
  const CONCERN_ORDER = ['pore','oil','acne','scar'];

  function renderConcernTabs(metrics){
    const byKey = {};
    metrics.forEach(m=> byKey[m.key] = m);

    const active = CONCERN_ORDER.filter(k=> state.concerns.has(k));
    const pool = active.length ? active : CONCERN_ORDER;
    let defaultKey = pool[0];
    let lowest = 11;
    pool.forEach(k=>{
      const score = byKey[CONCERN_DETAIL[k].metricKey].score;
      if(score < lowest){ lowest = score; defaultKey = k; }
    });

    const tabsEl = document.getElementById('diagTabs');
    const panelsEl = document.getElementById('diagPanels');

    tabsEl.innerHTML = CONCERN_ORDER.map(k=>{
      const m = byKey[CONCERN_DETAIL[k].metricKey];
      const band = m.score>=7?'good':m.score>=4?'mid':'bad';
      return '<button type="button" class="diag-tab' + (k===defaultKey?' active':'') + '" data-tab="' + k + '">' +
        '<span class="tab-dot" style="background:var(--' + band + ')"></span>' +
        CONCERN_DETAIL[k].label +
      '</button>';
    }).join('');

    panelsEl.innerHTML = CONCERN_ORDER.map(k=>{
      const detail = CONCERN_DETAIL[k];
      const m = byKey[detail.metricKey];
      const band = m.score>=7?'good':m.score>=4?'mid':'bad';
      const bandText = band==='good'?'좋음':band==='mid'?'보통':'나쁨';
      const descText = detail.desc[band];
      /* 상세 분석 페이지에서는 제품을 추천하지 않고 상태·관리 팁만 보여준다.
         제품은 '나에게 맞는 제품 찾기'로 넘어간 다음 페이지에서 확인. */
      return '<div class="diag-panel' + (k===defaultKey?' active':'') + '" data-panel="' + k + '">' +
        '<div class="panel-head">' +
          '<span class="panel-title">' + detail.label + ' · ' + m.score.toFixed(1) + '점</span>' +
          '<span class="panel-badge ' + band + '">' + bandText + '</span>' +
        '</div>' +
        '<div class="panel-score-track"><div class="panel-score-fill fill-' + band + '" style="width:' + (m.score*10) + '%"></div></div>' +
        '<p class="panel-desc">' + descText + '</p>' +
        '<div class="panel-tips">' +
          '<div class="panel-tips-title">관리 팁</div>' +
          '<ul>' + detail.tips.map(t=>'<li>'+t+'</li>').join('') + '</ul>' +
        '</div>' +
      '</div>';
    }).join('');

    tabsEl.querySelectorAll('.diag-tab').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        tabsEl.querySelectorAll('.diag-tab').forEach(b=>b.classList.remove('active'));
        panelsEl.querySelectorAll('.diag-panel').forEach(p=>p.classList.remove('active'));
        btn.classList.add('active');
        panelsEl.querySelector('[data-panel="' + btn.dataset.tab + '"]').classList.add('active');
      });
    });
  }

  document.getElementById('diagCta').addEventListener('click', enterApp);
  document.getElementById('diagBack').addEventListener('click', ()=> switchScreen(diagnosis, choice));

  function enterApp(){
    const active = diagnosis.classList.contains('visible') ? diagnosis : simpleResult;
    active.classList.remove('visible');
    setTimeout(()=>{
      diagnosis.classList.add('hidden');
      simpleResult.classList.add('hidden');
      const greet = document.getElementById('heroGreet');
      if(greet && nickname){ greet.textContent = nickname + '님, '; }
      state.analyzed = true;
      recordRecommend();
      appScreen.style.display = 'block';
      if(window.showAppStep){ window.showAppStep('recommend'); }
      window.scrollTo(0,0);
    }, 550);
  }

  /* ---------------- 5) simple result (radar) ---------------- */
  function formatToday(){
    const d = new Date();
    const pad = n => String(n).padStart(2,'0');
    return d.getFullYear() + '.' + pad(d.getMonth()+1) + '.' + pad(d.getDate());
  }

  function polarPoint(cx, cy, r, angleDeg){
    const rad = (angleDeg - 90) * Math.PI / 180;
    return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
  }

  function renderRadar(metrics){
    const size = 250, cx = 125, cy = 125, maxR = 88;
    const step = 360 / metrics.length;

    const rings = [0.33, 0.66, 1].map(f=>{
      const pts = metrics.map((_, i)=>{
        const p = polarPoint(cx, cy, maxR*f, i*step);
        return p.x.toFixed(1) + ',' + p.y.toFixed(1);
      }).join(' ');
      return '<polygon points="' + pts + '" class="radar-ring" />';
    }).join('');

    const axisLines = metrics.map((_, i)=>{
      const p = polarPoint(cx, cy, maxR, i*step);
      return '<line x1="' + cx + '" y1="' + cy + '" x2="' + p.x.toFixed(1) + '" y2="' + p.y.toFixed(1) + '" class="radar-axis" />';
    }).join('');

    const dataPts = metrics.map((m, i)=> polarPoint(cx, cy, maxR * (m.score/10), i*step));
    const dataPolygon = dataPts.map(p=> p.x.toFixed(1) + ',' + p.y.toFixed(1)).join(' ');
    const dataDots = dataPts.map(p=> '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="3.2" class="radar-dot" />').join('');

    const svg = '<svg viewBox="0 0 ' + size + ' ' + size + '" class="radar-svg">' +
      rings + axisLines +
      '<polygon points="' + dataPolygon + '" class="radar-shape" />' +
      dataDots +
    '</svg>';

    const labels = metrics.map((m, i)=>{
      const p = polarPoint(cx, cy, maxR * 1.36, i*step);
      const leftPct = (p.x / size * 100).toFixed(1);
      const topPct = (p.y / size * 100).toFixed(1);
      const band = m.score >= 7 ? 'good' : m.score >= 4 ? 'mid' : 'bad';
      const bandText = m.score >= 7 ? '충분' : m.score >= 4 ? '보통' : '부족';
      return '<div class="radar-label" style="left:' + leftPct + '%;top:' + topPct + '%;">' +
        '<span class="radar-badge ' + band + '">' + bandText + '</span>' +
        '<b>' + m.label + '</b><span class="radar-pct">' + Math.round(m.score*10) + '%</span>' +
      '</div>';
    }).join('');

    return '<div class="radar-wrap">' + svg + labels + '</div>';
  }

  function renderSimpleResult(){
    const metrics = computeDiagnosis();
    const overall10 = metrics.reduce((a,m)=>a+m.score,0) / metrics.length;
    const scorePct = Math.round(overall10 * 10);
    const tier = scorePct >= 80 ? '상위 10%' : scorePct >= 60 ? '중상위 20%' : scorePct >= 40 ? '중위 40%' : '하위 30%';
    const cmpAll = Math.max(3, Math.min(90, 100 - scorePct + 5));
    const cmpAge = Math.max(3, Math.min(90, 100 - scorePct - 3));

    document.getElementById('simpleDate').textContent = formatToday();
    document.getElementById('simpleNameTitle').textContent = (nickname || '고객') + '님의 피부 분석 리포트';
    document.getElementById('simpleScore').textContent = scorePct;
    document.getElementById('simpleTier').textContent = tier + '의 점수예요';
    document.getElementById('cmpAll').textContent = cmpAll + '%';
    const peerEl = document.getElementById('cmpAgeLabel');
    if(peerEl) peerEl.textContent = peerLabel();
    document.getElementById('cmpAge').textContent = cmpAge + '%';

    const ssEl = document.getElementById('simpleSurveyNote');
    if(ssEl){
      const pts = surveyCorrectionNote();
      let html = '';
      if(isSoothingMode()){ html += '<div class="ss-flag">저자극·진정 중심 추천</div>'; }
      html += pts.slice(0,3).map(p=>'<span class="ss-tag">'+p+'</span>').join('');
      ssEl.innerHTML = html;
    }

    document.getElementById('radarHolder').innerHTML = renderRadar(metrics);
  }
})();
</script>

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
  const state = window.appState;

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
      if(window.persistAnalysis){ window.persistAnalysis(); }
      if(window.awardPoints){ window.awardPoints('scan'); window.awardPoints('result'); }  /* 검사·결과 확인 포인트 */
    }, 1400);
  });

  const toRecoBtn = document.getElementById('toRecommend');
  if(toRecoBtn){ toRecoBtn.addEventListener('click', ()=>{ if(window.recordRecommend){ window.recordRecommend(); } }); }

  /* '최근 분석 결과 다시 보기' 진입점: 저장된 state.concerns 기준으로
     칩 UI를 동기화하고 결과를 즉시 렌더링한다(분석 로딩 없이 바로 표시). */
  window.showAnalysisResult = function(){
    chipRow.querySelectorAll('.chip').forEach(chip=>{
      const key = chip.dataset.key;
      const on = state.concerns.has(key);
      chip.classList.toggle('active', on);
      chip.innerHTML = (on ? CHECK_SVG : '') + CONCERNS[key].label;
    });
    hintEl.textContent = '';
    loadingEl.classList.remove('show');
    renderResult(computeMetrics());
    resultEl.classList.add('show');
    state.analyzed = true;
  };

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

  /* ---------------- step navigation (hero/analysis/recommend/extra/community/rewards) ---------------- */
  const APP_STEPS = ['hero','analysis','recommend','style','extra','community','rewards'];
  const STEP_EL = {
    hero: document.getElementById('stepHero'),
    analysis: document.getElementById('analysis'),
    recommend: document.getElementById('recommend'),
    style: document.getElementById('style'),
    extra: document.getElementById('extra'),
    community: document.getElementById('community'),
    rewards: document.getElementById('rewards')
  };
  let currentStep = 'hero';

  function showAppStep(name){
    if(!STEP_EL[name]) return;
    currentStep = name;
    APP_STEPS.forEach(s=> STEP_EL[s].classList.toggle('active', s===name));
    document.querySelectorAll('[data-step-dots]').forEach(dotsWrap=>{
      dotsWrap.innerHTML = APP_STEPS.map(s=>'<span class="step-dot' + (s===name?' active':'') + '"></span>').join('');
    });
    /* 현재 페이지에 해당하는 상단 메뉴 강조 */
    document.querySelectorAll('.nav-links a[data-step]').forEach(a=>
      a.classList.toggle('active', a.dataset.step === name));
    window.scrollTo(0,0);
    if(name === 'recommend' && !tierInitialized){ initTierTabs(); }
    if(name === 'style' && !styleInitialized){ initStyle(); }
    if(name === 'extra' && !extraInitialized){ initExtraTabs(); }
  }
  window.showAppStep = showAppStep;

  /* 개별 바인딩 대신 문서 위임: 나중에 추가되는 [data-step] 요소도 항상 동작하고,
     앵커 기본 이동(#)을 막아 iframe 환경에서도 안전하게 전환된다. */
  document.addEventListener('click', e=>{
    const el = e.target.closest('[data-step]');
    if(!el) return;
    e.preventDefault();
    showAppStep(el.dataset.step);
  });
  document.querySelectorAll('[data-step-next]').forEach(el=>{
    el.addEventListener('click', ()=>{
      const i = APP_STEPS.indexOf(currentStep);
      if(i < APP_STEPS.length-1){ showAppStep(APP_STEPS[i+1]); }
    });
  });
  document.querySelectorAll('[data-step-prev]').forEach(el=>{
    el.addEventListener('click', ()=>{
      const i = APP_STEPS.indexOf(currentStep);
      if(i > 0){ showAppStep(APP_STEPS[i-1]); }
    });
  });
  document.querySelectorAll('[data-step-loop]').forEach(el=>{
    el.addEventListener('click', ()=> showAppStep('hero'));
  });
  showAppStep('hero');

  /* ---------------- reward missions (포인트 적립) ---------------- */
  const REWARD_MISSIONS = [
    { key:'signup', label:'회원가입하고', short:'회원가입', amount:500,  tip:'가입 후 바로 포인트가 지급됩니다' },
    { key:'scan',   label:'피부 검사하고', short:'피부 검사', amount:1500, tip:'피부 상태를 분석하면 포인트를 받을 수 있습니다' },
    { key:'result', label:'결과 확인하고', short:'결과 확인', amount:300,  tip:'진단 결과 확인 후 포인트가 적립됩니다' }
  ];
  const REWARD_KEY = 'forhim_rewards';
  function loadRewards(){ try{ return JSON.parse(localStorage.getItem(REWARD_KEY) || '{"total":0,"done":{}}'); }catch(e){ return {total:0, done:{}}; } }
  let rewards = loadRewards();
  function saveRewards(){ try{ localStorage.setItem(REWARD_KEY, JSON.stringify(rewards)); }catch(e){} }
  function rewardToast(msg){
    const t = document.getElementById('toast'); if(!t) return;
    t.textContent = msg; t.classList.add('show');
    setTimeout(()=> t.classList.remove('show'), 2200);
  }
  function renderRewards(){
    const totalEl = document.getElementById('rewardTotal');
    if(totalEl) totalEl.textContent = (rewards.total || 0).toLocaleString();
    const wrap = document.getElementById('rewardMissions');
    if(!wrap) return;
    wrap.innerHTML = REWARD_MISSIONS.map(m=>{
      const done = !!(rewards.done && rewards.done[m.key]);
      const inner = done
        ? m.short + ' <span class="rw-p">' + m.amount + 'P</span> 적립 완료 ✓'
        : m.label + ' <span class="rw-p">' + m.amount + 'P</span> 받기';
      return '<div class="reward-mission">' +
        '<div class="rw-tip">' + m.tip + '</div>' +
        '<button type="button" class="rw-btn' + (done?' done':'') + '" data-mission="' + m.key + '"' + (done?' disabled':'') + '>' +
          '<span>' + inner + '</span>' +
        '</button>' +
      '</div>';
    }).join('');
    wrap.querySelectorAll('.rw-btn').forEach(btn=>{
      btn.addEventListener('click', ()=> missionClick(btn.dataset.mission));
    });
  }
  function awardPoints(key){
    const m = REWARD_MISSIONS.find(x=> x.key === key);
    if(!m) return;
    if(!rewards.done) rewards.done = {};
    if(rewards.done[key]) return;              /* 이미 적립됨 → 중복 지급 방지 */
    rewards.done[key] = true;
    rewards.total = (rewards.total || 0) + m.amount;
    saveRewards();
    renderRewards();
    rewardToast(m.amount + 'P 적립 완료');
  }
  function missionClick(key){
    if(rewards.done && rewards.done[key]) return;
    if(key === 'signup'){ if(window.rewardGoSignup){ window.rewardGoSignup(); } }
    else { showAppStep('analysis'); }          /* 피부 검사·결과 확인 → 분석 단계로 유도 */
  }
  window.awardPoints = awardPoints;
  renderRewards();

  /* ---------------- style guide (TPO 상황별 추천 + 스타일 피드) ---------------- */
  let styleInitialized = false;
  const TPO = {
    date:      { label:'소개팅',    emoji:'💗' },
    interview: { label:'면접',      emoji:'💼' },
    work:      { label:'출근',      emoji:'🏢' },
    weekend:   { label:'주말 약속', emoji:'🌤️' }
  };
  const TPO_ORDER = ['date','interview','work','weekend'];
  const TPO_LOOKS = {
    date: {
      male:{ impression:['부드러운 첫인상','청결','신뢰'],
        skin:'유분·번들거림을 잡아 매트하고 깨끗한 인상. 만나기 30분 전 가벼운 수분만 더하세요.',
        cosmetics:['메디힐 마데카소사이드 선세럼','정샘물 에센셜 스킨 누더 쿠션','아누아 어성초 토너'],
        routine:[
          {k:'skin', step:'스킨케어', d:'유분·번들거림부터 정리', items:['아누아 어성초 77 토너','메디힐 마데카소사이드 수분 선세럼']},
          {k:'base', step:'피부 표현', d:'얇게 한 겹, 깨끗한 톤 정돈', items:['정샘물 에센셜 스킨 누더 쿠션']},
          {k:'brow', step:'눈썹·마무리', d:'눈썹만 정리해도 인상이 달라져요', items:['클리오 킬브로우 오토 하드 브로우 펜슬']}
        ],
        extras:[
          {label:'립·수분 마무리', items:['립밤으로 입술 각질 정돈','메디큐브 PDRN 핑크 미스트 — 만나기 직전 수분 보충']},
          {label:'향', items:['포레 우디 머스크 오 드 퍼퓸 — 손목·목에 1~2회만 가볍게']}
        ],
        outfit:{main:'화이트 셔츠 + 베이지 슬랙스', sub:'깔끔한 컬러로 부담 없는 호감형'},
        hair:{main:'내추럴 덮머리', sub:'다운펌으로 자연스럽게'} },
      female:{ impression:['화사','생기','다정'],
        skin:'수분+비타C로 화사하게. 은은한 톤업으로 생기 있는 인상을 만드세요.',
        cosmetics:['토리든 다이브인 세럼','구달 청귤 비타C 세럼','클리오 킬커버 쿠션'],
        routine:[
          {k:'skin', step:'스킨케어', d:'수분과 비타민으로 화사한 바탕', items:['토리든 다이브인 저분자 히알루론산 세럼','구달 청귤 비타C 잡티 세럼']},
          {k:'base', step:'피부 표현', d:'은은한 톤업으로 생기 있게', items:['클리오 킬커버 파운웨어 쿠션']},
          {k:'point', step:'포인트·마무리', d:'입술에 생기만 살짝', items:['페리페라 틴트']}
        ],
        extras:[
          {label:'아이 메이크업', items:['루미르 라이트 온 아이즈 섀도우 팔레트 — 은은한 음영만']},
          {label:'향', items:['탬버린즈 베르가못 시트러스 오 드 퍼퓸']}
        ],
        outfit:{main:'아이보리 니트 + 연핑크 스커트', sub:'부드러운 파스텔로 다정한 무드'},
        hair:{main:'웨이브 반묶음', sub:'얼굴 라인을 부드럽게'} }
    },
    interview: {
      male:{ impression:['단정','신뢰','프로페셔널'],
        skin:'톤 정리 + 자연스러운 커버로 또렷하고 신뢰감 있는 인상.',
        cosmetics:['에스트라 아토베리어365 크림','헤라 블랙 쿠션','코스알엑스 6 펩타이드 세럼'],
        routine:[
          {k:'skin', step:'스킨케어', d:'결 정돈과 장벽 케어로 안정감 있게', items:['코스알엑스 더 6 펩타이드 스킨 부스터 세럼','에스트라 아토베리어365 크림']},
          {k:'base', step:'피부 표현', d:'번들거림 없는 커버로 신뢰감', items:['헤라 블랙 쿠션 파운데이션']},
          {k:'brow', step:'눈썹·마무리', d:'또렷한 눈썹으로 단정하게', items:['클리오 킬브로우 오토 하드 브로우 펜슬']}
        ],
        extras:[
          {label:'헤어 세팅', items:['매트 왁스로 이마 오픈 고정','스프레이로 잔머리 정리']},
          {label:'마무리 점검', items:['니베아 프레시 액티브 데오 롤온','그랑핸드 뉴트럴 오 드 퍼퓸 — 아주 가볍게 1회']}
        ],
        outfit:{main:'네이비 자켓 + 화이트 셔츠', sub:'기본에 충실한 신뢰형 조합'},
        hair:{main:'깐머리 (이마 오픈)', sub:'단정하게 넘겨 프로페셔널하게'} },
      female:{ impression:['단정','또렷','프로페셔널'],
        skin:'번들거림 없는 깔끔한 피부 표현 + 또렷한 눈썹으로 신뢰감 있는 인상.',
        cosmetics:['에스트라 아토베리어365 크림','클리오 킬커버 쿠션','클리오 킬브로우 펜슬'],
        routine:[
          {k:'skin', step:'스킨케어', d:'장벽 케어로 들뜸 없이', items:['에스트라 아토베리어365 크림']},
          {k:'base', step:'피부 표현', d:'깔끔한 커버로 단정하게', items:['클리오 킬커버 파운웨어 쿠션']},
          {k:'brow', step:'눈썹·마무리', d:'또렷한 눈썹으로 신뢰감', items:['클리오 킬브로우 오토 하드 브로우 펜슬']}
        ],
        extras:[
          {label:'헤어 세팅', items:['로우 포니테일 — 잔머리는 스프레이로 정리']}
        ],
        outfit:{main:'네이비 자켓 + 화이트 블라우스', sub:'클래식한 오피스 무드'},
        hair:{main:'로우 포니테일', sub:'깔끔하게 넘겨 단정하게'} }
    },
    work: {
      male:{ impression:['깔끔','부지런','호감'],
        skin:'빠른 아침 루틴 — 수분·선케어로 하루 컨디션을 유지하세요.',
        cosmetics:['AHC 마스터즈 선스틱','토리든 다이브인 세럼','라운드랩 1025 독도 로션'],
        routine:[
          {k:'skin', step:'스킨케어', d:'아침 3분, 수분부터 채우고', items:['토리든 다이브인 저분자 히알루론산 세럼','라운드랩 1025 독도 로션']},
          {k:'sun', step:'선케어', d:'출근길 자외선 차단은 필수', items:['AHC 마스터즈 에어 리치 선스틱']},
          {k:'hair', step:'헤어·마무리', d:'가볍게 정돈하고 출발', items:['드라이 1분으로 덮머리 정돈']}
        ],
        extras:[
          {label:'오후 컨디션 케어', items:['메디큐브 PDRN 핑크 미스트 — 오후 수분 보충','니베아 프레시 액티브 데오 롤온']}
        ],
        outfit:{main:'그레이 니트 + 화이트 이너', sub:'단정하지만 편한 데일리'},
        hair:{main:'가벼운 덮머리', sub:'힘 뺀 자연스러운 스타일'} },
      female:{ impression:['깔끔','생기','프로'],
        skin:'가벼운 수분 + 톤업 선크림으로 산뜻하게.',
        cosmetics:['구달 어성초 진정 선크림','토리든 다이브인 세럼','정샘물 쿠션'],
        routine:[
          {k:'skin', step:'스킨케어', d:'가벼운 수분으로 산뜻하게', items:['토리든 다이브인 저분자 히알루론산 세럼']},
          {k:'sun', step:'선케어', d:'톤업 겸 자외선 차단', items:['구달 맑은 어성초 진정 수분 선크림']},
          {k:'base', step:'피부 표현', d:'얇게 톤만 정돈', items:['정샘물 에센셜 스킨 누더 쿠션']}
        ],
        extras:[
          {label:'마무리', items:['로우 번으로 단정하게','립밤으로 생기 유지']}
        ],
        outfit:{main:'베이지 가디건 + 슬랙스', sub:'편안한 오피스 캐주얼'},
        hair:{main:'로우 번', sub:'단정한 하루용 스타일'} }
    },
    weekend: {
      male:{ impression:['편안','트렌디','자연스러움'],
        skin:'가볍게 수분+톤업, 힘 뺀 무드로 자연스럽게.',
        cosmetics:['구달 어성초 진정 선크림','메디큐브 PDRN 핑크 미스트','정샘물 쿠션(가볍게)'],
        routine:[
          {k:'skin', step:'스킨케어', d:'가볍게 수분만 채우고', items:['메디큐브 PDRN 핑크 콜라겐 젤리 미스트 세럼']},
          {k:'sun', step:'선케어', d:'외출 전 진정 겸 차단', items:['구달 맑은 어성초 진정 수분 선크림']},
          {k:'base', step:'피부 표현', d:'쿠션은 힘 빼고 얇게', items:['정샘물 에센셜 스킨 누더 쿠션 — 가볍게']}
        ],
        extras:[
          {label:'무드 마무리', items:['내추럴 애즈펌 볼륨 정돈','탬버린즈 베르가못 시트러스 오 드 퍼퓸 — 캐주얼하게']}
        ],
        outfit:{main:'블랙 후드 + 데님', sub:'꾸안꾸 캐주얼'},
        hair:{main:'내추럴 애즈펌', sub:'자연스러운 볼륨'} },
      female:{ impression:['편안','러블리','자연스러움'],
        skin:'수분 위주의 가벼운 피부 표현으로 촉촉한 무드.',
        cosmetics:['토리든 다이브인 세럼','메디큐브 PDRN 핑크 미스트','페리페라 틴트'],
        routine:[
          {k:'skin', step:'스킨케어', d:'촉촉한 바탕부터', items:['토리든 다이브인 저분자 히알루론산 세럼','메디큐브 PDRN 핑크 콜라겐 젤리 미스트 세럼']},
          {k:'base', step:'피부 표현', d:'수분감 살려 가볍게', items:['정샘물 에센셜 스킨 누더 쿠션 — 얇게']},
          {k:'point', step:'포인트·마무리', d:'입술로 러블리하게', items:['페리페라 틴트']}
        ],
        extras:[
          {label:'무드 마무리', items:['로우 웨이브로 자연스럽게','그랑핸드 뉴트럴 오 드 퍼퓸']}
        ],
        outfit:{main:'니트 + 데님', sub:'편안한 데이트 룩'},
        hair:{main:'로우 웨이브', sub:'자연스럽게 풀어서'} }
    }
  };
  /* 상황(TPO)별 스타일 피드 카드 세트 — 탭 전환 시 해당 상황 카드로 전체 교체.
     visual: 착장 합성(outfit)·사진 톤(filter)·크롭(pos), outfitText/hairText: 카드별 착장·헤어 설명 오버라이드.
     window.LOOK_IMGS 에 look_<id>.png 실사 에셋이 있으면 그 이미지를 우선 사용(합성 생략). */
  /* markers: 첨부된 최종 촬영 세트 기준 카드별 번호 위치(% 좌표) — look_<id>.png 크롭과 짝을 이룬다 */
  const STYLE_FEED = [
    /* 소개팅 */
    { id:'f1', sit:'date', gender:'male', title:'소개팅 클린 룩',
      visual:{ outfit:'shirt', c:{main:'#c9ddf0', line:'#8fb3d4'}, filter:'brightness(1.06) saturate(1.08)', pos:'center 16%' },
      markers:[{t:19, l:48}, {t:52, l:36}, {t:20, l:76}],
      outfitText:{main:'라이트 블루 셔츠', sub:'밝고 호감 가는 첫인상'}, hairText:'내추럴 덮머리' },
    { id:'f2', sit:'date', gender:'female', title:'소개팅 화사 룩',
      visual:{ outfit:'blouse', c:{main:'#efe6d8', line:'#d9c9b2'}, filter:'brightness(1.07) saturate(1.1) sepia(.05)', pos:'center 14%' },
      markers:[{t:31, l:70}, {t:52, l:72}, {t:58, l:60}],
      outfitText:{main:'아이보리 니트 블라우스', sub:'부드러운 파스텔 무드'}, hairText:'웨이브 반묶음' },
    { id:'f3', sit:'date', gender:'male', title:'소개팅 세미 캐주얼 룩',
      visual:{ outfit:'cardigan', c:{main:'#d8cbb6', line:'#c0ae92'}, filter:'brightness(1.04) sepia(.06)', pos:'center 20%' },
      markers:[{t:19, l:45}, {t:49, l:42}, {t:20, l:78}],
      outfitText:{main:'베이지 가디건 + 화이트 이너', sub:'편안하지만 정돈된 분위기'}, hairText:'내추럴 가르마' },
    /* 면접 */
    { id:'f4', sit:'interview', gender:'male', title:'면접 신뢰 룩',
      visual:{ outfit:'suit', c:{main:'#2e3a52', line:'#222b3e', shirt:'#f6f7f9', tie:'#5f7396'}, filter:'contrast(1.05) saturate(.9)', pos:'center 22%' },
      markers:[{t:40, l:57}, {t:48, l:26}, {t:29, l:33}],
      outfitText:{main:'네이비 수트 + 타이', sub:'기본에 충실한 신뢰형'}, hairText:'사이드 파트(가르마 깐머리)' },
    { id:'f5', sit:'interview', gender:'female', title:'면접 단정 룩',
      visual:{ outfit:'suit', c:{main:'#3a3f4a', line:'#2b2f38', shirt:'#f6f7f9', tie:''}, filter:'contrast(1.04) saturate(.88)', pos:'center 16%' },
      markers:[{t:42, l:64}, {t:51, l:38}, {t:29, l:39}],
      outfitText:{main:'차콜 블레이저 + 화이트 블라우스', sub:'클래식 오피스 무드'}, hairText:'로우 포니테일' },
    { id:'f6', sit:'interview', gender:'male', title:'면접 비즈 캐주얼 룩',
      visual:{ outfit:'shirt', c:{main:'#dfe3e8', line:'#b6bec9'}, filter:'saturate(.94) brightness(1.03)', pos:'center 18%' },
      markers:[{t:43, l:62}, {t:55, l:36}, {t:33, l:38}],
      outfitText:{main:'그레이 셔츠 (노타이)', sub:'단정하지만 딱딱하지 않게'}, hairText:'사이드 정돈' },
    /* 출근 */
    { id:'f7', sit:'work', gender:'male', title:'데일리 출근 룩',
      visual:{ outfit:'knit', c:{main:'#9aa3ad', line:'#7f8894'}, filter:'saturate(.88) brightness(1.02)', pos:'center 20%' },
      markers:[{t:42, l:52}, {t:32, l:50}, {t:19, l:56}],
      outfitText:{main:'그레이 니트 + 화이트 이너', sub:'단정하지만 편한 데일리'}, hairText:'가벼운 덮머리' },
    { id:'f8', sit:'work', gender:'female', title:'출근 산뜻 룩',
      visual:{ outfit:'cardigan', c:{main:'#e2d5c2', line:'#c9b699'}, filter:'brightness(1.05) sepia(.04)', pos:'center 15%' },
      markers:[{t:47, l:62}, {t:33, l:52}, {t:58, l:45}],
      outfitText:{main:'베이지 가디건 + 슬랙스', sub:'편안한 오피스 캐주얼'}, hairText:'로우 번' },
    { id:'f9', sit:'work', gender:'male', title:'출근 셔츠 룩',
      visual:{ outfit:'shirt', c:{main:'#5b6b85', line:'#465471'}, filter:'saturate(.95) contrast(1.03)', pos:'center 22%' },
      markers:[{t:47, l:55}, {t:33, l:55}, {t:22, l:57}],
      outfitText:{main:'네이비 셔츠', sub:'차분하고 신뢰감 있는 톤'}, hairText:'단정한 사이드 파트' },
    /* 주말 약속 */
    { id:'f10', sit:'weekend', gender:'male', title:'주말 캐주얼 룩',
      visual:{ outfit:'hoodie', c:{main:'#2b2b2e', line:'#1e1e21', string:'#8f8f95'}, filter:'saturate(1.14) contrast(1.03)', pos:'center 26%' },
      markers:[{t:48, l:62}, {t:33, l:50}, {t:58, l:42}],
      outfitText:{main:'블랙 후드 + 데님', sub:'꾸안꾸 캐주얼'}, hairText:'내추럴 애즈펌' },
    { id:'f11', sit:'weekend', gender:'female', title:'주말 데이트 룩',
      visual:{ outfit:'blouse', c:{main:'#d9c9b2', line:'#c4b096'}, filter:'brightness(1.04) sepia(.08) saturate(1.05)', pos:'center 16%' },
      markers:[{t:53, l:62}, {t:68, l:52}, {t:56, l:47}],
      outfitText:{main:'베이지 보트넥 니트', sub:'편안한 데이트 무드'}, hairText:'로우 웨이브' },
    { id:'f12', sit:'weekend', gender:'male', title:'주말 액티브 룩',
      visual:{ outfit:'henley', c:{main:'#2e3440', line:'#232834'}, filter:'saturate(1.08) contrast(1.04)', pos:'center 24%' },
      markers:[{t:47, l:68}, {t:33, l:62}, {t:60, l:55}],
      outfitText:{main:'다크 네이비 헨리넥', sub:'관리된 캐주얼'}, hairText:'가볍게 올린 앞머리' }
  ];
  /* 착장 합성 SVG — 2층 구조로 '입고 있는' 느낌을 만든다.
     · blend 레이어(멀티플라이): 옷 몸판 색이 사진과 곱해져 원본 티셔츠의 실제 주름·음영이
       원단 위로 그대로 비친다 → 얹힌 색면이 아니라 입은 옷처럼 보임
     · top 레이어(불투명): 카라·타이·단추·트임 등 디테일 — 멀티플라이로 사라지지 않게 위에 얹음
     uid: 카드마다 그라디언트 id가 겹치지 않게 하는 접미사 */
  function outfitSvg(v, uid){
    if(!v || !v.outfit) return '';
    const c = v.c || {};
    const main = c.main || '#dfe4ea', line = c.line || 'rgba(0,0,0,.18)';
    const gid = 'og' + (uid || '0');
    const svgOpen = cls => '<svg class="feed-outfit ' + cls + '" viewBox="0 0 100 46" preserveAspectRatio="none" aria-hidden="true">';
    const close = '</svg>';
    const defs =
      '<defs><linearGradient id="'+gid+'" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#ffffff" stop-opacity=".14"/>' +
        '<stop offset=".45" stop-color="#ffffff" stop-opacity="0"/>' +
        '<stop offset="1" stop-color="#000000" stop-opacity=".12"/>' +
      '</linearGradient>' +
      '<linearGradient id="'+gid+'s" x1="0" y1="0" x2="1" y2="0">' +
        '<stop offset="0" stop-color="#000000" stop-opacity=".10"/>' +
        '<stop offset=".2" stop-color="#000000" stop-opacity="0"/>' +
        '<stop offset=".8" stop-color="#000000" stop-opacity="0"/>' +
        '<stop offset="1" stop-color="#000000" stop-opacity=".10"/>' +
      '</linearGradient></defs>';
    /* 몸판(블렌드 레이어): 실루엣 채움 + 상하/좌우 음영 */
    const body = d =>
      '<path d="'+d+'" fill="'+main+'"/>' +
      '<path d="'+d+'" fill="url(#'+gid+')"/>' +
      '<path d="'+d+'" fill="url(#'+gid+'s)"/>';
    const seams =
      '<path d="M18 15 Q15 30 16 46" fill="none" stroke="rgba(0,0,0,.10)" stroke-width=".7"/>' +
      '<path d="M82 15 Q85 30 84 46" fill="none" stroke="rgba(0,0,0,.10)" stroke-width=".7"/>';
    const neckShadow = '<ellipse cx="50" cy="9.5" rx="6.5" ry="1.8" fill="rgba(0,0,0,.06)"/>';
    /* blendInner: 곱해질 몸판, topInner: 불투명 디테일 */
    const compose = (blendInner, topInner) =>
      svgOpen('blend') + defs + blendInner + close +
      svgOpen('top') + (topInner || '') + close;

    if(v.outfit === 'shirt'){
      const collar = c.collar || '#f2f4f7';
      /* 네크라인을 목 바로 아래(y11)로 올려 카라가 목에 붙어 보이게 */
      const bodyD = 'M0 46 V19 Q14 10 33 7 L43 4.5 50 11 57 4.5 67 7 Q86 10 100 19 V46 Z';
      return compose(
        neckShadow + body(bodyD) + seams +
        '<path d="M30 24 Q32 30 30 38" fill="none" stroke="rgba(0,0,0,.08)" stroke-width=".8"/>' +
        '<path d="M70 24 Q68 30 70 38" fill="none" stroke="rgba(0,0,0,.08)" stroke-width=".8"/>',
        '<path d="M43 4.5 50 11 45.8 14.5 40 7 Z" fill="'+collar+'" stroke="rgba(0,0,0,.16)" stroke-width=".4"/>' +
        '<path d="M57 4.5 50 11 54.2 14.5 60 7 Z" fill="'+collar+'" stroke="rgba(0,0,0,.16)" stroke-width=".4"/>' +
        '<path d="M50 11 V46" stroke="'+line+'" stroke-width=".7"/>' +
        '<circle cx="50" cy="17" r=".8" fill="'+line+'"/><circle cx="50" cy="25" r=".8" fill="'+line+'"/><circle cx="50" cy="33" r=".8" fill="'+line+'"/><circle cx="50" cy="41" r=".8" fill="'+line+'"/>');
    }
    if(v.outfit === 'suit'){
      const shirt = c.shirt || '#f6f7f9';
      const tie = c.tie || '';
      const left = 'M0 46 V18 Q14 9 34 6.5 L42 5 47 46 H0 Z';
      const right = 'M100 46 V18 Q86 9 66 6.5 L58 5 53 46 H100 Z';
      return compose(
        neckShadow + body(left) + body(right) +
        '<path d="M42 5 L50 24 43.5 31 37.5 9 Z" fill="'+line+'"/>' +
        '<path d="M58 5 L50 24 56.5 31 62.5 9 Z" fill="'+line+'"/>',
        /* 안쪽 셔츠가 재킷 사이 전체를 채워 원본 옷이 비치지 않게 */
        '<path d="M42 5 L47.2 46 H52.8 L58 5 Q50 9.5 42 5 Z" fill="'+shirt+'"/>' +
        (tie
          ? '<path d="M48.4 15.5 h3.2 l-.7 3.8 h-1.9 Z" fill="'+tie+'"/><path d="M50 19 L47.2 27 50 42 52.8 27 Z" fill="'+tie+'"/>'
          : '<path d="M45.5 12 Q50 16 54.5 12" fill="none" stroke="rgba(0,0,0,.16)" stroke-width=".8"/>') +
        '<circle cx="45.8" cy="38" r=".8" fill="rgba(255,255,255,.35)"/>');
    }
    if(v.outfit === 'hoodie'){
      const bodyD = 'M0 46 V21 Q14 11 33 8.5 Q41 7.5 44 10 Q50 16.5 56 10 Q59 7.5 67 8.5 Q86 11 100 21 V46 Z';
      return compose(
        '<path d="M30 16 Q50 -4 70 16 Q60 10 50 10 Q40 10 30 16 Z" fill="'+line+'"/>' +
        neckShadow + body(bodyD) + seams +
        '<path d="M28 36 Q50 40 72 36" fill="none" stroke="rgba(0,0,0,.10)" stroke-width=".7"/>',
        '<path d="M43 10 Q50 17 57 10" fill="none" stroke="'+line+'" stroke-width="1.8"/>' +
        '<path d="M46.5 13 Q46 20 46.8 25" fill="none" stroke="'+(c.string||'#999')+'" stroke-width=".9"/>' +
        '<path d="M53.5 13 Q54 20 53.2 25" fill="none" stroke="'+(c.string||'#999')+'" stroke-width=".9"/>');
    }
    if(v.outfit === 'cardigan'){
      /* 가디건 사이로는 사진 속 실제 이너(흰 티)가 그대로 보이게 둔다 — 가장 자연스러움 */
      const left = 'M0 46 V19 Q14 10 34 7.5 L41 7 46.5 46 H0 Z';
      const right = 'M100 46 V19 Q86 10 66 7.5 L59 7 53.5 46 H100 Z';
      return compose(
        neckShadow + body(left) + body(right),
        '<path d="M41 7 L46.5 46" fill="none" stroke="'+line+'" stroke-width=".8"/>' +
        '<path d="M59 7 L53.5 46" fill="none" stroke="'+line+'" stroke-width=".8"/>' +
        '<circle cx="45" cy="26" r=".9" fill="'+line+'"/><circle cx="45.7" cy="33" r=".9" fill="'+line+'"/><circle cx="46.3" cy="40" r=".9" fill="'+line+'"/>');
    }
    if(v.outfit === 'henley'){
      const bodyD = 'M0 46 V20 Q14 10.5 34 8 Q42 7 45 9 Q50 15 55 9 Q58 7 66 8 Q86 10.5 100 20 V46 Z';
      return compose(
        neckShadow + body(bodyD) + seams,
        '<path d="M44 9 Q50 16 56 9" fill="none" stroke="'+line+'" stroke-width="1.5"/>' +
        '<path d="M50 15 V28" stroke="'+line+'" stroke-width=".8"/>' +
        '<circle cx="50" cy="19" r=".8" fill="rgba(255,255,255,.5)"/><circle cx="50" cy="24" r=".8" fill="rgba(255,255,255,.5)"/>');
    }
    if(v.outfit === 'blouse'){
      /* 여성 보트넥/니트 블라우스: 넓고 완만한 네크라인 */
      const bodyD = 'M0 46 V20 Q13 11 32 8.5 Q40 7.5 50 12.5 Q60 7.5 68 8.5 Q87 11 100 20 V46 Z';
      return compose(
        neckShadow + body(bodyD) + seams +
        '<path d="M30 30 Q50 34 70 30" fill="none" stroke="rgba(0,0,0,.08)" stroke-width=".8"/>',
        '<path d="M35 9.5 Q50 15.5 65 9.5" fill="none" stroke="'+line+'" stroke-width="1.2"/>');
    }
    /* knit (라운드넥 니트) */
    const bodyD = 'M0 46 V20 Q14 10.5 34 8 Q42 7 45 9 Q50 15.5 55 9 Q58 7 66 8 Q86 10.5 100 20 V46 Z';
    return compose(
      neckShadow + body(bodyD) + seams +
      '<path d="M32 26 Q34 32 32 40" fill="none" stroke="rgba(0,0,0,.07)" stroke-width=".8"/>' +
      '<path d="M68 26 Q66 32 68 40" fill="none" stroke="rgba(0,0,0,.07)" stroke-width=".8"/>',
      '<path d="M43.5 8.5 Q50 16.5 56.5 8.5" fill="none" stroke="'+line+'" stroke-width="1.6"/>' +
      '<path d="M0 41.5 H100" stroke="'+line+'" stroke-width=".5" opacity=".4"/>');
  }
  const TAG_POS = [{top:'32%',left:'40%'},{top:'50%',left:'62%'},{top:'66%',left:'42%'}];
  /* 제품 카테고리별 마커 기준 부위 — 번호는 준비 순서, 위치는 그 제품이 닿는 부위 */
  const KIND_POS = {
    sun:       {t:27, l:50},   /* 선크림·톤업 — 이마 */
    suncheek:  {t:50, l:33},   /* 선케어 보조 — 볼 */
    base:      {t:64, l:42},   /* 쿠션·파운데이션 — 턱선·피부 */
    concealer: {t:43, l:59},   /* 컨실러 — 눈 밑 */
    lip:       {t:59, l:49},   /* 립밤·틴트 — 입술 */
    brow:      {t:31, l:41},   /* 아이브로우 — 눈썹 */
    blush:     {t:51, l:64},   /* 블러셔 — 볼 */
    shade:     {t:70, l:35},   /* 쉐이딩 — 턱선 */
    spot:      {t:56, l:67},   /* 스팟·트러블 케어 — 볼·턱 */
    skin:      {t:48, l:61},   /* 스킨케어 — 볼 */
    point:     {t:59, l:49},   /* 포인트 — 입술 */
    hair:      {t:11, l:52}    /* 헤어 — 머리 */
  };
  /* 단계의 실제 제품명에서 더 구체적인 카테고리를 추론 → 부위 매칭 */
  function inferMarkerKind(step){
    const txt = (step.items || []).join(' ');
    if(/컨실러/.test(txt)) return 'concealer';
    if(/틴트|립밤|립 /.test(txt)) return 'lip';
    if(/브로우|눈썹/.test(txt)) return 'brow';
    if(/블러셔/.test(txt)) return 'blush';
    if(/쉐이딩/.test(txt)) return 'shade';
    if(/트러블|스팟|블레미쉬/.test(txt)) return 'spot';
    if(/선크림|선스틱|선세럼|톤업/.test(txt)) return 'sun';
    if(/쿠션|파운데이션/.test(txt)) return 'base';
    return step.k;
  }
  /* 카드(id)+단계(index) 기반 결정적 지터: 카드마다 같은 좌표가 재사용되지 않게 ±3~4% 분산 */
  function markerPos(step, feedId, idx){
    const p = KIND_POS[inferMarkerKind(step)] || KIND_POS[step.k] || KIND_POS.skin;
    let h = 0;
    const s = feedId + ':' + idx + ':' + (step.step || '');
    for(let i=0; i<s.length; i++){ h = (h * 31 + s.charCodeAt(i)) & 0xffff; }
    const jt = ((h % 11) - 5) * 1.0;
    const jl = (((h >> 5) % 11) - 5) * 1.1;
    return { top:(p.t + jt).toFixed(1) + '%', left:(p.l + jl).toFixed(1) + '%' };
  }
  const IC_SKIN  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M9 10h.01M15 10h.01M8.5 15a4 4 0 0 0 7 0"/></svg>';
  const IC_COS   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 2h6v4l1 3v11a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V9l1-3z"/><path d="M9 9h6"/></svg>';
  const IC_SHIRT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 3l4 3-3 3-1-1v11H8V8L7 8 4 6l4-3 2 2h4z"/></svg>';
  const IC_HAIR  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 15a8 8 0 0 1 16 0M6 15c0 3 1 5 3 5M18 15c0 3-1 5-3 5"/></svg>';

  function currentStyleGender(){ return (window.appState && window.appState.gender) === 'female' ? 'female' : 'male'; }
  function faceImg(gender){ return gender === 'female' ? (window.FACE_FEMALE || '') : (window.FACE_MALE || ''); }

  function renderTpo(sit){
    const g = currentStyleGender();
    const look = TPO_LOOKS[sit][g];
    const t = TPO[sit];
    const slot = (icon,label,content)=>
      '<div class="tpo-slot"><div class="tpo-slot-label">'+icon+label+'</div>'+content+'</div>';
    /* 헤더는 날씨 위젯이 상주하므로, 상황(TPO) 타이틀은 본문 첫 줄로 렌더링 */
    document.getElementById('tpoComboBody').innerHTML =
      '<div class="tpo-slot full tpo-situ">' +
        '<div class="tpo-situ-title">'+t.emoji+' '+t.label+' 추천 룩</div>' +
        '<div class="tpo-impression">'+look.impression.map(k=>'<span>#'+k+'</span>').join('')+'</div>' +
      '</div>' +
      slot(IC_SKIN,'피부 포인트','<div class="tpo-slot-sub">'+look.skin+'</div>') +
      slot(IC_COS,'화장품','<ul class="tpo-slot-list">'+look.cosmetics.map(c=>'<li>'+c+'</li>').join('')+'</ul>') +
      slot(IC_SHIRT,'옷','<div class="tpo-slot-main">'+look.outfit.main+'</div><div class="tpo-slot-sub">'+look.outfit.sub+'</div>') +
      slot(IC_HAIR,'헤어','<div class="tpo-slot-main">'+look.hair.main+'</div><div class="tpo-slot-sub">'+look.hair.sub+'</div>');
  }

  /* ---------------- 오늘의 날씨 위젯 (Open-Meteo, API 키 불필요) ---------------- */
  const WX_DEFAULT = { lat:37.5665, lon:126.9780, name:'서울' };
  const WX_RECO = {
    hot:   { copy:'햇살이 강한 날이에요. 유분만 잡으면 완벽해요.',
             skin:'유분 조절 + 가벼운 수분', makeup:'가벼운 피부 표현, 무너짐 방지', outfit:'밝은 셔츠·통기성 좋은 소재', hair:'땀에 강한 깔끔한 세팅' },
    rain:  { copy:'비가 오는 날엔 무너지지 않는 세팅이 핵심이에요.',
             skin:'번들거림 방지, 산뜻한 마무리', makeup:'지속력 위주로 얇게', outfit:'어두운 톤 상의로 차분하게', hair:'습기에 강한 정돈된 스타일' },
    cold:  { copy:'차고 건조한 날이에요. 보습이 8할입니다.',
             skin:'보습 중심, 크림 든든하게', makeup:'각질 부각 없는 촉촉한 표현', outfit:'니트·아우터로 따뜻하게', hair:'부드러운 볼륨 스타일' },
    cloudy:{ copy:'흐린 날엔 피부 컨디션 관리에 집중하세요.',
             skin:'진정·장벽 보호 중심', makeup:'최소한만 가볍게', outfit:'차분한 톤 착장', hair:'힘 뺀 내추럴 스타일' },
    mild:  { copy:'활동하기 좋은 날씨예요. 기본에 충실하면 충분해요.',
             skin:'수분 밸런스 유지', makeup:'자연스러운 톤 정돈', outfit:'가벼운 레이어드', hair:'평소 스타일 유지' }
  };
  function wmoInfo(code){
    if(code===0 || code===1) return {label:'맑음', emoji:'☀️'};
    if(code===2) return {label:'구름 조금', emoji:'🌤️'};
    if(code===3) return {label:'흐림', emoji:'☁️'};
    if(code===45 || code===48) return {label:'안개', emoji:'🌫️'};
    if(code>=51 && code<=67) return {label:'비', emoji:'🌧️'};
    if((code>=71 && code<=77) || code===85 || code===86) return {label:'눈', emoji:'🌨️'};
    if(code>=80 && code<=82) return {label:'소나기', emoji:'🌦️'};
    if(code>=95) return {label:'뇌우', emoji:'⛈️'};
    return {label:'보통', emoji:'🌤️'};
  }
  function pickWxReco(code, temp, hum){
    const rainy = (code>=51 && code<=67) || (code>=80 && code<=99);
    const snowy = (code>=71 && code<=77) || code===85 || code===86;
    if(rainy || hum>=78) return 'rain';
    if(snowy || temp<=5 || (temp<=12 && hum<=35)) return 'cold';
    if(temp>=27 && code<=1) return 'hot';
    if(code>=2) return 'cloudy';
    if(temp>=26) return 'hot';
    return 'mild';
  }
  function renderWx(d, note){
    const head = document.getElementById('wxHead');
    head.classList.remove('wx-loading');
    const w = wmoInfo(d.code);
    const key = pickWxReco(d.code, d.temp, d.hum);
    const r = WX_RECO[key];
    document.getElementById('wxTitle').textContent = w.emoji + ' ' + d.name + ' · ' + w.label + ' ' + Math.round(d.temp) + '°C';
    document.getElementById('wxMeta').textContent = '체감 ' + Math.round(d.feels) + '°C · 습도 ' + Math.round(d.hum) + '%';
    document.getElementById('wxCopy').textContent = '"' + r.copy + '"';
    document.getElementById('wxReco').innerHTML = [
      ['스킨케어', r.skin], ['메이크업', r.makeup], ['옷', r.outfit], ['헤어', r.hair]
    ].map(x=>'<div class="wx-reco-item"><b>'+x[0]+'</b><span>'+x[1]+'</span></div>').join('');
    const noteEl = document.getElementById('wxNote');
    noteEl.hidden = !note;
    noteEl.textContent = note || '';
  }
  function renderWxError(msg){
    document.getElementById('wxHead').classList.remove('wx-loading');
    document.getElementById('wxTitle').textContent = '날씨 정보를 가져오지 못했어요';
    document.getElementById('wxMeta').textContent = '';
    document.getElementById('wxCopy').textContent = '';
    document.getElementById('wxReco').innerHTML = '';
    const noteEl = document.getElementById('wxNote');
    noteEl.hidden = false;
    noteEl.textContent = msg;
  }
  async function fetchWx(lat, lon, fallbackName){
    const url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon +
      '&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code&timezone=auto';
    const r = await fetch(url);
    if(!r.ok) throw new Error('HTTP ' + r.status);
    const j = await r.json();
    const c = j.current || {};
    let name = fallbackName;
    /* 지역명 역지오코딩(키 불필요) — 실패해도 날씨 표시엔 지장 없음 */
    try{
      const g = await fetch('https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=' + lat + '&longitude=' + lon + '&localityLanguage=ko');
      if(g.ok){ const gj = await g.json(); name = gj.city || gj.locality || gj.principalSubdivision || fallbackName; }
    }catch(e){}
    return { name:name, code:c.weather_code|0, temp:+c.temperature_2m, feels:+c.apparent_temperature, hum:+c.relative_humidity_2m };
  }
  let wxBusy = false;
  function loadWx(){
    if(wxBusy) return;
    wxBusy = true;
    const head = document.getElementById('wxHead');
    const btn = document.getElementById('wxRefresh');
    head.classList.add('wx-loading');
    btn.disabled = true;
    document.getElementById('wxTitle').textContent = '날씨 불러오는 중…';
    document.getElementById('wxMeta').textContent = '현재 위치를 확인하고 있어요';
    const finish = ()=>{ wxBusy = false; btn.disabled = false; };
    const useDefault = ()=>{
      fetchWx(WX_DEFAULT.lat, WX_DEFAULT.lon, WX_DEFAULT.name)
        .then(d=>{ renderWx(d, '위치 권한이 없어 기본 지역(서울) 날씨를 표시합니다.'); })
        .catch(()=> renderWxError('날씨 정보를 가져오지 못했습니다. 다시 시도해주세요.'))
        .finally(finish);
    };
    if(navigator.geolocation){
      navigator.geolocation.getCurrentPosition(
        pos=>{
          fetchWx(pos.coords.latitude, pos.coords.longitude, '내 위치')
            .then(d=>{ renderWx(d, ''); })
            .catch(useDefault)
            .finally(finish);
        },
        useDefault,
        { timeout:5000, maximumAge:600000 }
      );
    } else {
      useDefault();
    }
  }

  let activeFeedSit = 'date';
  function renderFeed(sit){
    if(sit){ activeFeedSit = sit; }
    const feedEl = document.getElementById('styleFeed');
    /* 피드 헤더에 현재 상황을 표시해 탭과 피드가 연결돼 있음을 분명히 한다 */
    const subEl = document.querySelector('.style-feed-sub');
    if(subEl){ subEl.textContent = TPO[activeFeedSit].emoji + ' ' + TPO[activeFeedSit].label + ' 상황 추천 룩 — 사진 속 번호는 준비 순서예요'; }
    feedEl.innerHTML = STYLE_FEED.filter(f=> f.sit === activeFeedSit).map(f=>{
      const look = TPO_LOOKS[f.sit][f.gender];
      const t = TPO[f.sit];
      const v = f.visual || {};
      /* look_<id>.png 실사 에셋이 있으면 우선 사용(필터·합성 생략) */
      const asset = (window.LOOK_IMGS || {})[f.id];
      const img = asset || faceImg(f.gender);
      const imgStyle = asset ? '' : 'style="' + (v.filter ? 'filter:'+v.filter+';' : '') + (v.pos ? 'object-position:'+v.pos+';' : '') + '"';
      /* 번호 = 실제 준비 순서(1 먼저 → 3 마지막).
         카드에 markers(촬영 세트 기준 좌표)가 있으면 그대로, 없으면 부위 기반 자동 배치 */
      const steps = look.routine || [];
      const tags = steps.map((s,i)=>{
        const m = f.markers && f.markers[i];
        const pos = m ? { top:m.t + '%', left:m.l + '%' } : markerPos(s, f.id, i);
        return '<div class="feed-tag" style="top:'+pos.top+';left:'+pos.left+'" title="'+(i+1)+'. '+s.step+'">'+(i+1)+'</div>';
      }).join('');
      const outfitMain = (f.outfitText && f.outfitText.main) || look.outfit.main;
      const hairMain = f.hairText || look.hair.main;
      return '<div class="feed-card" data-feed="'+f.id+'">' +
        '<div class="feed-photo">' + (img?'<img src="'+img+'" alt="'+f.title+'" '+imgStyle+' />':'') +
          (asset ? '' : outfitSvg(v, f.id)) +
          '<div class="feed-situation">'+t.emoji+' '+t.label+'</div>' + tags + '</div>' +
        '<div class="feed-foot"><div class="feed-look-title">'+f.title+'</div>' +
          '<div class="feed-keys">'+look.impression.map(k=>'<span>#'+k+'</span>').join('')+'</div>' +
          '<div class="feed-style-line">'+outfitMain+' · '+hairMain+'</div></div>' +
      '</div>';
    }).join('');
    /* 클릭 좌표를 넘겨 모달이 스크롤 없이 그 자리에 바로 뜨게 한다 */
    feedEl.querySelectorAll('.feed-card').forEach(c=>
      c.addEventListener('click', e=> openSheet(c.dataset.feed, e.clientY)));
  }

  const SAVED_KEY = 'forhim_saved_styles';
  function loadSavedStyles(){ try{ return new Set(JSON.parse(localStorage.getItem(SAVED_KEY) || '[]')); }catch(e){ return new Set(); } }
  function persistSavedStyles(set){ try{ localStorage.setItem(SAVED_KEY, JSON.stringify(Array.from(set))); }catch(e){} }

  function openSheet(feedId, clickY){
    const f = STYLE_FEED.find(x=> x.id === feedId); if(!f) return;
    const look = TPO_LOOKS[f.sit][f.gender];
    const t = TPO[f.sit];
    const img = faceImg(f.gender);
    const v = f.visual || {};
    const asset = (window.LOOK_IMGS || {})[f.id];
    const sheetImg = asset || img;
    const imgStyle = asset ? '' : 'style="' + (v.filter ? 'filter:'+v.filter+';' : '') + 'object-position:' + (v.pos || 'center 28%') + ';"';
    /* 카드별 착장·헤어 오버라이드가 있으면 시트에도 동일하게 반영 */
    const outfitInfo = f.outfitText || look.outfit;
    const hairInfo = f.hairText ? { main:f.hairText, sub:look.hair.sub } : look.hair;
    const sec = (icon,label,content)=>
      '<div class="sheet-sec"><div class="sheet-sec-label">'+icon+label+'</div>'+content+'</div>';
    document.getElementById('sheetCard').innerHTML =
      '<div class="sheet-photo"><button type="button" class="sheet-close" id="sheetClose">×</button>' +
        (sheetImg?'<img src="'+sheetImg+'" alt="'+f.title+'" '+imgStyle+' />':'') + (asset ? '' : outfitSvg(v, 'sheet-'+f.id)) + '</div>' +
      '<div class="sheet-body">' +
        '<div class="sheet-situation">'+t.emoji+' '+t.label+'</div>' +
        '<div class="sheet-title">'+f.title+'</div>' +
        '<div class="sheet-keys">'+look.impression.map(k=>'<span>#'+k+'</span>').join('')+'</div>' +
        sec(IC_SKIN,'피부 타입 추천 포인트','<div class="sheet-skin">'+look.skin+'</div>') +
        /* 준비 순서: 사진 속 번호와 동일한 순서로, 단계별 사용 제품을 나열 */
        (look.routine && look.routine.length
          ? sec(IC_COS,'준비 순서 · 사진 속 번호와 같아요',
              look.routine.map((s,i)=>
                '<div class="sheet-step">' +
                  '<div class="sheet-step-head"><div class="sheet-prod-no">'+(i+1)+'</div>' +
                    '<b class="sheet-step-name">'+s.step+'</b><span class="sheet-step-sub">'+s.d+'</span></div>' +
                  '<div class="sheet-step-items">'+s.items.map(it=>'<div class="sheet-step-item">'+it+'</div>').join('')+'</div>' +
                '</div>').join('') +
              (look.extras && look.extras.length
                ? '<button type="button" class="sheet-more-btn" id="sheetMoreBtn"><span>추가 추천 보기</span>' +
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M6 9l6 6 6-6"/></svg></button>' +
                  '<div class="sheet-extra" id="sheetExtra">' +
                    look.extras.map(g=>
                      '<div class="sheet-extra-group"><div class="sheet-extra-label">'+g.label+'</div>' +
                        g.items.map(it=>'<div class="sheet-step-item">'+it+'</div>').join('') +
                      '</div>').join('') +
                  '</div>'
                : ''))
          : sec(IC_COS,'사용 화장품', look.cosmetics.map((c,i)=>
              '<div class="sheet-prod"><div class="sheet-prod-no">'+(i+1)+'</div><div class="sheet-prod-txt"><b>'+c+'</b></div></div>').join(''))) +
        '<div class="sheet-sec"><div class="sheet-two">' +
          '<div><div class="sheet-sec-label">'+IC_SHIRT+'추천 옷 스타일</div><div class="sheet-mini-main">'+outfitInfo.main+'</div><div class="sheet-mini-sub">'+(outfitInfo.sub||'')+'</div></div>' +
          '<div><div class="sheet-sec-label">'+IC_HAIR+'헤어 스타일</div><div class="sheet-mini-main">'+hairInfo.main+'</div><div class="sheet-mini-sub">'+(hairInfo.sub||'')+'</div></div>' +
        '</div></div>' +
        '<div class="sheet-actions">' +
          '<button type="button" class="btn btn-gold btn-sm" id="sheetSave"></button>' +
          '<button type="button" class="btn btn-outline btn-sm" id="sheetCloseBtn">닫기</button>' +
        '</div>' +
      '</div>';
    const sheet = document.getElementById('styleSheet');
    sheet.hidden = false;
    /* 모달을 클릭한 위치에 바로 표시 — 하단으로 스크롤할 필요가 없다 */
    const card = document.getElementById('sheetCard');
    const y = (typeof clickY === 'number' && !isNaN(clickY)) ? clickY : 120;
    let top = Math.max(16, y - 160);
    card.style.top = top + 'px';
    requestAnimationFrame(()=>{
      const overflow = (card.offsetTop + card.offsetHeight) - (window.innerHeight - 16);
      if(overflow > 0){ card.style.top = Math.max(16, card.offsetTop - overflow) + 'px'; }
    });
    /* 배경 스크롤 잠금 (독립 실행 환경 기준; iframe에선 부모가 스크롤을 관리) */
    document.documentElement.style.overflow = 'hidden';
    document.getElementById('sheetClose').addEventListener('click', closeSheet);
    document.getElementById('sheetCloseBtn').addEventListener('click', closeSheet);
    /* 저장하기 */
    const saveBtn = document.getElementById('sheetSave');
    const saved = loadSavedStyles();
    const syncSave = ()=>{ saveBtn.textContent = saved.has(f.id) ? '저장됨 ✓' : '이 스타일 저장하기'; };
    syncSave();
    saveBtn.addEventListener('click', ()=>{
      if(saved.has(f.id)){ saved.delete(f.id); } else { saved.add(f.id); }
      persistSavedStyles(saved);
      syncSave();
      const toast = document.getElementById('toast');
      if(toast){
        toast.textContent = saved.has(f.id) ? '스타일을 저장했어요' : '저장을 해제했어요';
        toast.classList.add('show');
        setTimeout(()=> toast.classList.remove('show'), 1800);
      }
    });
    /* 추가 추천 열기/닫기 — 기본은 접힌 상태로 가볍게 유지 */
    const moreBtn = document.getElementById('sheetMoreBtn');
    if(moreBtn){
      moreBtn.addEventListener('click', ()=>{
        const ex = document.getElementById('sheetExtra');
        const open = ex.classList.toggle('open');
        moreBtn.classList.toggle('open', open);
        moreBtn.querySelector('span').textContent = open ? '접기' : '추가 추천 보기';
      });
    }
  }
  function closeSheet(){
    document.getElementById('styleSheet').hidden = true;
    document.documentElement.style.overflow = '';
  }

  function initStyle(){
    styleInitialized = true;
    const tabsEl = document.getElementById('tpoTabs');
    tabsEl.innerHTML = TPO_ORDER.map((k,i)=>
      '<button type="button" class="tpo-tab'+(i===0?' active':'')+'" data-tpo="'+k+'">' +
      '<span class="tpo-emoji">'+TPO[k].emoji+'</span>'+TPO[k].label+'</button>').join('');
    tabsEl.addEventListener('click', e=>{
      const b = e.target.closest('.tpo-tab'); if(!b) return;
      tabsEl.querySelectorAll('.tpo-tab').forEach(x=> x.classList.remove('active'));
      b.classList.add('active');
      /* 탭 전환 시 상단 추천 조합과 하단 스타일 피드를 함께 해당 상황으로 교체 */
      renderTpo(b.dataset.tpo);
      renderFeed(b.dataset.tpo);
    });
    document.getElementById('sheetBackdrop').addEventListener('click', closeSheet);
    document.addEventListener('keydown', e=>{
      if(e.key === 'Escape' && !document.getElementById('styleSheet').hidden){ closeSheet(); }
    });
    document.getElementById('wxRefresh').addEventListener('click', loadWx);
    loadWx();
    /* 기본 진입 시에도 활성 탭(소개팅)에 맞는 추천과 피드가 함께 보인다 */
    renderTpo('date');
    renderFeed('date');
  }

  /* ---------------- 올리브영 랭킹 뱃지 ----------------
     window.OY_RANKING: fetch_oy_ranking.py 배치(1일 1회 권장)가 갱신하는 랭킹 스냅샷.
     랭킹 데이터에 매칭되는 제품만 뱃지를 노출한다 — 근거 없는 '1위' 표기 방지. */
  function normTxt(s){ return String(s || '').split(' ').join('').toLowerCase(); }
  function getOyRank(p){
    const d = window.OY_RANKING;
    if(!d || !Array.isArray(d.entries)) return null;
    for(const e of d.entries){
      if(e.matchId && e.matchId === p.id) return e;
      /* 배치 수집 데이터: 브랜드 일치 + 제품명 부분 일치로 자사 카탈로그와 매칭 */
      if(!e.matchId && e.brand && normTxt(e.brand) === normTxt(p.brand) && e.name &&
         (normTxt(p.name).indexOf(normTxt(e.name)) >= 0 || normTxt(e.name).indexOf(normTxt(p.name)) >= 0)){
        return e;
      }
    }
    return null;
  }
  function userAgeGroup(){
    const age = (window.appState && window.appState.age) || 0;
    return age ? (Math.floor(age / 10) * 10) + '대' : '';
  }
  function userGenderLabel(){
    const g = (window.appState && window.appState.gender) || '';
    return g === 'male' ? '男' : g === 'female' ? '女' : '';
  }
  function getRankBadgeText({ rank, ageGroup, gender, hasSegmentedData }){
    if(rank !== 1) return null;   /* 1위가 아니면(또는 랭킹 정보가 없으면) 뱃지 미노출 */
    if(hasSegmentedData && ageGroup && gender){
      return ageGroup + ' ' + gender + ' 구매 1위';   /* 예: "30대 男 구매 1위" */
    }
    return '올리브영 판매 1위';   /* 연령/성별 세분화 데이터 없을 때 fallback */
  }
  window.getRankBadgeText = getRankBadgeText;
  function rankBadgeFor(p){
    const e = getOyRank(p);
    if(!e) return null;
    const d = window.OY_RANKING || {};
    return getRankBadgeText({
      rank: e.rank,
      ageGroup: e.ageGroup || userAgeGroup(),
      gender: e.gender || userGenderLabel(),
      hasSegmentedData: !!d.segmented
    });
  }

  /* 이미지 없는 제품용 카테고리 형태 일러스트 — 카드 비율을 이미지 카드와 동일하게 유지 */
  function prodShapeSvg(p){
    const c = p.color || '#8b6f47';
    const hl = 'rgba(255,255,255,.4)';
    const cat = (p.cats && p.cats[0]) || '';
    const wrap = inner => '<svg viewBox="0 0 60 100" aria-hidden="true">' + inner + '</svg>';
    if(cat === 'perfume') return wrap(
      '<rect x="25" y="6" width="10" height="12" rx="2" fill="#b6afa2"/>' +
      '<path d="M15 32 Q15 21 30 21 Q45 21 45 32 L43 87 Q43 93 30 93 Q17 93 17 87 Z" fill="'+c+'"/>' +
      '<ellipse cx="24" cy="42" rx="4" ry="9" fill="'+hl+'"/>');
    if(cat === 'deo') return wrap(
      '<path d="M18 30 Q18 18 30 18 Q42 18 42 30 V38 H18 Z" fill="'+c+'" opacity=".55"/>' +
      '<rect x="18" y="38" width="24" height="52" rx="7" fill="'+c+'"/>' +
      '<rect x="22" y="46" width="5" height="30" rx="2.5" fill="'+hl+'"/>');
    if(cat === 'bodylotion') return wrap(
      '<path d="M27 8 H33 V16 H43 V22 H27 Z" fill="#b6afa2"/><rect x="27" y="16" width="6" height="10" fill="#b6afa2"/>' +
      '<path d="M17 30 Q17 26 21 26 H39 Q43 26 43 30 L44 86 Q44 93 30 93 Q16 93 16 86 Z" fill="'+c+'"/>' +
      '<rect x="21" y="42" width="6" height="34" rx="3" fill="'+hl+'"/>');
    if(cat === 'foot' || cat === 'cleanser' || cat === 'sun') return wrap(
      '<rect x="22" y="8" width="16" height="10" rx="3" fill="#b6afa2"/>' +
      '<path d="M20 20 H40 L44 82 Q44 92 30 92 Q16 92 16 82 Z" fill="'+c+'"/>' +
      '<rect x="21" y="34" width="5" height="36" rx="2.5" fill="'+hl+'"/>');
    if(cat === 'cushion') return wrap(
      '<ellipse cx="30" cy="58" rx="24" ry="22" fill="'+c+'"/>' +
      '<ellipse cx="30" cy="50" rx="24" ry="6" fill="'+hl+'"/>' +
      '<ellipse cx="30" cy="38" rx="24" ry="7" fill="'+c+'" opacity=".7"/>');
    if(cat === 'brow') return wrap(
      '<rect x="26" y="14" width="8" height="58" rx="3" fill="'+c+'"/>' +
      '<path d="M26 72 L30 90 L34 72 Z" fill="#d8cfc0"/><path d="M28.6 82 L30 90 L31.4 82 Z" fill="#4a3a2c"/>' +
      '<rect x="27.5" y="18" width="2.5" height="46" fill="'+hl+'"/>');
    if(cat === 'eye') return wrap(
      '<rect x="8" y="30" width="44" height="40" rx="6" fill="'+c+'"/>' +
      '<circle cx="19" cy="42" r="4.5" fill="#e8d3bd"/><circle cx="30" cy="42" r="4.5" fill="#c9a184"/><circle cx="41" cy="42" r="4.5" fill="#8a6a52"/>' +
      '<circle cx="19" cy="56" r="4.5" fill="#d9b8a6"/><circle cx="30" cy="56" r="4.5" fill="#a87b62"/><circle cx="41" cy="56" r="4.5" fill="#5c4436"/>');
    if(cat === 'cream') return wrap(
      '<rect x="14" y="34" width="32" height="10" rx="4" fill="'+c+'" opacity=".65"/>' +
      '<path d="M15 46 H45 Q46 72 30 72 Q14 72 15 46 Z" fill="'+c+'"/>' +
      '<ellipse cx="24" cy="52" rx="3" ry="7" fill="'+hl+'"/>');
    if(cat === 'device') return wrap(
      '<rect x="18" y="12" width="24" height="76" rx="12" fill="'+c+'"/>' +
      '<circle cx="30" cy="30" r="7" fill="'+hl+'"/><rect x="26" y="56" width="8" height="16" rx="4" fill="'+hl+'"/>');
    /* 기본: 토너·세럼·로션 등 보틀 */
    return wrap(
      '<rect x="24" y="8" width="12" height="10" rx="2" fill="#b6afa2"/>' +
      '<path d="M18 26 Q18 20 24 20 H36 Q42 20 42 26 L42 84 Q42 92 30 92 Q18 92 18 84 Z" fill="'+c+'"/>' +
      '<rect x="22" y="36" width="5" height="34" rx="2.5" fill="'+hl+'"/>');
  }

  /* ---------------- product card helper ---------------- */
  /* CTA 문구는 특정 판매처에 종속되지 않는 중립 문구를 기본값으로 두고,
     판매 채널이 늘어나면 opts.ctaText로 호출부에서 교체할 수 있게 변수로 관리 */
  const PROD_CTA_DEFAULT = '판매 페이지로 이동 →';
  function renderProductCards(list, opts){
    const ctaText = (opts && opts.ctaText) || PROD_CTA_DEFAULT;
    return list.map(p=>{
      const query = encodeURIComponent(p.brand + ' ' + p.name);
      const url = 'https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=' + query;
      /* 랭킹 뱃지: 올리브영 랭킹 데이터에 1위로 매칭될 때만 노출 */
      const rankText = rankBadgeFor(p);
      const isReco = p.rank === 1;                    /* 내 피부 매칭 최상 → '추천' */
      /* 실물 사진 우선순위: 로컬 prod_<id> 파일 → 카탈로그 img URL → 카테고리 일러스트 */
      const photo = (window.PROD_IMGS || {})[p.id] || p.img;
      return '<a class="prod-card' + (isReco ? ' reco' : '') + '" href="' + url + '" target="_blank" rel="noopener noreferrer">' +
        (rankText ? '<div class="prod-rank">' + rankText + '</div>' : '') +
        (isReco ? '<div class="prod-reco">추천</div>' : '') +
        (photo
          ? '<div class="prod-photo"><img src="' + photo + '" alt="' + p.name + '" loading="lazy" /></div>'
          : '<div class="prod-photo prod-photo-ph">' + prodShapeSvg(p) + '</div>') +
        '<div class="prod-brand">' + p.brand + '</div>' +
        '<div class="prod-name">' + p.name + '</div>' +
        '<div class="prod-tags">' +
          '<span class="prod-tag">' + p.tag + '</span>' +
          (p.match ? '<span class="prod-match">나와 ' + p.match + '% 매치</span>' : '') +
        '</div>' +
        '<div class="prod-cart-btn">' + ctaText + '</div>' +
      '</a>';
    }).join('');
  }
  window.renderProductCards = renderProductCards;

  /* ---------------- recommend: tier tabs ---------------- */
  const PIMG = {
    cosrx: 'https://dn5hzapyfrpio.cloudfront.net/product/a97/a97c0080-1b38-11f0-a461-e9e3e4353caa.jpeg?w=426',
    toriden: 'https://dn5hzapyfrpio.cloudfront.net/product/302/3029f520-5fed-11f1-94d9-bb4c387ac818.jpeg?w=426',
    anua: 'https://dn5hzapyfrpio.cloudfront.net/product/18f/18f9d910-e811-11ef-b7ff-9d94b272a52e.jpeg?w=426',
    mediheal: 'https://dn5hzapyfrpio.cloudfront.net/product/bf9/bf9d94f0-77ef-11f0-ba45-05d1d2abb09d.jpeg?w=426',
    ahc: 'https://dn5hzapyfrpio.cloudfront.net/product/417/417b9320-49b2-11f1-ab05-f74f22f2eff9.jpeg?w=426',
    goodal: 'https://dn5hzapyfrpio.cloudfront.net/product/6f3/6f3891e0-c8cb-11f0-b07b-5b53b651bab0.jpeg?w=426',
    jsm: 'https://dn5hzapyfrpio.cloudfront.net/product/5f6/5f61dd30-7850-11ee-b842-db65e1eeb438.jpeg?w=426',
    hera: 'https://dn5hzapyfrpio.cloudfront.net/product/fe1/fe18aa80-ebc8-11ee-8b0a-6d2974cceb54.jpeg?w=426',
    clioCushion: 'https://dn5hzapyfrpio.cloudfront.net/product/a88/a88ee6f0-846b-11f0-b021-b5dec3c00b35.jpeg?w=426',
    lumir: 'https://dn5hzapyfrpio.cloudfront.net/product/629/629e9f90-47ff-11ef-9c5c-759480f80bcd.jpeg?w=426',
    peripera: 'https://dn5hzapyfrpio.cloudfront.net/product/d34/d3475980-92e5-11f0-9444-11e570e33be4.jpeg?w=426',
    clioEye: 'https://dn5hzapyfrpio.cloudfront.net/product/9cb/9cbc3980-4242-11ee-88cc-5d4011facace.jpeg?w=426',
    physiogel: 'https://dn5hzapyfrpio.cloudfront.net/product/b1f/b1fc6de0-b9f2-11f0-97cf-eb8f804ad159.jpeg?w=426',
    drg: 'https://dn5hzapyfrpio.cloudfront.net/product/c67/c671e760-8bd2-11ed-a6ae-7f4a9ccf8e92.jpeg?w=426',
    medicubeMist: 'https://dn5hzapyfrpio.cloudfront.net/product/adb/adbe3440-984e-11f0-9b5e-4999a7af4d26.jpeg?w=426'
  };
  window.PIMG = PIMG;

  /* ---------------- product catalog + recommendation engine ---------------- */
  /* aff: 관심사(concern) 태그별 적합도 가중치 0~3. pop: 기본 인기도(동점 보정). */
  const ALL_TAGS = ['pore','oil','acne','scar','elastic','texture','spot','blemish',
    'tone','blackhead','darkcircle','shave','ingrown','dull','dryness','redness','pigment','flake','wrinkle','cover'];

  let PRODUCTS = [
    {id:'cosrx', brand:'코스알엑스', name:'더 6 펩타이드 스킨 부스터 세럼', img:PIMG.cosrx, color:'#8b6f47', cats:['serum'], pop:96, tag:'결·컨디션 개선', aff:{pore:2,texture:3,acne:2,blemish:2,pigment:2,dull:2,spot:1,scar:1}},
    {id:'toriden', brand:'토리든', name:'다이브인 저분자 히알루론산 세럼', img:PIMG.toriden, color:'#5c7a8b', cats:['serum'], pop:94, tag:'저분자 수분 진정', aff:{dryness:3,texture:2,redness:2,flake:2,darkcircle:1}},
    {id:'anua', brand:'아누아', name:'PDRN 히알루론산 캡슐 100 세럼', img:PIMG.anua, color:'#7a8b5c', cats:['serum'], pop:90, tag:'PDRN 재생 케어', aff:{scar:3,pigment:2,elastic:2,tone:2,darkcircle:1,spot:2}},
    {id:'anuaTuner', brand:'아누아', name:'어성초 77 토너', color:'#7a8b5c', cats:['toner'], pop:82, tag:'모공·진정 토너', aff:{pore:3,oil:2,acne:2,ingrown:2,flake:2,texture:2,blackhead:2}},
    {id:'mediheal', brand:'메디힐', name:'마데카소사이드 수분 선세럼', img:PIMG.mediheal, color:'#6b8b6f', cats:['sun'], pop:85, tag:'저자극 선케어', aff:{oil:2,redness:2,acne:2}},
    {id:'ahc', brand:'AHC', name:'마스터즈 에어 리치 선스틱', img:PIMG.ahc, color:'#4a7a9b', cats:['sun'], pop:88, tag:'산뜻한 선스틱', aff:{oil:2,dull:1}},
    {id:'goodalSun', brand:'구달', name:'맑은 어성초 진정 수분 선크림', img:PIMG.goodal, color:'#7a9b6f', cats:['sun'], pop:80, tag:'민감성 선크림', aff:{oil:2,redness:2,acne:2}},
    {id:'goodalVitaC', brand:'구달', name:'청귤 비타C 잡티 세럼', color:'#c9915c', cats:['serum'], pop:87, tag:'비타민C 브라이트닝', aff:{spot:3,pigment:3,tone:2,dull:2,blemish:2}},
    {id:'jsm', brand:'정샘물', name:'에센셜 스킨 누더 쿠션', img:PIMG.jsm, color:'#c9915c', cats:['cushion'], pop:89, tag:'자연스러운 피부 보정', aff:{cover:3,tone:2,dull:1}},
    {id:'hera', brand:'헤라', name:'블랙 쿠션 파운데이션', img:PIMG.hera, color:'#9b7a4a', cats:['cushion'], pop:84, tag:'커버 + 지속력', aff:{cover:3,tone:2,scar:1}},
    {id:'clioCushion', brand:'클리오', name:'킬커버 파운웨어 쿠션', img:PIMG.clioCushion, color:'#b58b5c', cats:['cushion'], pop:83, tag:'모공 커버', aff:{cover:3,pore:1,tone:2}},
    {id:'lumir', brand:'루미르', name:'라이트 온 아이즈 섀도우 팔레트', img:PIMG.lumir, color:'#9b6f8b', cats:['eye'], pop:72, tag:'퍼스널컬러 팔레트', aff:{}},
    {id:'peripera', brand:'페리페라', name:'올테이크 무드 팔레트', img:PIMG.peripera, color:'#c15c5c', cats:['eye'], pop:78, tag:'데일리 아이 컬러', aff:{}},
    {id:'clioEye', brand:'클리오', name:'프로 아이 팔레트 에어', img:PIMG.clioEye, color:'#a85c6f', cats:['eye'], pop:76, tag:'데일리 섀도우', aff:{}},
    {id:'medicubeAger', brand:'메디큐브', name:'AGE-R 부스터 프로', color:'#5c6f8b', cats:['device'], pop:79, tag:'리프팅 디바이스', aff:{elastic:3,wrinkle:2,dull:1}},
    {id:'vflab', brand:'브이플랩', name:'브이토닝 디바이스', color:'#6f5c8b', cats:['device'], pop:70, tag:'얼굴 라인 관리', aff:{elastic:2}},
    {id:'wellbeing', brand:'웰빙시크릿', name:'4D 페이스 마사지기', color:'#5c8b7a', cats:['device'], pop:68, tag:'붓기 케어', aff:{darkcircle:2,elastic:1}},
    {id:'estraCream', brand:'에스트라', name:'아토베리어365 크림', color:'#6b7a8b', cats:['cream'], pop:86, tag:'장벽 강화 크림', aff:{dryness:3,redness:2,elastic:2,flake:2}},
    {id:'origins', brand:'오리진스', name:'메가 버섯 퍼스트 에센스', color:'#8b7a5c', cats:['serum'], pop:74, tag:'탄력 영양 에센스', aff:{elastic:2,dull:2,texture:2}},
    {id:'medicubeMist', brand:'메디큐브', name:'PDRN 핑크 콜라겐 젤리 미스트 세럼', img:PIMG.medicubeMist, color:'#a86f7a', cats:['serum'], pop:81, tag:'PDRN 재생 미스트', aff:{elastic:2,darkcircle:2,dryness:2,dull:1,scar:1}},
    {id:'esnature', brand:'에스네이처', name:'아쿠아 스쿠알란 수분크림', color:'#6b8b8b', cats:['cream'], pop:77, tag:'수분 진정 크림', aff:{dryness:3,redness:1,flake:1}},
    {id:'drg', brand:'닥터지', name:'레드 블레미쉬 클리어 수딩 토너', img:PIMG.drg, color:'#a85c5c', cats:['toner'], pop:88, tag:'트러블 진정 토너', aff:{acne:3,blemish:2,redness:3,shave:2}},
    {id:'roundlabMadeca', brand:'라운드랩', name:'마데카 크림', color:'#5c8b6f', cats:['cream'], pop:85, tag:'재생 진정 크림', aff:{redness:2,acne:2,shave:2,ingrown:2,elastic:1}},
    {id:'cosrxBHA', brand:'코스알엑스', name:'BHA 블랙헤드 파워 리퀴드', color:'#8b6f47', cats:['toner'], pop:84, tag:'모공 각질 케어', aff:{blackhead:3,pore:2,flake:2,ingrown:2,texture:2}},
    {id:'innisfree', brand:'이니스프리', name:'그린티 클렌징폼', color:'#5c8b6f', cats:['cleanser'], pop:75, tag:'산뜻한 세안', aff:{blackhead:2,oil:2}},
    {id:'estraCleanser', brand:'에스트라', name:'아토베리어365 클렌징폼', color:'#6b7a8b', cats:['cleanser'], pop:76, tag:'저자극 클렌징', aff:{dryness:2,redness:1}},
    {id:'roundlabBirch', brand:'라운드랩', name:'자작나무 수분크림', color:'#5c8b6f', cats:['cream'], pop:80, tag:'수분 진정', aff:{dryness:2,ingrown:1,redness:1}},
    {id:'physiogel', brand:'피지오겔', name:'데일리 모이스쳐 테라피 에센스 인 토너', img:PIMG.physiogel, color:'#a86f6f', cats:['toner'], pop:78, tag:'저자극 수분 토너', aff:{dryness:2,redness:2,shave:2,darkcircle:1,flake:2}},
    /* --- 스킨케어 로션 라인 --- */
    {id:'illiyoonLotion', brand:'일리윤', name:'세라마이드 아토 로션', color:'#8ba0b0', cats:['lotion'], pop:83, tag:'세라마이드 보습', aff:{dryness:3,flake:2,redness:1}},
    {id:'cnpLotion', brand:'CNP', name:'프로폴리스 에너지 앰플 로션', color:'#c9a86a', cats:['lotion'], pop:78, tag:'영양 보습 로션', aff:{dryness:2,dull:2,elastic:1}},
    {id:'roundlabLotion', brand:'라운드랩', name:'1025 독도 로션', color:'#5c7a8b', cats:['lotion'], pop:84, tag:'약산성 수분 로션', aff:{dryness:2,redness:1,flake:1}},
    /* --- 아이 메이크업: 아이브로우 --- */
    {id:'clioBrow', brand:'클리오', name:'킬브로우 오토 하드 브로우 펜슬', color:'#6b5744', cats:['brow'], pop:88, tag:'자연스러운 눈썹', aff:{}},
    {id:'etudeBrow', brand:'에뛰드', name:'드로잉 아이브로우', color:'#7a6248', cats:['brow'], pop:82, tag:'입문용 브로우', aff:{}},
    {id:'ridleBrow', brand:'롬앤', name:'한스텝 브로우 펜슬', color:'#5c4a38', cats:['brow'], pop:75, tag:'디테일 표현', aff:{}},
    /* --- 퍼퓸 & 바디: 향수 --- */
    {id:'foretPerfume', brand:'포레', name:'우디 머스크 오 드 퍼퓸', color:'#5c5c7a', cats:['perfume'], pop:86, tag:'포근한 우디', aff:{}},
    {id:'tamburinsPerfume', brand:'탬버린즈', name:'베르가못 시트러스 오 드 퍼퓸', color:'#7a8b5c', cats:['perfume'], pop:84, tag:'상쾌한 시트러스', aff:{}},
    {id:'granhandPerfume', brand:'그랑핸드', name:'뉴트럴 오 드 퍼퓸', color:'#8b7a5c', cats:['perfume'], pop:79, tag:'데일리 은은함', aff:{}},
    /* --- 퍼퓸 & 바디: 바디 로션 --- */
    {id:'aveenoBody', brand:'아비노', name:'데일리 모이스처라이징 바디로션', color:'#6b8b8b', cats:['bodylotion'], pop:85, tag:'귀리 보습', aff:{dryness:3,flake:2}},
    {id:'ceraveBody', brand:'세라비', name:'모이스처라이징 바디 크림', color:'#5c7a8b', cats:['bodylotion'], pop:88, tag:'세라마이드 장벽', aff:{dryness:3,redness:1}},
    {id:'sensodyneBody', brand:'존슨즈', name:'베이비 로션 바디', color:'#9b8b7a', cats:['bodylotion'], pop:74, tag:'순한 데일리 보습', aff:{dryness:2}},
    /* --- 퍼퓸 & 바디: 풋케어 --- */
    {id:'jejuFoot', brand:'제주마유', name:'풋 밸런스 크림', color:'#6b8b6f', cats:['foot'], pop:72, tag:'각질·건조 케어', aff:{dryness:2,flake:2}},
    {id:'scholFoot', brand:'닥터숄', name:'벨벳 스무스 풋 크림', color:'#8b6f5c', cats:['foot'], pop:76, tag:'매끈한 발뒤꿈치', aff:{flake:2,dryness:2}},
    /* --- 퍼퓸 & 바디: 데오라인 --- */
    {id:'niveaDeo', brand:'니베아', name:'프레시 액티브 데오 롤온', color:'#5c6f8b', cats:['deo'], pop:84, tag:'48시간 데오', aff:{}},
    {id:'domeDeo', brand:'돔', name:'데오드란트 스틱 무향', color:'#7a7a8b', cats:['deo'], pop:78, tag:'무향 데오 스틱', aff:{}}
  ];
  window.PRODUCTS = PRODUCTS;

  function buildUserProfile(){
    const c = (window.appState && window.appState.concerns) || new Set();
    const age = (window.appState && window.appState.age) ? window.appState.age : 29;
    const sev = {};
    const BASE = 0.32;
    ALL_TAGS.forEach(t=> sev[t] = BASE);
    const bump = (t,v)=>{ sev[t] = Math.min(1, Math.max(sev[t], v)); };
    if(c.has('oil')){ bump('oil',.95); bump('blackhead',.7); bump('shave',.55); bump('dull',.5); bump('acne',.55); }
    if(c.has('pore')){ bump('pore',.95); bump('blackhead',.7); bump('texture',.65); bump('flake',.5); }
    if(c.has('acne')){ bump('acne',.95); bump('blemish',.75); bump('redness',.65); bump('ingrown',.55); bump('shave',.6); }
    if(c.has('scar')){ bump('scar',.95); bump('pigment',.8); bump('spot',.6); bump('tone',.6); bump('texture',.55); }
    if(age>=30){ bump('elastic',.6); bump('wrinkle',.6); bump('darkcircle',.5); bump('dull',.5); bump('dryness',.5); }
    if(age>=40){ bump('elastic',.85); bump('wrinkle',.85); bump('pigment',.6); }

    /* 추가 설문(체감 상태)을 프로파일에 반영 → 영상 분석 + 설문 통합 추천 */
    const sv = (window.appState && window.appState.survey) || {};
    /* goal은 복수 선택 배열일 수 있으므로 배열로 정규화 */
    const goals = Array.isArray(sv.goal) ? sv.goal : (sv.goal ? [sv.goal] : []);
    const soothing = sv.sensitive==='high' || sv.atopy==='yes' || sv.redness==='high' || goals.indexOf('soothe')>=0;
    if(soothing){ bump('redness',.92); bump('dryness',.75); }
    if(sv.atopy==='yes'){ bump('dryness',.85); bump('flake',.62); bump('redness',.8); }
    if(sv.redness==='high'){ bump('redness',.9); }
    if(sv.oil==='high'){ bump('oil',.9); bump('blackhead',.62); }
    if(sv.oil==='low' || sv.dryness==='high'){ bump('dryness',.9); bump('flake',.6); }
    if(sv.trouble==='high'){ bump('acne',.9); bump('blemish',.68); }
    if(sv.focus==='trouble'){ bump('acne',.85); }
    else if(sv.focus==='pore'){ bump('pore',.85); bump('blackhead',.6); }
    else if(sv.focus==='pigment'){ bump('pigment',.85); bump('spot',.7); bump('tone',.6); }
    else if(sv.focus==='aging'){ bump('elastic',.85); bump('wrinkle',.75); }
    else if(sv.focus==='dry'){ bump('dryness',.9); bump('flake',.6); }
    if(goals.indexOf('hydrate')>=0){ bump('dryness',.85); }
    if(goals.indexOf('bright')>=0){ bump('spot',.8); bump('tone',.7); }
    if(goals.indexOf('pore')>=0){ bump('pore',.8); bump('blackhead',.6); }
    if(goals.indexOf('firm')>=0){ bump('elastic',.8); bump('wrinkle',.7); }

    return { sev:sev, age:age, soothing:soothing };
  }

  function scoreProduct(p, profile){
    let s = 0;
    for(const tag in p.aff){ s += p.aff[tag] * (profile.sev[tag] || 0); }
    s += (p.pop || 70) * 0.012;
    if(profile.soothing){
      /* 저자극·진정 모드: 강한 각질/피지 제거 제품은 후순위로, 진정 성분 제품은 가산 */
      if((p.aff.blackhead || 0) >= 3 || p.id==='cosrxBHA' || p.id==='innisfree'){ s *= 0.6; }
      if((p.aff.redness || 0) >= 2){ s += 0.5; }
    }
    return s;
  }

  function recommendFrom(pool, N, focal){
    const profile = buildUserProfile();
    /* focal: 지금 보고 있는 고민 태그. 그 고민 특화 제품이 범용 제품보다 우선되도록 가중. */
    const scored = pool.map(p=>({
      p:p,
      s: scoreProduct(p, profile) + (focal ? (p.aff[focal] || 0) * 1.7 : 0)
    }));
    const max = scored.reduce((m,x)=> Math.max(m, x.s), 0.0001);
    scored.sort((a,b)=> b.s - a.s);
    return scored.slice(0, N).map((x,i)=> Object.assign({}, x.p, {
      rank: i+1,
      match: Math.round(72 + 27 * (x.s / max))
    }));
  }
  function recommendForConcern(tag, N){
    return recommendFrom(PRODUCTS.filter(p=> (p.aff[tag] || 0) > 0), N, tag);
  }
  function recommendForCat(cat, N){
    return recommendFrom(PRODUCTS.filter(p=> p.cats.indexOf(cat) >= 0), N, null);
  }
  window.recommendForConcern = recommendForConcern;
  window.recommendForCat = recommendForCat;

  /* ---------------- optional Supabase catalog (graceful fallback) ---------------- */
  /* Supabase가 설정돼 있으면 products 테이블에서 카탈로그를 불러오고,
     없거나 실패하면 위의 내장 배열을 그대로 사용한다. 매칭 엔진은 동일하게 동작. */
  function normalizeProduct(row){
    return {
      id: row.id, brand: row.brand, name: row.name,
      cats: row.cats || [], pop: row.pop || 70, tag: row.tag || '',
      img: row.img_url || null, color: row.color || '#8b6f47', aff: row.aff || {}
    };
  }
  async function loadCatalogFromSupabase(){
    const url = window.SB_URL, key = window.SB_KEY;
    if(!url || !key || url.indexOf('http') !== 0) return;   // 미설정 → 내장 카탈로그 유지
    try{
      const r = await fetch(url + '/rest/v1/products?select=*', {
        headers: { apikey: key, Authorization: 'Bearer ' + key }
      });
      if(!r.ok) throw new Error('HTTP ' + r.status);
      const rows = await r.json();
      if(Array.isArray(rows) && rows.length){
        /* 교체가 아니라 병합: 원격 카탈로그가 오래돼 새 카테고리(브로우·퍼퓸·바디·풋·데오 등)가
           없어도 내장 항목이 유지되어 모든 추천 라인이 빈 화면이 되지 않는다.
           같은 id는 원격(Supabase) 값이 우선. */
        const merged = {};
        PRODUCTS.forEach(p=>{ merged[p.id] = p; });
        rows.map(normalizeProduct).forEach(p=>{ if(p && p.id) merged[p.id] = p; });
        PRODUCTS = Object.values(merged);
        window.PRODUCTS = PRODUCTS;
        /* 현재 열려 있는 추천 화면이 있으면 새 카탈로그로 다시 그린다 */
        if(typeof tierInitialized !== 'undefined' && tierInitialized){
          const active = document.querySelector('.tier-tab.active');
          if(active) renderTier(active.dataset.tier);
        }
      }
    }catch(e){ /* 폴백: 내장 카탈로그 사용 */ }
  }
  loadCatalogFromSupabase();

  /* ---- 1단계 스킨케어 설명 개인화 ----
     설문(체감 상태) 결과로 피부타입/대표 고민을 도출하고,
     {피부타입}_{고민} 조합별 문구 세트에서 골라 렌더링한다. 조합이 없으면 default로 폴백. */
  const ROUTINE_MESSAGES = {
    '지성_여드름트러블':'지성 피부에 트러블 케어가 필요한 당신에게는, 클렌징 후 진정 토너 → 저자극 앰플 → 산뜻한 로션 순서를 추천해요. 유분이 많은 날엔 크림은 생략해도 좋아요.',
    '지성_모공블랙헤드':'지성 피부에 모공 케어가 필요한 당신에게는, 클렌징 후 모공 토너 → 피지 조절 앰플 → 산뜻한 로션 순서를 추천해요.',
    '지성_칙칙함톤':'지성 피부의 칙칙함 개선이 필요한 당신에게는, 클렌징 후 결 정돈 토너 → 비타민 앰플 → 산뜻한 로션 순서를 추천해요.',
    '지성_탄력주름':'지성 피부의 탄력 관리가 필요한 당신에게는, 클렌징 후 결 정돈 토너 → 탄력 앰플 → 산뜻한 로션 순서를 추천해요.',
    '지성_건조함':'유분은 많지만 속은 건조한 당신에게는, 클렌징 후 수분 토너 → 수분 앰플 → 산뜻한 로션 순서를 추천해요.',
    '건성_여드름트러블':'건성 피부에 트러블 케어가 필요한 당신에게는, 클렌징 후 진정 토너 → 저자극 앰플 → 로션 → 보습 크림 순서를 추천해요.',
    '건성_모공블랙헤드':'건성 피부에 모공 케어가 필요한 당신에게는, 클렌징 후 수분 토너 → 모공 케어 앰플 → 로션 → 보습 크림 순서를 추천해요.',
    '건성_칙칙함톤':'건성 피부의 칙칙함 개선을 위해서는, 클렌징 후 보습 토너 → 영양 앰플 → 로션 → 고보습 크림 순서가 효과적이에요.',
    '건성_탄력주름':'건성 피부의 탄력 관리가 필요한 당신에게는, 클렌징 후 보습 토너 → 탄력 앰플 → 로션 → 영양 크림 순서를 추천해요.',
    '건성_건조함':'건조함이 심한 당신에게는, 클렌징 후 보습 토너 → 수분 앰플을 두 번 겹쳐 바르고 → 로션 → 고보습 크림으로 마무리하는 순서를 추천해요.',
    '복합성_여드름트러블':'복합성 피부에 트러블 케어가 필요한 당신에게는, 클렌징 후 진정 토너 → 저자극 앰플 → 가벼운 로션 순서를 추천해요. 건조한 볼에만 크림을 더해주세요.',
    '복합성_모공블랙헤드':'복합성 피부에 모공 케어가 필요한 당신에게는, 클렌징 후 모공 토너 → 피지 조절 앰플 → 산뜻한 로션 순서를 추천해요.',
    '복합성_칙칙함톤':'복합성 피부의 칙칙함 개선을 위해서는, 클렌징 후 결 정돈 토너 → 비타민 앰플 → 로션 순서가 효과적이에요.',
    '복합성_탄력주름':'복합성 피부의 탄력 관리가 필요한 당신에게는, 클렌징 후 토너 → 탄력 앰플 → 로션 → 볼·눈가 위주로 크림 순서를 추천해요.',
    '복합성_건조함':'겉은 번들거려도 속건조가 있는 당신에게는, 클렌징 후 수분 토너 → 수분 앰플 → 로션 순서를 추천해요. 당기는 부위엔 크림을 더해주세요.',
    '민감성_여드름트러블':'민감성 피부에 트러블 케어가 필요한 당신에게는, 클렌징 후 진정 토너 → 저자극 진정 앰플 → 순한 로션 순서를 추천해요. 새 제품은 한 번에 하나씩만 늘려주세요.',
    '민감성_모공블랙헤드':'민감성 피부에 모공 케어가 필요한 당신에게는, 클렌징 후 저자극 토너 → 순한 피지 조절 앰플 → 가벼운 로션 순서를 추천해요. 강한 필링은 피하는 게 좋아요.',
    '민감성_칙칙함톤':'민감성 피부의 칙칙함 개선을 위해서는, 클렌징 후 저자극 토너 → 순한 브라이트닝 앰플 → 로션 → 장벽 크림 순서가 효과적이에요.',
    '민감성_탄력주름':'민감성 피부의 탄력 관리가 필요한 당신에게는, 클렌징 후 저자극 토너 → 진정·탄력 앰플 → 로션 → 장벽 크림 순서를 추천해요.',
    '민감성_건조함':'민감성 피부에 건조함까지 있는 당신에게는, 클렌징 후 저자극 보습 토너 → 진정 앰플 → 로션 → 장벽 크림 순서를 추천해요.',
    'default':'클렌징 후 토너 → 앰플 → 로션 → 크림 순서로 피부 결과 컨디션을 정돈해요.'
  };
  function deriveSkinType(){
    const sv = (window.appState && window.appState.survey) || {};
    if(sv.sensitive==='high' || sv.atopy==='yes' || sv.redness==='high') return '민감성';
    const oily = sv.oil==='high' || sv.trouble==='high';
    const dry = sv.oil==='low' || sv.dryness==='high';
    if(oily && dry) return '복합성';
    if(oily) return '지성';
    if(dry) return '건성';
    if(sv.oil==='mid') return '복합성';
    return null;   /* 설문 미완료 → 폴백 문구 사용 */
  }
  function deriveSkinConcern(){
    const sv = (window.appState && window.appState.survey) || {};
    const focusMap = { trouble:'여드름트러블', pore:'모공블랙헤드', pigment:'칙칙함톤', aging:'탄력주름', dry:'건조함' };
    if(sv.focus && focusMap[sv.focus]) return focusMap[sv.focus];
    const c = (window.appState && window.appState.concerns) || new Set();
    if(c.has('acne')) return '여드름트러블';
    if(c.has('pore') || c.has('oil')) return '모공블랙헤드';
    if(c.has('scar')) return '칙칙함톤';
    return null;
  }
  function getRoutineMessage(){
    const type = deriveSkinType(), concern = deriveSkinConcern();
    return (type && concern && ROUTINE_MESSAGES[type + '_' + concern]) || ROUTINE_MESSAGES['default'];
  }

  /* 단계(step) → 그 안의 라인/세부 카테고리(lines). 각 라인은 카탈로그 cat으로 매칭. */
  const TIERS = [
    { key:'t1', label:'1단계', category:'스킨케어',
      descFn:getRoutineMessage,
      desc:ROUTINE_MESSAGES['default'],
      lines:[
        { label:'토너 라인', sub:'결 정돈·수분', cat:'toner' },
        { label:'앰플 라인', sub:'집중 케어', cat:'serum' },
        { label:'로션 라인', sub:'가벼운 보습', cat:'lotion' },
        { label:'크림 라인', sub:'마무리 보습·장벽', cat:'cream' }
      ] },
    { key:'t2', label:'2단계', category:'선케어',
      desc:'기초 위에 피부 타입에 맞는 선케어로 노화·색소 자국을 예방해요.',
      lines:[ { label:'선케어 라인', sub:'자외선 차단', cat:'sun' } ] },
    { key:'t3', label:'3단계', category:'베이스 메이크업',
      desc:'선케어에 이어 칙칙함 없이 깔끔한 피부로 톤과 결을 정돈해요.',
      lines:[ { label:'피부 표현 라인', sub:'톤·결 보정', cat:'cushion' } ] },
    { key:'t4', label:'4단계', category:'아이메이크업',
      desc:'눈썹 정리로 또렷한 인상을 만들고, 눈매를 자연스럽게 정돈해요.',
      lines:[
        { label:'아이브로우', sub:'눈썹 정리·또렷한 인상', cat:'brow' },
        { label:'아이섀도우', sub:'눈매 연출·자연스러운 분위기', cat:'eye' }
      ] },
    { key:'t5', label:'5단계', category:'퍼퓸&바디케어',
      desc:'향과 바디케어로 하루의 마무리까지 완성해요.',
      lines:[
        { label:'향수 추천', sub:'시그니처 향', cat:'perfume' },
        { label:'바디 로션 추천', sub:'전신 보습', cat:'bodylotion' },
        { label:'풋케어 추천', sub:'발 각질·건조', cat:'foot' },
        { label:'데오라인 추천', sub:'냄새·땀 케어', cat:'deo' }
      ] }
  ];
  let tierInitialized = false;

  function initTierTabs(){
    tierInitialized = true;
    const tabsEl = document.getElementById('tierTabs');
    tabsEl.innerHTML = TIERS.map((t,i)=>
      '<button type="button" class="tier-tab' + (i===0?' active':'') + '" data-tier="' + t.key + '">' + t.category + '</button>'
    ).join('');
    tabsEl.addEventListener('click', onTierTabClick);
    renderTier(TIERS[0].key);
  }

  function onTierTabClick(e){
    const btn = e.target.closest('.tier-tab');
    if(!btn) return;
    const tabsEl = document.getElementById('tierTabs');
    tabsEl.querySelectorAll('.tier-tab').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    renderTier(btn.dataset.tier);
  }

  function renderTier(key){
    const tier = TIERS.find(t=>t.key===key);
    /* descFn이 있으면 사용자 분석 결과 기반 개인화 문구를, 없으면 고정 문구를 표시 */
    document.getElementById('tierDesc').textContent = tier.descFn ? tier.descFn() : tier.desc;
    const rows = tier.lines.map(line=>{
      const products = recommendForCat(line.cat, 3);
      if(!products.length) return '';
      return '<div class="tier-line">' +
        '<div class="tier-line-label">' + line.label +
          (line.sub ? ' <span class="tier-line-sub">· ' + line.sub + '</span>' : '') + '</div>' +
        '<div class="prod-row">' + renderProductCards(products) + '</div>' +
      '</div>';
    }).join('');
    document.getElementById('tierProdRow').innerHTML = rows ||
      '<div class="tier-line"><div class="tier-line-sub">추천 제품을 준비 중이에요.</div></div>';
  }

  /* ---------------- extra concerns ---------------- */
  const EXTRA_CONCERNS = [
    { key:'elastic', label:'탄력 저하', tag:'elastic' },
    { key:'texture', label:'피부결 개선', tag:'texture' },
    { key:'spot', label:'기미', tag:'spot' },
    { key:'blemish', label:'잡티', tag:'blemish' },
    { key:'tone', label:'피부톤 불균일', tag:'tone' },
    { key:'blackhead', label:'블랙헤드', tag:'blackhead' },
    { key:'darkcircle', label:'다크서클', tag:'darkcircle' },
    { key:'shave', label:'면도 트러블', tag:'shave' },
    { key:'ingrown', label:'인그로운 헤어', tag:'ingrown' },
    { key:'dull', label:'얼굴 칙칙함', tag:'dull' },
    { key:'dryness', label:'세안 후 건조함', tag:'dryness' },
    { key:'redness', label:'안면 홍조', tag:'redness' },
    { key:'pigment', label:'색소 침착', tag:'pigment' },
    { key:'flake', label:'얼굴 각질', tag:'flake' }
  ];
  let extraInitialized = false;

  function initExtraTabs(){
    extraInitialized = true;
    const tabsEl = document.getElementById('extraTabs');
    tabsEl.innerHTML = EXTRA_CONCERNS.map((c,i)=>
      '<button type="button" class="extra-tab' + (i===0?' active':'') + '" data-extra="' + c.key + '">' + c.label + '</button>'
    ).join('');
    tabsEl.querySelectorAll('.extra-tab').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        tabsEl.querySelectorAll('.extra-tab').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        renderExtra(btn.dataset.extra);
      });
    });
    renderExtra(EXTRA_CONCERNS[0].key);
  }

  function renderExtra(key){
    const c = EXTRA_CONCERNS.find(c=>c.key===key);
    document.getElementById('extraProdRow').innerHTML = renderProductCards(recommendForConcern(c.tag, 3));
  }

  /* ---------------- community (localStorage + dummy data) ---------------- */
  const CM_CATS = [
    {key:'all', label:'전체'},
    {key:'vote', label:'남좋메/여좋메 투표', color:'#c15c8a'},
    {key:'ba', label:'비포·애프터', color:'#5c7a9b'},
    {key:'mkup_basic', label:'메이크업 입문', color:'#b58b5c'},
    {key:'natural', label:'자연스러운 피부 표현', color:'#7a9b6f'},
    {key:'date_makeup', label:'소개팅 메이크업', color:'#d9564f'},
    {key:'work_makeup', label:'면접/출근 메이크업', color:'#5c6f8b'},
    {key:'cover', label:'트러블 커버 팁', color:'#c98a3c'},
    {key:'review', label:'제품 후기', color:'#8b6f47'},
    {key:'pore', label:'모공', color:'#c86e46'},
    {key:'oil', label:'유분/피지', color:'#c98a3c'},
    {key:'acne', label:'여드름/트러블', color:'#c13c3c'},
    {key:'scar', label:'흉터/자국', color:'#965a96'},
    {key:'sensitive', label:'민감성', color:'#c1666b'},
    {key:'shave', label:'면도 자극', color:'#6b8b6f'}
  ];
  const CM_CAT_LABEL = {};
  CM_CATS.forEach(c=>{ CM_CAT_LABEL[c.key] = c.label; });
  /* 카테고리별 고유 색상: 상단 필터 탭의 dot 색(CM_CATS.color)을 단일 소스로 재사용해
     게시글 카드의 카테고리 라벨과 항상 일치하도록 관리 */
  const CM_CAT_COLOR = {};
  CM_CATS.forEach(c=>{ if(c.color) CM_CAT_COLOR[c.key] = c.color; });
  /* 배경 밝기에 따라 라벨 글자색 자동 결정(밝은 배경→진한 글자, 어두운 배경→흰 글자) */
  function cmCatTextColor(hex){
    const n = parseInt(hex.slice(1), 16);
    const r = (n>>16)&255, g = (n>>8)&255, b = n&255;
    return (0.299*r + 0.587*g + 0.114*b) > 160 ? '#1a1a18' : '#fff';
  }
  function cmCatChip(key){
    const bg = CM_CAT_COLOR[key];
    const style = bg ? ' style="background:'+bg+';color:'+cmCatTextColor(bg)+'"' : '';
    return '<span class="cm-cat-chip"'+style+'>'+esc(CM_CAT_LABEL[key]||key)+'</span>';
  }
  const CM_SKIN_LABEL = {scar:'흉터',pore:'모공',oil:'유분',acne:'여드름',sensitive:'민감성',dry:'건조',elastic:'탄력'};

  const CM_STORE = 'forhim_community_posts_v2';
  const CM_FAV = 'forhim_community_favs';
  const CM_VOTE = 'forhim_community_votes';   /* 사용자가 투표한 항목 {postId: optionKey} */

  function cmSeed(){
    const now = Date.now(); const H = 3600000, D = 86400000;
    const FM = (window.FACE_MALE || null), FF = (window.FACE_FEMALE || null);
    return [
      {id:'v1', cat:'vote', type:'vote', title:'남좋메 vs 여좋메 — 데일리 톤업 어디까지?', body:'출근·소개팅 때 톤업 어디까지 하세요? 투표 부탁드려요 🙏', author:'톤업고민', skin:['oil'], createdAt:now-2*H,
        options:[{key:'natural',label:'가볍게 톤업만 (남좋메)',votes:186},{key:'cover',label:'확실하게 커버 (여좋메)',votes:124}],
        comments:[{id:'cv1',author:'자연파',body:'저는 무조건 가볍게요. 과하면 부담스러워요.',createdAt:now-1*H}]},
      {id:'b1', cat:'ba', type:'ba', title:'화농성 트러블 → 3개월 진정 루틴 비포·애프터', body:'3개월 기록 공유해요. 유분 잡고 진정 위주로 갔어요.', author:'3개월기록', skin:['acne','oil'], createdAt:now-4*H,
        beforePhoto:FM, afterPhoto:FM,
        products:['닥터지 레드 블레미쉬 클리어 수딩 토너','라운드랩 마데카 크림','메디힐 마데카소사이드 선세럼'],
        change:'붉은기와 유분이 눈에 띄게 가라앉고 피부 톤이 밝아졌어요. 트러블 빈도도 확 줄었습니다.',
        comments:[{id:'cb1',author:'트러블탈출',body:'와 진짜 달라지셨네요. 토너 바로 사러 갑니다!',createdAt:now-3*H},{id:'cb2',author:'진정중',body:'선세럼 저도 쓰는데 자극 없어서 좋아요.',createdAt:now-2*H}]},
      {id:'v2', cat:'vote', type:'vote', title:'소개팅 날, 아이브로우 꼭 해야 할까?', body:'눈썹만 정리해도 인상이 산다는데… 다들 어떻게 생각하세요?', author:'소개팅D-1', skin:['pore'], createdAt:now-7*H,
        options:[{key:'yes',label:'해야 인상이 산다',votes:212},{key:'no',label:'자연스러운 게 낫다',votes:97}],
        comments:[]},
      {id:'b2', cat:'ba', type:'ba', title:'면접룩 메이크업 비포·애프터', body:'면접 전날 이렇게 준비했습니다. 과하지 않게 신뢰감 위주로.', author:'취준막바지', skin:['pore'], createdAt:now-1*D,
        beforePhoto:FM, afterPhoto:FM,
        products:['에스트라 아토베리어365 크림','헤라 블랙 쿠션','클리오 킬브로우 펜슬'],
        change:'톤 정리 + 자연스러운 커버로 또렷하고 단정한 인상이 됐어요.',
        comments:[{id:'cb3',author:'인사담당',body:'딱 좋네요. 깔끔한 인상이 제일 중요해요.',createdAt:now-20*H}]},
      {id:'m1', cat:'mkup_basic', type:'normal', title:'남자 메이크업 입문 — 딱 3종만', body:'처음이면 이거 3개로 충분해요. 얇게만 바르세요!', author:'입문가이드', skin:['oil'], createdAt:now-1*D-3*H,
        products:['산뜻한 선크림','내추럴 톤 쿠션','아이브로우 펜슬'], change:null, comments:[]},
      {id:'m2', cat:'date_makeup', type:'normal', title:'소개팅 메이크업, 과하지 않게 하는 법', body:'톤업 위주로 가볍게. 입술만 살짝 생기 주면 끝이에요.', author:'연애고수', skin:['oil'], createdAt:now-2*D,
        products:['정샘물 쿠션','페리페라 틴트'], change:null, comments:[{id:'cm2',author:'첫소개팅',body:'틴트 팁 감사해요! 바로 적용해볼게요.',createdAt:now-1*D-4*H}]},
      {id:'m3', cat:'natural', type:'normal', title:'자연스러운 피부 표현 핵심 팁', body:'한 번에 두껍게 X. 얇게 여러 번 올리는 게 자연스러움의 핵심이에요.', author:'피부표현러', skin:['pore'], createdAt:now-3*D, comments:[]},
      {id:'m4', cat:'cover', type:'normal', title:'트러블 자국 커버 어떻게 하세요?', body:'붉은 자국 위에 뭘 먼저 올려야 티가 안 날까요? 컨실러 순서 궁금해요.', author:'커버초보', skin:['acne'], createdAt:now-4*D, comments:[]}
    ];
  }
  function cmSave(list){ try{ localStorage.setItem(CM_STORE, JSON.stringify(list)); }catch(e){} }
  function cmLoad(){
    try{ const raw = localStorage.getItem(CM_STORE); if(raw){ return JSON.parse(raw); } }catch(e){}
    const seed = cmSeed(); cmSave(seed); return seed;
  }
  function cmSaveFavs(set){ try{ localStorage.setItem(CM_FAV, JSON.stringify(Array.from(set))); }catch(e){} }
  function cmLoadFavs(){ try{ return new Set(JSON.parse(localStorage.getItem(CM_FAV) || '[]')); }catch(e){ return new Set(); } }

  function cmLoadVotes(){ try{ return JSON.parse(localStorage.getItem(CM_VOTE) || '{}'); }catch(e){ return {}; } }
  function cmSaveVotes(v){ try{ localStorage.setItem(CM_VOTE, JSON.stringify(v)); }catch(e){} }

  let cmPosts = cmLoad();
  let cmFavs = cmLoadFavs();
  let cmVotes = cmLoadVotes();
  let cmActiveCat = 'all';
  let cmQuery = '';
  let cmEditingId = null;
  let cmPendingPhoto = null;
  let cmFormType = 'normal';
  function cmSetFormType(t){
    cmFormType = t;
    document.querySelectorAll('#cmFormType .cm-type-btn').forEach(function(b){ b.classList.toggle('on', b.dataset.type===t); });
    const vf = document.getElementById('cmFormVoteFields');
    const bf = document.getElementById('cmFormBaFields');
    if(vf) vf.hidden = (t!=='vote');
    if(bf) bf.hidden = (t!=='ba');
  }

  /* ---- optional Supabase backend + email auth (falls back to localStorage) ---- */
  const SB_ON = !!(window.SB_URL && window.SB_KEY && String(window.SB_URL).indexOf('http') === 0);
  const CM_SESS = 'forhim_sb_session';
  let cmSession = null;
  let cmAuthMode = 'login';
  try{ cmSession = JSON.parse(localStorage.getItem(CM_SESS) || 'null'); }catch(e){}
  function cmLoggedIn(){ return !!(cmSession && cmSession.access_token); }
  function cmUserName(){
    if(window.appState && window.appState.nickname) return window.appState.nickname;
    if(cmSession && cmSession.user && cmSession.user.email) return cmSession.user.email.split('@')[0];
    return '익명';
  }
  function cmSaveSession(s){ cmSession = s; try{ localStorage.setItem(CM_SESS, JSON.stringify(s)); }catch(e){} cmRenderAuth(); }
  function cmLogout(){ cmSession = null; try{ localStorage.removeItem(CM_SESS); }catch(e){} cmRenderAuth(); cmShowToast('로그아웃했어요.'); }
  function sbAuthHeaders(){ return { apikey: window.SB_KEY, 'Content-Type':'application/json' }; }
  function sbRestHeaders(useToken){
    const h = { apikey: window.SB_KEY, 'Content-Type':'application/json' };
    h.Authorization = 'Bearer ' + ((useToken && cmLoggedIn()) ? cmSession.access_token : window.SB_KEY);
    return h;
  }
  async function sbSignup(email, pw){
    const r = await fetch(window.SB_URL + '/auth/v1/signup', { method:'POST', headers:sbAuthHeaders(), body:JSON.stringify({ email:email, password:pw }) });
    return r.json();
  }
  async function sbSignin(email, pw){
    const r = await fetch(window.SB_URL + '/auth/v1/token?grant_type=password', { method:'POST', headers:sbAuthHeaders(), body:JSON.stringify({ email:email, password:pw }) });
    return r.json();
  }
  /* Supabase access tokens expire (~1h). Exchange the refresh_token for a new
     session so a write doesn't silently 401 after the user has been idle. */
  async function cmRefreshToken(){
    if(!(cmSession && cmSession.refresh_token)) return false;
    try{
      const r = await fetch(window.SB_URL + '/auth/v1/token?grant_type=refresh_token',
        { method:'POST', headers:sbAuthHeaders(), body:JSON.stringify({ refresh_token: cmSession.refresh_token }) });
      if(!r.ok) return false;
      const res = await r.json();
      if(res && res.access_token){ cmSaveSession(res); return true; }
    }catch(e){}
    return false;
  }
  /* Authenticated write with one automatic refresh-and-retry on 401/403. */
  async function sbWrite(url, method, bodyObj){
    const build = function(){ return { method:method, headers:sbRestHeaders(true), body:JSON.stringify(bodyObj) }; };
    let r = await fetch(url, build());
    if((r.status === 401 || r.status === 403) && await cmRefreshToken()){
      r = await fetch(url, build());
    }
    return r;
  }
  /* Session is truly gone (refresh failed): clear it quietly and prompt login. */
  function cmForceRelogin(hintEl, msg){
    cmSession = null; try{ localStorage.removeItem(CM_SESS); }catch(e){}
    cmRenderAuth();
    if(hintEl) hintEl.textContent = msg || '세션이 만료됐어요. 다시 로그인 후 등록해주세요.';
    cmOpenAuth();
  }

  /* ---- bridge the Google login into a Supabase community session ---- */
  /* The community stores posts in Supabase with RLS, so it needs a Supabase
     session — separate from the Google OIDC login. To avoid asking the user to
     log in twice, we derive a stable credential from their Google email and
     silently sign in/up. NOTE: demo-grade — the derived password is computable
     from the email, so it is not secure for production. Requires the Supabase
     project's email provider to NOT require email confirmation. */
  function cmDerivePw(email){
    const e = String(email || '').toLowerCase();
    let hash = 5381;
    for(let i=0;i<e.length;i++){ hash = ((hash*33) ^ e.charCodeAt(i)) >>> 0; }
    return 'FORHIM-g-' + hash.toString(36) + '-' + e.length + 'x';
  }
  async function cmBridgeFromGoogle(){
    if(!SB_ON || cmLoggedIn()) return cmLoggedIn();
    if(window.USER_LOGGED_IN !== '1' || !window.USER_EMAIL) return false;
    const email = window.USER_EMAIL, pw = cmDerivePw(email);
    try{
      let res = await sbSignin(email, pw);
      if(!(res && res.access_token)){
        await sbSignup(email, pw);
        res = await sbSignin(email, pw);
      }
      if(res && res.access_token){ cmSaveSession(res); return true; }
    }catch(e){}
    return false;
  }
  /* Ensure a community session before a write: reuse it, else bridge from
     Google, else fall back to the email login modal. */
  async function cmEnsureLogin(){
    if(cmLoggedIn()) return true;
    if(await cmBridgeFromGoogle()) return true;
    cmOpenAuth();
    return false;
  }
  function cmMapRow(p){
    return { id:String(p.id), cat:p.category, title:p.title, body:p.body, photo:p.photo_url||null,
      author:p.author||'익명', skin:p.skin_tags||[], createdAt:p.created_at?new Date(p.created_at).getTime():Date.now(),
      comments:(p.comments||[]).map(function(c){ return { id:String(c.id), author:c.author||'익명', body:c.body, createdAt:c.created_at?new Date(c.created_at).getTime():Date.now() }; })
        .sort(function(a,b){ return a.createdAt - b.createdAt; }) };
  }
  async function cmFetchRemote(){
    const q = '/rest/v1/posts?select=id,category,title,body,photo_url,author,skin_tags,created_at,comments(id,author,body,created_at)&order=created_at.desc';
    const r = await fetch(window.SB_URL + q, { headers: sbRestHeaders(false) });
    if(!r.ok) throw new Error('HTTP ' + r.status);
    return (await r.json()).map(cmMapRow);
  }
  async function cmRefresh(){
    if(!SB_ON) return;
    try{ cmPosts = await cmFetchRemote(); cmRenderCats(); cmRenderList(); }catch(e){ /* keep current data */ }
  }
  function cmNeedLogin(){
    if(cmLoggedIn()) return false;
    cmOpenAuth();
    return true;
  }

  /* ---- auth UI ---- */
  function cmRenderAuth(){
    const el = document.getElementById('cmAuth');
    if(!el) return;
    if(!SB_ON){ el.innerHTML = ''; return; }
    if(cmLoggedIn()){
      el.innerHTML = '<span class="cm-auth-name">'+esc(cmUserName())+'님</span><button type="button" class="cm-auth-btn" id="cmLogoutBtn">로그아웃</button>';
      document.getElementById('cmLogoutBtn').addEventListener('click', cmLogout);
    } else {
      el.innerHTML = '<button type="button" class="cm-auth-btn" id="cmLoginBtn">로그인</button>';
      document.getElementById('cmLoginBtn').addEventListener('click', cmOpenAuth);
    }
  }
  function cmSetAuthMode(m){
    cmAuthMode = m;
    document.getElementById('cmAuthTitle').textContent = (m==='login'?'로그인':'회원가입');
    document.getElementById('cmAuthSubmit').textContent = (m==='login'?'로그인':'회원가입');
    document.getElementById('cmAuthToggle').textContent = (m==='login'?'계정이 없으신가요? 회원가입':'이미 계정이 있으신가요? 로그인');
  }
  function cmOpenAuth(){
    if(!SB_ON){ cmShowToast('로그인은 Supabase 연동 후 사용할 수 있어요.'); return; }
    document.getElementById('cmAuthHint').textContent = '';
    /* Prefill the Google email so a fallback login is one step. */
    const emailInput = document.getElementById('cmAuthEmail');
    if(emailInput && !emailInput.value && window.USER_EMAIL){ emailInput.value = window.USER_EMAIL; }
    document.getElementById('cmAuthModal').hidden = false;
  }
  function cmCloseAuth(){ document.getElementById('cmAuthModal').hidden = true; }
  async function cmAuthSubmit(){
    const email = document.getElementById('cmAuthEmail').value.trim();
    const pw = document.getElementById('cmAuthPw').value;
    const hint = document.getElementById('cmAuthHint');
    if(!email || pw.length < 6){ hint.textContent = '이메일과 6자 이상 비밀번호를 입력해주세요.'; return; }
    hint.textContent = '처리 중...';
    try{
      let res;
      if(cmAuthMode === 'signup'){
        res = await sbSignup(email, pw);
        if(!(res && res.access_token)){ res = await sbSignin(email, pw); }
      } else {
        res = await sbSignin(email, pw);
      }
      if(res && res.access_token){
        cmSaveSession(res); cmCloseAuth(); cmShowToast('로그인되었어요.');
      } else {
        hint.textContent = (res && (res.msg || res.error_description || res.error)) || '실패했어요. 이메일 인증이 필요할 수 있어요.';
      }
    }catch(e){ hint.textContent = '네트워크 오류가 발생했어요.'; }
  }

  const STAR_OUTLINE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 6.5 7 .8-5.2 4.8 1.5 6.9L12 17.8 5.2 21l1.5-6.9L1.5 9.3l7-.8z"/></svg>';
  const STAR_FILL = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 .8-5.2 4.8 1.5 6.9L12 17.8 5.2 21l1.5-6.9L1.5 9.3l7-.8z"/></svg>';
  const EDIT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>';

  const cmViews = {
    list: document.getElementById('cmViewList'),
    detail: document.getElementById('cmViewDetail'),
    write: document.getElementById('cmViewWrite')
  };
  function cmShow(view){
    Object.keys(cmViews).forEach(k=>{ cmViews[k].hidden = (k !== view); });
    window.scrollTo(0,0);
  }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function cmAgo(ts){
    const diff = Date.now()-ts, m=60000, h=3600000, d=86400000;
    if(diff<m) return '방금 전';
    if(diff<h) return Math.floor(diff/m)+'분 전';
    if(diff<d) return Math.floor(diff/h)+'시간 전';
    if(diff<7*d) return Math.floor(diff/d)+'일 전';
    const dt = new Date(ts); return (dt.getMonth()+1)+'/'+dt.getDate();
  }
  function cmSkinTags(arr){
    if(!arr || !arr.length) return '';
    return '<div class="cm-skintags">' + arr.map(function(t){ return '<span class="cm-skintag">#'+(CM_SKIN_LABEL[t]||t)+'</span>'; }).join('') + '</div>';
  }
  function cmToggleFav(id){ if(cmFavs.has(id)) cmFavs.delete(id); else cmFavs.add(id); cmSaveFavs(cmFavs); }

  /* ----- 투표(남좋메/여좋메) ----- */
  function cmVoteTotal(p){ return (p.options||[]).reduce(function(a,o){ return a + (o.votes||0); }, 0); }
  function cmVote(id, optKey){
    const p = cmPosts.find(function(x){ return x.id===id; });
    if(!p || !p.options) return;
    if(cmVotes[id]) return;                 /* 이미 투표함 → 1인 1표 */
    const opt = p.options.find(function(o){ return o.key===optKey; });
    if(!opt) return;
    opt.votes = (opt.votes||0) + 1;
    cmVotes[id] = optKey; cmSaveVotes(cmVotes);
    cmSave(cmPosts);
    cmShowToast('투표 완료! 결과를 확인하세요.');
  }
  function cmRenderVote(p, interactive){
    const total = cmVoteTotal(p) || 1;
    const myVote = cmVotes[p.id];
    const voted = !!myVote;
    return '<div class="cm-vote'+(voted?' voted':'')+'" data-vote-post="'+p.id+'">' +
      (p.options||[]).map(function(o){
        const pct = Math.round((o.votes||0)/total*100);
        const mine = myVote===o.key;
        return '<button type="button" class="cm-vote-opt'+(mine?' mine':'')+'" '+
          (interactive && !voted ? 'data-vote-opt="'+o.key+'"' : 'disabled')+'>' +
          '<div class="cm-vote-fill" style="width:'+(voted?pct:0)+'%"></div>' +
          '<span class="cm-vote-label">'+esc(o.label)+(mine?' ✓':'')+'</span>' +
          (voted?'<span class="cm-vote-pct">'+pct+'%</span>':'') +
        '</button>';
      }).join('') +
      '<div class="cm-vote-total">'+(voted? (total + '명 참여') : '탭해서 투표하고 결과 보기')+'</div>' +
    '</div>';
  }
  function cmBindVote(scope, id){
    scope.querySelectorAll('[data-vote-opt]').forEach(function(b){
      b.addEventListener('click', function(e){ e.stopPropagation(); cmVote(id, b.dataset.voteOpt); cmRenderList(); if(document.getElementById('cmViewDetail') && !document.getElementById('cmViewDetail').hidden){ cmRenderDetail(id); } });
    });
  }

  /* ----- 비포·애프터 ----- */
  function cmRenderBA(p, big){
    const cls = big ? ' big' : '';
    const b = p.beforePhoto, a = p.afterPhoto;
    return '<div class="cm-ba'+cls+'">' +
      '<div class="cm-ba-col"><div class="cm-ba-tag before">BEFORE</div>' +
        (b?'<img class="cm-ba-img before" src="'+b+'" alt="before" />':'<div class="cm-ba-ph">사진 없음</div>') + '</div>' +
      '<div class="cm-ba-col"><div class="cm-ba-tag after">AFTER</div>' +
        (a?'<img class="cm-ba-img" src="'+a+'" alt="after" />':'<div class="cm-ba-ph">사진 없음</div>') + '</div>' +
    '</div>';
  }
  function cmRenderProducts(p){
    if(!p.products || !p.products.length) return '';
    return '<div class="cm-extra"><div class="cm-extra-label">사용 제품</div>' +
      '<div class="cm-prod-list">' + p.products.map(function(pr,i){
        return '<div class="cm-prod-item"><span class="cm-prod-no">'+(i+1)+'</span>'+esc(pr)+'</div>';
      }).join('') + '</div></div>';
  }
  function cmRenderChange(p){
    if(!p.change) return '';
    return '<div class="cm-extra"><div class="cm-extra-label">변화 포인트</div>' +
      '<div class="cm-change">'+esc(p.change)+'</div></div>';
  }

  const cmToast = document.getElementById('toast');
  function cmShowToast(msg){ cmToast.textContent = msg; cmToast.classList.add('show'); setTimeout(function(){ cmToast.classList.remove('show'); }, 2000); }

  /* ----- categories ----- */
  function cmRenderCats(){
    const el = document.getElementById('cmCats');
    const favCount = cmPosts.filter(function(p){ return cmFavs.has(p.id); }).length;
    let html = CM_CATS.map(function(c){
      const dot = c.color ? '<span class="cm-cat-dot" style="background:'+c.color+'"></span>' : '';
      return '<button type="button" class="cm-cat'+(cmActiveCat===c.key?' active':'')+'" data-cat="'+c.key+'">'+dot+c.label+'</button>';
    }).join('');
    html += '<button type="button" class="cm-cat fav'+(cmActiveCat==='__fav'?' active':'')+'" data-cat="__fav">★ 즐겨찾기'+(favCount?' '+favCount:'')+'</button>';
    el.innerHTML = html;
  }

  /* ----- list ----- */
  function cmFilter(){
    let list = cmPosts.slice();
    if(cmActiveCat==='__fav'){ list = list.filter(function(p){ return cmFavs.has(p.id); }); }
    else if(cmActiveCat!=='all'){ list = list.filter(function(p){ return p.cat===cmActiveCat; }); }
    if(cmQuery){ const q = cmQuery.toLowerCase(); list = list.filter(function(p){ return (p.title+' '+p.body).toLowerCase().indexOf(q)>=0; }); }
    list.sort(function(a,b){ return b.createdAt - a.createdAt; });
    return list;
  }
  function cmRenderList(){
    const listEl = document.getElementById('cmList');
    const emptyEl = document.getElementById('cmEmpty');
    const list = cmFilter();
    emptyEl.hidden = list.length > 0;
    listEl.innerHTML = list.map(function(p){
      const fav = cmFavs.has(p.id);
      const typeBadge = p.type==='vote' ? '<span class="cm-type-badge vote">투표</span>'
        : p.type==='ba' ? '<span class="cm-type-badge ba">비포·애프터</span>' : '';
      let mid;
      if(p.type==='vote'){ mid = cmRenderVote(p, true); }
      else if(p.type==='ba'){ mid = cmRenderBA(p, false) + (p.change ? '<div class="cm-card-body">'+esc(p.change)+'</div>' : ''); }
      else { mid = (p.photo ? '<img class="cm-card-thumb" src="'+p.photo+'" alt="" />' : '') + '<div class="cm-card-body">'+esc(p.body)+'</div>'; }
      return '<article class="cm-card" data-id="'+p.id+'">'+
        '<div class="cm-card-top">'+
          cmCatChip(p.cat)+ typeBadge +
          '<button type="button" class="cm-fav'+(fav?' on':'')+'" data-fav="'+p.id+'" aria-label="즐겨찾기">'+(fav?STAR_FILL:STAR_OUTLINE)+'</button>'+
        '</div>'+
        '<div class="cm-card-title">'+esc(p.title)+'</div>'+
        cmSkinTags(p.skin)+
        mid+
        '<div class="cm-card-foot">'+
          '<div class="avatar">'+esc((p.author||'익')[0])+'</div>'+
          '<div><div class="cm-author">'+esc(p.author||'익명')+'</div><div class="cm-time">'+cmAgo(p.createdAt)+'</div></div>'+
          '<div class="cm-card-stats"><span>'+CHAT_SVG+(p.comments?p.comments.length:0)+'</span></div>'+
        '</div>'+
      '</article>';
    }).join('');
  }

  /* ----- detail ----- */
  function cmRenderComments(p){
    if(!p.comments || !p.comments.length) return '<div class="cm-time" style="padding:8px 0;">아직 댓글이 없어요. 첫 댓글을 남겨보세요.</div>';
    return p.comments.map(function(c){
      return '<div class="cm-comment"><div class="avatar">'+esc((c.author||'익')[0])+'</div>'+
        '<div class="cm-comment-main"><b>'+esc(c.author||'익명')+'</b><span class="cm-time">'+cmAgo(c.createdAt)+'</span>'+
        '<p>'+esc(c.body)+'</p></div></div>';
    }).join('');
  }
  async function cmAddComment(id){
    const input = document.getElementById('cmCommentInput');
    const val = input.value.trim();
    if(!val) return;
    if(SB_ON){
      if(!(await cmEnsureLogin())) return;
      try{
        const r = await sbWrite(window.SB_URL + '/rest/v1/comments', 'POST',
          { post_id:id, user_id:cmSession.user.id, author:cmUserName(), body:val });
        if(r.status === 401 || r.status === 403){ cmForceRelogin(null, ''); cmShowToast('세션이 만료됐어요. 다시 로그인해주세요.'); return; }
        if(!r.ok) throw new Error('HTTP ' + r.status);
        await cmRefresh(); cmRenderDetail(id);
      }catch(e){ cmShowToast('댓글 등록에 실패했어요.'); }
      return;
    }
    const p = cmPosts.find(function(x){ return x.id===id; });
    if(!p.comments) p.comments = [];
    p.comments.push({ id:'c'+Date.now(), author:(window.appState.nickname||'익명'), body:val, createdAt:Date.now() });
    cmSave(cmPosts);
    cmRenderDetail(id);
  }
  function cmRenderDetail(id){
    const p = cmPosts.find(function(x){ return x.id===id; });
    if(!p) return;
    const fav = cmFavs.has(p.id);
    document.getElementById('cmDetailCard').innerHTML =
      '<div class="cm-detail-head">'+
        cmCatChip(p.cat)+
        '<div class="cm-detail-actions">'+
          '<button type="button" class="cm-icon-btn'+(fav?' on':'')+'" id="cmDetailFav">'+(fav?STAR_FILL:STAR_OUTLINE)+(fav?'저장됨':'즐겨찾기')+'</button>'+
          '<button type="button" class="cm-icon-btn" id="cmDetailEdit">'+EDIT_SVG+'수정</button>'+
        '</div>'+
      '</div>'+
      '<h2 class="cm-detail-title">'+esc(p.title)+'</h2>'+
      '<div class="cm-detail-meta"><div class="avatar">'+esc((p.author||'익')[0])+'</div>'+
        '<div><div class="cm-author">'+esc(p.author||'익명')+'</div><div class="cm-time">'+cmAgo(p.createdAt)+'</div></div></div>'+
      cmSkinTags(p.skin)+
      (p.type==='vote'
        ? cmRenderVote(p, true) + (p.body?'<div class="cm-detail-body">'+esc(p.body)+'</div>':'')
        : p.type==='ba'
          ? cmRenderBA(p, true) + (p.body?'<div class="cm-detail-body">'+esc(p.body)+'</div>':'') + cmRenderProducts(p) + cmRenderChange(p)
          : (p.photo ? '<img class="cm-detail-photo" src="'+p.photo+'" alt="첨부 사진" />' : '') + '<div class="cm-detail-body">'+esc(p.body)+'</div>' + cmRenderProducts(p) + cmRenderChange(p)
      )+
      '<div class="cm-comments">'+
        '<div class="cm-comments-title">댓글 '+(p.comments?p.comments.length:0)+'</div>'+
        '<div id="cmCommentList">'+cmRenderComments(p)+'</div>'+
        '<div class="cm-comment-form">'+
          '<input type="text" id="cmCommentInput" placeholder="댓글을 남겨보세요" maxlength="300" />'+
          '<button type="button" class="btn btn-dark btn-sm" id="cmCommentSubmit">등록</button>'+
        '</div>'+
      '</div>';
    document.getElementById('cmDetailCard').querySelectorAll('[data-vote-opt]').forEach(function(b){
      b.addEventListener('click', function(){ cmVote(p.id, b.dataset.voteOpt); cmRenderDetail(p.id); cmRenderList(); });
    });
    document.getElementById('cmDetailFav').addEventListener('click', function(){ cmToggleFav(p.id); cmRenderDetail(p.id); cmRenderCats(); });
    document.getElementById('cmDetailEdit').addEventListener('click', function(){ cmOpenWrite(p.id); });
    document.getElementById('cmCommentSubmit').addEventListener('click', function(){ cmAddComment(p.id); });
    document.getElementById('cmCommentInput').addEventListener('keydown', function(e){ if(e.key==='Enter'){ cmAddComment(p.id); } });
  }
  function cmOpenDetail(id){ cmRenderDetail(id); cmShow('detail'); }

  /* ----- write / edit ----- */
  function cmPopulateCatSelect(){
    document.getElementById('cmFormCat').innerHTML = CM_CATS.filter(function(c){ return c.key!=='all'; })
      .map(function(c){ return '<option value="'+c.key+'">'+c.label+'</option>'; }).join('');
  }
  function cmOpenWrite(id){
    cmEditingId = id || null;
    cmPendingPhoto = null;
    document.getElementById('cmFormHint').textContent = '';
    const catSel = document.getElementById('cmFormCat');
    const titleInput = document.getElementById('cmFormTitleInput');
    const bodyInput = document.getElementById('cmFormBody');
    const preview = document.getElementById('cmPhotoPreview');
    const pimg = document.getElementById('cmPhotoImg');
    const opt1 = document.getElementById('cmFormOpt1'), opt2 = document.getElementById('cmFormOpt2');
    const prodInput = document.getElementById('cmFormProducts'), changeInput = document.getElementById('cmFormChange');
    opt1.value = ''; opt2.value = ''; prodInput.value = ''; changeInput.value = '';
    if(id){
      const p = cmPosts.find(function(x){ return x.id===id; });
      document.getElementById('cmFormTitle').textContent = '글 수정';
      catSel.value = p.cat; titleInput.value = p.title; bodyInput.value = p.body || '';
      cmPendingPhoto = p.photo || null;
      cmSetFormType(p.type || 'normal');
      if(p.type==='vote' && p.options){ opt1.value = (p.options[0]||{}).label || ''; opt2.value = (p.options[1]||{}).label || ''; }
      if(p.type==='ba'){ prodInput.value = (p.products||[]).join('\\n'); changeInput.value = p.change || ''; }
      document.getElementById('cmFormSubmit').textContent = '수정 완료';
    } else {
      document.getElementById('cmFormTitle').textContent = '새 글 남기기';
      catSel.value = (cmActiveCat!=='all' && cmActiveCat!=='__fav') ? cmActiveCat : CM_CATS[1].key;
      titleInput.value = ''; bodyInput.value = '';
      cmSetFormType('normal');
      document.getElementById('cmFormSubmit').textContent = '등록하기';
    }
    if(cmPendingPhoto){ pimg.src = cmPendingPhoto; preview.classList.add('show'); }
    else { preview.classList.remove('show'); pimg.removeAttribute('src'); }
    document.getElementById('cmFormPhoto').value = '';
    cmShow('write');
  }
  async function cmSubmitForm(){
    const cat = document.getElementById('cmFormCat').value;
    const title = document.getElementById('cmFormTitleInput').value.trim();
    const body = document.getElementById('cmFormBody').value.trim();
    const hint = document.getElementById('cmFormHint');
    const o1 = document.getElementById('cmFormOpt1').value.trim();
    const o2 = document.getElementById('cmFormOpt2').value.trim();
    const prods = document.getElementById('cmFormProducts').value.split('\\n').map(function(s){ return s.trim(); }).filter(Boolean);
    const change = document.getElementById('cmFormChange').value.trim();
    if(!title){ hint.textContent = '제목을 입력해주세요.'; return; }
    if(cmFormType==='vote'){ if(!o1 || !o2){ hint.textContent = '투표 선택지 2개를 입력해주세요.'; return; } }
    else if(cmFormType!=='ba'){ if(!body){ hint.textContent = '내용을 입력해주세요.'; return; } }
    /* 유형별 추가 필드 */
    function applyTypeFields(obj){
      obj.type = cmFormType;
      if(cmFormType==='vote'){ obj.options = [{key:'a',label:o1,votes:0},{key:'b',label:o2,votes:0}]; }
      else { obj.options = null; }
      if(cmFormType==='ba'){ obj.products = prods; obj.change = change||null; obj.beforePhoto = obj.beforePhoto||null; obj.afterPhoto = cmPendingPhoto||null; }
      else { obj.products = prods.length?prods:(obj.products||null); obj.change = change||(obj.change||null); }
    }

    if(SB_ON){
      if(!(await cmEnsureLogin())) return;
      hint.textContent = '';
      try{
        if(cmEditingId){
          const r = await sbWrite(window.SB_URL + '/rest/v1/posts?id=eq.' + encodeURIComponent(cmEditingId),
            'PATCH', { category:cat, title:title, body:body, photo_url:cmPendingPhoto });
          if(r.status === 401 || r.status === 403){ cmForceRelogin(hint); return; }
          if(!r.ok) throw new Error('HTTP ' + r.status);
          cmShowToast('글이 수정되었어요.');
          await cmRefresh(); cmOpenDetail(cmEditingId);
        } else {
          const ins = { user_id:cmSession.user.id, author:cmUserName(), category:cat, title:title,
            body:body, photo_url:cmPendingPhoto, skin_tags:Array.from(window.appState.concerns||[]) };
          const r = await sbWrite(window.SB_URL + '/rest/v1/posts', 'POST', ins);
          if(r.status === 401 || r.status === 403){ cmForceRelogin(hint); return; }
          if(!r.ok) throw new Error('HTTP ' + r.status);
          cmShowToast('글이 등록되었어요.');
          cmActiveCat = 'all'; cmQuery = ''; document.getElementById('cmSearch').value = '';
          await cmRefresh(); cmShow('list');
        }
      }catch(e){ hint.textContent = '저장에 실패했어요. 잠시 후 다시 시도해주세요.'; }
      return;
    }

    if(cmEditingId){
      const p = cmPosts.find(function(x){ return x.id===cmEditingId; });
      p.cat = cat; p.title = title; p.body = body; p.photo = cmPendingPhoto;
      applyTypeFields(p);
      cmSave(cmPosts);
      cmShowToast('글이 수정되었어요.');
      cmOpenDetail(cmEditingId);
    } else {
      const np = { id:'p'+Date.now(), cat:cat, title:title, body:body, photo:cmPendingPhoto,
        author:(window.appState.nickname||'익명'),
        skin:Array.from(window.appState.concerns||[]),
        createdAt:Date.now(), comments:[] };
      applyTypeFields(np);
      cmPosts.unshift(np);
      cmSave(cmPosts);
      cmShowToast('글이 등록되었어요.');
      cmActiveCat = 'all'; cmQuery = ''; document.getElementById('cmSearch').value = '';
      cmRenderCats(); cmRenderList(); cmShow('list');
    }
  }
  function cmHandlePhoto(file){
    if(!file) return;
    const reader = new FileReader();
    reader.onload = function(e){
      const img = new Image();
      img.onload = function(){
        const max = 900; let w = img.width, h = img.height;
        if(w>max || h>max){ const r = Math.min(max/w, max/h); w = Math.round(w*r); h = Math.round(h*r); }
        const canvas = document.createElement('canvas'); canvas.width = w; canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        cmPendingPhoto = canvas.toDataURL('image/jpeg', 0.72);
        document.getElementById('cmPhotoImg').src = cmPendingPhoto;
        document.getElementById('cmPhotoPreview').classList.add('show');
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  /* ----- wire up ----- */
  cmPopulateCatSelect();
  cmRenderCats();
  cmRenderList();
  cmRenderAuth();
  if(SB_ON){
    cmRefresh();
    /* If already signed in with Google, bridge into a Supabase session now so
       the community shows as logged in and writes work without a 2nd login. */
    if(!cmLoggedIn() && window.USER_LOGGED_IN === '1'){ cmBridgeFromGoogle(); }
  }

  document.getElementById('cmCats').addEventListener('click', function(e){
    const btn = e.target.closest('.cm-cat'); if(!btn) return;
    cmActiveCat = btn.dataset.cat; cmRenderCats(); cmRenderList();
  });
  document.getElementById('cmSearch').addEventListener('input', function(e){ cmQuery = e.target.value.trim(); cmRenderList(); });
  document.getElementById('cmList').addEventListener('click', function(e){
    const vopt = e.target.closest('[data-vote-opt]');
    if(vopt){ e.stopPropagation(); const vp = vopt.closest('[data-vote-post]'); if(vp){ cmVote(vp.dataset.votePost, vopt.dataset.voteOpt); cmRenderList(); } return; }
    const fav = e.target.closest('.cm-fav');
    if(fav){ e.stopPropagation(); cmToggleFav(fav.dataset.fav); cmRenderCats(); cmRenderList(); return; }
    const card = e.target.closest('.cm-card'); if(card){ cmOpenDetail(card.dataset.id); }
  });
  document.getElementById('cmWriteBtn').addEventListener('click', function(){ cmOpenWrite(null); });
  document.getElementById('cmDetailBack').addEventListener('click', function(){ cmRenderList(); cmShow('list'); });
  document.getElementById('cmWriteBack').addEventListener('click', function(){ cmShow('list'); });
  document.getElementById('cmFormCancel').addEventListener('click', function(){ cmShow('list'); });
  document.getElementById('cmFormSubmit').addEventListener('click', cmSubmitForm);
  document.querySelectorAll('#cmFormType .cm-type-btn').forEach(function(b){
    b.addEventListener('click', function(){ cmSetFormType(b.dataset.type); });
  });
  document.getElementById('cmFormPhoto').addEventListener('change', function(e){ cmHandlePhoto(e.target.files[0]); });
  document.getElementById('cmPhotoRemove').addEventListener('click', function(){
    cmPendingPhoto = null;
    document.getElementById('cmPhotoPreview').classList.remove('show');
    document.getElementById('cmFormPhoto').value = '';
  });
  document.getElementById('cmAuthClose').addEventListener('click', cmCloseAuth);
  document.getElementById('cmAuthToggle').addEventListener('click', function(){ cmSetAuthMode(cmAuthMode==='login'?'signup':'login'); });
  document.getElementById('cmAuthSubmit').addEventListener('click', cmAuthSubmit);
  document.getElementById('cmAuthPw').addEventListener('keydown', function(e){ if(e.key==='Enter'){ cmAuthSubmit(); } });

})();
</script>
</body>
</html>
"""

def _secret(key: str, default: str = "") -> str:
    """Read a value from st.secrets, tolerating a missing secrets file."""
    try:
        return str(st.secrets.get(key, default))
    except Exception:
        return default


def _auth_configured() -> bool:
    """True only when a [auth] block exists in secrets (Google OIDC set up)."""
    try:
        return "auth" in st.secrets
    except Exception:
        return False


# Real Google login via Streamlit's native OIDC (st.login/st.user). This runs at
# the Python layer because OAuth cannot complete inside the sandboxed iframe.
# When [auth] is not configured, everything below is skipped and the in-app
# demo (simulated social login) keeps working unchanged.
auth_on = _auth_configured()
logged_in = False
user_email = ""
user_name = ""
app_url = ""
if auth_on:
    # Derive the app's own URL from the configured redirect_uri so the demo
    # (inside the iframe) can navigate the top window back here to start/stop
    # login. redirect_uri looks like "https://…/oauth2callback".
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

    # No standalone button at the top: login/logout are initiated from within
    # the membership flow, which navigates the top window to ?login=google or
    # ?logout=1. OAuth still runs here because it can't complete in the iframe.
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
            # Clean the URL so a later refresh doesn't look like a re-login.
            del st.query_params["login"]
    except Exception:
        pass

# Optional Supabase config. When absent, the frontend falls back to its
# built-in product catalog, so the demo keeps working with no secrets set.
supabase_url = _secret("SUPABASE_URL")
supabase_key = _secret("SUPABASE_ANON_KEY")

DEMO_HTML = DEMO_HTML.replace("__LOGO_SRC__", logo_data_uri)
DEMO_HTML = DEMO_HTML.replace("__SUPABASE_URL__", supabase_url)
DEMO_HTML = DEMO_HTML.replace("__SUPABASE_KEY__", supabase_key)
DEMO_HTML = DEMO_HTML.replace("__AUTH_ON__", json.dumps("1" if auth_on else ""))
DEMO_HTML = DEMO_HTML.replace("__USER_LOGGED_IN__", json.dumps("1" if logged_in else ""))
DEMO_HTML = DEMO_HTML.replace("__USER_EMAIL__", json.dumps(user_email))
DEMO_HTML = DEMO_HTML.replace("__USER_NAME__", json.dumps(user_name))
DEMO_HTML = DEMO_HTML.replace("__APP_URL__", json.dumps(app_url))
DEMO_HTML = DEMO_HTML.replace("__FACE_MALE__", face_male_uri)
DEMO_HTML = DEMO_HTML.replace("__FACE_FEMALE__", face_female_uri)
DEMO_HTML = DEMO_HTML.replace("__OY_RANKING__", json.dumps(oy_ranking, ensure_ascii=False))
DEMO_HTML = DEMO_HTML.replace("__LOOK_IMGS__", json.dumps(look_imgs))
DEMO_HTML = DEMO_HTML.replace("__PROD_IMGS__", json.dumps(prod_imgs))

# Sidebar view switch: main demo vs. the face-model preview page. The preview
# reuses the standalone face-model-preview.html (same faceSVG code as the demo).
view = st.sidebar.radio("화면", ["데모 앱", "얼굴 모델 미리보기"], index=0)
# 관리자 확인용: 올리브영 랭킹 데이터 갱신 시점
st.sidebar.caption(
    f"랭킹 데이터: {oy_ranking.get('updatedAt', '-')} · {oy_ranking.get('source', '-')}"
)

if view == "얼굴 모델 미리보기":
    preview_path = Path(__file__).parent / "face-model-preview.html"
    try:
        st.iframe(preview_path.read_text(encoding="utf-8"), height="content", width="stretch")
    except Exception:
        st.error("미리보기 파일(face-model-preview.html)을 찾을 수 없어요.")
else:
    st.iframe(DEMO_HTML, height="content", width="stretch")
