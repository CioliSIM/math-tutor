import math
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy as np


def plot_parametric(x_vals, y_vals, title,
                    color="crimson", point_start=True, point_end=True):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(x_vals, y_vals, color=color, linewidth=2)

    if point_start:
        ax.plot(x_vals[0], y_vals[0], "o", color="green",
                markersize=10,
                label=f"Start ({x_vals[0]:.2f}, {y_vals[0]:.2f})")
    if point_end:
        ax.plot(x_vals[-1], y_vals[-1], "s", color="steelblue",
                markersize=10,
                label=f"End ({x_vals[-1]:.2f}, {y_vals[-1]:.2f})")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def parametric_line():
    print(f"\n{'='*50}")
    print(f"LINE IN PARAMETRIC FORM")
    print(f"{'='*50}")
    print(f"")
    print(f"  A line can be described as a starting point")
    print(f"  plus a direction you move in:")
    print(f"")
    print(f"      x(t) = x₀ + a·t")
    print(f"      y(t) = y₀ + b·t")
    print(f"")
    print(f"  Think of t as time.")
    print(f"  At t=0 you're at (x₀, y₀) — your starting point.")
    print(f"  (a, b) is your direction — how fast you move")
    print(f"  horizontally and vertically.")
    print(f"  As t grows you move forward. Negative t goes backward.")
    print(f"")
    print(f"  The slope in Cartesian form is m = b/a.")
    print(f"")
    print(f"  Why bother with parametric form for a line?")
    print(f"  · Vertical lines (a=0) are impossible with y=mx+q")
    print(f"  · You know WHERE you are at every moment")
    print(f"  · It extends naturally to 3D — same idea, one more equation")
    print(f"")

    x0 = float(input("  Starting point x₀: "))
    y0 = float(input("  Starting point y₀: "))
    a  = float(input("  Direction a (horizontal): "))
    b  = float(input("  Direction b (vertical): "))

    print(f"\n--- The parametric line ---")
    print(f"  x(t) = {x0} + {a}·t")
    print(f"  y(t) = {y0} + {b}·t")

    print(f"\n--- Eliminating the parameter ---")
    print(f"  We want to find the Cartesian equation y = f(x).")
    print(f"  Strategy: isolate t from one equation, substitute into the other.")
    print(f"")
    if a != 0:
        print(f"  From x(t): t = (x - {x0}) / {a}")
        print(f"  Substitute into y(t):")
        m = b / a
        q = y0 - m*x0
        print(f"  y = {y0} + {b} · (x - {x0}) / {a}")
        print(f"  y = {m}x + {q:.4f}")
        print(f"")
        print(f"  Cartesian form: y = {m}x + {q:.4f}")
    elif a == 0 and b != 0:
        print(f"  a = 0 → x = {x0} for all t.")
        print(f"  This is a vertical line — impossible to write as y=mx+q.")
        print(f"  Parametric form handles it naturally.")
    else:
        print(f"  Both a and b are 0 — this is just a point, not a line.")

    print(f"\n--- Points at specific t values ---")
    print(f"  {'t':>8}  {'x':>10}  {'y':>10}")
    print(f"  {'─'*32}")
    for t_val in [-2, -1, 0, 1, 2, 3]:
        xv = x0 + a*t_val
        yv = y0 + b*t_val
        print(f"  {t_val:>8}  {xv:>10.4f}  {yv:>10.4f}")

    t_vals = np.linspace(-5, 5, 400)
    x_vals = x0 + a*t_vals
    y_vals = y0 + b*t_vals
    plot_parametric(x_vals, y_vals,
                    title=f"Line: x={x0}+{a}t,  y={y0}+{b}t")


