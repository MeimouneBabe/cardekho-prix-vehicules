"""
CarDekho — Enhanced Design System
Uses: Playfair Display (serif headlines) + DM Sans (body) + DM Mono (labels/code).
"""

ENHANCED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── RESETS & TOKENS ──────────────────────────────────────────── */
:root {
    --ink:        #1C1917;
    --ink2:       #44403C;
    --ink3:       #78716C;
    --cream:      #FAFAF8;
    --cream2:     #F5F3EF;
    --cream3:     #EDE9E3;
    --teal:       #0D6E68;
    --teal2:      #0A5652;
    --teal-light: #E8F4F3;
    --amber:      #C2710C;
    --border:     rgba(28,25,23,0.12);
    --border2:    rgba(28,25,23,0.22);
}

/* ── HIDE STREAMLIT CHROME ──────────────────────────────────────── */
[data-testid="collapsedControl"]  { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }
header[data-testid="stHeader"]    { display: none !important; }
#MainMenu                         { display: none !important; }
footer                            { display: none !important; }
[data-testid="stToolbar"]         { display: none !important; }

/* ── GLOBAL TYPOGRAPHY ──────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--ink);
    background-color: var(--cream) !important;
}

/* ── NAVBAR ──────────────────────────────────────────────────────── */
.app-navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 16px;
    background-color: var(--ink);
    padding: 0 28px;
    height: 60px;
    border-bottom: 3px solid var(--teal);
    z-index: 9998;
    box-sizing: border-box;
}
.app-navbar .nav-logo {
    width: 36px; height: 36px;
    background: var(--teal);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.app-navbar .nav-logo svg { width: 20px; height: 20px; fill: white; }
.app-navbar .nav-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: white;
    letter-spacing: 0.01em;
    margin: 0;
}
.app-navbar .nav-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--ink3);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin: 2px 0 0;
}
.app-navbar .nav-badge {
    margin-left: auto;
    background: var(--teal);
    color: white;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

section[data-testid="stMain"] > div:first-child { padding-top: 76px !important; }

/* ── FOOTER ──────────────────────────────────────────────────────── */
.app-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: var(--cream2);
    border-top: 1px solid var(--border);
    padding: 10px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--ink3);
    z-index: 9999;
}
.app-footer .footer-id {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
}
section[data-testid="stMain"] > div { padding-bottom: 60px; }

/* ── HEADINGS ──────────────────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--ink) !important;
}
h1 { font-size: 2rem !important; }
h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.2rem !important; font-weight: 600 !important; }

/* ── SECTION LABELS ──────────────────────────────────────────── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--ink3);
    margin-bottom: 6px;
}

/* ── METRICS ──────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--cream2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px 18px !important;
}
[data-testid="stMetric"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--ink3) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 400 !important;
    color: var(--ink) !important;
}
[data-testid="stMetricDelta"] { display: none; }

/* ── BUTTONS ──────────────────────────────────────────────────── */
[data-testid="stButton"] > button,
.stButton > button {
    background: var(--teal) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 12px 24px !important;
    transition: background 0.15s !important;
}
[data-testid="stButton"] > button:hover,
.stButton > button:hover {
    background: var(--teal2) !important;
    border: none !important;
}
[data-testid="stButton"]:first-of-type > button {
    background: transparent !important;
    color: var(--ink3) !important;
    border: 1px solid var(--border2) !important;
    font-size: 12px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stButton"]:first-of-type > button:hover {
    background: var(--cream2) !important;
    color: var(--ink) !important;
}
/* Restore teal for primary buttons even when first-of-type in their container */
[data-testid="stButton"]:first-of-type > button[data-testid="baseButton-primary"],
[data-testid="stButton"]:first-of-type > button[kind="primary"] {
    background: var(--teal) !important;
    color: white !important;
    border: none !important;
    font-size: 14px !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stButton"]:first-of-type > button[data-testid="baseButton-primary"]:hover {
    background: var(--teal2) !important;
}

