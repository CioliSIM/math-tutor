import streamlit as st

# ── Module descriptions ───────────────────────────────────────────────────────
MODULE_DESCRIPTIONS = {
    1:  "The quadratic equation is the first place where algebra stops being arithmetic and becomes something deeper. You will understand why the discriminant tells the whole story — before you touch the formula.",
    2:  "Inequalities demand a different kind of thinking: not a single answer, but an entire region. The sign chart makes it visual and exact.",
    3:  "When two conditions must hold simultaneously, the geometry and the algebra are the same problem. Substitution and elimination — two roads to the same destination.",
    4:  "Every polynomial carries its zeros inside it. Ruffini's device and factorization make them visible. The Fundamental Theorem of Algebra says they are always there.",
    5:  "A function is a machine. Domain, parity, zeros, monotonicity — these are its technical specifications. Sympy computes them; intuition explains them.",
    6:  "Sequences are the simplest infinite objects. Arithmetic, geometric, Fibonacci — each grows by a different internal logic. Limits reveal where they are heading.",
    7:  "The limit is the central concept of analysis. What does a function approach as the input moves? The answer defines continuity, derivatives, and integrals.",
    8:  "Trigonometry is the mathematics of angles and circles — and of everything periodic. The unit circle unifies all six functions. The identities are not to be memorized but derived.",
    9:  "Descartes' insight: every geometric object is an equation. Lines, circles, parabolas — all described algebraically. Distance and intersection become algebra.",
    10: "Logarithms were invented to turn multiplication into addition. Today they model everything that grows or decays proportionally — from compound interest to radioactive decay.",
    11: "How many ways can n objects be arranged? How many subsets of size k? Combinatorics answers questions of counting that intuition consistently gets wrong.",
    12: "Probability is the mathematics of uncertainty. Classical probability, conditional probability, Bayes' theorem — each a sharper tool for reasoning under incomplete information.",
    13: "The complex numbers complete the number system. Every polynomial has roots here. Euler's formula e^(iπ)+1=0 connects five fundamental constants in one equation.",
    14: "Euclidean geometry is 2000 years old and still the foundation. Triangles, circles, polygons — with the classical theorems of Thales, Ceva, and Menelaus.",
    15: "Number theory asks simple questions about integers that have resisted mathematicians for centuries. GCD, primes, Fermat's little theorem — and unsolved problems like Goldbach's conjecture.",
    16: "Mathematics meets money. Compound interest, present value, annuities, mortgage amortization — the formulas that govern financial decisions, derived from first principles.",
    17: "Some curves cannot be written as y=f(x). Parametric equations describe the journey, not just the shape. Cycloids, spirals, Lissajous figures — curves that Cartesian form cannot express.",
    18: "Three-dimensional analytic geometry. Vectors, dot products, cross products, lines and planes in space. Skew lines exist here — something impossible in 2D.",
    19: "How do you prove something? Velleman's method: read the goal's logical form, choose the strategy, write forward. Direct proof, contrapositive, induction — each has its place.",
    20: "Olympiad mathematics is not about knowing more formulas. It is about thinking. Invariants, colorings, pigeonhole, infinite descent, double counting — tools for problems you have never seen.",
    21: "The derivative measures instantaneous rate of change. Newton and Leibniz invented it in the 1660s to describe planetary motion. Today it underpins physics, economics, and machine learning.",
    22: "The integral accumulates. Area, volume, average value, total distance — all are integrals. The Fundamental Theorem connects integration and differentiation in one of mathematics' deepest results.",
}

