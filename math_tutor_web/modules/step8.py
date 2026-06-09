import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

x = sp.Symbol('x')
y = sp.Symbol('y')


# ── Pure logic ────────────────────────────────────────────────────────────────

NOTABLE_ANGLES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
SIN_EXACT = {0:"0", 30:"1/2", 45:"√2/2", 60:"√3/2", 90:"1",
             120:"√3/2", 135:"√2/2", 150:"1/2", 180:"0", 270:"−1", 360:"0"}
COS_EXACT = {0:"1", 30:"√3/2", 45:"√2/2", 60:"1/2", 90:"0",
             120:"−1/2", 135:"−√2/2", 150:"−√3/2", 180:"−1", 270:"0", 360:"1"}
TAN_EXACT = {0:"0", 30:"√3/3", 45:"1", 60:"√3", 90:"∞",
             120:"−√3", 135:"−1", 150:"−√3/3", 180:"0", 270:"∞", 360:"0"}

IDENTITIES = [
    ("Pythagorean Identity",
     "sin²(x) + cos²(x) = 1",
     "The Pythagorean theorem on the unit circle. "
     "The point (cos x, sin x) is always at distance 1 from the origin.<br>"
     "This single identity is the seed from which all of trigonometry grows."),
    ("Sine Addition",
     "sin(x+y) = sin(x)cos(y) + cos(x)sin(y)",
     "When you sum two angles, the sine mixes both functions.<br>"
     "Setting y = x immediately gives the double-angle formula."),
    ("Cosine Addition",
     "cos(x+y) = cos(x)cos(y) − sin(x)sin(y)",
     "Notice the minus sign — that is the key difference from sine.<br>"
     "cos(x+y) is NOT cos(x) + cos(y). This trips up almost everyone."),
    ("Double Angle — Sine",
     "sin(2x) = 2·sin(x)·cos(x)",
     "The addition formula with y = x.<br>"
     "Appears constantly in integration — turns a product into one function."),
    ("Double Angle — Cosine",
     "cos(2x) = cos²(x) − sin²(x) = 2cos²(x)−1 = 1−2sin²(x)",
     "Three equivalent forms — all correct. Which you use depends on what you need to simplify."),
    ("Tangent",
     "tan(x) = sin(x) / cos(x)",
     "Geometrically: the slope of the radius to (cos x, sin x).<br>"
     "Undefined wherever cos(x) = 0 — those are the vertical asymptotes."),
]