/* ── SELECTBOX & INPUTS ──────────────────────────────────────── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--ink3) !important;
    font-weight: 600 !important;
}
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    background: white !important;
    color: var(--ink) !important;
}
[data-baseweb="select"] > div:focus-within,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 2px rgba(13,110,104,0.12) !important;
}

/* ── TABS ──────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: white !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--ink3) !important;
    padding: 14px 20px !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom-color: var(--teal) !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--ink) !important;
    background: var(--cream2) !important;
}

/* ── DATAFRAMES ──────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    background: var(--cream2) !important;
    color: var(--ink3) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] td {
    font-size: 13px !important;
    color: var(--ink2) !important;
}

/* ── ALERTS ──────────────────────────────────────────────────── */
[data-testid="stSuccess"] {
    background: var(--teal-light) !important;
    border-left: 3px solid var(--teal) !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    color: var(--teal2) !important;
}
[data-testid="stInfo"] {
    background: #FEF9EC !important;
    border-left: 3px solid var(--amber) !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    color: var(--ink2) !important;
}
[data-testid="stError"] {
    background: #FFF0EF !important;
    border-left: 3px solid #B91C1C !important;
    border-radius: 6px !important;
}

/* ── EXPANDER ──────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    background: white !important;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--ink3) !important;
    font-weight: 600 !important;
}

/* ── DIVIDERS ──────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}

/* ── FILE UPLOADER ──────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border2) !important;
    border-radius: 8px !important;
    background: var(--cream2) !important;
}
[data-testid="stFileUploader"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--ink3) !important;
}

/* ── DOWNLOAD BUTTON ──────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--teal) !important;
    border: 1px solid var(--teal) !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: var(--teal-light) !important;
}

/* ── SPINNER ──────────────────────────────────────────────────── */
[data-testid="stSpinner"] { color: var(--teal) !important; }

/* ── HERO BANNER ──────────────────────────────────────────────── */
.hero-banner {
    background: var(--ink);
    color: white;
    padding: 64px 48px 64px;
    border-radius: 0;
    margin-top: -76px;
    margin-left:  calc(-50vw + 50%);
    margin-right: calc(-50vw + 50%);
    margin-bottom: 24px;
    width: 100vw;
    min-height: calc(100vh - 60px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(90deg, rgba(255,255,255,.015) 0, rgba(255,255,255,.015) 1px, transparent 1px, transparent 80px),
        repeating-linear-gradient(0deg,  rgba(255,255,255,.015) 0, rgba(255,255,255,.015) 1px, transparent 1px, transparent 80px);
    pointer-events: none;
}
.hero-banner .hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #5DCAA5;
    margin-bottom: 16px;
}
.hero-banner h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.4rem !important;
    line-height: 1.18 !important;
    color: white !important;
    font-weight: 700 !important;
    max-width: 580px;
}
.hero-banner h1 em { color: #5DCAA5; font-style: italic; }
.hero-banner p {
    font-size: 15px;
    color: rgba(255,255,255,.58);
    max-width: 520px;
    line-height: 1.7;
    margin-top: 12px;
}
.hero-cta {
    display: inline-block;
    margin-top: 32px;
    background: var(--teal);
    color: white !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.02em;
    padding: 14px 28px;
    border-radius: 4px;
    text-decoration: none !important;
    transition: background 0.15s;
}
.hero-cta:hover { background: var(--teal2); }

/* ── STEP CARDS ──────────────────────────────────────────────── */
.step-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 24px 20px;
}
.step-card .step-num {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    color: var(--teal);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.step-card h4 {
    font-family: 'Playfair Display', serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    margin-bottom: 8px;
}
.step-card p { font-size: 13px; color: var(--ink3); line-height: 1.65; }

/* ── RESULT PRICE CARD ──────────────────────────────────────── */
.result-display {
    background: var(--ink);
    color: white;
    border-radius: 8px;
    padding: 28px 32px;
    display: flex;
    align-items: center;
    gap: 32px;
    margin-top: 8px;
}
.result-display .price-inr {
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    font-weight: 700;
    line-height: 1;
}
.result-display .price-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: rgba(255,255,255,.4);
    margin-bottom: 6px;
}
.result-display .price-eur {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 600;
    color: #5DCAA5;
}
.result-display .divider {
    width: 1px; height: 60px;
    background: rgba(255,255,255,.12);
}
.result-display .model-badge {
    margin-left: auto;
    background: var(--teal);
    color: white;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 6px 16px;
    border-radius: 3px;
}

