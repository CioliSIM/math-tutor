import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit as st

import style

n_sym = sp.Symbol('n', positive=True, integer=True)


# ── Pure logic ────────────────────────────────────────────────────────────────

def compute_limit(expr_sym):
    try:
        return sp.limit(expr_sym, n_sym, sp.oo)
    except Exception:
        return None


def solve_arithmetic(a, d, n_terms):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    terms = [a + (i - 1) * d for i in range(1, n_terms + 1)]

    rows = "<br>".join(
        f"a({i}) = {a:g} + ({i}−1)·{d:g} = <strong>{terms[i-1]:g}</strong>"
        for i in range(1, min(n_terms + 1, 8))
    )
    if n_terms > 7:
        rows += f"<br><em>… up to a({n_terms}) = {terms[-1]:g}</em>"

    add("Build the sequence",
        f"""<span class="mf">a(n) = a + (n−1)·d = {a:g} + (n−1)·{d:g}</span><br><br>
{rows}""")

    S = n_terms / 2 * (terms[0] + terms[-1])
    add("Sum of the first terms — Gauss's trick",
        f"""Gauss noticed that pairing the first term with the last,
the second with the second-to-last, always gives the same sum.<br><br>
First + Last = {terms[0]:g} + {terms[-1]:g} = <strong>{terms[0]+terms[-1]:g}</strong><br>
There are {n_terms}/2 such pairs, so:<br><br>
<span class="mf">S({n_terms}) = {n_terms}/2 · ({terms[0]:g} + {terms[-1]:g}) = <strong>{S:g}</strong></span>""")

    a_s = sp.Rational(a).limit_denominator(1000)
    d_s = sp.Rational(d).limit_denominator(1000)
    lim = compute_limit(a_s + (n_sym - 1) * d_s)

    if lim == sp.oo:
        lim_body = f"d = {d:g} &gt; 0 → the sequence climbs forever. <strong>lim = +∞</strong> (diverges)"
    elif lim == -sp.oo:
        lim_body = f"d = {d:g} &lt; 0 → the sequence descends forever. <strong>lim = −∞</strong> (diverges)"
    else:
        lim_body = f"d = 0 → every term equals {a:g}. <strong>lim = {lim}</strong> (converges)"

    add("Limit as n → ∞", lim_body)

    return {"steps": steps, "terms": terms, "S": S, "kind": "arithmetic",
            "title": f"Arithmetic  (a={a:g}, d={d:g})"}


def solve_geometric(a, r, n_terms):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    terms = [a * r**(i - 1) for i in range(1, n_terms + 1)]

    rows = "<br>".join(
        f"a({i}) = {a:g}·{r:g}^{i-1} = <strong>{terms[i-1]:.4g}</strong>"
        for i in range(1, min(n_terms + 1, 8))
    )
    if n_terms > 7:
        rows += f"<br><em>… up to a({n_terms}) = {terms[-1]:.4g}</em>"

    add("Build the sequence",
        f"""<span class="mf">a(n) = a · r^(n−1) = {a:g} · {r:g}^(n−1)</span><br><br>
{rows}""")

    if r == 1:
        S = a * n_terms
        sum_body = f"r = 1 → every term = {a:g}. &nbsp;S({n_terms}) = {a:g} · {n_terms} = <strong>{S:g}</strong>"
    else:
        S = a * (1 - r**n_terms) / (1 - r)
        sum_body = (f"<span class='mf'>S(n) = a·(1 − r^n) / (1 − r)</span><br><br>"
                    f"S({n_terms}) = {a:g}·(1 − {r:g}^{n_terms}) / (1 − {r:g})"
                    f" = <strong>{S:.6g}</strong>")
    add("Sum of the first terms", sum_body)

    a_s = sp.Rational(a).limit_denominator(1000)
    r_s = sp.Rational(r).limit_denominator(1000)
    lim = compute_limit(a_s * r_s**(n_sym - 1))

    if abs(r) < 1:
        lim_body = (f"|r| = {abs(r):g} &lt; 1 → r^n shrinks to 0.<br>"
                    f"<strong>lim = 0</strong> (converges)"
                    + ("<br>Since r &lt; 0, terms alternate in sign while shrinking." if r < 0 else ""))
    elif abs(r) > 1:
        lim_body = f"|r| = {abs(r):g} &gt; 1 → r^n explodes. <strong>lim = ±∞</strong> (diverges)"
    elif r == 1:
        lim_body = f"r = 1 → every term = {a:g}. <strong>lim = {a:g}</strong> (converges)"
    else:
        lim_body = "r = −1 → terms oscillate between +1 and −1 forever. <strong>No limit.</strong>"

    add("Limit as n → ∞", lim_body)

    return {"steps": steps, "terms": terms, "S": S, "kind": "geometric",
            "title": f"Geometric  (a={a:g}, r={r:g})"}


