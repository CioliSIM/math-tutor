import math
import random
import matplotlib.pyplot as plt
import numpy as np


def plot_frequency_convergence(results, target, theoretical, label):
    running_freq = []
    count = 0
    for i, r in enumerate(results):
        if r == target:
            count += 1
        running_freq.append(count / (i+1))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(range(1, len(results)+1), running_freq,
            color="crimson", linewidth=1.5, label="Experimental frequency")
    ax.axhline(theoretical, color="steelblue", linewidth=2,
               linestyle="--", label=f"Theoretical {label} = {theoretical:.4f}")
    ax.set_title(f"Law of Large Numbers — {label}", fontsize=14)
    ax.set_xlabel("Number of trials")
    ax.set_ylabel("Running frequency")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.show()


def plot_venn(pA, pB, pAinB):
    fig, ax = plt.subplots(figsize=(8, 5))

    circleA = plt.Circle((0.35, 0.5), 0.28, color="crimson",
                          alpha=0.3, label=f"A  P={pA:.3f}")
    circleB = plt.Circle((0.65, 0.5), 0.28, color="steelblue",
                          alpha=0.3, label=f"B  P={pB:.3f}")
    ax.add_patch(circleA)
    ax.add_patch(circleB)

    ax.text(0.22, 0.5, f"A only\n{pA-pAinB:.3f}",
            ha="center", va="center", fontsize=11, color="crimson")
    ax.text(0.78, 0.5, f"B only\n{pB-pAinB:.3f}",
            ha="center", va="center", fontsize=11, color="steelblue")
    ax.text(0.5,  0.5, f"A∩B\n{pAinB:.3f}",
            ha="center", va="center", fontsize=11, color="black")
    ax.text(0.5, 0.08, f"P(A∪B) = {pA+pB-pAinB:.3f}",
            ha="center", fontsize=12)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Venn Diagram — Event Operations", fontsize=14)
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


def plot_bayes(prior, posterior, likelihood):
    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ["Prior P(A)\nbefore evidence", "Posterior P(A|B)\nafter evidence"]
    values     = [prior, posterior]
    colors     = ["steelblue", "crimson"]

    bars = ax.bar(categories, values, color=colors,
                  width=0.4, edgecolor="black", linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.015,
                f"{val:.4f}", ha="center", fontsize=13, fontweight="bold")

    ax.axhline(1, color="gray", linewidth=0.8,
               linestyle="--", alpha=0.5)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability")
    ax.set_title(f"Bayes' Theorem — How evidence updates belief\n"
                 f"(likelihood P(B|A) = {likelihood:.4f})", fontsize=13)
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.show()


