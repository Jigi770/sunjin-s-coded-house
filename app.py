import base64
import json
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="FOR HIM - Men's Beauty AI Demo", layout="wide")

logo_path = Path(__file__).parent / "로고.png"
logo_data_uri = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")

DEMO_HTML = """
<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FOR HIM — Men's Beauty AI Demo</title>
<script>window.SB_URL="__SUPABASE_URL__";window.SB_KEY="__SUPABASE_KEY__";window.AUTH_ON=__AUTH_ON__;window.USER_LOGGED_IN=__USER_LOGGED_IN__;window.USER_EMAIL=__USER_EMAIL__;window.USER_NAME=__USER_NAME__;</script>
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
  .prod-card.rank-1{border-color:var(--gold);background:linear-gradient(180deg,#fdf8ee,var(--bg));}
  .prod-cart-btn{
    margin-top:14px;padding:9px 0;border-radius:999px;background:var(--dark);color:#fff;
    font-size:11.5px;font-weight:700;
  }
  .prod-card.rank-1 .prod-cart-btn{background:var(--gold);color:#1a1a18;}
  .prod-rank{
    position:absolute;top:12px;left:12px;font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;
    background:var(--dark);color:#fff;z-index:1;
  }
  .prod-card.rank-1 .prod-rank{background:var(--gold);color:#1a1a18;}
  .prod-icon{width:58px;height:72px;border-radius:11px 11px 5px 5px;margin:14px auto 12px;position:relative;}
  .prod-icon::before{content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:24px;height:10px;border-radius:3px;background:rgba(0,0,0,.28);}
  .prod-photo{
    width:100%;height:150px;border-radius:12px;margin:0 auto 12px;background:#fff;
    display:flex;align-items:center;justify-content:center;overflow:hidden;
  }
  .prod-photo img{width:100%;height:100%;object-fit:contain;padding:8px;}
  .prod-brand{font-size:11.5px;font-weight:700;color:var(--ink-soft);}
  .prod-name{font-size:13.5px;font-weight:700;color:var(--ink);margin-top:4px;line-height:1.35;min-height:36px;}
  .prod-tag{display:inline-block;margin-top:8px;font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent);}
  .prod-tags{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;margin-top:8px;}
  .prod-tags .prod-tag{margin-top:0;}
  .prod-match{font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;background:#eef1e7;color:#54634a;}
  .prod-card.rank-1 .prod-match{background:#f6ecd6;color:#9a7b3f;}

  /* ---------- EXTRA CONCERNS ---------- */
  .extra-tabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;margin-top:20px;}
  .extra-tab{
    flex:0 0 auto;padding:9px 15px;border-radius:999px;border:1.5px solid var(--line);background:var(--bg);
    color:var(--ink-soft);font-size:12.5px;font-weight:700;font-family:inherit;cursor:pointer;white-space:nowrap;transition:all .15s ease;
  }
  .extra-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;}

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

  /* ---------- DIAGNOSIS RESULT (report dashboard) ---------- */
  .diagnosis{
    background:linear-gradient(180deg,#fbf8f4,#f3ede4);opacity:0;transition:opacity .5s ease;padding:32px 24px;
    --db-brown:#8a6a52; --db-brown-soft:#efe4d8; --db-line:#e6dccd;
  }
  .diagnosis.visible{opacity:1;}
  .diag-card{width:100%;max-width:1180px;}
  .diag-back{
    display:inline-flex;align-items:center;gap:6px;padding:8px 14px 8px 10px;border-radius:999px;
    border:1.5px solid var(--db-line);background:#fff;color:#8a8072;font-size:13px;font-weight:700;
    font-family:inherit;cursor:pointer;margin-bottom:18px;transition:border-color .15s ease,color .15s ease;
  }
  .diag-back:hover{border-color:var(--db-brown);color:var(--db-brown);}
  .diag-back svg{width:16px;height:16px;}
  .diag-title{font-size:clamp(19px,3vw,23px);margin-top:8px;font-weight:700;letter-spacing:-.02em;color:#2b241d;}
  .diag-face-title,.diag-summary-title{font-size:12px;font-weight:700;letter-spacing:.06em;color:#a89a86;text-transform:uppercase;margin-bottom:12px;}

  .diag-report{
    display:grid;grid-template-columns:1fr 1.25fr 1fr;grid-template-areas:"info face score";gap:22px;
    align-items:start;
  }
  .diag-info-panel,.diag-face-panel,.diag-scorelist{
    background:#fffdfa;border:1px solid var(--db-line);border-radius:24px;padding:26px;
    box-shadow:0 10px 28px rgba(120,96,68,.06);
  }
  .diag-info-panel{grid-area:info;}
  .diag-face-panel{grid-area:face;text-align:center;}
  .diag-scorelist{grid-area:score;}

  .diag-score-hero{display:flex;align-items:baseline;gap:6px;margin-top:16px;}
  .diag-score-hero b{font-size:52px;font-weight:800;color:var(--db-brown);letter-spacing:-.02em;line-height:1;}
  .diag-score-hero span{font-size:14px;color:#a89a86;font-weight:700;}
  .diag-score-tag{
    display:inline-block;margin-top:10px;font-size:11.5px;font-weight:700;color:var(--db-brown);
    background:var(--db-brown-soft);padding:5px 12px;border-radius:999px;
  }
  .diag-sentence{
    margin-top:16px;font-size:13.5px;color:#5c5346;line-height:1.7;padding-top:16px;border-top:1px solid var(--db-line);
  }
  .diag-userinfo{margin-top:16px;padding-top:16px;border-top:1px solid var(--db-line);}
  .diag-userinfo div{display:flex;justify-content:space-between;padding:6px 0;font-size:13px;}
  .diag-userinfo span{color:#a89a86;}
  .diag-userinfo b{color:#2b241d;font-weight:700;}
  #diagCta{margin-top:20px;width:100%;padding:14px;font-size:15px;background:var(--db-brown);}
  #diagCta:hover{opacity:.9;}

  .face-map{position:relative;width:170px;height:206px;margin:8px auto 0;}
  .face-ear{position:absolute;top:44%;width:11%;height:16%;border-radius:50%;background:#f1ede4;border:1.5px solid #ddd6c6;}
  .face-ear.left{left:-4%;}
  .face-ear.right{right:-4%;}
  .face-shape{position:absolute;inset:0;background:#f4f0e8;border:1.5px solid #ddd6c6;border-radius:48% 48% 44% 44% / 58% 58% 42% 42%;overflow:hidden;}
  .face-zone{position:absolute;border-radius:50%;transform:translate(-50%,-50%);opacity:0;transition:opacity .6s ease;}
  .face-zone[data-zone="tzone"]{
    top:20%;left:50%;width:26%;height:46%;border-radius:50% 50% 40% 40% / 60% 60% 40% 40%;
    background:repeating-linear-gradient(115deg, rgba(201,138,60,.5) 0 3px, rgba(201,138,60,0) 3px 7px);
  }
  .face-zone[data-zone="cheek-l"],.face-zone[data-zone="cheek-r"]{
    top:54%;width:30%;height:22%;
    background-image:radial-gradient(circle, rgba(200,110,70,.85) 0 6%, transparent 7%);
    background-size:11px 11px;background-position:center;background-color:rgba(200,110,70,.12);
  }
  .face-zone[data-zone="cheek-l"]{left:24%;}
  .face-zone[data-zone="cheek-r"]{left:76%;}
  .face-zone[data-zone="scar-mark"]{
    top:58%;left:76%;width:22%;height:16%;
    background-image:repeating-linear-gradient(20deg, rgba(150,90,150,.85) 0 2px, transparent 2px 9px);
  }
  .face-zone[data-zone="chin"]{
    top:82%;left:50%;width:24%;height:16%;
    background-image:
      radial-gradient(circle at 30% 35%, rgba(193,60,60,.9) 0 9%, transparent 10%),
      radial-gradient(circle at 65% 55%, rgba(193,60,60,.9) 0 8%, transparent 9%),
      radial-gradient(circle at 45% 75%, rgba(193,60,60,.9) 0 7%, transparent 8%);
    background-color:rgba(193,60,60,.1);
  }
  .face-zone.on{opacity:1;}
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

  .score-row{
    display:flex;align-items:center;justify-content:space-between;padding:12px 0;
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
    margin-top:24px;background:#fffdfa;border:1px solid var(--db-line);border-radius:24px;padding:26px;
    box-shadow:0 10px 28px rgba(120,96,68,.06);
  }
  .diag-tabs-layout{display:grid;grid-template-columns:190px 1fr;gap:24px;margin-top:16px;align-items:start;}
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
  .panel-score-track{height:7px;border-radius:999px;background:var(--bg);margin-top:12px;overflow:hidden;}
  .panel-score-fill{height:100%;border-radius:999px;}
  .panel-desc{margin-top:18px;font-size:13.5px;color:#4a4944;line-height:1.65;}
  .panel-tips{margin-top:14px;}
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
          <div><span>20대 남성</span><b id="cmpAge">-</b></div>
        </div>
      </div>
      <div class="simple-score-main"><b id="simpleScore">-</b><span>점 / 100</span></div>
      <div class="simple-tier" id="simpleTier">-</div>

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
        <button class="btn btn-gold" id="diagCta">맞춤 제품 추천</button>
      </div>

      <div class="diag-face-panel">
        <div class="diag-face-title">관리가 필요한 부위</div>
        <div class="face-map">
          <div class="face-ear left"></div>
          <div class="face-ear right"></div>
          <div class="face-shape"></div>
          <div class="face-zone" data-zone="tzone"></div>
          <div class="face-zone" data-zone="cheek-l"></div>
          <div class="face-zone" data-zone="cheek-r"></div>
          <div class="face-zone" data-zone="scar-mark"></div>
          <div class="face-zone" data-zone="chin"></div>
        </div>
        <div class="face-legend" id="faceLegend">
          <span class="legend-item" data-concern="oil"><span class="legend-dot oil"></span>유분 · T존</span>
          <span class="legend-item" data-concern="pore"><span class="legend-dot pore"></span>모공 · 볼</span>
          <span class="legend-item" data-concern="scar"><span class="legend-dot scar"></span>흉터 · 볼</span>
          <span class="legend-item" data-concern="acne"><span class="legend-dot acne"></span>여드름 · 턱</span>
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
      <button type="button" class="social-btn" data-provider="kakao">
        <span class="social-ic" style="background:#FEE500;color:#3A1D1D;">K</span>카카오로 시작하기
      </button>
      <button type="button" class="social-btn" data-provider="google">
        <span class="social-ic" style="background:#fff;color:#4285F4;border:1px solid #e6e4de;">G</span>구글로 시작하기
      </button>
      <button type="button" class="social-btn" data-provider="naver">
        <span class="social-ic" style="background:#03C75A;color:#fff;">N</span>네이버로 시작하기
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

<div id="screenApp" class="app-screen" style="display:none;">
<div class="nav">
  <div class="wrap">
    <div class="brand"><b>FOR HIM</b><span>Men's Skincare Lab</span></div>
    <div class="nav-links">
      <a href="javascript:void(0)" data-step="analysis">피부분석</a>
      <a href="javascript:void(0)" data-step="recommend">제품추천</a>
      <a href="javascript:void(0)" data-step="community">커뮤니티</a>
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
    <p class="sub">원하는 관리 단계를 선택하면, 선택하신 고민과 나이에 맞춰 AI가 매칭한 TOP 3 제품을 보여드려요.</p>

    <div class="tier-tabs" id="tierTabs"></div>
    <div class="tier-desc" id="tierDesc"></div>
    <div class="tier-cat-label" id="tierCatLabel"></div>
    <div class="prod-row" id="tierProdRow"></div>

    <div class="step-nav">
      <button type="button" class="btn btn-outline btn-sm step-nav-btn" data-step-prev>이전</button>
      <div class="step-progress" data-step-dots></div>
      <button type="button" class="btn btn-dark btn-sm step-nav-btn" data-step-next>상세 고민별 추천 보기 →</button>
    </div>
  </div>
</section>

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
          <label>카테고리</label>
          <select id="cmFormCat"></select>
        </div>
        <div class="cm-field">
          <label>제목</label>
          <input type="text" id="cmFormTitleInput" maxlength="60" placeholder="제목을 입력해주세요" />
        </div>
        <div class="cm-field">
          <label>내용</label>
          <textarea id="cmFormBody" placeholder="같은 고민을 가진 분들에게 편하게 이야기해보세요"></textarea>
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

<div class="toast" id="toast"></div>
</div>

<script>
(function(){
  window.appState = { concerns:new Set(), analyzed:false, allInOne:false, age:29, nickname:'' };
  const state = window.appState;

  const splash = document.getElementById('screenSplash');
  const splashLogo = document.getElementById('splashLogo');
  const intro = document.getElementById('screenIntro');
  const camera = document.getElementById('screenCamera');
  const choice = document.getElementById('screenChoice');
  const simpleResult = document.getElementById('screenSimple');
  const diagnosis = document.getElementById('screenDiagnosis');
  const appScreen = document.getElementById('screenApp');
  let nickname = '';
  let enteredAge = 29;

  /* ---------------- 0) last-result recall ---------------- */
  const RECALL_KEY = 'forhim_last_result';

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

    appScreen.style.display = 'none';
    [splash, intro, camera, simpleResult, diagnosis].forEach(s=> s.classList.add('hidden'));
    choice.classList.remove('hidden');
    requestAnimationFrame(()=> choice.classList.add('visible'));
    window.scrollTo(0,0);
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
  const RECORDS_KEY = 'forhim_records';
  const screenAuth = document.getElementById('screenAuth');
  const screenConsent = document.getElementById('screenConsent');
  const screenProfile = document.getElementById('screenProfile');
  const screenMyPage = document.getElementById('screenMyPage');
  const CONCERN_LABEL = { scar:'흉터', pore:'모공', oil:'유분', acne:'여드름' };
  /* 계정 연동 시 제공사에서 받아오는 정보(데모: 시뮬레이션). 실제 OAuth 연동 시
     이메일은 세션에서, 나이는 제공사 동의 범위에 따라 채워집니다. */
  const PROVIDER_SAMPLE = {
    kakao:  { email:'minjun.kim@kakao.com',  age:28, name:'김민준' },
    google: { email:'minjun.kim@gmail.com',  age:31, name:'Minjun' },
    naver:  { email:'minjun.kim@naver.com',  age:26, name:'민준' }
  };
  let authOrigin = 'intro';
  let pendingProvider = null;
  let pendingMarketing = false;
  let linkedAccount = null;
  let mpTab = 'analyses';

  function loadMember(){ try{ return JSON.parse(localStorage.getItem(MEMBER_KEY) || 'null'); }catch(e){ return null; } }
  function saveMember(m){ member = m; try{ if(m) localStorage.setItem(MEMBER_KEY, JSON.stringify(m)); else localStorage.removeItem(MEMBER_KEY); }catch(e){} }
  function isMember(){ return !!(member && member.loggedIn); }
  let member = loadMember();

  function seedRecords(){
    const now = Date.now(), D = 86400000;
    return {
      analyses:[
        { id:'a1', date:now-14*D, score:62, type:'복합성', top:'모공', summary:'모공·유분 중심 분석, 종합 62점' },
        { id:'a2', date:now-3*D,  score:71, type:'지성',   top:'트러블', summary:'유분·트러블 개선 추세, 종합 71점' }
      ],
      recommends:[
        { id:'r1', date:now-3*D, title:'유분·트러블 맞춤 루틴', summary:'AI 매칭 기반 단계별 추천', items:['닥터지 레드 블레미쉬 토너','메디힐 마데카소사이드 선세럼','코스알엑스 6펩타이드 세럼'] }
      ],
      consults:[
        { id:'s1', date:now-10*D, title:'화농성 여드름 상담', summary:'턱 트러블 반복 → 진정+유분 관리 제안', status:'답변완료' }
      ]
    };
  }
  function loadRecords(){ try{ const r = JSON.parse(localStorage.getItem(RECORDS_KEY) || 'null'); if(r) return r; }catch(e){} const s = seedRecords(); saveRecords(s); return s; }
  function saveRecords(r){ records = r; try{ localStorage.setItem(RECORDS_KEY, JSON.stringify(r)); }catch(e){} }
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
    const cs = Array.from(state.concerns);
    const rec = { id:'a'+Date.now(), date:Date.now(), score:overall, type:type, top:worst.label,
      summary:(cs.map(concernLabel).join('·')||'전반') + ' 중심 분석, 종합 ' + overall + '점' };
    if(records.analyses[0] && Date.now()-records.analyses[0].date < 60000){ records.analyses[0] = rec; }
    else { records.analyses.unshift(rec); }
    saveRecords(records);
  }
  function recordRecommend(){
    const cs = Array.from(state.concerns);
    const rec = { id:'r'+Date.now(), date:Date.now(), title:(cs.map(concernLabel).join('·')||'맞춤') + ' 루틴 추천',
      summary:'AI 매칭 기반 단계별 추천', items:['1단계 세럼','2단계 선케어','3단계 커버'] };
    if(records.recommends[0] && Date.now()-records.recommends[0].date < 60000){ records.recommends[0] = rec; }
    else { records.recommends.unshift(rec); }
    saveRecords(records);
  }

  const MEMBER_SCREENS = [splash, intro, camera, choice, simpleResult, diagnosis, screenAuth, screenConsent, screenProfile, screenMyPage];
  function showMemberScreen(el){
    MEMBER_SCREENS.forEach(s=>{ s.classList.add('hidden'); s.classList.remove('visible'); });
    appScreen.style.display = 'none';
    el.classList.remove('hidden'); requestAnimationFrame(()=> el.classList.add('visible'));
    window.scrollTo(0,0);
  }
  function backToApp(){
    [screenAuth, screenConsent, screenProfile, screenMyPage, intro, camera, choice, simpleResult, diagnosis].forEach(s=>{ s.classList.add('hidden'); s.classList.remove('visible'); });
    appScreen.style.display = 'block';
    if(window.showAppStep){ window.showAppStep('hero'); }
    window.scrollTo(0,0);
  }
  function goCamera(){
    if(!nickname){ nickname = (member && member.nickname) || '회원'; }
    state.nickname = nickname; state.age = enteredAge;
    showMemberScreen(camera);
    startCamera();
  }

  function showAuth(origin){ authOrigin = origin || 'intro'; if(isMember()){ showMyPage(); return; } showMemberScreen(screenAuth); }
  function backFromAuth(){ if(authOrigin==='app'){ backToApp(); } else { showMemberScreen(intro); } }
  function doSocial(provider){
    pendingProvider = provider;
    linkedAccount = Object.assign({ provider:provider }, PROVIDER_SAMPLE[provider] || PROVIDER_SAMPLE.kakao);
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

  function showProfile(){
    const acc = linkedAccount || PROVIDER_SAMPLE.kakao;
    document.getElementById('profProvider').textContent = providerLabel(pendingProvider) + ' 계정에서 정보를 가져왔어요';
    document.getElementById('profEmail').value = acc.email || '';
    document.getElementById('profAge').value = acc.age || '';
    document.getElementById('profNick').value = acc.name || nickname || '';
    document.getElementById('profHint').textContent = '';
    showMemberScreen(screenProfile);
  }
  function profileSubmit(){
    const nick = document.getElementById('profNick').value.trim();
    const age = parseInt(document.getElementById('profAge').value, 10);
    const email = document.getElementById('profEmail').value.trim();
    const hint = document.getElementById('profHint');
    if(!nick){ hint.textContent = '닉네임을 입력해주세요.'; return; }
    if(!age || age < 1 || age > 120){ hint.textContent = '나이를 올바르게 입력해주세요.'; return; }
    nickname = nick; enteredAge = age; state.nickname = nick; state.age = age;
    saveMember({ loggedIn:true, provider:pendingProvider||'kakao', nickname:nick, email:email, age:age,
      joinedAt:Date.now(), agreements:{ required:true, marketing:!!pendingMarketing } });
    updateMemberUI();
    showMyPage();
  }

  function memberToast(msg){ const t = document.getElementById('toast'); if(!t) return; t.textContent = msg; t.classList.add('show'); setTimeout(()=> t.classList.remove('show'), 2400); }
  function logout(){
    if(window.USER_LOGGED_IN==='1'){ memberToast('화면 상단의 로그아웃 버튼을 이용해주세요.'); return; }
    saveMember(null); updateMemberUI(); showMemberScreen(intro);
  }
  function updateMemberUI(){ const nav = document.getElementById('navMember'); if(nav){ nav.textContent = isMember() ? '마이페이지' : '로그인'; } }
  /* real Google session (from Streamlit st.login) → continue to profile setup */
  function initRealAuth(){
    if(window.USER_LOGGED_IN !== '1') return;
    if(isMember() && member.provider === 'google') return;
    pendingProvider = 'google';
    pendingMarketing = false;
    linkedAccount = { provider:'google', email:(window.USER_EMAIL||''), name:(window.USER_NAME||''), age:'' };
    showProfile();
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
      memberToast('화면 상단의 [Google 계정으로 로그인] 버튼을 눌러주세요.');
      return;
    }
    doSocial(b.dataset.provider);
  }));
  document.getElementById('consentBack').addEventListener('click', ()=> showMemberScreen(screenAuth));
  document.getElementById('profBack').addEventListener('click', ()=> showMemberScreen(screenConsent));
  document.getElementById('profSubmit').addEventListener('click', profileSubmit);
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
  updateMemberUI();
  initRealAuth();

  /* ---------------- 1) splash ---------------- */
  setTimeout(()=> splashLogo.classList.add('sharp'), 150);
  setTimeout(()=> splashLogo.classList.remove('sharp'), 2400);
  setTimeout(()=> splash.classList.add('fade-out'), 2900);
  setTimeout(()=>{
    splash.classList.add('hidden');
    intro.classList.remove('hidden');
    requestAnimationFrame(()=> intro.classList.add('visible'));
  }, 3700);

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
        camProgressFill.style.transition = 'width 1.9s linear';
        camProgressFill.style.width = '100%';
      });
      i++;
      setTimeout(step, 2000);
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
    saveLastResult();
    recordAnalysis();
    setTimeout(showChoice, 1300);
  }

  function showChoice(){
    camera.classList.remove('visible');
    setTimeout(()=>{
      camera.classList.add('hidden');
      choice.classList.remove('hidden');
      requestAnimationFrame(()=> choice.classList.add('visible'));
    }, 550);
  }

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
  });
  document.getElementById('goDetailed').addEventListener('click', ()=>{
    renderDiagnosis();
    switchScreen(choice, diagnosis);
  });
  document.getElementById('simpleBack').addEventListener('click', ()=>{
    switchScreen(simpleResult, choice);
  });
  document.getElementById('simpleToRecommend').addEventListener('click', enterApp);

  /* ---------------- 4) diagnosis result ---------------- */
  function clamp10(v){ return Math.max(0.5, Math.min(10, Math.round(v*10)/10)); }

  function computeDiagnosis(){
    const c = state.concerns;
    return [
      { key:'wrinkle', label:'주름', score: clamp10(8.2 - Math.max(0, enteredAge-25)*0.12) },
      { key:'pigment', label:'색소침착', score: clamp10(7.6 - (c.has('scar')?3.4:0)) },
      { key:'redness', label:'붉은기', score: clamp10(8.6 - (c.has('acne')?2.2:0) - (c.has('oil')?0.8:0)) },
      { key:'pore', label:'모공', score: clamp10(8.0 - (c.has('pore')?5.2:0)) },
      { key:'oil', label:'피지', score: clamp10(7.6 - (c.has('oil')?4.0:0) - (c.has('acne')?1.4:0)) },
      { key:'trouble', label:'트러블', score: clamp10(8.6 - (c.has('acne')?5.0:0) - (c.has('oil')?0.8:0)) }
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

    document.getElementById('diagSentence').textContent =
      '좋습니다! 당신의 피부 점수는 ' + overall.toFixed(1) + '입니다. 우선 ' + best.label +
      ' 은(는) 관리가 잘 되어 있어요. ' + worst.label + ' 은(는) 좀 더 관리가 필요해요.';

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

    document.querySelectorAll('.face-zone').forEach(z=>{
      const zone = z.dataset.zone;
      let on = false;
      if(zone === 'tzone'){ on = state.concerns.has('oil'); }
      if(zone === 'cheek-l' || zone === 'cheek-r'){ on = state.concerns.has('pore'); }
      if(zone === 'scar-mark'){ on = state.concerns.has('scar'); }
      if(zone === 'chin'){ on = state.concerns.has('acne'); }
      z.classList.toggle('on', on);
    });
    document.querySelectorAll('.legend-item').forEach(el=>{
      el.classList.toggle('active', state.concerns.has(el.dataset.concern));
    });

    document.getElementById('diagCta').textContent = (nickname || '고객') + '님 맞춤 제품 추천';

    renderConcernTabs(metrics);
  }

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
      const products = window.recommendForConcern(detail.tag, 3);
      return '<div class="diag-panel' + (k===defaultKey?' active':'') + '" data-panel="' + k + '">' +
        '<div class="panel-head">' +
          '<span class="panel-title">' + detail.label + ' · ' + m.score.toFixed(1) + '점</span>' +
          '<span class="panel-badge ' + band + '">' + bandText + '</span>' +
        '</div>' +
        '<div class="panel-score-track"><div class="panel-score-fill fill-' + band + '" style="width:' + (m.score*10) + '%"></div></div>' +
        '<div class="tier-cat-label">' + detail.label + ' 맞춤 추천 · TOP 3 (내 피부 매칭순)</div>' +
        '<div class="prod-row">' + window.renderProductCards(products) + '</div>' +
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
    document.getElementById('cmpAge').textContent = cmpAge + '%';
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

  /* ---------------- step navigation (hero/analysis/recommend/extra/community) ---------------- */
  const APP_STEPS = ['hero','analysis','recommend','extra','community'];
  const STEP_EL = {
    hero: document.getElementById('stepHero'),
    analysis: document.getElementById('analysis'),
    recommend: document.getElementById('recommend'),
    extra: document.getElementById('extra'),
    community: document.getElementById('community')
  };
  let currentStep = 'hero';

  function showAppStep(name){
    if(!STEP_EL[name]) return;
    currentStep = name;
    APP_STEPS.forEach(s=> STEP_EL[s].classList.toggle('active', s===name));
    document.querySelectorAll('[data-step-dots]').forEach(dotsWrap=>{
      dotsWrap.innerHTML = APP_STEPS.map(s=>'<span class="step-dot' + (s===name?' active':'') + '"></span>').join('');
    });
    window.scrollTo(0,0);
    if(name === 'recommend' && !tierInitialized){ initTierTabs(); }
    if(name === 'extra' && !extraInitialized){ initExtraTabs(); }
  }
  window.showAppStep = showAppStep;

  document.querySelectorAll('[data-step]').forEach(el=>{
    el.addEventListener('click', ()=> showAppStep(el.dataset.step));
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

  /* ---------------- product card helper ---------------- */
  function renderProductCards(list){
    return list.map(p=>{
      const query = encodeURIComponent(p.brand + ' ' + p.name);
      const url = 'https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=' + query;
      return '<a class="prod-card rank-' + p.rank + '" href="' + url + '" target="_blank" rel="noopener noreferrer">' +
        '<div class="prod-rank">' + p.rank + '위</div>' +
        (p.img
          ? '<div class="prod-photo"><img src="' + p.img + '" alt="' + p.name + '" loading="lazy" /></div>'
          : '<div class="prod-icon" style="background:' + p.color + '"></div>') +
        '<div class="prod-brand">' + p.brand + '</div>' +
        '<div class="prod-name">' + p.name + '</div>' +
        '<div class="prod-tags">' +
          '<span class="prod-tag">' + p.tag + '</span>' +
          (p.match ? '<span class="prod-match">나와 ' + p.match + '% 매치</span>' : '') +
        '</div>' +
        '<div class="prod-cart-btn">올리브영에서 담기 →</div>' +
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
    {id:'physiogel', brand:'피지오겔', name:'데일리 모이스쳐 테라피 에센스 인 토너', img:PIMG.physiogel, color:'#a86f6f', cats:['toner'], pop:78, tag:'저자극 수분 토너', aff:{dryness:2,redness:2,shave:2,darkcircle:1,flake:2}}
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
    return { sev:sev, age:age };
  }

  function scoreProduct(p, profile){
    let s = 0;
    for(const tag in p.aff){ s += p.aff[tag] * (profile.sev[tag] || 0); }
    s += (p.pop || 70) * 0.012;
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
        PRODUCTS = rows.map(normalizeProduct);
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

  const TIERS = [
    { key:'t1', label:'1단계', category:'세럼', cat:'serum',
      desc:'클렌징·스킨·로션·세럼·크림으로 여드름을 억제하고 전반적인 피부 컨디션을 개선해요.' },
    { key:'t2', label:'2단계', category:'선크림', cat:'sun',
      desc:'기초 제품에 이어 피부 타입에 맞는 선케어로 노화·주름까지 예방해요.' },
    { key:'t3', label:'3단계', category:'쿠션', cat:'cushion',
      desc:'기초·선케어에 이어 간단한 색조 화장으로 피부 보정 효과까지 더해요.' },
    { key:'t4', label:'4단계', category:'아이 메이크업', cat:'eye',
      desc:'색조 화장에 이어 퍼스널 컬러에 맞는 쉐도우 제품으로 나만의 개성을 표현해요.' },
    { key:'t5', label:'5단계', category:'뷰티 디바이스', cat:'device',
      desc:'클렌징·기초·색조 3요소를 갖춘 뒤, 뷰티 디바이스로 얼굴형과 붓기까지 관리해요.' }
  ];
  let tierInitialized = false;

  function initTierTabs(){
    tierInitialized = true;
    const tabsEl = document.getElementById('tierTabs');
    tabsEl.innerHTML = TIERS.map((t,i)=>
      '<button type="button" class="tier-tab' + (i===0?' active':'') + '" data-tier="' + t.key + '">' + t.label + '</button>'
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
    document.getElementById('tierDesc').textContent = tier.desc;
    document.getElementById('tierCatLabel').textContent = tier.label + ' 추천 · ' + tier.category + ' TOP 3 (내 피부 맞춤순)';
    document.getElementById('tierProdRow').innerHTML = renderProductCards(recommendForCat(tier.cat, 3));
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
    {key:'pore', label:'모공', color:'#c86e46'},
    {key:'oil', label:'유분/피지', color:'#c98a3c'},
    {key:'acne', label:'여드름/트러블', color:'#c13c3c'},
    {key:'scar', label:'흉터/자국', color:'#965a96'},
    {key:'sensitive', label:'민감성', color:'#c1666b'},
    {key:'dry', label:'건조', color:'#5c8b9b'},
    {key:'elastic', label:'탄력/주름', color:'#8b6f47'},
    {key:'shave', label:'면도 자극', color:'#6b8b6f'},
    {key:'allinone', label:'올인원 추천', color:'#7a8b5c'},
    {key:'beginner', label:'초보자 루틴', color:'#54634a'},
    {key:'product', label:'제품 추천', color:'#b58b5c'}
  ];
  const CM_CAT_LABEL = {};
  CM_CATS.forEach(c=>{ CM_CAT_LABEL[c.key] = c.label; });
  const CM_SKIN_LABEL = {scar:'흉터',pore:'모공',oil:'유분',acne:'여드름',sensitive:'민감성',dry:'건조',elastic:'탄력'};

  const CM_STORE = 'forhim_community_posts';
  const CM_FAV = 'forhim_community_favs';

  function cmSeed(){
    const now = Date.now(); const H = 3600000, D = 86400000;
    return [
      {id:'seed2', cat:'acne', title:'턱에 화농성 여드름이 계속 올라와요', body:'턱 주변으로 크고 아픈 여드름이 반복돼요. 뭐부터 시작하면 좋을까요? 진정 위주로 가는 게 맞나요?', author:'야근장인', skin:['acne','oil'], photo:null, createdAt:now-5*H, comments:[{id:'c2',author:'초보탈출',body:'저도 비슷했는데 유분 잡고 진정 토너 쓰니 확실히 덜 나요.',createdAt:now-4*H},{id:'c3',author:'피부과다녀옴',body:'심하면 피부과 병행도 추천이요!',createdAt:now-3*H}]},
      {id:'seed1', cat:'pore', title:'모공 넓은데 클렌징만 잘해도 나아질까요?', body:'파운데이션도 안 바르는데 코 옆 모공이 너무 신경 쓰여요. 세안만 신경 써도 좀 나아질까요? 이중세안 꼭 해야 하나요?', author:'코딩하는곰', skin:['pore','oil'], photo:null, createdAt:now-3*H, comments:[{id:'c1',author:'루틴관리중',body:'저는 미온수 세안 + 주2회 각질케어로 확실히 줄었어요!',createdAt:now-2*H}]},
      {id:'seed3', cat:'beginner', title:'스킨케어 완전 초보인데 뭐부터 사야 하나요?', body:'화장품 한 번도 안 써봤어요. 올인원 하나로 시작해도 괜찮을까요? 순서도 잘 모르겠어요.', author:'초보루틴', skin:['acne'], photo:null, createdAt:now-1*D, comments:[]},
      {id:'seed4', cat:'oil', title:'T존만 번들거리는 복합성 관리 팁', body:'T존은 기름지고 볼은 당기는데 다들 어떻게 관리하세요? 제품을 부위별로 다르게 써야 하나요?', author:'T존건조', skin:['oil','dry'], photo:null, createdAt:now-1*D-2*H, comments:[]},
      {id:'seed5', cat:'shave', title:'면도 후 따갑고 붉어지는 거 어떻게 잡죠?', body:'매일 면도하는데 턱 라인이 늘 붉고 따가워요. 면도 후에 뭘 발라야 진정이 될까요?', author:'아침면도', skin:['sensitive','acne'], photo:null, createdAt:now-2*D, comments:[{id:'c4',author:'수염관리',body:'면도 후 진정크림 필수예요. 알콜 든 애프터쉐이브는 피하세요!',createdAt:now-1*D}]},
      {id:'seed6', cat:'product', title:'입문용 선크림 추천 좀 해주세요', body:'백탁 없고 산뜻한 남성용 선크림 찾고 있어요. 데일리로 부담 없이 쓸만한 거 있을까요?', author:'출근전5분', skin:['oil'], photo:null, createdAt:now-3*D, comments:[]},
      {id:'seed7', cat:'dry', title:'세안 후 당김이 너무 심해요', body:'세안하고 나면 얼굴이 쫙 당겨요. 보습을 어떻게 쌓아야 촉촉함이 오래 갈까요?', author:'건조주의보', skin:['dry','sensitive'], photo:null, createdAt:now-4*D, comments:[]},
      {id:'seed8', cat:'allinone', title:'귀찮은 사람용 올인원 루틴 공유', body:'아침에 시간 없어서 올인원 + 선크림만 발라요. 이 정도만 해도 충분할까요? 다들 최소 루틴 뭐 쓰세요?', author:'미니멀케어', skin:['oil'], photo:null, createdAt:now-5*D, comments:[{id:'c5',author:'바쁨',body:'저도 딱 그 루틴인데 안 하는 것보단 훨씬 나아요.',createdAt:now-4*D}]}
    ];
  }
  function cmSave(list){ try{ localStorage.setItem(CM_STORE, JSON.stringify(list)); }catch(e){} }
  function cmLoad(){
    try{ const raw = localStorage.getItem(CM_STORE); if(raw){ return JSON.parse(raw); } }catch(e){}
    const seed = cmSeed(); cmSave(seed); return seed;
  }
  function cmSaveFavs(set){ try{ localStorage.setItem(CM_FAV, JSON.stringify(Array.from(set))); }catch(e){} }
  function cmLoadFavs(){ try{ return new Set(JSON.parse(localStorage.getItem(CM_FAV) || '[]')); }catch(e){ return new Set(); } }

  let cmPosts = cmLoad();
  let cmFavs = cmLoadFavs();
  let cmActiveCat = 'all';
  let cmQuery = '';
  let cmEditingId = null;
  let cmPendingPhoto = null;

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
      return '<article class="cm-card" data-id="'+p.id+'">'+
        '<div class="cm-card-top">'+
          '<span class="cm-cat-chip">'+esc(CM_CAT_LABEL[p.cat]||p.cat)+'</span>'+
          '<button type="button" class="cm-fav'+(fav?' on':'')+'" data-fav="'+p.id+'" aria-label="즐겨찾기">'+(fav?STAR_FILL:STAR_OUTLINE)+'</button>'+
        '</div>'+
        '<div class="cm-card-title">'+esc(p.title)+'</div>'+
        cmSkinTags(p.skin)+
        (p.photo ? '<img class="cm-card-thumb" src="'+p.photo+'" alt="" />' : '')+
        '<div class="cm-card-body">'+esc(p.body)+'</div>'+
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
      if(cmNeedLogin()) return;
      try{
        const r = await fetch(window.SB_URL + '/rest/v1/comments', {
          method:'POST', headers:sbRestHeaders(true),
          body:JSON.stringify({ post_id:id, user_id:cmSession.user.id, author:cmUserName(), body:val })
        });
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
        '<span class="cm-cat-chip">'+esc(CM_CAT_LABEL[p.cat]||p.cat)+'</span>'+
        '<div class="cm-detail-actions">'+
          '<button type="button" class="cm-icon-btn'+(fav?' on':'')+'" id="cmDetailFav">'+(fav?STAR_FILL:STAR_OUTLINE)+(fav?'저장됨':'즐겨찾기')+'</button>'+
          '<button type="button" class="cm-icon-btn" id="cmDetailEdit">'+EDIT_SVG+'수정</button>'+
        '</div>'+
      '</div>'+
      '<h2 class="cm-detail-title">'+esc(p.title)+'</h2>'+
      '<div class="cm-detail-meta"><div class="avatar">'+esc((p.author||'익')[0])+'</div>'+
        '<div><div class="cm-author">'+esc(p.author||'익명')+'</div><div class="cm-time">'+cmAgo(p.createdAt)+'</div></div></div>'+
      cmSkinTags(p.skin)+
      (p.photo ? '<img class="cm-detail-photo" src="'+p.photo+'" alt="첨부 사진" />' : '')+
      '<div class="cm-detail-body">'+esc(p.body)+'</div>'+
      '<div class="cm-comments">'+
        '<div class="cm-comments-title">댓글 '+(p.comments?p.comments.length:0)+'</div>'+
        '<div id="cmCommentList">'+cmRenderComments(p)+'</div>'+
        '<div class="cm-comment-form">'+
          '<input type="text" id="cmCommentInput" placeholder="댓글을 남겨보세요" maxlength="300" />'+
          '<button type="button" class="btn btn-dark btn-sm" id="cmCommentSubmit">등록</button>'+
        '</div>'+
      '</div>';
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
    if(id){
      const p = cmPosts.find(function(x){ return x.id===id; });
      document.getElementById('cmFormTitle').textContent = '글 수정';
      catSel.value = p.cat; titleInput.value = p.title; bodyInput.value = p.body;
      cmPendingPhoto = p.photo || null;
      document.getElementById('cmFormSubmit').textContent = '수정 완료';
    } else {
      document.getElementById('cmFormTitle').textContent = '새 글 남기기';
      catSel.value = (cmActiveCat!=='all' && cmActiveCat!=='__fav') ? cmActiveCat : CM_CATS[1].key;
      titleInput.value = ''; bodyInput.value = '';
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
    if(!title || !body){ hint.textContent = '제목과 내용을 모두 입력해주세요.'; return; }

    if(SB_ON){
      if(cmNeedLogin()) return;
      hint.textContent = '';
      try{
        if(cmEditingId){
          const r = await fetch(window.SB_URL + '/rest/v1/posts?id=eq.' + encodeURIComponent(cmEditingId), {
            method:'PATCH', headers:sbRestHeaders(true),
            body:JSON.stringify({ category:cat, title:title, body:body, photo_url:cmPendingPhoto })
          });
          if(!r.ok) throw new Error('HTTP ' + r.status);
          cmShowToast('글이 수정되었어요.');
          await cmRefresh(); cmOpenDetail(cmEditingId);
        } else {
          const ins = { user_id:cmSession.user.id, author:cmUserName(), category:cat, title:title,
            body:body, photo_url:cmPendingPhoto, skin_tags:Array.from(window.appState.concerns||[]) };
          const r = await fetch(window.SB_URL + '/rest/v1/posts', { method:'POST', headers:sbRestHeaders(true), body:JSON.stringify(ins) });
          if(!r.ok) throw new Error('HTTP ' + r.status);
          cmShowToast('글이 등록되었어요.');
          cmActiveCat = 'all'; cmQuery = ''; document.getElementById('cmSearch').value = '';
          await cmRefresh(); cmShow('list');
        }
      }catch(e){ hint.textContent = '저장에 실패했어요. 로그인이 만료됐다면 다시 로그인해주세요.'; }
      return;
    }

    if(cmEditingId){
      const p = cmPosts.find(function(x){ return x.id===cmEditingId; });
      p.cat = cat; p.title = title; p.body = body; p.photo = cmPendingPhoto;
      cmSave(cmPosts);
      cmShowToast('글이 수정되었어요.');
      cmOpenDetail(cmEditingId);
    } else {
      cmPosts.unshift({ id:'p'+Date.now(), cat:cat, title:title, body:body, photo:cmPendingPhoto,
        author:(window.appState.nickname||'익명'),
        skin:Array.from(window.appState.concerns||[]),
        createdAt:Date.now(), comments:[] });
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
  if(SB_ON){ cmRefresh(); }

  document.getElementById('cmCats').addEventListener('click', function(e){
    const btn = e.target.closest('.cm-cat'); if(!btn) return;
    cmActiveCat = btn.dataset.cat; cmRenderCats(); cmRenderList();
  });
  document.getElementById('cmSearch').addEventListener('input', function(e){ cmQuery = e.target.value.trim(); cmRenderList(); });
  document.getElementById('cmList').addEventListener('click', function(e){
    const fav = e.target.closest('.cm-fav');
    if(fav){ e.stopPropagation(); cmToggleFav(fav.dataset.fav); cmRenderCats(); cmRenderList(); return; }
    const card = e.target.closest('.cm-card'); if(card){ cmOpenDetail(card.dataset.id); }
  });
  document.getElementById('cmWriteBtn').addEventListener('click', function(){ cmOpenWrite(null); });
  document.getElementById('cmDetailBack').addEventListener('click', function(){ cmRenderList(); cmShow('list'); });
  document.getElementById('cmWriteBack').addEventListener('click', function(){ cmShow('list'); });
  document.getElementById('cmFormCancel').addEventListener('click', function(){ cmShow('list'); });
  document.getElementById('cmFormSubmit').addEventListener('click', cmSubmitForm);
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
if auth_on:
    try:
        if st.user.is_logged_in:
            logged_in = True
            user_email = getattr(st.user, "email", "") or ""
            user_name = getattr(st.user, "name", "") or ""
    except Exception:
        pass

    if logged_in:
        _c1, _c2 = st.columns([5, 1])
        _c1.caption(f"구글 계정으로 로그인됨 · {user_email}")
        if _c2.button("로그아웃", use_container_width=True):
            st.logout()
    else:
        if st.button("Google 계정으로 로그인", type="primary"):
            st.login("google")

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

st.iframe(DEMO_HTML, height="content", width="stretch")