/* ── ALGORITHM RADIO CARDS ─────────────────────────────────── */
div[data-testid="stRadio"] > div[role="radiogroup"],
div[data-testid="stRadio"] > div > div[role="radiogroup"] {
    gap: 8px !important;
    flex-direction: column !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
    cursor: pointer !important;
    transition: background 0.15s, border-color 0.15s !important;
    width: 100% !important;
    box-sizing: border-box !important;
    align-items: center !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"]:hover {
    border-color: var(--teal) !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) {
    background: var(--teal) !important;
    border-color: var(--teal) !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stRadio"] [data-baseweb="radio"] [data-testid="stMarkdownContainer"] * {
    color: var(--ink) !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) div,
div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) p,
div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) [data-testid="stMarkdownContainer"] p,
div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) [data-testid="stMarkdownContainer"] * {
    color: white !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] > div:last-child {
    margin-left: 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    line-height: 1.4 !important;
    color: var(--ink) !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] > div:last-child p {
    color: var(--ink) !important;
    margin: 0 !important;
}

/* ── ALGO METRICS GRID ─────────────────────────────────────── */
.algo-metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 16px;
}
.algo-metric {
    background: var(--cream2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
}
.algo-metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--ink3);
    margin-bottom: 6px;
}
.algo-metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    font-weight: 500;
    color: var(--ink);
}

/* ── VARIABLE IMPORTANCE BARS ──────────────────────────────── */
.fi-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border);
}
.fi-row:last-child { border: none; }
.fi-name {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--ink2);
    width: 230px;
    flex-shrink: 0;
}
.fi-bar-wrap {
    flex: 1;
    background: var(--cream3);
    border-radius: 2px;
    height: 7px;
    overflow: hidden;
}
.fi-bar { height: 100%; background: var(--teal); border-radius: 2px; }
.fi-pct {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: var(--ink2);
    min-width: 42px;
    text-align: right;
}
</style>
"""


NAVBAR_HTML = """
<div class="app-navbar">
    <div class="nav-logo">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8
                     c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1
                     v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5
                     S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5s1.5.67 1.5 1.5
                     -.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
        </svg>
    </div>
    <div>
        <p class="nav-title">Prédiction du Prix des Voitures d'Occasion</p>
        <p class="nav-sub">Car Dekho · Projet Python</p>
    </div>
    <span class="nav-badge">ML · 4 Modèles</span>
</div>
"""

FOOTER_HTML = """
<div class="app-footer">
    <div><strong>Étudiant :</strong> Meimoune Baba Cheikh Sidiya &nbsp;·&nbsp; <strong>Matricule :</strong> C34620</div>
    <div class="footer-id">CarDekho · Projet Python · 2024</div>
</div>
"""

HERO_HTML = """
<div class="hero-banner">
    <div class="hero-label">&#x2014;&nbsp; Analyse par Machine Learning</div>
    <h1>Estimez le prix d'une voiture<br><em>d'occasion</em> en quelques secondes</h1>
    <p>Entraîné sur <strong style="color:rgba(255,255,255,.85)">8 128 annonces réelles</strong>
       de la plateforme CarDekho — quatre algorithmes comparés pour une estimation fiable.</p>
</div>
"""


def _fmt_indian(n: int) -> str:
    s = str(abs(int(n)))
    if len(s) <= 3:
        return s
    result = s[-3:]
    s = s[:-3]
    while s:
        chunk = s[-2:] if len(s) > 2 else s
        result = chunk + ',' + result
        s = s[:-2] if len(s) > 2 else ''
    return result


def result_card_html(price_inr: float, model_name: str, car_label: str = "") -> str:
    price_eur = price_inr / 90
    inr_str = _fmt_indian(int(price_inr))
    eur_str = f"{price_eur:,.0f}".replace(",", " ")
    return f"""
<div class="result-display">
    <div>
        <div class="price-label">Prix estimé</div>
        <div class="price-inr">₹ {inr_str}</div>
        <div style="font-size:12px;color:rgba(255,255,255,.35);margin-top:5px">{car_label}</div>
    </div>
    <div class="divider"></div>
    <div>
        <div class="price-label">Équivalent</div>
        <div class="price-eur">≈ {eur_str} €</div>
    </div>
    <div class="model-badge">{model_name}</div>
</div>
"""
