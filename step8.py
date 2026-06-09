import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def draw_unit_circle(angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_val   = math.cos(angle_rad)
    sin_val   = math.sin(angle_rad)

    fig, ax = plt.subplots(figsize=(7, 7))

    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=1.5)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    ax.plot([0, cos_val], [0, sin_val], color="steelblue", linewidth=2,
            label=f"angle = {angle_deg}°")
    ax.plot(cos_val, sin_val, "o", color="steelblue", markersize=10)
    ax.annotate(f"  ({cos_val:.3f}, {sin_val:.3f})",
                (cos_val, sin_val), fontsize=10)

    ax.plot([0, cos_val], [0, 0], color="crimson", linewidth=2,
            linestyle="--", label=f"cos({angle_deg}°) = {cos_val:.4f}")
    ax.plot([cos_val, cos_val], [0, sin_val], color="green", linewidth=2,
            linestyle="--", label=f"sin({angle_deg}°) = {sin_val:.4f}")

    notable_angles = [0, 30, 45, 60, 90, 120, 135, 150,
                      180, 210, 225, 240, 270, 300, 315, 330]
    for a in notable_angles:
        r = math.radians(a)
        ax.plot(math.cos(r), math.sin(r), ".", color="gray", markersize=6)
        ax.annotate(f"{a}°", (math.cos(r)*1.12, math.sin(r)*1.12),
                    ha="center", va="center", fontsize=8, color="gray")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.set_title(f"Unit Circle — angle = {angle_deg}°", fontsize=14)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def explain_notable_values():
    print(f"\n{'='*50}")
    print(f"NOTABLE TRIGONOMETRIC VALUES")
    print(f"{'='*50}")
    print(f"")
    print(f"  Before memorizing a table, understand where it comes from.")
    print(f"  Every notable value traces back to two simple triangles.")
    print(f"")
    print(f"  Triangle 1 — the 45-45-90 triangle:")
    print(f"  Take a square with side 1 and cut it diagonally.")
    print(f"  The diagonal has length √2. The angles are 45-45-90.")
    print(f"  Divide everything by √2 to get a unit hypotenuse:")
    print(f"  sin(45°) = cos(45°) = 1/√2 = √2/2 ≈ 0.7071")
    print(f"")
    print(f"  Triangle 2 — the 30-60-90 triangle:")
    print(f"  Take an equilateral triangle with side 1 and cut it in half.")
    print(f"  You get a triangle with angles 30-60-90.")
    print(f"  sin(30°) = 1/2,  cos(30°) = √3/2")
    print(f"  sin(60°) = √3/2, cos(60°) = 1/2")
    print(f"")
    print(f"  Everything else follows from symmetry on the unit circle.")
    print(f"  Second quadrant: sin stays positive, cos flips sign.")
    print(f"  Third quadrant:  both flip sign.")
    print(f"  Fourth quadrant: cos stays positive, sin flips sign.")
    print(f"")

    angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]

    sin_exact = {0:"0", 30:"1/2", 45:"√2/2", 60:"√3/2",
                 90:"1", 120:"√3/2", 135:"√2/2", 150:"1/2",
                 180:"0", 270:"-1", 360:"0"}
    cos_exact = {0:"1", 30:"√3/2", 45:"√2/2", 60:"1/2",
                 90:"0", 120:"-1/2", 135:"-√2/2", 150:"-√3/2",
                 180:"-1", 270:"0", 360:"1"}
    tan_exact = {0:"0", 30:"√3/3", 45:"1", 60:"√3",
                 90:"∞", 120:"-√3", 135:"-1", 150:"-√3/3",
                 180:"0", 270:"∞", 360:"0"}

    print(f"  {'Angle':>8}  {'sin':>12}  {'cos':>12}  {'tan':>12}")
    print(f"  {'─'*48}")

    for deg in angles:
        rad   = math.radians(deg)
        s_str = sin_exact.get(deg, f"{math.sin(rad):.4f}")
        c_str = cos_exact.get(deg, f"{math.cos(rad):.4f}")
        t_str = tan_exact.get(deg, "∞")
        print(f"  {deg:>6}°    {s_str:>12}  {c_str:>12}  {t_str:>12}")

    print(f"")
    print(f"  Quick patterns worth noticing:")
    print(f"  · sin and cos are always between -1 and 1")
    print(f"  · sin(x) = cos(90° - x)  — they're complementary")
    print(f"  · tan = 1 exactly at 45° — the slope of a 45° line")
    print(f"  · wherever cos = 0, tan is undefined — vertical asymptote")
    print(f"")
    print(f"  Interesting fact: the word 'sine' comes from a mistranslation")
    print(f"  of the Arabic word 'jayb' (meaning pocket or fold) which was")
    print(f"  a translation of the Sanskrit word for half-chord.")
    print(f"  Mathematics traveled from India to Arabia to Europe,")
    print(f"  and the name got garbled along the way.")


