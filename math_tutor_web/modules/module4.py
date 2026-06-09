import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Pure logic ────────────────────────────────────────────────────────────────

def get_divisors(n):
    n = abs(int(n))
    if n == 0:
        return [0]
    divs = []
    for i in range(1, n + 1):
        if n % i == 0:
            divs.append(i)
            divs.append(-i)
    return sorted(set(divs))


def ruffini(coeffs, r):
    """Synthetic division by (x - r). Returns (new_coeffs, remainder, carry_row)."""
    new_coeffs  = [coeffs[0]]
    carry_row   = [0]
    for i in range(1, len(coeffs)):
        carry = new_coeffs[-1] * r
        carry_row.append(carry)
        new_coeffs.append(coeffs[i] + carry)
    remainder  = new_coeffs[-1]
    return new_coeffs[:-1], remainder, carry_row


def solve(coeffs):
    """
    Returns a dict with all steps and results for rendering.
    coeffs: list of floats, highest degree first.
    """
    degree     = len(coeffs) - 1
    candidates = get_divisors(coeffs[-1]) if coeffs[-1] != 0 else list(range(-10, 11))
    steps      = []   # (label, body, variant)
    all_roots  = []

    def add(label, body, variant=""):
        steps.append((label, body, variant))

    p_orig = np.poly1d(coeffs)

    # ── Step 0: overview ─────────────────────────────────────────────────
    poly_str = str(p_orig).replace("\n", " ").strip()
    add("The polynomial",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.2rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  p(x) = {poly_str}
</span><br>
<strong>Degree:</strong> {degree} &nbsp;·&nbsp;
<strong>Constant term:</strong> {coeffs[-1]:g}<br><br>
Plan: use the <strong>Rational Root Theorem</strong> to find candidates,
test each with the <strong>Remainder Theorem</strong>,
and peel off roots one by one using <strong>Ruffini's scheme</strong>
until the degree is small enough to solve directly.""",
        "warm")

    # ── Step 1: candidates ────────────────────────────────────────────────
    add("Step 1 — Find the candidate roots",
        f"""The Rational Root Theorem says: every integer root of this polynomial
must be a divisor of the constant term <strong>{coeffs[-1]:g}</strong>.<br><br>
Instead of guessing, we only need to test a finite list:<br><br>
<code>{candidates}</code><br><br>
That is {len(candidates)} numbers — let's go.""")

    # ── Step 2: test candidates ───────────────────────────────────────────
    current = list(coeffs)
    roots_found = []
    test_lines  = []

    for r in candidates:
        val = round(np.poly1d(current)(r), 10)
        if val == 0:
            test_lines.append(f'<code>p({r:g}) = 0</code> &nbsp;✓ &nbsp;<strong>root found</strong>')
            roots_found.append(r)
        else:
            test_lines.append(f'<code>p({r:g}) = {val:.3g}</code> &nbsp;✗')

    add("Step 2 — Test each candidate",
        "Plug each candidate into the current polynomial. "
        "If p(r) = 0, then (x − r) divides it exactly.<br><br>"
        + "<br>".join(test_lines))

    if not roots_found:
        add("No integer roots",
            "None of the candidates gave p(r) = 0.<br>"
            "The roots of this polynomial are irrational or complex — "
            "numerical methods are needed.",
            "error")
        return {"steps": steps, "all_roots": [], "coeffs": coeffs,
                "ruffini_tables": [], "factored": None}

    # ── Step 3: Ruffini tables ────────────────────────────────────────────
    ruffini_tables = []   # for separate rendering

    for r in roots_found:
        new_c, remainder, carry = ruffini(current, r)

        # build HTML table
        def fmt(v):
            return str(int(v)) if v == int(v) else f"{v:.3g}"

        header_cells = "".join(f"<td><strong>{fmt(v)}</strong></td>" for v in current)
        carry_cells  = "".join(f"<td style='color:var(--sage2);'>{fmt(v)}</td>" for v in carry)
        result_cells = "".join(f"<td><strong>{fmt(v)}</strong></td>" for v in new_c) \
                     + f"<td style='color:var(--warm);'><strong>{fmt(remainder)}</strong></td>"

        table_html = f"""
<table style="border-collapse:collapse;font-family:'DM Mono',monospace;
              font-size:0.82rem;margin:0.6rem 0;">
  <tr style="border-bottom:1px solid var(--border);">
    <td style="padding:0.3rem 0.7rem;color:var(--warm);"><strong>{fmt(r)}</strong></td>
    {header_cells}
  </tr>
  <tr style="color:var(--sage2);">
    <td></td>{carry_cells}
  </tr>
  <tr style="border-top:1px solid var(--border);">
    <td></td>{result_cells}
  </tr>
</table>
<div style="font-size:0.8rem;color:var(--ink2);margin-top:0.3rem;">
  Remainder = <strong style="color:{'var(--sage)' if abs(remainder)<1e-9 else 'var(--warm)'};">
  {fmt(remainder)}</strong>
  {'✓ — clean division confirmed.' if abs(remainder)<1e-9 else '— unexpected remainder.'}
  {'Polynomial reduced to degree ' + str(len(new_c)-1) + '.' if abs(remainder)<1e-9 else ''}
</div>"""

        ruffini_tables.append((r, table_html))

        add(f"Step 3 — Ruffini's scheme for root x = {fmt(r)}",
            f"""Dividing by <span class="mf">(x − {fmt(r)})</span>:<br>
Each step: multiply the running value by {fmt(r)}, add to the next coefficient.
The last number is the remainder — must be 0 to confirm the root.<br>
{table_html}
New coefficients: <code>{[fmt(v) for v in new_c]}</code>""")

        all_roots.append(r)
        current = new_c

    # ── Step 4: solve the reduced polynomial ─────────────────────────────
    deg_remaining = len(current) - 1

    if deg_remaining == 1:
        a, b   = current
        x_lin  = -b / a
        all_roots.append(x_lin)
        add("Step 4 — Solve the linear remainder",
            f"Reduced to: <span class='mf'>{fmt(a)}x + {fmt(b)} = 0</span><br><br>"
            f"x = −{fmt(b)} / {fmt(a)} = <strong>{x_lin:.4f}</strong>",
            "sage")

    elif deg_remaining == 2:
        a, b, c = current
        delta   = b**2 - 4*a*c
        if delta > 0:
            sq    = math.sqrt(delta)
            x1    = (-b + sq) / (2*a)
            x2    = (-b - sq) / (2*a)
            all_roots.extend([x1, x2])
            add("Step 4 — Solve the quadratic remainder",
                f"Reduced to: <span class='mf'>{fmt(a)}x² + {fmt(b)}x + {fmt(c)} = 0</span><br><br>"
                f"Δ = {delta:.4f} &gt; 0 → two more roots:<br>"
                f"x₁ = <strong>{x1:.4f}</strong> &nbsp;·&nbsp; x₂ = <strong>{x2:.4f}</strong>",
                "sage")
        elif delta == 0:
            x_d = -b / (2*a)
            all_roots.append(x_d)
            add("Step 4 — Solve the quadratic remainder",
                f"Reduced to: <span class='mf'>{fmt(a)}x² + {fmt(b)}x + {fmt(c)} = 0</span><br><br>"
                f"Δ = 0 → one repeated root: x = <strong>{x_d:.4f}</strong>",
                "sage")
        else:
            add("Step 4 — Quadratic remainder has no real roots",
                f"Reduced to: <span class='mf'>{fmt(a)}x² + {fmt(b)}x + {fmt(c)} = 0</span><br><br>"
                f"Δ = {delta:.4f} &lt; 0 → no further real roots. "
                "The remaining two roots are complex.",
                "error")

    elif deg_remaining == 0:
        add("Step 4 — Fully factored",
            "The polynomial has been completely factored — no remainder polynomial left.",
            "sage")

    # ── Factored form ─────────────────────────────────────────────────────
    def fmt(v):
        return str(int(v)) if v == int(v) else f"{v:.4f}"

    leading  = fmt(coeffs[0])
    factors  = " · ".join(f"(x − {fmt(round(r,4))})" for r in all_roots)
    factored = f"p(x) = {leading} · {factors}"

    return {"steps": steps, "all_roots": all_roots, "coeffs": coeffs,
            "ruffini_tables": ruffini_tables, "factored": factored}


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(coeffs, roots):
    p = np.poly1d(coeffs)
    if roots:
        center = sum(roots) / len(roots)
        spread = max(max(roots) - min(roots), 2) * 2
    else:
        center, spread = 0, 6

    x = np.linspace(center - spread, center + spread, 500)
    y = p(x)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    ax.plot(x, y, color="#e8602a", linewidth=2.2, label="p(x)")
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)

    for r in roots:
        ax.plot(r, 0, "o", color="#c8a96e", markersize=9, zorder=5)
        ax.annotate(f"x={r:.2f}", (r, 0),
                    textcoords="offset points", xytext=(0, 13),
                    ha="center", fontsize=9, fontfamily="serif", color="#4a4540")

    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.set_xlabel("x",    color="#4a4540", fontsize=9)
    ax.set_ylabel("p(x)", color="#4a4540", fontsize=9)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    # keep y-axis readable
    finite = y[np.isfinite(y)]
    if len(finite):
        lo, hi = np.percentile(finite, 2), np.percentile(finite, 98)
        ax.set_ylim(lo - abs(hi-lo)*0.1, hi + abs(hi-lo)*0.1)
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render_steps(r):
    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    if not r["all_roots"]:
        return

    # result band
    roots_str = "  ·  ".join(
        str(int(x)) if x == int(x) else f"{x:.4f}"
        for x in r["all_roots"]
    )
    style.result_band(
        ("Real roots",    roots_str),
        ("Degree",        str(len(r["coeffs"]) - 1)),
        ("Factored form", r["factored"] or "—"),
    )

    # verify
    p_orig = np.poly1d(r["coeffs"])
    pills  = [
        f"p({x:.3g}) = {p_orig(x):.2e} ✓"
        for x in r["all_roots"]
    ]
    style.step("Verify — substitute each root back",
               "p(r) must equal zero for every root found.",
               "sage")
    style.pills(*pills)

    # graph
    st.markdown('<div class="graph-label">The polynomial and its roots</div>',
                unsafe_allow_html=True)
    fig = make_plot(r["coeffs"], r["all_roots"])
    st.pyplot(fig)
    plt.close(fig)

    style.step(
        "Reading the graph",
        "Each gold dot is a root — a point where p(x) crosses (or touches) the x-axis.<br>"
        "A root where the curve crosses is a <strong>simple root</strong>. "
        "A root where it only touches is a <strong>repeated root</strong> (even multiplicity).",
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Enter coefficients (highest degree first)</div>',
                    unsafe_allow_html=True)

        degree = st.selectbox("Degree", [2, 3, 4, 5], index=1, key="p_deg")

        coeffs = []
        for i in range(degree, -1, -1):
            label = f"x^{i}" if i > 1 else ("x" if i == 1 else "constant")
            val   = {3: [1,-6,11,-6], 2: [1,-3,2], 4: [1,-5,5,5,-6],
                     5: [1,-3,-5,15,4,-12]}.get(degree, [1]+[0]*degree)
            default = val[degree - i] if degree - i < len(val) else 0.0
            c = st.number_input(f"Coefficient of {label}",
                                value=float(default),
                                step=1.0, format="%.4g",
                                key=f"p_c{i}")
            coeffs.append(c)

        # live preview
        p_preview = np.poly1d(coeffs)
        st.markdown(
            f'<div class="eq-display" style="font-size:1rem;">'
            f'p(x) = {str(p_preview).replace(chr(10)," ").strip()}'
            f'</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Solve →", key="p_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Degree 3: <code>1, −6, 11, −6</code><br>
    roots: 1, 2, 3<br><br>
    Degree 3: <code>1, −3, 2, 0</code><br>
    roots: 0, 1, 2<br><br>
    Degree 4: <code>1, −5, 5, 5, −6</code><br>
    roots: −1, 1, 2, 3
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if coeffs[0] == 0:
                st.error("The leading coefficient cannot be zero.")
            else:
                render_steps(solve(coeffs))
        else:
            style.empty_state("p(x)")