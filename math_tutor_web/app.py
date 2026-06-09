import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

st.set_page_config(
    page_title="Math Tutor",
    page_icon="∑",
    layout="wide",
    initial_sidebar_state="expanded",
)

import style

# ── Module registry ───────────────────────────────────────────────────────────
# (number, display_name, subtitle, category, implemented)
MODULES = [
    (1,  "Quadratic Equations",       "discriminant · formula · graph",           "Algebra",      True),
    (2,  "Quadratic Inequalities",    "sign analysis · parabola",                 "Algebra",      True),
    (3,  "Systems of Equations",      "substitution · elimination",               "Algebra",      True),
    (4,  "Polynomials",               "Ruffini · factorization",                  "Algebra",      True),
    (5,  "Function Analysis",         "domain · parity · monotonicity",           "Analysis",     True),
    (6,  "Sequences",                 "arithmetic · geometric · limits",          "Analysis",     True),
    (7,  "Limits",                    "at a point · infinity · continuity",       "Analysis",     True),
    (8,  "Trigonometry",              "unit circle · identities · equations",     "Geometry",     True),
    (9,  "Analytic Geometry 2D",      "lines · circles · parabolas",              "Geometry",     True),
    (10, "Logarithms & Exponentials", "properties · equations · models",          "Analysis",     True),
    (11, "Combinatorics",             "factorials · combinations · Pascal",       "Discrete",     True),
    (12, "Probability",               "classical · conditional · Bayes",          "Discrete",     True),
    (13, "Complex Numbers",           "operations · polar · De Moivre",           "Algebra",      True),
    (14, "Euclidean Geometry",        "triangles · circles · polygons",           "Geometry",     True),
    (15, "Number Theory",             "GCD · primes · Fermat · Goldbach",         "Discrete",     True),
    (16, "Financial Math",            "interest · mortgages · inflation",         "Applied",      True),
    (17, "Parametric Equations",      "lines · circles · cycloids",               "Geometry",     True),
    (18, "Analytic Geometry 3D",      "vectors · lines · planes",                 "Geometry",     True),
    (19, "Mathematical Proofs",       "logic · structure · techniques",           "Foundations",  True),
    (20, "Olympic Mathematics",       "method · techniques · problems",           "Foundations",  False),
    (21, "Derivatives",               "rules · chain · applications",             "Analysis",     False),
    (22, "Integrals",                 "Riemann · FTC · techniques · applications","Analysis",     False),
]

CATEGORY_ORDER = ["Algebra", "Analysis", "Geometry", "Discrete", "Applied", "Foundations"]


# ── CSS ───────────────────────────────────────────────────────────────────────
style.inject()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:1.3rem 1.2rem 1rem; border-bottom:1px solid #2e2a25; margin-bottom:0.5rem;">
  <div style="font-family:'Fraunces',serif; font-size:2rem; color:#c8a96e; line-height:1;">∑</div>
  <div style="font-family:'Fraunces',serif; font-size:1.1rem; color:#f0ebe3; margin-top:0.2rem;">Math Tutor</div>
  <div style="font-family:'DM Mono',monospace; font-size:0.56rem; letter-spacing:0.18em;
              text-transform:uppercase; color:#3e3830; margin-top:0.25rem;">
    one language · 22 chapters
  </div>
</div>
""", unsafe_allow_html=True)

    for cat in CATEGORY_ORDER:
        cat_mods = [m for m in MODULES if m[3] == cat]
        if cat_mods:
            st.markdown(
                f'<div style="font-family:\'DM Mono\',monospace; font-size:0.56rem; '
                f'letter-spacing:0.2em; text-transform:uppercase; color:#3e3830; '
                f'padding:0.85rem 1.2rem 0.2rem;">{cat}</div>',
                unsafe_allow_html=True,
            )

    nav_options = ["Home"] + [f"{n:02d}. {name}" for n, name, *_ in MODULES]

    selection = st.radio(
        "",
        nav_options,
        label_visibility="collapsed",
        key="nav",
    )

    st.markdown("""
<div style="padding:1rem 1.2rem; margin-top:1rem; border-top:1px solid #1e1c18;
            font-size:0.72rem; color:#3e3830; line-height:1.7;
            font-family:'DM Mono',monospace;">
  22 chapters · Python + Streamlit<br>
  <span style="font-size:0.63rem;">WHY before HOW. Always.</span>
</div>
""", unsafe_allow_html=True)


# ── Home page ─────────────────────────────────────────────────────────────────
def render_home():
    st.markdown("""
<div style="padding:2.8rem 0 1rem;">
  <div style="font-family:'DM Mono',monospace; font-size:0.62rem; letter-spacing:0.18em;
              text-transform:uppercase; color:#c8a96e; margin-bottom:0.8rem;">
    A complete mathematics curriculum
  </div>
  <h1 style="font-family:'Fraunces',serif; font-size:3.5rem; font-weight:400;
             line-height:1.0; color:#1a1814; margin:0 0 0.5rem;">
    Math<br><em style="color:#e8602a;">Tutor</em>
  </h1>
  <div style="width:50px; height:1px; background:#c8a96e; opacity:0.5; margin:0.9rem 0 1rem;"></div>
  <p style="font-size:0.96rem; font-weight:300; color:#4a4540;
            max-width:500px; line-height:1.7; margin:0 0 0.5rem;">
    Mathematics is one language.<br>
    Not 22 separate topics — 22 chapters of the same story.<br>
    Every concept explained from first principles,
    with <strong style="color:#1a1814; font-weight:500;">intuition before formulas</strong>.
  </p>