def plot_independent(probs, joint):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    labels = [f"P(E{i+1})\n={p:.3f}" for i, p in enumerate(probs)]
    colors = plt.cm.RdYlGn([p for p in probs])
    axes[0].bar(labels, probs, color=colors,
                edgecolor="black", linewidth=0.5)
    axes[0].axhline(0.5, color="gray", linewidth=1,
                    linestyle="--", alpha=0.6, label="0.5")
    axes[0].set_ylim(0, 1.1)
    axes[0].set_title("Individual probabilities", fontsize=12)
    axes[0].set_ylabel("Probability")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis="y")

    running = []
    prod = 1
    for p in probs:
        prod *= p
        running.append(prod)

    axes[1].plot(range(1, len(probs)+1), running,
                 color="crimson", linewidth=2, marker="o", markersize=8)
    axes[1].axhline(joint, color="steelblue", linewidth=1.5,
                    linestyle="--", label=f"Joint = {joint:.6f}")
    axes[1].set_title("Running joint probability\n(watch how fast it shrinks)",
                      fontsize=12)
    axes[1].set_xlabel("Number of events")
    axes[1].set_ylabel("P(all events so far)")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Independent Events", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def classical_probability():
    print(f"\n{'='*50}")
    print(f"CLASSICAL PROBABILITY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Probability answers one question:")
    print(f"  how likely is something to happen?")
    print(f"")
    print(f"  The classical definition gives a precise number:")
    print(f"")
    print(f"      P(A) = favorable outcomes / total outcomes")
    print(f"")
    print(f"  This works whenever all outcomes are equally likely —")
    print(f"  a fair die, a shuffled deck, a fair coin.")
    print(f"")
    print(f"  Three rules that always hold:")
    print(f"  · 0 ≤ P(A) ≤ 1    probability lives between 0 and 1")
    print(f"  · P(impossible) = 0   something that can't happen")
    print(f"  · P(certain) = 1      something that always happens")
    print(f"")
    print(f"  The frequentist view adds something important:")
    print(f"  run the experiment thousands of times.")
    print(f"  The proportion of times A occurs approaches P(A).")
    print(f"  This is the Law of Large Numbers — and we'll see it live.")
    print(f"")
    print(f"  Choose an experiment:")
    print(f"  1 — Roll a die")
    print(f"  2 — Flip a coin")
    print(f"  3 — Draw from a deck of cards")
    print(f"  4 — Custom experiment")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        print(f"\n--- Rolling a fair die ---")
        print(f"  Six faces, each equally likely.")
        print(f"  P(any face) = 1/6 ≈ {1/6:.4f}")
        print(f"")
        target = int(input("  Which face are you interested in? (1-6): "))
        if not 1 <= target <= 6:
            print(f"  Must be between 1 and 6.")
            return

        print(f"\n  P(rolling {target}) = 1/6 = {1/6:.4f}")
        print(f"")
        n = int(input("  How many times to simulate? "))
        results = [random.randint(1, 6) for _ in range(n)]
        hits    = results.count(target)
        freq    = hits / n

        print(f"\n--- Simulation ---")
        print(f"  Rolled {n} times.")
        print(f"  Got {target} exactly {hits} times.")
        print(f"  Experimental: {hits}/{n} = {freq:.4f}")
        print(f"  Theoretical:  1/6   = {1/6:.4f}")
        print(f"  Gap: {abs(freq - 1/6):.4f}")
        print(f"")
        print(f"  The more rolls, the smaller the gap.")
        print(f"  That's the Law of Large Numbers — not a coincidence,")
        print(f"  a theorem. Watch it on the graph.")

        plot_frequency_convergence(results, target, 1/6,
                                   f"P(rolling {target})")

    elif choice == "2":
        print(f"\n--- Flipping a fair coin ---")
        print(f"  Two outcomes, equally likely.")
        print(f"  P(heads) = P(tails) = 1/2 = 0.5")
        print(f"")
        n       = int(input("  How many flips to simulate? "))
        results = [random.choice([1, 0]) for _ in range(n)]
        heads   = sum(results)
        freq    = heads / n

        print(f"\n--- Simulation ---")
        print(f"  Flipped {n} times.")
        print(f"  Heads: {heads},  Tails: {n-heads}")
        print(f"  Experimental P(heads) = {heads}/{n} = {freq:.4f}")
        print(f"  Theoretical  P(heads) = 0.5000")
        print(f"  Gap: {abs(freq-0.5):.4f}")

        plot_frequency_convergence(results, 1, 0.5, "P(heads)")

    elif choice == "3":
        print(f"\n--- Drawing from a standard deck ---")
        print(f"  52 cards: 4 suits × 13 values")
        print(f"  13 of each suit, 4 of each value.")
        print(f"")
        print(f"  Which event?")
        print(f"  1 — Drawing a heart      (13 out of 52)")
        print(f"  2 — Drawing an ace       (4 out of 52)")
        print(f"  3 — Drawing a face card  (12 out of 52: J, Q, K)")
        print(f"")
        ev = input("  Enter 1, 2, or 3: ")

        if ev == "1":
            fav, tot, label = 13, 52, "heart"
        elif ev == "2":
            fav, tot, label = 4, 52, "ace"
        elif ev == "3":
            fav, tot, label = 12, 52, "face card"
        else:
            print(f"  Invalid choice.")
            return

        prob = fav / tot
        g    = math.gcd(fav, tot)
        print(f"\n  P({label}) = {fav}/{tot} = {fav//g}/{tot//g} = {prob:.4f}")
        print(f"")
        print(f"  {fav} favorable outcomes out of {tot} total.")
        print(f"  One in every {tot//fav} cards on average.")

    elif choice == "4":
        print(f"\n--- Custom experiment ---")
        total = int(input("  Total equally likely outcomes: "))
        fav   = int(input("  Favorable outcomes: "))

        if fav > total or fav < 0 or total <= 0:
            print(f"  Invalid inputs.")
            return

        prob = fav / total
        print(f"\n  P(A) = {fav}/{total} = {prob:.4f}")
        print(f"  P(Aᶜ) = {total-fav}/{total} = {(total-fav)/total:.4f}")
        print(f"  P(A) + P(Aᶜ) = {prob + (total-fav)/total:.4f} = 1 ✓")
        print(f"")
        print(f"  The complement always brings you back to 1.")
        print(f"  Something either happens or it doesn't — no other option.")

    else:
        print(f"  Invalid choice.")


