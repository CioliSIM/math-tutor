import math
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.grid(True, alpha=0.2, color="#e0d8cc")


# ── CLASSICAL PROBABILITY ─────────────────────────────────────────────────────

def solve_classical(experiment, n_sim, target=None, fav=None, total=None):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Classical probability",
        """P(A) = favorable outcomes / total outcomes<br><br>
This works when all outcomes are equally likely.<br><br>
Three axioms always hold:<br>
&emsp;· 0 ≤ P(A) ≤ 1<br>
&emsp;· P(impossible event) = 0<br>
&emsp;· P(certain event) = 1<br><br>
The <strong>Law of Large Numbers</strong>: run the experiment many times —
the experimental frequency converges to the theoretical probability.""",
        "warm")

    if experiment == "die":
        theoretical = 1/6
        results = [random.randint(1,6) for _ in range(n_sim)]
        hits    = results.count(target)
        freq    = hits / n_sim
        add("P(rolling " + str(target) + ")",
            f"6 equally likely faces → P({target}) = 1/6 = <strong>{theoretical:.4f}</strong>")
        add("Simulation result",
            f"{n_sim} rolls → got {target} exactly {hits} times<br>"
            f"Experimental: {hits}/{n_sim} = {freq:.4f}<br>"
            f"Theoretical:  1/6 = {theoretical:.4f}<br>"
            f"Gap: {abs(freq-theoretical):.4f}",
            "sage")
        return {"steps": steps, "results": results, "target": target,
                "theoretical": theoretical, "label": f"P(rolling {target})"}

    elif experiment == "coin":
        theoretical = 0.5
        results = [random.choice([1,0]) for _ in range(n_sim)]
        heads   = sum(results)
        freq    = heads / n_sim
        add("P(heads)",
            f"Two equally likely outcomes → P(heads) = 1/2 = <strong>0.5</strong>")
        add("Simulation result",
            f"{n_sim} flips → Heads: {heads}, Tails: {n_sim-heads}<br>"
            f"Experimental P(heads) = {freq:.4f}<br>"
            f"Theoretical  P(heads) = 0.5000<br>"
            f"Gap: {abs(freq-0.5):.4f}",
            "sage")
        return {"steps": steps, "results": results, "target": 1,
                "theoretical": theoretical, "label": "P(heads)"}

    else:  # custom
        if total is None or total <= 0 or fav is None or fav < 0 or fav > total:
            add("Error", "Invalid inputs.", "error")
            return {"steps": steps}
        prob  = fav / total
        prob_c = (total - fav) / total
        add("Your experiment",
            f"P(A) = {fav}/{total} = <strong>{prob:.4f}</strong><br>"
            f"P(Aᶜ) = {total-fav}/{total} = {prob_c:.4f}<br><br>"
            f"P(A) + P(Aᶜ) = {prob+prob_c:.4f} = 1 ✓<br>"
            "Something either happens or it doesn't — they sum to 1.",
            "sage")
        return {"steps": steps, "results": None}


def plot_convergence(results, target, theoretical, label):
    running = []
    count = 0
    for i, r in enumerate(results):
        if r == target: count += 1
        running.append(count / (i+1))

    fig, ax = plt.subplots(figsize=(7, 4))
    styled_ax(ax, fig)
    ax.plot(range(1, len(results)+1), running,
            color="#e8602a", linewidth=1.2, label="Experimental frequency")
    ax.axhline(theoretical, color="#3d6b5e", linewidth=2,
               linestyle="--", label=f"Theoretical {theoretical:.4f}")
    ax.set_xlabel("Number of trials", color="#4a4540", fontsize=9)
    ax.set_ylabel("Running frequency", color="#4a4540", fontsize=9)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


# ── EVENT OPERATIONS ──────────────────────────────────────────────────────────

