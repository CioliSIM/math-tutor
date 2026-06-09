import streamlit as st


def inject():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=DM+Mono:wght@400;500&family=Nunito:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:       #fdfaf5;
    --bg2:      #f7f2ea;
    --ink:      #1a1814;
    --ink2:     #4a4540;
    --warm:     #e8602a;
    --warm2:    #f0956a;
    --sage:     #3d6b5e;
    --sage2:    #5a9080;
    --sand:     #c8a96e;
    --sand2:    #e8d5a8;
    --lavender: #7b6fb0;
    --border:   #e0d8cc;
    --card:     #ffffff;
}

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--bg) !important;
    font-family: 'Nunito', sans-serif;
    color: var(--ink);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header       { visibility: hidden; }
[data-testid="stDecoration"]    { display: none; }
[data-testid="stSidebarNav"]    { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 1px solid #2e2a25 !important;
}
[data-testid="stSidebar"] * {
    color: #f0ebe3 !important;
    font-family: 'Nunito', sans-serif !important;
}

/* sidebar radio → nav items */
[data-testid="stSidebar"] .stRadio > div        { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    display: block;
    padding: 0.42rem 1.2rem 0.42rem 1.1rem !important;
    border-left: 2px solid transparent;
    font-size: 0.83rem !important;
    color: #9e9080 !important;
    cursor: pointer;
    transition: all 0.12s;
    line-height: 1.4;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #22201c !important;
    color: #e8ddd0 !important;
    border-left-color: var(--sand) !important;
}
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    padding: 0 !important;
    background: transparent !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    margin: 0 !important;
}

/* ── Module page header ── */
.mod-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--sage);
    margin-bottom: 0.4rem;
}
.mod-title {
    font-family: 'Fraunces', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: var(--ink);
    line-height: 1.05;
    margin: 0;
}
.mod-sub {
    font-size: 0.88rem;
    color: var(--ink2);
    margin-top: 0.4rem;
    font-style: italic;
}
.mod-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0 1.5rem;
}

/* ── Input panel ── */
.input-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.3rem 1.4rem;
}
.input-panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.9rem;
}
.eq-display {
    font-family: 'Fraunces', serif;
    font-size: 1.3rem;
    text-align: center;
    padding: 0.75rem;
    background: var(--bg2);
    border-radius: 6px;
    margin: 0.8rem 0 1rem;
    color: var(--ink);
}
.hint-panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.9rem 1rem;
    margin-top: 0.8rem;
}
.hint-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.5rem;
}
.hint-body {
    font-size: 0.78rem;
    color: var(--ink2);
    line-height: 1.9;
}
.hint-body code {
    font-family: 'DM Mono', monospace;
    background: var(--card);
    padding: 0.05rem 0.35rem;
    border-radius: 4px;
    font-size: 0.82em;
}

/* ── Streamlit inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    color: var(--ink) !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--warm) !important;
    box-shadow: 0 0 0 2px rgba(232,96,42,0.12) !important;
}

/* ── Solve button ── */
.stButton > button {
    background: var(--warm) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    padding: 0.6rem 1.6rem !important;
    transition: background 0.12s !important;
    width: 100% !important;
}
.stButton > button:hover { background: #d4521f !important; }
.stButton > button:active { background: var(--sage) !important; }

/* ── Step boxes ── */
.step {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem 1rem 1.5rem;
    margin-bottom: 0.7rem;
    position: relative;
    animation: fadeUp 0.28s ease both;
}
.step::before {
    content: '';
    position: absolute;
    left: 0; top: 0.6rem; bottom: 0.6rem;
    width: 3px;
    background: var(--sand2);
    border-radius: 0 2px 2px 0;
}
.step.warm::before  { background: var(--warm); }
.step.sage::before  { background: var(--sage); }
.step.error::before { background: #c0392b; }

.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.5rem;
}
.step-body {
    font-size: 0.88rem;
    line-height: 1.78;
    color: var(--ink2);
}
.step-body code {
    font-family: 'DM Mono', monospace;
    background: var(--bg2);
    padding: 0.08rem 0.32rem;
    border-radius: 4px;
    font-size: 0.83em;
    color: var(--ink);
}
.step-body .mf {
    font-family: 'Fraunces', serif;
    font-size: 1.08em;
    color: var(--ink);
}
.step-body strong { color: var(--ink); }

/* staggered fade */
.step:nth-child(1) { animation-delay: 0.03s; }
.step:nth-child(2) { animation-delay: 0.09s; }
.step:nth-child(3) { animation-delay: 0.15s; }
.step:nth-child(4) { animation-delay: 0.21s; }
.step:nth-child(5) { animation-delay: 0.27s; }
.step:nth-child(6) { animation-delay: 0.33s; }
.step:nth-child(7) { animation-delay: 0.39s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(7px); }
    to   { opacity: 1; transform: translateY(0);   }
}

