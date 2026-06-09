import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Pure logic ────────────────────────────────────────────────────────────────

def solve_factorial(n):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    if n < 0:
        add("Error", "Factorial is not defined for negative numbers.", "error")
        return {"steps": steps}

    add("What is a factorial?",
        """n! is the product of all integers from 1 to n:<br><br>
<span class="mf">n! = 1 · 2 · 3 · … · n</span><br><br>
Intuition: if you have n distinct objects, n! is the number of ways to arrange them in a line.<br>
Three objects A, B, C → 3! = 6 arrangements: ABC, ACB, BAC, BCA, CAB, CBA.<br><br>
Special case: <strong>0! = 1</strong> by definition — there is exactly one way to arrange nothing.""",
        "warm")

    if n == 0:
        add("Result", "0! = <strong>1</strong>  (by definition)", "sage")
        result = 1
    else:
        factors = list(range(1, n+1))
        expansion = " · ".join(str(f) for f in factors)
        running = []
        r = 1
        for f in factors:
            r *= f
            running.append(f"{f} → {r}")
        add("Step by step",
            f"{n}! = {expansion}<br><br>" + "<br>".join(running))
        result = r
        add("Result", f"{n}! = <strong>{result}</strong>", "sage")

    # growth table
    rows = ""
    for i in [1,2,3,4,5,10,15,20]:
        rows += f"<tr><td style='padding:0.25rem 0.8rem;font-family:\"DM Mono\",monospace;'>{i}</td><td style='padding:0.25rem 0.8rem;'>{math.factorial(i):,}</td></tr>"
    add("How fast does factorial grow?",
        f"""<table style="border-collapse:collapse;font-size:0.84rem;">
<thead><tr style="border-bottom:1px solid var(--border);font-family:'DM Mono',monospace;
font-size:0.62rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--sand);">
<td style="padding:0.25rem 0.8rem;">n</td><td style="padding:0.25rem 0.8rem;">n!</td></tr></thead>
<tbody>{rows}</tbody></table><br>
20! has {len(str(math.factorial(20)))} digits. Factorials grow faster than exponentials — much faster.""")

    return {"steps": steps, "result": result}


def solve_dispositions(n, k, with_rep):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Dispositions — ordered selections",
        """A disposition is an <strong>ordered</strong> selection of k objects from n.<br>
(A,B) and (B,A) are two different dispositions.<br><br>
<strong>Without repetition:</strong> &nbsp;D(n,k) = n!/(n−k)!<br>
<strong>With repetition:</strong> &nbsp;&nbsp;D′(n,k) = n^k""",
        "warm")

    if n < 0 or k < 0:
        add("Error", "n and k must be non-negative.", "error")
        return {"steps": steps}

    if with_rep:
        result = n**k
        add("Computing D′(n,k) = n^k",
            f"Each of the {k} slots has {n} independent choices.<br><br>"
            + "<br>".join(f"Slot {i+1}: {n} choices" for i in range(min(k,6)))
            + (f"<br>… ({k} slots total)" if k > 6 else "")
            + f"<br><br>D′({n},{k}) = {n}^{k} = <strong>{result}</strong>",
            "sage")
    else:
        if k > n:
            add("Impossible", f"k={k} &gt; n={n} — cannot pick {k} distinct objects from {n}.", "error")
            return {"steps": steps}
        factors = list(range(n, n-k, -1))
        result = math.prod(factors)
        add("Computing D(n,k) = n·(n−1)·…·(n−k+1)",
            f"Multiply {k} consecutive integers starting from {n}:<br><br>"
            + " · ".join(str(f) for f in factors)
            + f" = <strong>{result}</strong><br><br>"
            f"D({n},{k}) = {result}",
            "sage")

    return {"steps": steps, "result": result}