def solve_events(pA, pB, pAinB):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Event operations",
        """Events combine like sets:<br><br>
<strong>Complement</strong> Aᶜ: P(Aᶜ) = 1 − P(A)<br>
<strong>Union</strong> A∪B: P(A∪B) = P(A) + P(B) − P(A∩B) &nbsp;(don't count the overlap twice)<br>
<strong>Intersection</strong> A∩B: P(A∩B) = P(A)·P(B|A)""",
        "warm")

    if not (0<=pA<=1 and 0<=pB<=1 and 0<=pAinB<=1):
        add("Error","All probabilities must be between 0 and 1.","error")
        return {"steps":steps,"valid":False}
    if pAinB > min(pA,pB):
        add("Error",f"P(A∩B) cannot exceed min(P(A),P(B)) = {min(pA,pB):.4f}.","error")
        return {"steps":steps,"valid":False}

    pAunB = pA + pB - pAinB
    if pAunB > 1:
        add("Warning","P(A∪B) &gt; 1 — check your inputs.","error")
        return {"steps":steps,"valid":False}

    add("Computed values",
        f"P(Aᶜ) = 1 − {pA:g} = <strong>{1-pA:.4f}</strong><br>"
        f"P(Bᶜ) = 1 − {pB:g} = <strong>{1-pB:.4f}</strong><br>"
        f"P(A∪B) = {pA:g} + {pB:g} − {pAinB:g} = <strong>{pAunB:.4f}</strong>")

    excl = "YES — P(A∩B) = 0, they can't both happen at once." if pAinB==0 \
           else f"NO — P(A∩B) = {pAinB:g} ≠ 0, they can overlap."
    add("Mutually exclusive?", excl, "sage" if pAinB==0 else "")

    return {"steps":steps,"valid":True,"pA":pA,"pB":pB,"pAinB":pAinB,"pAunB":pAunB}


def plot_venn(pA, pB, pAinB, pAunB):
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")
    circA = plt.Circle((0.35, 0.5), 0.28, color="#e8602a", alpha=0.3)
    circB = plt.Circle((0.65, 0.5), 0.28, color="#3d6b5e", alpha=0.3)
    ax.add_patch(circA); ax.add_patch(circB)
    ax.text(0.22, 0.5, f"A only\n{pA-pAinB:.3f}", ha="center", va="center",
            fontsize=10, color="#e8602a")
    ax.text(0.78, 0.5, f"B only\n{pB-pAinB:.3f}", ha="center", va="center",
            fontsize=10, color="#3d6b5e")
    ax.text(0.5,  0.5, f"A∩B\n{pAinB:.3f}", ha="center", va="center",
            fontsize=10, color="#1a1814")
    ax.text(0.5, 0.1, f"P(A∪B) = {pAunB:.3f}", ha="center", fontsize=11,
            color="#4a4540")
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.axis("off")
    plt.tight_layout()
    return fig


# ── CONDITIONAL ───────────────────────────────────────────────────────────────

def solve_conditional(pA, pB, pAinB):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Conditional probability",
        """P(A|B) — the probability of A, <em>given that</em> B has happened.<br><br>
<span class="mf">P(A|B) = P(A∩B) / P(B)</span><br><br>
Intuition: knowing B restricts the world to outcomes in B.
Inside that smaller world, what fraction belongs to A?""",
        "warm")

    if pB == 0:
        add("Error","P(B) = 0 — cannot condition on an impossible event.","error")
        return {"steps":steps}

    pAgB = pAinB / pB
    pBgA = pAinB / pA if pA > 0 else None

    add("Computing P(A|B)",
        f"P(A|B) = {pAinB:g} / {pB:g} = <strong>{pAgB:.4f}</strong><br><br>"
        + (f"P(B|A) = {pAinB:g} / {pA:g} = <strong>{pBgA:.4f}</strong>"
           if pBgA is not None else "P(B|A) undefined (P(A)=0)"))

    if abs(pAgB - pA) < 1e-9:
        verdict = f"P(A|B) = P(A) = {pA:.4f} → A and B are <strong>INDEPENDENT</strong>. B carries no information about A."
        var = "sage"
    elif pAgB > pA:
        verdict = f"P(A|B) = {pAgB:.4f} &gt; P(A) = {pA:.4f} → knowing B makes A <strong>more likely</strong>."
        var = ""
    else:
        verdict = f"P(A|B) = {pAgB:.4f} &lt; P(A) = {pA:.4f} → knowing B makes A <strong>less likely</strong>."
        var = ""

    add("Did knowing B change anything?", verdict, var)

    add("Multiplication rule",
        f"Rearranging: P(A∩B) = P(B)·P(A|B) = {pB:g}·{pAgB:.4f} = {pB*pAgB:.4f}<br>"
        "Use this when you know P(A|B) and need P(A∩B).",
        "sage")

    return {"steps":steps}


# ── BAYES ─────────────────────────────────────────────────────────────────────

