import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import style

st.set_page_config(
    page_title="Mathematics",
    page_icon="∑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme toggle (persisted in session) ───────────────────────────────────────
if "dark" not in st.session_state:
    st.session_state["dark"] = False

# ── Inject CSS ────────────────────────────────────────────────────────────────
style.inject(dark=st.session_state["dark"])

# ── Module registry ───────────────────────────────────────────────────────────
MODULES = [
    # (n, name, subtitle, category, implemented)
    ( 1, "Quadratic Equations",     "discriminant · formula · graph",           "Algebra",      True),
    ( 2, "Quadratic Inequalities",  "sign analysis · solution sets",            "Algebra",      True),
    ( 3, "Systems of Equations",    "substitution · elimination · geometry",    "Algebra",      True),
    ( 4, "Polynomials",             "Ruffini · factorization · roots",          "Algebra",      True),
    ( 5, "Function Analysis",       "domain · parity · monotonicity",           "Analysis",     True),
    ( 6, "Sequences",               "arithmetic · geometric · limits",          "Analysis",     True),
    ( 7, "Limits",                  "definition · techniques · asymptotes",     "Analysis",     True),
    ( 8, "Trigonometry",            "unit circle · identities · equations",     "Geometry",     True),
    ( 9, "Analytic Geometry 2D",    "lines · circles · conics",                 "Geometry",     True),
    (10, "Logarithms & Exponentials","properties · equations · models",         "Analysis",     True),
    (11, "Combinatorics",           "factorials · combinations · Pascal",       "Discrete",     True),
    (12, "Probability",             "classical · conditional · Bayes",          "Discrete",     True),
    (13, "Complex Numbers",         "operations · polar · De Moivre",           "Algebra",      True),
    (14, "Euclidean Geometry",      "triangles · circles · polygons",           "Geometry",     True),
    (15, "Number Theory",           "GCD · primes · Fermat · Goldbach",         "Discrete",     True),
    (16, "Financial Math",          "interest · mortgages · inflation",         "Applied",      True),
    (17, "Parametric Equations",    "lines · circles · cycloids",               "Geometry",     True),
    (18, "Analytic Geometry 3D",    "vectors · lines · planes",                 "Geometry",     True),
    (19, "Mathematical Proofs",     "logic · structure · techniques",           "Foundations",  True),
    (20, "Olympic Mathematics",     "problems · techniques · proofs",           "Foundations",  True),
    (21, "Derivatives",             "limits · rules · applications",            "Analysis",     True),
    (22, "Integrals",               "Riemann · FTC · techniques",               "Analysis",     True),
]

CATEGORY_ORDER = ["Algebra", "Analysis", "Geometry", "Discrete", "Applied", "Foundations"]

CATEGORY_COLORS = {
    "Algebra":     "#c8602a",
    "Analysis":    "#2d5a4e",
    "Geometry":    "#7b6fb0",
    "Discrete":    "#a8893e",
    "Applied":     "#4a7a9b",
    "Foundations": "#8b5e3c",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Theme toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;'
            'letter-spacing:0.14em;text-transform:uppercase;color:#6a6058;'
            'padding:0.8rem 0.1rem 0.4rem;">Mathematics</div>',
            unsafe_allow_html=True)
    with col2:
        theme_label = "☀️" if st.session_state["dark"] else "🌙"
        if st.button(theme_label, key="theme_btn"):
            st.session_state["dark"] = not st.session_state["dark"]
            st.rerun()

    st.markdown(
        '<div style="height:1px;background:#1e1c18;margin:0 0 0.6rem;"></div>',
        unsafe_allow_html=True)

    nav_options = ["Home"] + [f"{n:02d}. {name}" for n, name, *_ in MODULES]
    selection = st.radio("nav", nav_options, label_visibility="collapsed", key="nav")

# ── Home page ─────────────────────────────────────────────────────────────────
def render_home():
    dark = st.session_state.get("dark", False)
    ink  = "#e8e0d4" if dark else "#1a1814"
    ink2 = "#9e9080" if dark else "#4a4540"
    bg2  = "#181510" if dark else "#f2ede4"
    bdr  = "#2a2620" if dark else "#ddd5c8"
    card = "#161410" if dark else "#ffffff"
    warm = "#d4703a" if dark else "#c8602a"
    sage = "#4a8070" if dark else "#2d5a4e"
    sand = "#b89848" if dark else "#a8893e"

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="max-width:680px; padding: 3rem 0 1rem;">
  <div style="font-family:'DM Mono',monospace; font-size:0.6rem;
              letter-spacing:0.22em; text-transform:uppercase;
              color:{sand}; margin-bottom:1.2rem;">
    A curriculum in 22 chapters
  </div>
  <h1 style="font-family:'Fraunces',serif; font-size:3.2rem;
             font-weight:400; color:{ink}; line-height:1.08; margin:0 0 1.5rem;">
    Mathematics is<br>one language.
  </h1>
  <div style="width:48px; height:2px; background:{warm}; margin-bottom:1.8rem;"></div>
  <p style="font-size:1.02rem; font-weight:300; color:{ink2};
            line-height:1.85; margin:0 0 1rem; max-width:580px;">
    Not a collection of disconnected techniques, but a single conversation
    that has been going on for three thousand years. Algebra, geometry,
    analysis, probability — different chapters of the same story.
  </p>
  <p style="font-size:1.02rem; font-weight:300; color:{ink2};
            line-height:1.85; margin:0 0 1rem; max-width:580px;">
    Each chapter starts from intuition, not formulas. You will understand
    <em>why</em> the quadratic formula works before you use it.
    You will see <em>why</em> the derivative is a slope, the integral an area,
    and why these two ideas are secretly the same operation.
  </p>
  <p style="font-size:1.02rem; font-weight:300; color:{ink2};
            line-height:1.85; margin:0; max-width:580px;">
    Mathematics is the only language spoken the same way in every country,
    in every century. This program is an introduction to that language —
    written for anyone willing to think carefully.
  </p>
</div>
""", unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────────────────────────
    total = len(MODULES)
    done  = sum(1 for m in MODULES if m[4])
    st.markdown(f"""
<div style="display:flex; gap:0; border:1px solid {bdr}; border-radius:10px;
            background:{card}; overflow:hidden; width:fit-content;
            margin:2.5rem 0 3.5rem;">
  <div style="padding:1rem 2rem; border-right:1px solid {bdr};">
    <div style="font-family:'Fraunces',serif; font-size:2.2rem;
                color:{ink}; line-height:1;">{total}</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.55rem;
                letter-spacing:0.16em; text-transform:uppercase;
                color:{ink2}; margin-top:0.2rem;">Chapters</div>
  </div>
  <div style="padding:1rem 2rem; border-right:1px solid {bdr};">
    <div style="font-family:'Fraunces',serif; font-size:2.2rem;
                color:{sage}; line-height:1;">{done}</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.55rem;
                letter-spacing:0.16em; text-transform:uppercase;
                color:{ink2}; margin-top:0.2rem;">Available</div>
  </div>
  <div style="padding:1rem 2rem;">
    <div style="font-family:'Fraunces',serif; font-size:2.2rem;
                color:{ink}; line-height:1;">∞</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.55rem;
                letter-spacing:0.16em; text-transform:uppercase;
                color:{ink2}; margin-top:0.2rem;">Patience</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Module cards by category ──────────────────────────────────────────────
    for cat in CATEGORY_ORDER:
        cat_mods = [m for m in MODULES if m[3] == cat]
        if not cat_mods:
            continue

        cat_color = CATEGORY_COLORS.get(cat, warm)
        st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.9rem; margin:2.8rem 0 1.2rem;">
  <div style="width:8px; height:8px; border-radius:50%;
              background:{cat_color}; flex-shrink:0;"></div>
  <div style="font-family:'DM Mono',monospace; font-size:0.58rem;
              letter-spacing:0.2em; text-transform:uppercase;
              color:{ink2};">{cat}</div>
  <div style="flex:1; height:1px; background:{bdr};"></div>
</div>
""", unsafe_allow_html=True)

        cols = st.columns(3, gap="small")
        for i, (n, name, subtitle, _, implemented) in enumerate(cat_mods):
            with cols[i % 3]:
                desc = style.MODULE_DESCRIPTIONS.get(n, "")
                cat_color = CATEGORY_COLORS.get(cat, warm)
                opacity = "1" if implemented else "0.45"
                top_border = f"border-top:2px solid {cat_color};" if implemented else f"border-top:2px solid {bdr};"

                st.markdown(f"""
<div style="background:{card}; border:1px solid {bdr}; border-radius:10px;
            padding:1.3rem 1.4rem 1.2rem; margin-bottom:12px;
            {top_border} opacity:{opacity}; min-height:180px;
            display:flex; flex-direction:column; justify-content:space-between;">
  <div>
    <div style="font-family:'DM Mono',monospace; font-size:0.54rem;
                letter-spacing:0.16em; text-transform:uppercase;
                color:{sand}; margin-bottom:0.5rem;">{n:02d}</div>
    <div style="font-family:'Fraunces',serif; font-size:1.05rem;
                color:{ink}; line-height:1.2; margin-bottom:0.5rem;
                font-weight:400;">{name}</div>
    <div style="font-size:0.72rem; color:{ink2}; font-style:italic;
                margin-bottom:0.7rem;">{subtitle}</div>
    <div style="font-size:0.78rem; color:{ink2}; line-height:1.65;
                font-weight:300;">{desc}</div>
  </div>
  <div style="margin-top:1rem; font-family:'DM Mono',monospace;
              font-size:0.58rem; letter-spacing:0.1em;
              color:{''+cat_color if implemented else bdr};">
    {'← select in sidebar' if implemented else 'coming soon'}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Feedback section ──────────────────────────────────────────────────────
    st.markdown(f"""
<div style="margin:4rem 0 1.5rem; max-width:680px;">
  <div style="width:48px; height:2px; background:{warm}; margin-bottom:1.8rem;"></div>
  <h2 style="font-family:'Fraunces',serif; font-size:1.9rem; font-weight:400;
             color:{ink}; margin:0 0 0.8rem;">Share your thoughts.</h2>
  <p style="font-size:0.93rem; font-weight:300; color:{ink2};
            line-height:1.8; margin:0 0 1.5rem; max-width:560px;">
    This program is a work in progress — and your experience is the best way
    to improve it. Whether you found something confusing, something that worked
    beautifully, or something missing entirely: I want to hear it.
    Every piece of feedback, however small, shapes what this becomes.
  </p>
</div>
""", unsafe_allow_html=True)

    with st.form("feedback_form", clear_on_submit=True):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            comment = st.text_area(
                "What's on your mind?",
                placeholder="Which module did you try? What worked well? What was unclear? What would you add?",
                height=130,
            )
        with col_b:
            rating = st.select_slider(
                "Overall rating",
                options=["1 — poor", "2 — fair", "3 — good", "4 — great", "5 — excellent"],
                value="3 — good",
            )
            name_field = st.text_input("Your name (optional)", placeholder="Anonymous")

        submitted = st.form_submit_button("Send feedback →")
        if submitted:
            if comment.strip():
                # Store in session for display (no external DB needed)
                if "feedbacks" not in st.session_state:
                    st.session_state["feedbacks"] = []
                st.session_state["feedbacks"].append({
                    "name": name_field.strip() or "Anonymous",
                    "rating": rating[0],
                    "comment": comment.strip(),
                })
                st.success("Thank you — your feedback has been received. It genuinely helps.")
            else:
                st.warning("Please write something before sending.")

    # Show collected feedback (this session)
    feedbacks = st.session_state.get("feedbacks", [])
    if feedbacks:
        st.markdown(f"""
<div style="margin-top:1.5rem; font-family:'DM Mono',monospace; font-size:0.56rem;
            letter-spacing:0.16em; text-transform:uppercase; color:{sand};
            margin-bottom:0.8rem;">Feedback received this session</div>
""", unsafe_allow_html=True)
        for fb in feedbacks:
            stars = "★" * int(fb["rating"]) + "☆" * (5 - int(fb["rating"]))
            st.markdown(f"""
<div style="background:{card}; border:1px solid {bdr}; border-left:3px solid {warm};
            border-radius:0 8px 8px 0; padding:0.9rem 1.1rem; margin-bottom:0.6rem;">
  <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
    <span style="font-size:0.8rem; font-weight:500; color:{ink};">{fb['name']}</span>
    <span style="color:#c8a050; font-size:0.8rem;">{stars}</span>
  </div>
  <div style="font-size:0.83rem; color:{ink2}; line-height:1.65;">{fb['comment']}</div>
</div>
""", unsafe_allow_html=True)


# ── Router ────────────────────────────────────────────────────────────────────
if selection == "Home":
    render_home()
else:
    mod_num = int(selection.split(".")[0])
    mod = next((m for m in MODULES if m[0] == mod_num), None)
    if mod:
        n, name, subtitle, category, implemented = mod
        if implemented:
            if n == 1:
                from modules import step1; step1.render(n, name, subtitle, category)
            elif n == 2:
                from modules import step2; step2.render(n, name, subtitle, category)
            elif n == 3:
                from modules import step3; step3.render(n, name, subtitle, category)
            elif n == 4:
                from modules import step4; step4.render(n, name, subtitle, category)
            elif n == 5:
                from modules import step5; step5.render(n, name, subtitle, category)
            elif n == 6:
                from modules import step6; step6.render(n, name, subtitle, category)
            elif n == 7:
                from modules import step7; step7.render(n, name, subtitle, category)
            elif n == 8:
                from modules import step8; step8.render(n, name, subtitle, category)
            elif n == 9:
                from modules import step9; step9.render(n, name, subtitle, category)
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
        else:
            style.module_header(category, n, name, subtitle)
            style.coming_soon(n, name)