def solve_combinations(n, k):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Combinations — unordered selections",
        """A combination is a selection where <strong>order does not matter</strong>.<br>
(A,B) and (B,A) are the <em>same</em> combination.<br><br>
<span class="mf">C(n,k) = n! / (k! · (n−k)!)</span><br><br>
Where it comes from: start with D(n,k) ordered selections.
Each group of k objects appears k! times (one per ordering).
Since order doesn't matter, divide by k!.<br><br>
Beautiful symmetry: <strong>C(n,k) = C(n, n−k)</strong><br>
Choosing k to include = choosing n−k to leave out.""",
        "warm")

    if n < 0 or k < 0:
        add("Error", "n and k must be non-negative.", "error")
        return {"steps": steps}
    if k > n:
        add("Result", f"k &gt; n → C({n},{k}) = 0. Can't choose more objects than available.", "sage")
        return {"steps": steps, "result": 0}

    num   = math.factorial(n)
    den_k = math.factorial(k)
    den_r = math.factorial(n-k)
    den   = den_k * den_r
    result = num // den
    disp  = math.factorial(n) // math.factorial(n-k)

    add("Computing C(n,k)",
        f"C({n},{k}) = {n}! / ({k}! · {n-k}!)<br><br>"
        f"{n}! = {num:,}<br>"
        f"{k}! = {den_k:,}<br>"
        f"{n-k}! = {den_r:,}<br>"
        f"{k}!·{n-k}! = {den:,}<br><br>"
        f"C({n},{k}) = {num:,} / {den:,} = <strong>{result:,}</strong>",
        "sage")

    add("Comparison with dispositions",
        f"D({n},{k}) = {disp:,} &nbsp;ordered selections<br>"
        f"C({n},{k}) = {result:,} &nbsp;unordered selections<br><br>"
        f"{disp:,} / {result:,} = {disp//result} = {k}! ✓ &nbsp;(each combination maps to {k}! dispositions)<br><br>"
        f"Symmetry: C({n},{n-k}) = {math.comb(n,n-k):,} = C({n},{k}) ✓")

    return {"steps": steps, "result": result}


def solve_pascal(rows):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    triangle = [[math.comb(n, k) for k in range(n+1)] for n in range(rows)]

    add("Triangolo di Tartaglia — Pascal's Triangle",
        """Construction rule: each number is the sum of the two above it. Edges are always 1.<br><br>
What makes it extraordinary: every number at row n, position k is <strong>C(n,k)</strong>.<br>
The triangle <em>is</em> the complete table of binomial coefficients, disguised as simple addition.<br><br>
<em>Historical note: known in China, Persia, and India centuries before Tartaglia (1500s) and Pascal (1600s).</em>""",
        "warm")

    # row sums
    sums = "<br>".join(
        f"Row {n}: sum = {sum(triangle[n])} = 2^{n}"
        for n in range(min(rows, 8))
    )
    add("Five hidden patterns",
        f"<strong>1. Row sums = powers of 2:</strong><br>{sums}<br><br>"
        f"<strong>2. Symmetry:</strong> C(n,k) = C(n,n−k) — every row is a palindrome.<br><br>"
        f"<strong>3. Hockey stick identity:</strong> C(r,r)+C(r+1,r)+…+C(n,r) = C(n+1,r+1)<br><br>"
        f"<strong>4. Fibonacci in the diagonals:</strong> shallow diagonal sums give 1,1,2,3,5,8,13,…<br><br>"
        f"<strong>5. Sierpinski fractal:</strong> colour odd numbers black — the Sierpinski triangle appears.")

    # Sierpinski text preview
    sier_lines = []
    sz = min(rows, 16)
    tri2 = [[math.comb(n, k) for k in range(n+1)] for n in range(sz)]
    for n in range(sz):
        sp = " " * (sz - n - 1)
        chars = "  ".join("█" if x%2==1 else "·" for x in tri2[n])
        sier_lines.append(f"{sp}{chars}")

    add("Sierpinski preview  (█=odd, ·=even)",
        "<code style='font-size:0.75rem;line-height:1.6;'>"
        + "<br>".join(sier_lines) + "</code>")

    return {"steps": steps, "triangle": triangle, "rows": rows}