def event_operations():
    print(f"\n{'='*50}")
    print(f"EVENT OPERATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  An event is any collection of outcomes we care about.")
    print(f"  We can combine events — just like sets in algebra.")
    print(f"")
    print(f"  COMPLEMENT  Aᶜ — everything that is NOT A")
    print(f"      P(Aᶜ) = 1 - P(A)")
    print(f"  If P(rain) = 0.3, then P(no rain) = 0.7.")
    print(f"  Simple — but used constantly.")
    print(f"")
    print(f"  UNION  A ∪ B — A or B or both")
    print(f"      P(A ∪ B) = P(A) + P(B) - P(A ∩ B)")
    print(f"  We subtract P(A∩B) because it would be counted twice.")
    print(f"  Think of it as: don't count the overlap twice.")
    print(f"")
    print(f"  INTERSECTION  A ∩ B — both A and B")
    print(f"      P(A ∩ B) = P(A) · P(B|A)")
    print(f"  Both events must happen simultaneously.")
    print(f"")
    print(f"  Special case — mutually exclusive events:")
    print(f"  If A and B can't both happen at once, P(A∩B) = 0")
    print(f"  and the union simplifies to P(A∪B) = P(A) + P(B).")
    print(f"  Rolling a 3 and rolling a 5 on the same die — exclusive.")
    print(f"")

    pA    = float(input("  P(A): "))
    pB    = float(input("  P(B): "))
    pAinB = float(input("  P(A ∩ B): "))

    if not (0 <= pA <= 1 and 0 <= pB <= 1 and 0 <= pAinB <= 1):
        print(f"  Probabilities must be between 0 and 1.")
        return
    if pAinB > min(pA, pB):
        print(f"  P(A∩B) can't exceed min(P(A), P(B)) = {min(pA,pB):.4f}.")
        return

    pAunB = pA + pB - pAinB
    pAc   = 1 - pA
    pBc   = 1 - pB

    print(f"\n--- Results ---")
    print(f"  P(A)     = {pA:.4f}")
    print(f"  P(B)     = {pB:.4f}")
    print(f"  P(A∩B)   = {pAinB:.4f}")
    print(f"")
    print(f"  P(Aᶜ)    = 1 - {pA} = {pAc:.4f}")
    print(f"  P(Bᶜ)    = 1 - {pB} = {pBc:.4f}")
    print(f"  P(A∪B)   = {pA} + {pB} - {pAinB} = {pAunB:.4f}")
    print(f"")

    if pAunB > 1:
        print(f"  Warning: P(A∪B) > 1 — check your inputs.")
        return

    print(f"--- Are A and B mutually exclusive? ---")
    if pAinB == 0:
        print(f"  P(A∩B) = 0 → YES.")
        print(f"  They can't both happen.")
        print(f"  P(A∪B) = P(A) + P(B) = {pA+pB:.4f} — no subtraction needed.")
    else:
        print(f"  P(A∩B) = {pAinB} ≠ 0 → NO.")
        print(f"  They can overlap — and they do.")

    plot_venn(pA, pB, pAinB)