def explain_identities():
    print(f"\n{'='*50}")
    print(f"TRIGONOMETRIC IDENTITIES")
    print(f"{'='*50}")
    print(f"")
    print(f"  An identity is true for every value of x — always.")
    print(f"  Not just sometimes, not just approximately. Always.")
    print(f"  These are the tools you reach for when an expression")
    print(f"  looks complicated and you need to simplify it.")
    print(f"")
    print(f"  The single most important one is the Pythagorean identity.")
    print(f"  Everything else can be derived from it.")
    print(f"")

    x = sp.Symbol('x')
    y = sp.Symbol('y')

    identities = [
        (
            "1. Pythagorean Identity — the foundation of everything",
            "sin²(x) + cos²(x) = 1",
            sp.sin(x)**2 + sp.cos(x)**2,
            "  This is literally the Pythagorean theorem on the unit circle.\n"
            "  The point (cos x, sin x) is always at distance 1 from the origin.\n"
            "  Distance formula: √(cos²x + sin²x) = 1 → cos²x + sin²x = 1.\n"
            "  From this one identity you can derive ALL the others.\n"
            "  It's the seed from which trigonometry grows."
        ),
        (
            "2. Sine Addition Formula",
            "sin(x+y) = sin(x)cos(y) + cos(x)sin(y)",
            sp.expand_trig(sp.sin(x + y)),
            "  When you sum two angles, the sine mixes both functions.\n"
            "  This isn't obvious — it takes a geometric proof to see why.\n"
            "  But once you have it, you can find sin of any sum of angles.\n"
            "  Setting y = x gives the double angle formula immediately."
        ),
        (
            "3. Cosine Addition Formula",
            "cos(x+y) = cos(x)cos(y) - sin(x)sin(y)",
            sp.expand_trig(sp.cos(x + y)),
            "  Notice the minus sign — that's the key difference from sine.\n"
            "  cos(x+y) is NOT cos(x) + cos(y). Not even close.\n"
            "  This trips up almost everyone the first time."
        ),
        (
            "4. Double Angle — Sine",
            "sin(2x) = 2·sin(x)·cos(x)",
            sp.expand_trig(sp.sin(2*x)),
            "  Just the addition formula with y = x.\n"
            "  sin(x+x) = sin(x)cos(x) + cos(x)sin(x) = 2sin(x)cos(x).\n"
            "  This appears constantly in integration — it lets you\n"
            "  split a product of sin and cos into a single function."
        ),
        (
            "5. Double Angle — Cosine",
            "cos(2x) = cos²(x) - sin²(x)",
            sp.expand_trig(sp.cos(2*x)),
            "  Three equivalent forms exist — all correct:\n"
            "  cos(2x) = cos²x - sin²x\n"
            "  cos(2x) = 2cos²x - 1       (use sin²x = 1 - cos²x)\n"
            "  cos(2x) = 1 - 2sin²x       (use cos²x = 1 - sin²x)\n"
            "  Which form you use depends on what you're trying to simplify."
        ),
        (
            "6. Tangent Identity",
            "tan(x) = sin(x) / cos(x)",
            sp.sin(x) / sp.cos(x),
            "  The definition of tangent — geometrically it's the slope\n"
            "  of the radius to the point (cos x, sin x) on the unit circle.\n"
            "  It's also the length of the tangent line from the circle\n"
            "  to the x-axis — that's where the name 'tangent' comes from."
        ),
    ]

    for name, formula, sympy_expr, explanation in identities:
        print(f"  {'─'*46}")
        print(f"  {name}")
        print(f"  {formula}")
        print(f"")
        print(f"  Verified symbolically: {sympy_expr}")
        print(f"")
        for line in explanation.split('\n'):
            print(f"  {line}")
        print(f"")

    print(f"  {'─'*46}")
    print(f"  A powerful habit: whenever you see sin² or cos²,")
    print(f"  think Pythagorean identity. Whenever you see a double")
    print(f"  angle, think addition formula with y = x.")
    print(f"  These two moves unlock most trigonometric problems.")