def parametric_conics():
    print(f"\n{'='*50}")
    print(f"CIRCLE AND ELLIPSE")
    print(f"{'='*50}")
    print(f"")
    print(f"  The circle is where parametric equations truly shine.")
    print(f"")
    print(f"  In Cartesian form: x² + y² = r²")
    print(f"  You know the shape — but not how to move along it.")
    print(f"")
    print(f"  In parametric form:")
    print(f"      x(t) = r·cos(t)")
    print(f"      y(t) = r·sin(t)    t ∈ [0, 2π]")
    print(f"  Now t is the angle — at each t you know exactly")
    print(f"  where you are on the circle.")
    print(f"")
    print(f"  The ellipse is a stretched circle:")
    print(f"      x(t) = a·cos(t)")
    print(f"      y(t) = b·sin(t)")
    print(f"  a stretches horizontally, b vertically.")
    print(f"  When a = b you get a circle. Simple.")
    print(f"")
    print(f"  Which curve?")
    print(f"  1 — Circle")
    print(f"  2 — Ellipse")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        cx = float(input("  Center x: "))
        cy = float(input("  Center y: "))
        r  = float(input("  Radius r: "))

        t_vals = np.linspace(0, 2*np.pi, 400)
        x_vals = cx + r*np.cos(t_vals)
        y_vals = cy + r*np.sin(t_vals)

        print(f"\n--- Circle ---")
        print(f"  x(t) = {cx} + {r}·cos(t)")
        print(f"  y(t) = {cy} + {r}·sin(t)    t ∈ [0, 2π]")

        print(f"\n--- Eliminating the parameter ---")
        print(f"  cos(t) = (x - {cx}) / {r}")
        print(f"  sin(t) = (y - {cy}) / {r}")
        print(f"  Use the Pythagorean identity: cos²t + sin²t = 1")
        print(f"  ((x-{cx})/{r})² + ((y-{cy})/{r})² = 1")
        print(f"  (x-{cx})² + (y-{cy})² = {r**2}")
        print(f"")
        print(f"  Cartesian form confirmed ✓")
        print(f"  The identity cos²+sin²=1 is exactly what makes")
        print(f"  the circle possible — geometry and algebra unified.")

        plot_parametric(x_vals, y_vals,
                        title=f"Circle: center=({cx},{cy}),  r={r}")

    elif choice == "2":
        cx = float(input("  Center x: "))
        cy = float(input("  Center y: "))
        a  = float(input("  Semi-axis a (horizontal): "))
        b  = float(input("  Semi-axis b (vertical): "))

        t_vals = np.linspace(0, 2*np.pi, 400)
        x_vals = cx + a*np.cos(t_vals)
        y_vals = cy + b*np.sin(t_vals)

        print(f"\n--- Ellipse ---")
        print(f"  x(t) = {cx} + {a}·cos(t)")
        print(f"  y(t) = {cy} + {b}·sin(t)    t ∈ [0, 2π]")

        print(f"\n--- Eliminating the parameter ---")
        print(f"  cos(t) = (x-{cx})/{a}  →  cos²t = (x-{cx})²/{a**2}")
        print(f"  sin(t) = (y-{cy})/{b}  →  sin²t = (y-{cy})²/{b**2}")
        print(f"  cos²t + sin²t = 1:")
        print(f"  (x-{cx})²/{a**2} + (y-{cy})²/{b**2} = 1")
        print(f"")
        print(f"  Standard ellipse equation ✓")

        area = math.pi * a * b
        print(f"\n--- Properties ---")
        print(f"  Semi-axes: a={a} (horizontal), b={b} (vertical)")
        print(f"  Area = π·a·b = {area:.4f}")
        print(f"  When a=b, area = πr² — the circle area. ✓")

        if a != b:
            c = math.sqrt(abs(a**2 - b**2))
            e = c / max(a, b)
            longer = "horizontal" if a > b else "vertical"
            print(f"  Foci along the {longer} axis: c = {c:.4f}")
            print(f"  Eccentricity e = c/max(a,b) = {e:.4f}")
            print(f"  (e=0 is a circle, e→1 is very flat)")

        plot_parametric(x_vals, y_vals,
                        title=f"Ellipse: a={a},  b={b}")
    else:
        print(f"  Invalid choice.")