def solve_trig_eq(func, k):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    add("The equation",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.3rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  {func}(x) = {k:g}
</span><br>
Trig equations always have <strong>infinitely many solutions</strong>
because sin, cos, and tan are periodic.<br>
Strategy: find the reference angle, use symmetry for all solutions in [0, 2π],
then add multiples of the period.""",
        "warm")

    if func in ["sin", "cos"] and abs(k) > 1:
        add("No solution",
            f"{func}(x) is always between −1 and 1. "
            f"k = {k:g} is outside this range — no angle can give it.",
            "error")
        return {"steps": steps, "solutions": [], "func": func, "k": k}

    solutions = []

    if func == "sin":
        x0 = math.asin(k)
        add("Step 1 — Reference angle",
            f"x₀ = arcsin({k:g}) = <strong>{x0:.4f} rad</strong> = {math.degrees(x0):.2f}°<br><br>"
            f"This is the angle in [−π/2, π/2] whose sine equals {k:g}.")
        x1 = x0 if x0 >= 0 else x0 + 2*math.pi
        x2 = math.pi - x0 if math.pi - x0 >= 0 else math.pi - x0 + 2*math.pi
        add("Step 2 — Symmetry in [0, 2π]",
            f"sin is symmetric about x = π/2:<br>"
            f"x₁ = {x1:.4f} rad = {math.degrees(x1):.2f}°<br>"
            f"x₂ = π − {x0:.4f} = {x2:.4f} rad = {math.degrees(x2):.2f}°")
        add("Step 3 — General solution",
            f"<span class='mf'>x = {x1:.4f} + 2kπ &nbsp;(k ∈ ℤ)</span><br>"
            f"<span class='mf'>x = {x2:.4f} + 2kπ &nbsp;(k ∈ ℤ)</span><br><br>"
            f"Verify: sin({x1:.4f}) = {math.sin(x1):.6f} ✓ &nbsp;·&nbsp; "
            f"sin({x2:.4f}) = {math.sin(x2):.6f} ✓",
            "sage")
        solutions = [x1, x2]

    elif func == "cos":
        x0 = math.acos(k)
        x2 = 2*math.pi - x0
        add("Step 1 — Reference angle",
            f"x₀ = arccos({k:g}) = <strong>{x0:.4f} rad</strong> = {math.degrees(x0):.2f}°<br><br>"
            f"This is the angle in [0, π] whose cosine equals {k:g}.")
        add("Step 2 — Symmetry in [0, 2π]",
            f"cos is symmetric about x = 0 (y-axis):<br>"
            f"x₁ = {x0:.4f} rad = {math.degrees(x0):.2f}°<br>"
            f"x₂ = 2π − {x0:.4f} = {x2:.4f} rad = {math.degrees(x2):.2f}°")
        add("Step 3 — General solution",
            f"<span class='mf'>x = ±{x0:.4f} + 2kπ &nbsp;(k ∈ ℤ)</span><br><br>"
            f"Verify: cos({x0:.4f}) = {math.cos(x0):.6f} ✓ &nbsp;·&nbsp; "
            f"cos({x2:.4f}) = {math.cos(x2):.6f} ✓",
            "sage")
        solutions = [x0, x2]

    else:  # tan
        x0 = math.atan(k)
        add("Step 1 — Reference angle",
            f"x₀ = arctan({k:g}) = <strong>{x0:.4f} rad</strong> = {math.degrees(x0):.2f}°<br><br>"
            f"tan has no restricted range — there is always a solution.")
        add("Step 2 — General solution",
            f"tan repeats every <strong>π</strong> (half the period of sin/cos):<br><br>"
            f"<span class='mf'>x = {x0:.4f} + kπ &nbsp;(k ∈ ℤ)</span><br><br>"
            f"Verify: tan({x0:.4f}) = {math.tan(x0):.6f} ✓",
            "sage")
        solutions = [x0]

    return {"steps": steps, "solutions": solutions, "func": func, "k": k}


# ── Plots ─────────────────────────────────────────────────────────────────────

def make_unit_circle(angle_deg):
    angle_rad = math.radians(angle_deg)
    cv, sv = math.cos(angle_rad), math.sin(angle_rad)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="#1a1814", linewidth=1.5)
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)

    ax.plot([0, cv], [0, sv], color="#3d6b5e", linewidth=2.2,
            label=f"θ = {angle_deg}°")
    ax.plot(cv, sv, "o", color="#c8a96e", markersize=10, zorder=5)
    ax.annotate(f"  ({cv:.3f}, {sv:.3f})", (cv, sv), fontsize=9,
                color="#4a4540", fontfamily="serif")
    ax.plot([0, cv], [0, 0], color="#e8602a", linewidth=2,
            linestyle="--", label=f"cos = {cv:.4f}")
    ax.plot([cv, cv], [0, sv], color="#7b6fb0", linewidth=2,
            linestyle="--", label=f"sin = {sv:.4f}")

    for a_deg in [0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330]:
        r = math.radians(a_deg)
        ax.plot(math.cos(r), math.sin(r), ".", color="#b0a090", markersize=5)
        ax.annotate(f"{a_deg}°",
                    (math.cos(r)*1.15, math.sin(r)*1.15),
                    ha="center", va="center", fontsize=7, color="#9e9080")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.spines[["top","right","bottom","left"]].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc", loc="upper right")
    ax.grid(True, alpha=0.15, color="#e0d8cc")
    plt.tight_layout()
    return fig


def make_trig_graphs():
    x_vals = np.linspace(-2*np.pi, 2*np.pi, 1000)
    tan_v  = np.tan(x_vals)
    tan_v[np.abs(tan_v) > 10] = np.nan

    fig, axes = plt.subplots(3, 1, figsize=(8, 9))
    fig.patch.set_facecolor("#fdfaf5")

    configs = [
        (np.sin(x_vals), "#e8602a", "sin(x) — period 2π, amplitude 1"),
        (np.cos(x_vals), "#3d6b5e", "cos(x) — period 2π, amplitude 1"),
        (tan_v,          "#7b6fb0", "tan(x) — period π, asymptotes at π/2 + kπ"),
    ]
    ylims = [(-1.5,1.5), (-1.5,1.5), (-5,5)]

    for ax, (y_v, col, title), ylim in zip(axes, configs, ylims):
        ax.set_facecolor("#fdfaf5")
        ax.plot(x_vals, y_v, color=col, linewidth=2.2)
        ax.axhline(0, color="#1a1814", linewidth=0.6)
        ax.set_ylim(*ylim)
        ax.set_title(title, fontsize=10, color="#4a4540", pad=6)
        ticks  = [-2*np.pi, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 2*np.pi]
        labels = ["-2π", "-π", "-π/2", "0", "π/2", "π", "2π"]
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, fontsize=8)
        ax.spines[["top","right"]].set_visible(False)
        ax.spines["bottom"].set_color("#e0d8cc")
        ax.spines["left"].set_color("#e0d8cc")
        ax.tick_params(colors="#4a4540", labelsize=8)
        ax.grid(True, alpha=0.2, color="#e0d8cc")

    plt.tight_layout()
    return fig


def make_eq_plot(func, k, solutions):
    x_vals = np.linspace(-2*np.pi, 2*np.pi, 1000)
    if func == "sin":
        y_vals = np.sin(x_vals); col = "#e8602a"
    elif func == "cos":
        y_vals = np.cos(x_vals); col = "#3d6b5e"
    else:
        y_vals = np.tan(x_vals)
        y_vals[np.abs(y_vals) > 10] = np.nan
        col = "#7b6fb0"

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")
    ax.plot(x_vals, y_vals, color=col, linewidth=2.2, label=f"{func}(x)")
    ax.axhline(k, color="#1a1814", linewidth=1.5, linestyle="--", label=f"y = {k:g}")

    for s in solutions:
        ax.plot(s, k, "o", color="#c8a96e", markersize=10, zorder=5)
        ax.annotate(f"{s:.2f}", (s, k),
                    textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=8.5, fontfamily="serif", color="#4a4540")

    ax.set_ylim(-3,3) if func != "tan" else ax.set_ylim(-5,5)
    ticks  = [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi]
    labels = ["-2π", "-π", "0", "π", "2π"]
    ax.set_xticks(ticks); ax.set_xticklabels(labels)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.set_xlabel("x (radians)", color="#4a4540", fontsize=9)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render_unit_circle(angle_deg):
    rad = math.radians(angle_deg)
    cv, sv = math.cos(rad), math.sin(rad)
    tv = math.tan(rad) if abs(math.cos(rad)) > 1e-9 else None

    style.step("The unit circle",
        f"""A circle of radius 1 centred at the origin.<br>
Every angle θ corresponds to a unique point <strong>(cos θ, sin θ)</strong> on it.<br><br>
For θ = <strong>{angle_deg}°</strong>:<br>
cos({angle_deg}°) = <strong>{cv:.6f}</strong><br>
sin({angle_deg}°) = <strong>{sv:.6f}</strong><br>
tan({angle_deg}°) = <strong>{"∞" if tv is None else f"{tv:.6f}"}</strong>""",
        "warm")

    style.result_band(
        ("θ",   f"{angle_deg}°  =  {math.radians(angle_deg):.4f} rad"),
        ("cos", f"{cv:.6f}"),
        ("sin", f"{sv:.6f}"),
        ("tan", "∞" if tv is None else f"{tv:.6f}"),
    )
    st.markdown('<div class="graph-label">Unit circle</div>', unsafe_allow_html=True)
    fig = make_unit_circle(angle_deg)
    st.pyplot(fig); plt.close(fig)


def render_notable():
    style.step("Where do notable values come from?",
        """Two simple triangles generate every value in the table.<br><br>
<strong>45-45-90 triangle:</strong> cut a unit square diagonally.<br>
Diagonal = √2. Divide by √2 → sin(45°) = cos(45°) = √2/2.<br><br>
<strong>30-60-90 triangle:</strong> cut an equilateral triangle in half.<br>
sin(30°) = 1/2 &nbsp;·&nbsp; cos(30°) = √3/2 &nbsp;·&nbsp;
sin(60°) = √3/2 &nbsp;·&nbsp; cos(60°) = 1/2.<br><br>
Everything else follows from <strong>symmetry</strong> on the unit circle.""",
        "warm")

    rows = ""
    for deg in NOTABLE_ANGLES:
        rows += (f"<tr><td style='padding:0.3rem 0.8rem;font-family:\"DM Mono\",monospace;"
                 f"font-size:0.8rem;'>{deg}°</td>"
                 f"<td style='padding:0.3rem 0.8rem;'>{SIN_EXACT[deg]}</td>"
                 f"<td style='padding:0.3rem 0.8rem;'>{COS_EXACT[deg]}</td>"
                 f"<td style='padding:0.3rem 0.8rem;'>{TAN_EXACT[deg]}</td></tr>")

    style.step("Notable values table",
        f"""<table style="border-collapse:collapse;font-size:0.85rem;width:100%;">
<thead><tr style="border-bottom:1px solid var(--border);font-family:'DM Mono',monospace;
font-size:0.65rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--sand);">
<td style="padding:0.3rem 0.8rem;">Angle</td>
<td style="padding:0.3rem 0.8rem;">sin</td>
<td style="padding:0.3rem 0.8rem;">cos</td>
<td style="padding:0.3rem 0.8rem;">tan</td></tr></thead>
<tbody>{rows}</tbody></table>""")

    style.step("Patterns to notice",
        """· sin and cos are always between −1 and 1<br>