def conditional_probability():
    print(f"\n{'='*50}")
    print(f"CONDITIONAL PROBABILITY")
    print(f"{'='*50}")
    print(f"")
    print(f"  New information changes probabilities.")
    print(f"  Conditional probability captures this precisely.")
    print(f"")
    print(f"  P(A|B) — read 'probability of A given B' —")
    print(f"  is the probability of A, knowing that B has happened.")
    print(f"")
    print(f"      P(A|B) = P(A ∩ B) / P(B)")
    print(f"")
    print(f"  The intuition:")
    print(f"  Knowing B restricts the world to only outcomes in B.")
    print(f"  Inside that smaller world, what fraction belongs to A?")
    print(f"  That fraction is P(A∩B) / P(B).")
    print(f"")
    print(f"  A concrete example:")
    print(f"  Roll a die. You're told the result is even — {'{'}2,4,6{'}'}.")
    print(f"  What's the probability it's greater than 4?")
    print(f"")
    print(f"  Without the info: P(>4) = P({'{'}5,6{'}'}) = 2/6 = 1/3")
    print(f"  With the info: only {'{'}2,4,6{'}'} are possible.")
    print(f"  Of these, only 6 is greater than 4.")
    print(f"  P(>4 | even) = P({'{'}6{'}'}) / P({'{'}2,4,6{'}'}) = (1/6)/(3/6) = 1/3")
    print(f"")
    print(f"  Same result — knowing it's even didn't help.")
    print(f"  That means these two events are independent.")
    print(f"  (More on this soon.)")
    print(f"")

    pA    = float(input("  P(A): "))
    pB    = float(input("  P(B): "))
    pAinB = float(input("  P(A ∩ B): "))

    if not (0 <= pA <= 1 and 0 <= pB <= 1 and 0 <= pAinB <= 1):
        print(f"  All probabilities must be between 0 and 1.")
        return
    if pB == 0:
        print(f"  P(B) = 0 — you can't condition on an impossible event.")
        return
    if pAinB > min(pA, pB):
        print(f"  P(A∩B) can't exceed min(P(A), P(B)).")
        return

    pAgB = pAinB / pB
    pBgA = pAinB / pA if pA > 0 else None

    print(f"\n--- Computing P(A|B) ---")
    print(f"  P(A|B) = P(A∩B) / P(B)")
    print(f"         = {pAinB} / {pB}")
    print(f"         = {pAgB:.4f}")
    print(f"")
    if pBgA is not None:
        print(f"  P(B|A) = P(A∩B) / P(A)")
        print(f"         = {pAinB} / {pA}")
        print(f"         = {pBgA:.4f}")
        print(f"")

    print(f"--- Did knowing B change anything? ---")
    print(f"  P(A)   = {pA:.4f}  (without information)")
    print(f"  P(A|B) = {pAgB:.4f}  (knowing B happened)")
    print(f"")
    if abs(pAgB - pA) < 1e-9:
        print(f"  They're equal → A and B are INDEPENDENT.")
        print(f"  B carries no information about A.")
    elif pAgB > pA:
        print(f"  P(A|B) > P(A) → knowing B makes A more likely.")
        print(f"  B is positive evidence for A.")
    else:
        print(f"  P(A|B) < P(A) → knowing B makes A less likely.")
        print(f"  B is evidence against A.")

    print(f"\n--- The multiplication rule ---")
    print(f"  Rearranging the formula gives something useful:")
    print(f"  P(A∩B) = P(B) · P(A|B)")
    print(f"         = {pB} · {pAgB:.4f} = {pB*pAgB:.4f}")
    print(f"  Use this when you know P(A|B) and need P(A∩B).")