def cycloid_and_spirals():
    print(f"\n{'='*50}")
    print(f"CYCLOIDS AND SPIRALS")
    print(f"{'='*50}")
    print(f"")
    print(f"  These are curves that Cartesian equations can't describe")
    print(f"  easily — but parametric equations handle naturally.")
    print(f"")
    print(f"  1 — Cycloid           (the fastest descent curve)")
    print(f"  2 — Archimedean spiral")
    print(f"  3 — Lissajous figures (two oscillations combined)")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        print(f"\n{'='*50}")
        print(f"THE CYCLOID")
        print(f"{'='*50}")
        print(f"")
        print(f"  Imagine marking a point on the rim of a bicycle tire.")
        print(f"  As the wheel rolls along the ground, that point")
        print(f"  traces a curve. That curve is the cycloid.")
        print(f"")
        print(f"      x(t) = r·(t - sin(t))")
        print(f"      y(t) = r·(1 - cos(t))")
        print(f"")
        print(f"  t is the angle the wheel has rotated.")
        print(f"  When t=0 the point is on the ground.")
        print(f"  When t=π it's at the top of the wheel.")
        print(f"  When t=2π it's back on the ground — one arch completed.")
        print(f"")
        print(f"  The cycloid is historically famous for two reasons:")
        print(f"")
        print(f"  1. THE BRACHISTOCHRONE PROBLEM (1696):")
        print(f"     'What is the fastest path for a ball to slide")
        print(f"      from A to B under gravity?'")
        print(f"     Intuition says: straight line.")
        print(f"     Mathematics says: cycloid arc.")
        print(f"     The ball goes faster by curving down steeply first.")
        print(f"     Johann Bernoulli posed the problem.")
        print(f"     Newton solved it overnight — anonymously.")
        print(f"     Bernoulli recognized the solution: 'I know the lion")
        print(f"     by his paw.'")
        print(f"")
        print(f"  2. THE TAUTOCHRONE PROPERTY:")
        print(f"     A ball released from ANY point on a cycloid arc")
        print(f"     reaches the bottom in EXACTLY the same time.")
        print(f"     No matter the starting height. Always.")
        print(f"     Huygens used this to build more accurate pendulum clocks.")
        print(f"")

        r      = float(input("  Circle radius r: "))
        n_arch = int(input("  Number of arches: "))

        t_vals = np.linspace(0, 2*np.pi*n_arch, 1000*n_arch)
        x_vals = r * (t_vals - np.sin(t_vals))
        y_vals = r * (1 - np.cos(t_vals))

        print(f"\n--- Properties ---")
        print(f"  Arc length of one arch = 8r = {8*r:.4f}")
        print(f"  Area under one arch    = 3πr² = {3*math.pi*r**2:.4f}")
        print(f"  That's exactly three times the area of the rolling circle.")
        print(f"  A remarkable result — discovered by Torricelli in 1644.")

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(x_vals, y_vals, color="crimson", linewidth=2,
                label=f"Cycloid (r={r})")

        for t_pos in np.linspace(np.pi*0.5, 2*np.pi*n_arch - np.pi*0.5, 4):
            cx    = r * (t_pos - math.sin(t_pos))
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(cx + r*np.cos(theta), r + r*np.sin(theta),
                    color="steelblue", linewidth=0.8, alpha=0.35)
            px = r * (t_pos - math.sin(t_pos))
            py = r * (1 - math.cos(t_pos))
            ax.plot(px, py, "o", color="steelblue", markersize=6)

        ax.axhline(0, color="black", linewidth=1.2)
        ax.set_aspect("equal")
        ax.set_title(f"Cycloid — the brachistochrone  (r={r})", fontsize=13)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        print(f"\n{'='*50}")
        print(f"ARCHIMEDEAN SPIRAL")
        print(f"{'='*50}")
        print(f"")
        print(f"  The Archimedean spiral unwinds at a constant rate.")
        print(f"  Each full turn adds exactly the same distance outward.")
        print(f"")
        print(f"      x(t) = a·t·cos(t)")
        print(f"      y(t) = a·t·sin(t)")
        print(f"")
        print(f"  a controls how spread out the spiral is.")
        print(f"  Large a → wide spacing. Small a → tight coils.")
        print(f"")
        print(f"  You see it in:")
        print(f"  · A coiled rope or garden hose")
        print(f"  · A rolled-up paper")
        print(f"  · The groove of a vinyl record")
        print(f"  · Certain shells and fossils")
        print(f"")

        a     = float(input("  Growth rate a: "))
        turns = float(input("  Number of turns: "))

        t_vals = np.linspace(0, 2*np.pi*turns, 1000)
        x_vals = a * t_vals * np.cos(t_vals)
        y_vals = a * t_vals * np.sin(t_vals)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x_vals, y_vals, color="crimson", linewidth=2,
                label=f"Archimedean spiral (a={a})")
        ax.plot(0, 0, "o", color="black", markersize=8)
        ax.set_aspect("equal")
        ax.set_title(f"Archimedean Spiral  (a={a},  {turns} turns)",
                     fontsize=13)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    elif choice == "3":
        print(f"\n{'='*50}")
        print(f"LISSAJOUS FIGURES")
        print(f"{'='*50}")
        print(f"")
        print(f"  What happens when you combine two sine waves")
        print(f"  oscillating at different frequencies?")
        print(f"  You get a Lissajous figure.")
        print(f"")
        print(f"      x(t) = A·sin(a·t + δ)")
        print(f"      y(t) = B·sin(b·t)")
        print(f"")
        print(f"  The ratio a:b determines the shape.")
        print(f"  The phase δ rotates and distorts it.")
        print(f"")
        print(f"  If a:b is a simple ratio (1:1, 2:1, 3:2 ...)")
        print(f"  the curve closes and repeats — a clean figure.")
        print(f"  If irrational, it never closes and fills a rectangle.")
        print(f"")
        print(f"  These appear on oscilloscopes in electronics labs.")
        print(f"  Engineers use them to compare signal frequencies.")
        print(f"  The shape immediately tells you the frequency ratio.")
        print(f"")

        A     = float(input("  Amplitude A: "))
        B     = float(input("  Amplitude B: "))
        a     = float(input("  Frequency a: "))
        b     = float(input("  Frequency b: "))
        delta = float(input("  Phase shift δ (e.g. 0, π/4≈0.785, π/2≈1.571): "))

        t_vals = np.linspace(0, 6*np.pi, 3000)
        x_vals = A * np.sin(a*t_vals + delta)
        y_vals = B * np.sin(b*t_vals)

        ratio = a/b if b != 0 else float('inf')
        print(f"\n  Frequency ratio a:b = {a}:{b} = {ratio:.4f}")
        frac = ratio
        is_simple = abs(round(frac) - frac) < 0.02 or \
                    any(abs(frac - p/q) < 0.02
                        for p in range(1,10) for q in range(1,10))
        if is_simple:
            print(f"  Simple ratio → closed curve that repeats.")
        else:
            print(f"  Irrational ratio → curve never closes,")
            print(f"  eventually fills the {2*A}×{2*B} rectangle.")

        points   = np.array([x_vals, y_vals]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc       = mc.LineCollection(segments,
                                     cmap="plasma",
                                     linewidth=1.5, alpha=0.8)
        lc.set_array(np.linspace(0, 1, len(segments)))

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.add_collection(lc)
        ax.set_xlim(-A-0.3, A+0.3)
        ax.set_ylim(-B-0.3, B+0.3)
        ax.set_aspect("equal")
        ax.set_title(f"Lissajous figure  (a={a}, b={b}, δ={delta:.3f})",
                     fontsize=13)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    else:
        print(f"  Invalid choice.")


def projectile_motion():
    print(f"\n{'='*50}")
    print(f"PROJECTILE MOTION")
    print(f"{'='*50}")
    print(f"")
    print(f"  A ball thrown through the air moves in two ways:")
    print(f"  horizontally at constant speed — nothing pushes it sideways.")
    print(f"  vertically slowing down then speeding up — gravity pulls it down.")
    print(f"  These two motions are completely independent.")
    print(f"  Parametric equations capture this perfectly.")
    print(f"")
    print(f"      x(t) = v₀·cos(α)·t")
    print(f"      y(t) = h₀ + v₀·sin(α)·t - ½·g·t²")
    print(f"")
    print(f"  v₀ = launch speed")
    print(f"  α  = launch angle")
    print(f"  h₀ = initial height")
    print(f"  g  = 9.81 m/s²")
    print(f"  t  = time")
    print(f"")
    print(f"  Eliminating t gives a parabola — connecting back")
    print(f"  to Module 9 (analytic geometry).")
    print(f"")

    v0    = float(input("  Launch speed v₀ (m/s): "))
    alpha = float(input("  Launch angle α (degrees): "))
    h0    = float(input("  Initial height h₀ (m, 0 if from ground): "))
    g     = 9.81

    alpha_rad = math.radians(alpha)
    vx        = v0 * math.cos(alpha_rad)
    vy        = v0 * math.sin(alpha_rad)

    discriminant = vy**2 + 2*g*h0
    t_flight     = (vy + math.sqrt(discriminant)) / g

    t_vals = np.linspace(0, t_flight, 500)
    x_vals = vx * t_vals
    y_vals = h0 + vy*t_vals - 0.5*g*t_vals**2
    y_vals = np.maximum(y_vals, 0)

    t_max  = vy / g
    x_max  = vx * t_max
    y_max  = h0 + vy*t_max - 0.5*g*t_max**2
    x_land = vx * t_flight

    print(f"\n--- Equations of motion ---")
    print(f"  x(t) = {vx:.4f}·t")
    print(f"  y(t) = {h0} + {vy:.4f}t - {0.5*g:.4f}t²")
    print(f"")
    print(f"  Horizontal speed: {vx:.4f} m/s  (constant throughout)")
    print(f"  Initial vertical: {vy:.4f} m/s  (decreases due to gravity)")

    print(f"\n--- Key values ---")
    print(f"  Time in the air:  {t_flight:.4f} s")
    print(f"  Time to peak:     {t_max:.4f} s")
    print(f"  Maximum height:   {y_max:.4f} m  at x = {x_max:.4f} m")
    print(f"  Horizontal range: {x_land:.4f} m")

    print(f"\n--- Eliminating the parameter ---")
    print(f"  From x(t) = {vx:.4f}·t  →  t = x / {vx:.4f}")
    print(f"  Substitute into y(t):")
    A_c = -0.5*g / vx**2
    B_c =  vy / vx
    print(f"  y = {A_c:.6f}·x² + {B_c:.4f}·x + {h0}")
    print(f"  This is a downward parabola — as expected. ✓")

    print(f"\n--- Optimal launch angle ---")
    print(f"  For maximum range from flat ground (h₀=0):")
    print(f"  Range = v₀²·sin(2α)/g  →  maximized when sin(2α)=1  →  α=45°")
    range_current = v0**2 * math.sin(2*alpha_rad) / g
    range_optimal = v0**2 / g
    print(f"  Your range at {alpha}°: {range_current:.4f} m")
    print(f"  Optimal at 45°:         {range_optimal:.4f} m")
    if abs(alpha - 45) > 1:
        print(f"  You're leaving {range_optimal-range_current:.4f} m on the table.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(x_vals, y_vals, color="crimson", linewidth=2.5,
                 label=f"α={alpha}°,  v₀={v0} m/s")
    axes[0].plot(0, h0, "o", color="green", markersize=12,
                 label=f"Launch (0, {h0})")
    axes[0].plot(x_max, y_max, "^", color="steelblue", markersize=12,
                 label=f"Peak ({x_max:.1f}, {y_max:.1f})")
    axes[0].plot(x_land, 0, "s", color="orange", markersize=12,
                 label=f"Landing ({x_land:.1f}, 0)")
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_title("Projectile trajectory", fontsize=12)
    axes[0].set_xlabel("x (m)")
    axes[0].set_ylabel("y (m)")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    angles = np.linspace(0, 90, 200)
    ranges = v0**2 * np.sin(2*np.radians(angles)) / g
    axes[1].plot(angles, ranges, color="steelblue", linewidth=2)
    axes[1].axvline(45, color="crimson", linewidth=1.5,
                    linestyle="--", label="Optimal 45°")
    axes[1].axvline(alpha, color="green", linewidth=1.5,
                    linestyle="--", label=f"Your angle {alpha}°")
    axes[1].set_title("Range vs launch angle", fontsize=12)
    axes[1].set_xlabel("Launch angle (degrees)")
    axes[1].set_ylabel("Range (m)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Projectile Motion — Parametric Equations",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def eliminate_parameter():
    print(f"\n{'='*50}")
    print(f"ELIMINATING THE PARAMETER")
    print(f"{'='*50}")
    print(f"")
    print(f"  Sometimes you have a parametric curve and want")
    print(f"  to find the Cartesian equation — a direct relation")
    print(f"  between x and y without t.")
    print(f"")
    print(f"  The strategy depends on the form of x(t) and y(t):")
    print(f"")
    print(f"  · Linear in t:")
    print(f"    isolate t from one equation, substitute into the other")
    print(f"")
    print(f"  · sin(t) and cos(t):")
    print(f"    isolate them, then use cos²t + sin²t = 1")
    print(f"")
    print(f"  Choose an example:")
    print(f"  1 — Parabola   x=at², y=t")
    print(f"  2 — Circle     x=r·cos(t), y=r·sin(t)")
    print(f"  3 — Line       x=x₀+at, y=y₀+bt")
    print(f"  4 — Ellipse    x=a·cos(t), y=b·sin(t)")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        a = float(input("  Coefficient a in x=at²: "))
        print(f"\n  Parametric: x = {a}t²,  y = t")
        print(f"")
        print(f"  Step 1: from y = t, we get t = y  (immediate)")
        print(f"  Step 2: substitute into x = {a}t²:")
        print(f"  x = {a}·y²")
        print(f"")
        print(f"  Cartesian: x = {a}y²")
        print(f"  Horizontal parabola, vertex at origin,")
        print(f"  opening {'right' if a > 0 else 'left'}.")

        t_vals = np.linspace(-3, 3, 400)
        x_vals = a * t_vals**2
        y_vals = t_vals
        plot_parametric(x_vals, y_vals,
                        title=f"Parabola: x={a}t², y=t  →  x={a}y²")

    elif choice == "2":
        r = float(input("  Radius r: "))
        print(f"\n  Parametric: x = {r}·cos(t),  y = {r}·sin(t)")
        print(f"")
        print(f"  Step 1: isolate cos and sin:")
        print(f"  cos(t) = x/{r},   sin(t) = y/{r}")
        print(f"")
        print(f"  Step 2: Pythagorean identity cos²t + sin²t = 1:")
        print(f"  (x/{r})² + (y/{r})² = 1")
        print(f"  x² + y² = {r**2}")
        print(f"")
        print(f"  Cartesian: x² + y² = {r**2}  ✓")
        print(f"  Circle with radius {r}.")

        t_vals = np.linspace(0, 2*np.pi, 400)
        x_vals = r * np.cos(t_vals)
        y_vals = r * np.sin(t_vals)
        plot_parametric(x_vals, y_vals,
                        title=f"Circle: x={r}cos(t), y={r}sin(t)  →  x²+y²={r**2}")

    elif choice == "3":
        x0 = float(input("  x₀: "))
        y0 = float(input("  y₀: "))
        a  = float(input("  a: "))
        b  = float(input("  b: "))
        print(f"\n  Parametric: x = {x0}+{a}t,  y = {y0}+{b}t")
        print(f"")
        if a != 0:
            print(f"  Step 1: from x = {x0}+{a}t:")
            print(f"  t = (x - {x0}) / {a}")
            print(f"")
            print(f"  Step 2: substitute into y:")
            m = b / a
            q = y0 - m*x0
            print(f"  y = {y0} + {b}·(x-{x0})/{a}")
            print(f"  y = {m}x + {q:.4f}")
            print(f"")
            print(f"  Cartesian: y = {m}x + {q:.4f}  ✓")
        else:
            print(f"  a=0 → x = {x0} for all t.")
            print(f"  Vertical line — no Cartesian slope form possible.")

        t_vals = np.linspace(-5, 5, 400)
        x_vals = x0 + a*t_vals
        y_vals = y0 + b*t_vals
        plot_parametric(x_vals, y_vals,
                        title=f"Line: x={x0}+{a}t, y={y0}+{b}t")

    elif choice == "4":
        a = float(input("  Semi-axis a: "))
        b = float(input("  Semi-axis b: "))
        print(f"\n  Parametric: x = {a}·cos(t),  y = {b}·sin(t)")
        print(f"")
        print(f"  Step 1: isolate cos and sin:")
        print(f"  cos(t) = x/{a},   sin(t) = y/{b}")
        print(f"")
        print(f"  Step 2: Pythagorean identity:")
        print(f"  (x/{a})² + (y/{b})² = 1")
        print(f"  x²/{a**2} + y²/{b**2} = 1")
        print(f"")
        print(f"  Standard ellipse equation ✓")

        t_vals = np.linspace(0, 2*np.pi, 400)
        x_vals = a * np.cos(t_vals)
        y_vals = b * np.sin(t_vals)
        plot_parametric(x_vals, y_vals,
                        title=f"Ellipse: x={a}cos(t), y={b}sin(t)  →  x²/{a**2}+y²/{b**2}=1")

    else:
        print(f"  Invalid choice.")


def parametric_equations():
    print(f"\n{'='*50}")
    print(f"PARAMETRIC EQUATIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A Cartesian equation tells you the SHAPE of a curve.")
    print(f"  A parametric equation tells you the JOURNEY along it.")
    print(f"")
    print(f"      x = f(t)")
    print(f"      y = g(t)")
    print(f"")
    print(f"  As t varies, the point (x,y) moves along a path.")
    print(f"  t is often time — but it can be any quantity.")
    print(f"  On a circle, t is the angle.")
    print(f"  On a cycloid, t is how far the wheel has rotated.")
    print(f"")
    print(f"  Some curves simply can't be written as y=f(x).")
    print(f"  A circle has two y-values for each x.")
    print(f"  A figure-8 crosses itself.")
    print(f"  A cycloid has cusps and arches.")
    print(f"  Parametric form handles all of these naturally.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Line in parametric form")
    print(f"  2 — Circle and ellipse")
    print(f"  3 — Cycloids and spirals    (the beautiful curves)")
    print(f"  4 — Projectile motion       (physics meets math)")
    print(f"  5 — Eliminating the parameter  (back to Cartesian)")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        parametric_line()
    elif choice == "2":
        parametric_conics()
    elif choice == "3":
        cycloid_and_spirals()
    elif choice == "4":
        projectile_motion()
    elif choice == "5":
        eliminate_parameter()
    else:
        print(f"  Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    parametric_equations()
    