def solve_fibonacci(n_terms):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    terms = [1, 1]
    for i in range(2, n_terms):
        terms.append(terms[-1] + terms[-2])
    terms = terms[:n_terms]

    rows = "<br>".join(
        f"a({i+1}) = a({i}) + a({i-1}) = {terms[i-1]} + {terms[i-2]} = <strong>{terms[i]}</strong>"
        for i in range(2, min(n_terms, 8))
    )
    add("Build the sequence",
        f"""Rule: <span class="mf">a(n) = a(n−1) + a(n−2)</span><br>
Base: a(1) = 1, a(2) = 1<br><br>
{rows}{"<br><em>…</em>" if n_terms > 8 else ""}""")

    phi = (1 + math.sqrt(5)) / 2
    ratio_rows = "<br>".join(
        f"a({i+1})/a({i}) = {terms[i]}/{terms[i-1]} = <strong>{terms[i]/terms[i-1]:.8f}</strong>"
        f"  &nbsp;(distance from φ: {abs(terms[i]/terms[i-1]-phi):.2e})"
        for i in range(max(0, n_terms-5), n_terms-1)
    )
    add("The golden ratio emerges",
        f"""The terms grow without bound: lim a(n) = +∞.<br><br>
But the <strong>ratio</strong> a(n+1)/a(n) converges to something remarkable:<br><br>
{ratio_rows}<br><br>
<span class="mf">lim a(n+1)/a(n) = φ = (1+√5)/2 ≈ {phi:.10f}</span><br><br>
The golden ratio — found in sunflowers, shells, and art.
Fibonacci leads straight to it.""",
        "sage")

    return {"steps": steps, "terms": terms, "kind": "fibonacci",
            "title": "Fibonacci Sequence"}


def solve_recursive(a1, k, c, n_terms):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    terms = [a1]
    for _ in range(1, n_terms):
        terms.append(terms[-1] * k + c)

    rows = "<br>".join(
        f"a({i+1}) = {terms[i-1]:.4g}·{k:g} + {c:g} = <strong>{terms[i]:.4g}</strong>"
        for i in range(1, min(n_terms, 7))
    )
    add("Build the sequence",
        f"""Rule: <span class="mf">a(n) = a(n−1)·{k:g} + {c:g}</span><br>
Base: a(1) = {a1:g}<br><br>
{rows}{"<br><em>…</em>" if n_terms > 7 else ""}""")

    if k == 1:
        lim_body = (f"k = 1 → this is arithmetic with d = {c:g}.<br>"
                    + ("lim = +∞" if c > 0 else "lim = −∞" if c < 0 else f"lim = {a1:g}"))
    elif k == -1:
        lim_body = "k = −1 → oscillates between two values. <strong>No limit.</strong>"
    else:
        k_s  = sp.Rational(k).limit_denominator(1000)
        c_s  = sp.Rational(c).limit_denominator(1000)
        a1_s = sp.Rational(a1).limit_denominator(1000)
        closed = k_s**(n_sym-1)*a1_s + c_s*(1-k_s**(n_sym-1))/(1-k_s)
        lim    = compute_limit(closed)

        if lim is not None and lim not in [sp.oo, -sp.oo]:
            L = float(lim)
            lim_body = (f"|k| = {abs(k):g} &lt; 1 → converges.<br><br>"
                        f"Fixed point: L = c/(1−k) = {c:g}/(1−{k:g}) = <strong>{L:.6f}</strong><br>"
                        f"Last three terms: {[f'{t:.6f}' for t in terms[-3:]]}")
        else:
            lim_body = f"|k| = {abs(k):g} &gt; 1 → <strong>diverges</strong> (terms escape to infinity)."

    add("Limit — fixed point method",
        f"""If the sequence converges to L, then at the limit it stops changing:<br><br>
<span class="mf">L = L·k + c &nbsp;→ &nbsp;L·(1−k) = c &nbsp;→ &nbsp;L = c/(1−k)</span><br><br>
This only works if |k| &lt; 1. If |k| ≥ 1, the sequence escapes.<br><br>
{lim_body}""")

    return {"steps": steps, "terms": terms, "kind": "recursive",
            "title": f"Recursive  (k={k:g}, c={c:g})"}