def bayes_theorem():
    print(f"\n{'='*50}")
    print(f"BAYES' THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  Bayes' theorem is the most surprising result in probability.")
    print(f"  It lets you flip a conditional probability:")
    print(f"  if you know P(B|A), you can compute P(A|B).")
    print(f"")
    print(f"      P(A|B) = P(B|A) · P(A) / P(B)")
    print(f"")
    print(f"  Where it comes from — just algebra:")
    print(f"  P(A|B) = P(A∩B)/P(B)")
    print(f"  P(B|A) = P(A∩B)/P(A)  →  P(A∩B) = P(B|A)·P(A)")
    print(f"  Substitute: P(A|B) = P(B|A)·P(A) / P(B)  ✓")
    print(f"")
    print(f"  The terms have names:")
    print(f"  · P(A)    = prior    — your belief before seeing evidence")
    print(f"  · P(A|B)  = posterior — your updated belief after evidence")
    print(f"  · P(B|A)  = likelihood — how well A explains the evidence")
    print(f"  · P(B)    = normalizer — makes everything sum to 1")
    print(f"")
    print(f"  Bayes tells you HOW TO UPDATE your beliefs")
    print(f"  when new evidence arrives.")
    print(f"  This is why it's the foundation of machine learning.")
    print(f"")

    print(f"--- The medical test paradox ---")
    print(f"")
    print(f"  A disease affects 1% of the population.")
    print(f"  A test is 99% accurate:")
    print(f"  · If you have it, test is positive 99% of the time")
    print(f"  · If you don't, test is negative 99% of the time")
    print(f"")
    print(f"  You test positive.")
    print(f"  What's the probability you actually have the disease?")
    print(f"")
    print(f"  Most people say: 99%.")
    print(f"  Let's find the real answer.")
    print(f"")

    p_sick       = 0.01
    p_pos_given_sick    = 0.99
    p_pos_given_healthy = 0.01

    p_pos = (p_pos_given_sick * p_sick +
             p_pos_given_healthy * (1 - p_sick))
    p_sick_given_pos = (p_pos_given_sick * p_sick) / p_pos

    print(f"  A = 'you have the disease'   P(A) = {p_sick}")
    print(f"  B = 'test is positive'")
    print(f"")
    print(f"  P(B|A)  = {p_pos_given_sick}   test catches it when you're sick")
    print(f"  P(B|Aᶜ) = {p_pos_given_healthy}   false positive rate")
    print(f"")
    print(f"  Step 1: compute P(B) — total probability of testing positive")
    print(f"  P(B) = P(B|A)·P(A) + P(B|Aᶜ)·P(Aᶜ)")
    print(f"       = {p_pos_given_sick}·{p_sick} + {p_pos_given_healthy}·{1-p_sick}")
    print(f"       = {p_pos_given_sick*p_sick:.4f} + {p_pos_given_healthy*(1-p_sick):.4f}")
    print(f"       = {p_pos:.4f}")
    print(f"")
    print(f"  Step 2: apply Bayes")
    print(f"  P(A|B) = P(B|A)·P(A) / P(B)")
    print(f"         = {p_pos_given_sick}·{p_sick} / {p_pos:.4f}")
    print(f"         = {p_pos_given_sick*p_sick:.4f} / {p_pos:.4f}")
    print(f"         = {p_sick_given_pos:.4f}  ≈  {p_sick_given_pos*100:.1f}%")
    print(f"")
    print(f"  Not 99%. About {p_sick_given_pos*100:.1f}%.")
    print(f"")
    print(f"  Why? Think about 10000 people:")
    print(f"  · ~100 are sick.   Test catches ~99 of them.")
    print(f"  · ~9900 are healthy. Test falsely flags ~99 of them.")
    print(f"  Among ~198 positive tests, only ~99 are truly sick.")
    print(f"  That's about 50% — not 99%.")
    print(f"")
    print(f"  The lesson: when the prior probability is low,")
    print(f"  even an accurate test produces many false positives.")
    print(f"  This is called the base rate fallacy —")
    print(f"  and it trips up doctors, journalists, and courts.")
    print(f"")

    print(f"--- Now try with your own values ---")
    pA   = float(input("  P(A) — prior: "))
    pBgA = float(input("  P(B|A) — likelihood: "))
    pB   = float(input("  P(B) — total probability of B: "))

    if not (0 <= pA <= 1 and 0 <= pBgA <= 1 and 0 < pB <= 1):
        print(f"  Invalid inputs.")
        return

    pAgB = pBgA * pA / pB

    print(f"\n--- Applying Bayes ---")
    print(f"  P(A|B) = P(B|A) · P(A) / P(B)")
    print(f"         = {pBgA} · {pA} / {pB}")
    print(f"         = {pBgA*pA:.4f} / {pB}")
    print(f"         = {pAgB:.4f}")
    print(f"")
    print(f"  Before evidence:  P(A)   = {pA:.4f}")
    print(f"  After evidence:   P(A|B) = {pAgB:.4f}")
    print(f"")
    if pAgB > pA:
        print(f"  Evidence B made A more likely.")
        print(f"  B supports A.")
    elif pAgB < pA:
        print(f"  Evidence B made A less likely.")
        print(f"  B works against A.")
    else:
        print(f"  Evidence B changed nothing.")
        print(f"  A and B are independent.")

    plot_bayes(pA, pAgB, pBgA)