/* ── Result band ── */
.result-band {
    display: flex;
    background: var(--ink);
    border-radius: 10px;
    overflow: hidden;
    margin: 0.8rem 0 1.2rem;
}
.res-block {
    flex: 1;
    padding: 1rem 1.3rem;
    border-right: 1px solid #2e2a25;
}
.res-block:last-child { border-right: none; }
.res-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.57rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.3rem;
}
.res-value {
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    color: #f0ebe3;
    line-height: 1.1;
}

/* ── Verify pills ── */
.pills { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; }
.pill {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    background: #eef4f1;
    border: 1px solid #8ab89a;
    color: #2d5a3e;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
}

/* ── Graph label ── */
.graph-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--sand);
    margin: 1.5rem 0 0.5rem;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 280px;
    color: var(--ink2);
    text-align: center;
    gap: 0.7rem;
}
.empty-symbol {
    font-family: 'Fraunces', serif;
    font-size: 4rem;
    opacity: 0.1;
    color: var(--ink);
    line-height: 1;
}
.empty-text {
    font-size: 0.85rem;
    font-weight: 300;
    color: var(--ink2);
}

/* ── Coming soon ── */
.coming-soon {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--sand2);
    border-radius: 0 8px 8px 0;
    padding: 1.4rem 1.6rem;
    font-size: 0.88rem;
    color: var(--ink2);
    line-height: 1.7;
}
.coming-soon code {
    font-family: 'DM Mono', monospace;
    background: var(--card);
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
    font-size: 0.85em;
    color: var(--ink);
}

/* ── Matplotlib plots ── */
[data-testid="stImage"] img,
.stPyplot img {
    border-radius: 8px;
    border: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)


# ── Reusable HTML helpers ─────────────────────────────────────────────────────

def step(label, body, variant=""):
    """Render a step box. variant: '' | 'warm' | 'sage' | 'error'"""
    cls = f"step {variant}".strip()
    st.markdown(f"""
<div class="{cls}">
  <div class="step-label">{label}</div>
  <div class="step-body">{body}</div>
</div>""", unsafe_allow_html=True)


def result_band(*blocks):
    """
    Render the dark result band.
    blocks: list of (label, value) tuples.
    """
    inner = "".join(
        f'<div class="res-block"><div class="res-label">{lbl}</div>'
        f'<div class="res-value">{val}</div></div>'
        for lbl, val in blocks
    )
    st.markdown(f'<div class="result-band">{inner}</div>',
                unsafe_allow_html=True)


def pills(*items):
    """Render green verify pills."""
    inner = "".join(f'<span class="pill">{item}</span>' for item in items)
    st.markdown(f'<div class="pills">{inner}</div>', unsafe_allow_html=True)


def module_header(category, number, title, subtitle):
    st.markdown(f"""
<div class="mod-meta">{category} · Chapter {number:02d}</div>
<h1 class="mod-title">{title}</h1>
<div class="mod-sub">{subtitle}</div>
<hr class="mod-divider">
""", unsafe_allow_html=True)


def empty_state(symbol="∫"):
    st.markdown(f"""
<div class="empty-state">
  <div class="empty-symbol">{symbol}</div>
  <div class="empty-text">Enter values and press Solve</div>
</div>""", unsafe_allow_html=True)


def coming_soon(number, name):
    st.markdown(f"""
<div class="coming-soon">
  <strong>Chapter {number:02d} — {name}</strong> is not yet available
  in the web interface.<br>
  Use the terminal version in the meantime:
  <code>python main.py</code> → option {number}.
</div>""", unsafe_allow_html=True)