def plot_trig_functions():
    print(f"\n{'='*50}")
    print(f"GRAPHS OF TRIGONOMETRIC FUNCTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  sin(x) and cos(x) are the smoothest waves in mathematics.")
    print(f"  They're periodic — the same pattern repeats forever.")
    print(f"  This is why they describe anything that oscillates:")
    print(f"  sound, light, alternating current, pendulums, tides.")
    print(f"")
    print(f"  sin(x) and cos(x):")
    print(f"  · Period = 2π ≈ 6.28  (one full revolution of the circle)")
    print(f"  · Amplitude = 1       (max distance from the x-axis)")
    print(f"  · cos(x) = sin(x + π/2) — same wave, shifted left by π/2")
    print(f"")
    print(f"  tan(x):")
    print(f"  · Period = π  (half the period of sin and cos)")
    print(f"  · No amplitude — it goes to ±∞ at every asymptote")
    print(f"  · The asymptotes are where cos(x) = 0")
    print(f"")
    print(f"  Interesting fact: any periodic signal — a musical note,")
    print(f"  a radio wave, even a square wave — can be built by adding")
    print(f"  up sines and cosines at different frequencies.")
    print(f"  This is called Fourier analysis, and it's one of the most")
    print(f"  powerful ideas in all of applied mathematics.")
    print(f"")

    x_vals   = np.linspace(-2*np.pi, 2*np.pi, 1000)
    sin_vals = np.sin(x_vals)
    cos_vals = np.cos(x_vals)
    tan_vals = np.tan(x_vals)
    tan_vals[np.abs(tan_vals) > 10] = np.nan

    fig, axes = plt.subplots(3, 1, figsize=(10, 9))

    axes[0].plot(x_vals, sin_vals, color="crimson", linewidth=2)
    axes[0].set_title("f(x) = sin(x)  —  period = 2π,  amplitude = 1", fontsize=12)
    axes[0].axhline(0,  color="black", linewidth=0.8)
    axes[0].axhline(1,  color="gray",  linewidth=0.5, linestyle="--")
    axes[0].axhline(-1, color="gray",  linewidth=0.5, linestyle="--")
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].grid(True, alpha=0.3)
    axes[0].annotate("", xy=(2*np.pi, -1.3), xytext=(0, -1.3),
                     arrowprops=dict(arrowstyle="<->", color="black"))
    axes[0].text(np.pi, -1.45, "period = 2π", ha="center", fontsize=10)

    axes[1].plot(x_vals, cos_vals, color="steelblue", linewidth=2)
    axes[1].set_title("f(x) = cos(x)  —  period = 2π,  amplitude = 1", fontsize=12)
    axes[1].axhline(0,  color="black", linewidth=0.8)
    axes[1].axhline(1,  color="gray",  linewidth=0.5, linestyle="--")
    axes[1].axhline(-1, color="gray",  linewidth=0.5, linestyle="--")
    axes[1].set_ylim(-1.5, 1.5)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(x_vals, tan_vals, color="green", linewidth=2)
    axes[2].set_title("f(x) = tan(x)  —  period = π,  vertical asymptotes at π/2 + kπ", fontsize=12)
    axes[2].axhline(0, color="black", linewidth=0.8)
    axes[2].set_ylim(-5, 5)
    axes[2].grid(True, alpha=0.3)

    ticks  = [-2*np.pi, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 2*np.pi]
    labels = ["-2π", "-π", "-π/2", "0", "π/2", "π", "2π"]
    for ax in axes:
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)

    plt.tight_layout()
    plt.show()


