import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import style

st.set_page_config(
    page_title="Mathematics",
    page_icon="∑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "dark" not in st.session_state:
    st.session_state["dark"] = False
if "current_module" not in st.session_state:
    st.session_state["current_module"] = None

style.inject(dark=st.session_state["dark"])

dark  = st.session_state["dark"]
ink   = "#e8e0d4" if dark else "#1a1814"
ink2  = "#9e9080" if dark else "#4a4540"
bg2   = "#181510" if dark else "#f2ede4"
bdr   = "#2a2620" if dark else "#ddd5c8"
card  = "#161410" if dark else "#ffffff"
warm  = "#d4703a" if dark else "#c8602a"
sand  = "#b89848" if dark else "#a8893e"
bg    = "#0f0e0c" if dark else "#f9f6f0"
sage  = "#4a8070" if dark else "#2d5a4e"

st.markdown(f"""
<style>
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
.mod-card {{
    background: {card};
    border: 1px solid {bdr};
    border-radius: 12px;
    padding: 1.4rem 1.5rem 1.3rem;
    margin-bottom: 0;
    transition: all 0.15s ease;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.mod-card:hover {{
    border-color: {warm};
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
}}
.mod-card-num {{
    font-family: 'DM Mono', monospace;
    font-size: 0.54rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {sand};
    margin-bottom: 0.5rem;
}}
.mod-card-title {{
    font-family: 'Fraunces', serif;
    font-size: 1.1rem;
    color: {ink};
    line-height: 1.2;
    margin-bottom: 0.4rem;
    font-weight: 400;
}}
.mod-card-sub {{
    font-size: 0.72rem;
    color: {ink2};
    font-style: italic;
    margin-bottom: 0.7rem;
}}
.mod-card-desc {{
    font-size: 0.78rem;
    color: {ink2};
    line-height: 1.65;
    font-weight: 300;
    flex: 1;
}}
.mod-card-cta {{
    margin-top: 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
}}
.cat-header {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 2.8rem 0 1.1rem;
}}
.cat-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}
.cat-label {{
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {ink2};
}}
.cat-line {{ flex:1; height:1px; background:{bdr}; }}
</style>
""", unsafe_allow_html=True)

MODULES = [
    ( 1, "Quadratic Equations",      "discriminant · formula · graph",           "Algebra",      True),
    ( 2, "Quadratic Inequalities",   "sign analysis · solution sets",            "Algebra",      True),
    ( 3, "Systems of Equations",     "substitution · elimination · geometry",    "Algebra",      True),
    ( 4, "Polynomials",              "Ruffini · factorization · roots",          "Algebra",      True),
    ( 5, "Function Analysis",        "domain · parity · monotonicity",           "Analysis",     True),
    ( 6, "Sequences",                "arithmetic · geometric · limits",          "Analysis",     True),
    ( 7, "Limits",                   "definition · techniques · Bolzano",        "Analysis",     True),
    ( 8, "Trigonometry",             "unit circle · identities · equations",     "Geometry",     True),
    ( 9, "Analytic Geometry 2D",     "lines · circles · conics",                "Geometry",     True),
    (10, "Logarithms & Exponentials","properties · equations · models",          "Analysis",     True),
    (11, "Combinatorics",            "factorials · combinations · Pascal",       "Discrete",     True),
    (12, "Probability",              "classical · conditional · Bayes",          "Discrete",     True),
    (13, "Complex Numbers",          "operations · polar · De Moivre",           "Algebra",      True),
    (14, "Euclidean Geometry",       "triangles · circles · polygons",           "Geometry",     True),
    (15, "Number Theory",            "GCD · primes · Fermat · Goldbach",         "Discrete",     True),
    (16, "Financial Math",           "interest · mortgages · inflation",         "Applied",      True),
    (17, "Parametric Equations",     "lines · circles · cycloids",               "Geometry",     True),
    (18, "Analytic Geometry 3D",     "vectors · lines · planes",                 "Geometry",     True),
    (19, "Mathematical Proofs",      "logic · structure · techniques",           "Foundations",  True),
    (20, "Olympic Mathematics",      "problems · techniques · proofs",           "Foundations",  True),
    (21, "Derivatives",              "Rolle · Lagrange · Cauchy · concavity",    "Analysis",     True),
    (22, "Integrals",                "Riemann · FTC · techniques",               "Analysis",     True),
]

CATEGORY_ORDER  = ["Algebra","Analysis","Geometry","Discrete","Applied","Foundations"]
CATEGORY_COLORS = {
    "Algebra":     "#c8602a",
    "Analysis":    "#2d5a4e",
    "Geometry":    "#7b6fb0",
    "Discrete":    "#a8893e",
    "Applied":     "#4a7a9b",
    "Foundations": "#8b5e3c",
}

def render_topbar(show_back=False):
    theme_icon = "☀️" if dark else "🌙"
    c1, c2 = st.columns([8, 1])
    with c1:
        if show_back:
            if st.button("← Back to chapters", key="back_btn"):
                st.session_state["current_module"] = None
                st.rerun()
        else:
            st.markdown(
                f'<div style="font-family:\'Fraunces\',serif;font-size:1.05rem;'
                f'font-weight:400;color:{ink};padding:0.3rem 0 1rem;">Mathematics</div>',
                unsafe_allow_html=True)
    with c2:
        if st.button(theme_icon, key="theme_btn"):
            st.session_state["dark"] = not st.session_state["dark"]
            st.rerun()


def render_home():
    render_topbar(show_back=False)

    st.markdown(f"""
<div style="max-width:680px;padding:0.5rem 0 0;">
  <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.22em;
              text-transform:uppercase;color:{sand};margin-bottom:1.1rem;">
    A curriculum in 22 chapters
  </div>
  <h1 style="font-family:'Fraunces',serif;font-size:2.9rem;font-weight:400;
             color:{ink};line-height:1.08;margin:0 0 1.4rem;">
    Mathematics is<br>one language.
  </h1>
  <div style="width:48px;height:2px;background:{warm};margin-bottom:1.7rem;"></div>
  <p style="font-size:0.97rem;font-weight:300;color:{ink2};line-height:1.85;
            margin:0 0 0.85rem;max-width:580px;">
    Not a collection of disconnected techniques — a single conversation
    that has been going on for three thousand years. Algebra, geometry,
    analysis, probability: different chapters of the same story,
    written in the only language spoken identically in every country and every century.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{ink2};line-height:1.85;
            margin:0 0 0.85rem;max-width:580px;">
    Learning mathematics is not so different from training for a sport.
    There are <em>drills</em> — the exercises you repeat until the technique becomes automatic.
    There is <em>theory</em> — understanding why the technique works, not just that it does.
    And then there are <em>matches</em>: problems where you don't know in advance
    which tool to use, where you have to read the situation and decide.
    Most mathematics education stops at drills. This program doesn't.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{ink2};line-height:1.85;
            margin:0;max-width:580px;">
    Each chapter starts from intuition — the <em>why</em> before the formula.
    Work through them in order, or jump to what you need.
    The goal is not to memorize, but to understand deeply enough
    that you could reconstruct everything from scratch.
  </p>
</div>
""", unsafe_allow_html=True)

    total = len(MODULES)
    done  = sum(1 for m in MODULES if m[4])
    st.markdown(f"""
<div style="display:flex;gap:0;border:1px solid {bdr};border-radius:10px;
            background:{card};overflow:hidden;width:fit-content;margin:2.2rem 0 0.5rem;">
  <div style="padding:0.9rem 1.8rem;border-right:1px solid {bdr};">
    <div style="font-family:'Fraunces',serif;font-size:1.9rem;color:{ink};line-height:1;">{total}</div>
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.16em;
                text-transform:uppercase;color:{ink2};margin-top:0.2rem;">Chapters</div>
  </div>
  <div style="padding:0.9rem 1.8rem;border-right:1px solid {bdr};">
    <div style="font-family:'Fraunces',serif;font-size:1.9rem;color:{sage};line-height:1;">{done}</div>
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.16em;
                text-transform:uppercase;color:{ink2};margin-top:0.2rem;">Available</div>
  </div>
  <div style="padding:0.9rem 1.8rem;">
    <div style="font-family:'Fraunces',serif;font-size:1.9rem;color:{ink};line-height:1;">∞</div>
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.16em;
                text-transform:uppercase;color:{ink2};margin-top:0.2rem;">Patience</div>
  </div>
</div>
""", unsafe_allow_html=True)

    for cat in CATEGORY_ORDER:
        cat_mods = [m for m in MODULES if m[3] == cat]
        if not cat_mods:
            continue
        cat_color = CATEGORY_COLORS.get(cat, warm)
        st.markdown(f"""
<div class="cat-header">
  <div class="cat-dot" style="background:{cat_color};"></div>
  <div class="cat-label">{cat}</div>
  <div class="cat-line"></div>
</div>
""", unsafe_allow_html=True)

        cols = st.columns(3, gap="medium")
        for i, (n, name, subtitle, _, implemented) in enumerate(cat_mods):
            with cols[i % 3]:
                desc = style.MODULE_DESCRIPTIONS.get(n, "")
                opacity = "1" if implemented else "0.38"
                top_color = cat_color if implemented else bdr
                cta_color = cat_color if implemented else bdr
                cta_text  = "Open chapter →" if implemented else "coming soon"

                st.markdown(f"""
<div class="mod-card" style="opacity:{opacity};border-top:2px solid {top_color};">
  <div>
    <div class="mod-card-num">{n:02d}</div>
    <div class="mod-card-title">{name}</div>
    <div class="mod-card-sub">{subtitle}</div>
    <div class="mod-card-desc">{desc}</div>
  </div>
  <div class="mod-card-cta" style="color:{cta_color};">{cta_text}</div>
</div>
""", unsafe_allow_html=True)

                if implemented:
                    if st.button(f"Open", key=f"open_{n}"):
                        st.session_state["current_module"] = n
                        st.rerun()

    # Feedback
    st.markdown(f"""
<div style="margin:4rem 0 1.5rem;max-width:680px;">
  <div style="width:48px;height:2px;background:{warm};margin-bottom:1.7rem;"></div>
  <h2 style="font-family:'Fraunces',serif;font-size:1.75rem;font-weight:400;
             color:{ink};margin:0 0 0.75rem;">Share your thoughts.</h2>
  <p style="font-size:0.91rem;font-weight:300;color:{ink2};line-height:1.8;
            margin:0;max-width:560px;">
    This is a work in progress — your experience is the best way to improve it.
    Whether you found something confusing, something that worked beautifully,
    or something missing: I genuinely want to hear it.
    Every piece of feedback shapes what this becomes.
  </p>
</div>
""", unsafe_allow_html=True)

    with st.form("feedback_form", clear_on_submit=True):
        col_a, col_b = st.columns([2,1])
        with col_a:
            comment = st.text_area("What's on your mind?",
                placeholder="Which module did you try? What worked? What was unclear? What would you add?",
                height=120)
        with col_b:
            rating = st.select_slider("Rating",
                options=["1 — poor","2 — fair","3 — good","4 — great","5 — excellent"],
                value="3 — good")
            name_field = st.text_input("Name (optional)", placeholder="Anonymous")
        if st.form_submit_button("Send →"):
            if comment.strip():
                if "feedbacks" not in st.session_state:
                    st.session_state["feedbacks"] = []
                st.session_state["feedbacks"].append({
                    "name": name_field.strip() or "Anonymous",
                    "rating": rating[0],
                    "comment": comment.strip(),
                })
                st.success("Thank you — your feedback has been received.")
            else:
                st.warning("Please write something before sending.")

    for fb in st.session_state.get("feedbacks", []):
        stars = "★"*int(fb["rating"]) + "☆"*(5-int(fb["rating"]))
        st.markdown(f"""
<div style="background:{card};border:1px solid {bdr};border-left:3px solid {warm};
            border-radius:0 8px 8px 0;padding:0.85rem 1.1rem;margin-bottom:0.55rem;">
  <div style="display:flex;justify-content:space-between;margin-bottom:0.35rem;">
    <span style="font-size:0.8rem;font-weight:500;color:{ink};">{fb['name']}</span>
    <span style="color:#c8a050;font-size:0.8rem;">{stars}</span>
  </div>
  <div style="font-size:0.82rem;color:{ink2};line-height:1.65;">{fb['comment']}</div>
</div>""", unsafe_allow_html=True)


def render_module(n):
    render_topbar(show_back=True)
    mod = next((m for m in MODULES if m[0] == n), None)
    if not mod:
        return
    _, name, subtitle, category, implemented = mod
    if not implemented:
        style.module_header(category, n, name, subtitle)
        style.coming_soon(n, name)
        return

    if n == 1:
        from modules import step1;  step1.render(n, name, subtitle, category)
    elif n == 2:
        from modules import step2;  step2.render(n, name, subtitle, category)
    elif n == 3:
        from modules import step3;  step3.render(n, name, subtitle, category)
    elif n == 4:
        from modules import step4;  step4.render(n, name, subtitle, category)
    elif n == 5:
        from modules import step5;  step5.render(n, name, subtitle, category)
    elif n == 6:
        from modules import step6;  step6.render(n, name, subtitle, category)
    elif n == 7:
        from modules import step7;  step7.render(n, name, subtitle, category)
    elif n == 8:
        from modules import step8;  step8.render(n, name, subtitle, category)
    elif n == 9:
        from modules import step9;  step9.render(n, name, subtitle, category)
    elif n == 10:
        from modules import step10; step10.render(n, name, subtitle, category)
    elif n == 11:
        from modules import step11; step11.render(n, name, subtitle, category)
    elif n == 12:
        from modules import step12; step12.render(n, name, subtitle, category)
    elif n == 13:
        from modules import step13; step13.render(n, name, subtitle, category)
    elif n == 14:
        from modules import step14; step14.render(n, name, subtitle, category)
    elif n == 15:
        from modules import step15; step15.render(n, name, subtitle, category)
    elif n == 16:
        from modules import step16; step16.render(n, name, subtitle, category)
    elif n == 17:
        from modules import step17; step17.render(n, name, subtitle, category)
    elif n == 18:
        from modules import step18; step18.render(n, name, subtitle, category)
    elif n == 19:
        from modules import step19; step19.render(n, name, subtitle, category)
    elif n == 20:
        from modules import step20; step20.render(n, name, subtitle, category)
    elif n == 21:
        from modules import step21; step21.render(n, name, subtitle, category)
    elif n == 22:
        from modules import step22; step22.render(n, name, subtitle, category)


current = st.session_state.get("current_module")
if current is None:
    render_home()
else:
    render_module(current)