def solve_bayes(pA, pBgA, pB):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Bayes' theorem",
        """The most surprising result in probability — it lets you <em>flip</em> a conditional probability.<br><br>
<span class="mf">P(A|B) = P(B|A) · P(A) / P(B)</span><br><br>
<strong>Prior P(A):</strong> your belief before evidence<br>
<strong>Posterior P(A|B):</strong> updated belief after evidence<br>
<strong>Likelihood P(B|A):</strong> how well A explains the evidence<br><br>
This is the mathematical foundation of how rational agents update beliefs.""",
        "warm")

    # Medical test example (always shown)
    p_sick, p_pos_given_sick, p_pos_given_healthy = 0.01, 0.99, 0.01
    p_pos = p_pos_given_sick*p_sick + p_pos_given_healthy*(1-p_sick)
    p_sick_given_pos = p_pos_given_sick*p_sick / p_pos

    add("The medical test paradox",
        f"""Disease affects 1% of people. Test is 99% accurate.<br>
You test positive. What's the real probability you're sick?<br><br>
P(sick) = {p_sick} &nbsp;·&nbsp; P(+|sick) = {p_pos_given_sick} &nbsp;·&nbsp; P(+|healthy) = {p_pos_given_healthy}<br><br>
P(+) = {p_pos_given_sick}·{p_sick} + {p_pos_given_healthy}·{1-p_sick} = <strong>{p_pos:.4f}</strong><br><br>
P(sick|+) = {p_pos_given_sick}·{p_sick} / {p_pos:.4f} = <strong>{p_sick_given_pos:.4f} ≈ {p_sick_given_pos*100:.1f}%</strong><br><br>
Not 99%. Why? Among 10 000 people: ~99 true positives, ~99 false positives → 50/50.<br>
When the <em>prior</em> is low, even an accurate test produces many false positives.<br>
This is the <strong>base rate fallacy</strong> — it trips up doctors, journalists, and courts.""")

    if not (0<pB<=1 and 0<=pA<=1 and 0<=pBgA<=1):
        add("Error", "Invalid inputs.", "error")
        return {"steps":steps}

    pAgB = pBgA * pA / pB
    change = "more likely" if pAgB > pA else "less likely" if pAgB < pA else "unchanged"
    add("Your values",
        f"P(A|B) = P(B|A)·P(A)/P(B) = {pBgA:g}·{pA:g}/{pB:g} = <strong>{pAgB:.4f}</strong><br><br>"
        f"Before evidence: P(A) = {pA:.4f}<br>"
        f"After evidence:  P(A|B) = {pAgB:.4f}<br>"
        f"→ Evidence made A <strong>{change}</strong>.",
        "sage")

    return {"steps":steps, "prior":pA, "posterior":pAgB, "likelihood":pBgA}


def plot_bayes_chart(prior, posterior, likelihood):
    fig, ax = plt.subplots(figsize=(6, 4))
    styled_ax(ax, fig)
    cats   = ["Prior P(A)\nbefore evidence", "Posterior P(A|B)\nafter evidence"]
    vals   = [prior, posterior]
    colors = ["#3d6b5e", "#e8602a"]
    bars   = ax.bar(cats, vals, color=colors, width=0.4,
                    edgecolor="#fdfaf5", linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.015,
                f"{val:.4f}", ha="center", fontsize=12, color="#1a1814")
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability", color="#4a4540", fontsize=9)
    plt.tight_layout()
    return fig


# ── INDEPENDENT EVENTS ────────────────────────────────────────────────────────

