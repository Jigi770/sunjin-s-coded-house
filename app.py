import base64
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
  .cam-scanline{
    position:absolute;left:8%;right:8%;height:3px;top:15%;
    background:linear-gradient(90deg, transparent, rgba(201,168,106,.95), transparent);
    box-shadow:0 0 14px 3px rgba(201,168,106,.75);
    animation:cam-scan 2.4s ease-in-out infinite;pointer-events:none;
  }
  @keyframes cam-scan{
    0%,100%{ top:15%; opacity:.25; }
    50%{ top:82%; opacity:1; }
  }
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

  /* ---------- DIAGNOSIS RESULT ---------- */
  .diagnosis{background:var(--bg);opacity:0;transition:opacity .5s ease;padding:24px;}
  .diagnosis.visible{opacity:1;}
  .diag-card{width:100%;max-width:640px;}
  .diag-back{
    display:inline-flex;align-items:center;gap:6px;padding:8px 14px 8px 10px;border-radius:999px;
    border:1.5px solid var(--line);background:var(--surface);color:var(--ink-soft);font-size:13px;font-weight:700;
    font-family:inherit;cursor:pointer;margin-bottom:16px;transition:border-color .15s ease,color .15s ease;
  }
  .diag-back:hover{border-color:#c8c6bd;color:var(--ink);}
  .diag-back svg{width:16px;height:16px;}
  .diag-title{font-size:clamp(20px,3.4vw,26px);margin-top:10px;font-weight:700;letter-spacing:-.02em;color:var(--ink);}
  .diag-top{display:grid;grid-template-columns:1fr 1.15fr;gap:16px;margin-top:22px;}
  .diag-summary,.diag-face{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;}
  .diag-summary-title,.diag-face-title{font-size:12.5px;font-weight:700;letter-spacing:.06em;color:var(--ink-soft);text-transform:uppercase;margin-bottom:14px;}
  .diag-summary-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .diag-summary-grid span{display:block;font-size:12px;color:var(--ink-soft);margin-bottom:4px;}
  .diag-summary-grid b{font-size:19px;font-weight:700;color:var(--ink);}
  .diag-summary-grid b i{font-style:normal;font-size:11px;font-weight:600;color:var(--ink-soft);margin-left:2px;}

  .face-map{position:relative;width:132px;height:160px;margin:0 auto;}
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

  .diag-sentence{margin-top:18px;padding:16px 20px;background:var(--accent-soft);border-radius:var(--radius);font-size:14px;color:#3c4636;line-height:1.6;}
  .diag-concerns{margin-top:22px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;}
  .diag-concerns-head{display:flex;justify-content:space-between;align-items:center;font-size:13.5px;font-weight:700;color:var(--ink);}
  .diag-tag{font-size:11px;font-weight:700;color:var(--ink-soft);background:var(--bg);border:1px solid var(--line);padding:4px 10px;border-radius:999px;}
  .diag-scale{display:flex;justify-content:space-between;font-size:11px;color:var(--ink-soft);margin-top:14px;padding:0 2px;}
  .diag-row{display:grid;grid-template-columns:64px 1fr 38px 18px;align-items:center;gap:12px;margin-top:14px;}
  .diag-row-label{font-size:13.5px;font-weight:600;color:var(--ink);}
  .diag-row-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#c1666b,#c98a3c,#54634a);position:relative;}
  .diag-row-marker{position:absolute;top:50%;width:12px;height:12px;border-radius:50%;background:#fff;border:2.5px solid var(--ink);transform:translate(-50%,-50%);}
  .diag-row-value{font-size:13px;font-weight:700;text-align:right;color:var(--ink);}
  .diag-row-dot{width:10px;height:10px;border-radius:50%;margin:0 auto;}
  .diag-row-dot.good{background:var(--good);}
  .diag-row-dot.mid{background:var(--mid);}
  .diag-row-dot.bad{background:var(--bad);}
  #diagCta{margin-top:26px;width:100%;padding:14px;font-size:15px;}

  /* ---------- CONCERN TABS ---------- */
  .diag-tabsblock{margin-top:22px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;}
  .diag-tabs{display:flex;gap:8px;flex-wrap:wrap;}
  .diag-tab{
    display:flex;align-items:center;gap:6px;padding:9px 15px;border-radius:999px;border:1.5px solid var(--line);
    background:var(--bg);color:var(--ink-soft);font-size:13.5px;font-weight:700;font-family:inherit;cursor:pointer;
    transition:all .15s ease;
  }
  .diag-tab .tab-dot{width:7px;height:7px;border-radius:50%;flex:none;}
  .diag-tab.active{background:var(--dark);border-color:var(--dark);color:#fff;}
  .diag-panel{display:none;margin-top:18px;padding-top:18px;border-top:1px solid var(--line);}
  .diag-panel.active{display:block;animation:fade .4s ease;}
  .panel-head{display:flex;align-items:center;justify-content:space-between;}
  .panel-title{font-size:15.5px;font-weight:700;color:var(--ink);}
  .panel-badge{font-size:11.5px;font-weight:700;padding:4px 11px;border-radius:999px;}
  .panel-badge.good{background:var(--accent-soft);color:var(--accent);}
  .panel-badge.mid{background:#fbe9d2;color:var(--mid);}
  .panel-badge.bad{background:#f7dede;color:var(--bad);}
  .panel-score-track{height:7px;border-radius:999px;background:var(--bg);margin-top:12px;overflow:hidden;}
  .panel-score-fill{height:100%;border-radius:999px;}
  .panel-desc{margin-top:14px;font-size:13.5px;color:#4a4944;line-height:1.65;}
  .panel-tips{margin-top:14px;}
  .panel-tips-title{font-size:11.5px;font-weight:700;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.05em;}
  .panel-tips ul{margin:8px 0 0;padding:0;list-style:none;}
  .panel-tips li{position:relative;padding-left:16px;font-size:13px;color:#4a4944;line-height:1.6;margin-top:6px;}
  .panel-tips li::before{content:'';position:absolute;left:0;top:8px;width:5px;height:5px;border-radius:50%;background:var(--accent);}
  .panel-routine{margin-top:14px;display:flex;align-items:center;gap:10px;padding:12px 14px;background:var(--bg);border-radius:var(--radius-sm);}
  .panel-routine-label{font-size:11px;font-weight:700;color:var(--ink-soft);}
  .panel-routine-name{font-size:13px;font-weight:700;color:var(--ink);}

  @media (max-width:640px){
    .diag-top{grid-template-columns:1fr;}
    .face-map{margin-top:10px;}
    .diag-row{grid-template-columns:56px 1fr 34px 16px;gap:8px;}
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
        <div class="cam-scanline"></div>
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
    <div class="eyebrow">DIAGNOSIS</div>
    <h2 class="diag-title">피부 진단 결과예요</h2>

    <div class="diag-top">
      <div class="diag-summary">
        <div class="diag-summary-title">요약</div>
        <div class="diag-summary-grid">
          <div><span>피부 나이</span><b id="diagAge">-</b></div>
          <div><span>피부 점수</span><b id="diagScore">-</b></div>
          <div><span>우선 관리 항목</span><b id="diagPriority">-</b></div>
          <div><span>피부 타입</span><b id="diagType">-</b></div>
        </div>
      </div>
      <div class="diag-face">
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
    </div>

    <div class="diag-sentence" id="diagSentence"></div>

    <div class="diag-concerns">
      <div class="diag-concerns-head"><span>피부 고민</span><span class="diag-tag">맞춤 기준: 기본</span></div>
      <div class="diag-scale"><span>나쁨</span><span>보통</span><span>좋음</span></div>
      <div id="diagRows"></div>
    </div>

    <div class="diag-tabsblock">
      <div class="diag-concerns-head" style="margin-bottom:14px;">
        <span>고민별 자세히 보기</span>
      </div>
      <div class="diag-tabs" id="diagTabs"></div>
      <div id="diagPanels"></div>
    </div>

    <button class="btn btn-gold" id="diagCta">맞춤 제품 추천</button>
  </div>
</div>

<div id="screenApp" class="app-screen" style="display:none;">
<div class="nav">
  <div class="wrap">
    <div class="brand"><b>FOR HIM</b><span>Men's Skincare Lab</span></div>
    <div class="nav-links">
      <a href="#analysis">피부분석</a>
      <a href="#recommend">제품추천</a>
      <a href="#community">커뮤니티</a>
    </div>
    <button type="button" class="btn btn-outline btn-sm" id="navRecall" style="display:none;">최근 결과 다시 보기</button>
    <a href="#analysis" class="btn btn-dark btn-sm">분석 시작</a>
  </div>
</div>

<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow on-dark">MEN'S BEAUTY, SIMPLIFIED</div>
      <h1><span id="heroGreet"></span>피부 관리, <em>어렵게</em><br/>생각하지 마세요</h1>
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
</div>

<script>
(function(){
  window.appState = { concerns:new Set(), analyzed:false, allInOne:false };
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

  function runSteps(){
    let i = 0;
    function step(){
      if(i >= DIRECTIONS.length){ finishCamera(); return; }
      const d = DIRECTIONS[i];
      camSub.textContent = d.label;
      camArrow.textContent = d.arrow;
      camArrow.className = 'cam-arrow dir-' + d.dir;
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
    document.getElementById('diagScore').innerHTML = overall.toFixed(1) + '<i> 10점 만점</i>';
    document.getElementById('diagPriority').textContent = worst.label;
    document.getElementById('diagType').textContent = skinType;

    document.getElementById('diagSentence').textContent =
      '좋습니다! 당신의 피부 점수는 ' + overall.toFixed(1) + '입니다. 우선 ' + best.label +
      ' 은(는) 관리가 잘 되어 있어요. ' + worst.label + ' 은(는) 좀 더 관리가 필요해요.';

    document.getElementById('diagRows').innerHTML = metrics.map(m=>{
      const band = m.score>=7 ? 'good' : m.score>=4 ? 'mid' : 'bad';
      return '<div class="diag-row">' +
        '<div class="diag-row-label">' + m.label + '</div>' +
        '<div class="diag-row-track"><div class="diag-row-marker" style="left:' + (m.score*10) + '%"></div></div>' +
        '<div class="diag-row-value">' + m.score.toFixed(1) + '</div>' +
        '<div class="diag-row-dot ' + band + '"></div>' +
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
      label:'모공', metricKey:'pore',
      desc:{
        bad:'모공이 눈에 띄게 넓어져 있어요. 피지와 노폐물이 쌓이기 쉬운 상태라 꾸준한 관리가 필요해요.',
        mid:'모공이 약간 넓어진 편이에요. 지금부터 관리하면 눈에 띄게 좋아질 수 있어요.',
        good:'모공 상태가 양호해요. 지금 루틴을 유지해주세요.'
      },
      tips:['이중세안으로 모공 속 노폐물을 자주 제거해주세요.','뜨거운 물 세안은 피하고 미온수를 사용하세요.','주 1~2회 각질 케어로 모공을 정돈해주세요.'],
      routine:'포어 타이트닝 토너'
    },
    oil: {
      label:'유분', metricKey:'oil',
      desc:{
        bad:'T존을 중심으로 유분이 많이 분비되고 있어요. 번들거림과 트러블로 이어지기 쉬운 상태예요.',
        mid:'유분이 약간 많은 편이에요. 가벼운 제형으로 관리하면 균형을 잡을 수 있어요.',
        good:'유분·수분 밸런스가 좋은 편이에요. 지금 루틴을 유지해주세요.'
      },
      tips:['하루 2회, 약산성 클렌저로 과도한 유분만 부드럽게 제거해주세요.','무거운 크림 대신 가벼운 젤 타입 제형을 사용해보세요.','오후에 유분이 심하면 블로팅 페이퍼로 가볍게 눌러주세요.'],
      routine:'라이트 젤 로션'
    },
    acne: {
      label:'여드름', metricKey:'trouble',
      desc:{
        bad:'염증성 트러블이 반복되고 있어요. 자극을 줄이고 원인균 관리가 필요한 상태예요.',
        mid:'가끔 트러블이 올라오는 편이에요. 초기에 진정시켜주면 흉터로 남는 걸 줄일 수 있어요.',
        good:'트러블이 잘 관리되고 있어요. 지금 상태를 유지해주세요.'
      },
      tips:['손으로 만지거나 짜지 말고 진정 성분으로 케어해주세요.','베개 커버, 마스크 등 피부에 닿는 물건을 자주 세척해주세요.','트러블 부위엔 저자극 스팟 제품을 사용해보세요.'],
      routine:'포어 클린 폼'
    },
    scar: {
      label:'흉터', metricKey:'pigment',
      desc:{
        bad:'흉터·색소 자국이 두드러져 피부결이 고르지 않은 상태예요. 꾸준한 진정·재생 관리가 필요해요.',
        mid:'옅은 자국이 남아있어요. 꾸준히 관리하면 결이 점점 매끈해질 수 있어요.',
        good:'흉터·색소 부담이 적은 편이에요. 지금 루틴을 유지해주세요.'
      },
      tips:['자외선 차단제를 매일 발라 색소 자국이 짙어지는 걸 막아주세요.','브라이트닝 성분(나이아신아마이드 등)을 꾸준히 사용해보세요.','새로 생긴 트러블은 짜지 않아야 흉터로 남지 않아요.'],
      routine:'브라이트닝 세럼'
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
        '<div class="panel-routine">' +
          '<span class="panel-routine-label">추천 루틴</span>' +
          '<span class="panel-routine-name">' + detail.routine + '</span>' +
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
      if(window.renderRoutine){ window.renderRoutine(); }
      appScreen.style.display = 'block';
      const target = document.getElementById('recommend');
      if(target){ target.scrollIntoView(); } else { window.scrollTo(0,0); }
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
  window.renderRoutine = renderRoutine;
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

DEMO_HTML = DEMO_HTML.replace("__LOGO_SRC__", logo_data_uri)

st.iframe(DEMO_HTML, height="content", width="stretch")