</div>
""", unsafe_allow_html=True)

    total = len(MODULES)
    done  = sum(1 for m in MODULES if m[4])
    st.markdown(f"""
<div style="display:flex; gap:0; border:1px solid #e0d8cc; border-radius:10px;
            background:white; overflow:hidden; width:fit-content; margin:1.2rem 0 2.5rem;">
  <div style="padding:0.85rem 1.6rem; border-right:1px solid #e0d8cc;">
    <div style="font-family:'Fraunces',serif; font-size:1.9rem; color:#1a1814; line-height:1;">{total}</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.57rem; letter-spacing:0.14em;
                text-transform:uppercase; color:#4a4540; margin-top:0.15rem;">Chapters</div>
  </div>
  <div style="padding:0.85rem 1.6rem; border-right:1px solid #e0d8cc;">
    <div style="font-family:'Fraunces',serif; font-size:1.9rem; color:#3d6b5e; line-height:1;">{done}</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.57rem; letter-spacing:0.14em;
                text-transform:uppercase; color:#4a4540; margin-top:0.15rem;">Live now</div>
  </div>
  <div style="padding:0.85rem 1.6rem;">
    <div style="font-family:'Fraunces',serif; font-size:1.9rem; color:#1a1814; line-height:1;">∞</div>
    <div style="font-family:'DM Mono',monospace; font-size:0.57rem; letter-spacing:0.14em;
                text-transform:uppercase; color:#4a4540; margin-top:0.15rem;">Patience</div>
  </div>
</div>
""", unsafe_allow_html=True)

    for cat in CATEGORY_ORDER:
        cat_mods = [m for m in MODULES if m[3] == cat]
        if not cat_mods:
            continue

        st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.8rem; margin:2rem 0 0.9rem;">
  <div style="font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.18em;
              text-transform:uppercase; color:#4a4540;">{cat}</div>
  <div style="flex:1; height:1px; background:#e0d8cc;"></div>
</div>
""", unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (n, name, subtitle, _, implemented) in enumerate(cat_mods):
            with cols[i % 3]:
                left_border = "border-left:3px solid #3d6b5e;" if implemented else ""
                st.markdown(f"""
<div style="background:white; border:1px solid #e0d8cc; border-radius:8px;
            padding:0.9rem 1rem; margin-bottom:8px; {left_border}">
  <div style="font-family:'DM Mono',monospace; font-size:0.6rem;
              color:#c8a96e; margin-bottom:0.3rem;">Chapter {n:02d}</div>
  <div style="font-family:'Fraunces',serif; font-size:0.95rem;
              color:#1a1814; line-height:1.25; margin-bottom:0.2rem;">{name}</div>
  <div style="font-size:0.7rem; color:#4a4540; font-style:italic;">{subtitle}</div>
</div>
""", unsafe_allow_html=True)
                if implemented:
                    if st.button("Open →", key=f"home_{n}"):
                        st.session_state["nav"] = f"{n:02d}. {name}"
                        st.rerun()


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
                from modules import step1
                step1.render(n, name, subtitle, category)
            elif n == 2:
                from modules import step2
                step2.render(n, name, subtitle, category)
            elif n == 3:
                from modules import step3
                step3.render(n, name, subtitle, category)
            elif n == 4:
                from modules import step4
                step4.render(n, name, subtitle, category)
            elif n == 5:
                from modules import step5
                step5.render(n, name, subtitle, category)
            elif n == 6:
                from modules import step6
                step6.render(n, name, subtitle, category)
            elif n == 7:
                from modules import step7
                step7.render(n, name, subtitle, category)
            elif n == 8:
                from modules import step8
                step8.render(n, name, subtitle, category)
            elif n == 9:
                from modules import step9
                step9.render(n, name, subtitle, category)
            elif n == 10:
                from modules import step10
                step10.render(n, name, subtitle, category)
            elif n == 11:
                from modules import step11
                step11.render(n, name, subtitle, category)
            elif n == 12:
                from modules import step12
                step12.render(n, name, subtitle, category)
            elif n == 13:
                from modules import step13
                step13.render(n, name, subtitle, category)
            elif n == 14:
                from modules import step14
                step14.render(n, name, subtitle, category)
            elif n == 15:
                from modules import step15
                step15.render(n, name, subtitle, category)
            elif n == 16:
                from modules import step16
                step16.render(n, name, subtitle, category)
            elif n == 17:
                from modules import step17
                step17.render(n, name, subtitle, category)
            elif n == 18:
                from modules import step18
                step18.render(n, name, subtitle, category)
            elif n == 19:
                from modules import step19
                step19.render(n, name, subtitle, category)
            elif n == 20:
                from modules import step20
                step20.render(n, name, subtitle, category)
            elif n == 21:
                from modules import step21
                step21.render(n, name, subtitle, category)
            elif n == 22:
                from modules import step22
                step22.render(n, name, subtitle, category)
            #     from modules import step3
            #     step3.render(n, name, subtitle, category)
        else:
            style.module_header(category, n, name, subtitle)
            style.coming_soon(n, name)