def independent_events():
    print(f"\n{'='*50}")
    print(f"INDEPENDENT EVENTS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Two events are independent if knowing one happened")
    print(f"  tells you absolutely nothing about the other.")
    print(f"  The outcome of one doesn't influence the other at all.")
    print(f"")
    print(f"  Formal definition:")
    print(f"      A and B independent  ↔  P(A|B) = P(A)")
    print(f"")
    print(f"  Which is equivalent to — and easier to use:")
    print(f"      P(A ∩ B) = P(A) · P(B)")
    print(f"")
    print(f"  If you can just multiply the probabilities, they're independent.")
    print(f"  If the product doesn't match the actual P(A∩B), they're not.")
    print(f"")
    print(f"  Independent events:")
    print(f"  · Two separate coin flips — first flip can't affect second")
    print(f"  · Rolling two different dice")
    print(f"  · Drawing WITH replacement — deck resets each time")
    print(f"")
    print(f"  Dependent events:")
    print(f"  · Drawing WITHOUT replacement — second draw depends on first")
    print(f"  · Weather two days in a row — correlated")
    print(f"  · Studying hard and passing — clearly related")
    print(f"")
    print(f"  The connection to conditional probability:")
    print(f"  If A and B are independent:")
    print(f"  P(A|B) = P(A∩B)/P(B) = P(A)·P(B)/P(B) = P(A)")
    print(f"  Knowing B happened leaves P(A) completely unchanged.")
    print(f"  B carries zero information about A.")
    print(f"")

    pA    = float(input("  P(A): "))
    pB    = float(input("  P(B): "))
    pAinB = float(input("  P(A ∩ B) observed: "))

    if not (0 <= pA <= 1 and 0 <= pB <= 1 and 0 <= pAinB <= 1):
        print(f"  All probabilities must be between 0 and 1.")
        return
    if pAinB > min(pA, pB):
        print(f"  P(A∩B) can't exceed min(P(A), P(B)).")
        return

    expected = pA * pB

    print(f"\n--- Checking independence ---")
    print(f"  If A and B were independent:")
    print(f"  P(A∩B) should = P(A)·P(B) = {pA}·{pB} = {expected:.4f}")
    print(f"")
    print(f"  Observed P(A∩B)  = {pAinB:.4f}")
    print(f"  Expected P(A)·P(B) = {expected:.4f}")
    print(f"  Difference: {abs(pAinB - expected):.6f}")
    print(f"")

    if abs(pAinB - expected) < 1e-9:
        print(f"  P(A∩B) = P(A)·P(B) ✓")
        print(f"  A and B are INDEPENDENT.")
        print(f"  One tells you nothing about the other.")
    else:
        print(f"  P(A∩B) ≠ P(A)·P(B)")
        print(f"  A and B are DEPENDENT.")
        if pAinB > expected:
            print(f"  They occur together MORE than chance predicts.")
            print(f"  Positive dependence — one makes the other more likely.")
        else:
            print(f"  They avoid each other MORE than chance predicts.")
            print(f"  Negative dependence — one makes the other less likely.")

    print(f"\n--- Multiple independent events ---")
    print(f"  For independent events, probabilities multiply:")
    print(f"  P(A ∩ B ∩ C ∩ ...) = P(A) · P(B) · P(C) · ...")
    print(f"")
    print(f"  Watch how fast the product shrinks.")
    print(f"  Flip a coin 10 times: P(all heads) = (1/2)^10 = {0.5**10:.6f}")
    print(f"  That's roughly 1 in {int(1/0.5**10)}.")
    print(f"  Not impossible — just unlikely. Exponentially unlikely.")
    print(f"")

    n = int(input("  How many independent events to chain? "))
    probs = []
    for i in range(n):
        p = float(input(f"  P(event {i+1}): "))
        if not 0 <= p <= 1:
            print(f"  Invalid.")
            return
        probs.append(p)

    joint = 1
    print(f"\n--- Running product ---")
    print(f"  P(all) = " + " · ".join(str(p) for p in probs))
    for i, p in enumerate(probs):
        joint *= p
        print(f"  After event {i+1}: {joint:.8f}")

    print(f"")
    print(f"  P(all {n} events) = {joint:.8f}")
    print(f"")
    if joint < 0.01:
        print(f"  Less than 1% — small but not zero.")
        print(f"  Chaining independent events shrinks probability fast.")
        print(f"  This is why rare event chains are genuinely rare.")
    elif joint > 0.5:
        print(f"  Greater than 50% — more likely than not overall.")

    plot_independent(probs, joint)