def solve_trig_equation():
    print(f"\n{'='*50}")
    print(f"TRIGONOMETRIC EQUATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Here's what makes trig equations different from")
    print(f"  everything else we've solved so far:")
    print(f"  they always have infinitely many solutions.")
    print(f"  Because sin, cos, and tan are periodic, every solution")
    print(f"  repeats forever — shifted by the period each time.")
    print(f"")
    print(f"  The strategy is always the same:")
    print(f"  1. Find the reference angle in the standard range")
    print(f"  2. Use symmetry to find all solutions in [0, 2π]")
    print(f"  3. Add multiples of the period to get every solution")
    print(f"")
    print(f"  What type of equation do you want to solve?")
    print(f"  1 — sin(x) = k")
    print(f"  2 — cos(x) = k")
    print(f"  3 — tan(x) = k")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")
    k = float(input("  Enter k: "))

    if choice == "1":
        print(f"\n  Solving sin(x) = {k}")
        print(f"")

        if abs(k) > 1:
            print(f"  No solution.")
            print(f"  sin(x) is always between -1 and 1 — that's its range.")
            print(f"  k = {k} is outside this range, so no angle can give it.")
            return

        print(f"--- Step 1: Find the reference angle ---")
        print(f"  The reference angle x₀ = arcsin({k}) is the angle")
        print(f"  in [-π/2, π/2] whose sine equals {k}.")
        print(f"  It's the 'base' solution — everything else comes from it.")
        print(f"")
        x0 = math.asin(k)
        print(f"  x₀ = arcsin({k}) = {x0:.4f} rad = {math.degrees(x0):.2f}°")

        print(f"\n--- Step 2: Use symmetry to find all solutions in [0, 2π] ---")
        print(f"  sin is positive in quadrants 1 and 2.")
        print(f"  sin is negative in quadrants 3 and 4.")
        print(f"  The sine curve is symmetric about x = π/2,")
        print(f"  so if x₀ is one solution, then π - x₀ is another.")
        print(f"")

        x1 = x0 if x0 >= 0 else x0 + 2*math.pi
        x2 = math.pi - x0 if math.pi - x0 >= 0 else math.pi - x0 + 2*math.pi

        print(f"  x₁ = {x1:.4f} rad = {math.degrees(x1):.2f}°")
        print(f"  x₂ = π - ({x0:.4f}) = {x2:.4f} rad = {math.degrees(x2):.2f}°")

        print(f"\n--- Step 3: General solution ---")
        print(f"  sin repeats every 2π — add 2kπ to each solution:")
        print(f"")
        print(f"  x = {x1:.4f} + 2kπ   (k = 0, ±1, ±2, ...)")
        print(f"  x = {x2:.4f} + 2kπ   (k = 0, ±1, ±2, ...)")
        print(f"")
        print(f"  In degrees:")
        print(f"  x = {math.degrees(x1):.2f}° + 360°k")
        print(f"  x = {math.degrees(x2):.2f}° + 360°k")
        print(f"")
        print(f"  Let's verify: sin({x1:.4f}) = {math.sin(x1):.6f} ✓")
        print(f"               sin({x2:.4f}) = {math.sin(x2):.6f} ✓")

        plot_trig_equation("sin", k, [x1, x2])

    elif choice == "2":
        print(f"\n  Solving cos(x) = {k}")
        print(f"")

        if abs(k) > 1:
            print(f"  No solution.")
            print(f"  cos(x) is always between -1 and 1.")
            print(f"  k = {k} is outside this range.")
            return

        print(f"--- Step 1: Find the reference angle ---")
        print(f"  x₀ = arccos({k}) — the angle in [0, π] whose cosine equals {k}.")
        print(f"")
        x0 = math.acos(k)
        print(f"  x₀ = {x0:.4f} rad = {math.degrees(x0):.2f}°")

        print(f"\n--- Step 2: Use symmetry to find all solutions in [0, 2π] ---")
        print(f"  cos is symmetric about x = 0 (the y-axis).")
        print(f"  If x₀ is one solution, then -x₀ (or equivalently 2π-x₀) is another.")
        print(f"")

        x1 = x0
        x2 = 2*math.pi - x0

        print(f"  x₁ = {x1:.4f} rad = {math.degrees(x1):.2f}°")
        print(f"  x₂ = 2π - {x0:.4f} = {x2:.4f} rad = {math.degrees(x2):.2f}°")

        print(f"\n--- Step 3: General solution ---")
        print(f"  cos repeats every 2π:")
        print(f"")
        print(f"  x = ±{x1:.4f} + 2kπ   (k = 0, ±1, ±2, ...)")
        print(f"")
        print(f"  Or written separately:")
        print(f"  x = {x1:.4f} + 2kπ")
        print(f"  x = {x2:.4f} + 2kπ")
        print(f"")
        print(f"  Let's verify: cos({x1:.4f}) = {math.cos(x1):.6f} ✓")
        print(f"               cos({x2:.4f}) = {math.cos(x2):.6f} ✓")

        plot_trig_equation("cos", k, [x1, x2])

    elif choice == "3":
        print(f"\n  Solving tan(x) = {k}")
        print(f"")
        print(f"  Unlike sin and cos, tan has no restricted range —")
        print(f"  it takes every real value. So there's always a solution.")
        print(f"")
        print(f"--- Step 1: Find the reference angle ---")
        print(f"  x₀ = arctan({k}) — gives the angle in (-π/2, π/2).")
        print(f"")
        x0 = math.atan(k)
        print(f"  x₀ = {x0:.4f} rad = {math.degrees(x0):.2f}°")

        print(f"\n--- Step 2: General solution ---")
        print(f"  tan repeats every π — half the period of sin and cos.")
        print(f"  Why? Because tan = sin/cos, and after π the ratio repeats.")
        print(f"  So there is only ONE family of solutions:")
        print(f"")
        print(f"  x = {x0:.4f} + kπ   (k = 0, ±1, ±2, ...)")
        print(f"")
        print(f"  In degrees: x = {math.degrees(x0):.2f}° + 180°k")
        print(f"")
        print(f"  Let's verify: tan({x0:.4f}) = {math.tan(x0):.6f} ✓")

        plot_trig_equation("tan", k, [x0])

    else:
        print(f"  Invalid choice.")