def solve_binomial(n):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("The binomial theorem",
        """How do you expand (a+b)^n without multiplying n times?<br><br>
<span class="mf">(a+b)^n = Σ C(n,k) · a^(n−k) · b^k &nbsp;&nbsp; k=0…n</span><br><br>
The coefficients are exactly row n of Pascal's triangle.<br><br>
<strong>Why?</strong> Each term a^(n−k)·b^k appears whenever you choose b from exactly k of the n factors.
There are C(n,k) ways to make that choice.""",
        "warm")

    if n < 0:
        add("Error", "n must be non-negative.", "error")
        return {"steps": steps}

    terms = []
    term_lines = []
    for k in range(n+1):
        coeff = math.comb(n, k)
        a_exp, b_exp = n-k, k
        a_str = "" if a_exp==0 else ("a" if a_exp==1 else f"a^{a_exp}")
        b_str = "" if b_exp==0 else ("b" if b_exp==1 else f"b^{b_exp}")
        c_str = "" if (coeff==1 and (a_str or b_str)) else str(coeff)
        term  = (c_str + a_str + b_str) or "1"
        terms.append(term)
        term_lines.append(f"k={k}: C({n},{k}) · {a_str or '1'} · {b_str or '1'} = {coeff}·{a_str or '1'}·{b_str or '1'}")

    coeffs = [math.comb(n,k) for k in range(n+1)]
    add("Expansion term by term",
        "<br>".join(term_lines) + f"<br><br>"
        f"<span class='mf'>(a+b)^{n} = {' + '.join(terms)}</span>",
        "sage")

    alt = sum((-1)**k * math.comb(n,k) for k in range(n+1))
    add("Two quick verifications",
        f"a=1, b=1: &nbsp;(1+1)^{n} = 2^{n} = {2**n} &nbsp;·&nbsp; sum of coefficients = {sum(coeffs)} ✓<br>"
        f"a=1, b=−1: (1−1)^{n} = {0 if n>0 else 1} &nbsp;·&nbsp; alternating sum = {alt} "
        f"{'✓' if (n>0 and alt==0) or (n==0 and alt==1) else '✗'}")

    return {"steps": steps, "coeffs": coeffs, "n": n}


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_pascal(triangle, rows):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#fdfaf5")

    # heatmap
    matrix = np.zeros((rows, rows))
    for n, row in enumerate(triangle):
        for k, val in enumerate(row):
            matrix[n][k] = val
    im = axes[0].imshow(matrix, cmap="YlOrRd", aspect="auto")
    axes[0].set_facecolor("#fdfaf5")
    axes[0].set_title("Pascal's Triangle — value heatmap", fontsize=10, color="#4a4540")
    axes[0].set_xlabel("k", color="#4a4540", fontsize=9)
    axes[0].set_ylabel("n", color="#4a4540", fontsize=9)
    axes[0].tick_params(colors="#4a4540")
    plt.colorbar(im, ax=axes[0])
    max_val = max(max(r) for r in triangle) if triangle else 1
    for n in range(min(rows, 10)):
        for k in range(n+1):
            axes[0].text(k, n, str(triangle[n][k]),
                        ha="center", va="center",
                        fontsize=max(5, 9-rows//3),
                        color="black" if triangle[n][k] < max_val*0.6 else "white")

    # sierpinski
    sz  = min(rows, 32)
    tri2 = [[math.comb(n, k) for k in range(n+1)] for n in range(sz)]
    sier = np.zeros((sz, sz))
    for n in range(sz):
        for k in range(n+1):
            sier[n][k] = tri2[n][k] % 2
    axes[1].imshow(sier, cmap="binary", aspect="auto")
    axes[1].set_facecolor("#fdfaf5")
    axes[1].set_title("Sierpinski Triangle\n(odd=black, even=white)", fontsize=10, color="#4a4540")
    axes[1].set_xlabel("k", color="#4a4540", fontsize=9)
    axes[1].set_ylabel("n", color="#4a4540", fontsize=9)
    axes[1].tick_params(colors="#4a4540")

    plt.tight_layout()
    return fig


def plot_binomial(coeffs, n):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.patch.set_facecolor("#fdfaf5")

    for ax in axes:
        ax.set_facecolor("#fdfaf5")
        ax.spines[["top","right"]].set_visible(False)
        ax.spines["bottom"].set_color("#e0d8cc")
        ax.spines["left"].set_color("#e0d8cc")
        ax.tick_params(colors="#4a4540", labelsize=8.5)
        ax.grid(True, alpha=0.2, color="#e0d8cc")

    k_vals = list(range(n+1))
    ml, sl, bl = axes[0].stem(k_vals, coeffs, linefmt="#e8602a",
                               markerfmt="o", basefmt="#1a1814")
    plt.setp(ml, color="#c8a96e", markersize=7)
    plt.setp(sl, linewidth=1.5)
    axes[0].set_title(f"Coefficients of (a+b)^{n}", fontsize=10, color="#4a4540", pad=6)
    axes[0].set_xlabel("k", color="#4a4540", fontsize=9)
    axes[0].set_ylabel("C(n,k)", color="#4a4540", fontsize=9)

    # normalised (probability distribution shape)
    total = sum(coeffs)
    norm  = [c/total for c in coeffs]
    axes[1].bar(k_vals, norm, color="#e8602a", alpha=0.7, edgecolor="#fdfaf5")
    axes[1].set_title(f"Normalised (sums to 1)", fontsize=10, color="#4a4540", pad=6)
    axes[1].set_xlabel("k", color="#4a4540", fontsize=9)
    axes[1].set_ylabel("C(n,k) / 2^n", color="#4a4540", fontsize=9)

    plt.tight_layout()
    return fig


# ── Public entry point ────────────────────────────────────────────────────────

def render(n, name, subtitle, category):
    style.module_header(category, n, name, subtitle)

    left, right = st.columns([1, 1.75], gap="large")

    with left:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="input-panel-label">Choose topic</div>',
                    unsafe_allow_html=True)

        topic = st.selectbox("Topic",
            ["Factorial", "Dispositions", "Combinations",
             "Pascal's Triangle", "Binomial Theorem"],
            key="comb_topic")

        if topic == "Factorial":
            n_val = st.number_input("n", value=5, min_value=0, step=1, key="comb_n")

        elif topic == "Dispositions":
            n_val  = st.number_input("Total objects n", value=5, min_value=0, step=1, key="disp_n")
            k_val  = st.number_input("Select k", value=2, min_value=0, step=1, key="disp_k")
            rep    = st.checkbox("Allow repetition", value=False, key="disp_rep")

        elif topic == "Combinations":
            n_val = st.number_input("Total objects n", value=6, min_value=0, step=1, key="comb_cn")
            k_val = st.number_input("Choose k", value=2, min_value=0, step=1, key="comb_ck")

        elif topic == "Pascal's Triangle":
            rows_val = st.number_input("Rows to display", value=8,
                                       min_value=2, max_value=20, step=1, key="comb_rows")

        else:  # Binomial
            n_val = st.number_input("Exponent n", value=4, min_value=0, step=1, key="binom_n")

        solve_btn = st.button("Compute →", key="comb_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Factorial: <code>n=10</code> → 3 628 800<br>
    Dispositions: <code>n=5, k=2</code> (no rep) → 20<br>
    Combinations: <code>n=52, k=5</code> → poker hands<br>
    Pascal: <code>rows=12</code> → see Sierpinski<br>
    Binomial: <code>n=4</code> → expand (a+b)⁴
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Factorial":
                r = solve_factorial(int(n_val))
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)

            elif topic == "Dispositions":
                r = solve_dispositions(int(n_val), int(k_val), rep)
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if "result" in r:
                    style.result_band(
                        ("n", str(int(n_val))),
                        ("k", str(int(k_val))),
                        ("Result", f"{r['result']:,}"),
                    )

            elif topic == "Combinations":
                r = solve_combinations(int(n_val), int(k_val))
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if "result" in r:
                    style.result_band(
                        ("C(n,k)", f"C({int(n_val)},{int(k_val)})"),
                        ("Result", f"{r['result']:,}"),
                    )

            elif topic == "Pascal's Triangle":
                r = solve_pascal(int(rows_val))
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                st.markdown('<div class="graph-label">Triangle visualisation</div>',
                            unsafe_allow_html=True)
                fig = plot_pascal(r["triangle"], r["rows"])
                st.pyplot(fig); plt.close(fig)

            else:  # Binomial
                r = solve_binomial(int(n_val))
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if "coeffs" in r:
                    st.markdown('<div class="graph-label">Coefficient distribution</div>',
                                unsafe_allow_html=True)
                    fig = plot_binomial(r["coeffs"], r["n"])
                    st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("C(n,k)")