def probability():
    print(f"\n{'='*50}")
    print(f"PROBABILITY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Probability is the mathematics of uncertainty.")
    print(f"  It takes vague words like 'probably' and 'unlikely'")
    print(f"  and replaces them with precise numbers between 0 and 1.")
    print(f"")
    print(f"  It started with gambling in the 1600s.")
    print(f"  Pascal and Fermat exchanged letters about dice games")
    print(f"  and accidentally built a new branch of mathematics.")
    print(f"  Today probability underpins statistics, machine learning,")
    print(f"  quantum mechanics, finance, and medicine.")
    print(f"")
    print(f"  The most interesting results are the counterintuitive ones:")
    print(f"  · Birthday paradox: 23 people → 50% chance two share a birthday")
    print(f"  · Monty Hall problem: switching doors doubles your odds")
    print(f"  · Bayes' paradox: a 99% accurate test can still be wrong")
    print(f"    most of the time when the disease is rare")
    print(f"")
    print(f"  Probability rewards careful, slow thinking.")
    print(f"  The quick intuitive answer is often wrong.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Classical and frequentist probability")
    print(f"  2 — Event operations  (complement, union, intersection)")
    print(f"  3 — Conditional probability")
    print(f"  4 — Bayes' theorem")
    print(f"  5 — Independent events")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        classical_probability()
    elif choice == "2":
        event_operations()
    elif choice == "3":
        conditional_probability()
    elif choice == "4":
        bayes_theorem()
    elif choice == "5":
        independent_events()
    else:
        print(f"  Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    probability()