· sin(x) = cos(90° − x) — they are complementary<br>
· tan = 1 exactly at 45° — the slope of a 45° line<br>
· wherever cos = 0, tan is undefined (vertical asymptote)<br><br>
<em>Historical note:</em> the word 'sine' comes from a mistranslation of the Arabic 'jayb'
(meaning pocket), itself a translation of the Sanskrit word for half-chord.
Mathematics traveled from India to Arabia to Europe — and the name got garbled along the way.</em>""")


def render_identities():
    style.step("What is an identity?",
        "An identity is true for <strong>every</strong> value of x — always, not just sometimes.<br>"
        "These are the tools you reach for when an expression looks complicated.<br>"
        "The single most important one is the Pythagorean identity — everything else follows from it.",
        "warm")

    for name, formula, explanation in IDENTITIES:
        style.step(name,
            f"<span class='mf' style='font-size:1.05rem;'>{formula}</span><br><br>{explanation}")

    style.step("Two powerful habits",
        "Whenever you see sin² or cos² → think <strong>Pythagorean identity</strong>.<br>"
        "Whenever you see a double angle → think <strong>addition formula with y = x</strong>.<br>"
        "These two moves unlock most trigonometric problems.")


def render_equations(r):
    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    if r["solutions"]:
        style.result_band(
            ("Function", f"{r['func']}(x) = {r['k']:g}"),
            ("Solutions in [0,2π]", "  ·  ".join(f"{s:.4f}" for s in r["solutions"])),
        )
        st.markdown('<div class="graph-label">Graph and solutions</div>',
                    unsafe_allow_html=True)
        fig = make_eq_plot(r["func"], r["k"], r["solutions"])
        st.pyplot(fig); plt.close(fig)


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>',
                    unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Unit circle", "Notable values", "Identities", "Equations"],
            key="trig_topic")

        if topic == "Unit circle":
            angle = st.number_input("Angle (degrees)", value=45.0,
                                    step=15.0, format="%.4g", key="trig_angle")
            preview = f"θ = {angle:g}°"

        elif topic == "Equations":
            func = st.selectbox("Function", ["sin", "cos", "tan"], key="trig_func")
            k    = st.number_input("k", value=0.5, step=0.1,
                                   format="%.4g", key="trig_k")
            preview = f"{func}(x) = {k:g}"

        else:
            preview = topic

        st.markdown(
            f'<div class="eq-display" style="font-size:1rem;">{preview}</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Explore →", key="trig_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Unit circle: <code>0, 30, 45, 60, 90, 180</code><br>
    Equation sin: <code>k = 0.5</code> → 30° and 150°<br>
    Equation cos: <code>k = 0</code> → 90° and 270°<br>
    Equation tan: <code>k = 1</code> → 45°
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Unit circle":
                render_unit_circle(angle)
            elif topic == "Notable values":
                render_notable()
            elif topic == "Identities":
                render_identities()
            else:
                render_equations(solve_trig_eq(func, k))
        else:
            style.empty_state("sin cos tan")