def plot_trig_equation(func, k, solutions):
    x_vals = np.linspace(-2*np.pi, 2*np.pi, 1000)

    if func == "sin":
        y_vals = np.sin(x_vals)
        color  = "crimson"
        title  = f"sin(x) = {k}  —  solutions marked in orange"
    elif func == "cos":
        y_vals = np.cos(x_vals)
        color  = "steelblue"
        title  = f"cos(x) = {k}  —  solutions marked in orange"
    else:
        y_vals = np.tan(x_vals)
        y_vals[np.abs(y_vals) > 10] = np.nan
        color  = "green"
        title  = f"tan(x) = {k}  —  solutions marked in orange"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_vals, y_vals, color=color, linewidth=2, label=f"{func}(x)")
    ax.axhline(k, color="black", linewidth=1.5, linestyle="--",
               label=f"y = {k}")

    for s in solutions:
        ax.plot(s, k, "o", color="orange", markersize=10)
        ax.annotate(f"  {s:.2f} rad\n  {math.degrees(s):.1f}°",
                    (s, k), fontsize=9)

    ax.set_ylim(-3, 3) if func != "tan" else ax.set_ylim(-5, 5)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("x (radians)")
    ax.set_ylabel(f"{func}(x)")

    ticks  = [-2*np.pi, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 2*np.pi]
    labels = ["-2π", "-π", "-π/2", "0", "π/2", "π", "2π"]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)

    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def trigonometry():
    print(f"\n{'='*50}")
    print(f"TRIGONOMETRY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Trigonometry started as the mathematics of triangles —")
    print(f"  a tool for astronomers and navigators who needed to")
    print(f"  measure distances they couldn't walk.")
    print(f"  Over time it became something much deeper:")
    print(f"  the language of waves, oscillations, and cycles.")
    print(f"")
    print(f"  Sound is a wave. Light is a wave. Alternating current")
    print(f"  is a wave. The seasons are a cycle. The tides are a cycle.")
    print(f"  Wherever something repeats, trigonometry is there.")
    print(f"")
    print(f"  At the heart of it all: the unit circle.")
    print(f"  One circle, radius 1, and it explains everything.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Unit circle         visualize any angle")
    print(f"  2 — Notable values      the angles every mathematician knows")
    print(f"  3 — Identities          the tools for simplification")
    print(f"  4 — Graphs              sin, cos, tan as waves")
    print(f"  5 — Equations           solve sin(x)=k, cos(x)=k, tan(x)=k")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        deg = float(input("  Enter an angle in degrees: "))
        draw_unit_circle(deg)
    elif choice == "2":
        explain_notable_values()
    elif choice == "3":
        explain_identities()
    elif choice == "4":
        plot_trig_functions()
    elif choice == "5":
        solve_trig_equation()
    else:
        print(f"  Invalid choice. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    trigonometry()
    