import streamlit as st
from PIL import Image
from ultralytics import YOLO
from collections import Counter

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="LipCare Vision AI",
    page_icon="🫦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS MODERN, RESPONSIF & POLISH
# ==========================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap" rel="stylesheet">

<style>
    /* ─── ROOT VARIABLES ─── */
    :root {
        --bg-main:        #09080C;
        --bg-surface:     #110F16;
        --bg-card:        rgba(255,255,255,0.03);
        --bg-card-hover:  rgba(255,255,255,0.055);
        --border:         rgba(255,255,255,0.07);
        --border-glow:    rgba(205,100,120,0.45);

        --rose:           #D9607A;
        --rose-2:         #F08898;
        --rose-glow:      rgba(217,96,122,0.22);
        --rose-muted:     rgba(217,96,122,0.12);

        --amber:          #E8A84A;
        --amber-muted:    rgba(232,168,74,0.12);

        --teal:           #4ABFB0;
        --teal-muted:     rgba(74,191,176,0.12);

        --violet:         #9A7ECC;
        --violet-muted:   rgba(154,126,204,0.12);

        --sienna:         #BF8A6A;
        --sienna-muted:   rgba(191,138,106,0.12);

        --success:        #56C99A;
        --success-muted:  rgba(86,201,154,0.12);

        --danger:         #E05757;
        --danger-muted:   rgba(224,87,87,0.12);

        --text-1:  #F2EDF0;
        --text-2:  #A8979F;
        --text-3:  #665860;

        --r-sm: 8px;
        --r-md: 14px;
        --r-lg: 20px;
        --r-xl: 28px;

        --font-display: 'Syne', sans-serif;
        --font-body:    'DM Sans', sans-serif;
    }

    /* ─── RESET & BASE ─── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--bg-main) !important;
        font-family: var(--font-body);
        color: var(--text-1);
    }

    /* Mesh gradient background */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 70% 50% at 10% 0%,   rgba(217,96,122,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 90% 100%,  rgba(154,126,204,0.06) 0%, transparent 60%),
            radial-gradient(ellipse 50% 40% at 50% 50%,  rgba(74,191,176,0.03)  0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    /* Fine grain texture */
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.5;
    }

    .block-container {
        padding: 1.8rem 2rem 3rem !important;
        max-width: 1380px !important;
        position: relative;
        z-index: 1;
    }

    /* ─── HIDE STREAMLIT UI ─── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }
    .stFileUploader > label { display: none; }
    [data-testid="stSpinner"] { display: none !important; }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--text-3); border-radius: 10px; }

    /* =========================================
       HERO SECTION
    ========================================= */
    .hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
        padding: 0 0 1.8rem;
        margin-bottom: 1.8rem;
        border-bottom: 1px solid var(--border);
        animation: slideDown .55s cubic-bezier(.22,1,.36,1) both;
    }
    .hero-brand { display: flex; align-items: center; gap: 16px; }
    .hero-logo {
        width: 52px; height: 52px;
        background: linear-gradient(140deg, #D9607A 0%, #9A3058 100%);
        border-radius: 15px;
        display: flex; align-items: center; justify-content: center;
        font-size: 26px;
        box-shadow: 0 0 0 1px rgba(217,96,122,.3), 0 8px 28px rgba(217,96,122,.25);
        flex-shrink: 0;
        position: relative;
        overflow: hidden;
    }
    .hero-logo::after {
        content: '';
        position: absolute;
        top: -30%; left: -30%;
        width: 70%; height: 60%;
        background: rgba(255,255,255,.18);
        transform: rotate(-30deg);
        border-radius: 50%;
    }
    .hero-name {
        font-family: var(--font-display);
        font-size: clamp(20px, 3.2vw, 32px);
        font-weight: 700;
        color: var(--text-1);
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .hero-name span { color: var(--rose); }
    .hero-tagline {
        font-size: 12px;
        color: var(--text-3);
        letter-spacing: .8px;
        margin-top: 5px;
        text-transform: uppercase;
        font-weight: 500;
    }
    .status-pill {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 8px 18px;
        border-radius: 100px;
        font-size: 11.5px; font-weight: 600;
        letter-spacing: .4px;
        border: 1px solid;
        white-space: nowrap;
    }
    .status-online {
        background: var(--success-muted);
        border-color: rgba(86,201,154,.22);
        color: var(--success);
    }
    .status-offline {
        background: var(--danger-muted);
        border-color: rgba(224,87,87,.22);
        color: var(--danger);
    }
    .pulse-dot {
        width: 7px; height: 7px;
        background: currentColor;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }

    /* =========================================
       GLASS CARD
    ========================================= */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-xl);
        padding: 22px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: border-color .3s, background .3s;
    }
    .card:hover { border-color: var(--border-glow); background: var(--bg-card-hover); }

    /* =========================================
       SECTION LABEL
    ========================================= */
    .sec-label {
        display: flex; align-items: center; gap: 10px;
        font-family: var(--font-display);
        font-size: 9.5px; font-weight: 700;
        letter-spacing: 2.2px; text-transform: uppercase;
        color: var(--text-3);
        margin-bottom: 18px;
    }
    .sec-label svg { color: var(--rose); flex-shrink: 0; }
    .sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

    /* =========================================
       TOGGLE BUTTON OVERRIDE (NEW)
    ========================================= */
    /* Tombol di dalam kolom (toggle sumber gambar): base abu-abu */
    [data-testid="column"] .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        color: var(--text-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r-sm) !important;
        font-size: 11.5px !important;
        font-weight: 700 !important;
        letter-spacing: .4px !important;
        padding: 9px 10px !important;
        box-shadow: none !important;
        transition: all .22s !important;
    }
    [data-testid="column"] .stButton > button:hover {
        background: rgba(255,255,255,0.09) !important;
        border-color: rgba(255,255,255,0.15) !important;
        color: var(--text-1) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* =========================================
       INPUT MODE TOGGLE (NEW)
    ========================================= */
    .mode-toggle {
        display: flex;
        background: rgba(0,0,0,.35);
        border: 1px solid var(--border);
        border-radius: var(--r-md);
        padding: 4px;
        margin-bottom: 16px;
        gap: 4px;
    }
    .mode-btn {
        flex: 1;
        padding: 9px 10px;
        border-radius: 10px;
        font-family: var(--font-display);
        font-size: 11.5px; font-weight: 700;
        letter-spacing: .4px;
        text-align: center;
        cursor: pointer;
        transition: all .22s;
        color: var(--text-3);
        border: 1px solid transparent;
        display: flex; align-items: center; justify-content: center; gap: 6px;
    }
    .mode-btn.active {
        background: linear-gradient(135deg, #D9607A 0%, #A03058 100%);
        color: white;
        border-color: rgba(217,96,122,.4);
        box-shadow: 0 3px 14px var(--rose-glow);
    }

    /* =========================================
       CAMERA ZONE (NEW)
    ========================================= */
    .camera-zone {
        border: 1.5px dashed rgba(74,191,176,.35);
        border-radius: var(--r-lg);
        padding: 20px 16px;
        text-align: center;
        background: linear-gradient(145deg, rgba(74,191,176,.04), rgba(154,126,204,.04));
        position: relative;
        overflow: hidden;
    }
    .camera-zone::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(74,191,176,.07), transparent 65%);
    }
    .camera-title {
        font-family: var(--font-display);
        font-size: 13px; font-weight: 600;
        color: var(--text-1); margin-bottom: 4px;
    }
    .camera-hint { font-size: 11px; color: var(--text-3); margin-bottom: 12px; }

    /* Kamera widget Streamlit override */
    [data-testid="stCameraInput"] {
        background: transparent !important;
    }
    [data-testid="stCameraInput"] > label { display: none !important; }
    [data-testid="stCameraInput"] video {
        border-radius: var(--r-md) !important;
    }
    [data-testid="stCameraInput"] button {
        background: linear-gradient(135deg, #4ABFB0 0%, #2A8F83 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--r-sm) !important;
        font-family: var(--font-display) !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        letter-spacing: .4px !important;
        padding: 10px 20px !important;
        transition: all .22s !important;
        box-shadow: 0 4px 16px rgba(74,191,176,.25) !important;
        cursor: pointer !important;
    }
    [data-testid="stCameraInput"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(74,191,176,.35) !important;
    }

    /* =========================================
       UPLOAD ZONE
    ========================================= */
    .upload-zone {
        border: 1.5px dashed rgba(217,96,122,.35);
        border-radius: var(--r-lg);
        padding: 30px 16px;
        text-align: center;
        background: linear-gradient(145deg, rgba(217,96,122,.04), rgba(154,126,204,.04));
        cursor: pointer;
        transition: all .28s;
        position: relative;
        overflow: hidden;
    }
    .upload-zone::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(217,96,122,.08), transparent 65%);
        opacity: 0; transition: opacity .3s;
    }
    .upload-zone:hover::before { opacity: 1; }
    .upload-zone:hover { border-color: var(--rose); }

    .upload-svg { margin-bottom: 10px; }
    .upload-title { font-family: var(--font-display); font-size: 13.5px; font-weight: 600; color: var(--text-1); margin-bottom: 4px; }
    .upload-hint  { font-size: 11px; color: var(--text-3); }

    /* =========================================
       PREVIEW IMAGE
    ========================================= */
    .preview-wrap {
        background: rgba(0,0,0,.35);
        border: 1px solid var(--border);
        border-radius: var(--r-md);
        overflow: hidden;
        margin-top: 12px;
    }
    .preview-bar {
        padding: 9px 14px;
        font-size: 10px; font-weight: 700;
        letter-spacing: 1.8px; text-transform: uppercase;
        border-bottom: 1px solid var(--border);
        display: flex; align-items: center; gap: 7px;
    }
    .preview-bar.orig { color: var(--text-2); }
    .preview-bar.result-bar { color: var(--rose-2); }
    .preview-bar .bar-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
    .preview-body { padding: 10px; }

    /* =========================================
       DETECT BUTTON
    ========================================= */
    .stButton > button {
        width: 100% !important;
        padding: 13px 20px !important;
        background: linear-gradient(135deg, #D9607A 0%, #A03058 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--r-md) !important;
        font-family: var(--font-display) !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        letter-spacing: .5px !important;
        cursor: pointer !important;
        transition: all .22s !important;
        box-shadow: 0 4px 20px var(--rose-glow) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.1), transparent);
        transition: left .5s;
    }
    .stButton > button:hover::before { left: 100%; }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 36px rgba(217,96,122,.4) !important;
        background: linear-gradient(135deg, #E8708A 0%, #B84068 100%) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* =========================================
       LOADING OVERLAY
    ========================================= */
    .loader-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 200px;
        gap: 20px;
    }
    .scanner {
        position: relative;
        width: 80px; height: 80px;
    }
    .scanner-ring {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 2px solid transparent;
        animation: spin 1.2s linear infinite;
    }
    .scanner-ring:nth-child(1) {
        border-top-color: var(--rose);
        border-right-color: var(--rose);
        animation-duration: 1.0s;
    }
    .scanner-ring:nth-child(2) {
        inset: 10px;
        border-bottom-color: var(--violet);
        border-left-color: var(--violet);
        animation-duration: 1.4s;
        animation-direction: reverse;
    }
    .scanner-ring:nth-child(3) {
        inset: 20px;
        border-top-color: var(--teal);
        animation-duration: 0.8s;
    }
    .scanner-center {
        position: absolute;
        inset: 0;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        animation: breathe 1.5s ease-in-out infinite;
    }
    .scan-line {
        position: absolute;
        left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--rose), transparent);
        animation: scan 1.5s ease-in-out infinite;
        box-shadow: 0 0 8px var(--rose);
    }
    .loader-text {
        font-family: var(--font-display);
        font-size: 13px; font-weight: 600;
        color: var(--text-2);
        letter-spacing: 1px;
        animation: blink 1.5s ease-in-out infinite;
    }
    .loader-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }

    /* =========================================
       CLASS CHIPS
    ========================================= */
    .chip-row { display: flex; flex-wrap: wrap; gap: 7px; }
    .chip {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 5px 13px;
        border-radius: 100px;
        font-size: 11px; font-weight: 600;
        border: 1px solid;
        letter-spacing: .3px;
        transition: transform .18s, box-shadow .18s;
        cursor: default;
    }
    .chip:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,.3); }
    .chip-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }

    .chip-normal    { background: var(--success-muted); border-color: rgba(86,201,154,.3);   color: var(--success); }
    .chip-dry       { background: var(--amber-muted);   border-color: rgba(232,168,74,.3);    color: var(--amber); }
    .chip-cheilitis { background: var(--danger-muted);  border-color: rgba(224,87,87,.3);     color: var(--danger); }
    .chip-herpes    { background: var(--violet-muted);  border-color: rgba(154,126,204,.3);   color: var(--violet); }
    .chip-stomatitis{ background: var(--sienna-muted);  border-color: rgba(191,138,106,.3);   color: var(--sienna); }

    /* =========================================
       STAT / RESULT ITEMS
    ========================================= */
    .stat-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 13px 16px;
        background: rgba(0,0,0,.28);
        border: 1px solid var(--border);
        border-left: 3px solid var(--rose);
        border-radius: var(--r-sm);
        margin-bottom: 8px;
        transition: background .2s, transform .2s;
        animation: slideRight .4s cubic-bezier(.22,1,.36,1) both;
    }
    .stat-row:hover { background: rgba(217,96,122,.06); transform: translateX(3px); }
    .stat-label { font-size: 13px; font-weight: 500; color: var(--text-2); }
    .stat-conf  { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--rose-2); }
    .bar-bg { height: 3px; background: rgba(255,255,255,.06); border-radius: 10px; overflow: hidden; margin-top: 5px; }
    .bar-fill { height: 100%; border-radius: 10px; background: linear-gradient(90deg, var(--rose), var(--rose-2)); transition: width .9s cubic-bezier(.4,0,.2,1); }

    /* =========================================
       METRIC CARDS
    ========================================= */
    .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 18px; }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-md);
        padding: 18px 14px;
        text-align: center;
        transition: all .25s;
        position: relative;
        overflow: hidden;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--rose), transparent);
        opacity: 0; transition: opacity .3s;
    }
    .metric-card:hover { border-color: var(--border-glow); }
    .metric-card:hover::after { opacity: 1; }
    .metric-val {
        font-family: var(--font-display);
        font-size: 32px; font-weight: 700;
        line-height: 1;
        color: var(--text-1);
        margin-bottom: 5px;
    }
    .metric-val.accent { color: var(--rose); font-size: 20px; }
    .metric-lbl {
        font-size: 9.5px; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: var(--text-3);
    }

    /* =========================================
       HEALTHY BANNER
    ========================================= */
    .healthy-banner {
        display: flex; align-items: center; gap: 16px;
        background: var(--success-muted);
        border: 1px solid rgba(86,201,154,.22);
        border-radius: var(--r-md);
        padding: 20px 22px;
        animation: slideRight .45s cubic-bezier(.22,1,.36,1) both;
    }
    .healthy-icon { font-size: 32px; flex-shrink: 0; }
    .healthy-title { font-family: var(--font-display); font-size: 15px; font-weight: 700; color: var(--success); margin-bottom: 3px; }
    .healthy-sub   { font-size: 12px; color: var(--text-3); line-height: 1.5; }

    /* =========================================
       EMPTY STATE
    ========================================= */
    .empty {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        min-height: 240px;
        gap: 14px; text-align: center; opacity: .45;
    }
    .empty-icon { font-size: 52px; }
    .empty-text { font-size: 13.5px; color: var(--text-2); line-height: 1.7; }

    /* =========================================
       DIVIDER
    ========================================= */
    .divider {
        display: flex; align-items: center; gap: 12px;
        margin: 22px 0;
    }
    .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
    .divider span {
        font-family: var(--font-display);
        font-size: 9.5px; letter-spacing: 2.5px;
        color: var(--text-3); text-transform: uppercase; font-weight: 700;
    }

    /* =========================================
       STREAMLIT OVERRIDES
    ========================================= */
    [data-testid="stImage"] img { border-radius: var(--r-sm); width: 100%; }
    [data-testid="stInfo"] {
        background: rgba(255,255,255,.03) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r-md) !important;
        color: var(--text-2) !important;
    }

    /* =========================================
       FOOTER
    ========================================= */
    .footer {
        margin-top: 3rem;
        padding-top: 1.4rem;
        border-top: 1px solid rgba(255,255,255,.05);
        display: flex; flex-wrap: wrap; gap: 8px;
        justify-content: space-between; align-items: center;
        font-size: 11px; color: var(--text-3); letter-spacing: .4px;
    }
    .footer-brand { font-family: var(--font-display); font-weight: 700; color: var(--text-3); }
    .footer-brand span { color: var(--rose); }

    /* =========================================
       ANIMATIONS
    ========================================= */
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideRight {
        from { opacity: 0; transform: translateX(-14px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: .35; transform: scale(.75); }
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes breathe {
        0%, 100% { transform: scale(1); }
        50%       { transform: scale(1.12); }
    }
    @keyframes scan {
        0%   { top: 0%; opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 1; }
        100% { top: 100%; opacity: 0; }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%       { opacity: .4; }
    }
    @keyframes dots {
        0%  { content: '.'; }
        33% { content: '..'; }
        66% { content: '...'; }
        100%{ content: ''; }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(.97); }
        to   { opacity: 1; transform: scale(1); }
    }

    /* =========================================
       RESPONSIVE — MOBILE
    ========================================= */
    @media (max-width: 768px) {
        .block-container { padding: 1rem .9rem 2rem !important; }

        .hero { padding-bottom: 1.2rem; margin-bottom: 1.2rem; }
        .hero-name { font-size: 20px; }
        .hero-tagline { font-size: 10px; }
        .hero-logo { width: 44px; height: 44px; font-size: 22px; border-radius: 12px; }

        .card { padding: 14px; border-radius: 18px; }
        .upload-zone { padding: 22px 12px; }
        .upload-title { font-size: 12.5px; }

        .metric-grid { gap: 8px; }
        .metric-val { font-size: 24px; }
        .metric-val.accent { font-size: 16px; }
        .metric-lbl { font-size: 9px; letter-spacing: 1.5px; }
        .metric-card { padding: 14px 10px; }

        .stat-conf { font-size: 15px; }
        .stat-label { font-size: 12px; }

        .healthy-banner { gap: 12px; padding: 16px 14px; }
        .healthy-icon { font-size: 26px; }
        .healthy-title { font-size: 13px; }

        .chip { font-size: 10px; padding: 4px 11px; }

        .scanner { width: 60px; height: 60px; }
        .scanner-center { font-size: 18px; }
        .scanner-ring:nth-child(2) { inset: 8px; }
        .scanner-ring:nth-child(3) { inset: 16px; }

        .footer { flex-direction: column; text-align: center; gap: 4px; }
    }

    @media (max-width: 480px) {
        .hero-logo { width: 38px; height: 38px; font-size: 18px; }
        .hero-name { font-size: 18px; }
        .status-pill { padding: 6px 12px; font-size: 10.5px; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MUAT MODEL AI
# ==========================================
@st.cache_resource
def load_model():
    return YOLO('best.pt')

model_loaded = True
try:
    model = load_model()
except Exception:
    model_loaded = False

# ==========================================
# 4. HERO HEADER
# ==========================================
if model_loaded:
    status_class = "status-online"
    status_text  = "Model Aktif"
    status_icon  = '<span class="pulse-dot"></span>'
else:
    status_class = "status-offline"
    status_text  = "Model Tidak Ditemukan"
    status_icon  = "⚠"

st.markdown(f"""
<div class="hero">
    <div class="hero-brand">
        <div class="hero-logo">🫦</div>
        <div>
            <div class="hero-name">LipCare <span>Vision</span> AI</div>
            <div class="hero-tagline">Sistem Deteksi Kesehatan Bibir · YOLOv8</div>
        </div>
    </div>
    <div class="status-pill {status_class}">
        {status_icon} {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ File **best.pt** tidak ditemukan. Pastikan model ada di folder yang sama dengan app.py.")
    st.stop()

# ==========================================
# 5. LAYOUT UTAMA
# ==========================================
col_left, col_right = st.columns([1, 2.3], gap="large")

# ─── PANEL KIRI ───────────────────────────
with col_left:

    # ── INPUT MODE TOGGLE (BARU) ──────────
    # Session state untuk mode input
    if "input_mode" not in st.session_state:
        st.session_state["input_mode"] = "upload"

    mode = st.session_state["input_mode"]

    st.markdown(f"""
    <div class="card" style="margin-bottom:14px;">
        <div class="sec-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--rose)"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
            Sumber Gambar
        </div>
        <div class="mode-toggle">
            <div class="mode-btn {'active' if mode == 'upload' else ''}">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                Upload Foto
            </div>
            <div class="mode-btn {'active' if mode == 'camera' else ''}">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                Kamera Langsung
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    toggle_col1, toggle_col2 = st.columns(2)
    with toggle_col1:
        if st.button("📁  Upload Foto", use_container_width=True):
            st.session_state["input_mode"] = "upload"
            for key in ["results", "current_file_id", "camera_image"]:
                st.session_state.pop(key, None)
            st.rerun()
    with toggle_col2:
        if st.button("📷  Kamera Langsung", use_container_width=True):
            st.session_state["input_mode"] = "camera"
            for key in ["results", "current_file_id", "camera_image"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

    # ── MODE UPLOAD ───────────────────────
    if st.session_state["input_mode"] == "upload":

        st.markdown("""
        <div class="card" style="margin-bottom:14px;">
            <div class="sec-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--rose)"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                Unggah Foto Bibir
            </div>
            <div class="upload-zone">
                <div class="upload-svg">
                    <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="var(--rose)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity=".75"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                </div>
                <div class="upload-title">Pilih atau Drop Foto</div>
                <div class="upload-hint">JPG · PNG · JPEG · Maks 10MB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload",
            type=['jpg', 'png', 'jpeg'],
            label_visibility="collapsed"
        )

        # Deteksi pergantian foto & simpan bytes ke session state
        if uploaded_file is not None:
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.get("current_file_id") != file_id:
                # Foto baru → simpan bytes & hapus hasil lama
                st.session_state["current_file_id"] = file_id
                st.session_state["upload_image"] = uploaded_file.read()
                st.session_state.pop("results", None)
            elif "upload_image" not in st.session_state:
                st.session_state["upload_image"] = uploaded_file.read()
        # Jika uploaded_file None (rerun biasa), jangan hapus session state

        # Ambil bytes dari session state agar aman dari rerun
        import io
        upload_bytes = st.session_state.get("upload_image")

        # Preview thumbnail
        if upload_bytes:
            st.markdown("""
            <div class="preview-wrap">
                <div class="preview-bar orig">
                    <span class="bar-dot"></span> Foto Dipilih
                </div>
                <div class="preview-body">
            """, unsafe_allow_html=True)
            st.image(upload_bytes, use_container_width=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        active_image = Image.open(io.BytesIO(upload_bytes)) if upload_bytes else None

    # ── MODE KAMERA (BARU) ────────────────
    else:
        st.markdown("""
        <div class="card" style="margin-bottom:14px;">
            <div class="sec-label">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--teal)"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                Ambil Foto via Kamera
            </div>
            <div class="camera-zone">
                <div class="camera-title">📷 Arahkan Kamera ke Bibir</div>
                <div class="camera-hint">Pastikan pencahayaan cukup & posisi frontal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        camera_photo = st.camera_input(
            "Ambil Foto",
            label_visibility="collapsed"
        )

        # Simpan foto kamera ke session state & deteksi pergantian foto
        if camera_photo is not None:
            cam_id = f"cam_{camera_photo.size}"
            if st.session_state.get("current_file_id") != cam_id:
                st.session_state["current_file_id"] = cam_id
                if "results" in st.session_state:
                    del st.session_state["results"]
            st.session_state["camera_image"] = camera_photo
        else:
            # Jika kamera direset, bersihkan semua
            for key in ["results", "current_file_id", "camera_image"]:
                if key in st.session_state:
                    del st.session_state[key]

        # Info tip kamera
        st.markdown("""
        <div style="margin-top:10px; padding:11px 13px; background:rgba(74,191,176,.07);
             border-radius:10px; border:1px solid rgba(74,191,176,.2);">
            <p style="margin:0; font-size:11px; color:var(--teal); line-height:1.75;">
                💡 <strong>Tips:</strong> Tekan tombol kamera untuk mengambil snapshot,
                lalu klik <em>Mulai Analisis AI</em> untuk mendeteksi kondisi bibir.
            </p>
        </div>
        """, unsafe_allow_html=True)

        cam_file = st.session_state.get("camera_image")
        active_image = Image.open(cam_file) if cam_file else None

    # ── TOMBOL ANALISIS ───────────────────
    st.markdown("<div style='margin:18px 0 6px;'>", unsafe_allow_html=True)
    mulai_btn = st.button("✦  Mulai Analisis AI", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Kelas Deteksi
    st.markdown("""
    <div class="card">
        <div class="sec-label">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--rose)"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
            Kelas Deteksi
        </div>
        <div class="chip-row">
            <span class="chip chip-normal"><span class="chip-dot"></span> Normal</span>
            <span class="chip chip-dry"><span class="chip-dot"></span> Dry</span>
            <span class="chip chip-cheilitis"><span class="chip-dot"></span> Cheilitis</span>
            <span class="chip chip-herpes"><span class="chip-dot"></span> Herpes</span>
            <span class="chip chip-stomatitis"><span class="chip-dot"></span> Stomatitis</span>
        </div>
        <div style="margin-top:15px; padding:11px 13px; background:rgba(0,0,0,.22); border-radius:10px; border:1px solid var(--border);">
            <p style="margin:0; font-size:11px; color:var(--text-3); line-height:1.75;">
                Gunakan foto bibir dengan pencahayaan cukup, posisi frontal, dan latar belakang netral untuk akurasi optimal.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── PANEL KANAN ──────────────────────────
with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--rose)"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        Panel Analisis
    </div>
    """, unsafe_allow_html=True)

    if active_image:
        image = active_image
        c1, c2 = st.columns(2, gap="small")

        with c1:
            st.markdown("""
            <div class="preview-wrap">
                <div class="preview-bar orig"><span class="bar-dot"></span> Gambar Asli</div>
                <div class="preview-body">
            """, unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="preview-wrap">
                <div class="preview-bar result-bar"><span class="bar-dot"></span> Hasil YOLOv8</div>
                <div class="preview-body">
            """, unsafe_allow_html=True)

            if mulai_btn:
                # Custom loading animation
                st.markdown("""
                <div class="loader-wrap">
                    <div class="scanner">
                        <div class="scanner-ring"></div>
                        <div class="scanner-ring"></div>
                        <div class="scanner-ring"></div>
                        <div class="scanner-center">🫦</div>
                        <div class="scan-line"></div>
                    </div>
                    <div class="loader-text">Memindai<span class="loader-dots"></span></div>
                </div>
                """, unsafe_allow_html=True)

                results = model.predict(image)
                res_img = results[0].plot()
                res_img_rgb = res_img[:, :, ::-1]
                st.session_state["results"] = results

                st.rerun()

            elif "results" in st.session_state:
                results = st.session_state["results"]
                res_img = results[0].plot()
                res_img_rgb = res_img[:, :, ::-1]
                st.markdown('<div style="animation:fadeIn .5s ease both;">', unsafe_allow_html=True)
                st.image(res_img_rgb, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="empty" style="min-height:180px;">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity=".4"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                    <div class="empty-text">Tekan <strong>Mulai Analisis</strong><br>untuk melihat hasil deteksi</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

        # ── Hasil Analisis ──────────────────────
        st.markdown('<div class="divider"><span>Hasil Analisis</span></div>', unsafe_allow_html=True)

        if "results" in st.session_state:
            results = st.session_state["results"]
            boxes   = results[0].boxes

            if len(boxes) == 0:
                st.markdown("""
                <div class="healthy-banner">
                    <div class="healthy-icon">✅</div>
                    <div>
                        <div class="healthy-title">Bibir Sehat & Normal</div>
                        <div class="healthy-sub">Tidak ada indikasi kondisi abnormal yang terdeteksi oleh model AI.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                class_counts  = Counter([model.names[int(b.cls[0])] for b in boxes])
                dominan_class = class_counts.most_common(1)[0][0]
                avg_conf      = sum(float(b.conf[0]) for b in boxes) / len(boxes) * 100

                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-val">{len(boxes)}</div>
                        <div class="metric-lbl">Objek Terdeteksi</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val accent">{dominan_class}</div>
                        <div class="metric-lbl">Indikasi Utama</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val">{avg_conf:.0f}<span style="font-size:16px;color:var(--text-3);">%</span></div>
                        <div class="metric-lbl">Rata‑rata Konfiden</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                for i, box in enumerate(boxes):
                    class_id   = int(box.cls[0])
                    class_name = model.names[class_id]
                    conf       = float(box.conf[0]) * 100
                    delay      = i * 70

                    st.markdown(f"""
                    <div class="stat-row" style="animation-delay:{delay}ms;">
                        <div style="flex:1;">
                            <div class="stat-label">{class_name}</div>
                            <div class="bar-bg">
                                <div class="bar-fill" style="width:{conf:.1f}%;"></div>
                            </div>
                        </div>
                        <div class="stat-conf" style="margin-left:16px;">{conf:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="empty" style="min-height:100px;">
                <div class="empty-text" style="font-size:12px;">Hasil deteksi akan tampil di sini setelah analisis dijalankan.</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # Empty panel kanan
        st.markdown("""
        <div class="empty">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" opacity=".35"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <div class="empty-text">
                Unggah foto atau ambil gambar via kamera<br>untuk memulai analisis kesehatan bibir
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">LipCare <span>Vision</span> AI &nbsp;·&nbsp; 2026</div>
    <div>Untuk keperluan diagnostik awal — bukan pengganti konsultasi medis profesional</div>
</div>
""", unsafe_allow_html=True)