LIGHT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=DM+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:       #f9f6f0;
    --bg2:      #f2ede4;
    --ink:      #1a1814;
    --ink2:     #4a4540;
    --warm:     #c8602a;
    --warm2:    #e07848;
    --sage:     #2d5a4e;
    --sage2:    #4a8070;
    --sand:     #a8893e;
    --sand2:    #d4c080;
    --border:   #ddd5c8;
    --card:     #ffffff;
    --sidebar:  #1a1814;
    --sid-text: #9e9080;
    --sid-act:  #c8a96e;
}
"""

DARK_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=DM+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:       #0f0e0c;
    --bg2:      #181510;
    --ink:      #e8e0d4;
    --ink2:     #9e9080;
    --warm:     #d4703a;
    --warm2:    #e89060;
    --sage:     #4a8070;
    --sage2:    #6aaa90;
    --sand:     #b89848;
    --sand2:    #d4b860;
    --border:   #2a2620;
    --card:     #161410;
    --sidebar:  #0a0908;
    --sid-text: #6a6058;
    --sid-act:  #b89848;
}
"""

SHARED_CSS = """
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

#MainMenu, footer, header       { visibility: hidden; }
[data-testid="stDecoration"]    { display: none; }
[data-testid="stSidebarNav"]    { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
    border-right: 1px solid #1e1c18 !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    display: block;
    padding: 0.38rem 1.2rem 0.38rem 1.1rem !important;
    border-left: 2px solid transparent;
    font-size: 0.8rem !important;
    color: var(--sid-text) !important;
    cursor: pointer;
    transition: all 0.1s;
    line-height: 1.4;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.04) !important;
    color: var(--sid-act) !important;
    border-left-color: var(--sid-act) !important;
}
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

/* ── Module header ── */
.mod-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--sage);
    margin-bottom: 0.4rem;
}
.mod-title {
    font-family: 'Fraunces', serif;
    font-size: 2.5rem;
    font-weight: 400;
    color: var(--ink);
    line-height: 1.05;
    margin: 0;
}
.mod-sub {
    font-size: 0.85rem;
    color: var(--ink2);
    margin-top: 0.35rem;
    font-style: italic;
}
.mod-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.1rem 0 1.4rem;
}

/* ── Input panel ── */
.input-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.3rem;
}
.input-panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.8rem;
}
.eq-display {
    font-family: 'Fraunces', serif;
    font-size: 1.25rem;
    text-align: center;
    padding: 0.7rem;
    background: var(--bg2);
    border-radius: 6px;
    margin: 0.7rem 0 0.9rem;
    color: var(--ink);
}
.hint-panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.85rem 0.95rem;
    margin-top: 0.75rem;
}
.hint-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.45rem;
}
.hint-body {
    font-size: 0.76rem;
    color: var(--ink2);
    line-height: 1.9;
}
.hint-body code {
    font-family: 'DM Mono', monospace;
    background: var(--card);
    padding: 0.04rem 0.3rem;
    border-radius: 3px;
    font-size: 0.82em;
}

/* ── Streamlit inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    color: var(--ink) !important;
    font-size: 0.93rem !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--warm) !important;
    box-shadow: 0 0 0 2px rgba(200,96,42,0.12) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: var(--ink2) !important;
    font-size: 0.8rem !important;
}
.stSelectbox > div > div {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--ink) !important;
    border-radius: 6px !important;
}

/* ── Solve button ── */
.stButton > button {
    background: var(--warm) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    padding: 0.58rem 1.5rem !important;
    transition: background 0.12s !important;
    width: 100% !important;
}
.stButton > button:hover  { background: var(--warm2) !important; }
.stButton > button:active { background: var(--sage)  !important; }

/* ── Step boxes ── */
.step {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.95rem 1.1rem 0.95rem 1.4rem;
    margin-bottom: 0.65rem;
    position: relative;
    animation: fadeUp 0.25s ease both;
}
.step::before {
    content: '';
    position: absolute;
    left: 0; top: 0.55rem; bottom: 0.55rem;
    width: 3px;
    background: var(--border);
    border-radius: 0 2px 2px 0;
}
.step.warm::before  { background: var(--warm); }
.step.sage::before  { background: var(--sage); }
.step.error::before { background: #b03030; }

.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand);
    margin-bottom: 0.45rem;
}
.step-body {
    font-size: 0.87rem;
    line-height: 1.78;
    color: var(--ink2);
}
.step-body code {
    font-family: 'DM Mono', monospace;
    background: var(--bg2);
    padding: 0.06rem 0.3rem;
    border-radius: 3px;
    font-size: 0.83em;
    color: var(--ink);
}
.step-body .mf {
    font-family: 'Fraunces', serif;
    font-size: 1.07em;
    color: var(--ink);
}
.step-body strong { color: var(--ink); }
.step-body pre {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 0.6rem 0.8rem;
    font-size: 0.8rem;
    white-space: pre-wrap;
    color: var(--ink2);
}

.step:nth-child(1) { animation-delay: 0.02s; }
.step:nth-child(2) { animation-delay: 0.07s; }
.step:nth-child(3) { animation-delay: 0.12s; }
.step:nth-child(4) { animation-delay: 0.17s; }
.step:nth-child(5) { animation-delay: 0.22s; }
.step:nth-child(6) { animation-delay: 0.27s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0);   }
}

/* ── Result band ── */
.result-band {
    display: flex;
    background: var(--ink);
    border-radius: 10px;
    overflow: hidden;
    margin: 0.75rem 0 1.1rem;
}
.res-block {
    flex: 1;
    padding: 0.9rem 1.2rem;
    border-right: 1px solid rgba(255,255,255,0.06);
}
.res-block:last-child { border-right: none; }
.res-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sand2);
    margin-bottom: 0.25rem;
}
.res-value {
    font-family: 'Fraunces', serif;
    font-size: 1.45rem;
    color: var(--bg);
    line-height: 1.1;
}

/* ── Verify pills ── */
.pills { display: flex; gap: 0.45rem; flex-wrap: wrap; margin-top: 0.45rem; }
.pill {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    background: rgba(74,128,112,0.12);
    border: 1px solid var(--sage2);
    color: var(--sage2);
    padding: 0.22rem 0.6rem;
    border-radius: 20px;
}

/* ── Graph label ── */
.graph-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--sand);
    margin: 1.4rem 0 0.45rem;
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
    gap: 0.65rem;
}
.empty-symbol {
    font-family: 'Fraunces', serif;
    font-size: 4rem;
    opacity: 0.08;
    color: var(--ink);
    line-height: 1;
}
.empty-text {
    font-size: 0.83rem;
    font-weight: 300;
    color: var(--ink2);
}

/* ── Coming soon ── */
.coming-soon {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--sand2);
    border-radius: 0 8px 8px 0;
    padding: 1.3rem 1.5rem;
    font-size: 0.86rem;
    color: var(--ink2);
    line-height: 1.7;
}

/* ── Plots ── */
[data-testid="stImage"] img, .stPyplot img {
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* ── Checkbox ── */
.stCheckbox label { color: var(--ink2) !important; font-size: 0.82rem !important; }
"""


def inject(dark=False):
    palette = DARK_CSS if dark else LIGHT_CSS
    st.markdown(f"<style>{palette}{SHARED_CSS}</style>", unsafe_allow_html=True)


# ── Reusable helpers ──────────────────────────────────────────────────────────

def step(label, body, variant=""):
    cls = f"step {variant}".strip()
    st.markdown(f"""
<div class="{cls}">
  <div class="step-label">{label}</div>
  <div class="step-body">{body}</div>
</div>""", unsafe_allow_html=True)


def result_band(*blocks):
    inner = "".join(
        f'<div class="res-block"><div class="res-label">{lbl}</div>'
        f'<div class="res-value">{val}</div></div>'
        for lbl, val in blocks
    )
    st.markdown(f'<div class="result-band">{inner}</div>', unsafe_allow_html=True)


def pills(*items):
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
  <strong>Chapter {number:02d} — {name}</strong> is not yet available in the web interface.
</div>""", unsafe_allow_html=True)