# ── Plot ──────────────────────────────────────────────────────────────────────

def make_plot(terms, title):
    n_vals = list(range(1, len(terms) + 1))

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")

    markerline, stemlines, baseline = ax.stem(
        n_vals, terms, linefmt="#e8602a", markerfmt="o", basefmt="#1a1814"
    )
    plt.setp(markerline, color="#c8a96e", markersize=7, zorder=5)
    plt.setp(stemlines, linewidth=1.2)

    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.set_xlabel("n  (position)", color="#4a4540", fontsize=9)
    ax.set_ylabel("a(n)  (value)", color="#4a4540", fontsize=9)
    ax.set_title(title, fontsize=10, color="#4a4540", pad=8)
    ax.grid(True, alpha=0.2, color="#e0d8cc")
    plt.tight_layout()
    return fig


# ── Render ────────────────────────────────────────────────────────────────────

def render_steps(r):
    for label, body, variant in r["steps"]:
        style.step(label, body, variant)

    style.result_band(
        ("Type",   r["kind"].capitalize()),
        ("Terms",  str(len(r["terms"]))),
        ("First",  f"{r['terms'][0]:.4g}"),
        ("Last",   f"{r['terms'][-1]:.4g}"),
    )

    st.markdown('<div class="graph-label">Sequence plot</div>',
                unsafe_allow_html=True)
    fig = make_plot(r["terms"], r["title"])
    st.pyplot(fig)
    plt.close(fig)

    style.step(
        "Reading the graph",
        "Each vertical bar represents one term. "
        "The height is the value, the position on the x-axis is the index n.<br>"
        "Convergence looks like the bars settling toward a horizontal level. "
        "Divergence looks like the bars escaping upward or downward.",
    )


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose sequence type</div>',
                    unsafe_allow_html=True)

        seq_type = st.selectbox("Type", ["Arithmetic", "Geometric",
                                          "Fibonacci", "Recursive"],
                                key="seq_type")

        n_terms = st.number_input("Number of terms", value=10,
                                  min_value=3, max_value=40,
                                  step=1, key="seq_n")

        if seq_type == "Arithmetic":
            a = st.number_input("First term a", value=2.0,
                                step=1.0, format="%.4g", key="seq_a")
            d = st.number_input("Common difference d", value=3.0,
                                step=1.0, format="%.4g", key="seq_d")
            preview = f"a(n) = {a:g} + (n−1)·{d:g}"

        elif seq_type == "Geometric":
            a = st.number_input("First term a", value=2.0,
                                step=1.0, format="%.4g", key="seq_ga")
            r = st.number_input("Common ratio r", value=0.5,
                                step=0.1, format="%.4g", key="seq_r")
            preview = f"a(n) = {a:g} · {r:g}^(n−1)"

        elif seq_type == "Fibonacci":
            preview = "a(n) = a(n−1) + a(n−2), a(1)=a(2)=1"

        else:  # Recursive
            a1 = st.number_input("First term a(1)", value=10.0,
                                 step=1.0, format="%.4g", key="seq_ra1")
            k  = st.number_input("Multiplier k", value=0.5,
                                 step=0.1, format="%.4g", key="seq_k")
            c  = st.number_input("Constant c", value=1.0,
                                 step=0.5, format="%.4g", key="seq_c")
            preview = f"a(n) = a(n−1)·{k:g} + {c:g}"

        st.markdown(
            f'<div class="eq-display" style="font-size:1rem;">{preview}</div>',
            unsafe_allow_html=True,
        )

        solve_btn = st.button("Analyze →", key="seq_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Arithmetic <code>a=1, d=1</code> → natural numbers<br>
    Geometric &nbsp;<code>a=1, r=0.5</code> → converges to 0<br>
    Geometric &nbsp;<code>a=1, r=2</code> → diverges<br>
    Fibonacci &nbsp;→ watch the golden ratio emerge<br>
    Recursive <code>k=0.5, c=1</code> → converges to 2
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if seq_type == "Arithmetic":
                render_steps(solve_arithmetic(a, d, int(n_terms)))
            elif seq_type == "Geometric":
                render_steps(solve_geometric(a, r, int(n_terms)))
            elif seq_type == "Fibonacci":
                render_steps(solve_fibonacci(int(n_terms)))
            else:
                render_steps(solve_recursive(a1, k, c, int(n_terms)))
        else:
            style.empty_state("a(n)")