def solve_independence(pA, pB, pAinB, chain_probs):
    steps = []
    def add(l, b, v=""): steps.append((l, b, v))

    add("Independent events",
        """Two events are independent if knowing one happened tells you nothing about the other.<br><br>
<strong>Formal test:</strong><br>
<span class="mf">A ⊥ B &nbsp;⟺&nbsp; P(A∩B) = P(A)·P(B)</span><br><br>
If you can just multiply the probabilities, they're independent.<br><br>
Examples of independence: two separate coin flips, two separate dice.<br>
Examples of dependence: drawing without replacement, weather on consecutive days.""",
        "warm")

    expected = pA * pB
    diff = abs(pAinB - expected)
    if diff < 1e-9:
        verdict = f"P(A∩B) = P(A)·P(B) = {expected:.4f} ✓ → A and B are <strong>INDEPENDENT</strong>."
        var = "sage"
    elif pAinB > expected:
        verdict = (f"P(A∩B) = {pAinB:.4f} &gt; P(A)·P(B) = {expected:.4f}<br>"
                   "→ <strong>DEPENDENT</strong> — they occur together more than chance predicts.")
        var = "error"
    else:
        verdict = (f"P(A∩B) = {pAinB:.4f} &lt; P(A)·P(B) = {expected:.4f}<br>"
                   "→ <strong>DEPENDENT</strong> — they avoid each other more than chance predicts.")
        var = "error"

    add("Independence test", verdict, var)

    # chain
    if chain_probs:
        joint = math.prod(chain_probs)
        rows  = ""
        r = 1
        for i, p in enumerate(chain_probs):
            r *= p
            rows += f"After event {i+1}: {r:.8f}<br>"
        add("Chain of independent events",
            f"For independent events: P(all) = P(E₁)·P(E₂)·…<br><br>"
            f"{rows}<br>"
            f"P(all {len(chain_probs)} events) = <strong>{joint:.8f}</strong><br><br>"
            + ("Less than 1% — chaining independent events shrinks probability fast."
               if joint < 0.01 else
               "Greater than 50% — more likely than not." if joint > 0.5 else ""),
            "sage")
        return {"steps":steps, "chain_probs":chain_probs, "joint":joint}

    return {"steps":steps}


def plot_chain(probs, joint):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.patch.set_facecolor("#fdfaf5")

    for ax in axes:
        ax.set_facecolor("#fdfaf5")
        ax.spines[["top","right"]].set_visible(False)
        ax.spines["bottom"].set_color("#e0d8cc")
        ax.spines["left"].set_color("#e0d8cc")
        ax.tick_params(colors="#4a4540", labelsize=8.5)
        ax.grid(True, alpha=0.2, color="#e0d8cc")

    labels = [f"E{i+1}" for i in range(len(probs))]
    axes[0].bar(labels, probs, color="#e8602a", alpha=0.8, edgecolor="#fdfaf5")
    axes[0].set_ylim(0, 1.1)
    axes[0].set_title("Individual probabilities", fontsize=10, color="#4a4540")
    axes[0].set_ylabel("P", color="#4a4540", fontsize=9)

    running = []
    r = 1
    for p in probs:
        r *= p
        running.append(r)
    axes[1].plot(range(1, len(probs)+1), running,
                 color="#e8602a", linewidth=2, marker="o",
                 markersize=7, markerfacecolor="#c8a96e")
    axes[1].axhline(joint, color="#3d6b5e", linewidth=1.5,
                    linestyle="--", label=f"Joint = {joint:.6f}")
    axes[1].set_ylim(0, 1.05)
    axes[1].set_title("Running joint probability", fontsize=10, color="#4a4540")
    axes[1].set_xlabel("Events chained", color="#4a4540", fontsize=9)
    axes[1].set_ylabel("P(all so far)", color="#4a4540", fontsize=9)
    axes[1].legend(fontsize=8.5, framealpha=0.7,
                   facecolor="#fdfaf5", edgecolor="#e0d8cc")
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
            ["Classical probability", "Event operations",
             "Conditional probability", "Bayes' theorem",
             "Independent events"],
            key="prob_topic")

        if topic == "Classical probability":
            exp = st.selectbox("Experiment", ["Die","Coin","Custom"], key="prob_exp")
            n_sim = st.number_input("Simulations", value=1000, min_value=10,
                                    max_value=50000, step=500, key="prob_sim")
            if exp == "Die":
                target = st.number_input("Target face", value=6, min_value=1,
                                         max_value=6, step=1, key="prob_die")
            elif exp == "Custom":
                fav   = st.number_input("Favorable outcomes", value=3, min_value=0, key="prob_fav")
                total = st.number_input("Total outcomes", value=10, min_value=1, key="prob_tot")

        elif topic in ["Event operations", "Conditional probability"]:
            pA    = st.number_input("P(A)", value=0.5, min_value=0.0, max_value=1.0,
                                    step=0.05, format="%.3f", key="prob_pA")
            pB    = st.number_input("P(B)", value=0.4, min_value=0.0, max_value=1.0,
                                    step=0.05, format="%.3f", key="prob_pB")
            pAinB = st.number_input("P(A∩B)", value=0.2, min_value=0.0, max_value=1.0,
                                    step=0.05, format="%.3f", key="prob_pAB")

        elif topic == "Bayes' theorem":
            pA_b  = st.number_input("Prior P(A)", value=0.01, min_value=0.0, max_value=1.0,
                                    step=0.01, format="%.4f", key="prob_bpA")
            pBgA  = st.number_input("Likelihood P(B|A)", value=0.99, min_value=0.0, max_value=1.0,
                                    step=0.01, format="%.4f", key="prob_bpBgA")
            pB_b  = st.number_input("P(B)", value=0.0198, min_value=0.0001, max_value=1.0,
                                    step=0.005, format="%.4f", key="prob_bpB")

        else:  # Independent
            pA_i  = st.number_input("P(A)", value=0.5, min_value=0.0, max_value=1.0,
                                    step=0.05, format="%.3f", key="prob_iA")
            pB_i  = st.number_input("P(B)", value=0.3, min_value=0.0, max_value=1.0,
                                    step=0.05, format="%.3f", key="prob_iB")
            pAinB_i = st.number_input("P(A∩B) observed", value=0.15, min_value=0.0,
                                       max_value=1.0, step=0.05, format="%.3f", key="prob_iAB")
            n_chain = st.number_input("Chain events to multiply", value=3,
                                      min_value=0, max_value=8, step=1, key="prob_cn")
            chain_inputs = []
            if n_chain > 0:
                for i in range(int(n_chain)):
                    p = st.number_input(f"P(E{i+1})", value=0.5, min_value=0.0,
                                        max_value=1.0, step=0.05, format="%.3f",
                                        key=f"prob_cp{i}")
                    chain_inputs.append(p)

        solve_btn = st.button("Compute →", key="prob_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Classical: die, target=6, 5000 sims<br>
    Events: P(A)=0.6, P(B)=0.5, P(A∩B)=0.3<br>
    Bayes: prior=0.01, lik=0.99, P(B)=0.0198<br>
    Independence: P(A∩B) = P(A)·P(B)?
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Classical probability":
                if exp == "Die":
                    r = solve_classical("die", int(n_sim), target=int(target))
                elif exp == "Coin":
                    r = solve_classical("coin", int(n_sim))
                else:
                    r = solve_classical("custom", int(n_sim), fav=int(fav), total=int(total))
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if r.get("results"):
                    st.markdown('<div class="graph-label">Law of Large Numbers</div>',
                                unsafe_allow_html=True)
                    fig = plot_convergence(r["results"], r["target"],
                                          r["theoretical"], r["label"])
                    st.pyplot(fig); plt.close(fig)

            elif topic == "Event operations":
                r = solve_events(pA, pB, pAinB)
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if r.get("valid"):
                    style.result_band(
                        ("P(A∪B)", f"{r['pAunB']:.4f}"),
                        ("P(Aᶜ)",  f"{1-pA:.4f}"),
                        ("P(Bᶜ)",  f"{1-pB:.4f}"),
                    )
                    st.markdown('<div class="graph-label">Venn diagram</div>',
                                unsafe_allow_html=True)
                    fig = plot_venn(pA, pB, pAinB, r["pAunB"])
                    st.pyplot(fig); plt.close(fig)

            elif topic == "Conditional probability":
                r = solve_conditional(pA, pB, pAinB)
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)

            elif topic == "Bayes' theorem":
                r = solve_bayes(pA_b, pBgA, pB_b)
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if "prior" in r:
                    style.result_band(
                        ("Prior P(A)",     f"{r['prior']:.4f}"),
                        ("Posterior P(A|B)", f"{r['posterior']:.4f}"),
                        ("Likelihood P(B|A)", f"{r['likelihood']:.4f}"),
                    )
                    st.markdown('<div class="graph-label">Belief update</div>',
                                unsafe_allow_html=True)
                    fig = plot_bayes_chart(r["prior"], r["posterior"], r["likelihood"])
                    st.pyplot(fig); plt.close(fig)

            else:
                chain_probs = chain_inputs if n_chain > 0 else []
                r = solve_independence(pA_i, pB_i, pAinB_i, chain_probs)
                for lbl, body, var in r["steps"]:
                    style.step(lbl, body, var)
                if r.get("chain_probs"):
                    st.markdown('<div class="graph-label">Chain probability</div>',
                                unsafe_allow_html=True)
                    fig = plot_chain(r["chain_probs"], r["joint"])
                    st.pyplot(fig); plt.close(fig)
        else:
            style.empty_state("P(A)")