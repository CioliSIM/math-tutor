import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def analyze_line():
    print(f"\n{'='*50}")
    print(f"THE LINE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A line is the simplest object in geometry.")
    print(f"  No curves, no bends — just a constant direction forever.")
    print(f"  In the coordinate plane, every non-vertical line")
    print(f"  can be written as:")
    print(f"")
    print(f"      y = mx + q")
    print(f"")
    print(f"  m is the slope — it measures steepness and direction.")
    print(f"  q is the y-intercept — where the line crosses the y-axis.")
    print(f"")
    print(f"  The slope tells you everything about direction:")
    print(f"  · m > 0  → rising from left to right")
    print(f"  · m < 0  → falling from left to right")
    print(f"  · m = 0  → perfectly horizontal")
    print(f"  · undefined slope → vertical line (can't write as y=mx+q)")
    print(f"")
    print(f"  Interesting fact: the slope m is exactly the tangent")
    print(f"  of the angle the line makes with the x-axis.")
    print(f"  m = tan(θ) — trigonometry and geometry, connected.")
    print(f"")
    print(f"  How do you want to define the line?")
    print(f"  1 — slope and y-intercept  (y = mx + q)")
    print(f"  2 — two points")
    print(f"  3 — one point and a slope")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        m = float(input("  Slope m: "))
        q = float(input("  y-intercept q: "))

        print(f"\n--- The line ---")
        print(f"  y = {m}x + {q}")
        print(f"")
        if m > 0:
            print(f"  Slope = {m} > 0 → the line rises left to right.")
        elif m < 0:
            print(f"  Slope = {m} < 0 → the line falls left to right.")
        else:
            print(f"  Slope = 0 → horizontal line.")
        print(f"")
        print(f"  y-intercept: (0, {q})")

        if m != 0:
            x_int = -q / m
            print(f"  x-intercept: set y = 0 → {m}x + {q} = 0 → x = {x_int:.4f}")
            print(f"  x-intercept: ({x_int:.4f}, 0)")
        else:
            if q == 0:
                print(f"  This line IS the x-axis.")
            else:
                print(f"  No x-intercept — line is parallel to the x-axis.")

    elif choice == "2":
        x1 = float(input("  x₁: "))
        y1 = float(input("  y₁: "))
        x2 = float(input("  x₂: "))
        y2 = float(input("  y₂: "))

        print(f"\n--- Step 1: Compute the slope ---")
        print(f"  The slope measures how much y changes per unit of x.")
        print(f"  m = (y₂ - y₁) / (x₂ - x₁)")
        print(f"    = ({y2} - {y1}) / ({x2} - {x1})")

        if x2 == x1:
            print(f"    = undefined — this is a vertical line.")
            print(f"\n  Equation: x = {x1}")
            plot_line(None, None, x_vertical=x1, points=[(x1,y1),(x2,y2)])
            return

        m = (y2 - y1) / (x2 - x1)
        print(f"    = {y2-y1} / {x2-x1} = {m:.4f}")

        print(f"\n--- Step 2: Find q ---")
        print(f"  Plug point ({x1}, {y1}) into y = mx + q and solve for q:")
        print(f"  {y1} = {m:.4f}·{x1} + q")
        q = y1 - m * x1
        print(f"  q = {y1} - {m:.4f}·{x1} = {q:.4f}")

        print(f"\n--- Result ---")
        print(f"  y = {m:.4f}x + {q:.4f}")

    elif choice == "3":
        x1 = float(input("  Point x: "))
        y1 = float(input("  Point y: "))
        m  = float(input("  Slope m: "))

        print(f"\n--- Point-slope form ---")
        print(f"  When you know a point and a slope, use:")
        print(f"  y - y₁ = m(x - x₁)")
        print(f"  y - {y1} = {m}(x - {x1})")
        print(f"  y = {m}x - {m*x1:.4f} + {y1}")
        q = y1 - m * x1
        print(f"  y = {m}x + {q:.4f}")

    else:
        print(f"  Invalid choice.")
        return

    print(f"\n--- Parallel and perpendicular lines ---")
    print(f"  Two lines are PARALLEL if they have the same slope")
    print(f"  and never meet. A line parallel to this one has m = {m}.")
    print(f"")
    if m != 0:
        m_perp = -1/m
        print(f"  Two lines are PERPENDICULAR if their slopes satisfy:")
        print(f"  m₁ · m₂ = -1")
        print(f"  So the perpendicular slope is: -1/{m} = {m_perp:.4f}")
        print(f"")
        print(f"  Why? Because rotating a direction by 90° inverts")
        print(f"  and negates the slope. It's a beautiful geometric fact.")
    else:
        print(f"  The perpendicular to a horizontal line is vertical.")

    print(f"\n--- Theorem: distance from a point to a line ---")
    print(f"  This is one of the most useful formulas in geometry.")
    print(f"  Rewrite the line as: {m}x - y + {q:.4f} = 0  (ax + by + c = 0)")
    print(f"  Then the distance from point (x₀, y₀) to the line is:")
    print(f"")
    print(f"      d = |a·x₀ + b·y₀ + c| / √(a² + b²)")
    print(f"")
    print(f"  The denominator normalizes by the length of the")
    print(f"  direction vector — it makes the formula work regardless")
    print(f"  of how the line equation is scaled.")
    print(f"")
    px = float(input("  Point x: "))
    py = float(input("  Point y: "))

    a_c = m
    b_c = -1
    c_c = q
    dist = abs(a_c*px + b_c*py + c_c) / math.sqrt(a_c**2 + b_c**2)

    print(f"")
    print(f"  d = |{a_c}·{px} + ({b_c})·{py} + {c_c:.4f}|")
    print(f"      / √({a_c}² + ({b_c})²)")
    print(f"    = |{a_c*px + b_c*py + c_c:.4f}| / √{a_c**2 + b_c**2:.4f}")
    print(f"    = {dist:.6f}")

    plot_line(m, q, points=[(px, py)])


def plot_line(m, q, x_vertical=None, points=None):
    fig, ax = plt.subplots(figsize=(7, 7))

    if x_vertical is not None:
        ax.axvline(x_vertical, color="crimson", linewidth=2,
                   label=f"x = {x_vertical}")
    else:
        x_vals = np.linspace(-10, 10, 400)
        y_vals = m * x_vals + q
        ax.plot(x_vals, y_vals, color="crimson", linewidth=2,
                label=f"y = {m:.4f}x + {q:.4f}")

    if points:
        for px, py in points:
            ax.plot(px, py, "o", color="steelblue", markersize=10)
            ax.annotate(f"  ({px}, {py})", (px, py), fontsize=10)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect("equal")
    ax.set_title("Line in the coordinate plane", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def analyze_circle():
    print(f"\n{'='*50}")
    print(f"THE CIRCLE")
    print(f"{'='*50}")
    print(f"")
    print(f"  A circle is the set of all points at the same distance")
    print(f"  from a fixed center. That distance is the radius.")
    print(f"  Simple definition — surprisingly rich consequences.")
    print(f"")
    print(f"  If the center is (a, b) and the radius is r,")
    print(f"  the equation comes directly from the distance formula:")
    print(f"")
    print(f"      (x - a)² + (y - b)² = r²")
    print(f"")
    print(f"  It's the Pythagorean theorem — the distance from")
    print(f"  any point (x,y) on the circle to (a,b) must equal r.")
    print(f"")
    print(f"  Interesting theorem — Thales' theorem:")
    print(f"  If you take any diameter of a circle and pick any")
    print(f"  point on the circle (not on the diameter),")
    print(f"  the angle at that point is always exactly 90°.")
    print(f"  Always. No matter where on the circle you pick.")
    print(f"  This is one of the oldest theorems in geometry.")
    print(f"")
    print(f"  How do you want to define the circle?")
    print(f"  1 — center and radius")
    print(f"  2 — general form  x² + y² + dx + ey + f = 0")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        a = float(input("  Center x (a): "))
        b = float(input("  Center y (b): "))
        r = float(input("  Radius r: "))

        if r <= 0:
            print(f"  Radius must be positive.")
            return

        print(f"\n--- The circle ---")
        print(f"  (x - {a})² + (y - {b})² = {r}²  =  {r**2}")
        print(f"")
        print(f"  Center: ({a}, {b})")
        print(f"  Radius: {r}")
        print(f"  Diameter: {2*r}")
        print(f"  Circumference: 2πr = {2*math.pi*r:.4f}")
        print(f"  Area: πr² = {math.pi*r**2:.4f}")
        print(f"")

        print(f"--- Expanding to general form ---")
        print(f"  We expand (x-{a})² and (y-{b})²:")
        d = -2*a
        e = -2*b
        f = a**2 + b**2 - r**2
        print(f"  x² - {2*a}x + {a**2} + y² - {2*b}y + {b**2} = {r**2}")
        print(f"  x² + y² + {d}x + {e}y + {f} = 0")
        print(f"")
        print(f"  General form: x² + y² + {d}x + {e}y + {f} = 0")

    elif choice == "2":
        print(f"  x² + y² + dx + ey + f = 0")
        d = float(input("  Enter d: "))
        e = float(input("  Enter e: "))
        f = float(input("  Enter f: "))

        print(f"\n--- Step 1: Complete the square ---")
        print(f"  We rewrite the equation to reveal center and radius.")
        print(f"  The trick: complete the square for both x and y.")
        print(f"")
        print(f"  x² + {d}x + y² + {e}y = {-f}")
        print(f"")
        print(f"  For x: half the coefficient of x is {d/2},")
        print(f"         its square is {(d/2)**2}. Add it to both sides.")
        print(f"  For y: half the coefficient of y is {e/2},")
        print(f"         its square is {(e/2)**2}. Add it to both sides.")
        print(f"")

        a = -d/2
        b = -e/2
        r_sq = a**2 + b**2 - f

        print(f"  (x - {a})² + (y - {b})² = {-f} + {(d/2)**2} + {(e/2)**2}")
        print(f"  (x - {a})² + (y - {b})² = {r_sq}")
        print(f"")

        if r_sq < 0:
            print(f"  r² = {r_sq} < 0 — this equation has no real solution.")
            print(f"  No circle exists in the real plane.")
            return
        elif r_sq == 0:
            print(f"  r² = 0 — this is a single point at ({a}, {b}),")
            print(f"  called a degenerate circle.")
            return

        r = math.sqrt(r_sq)
        print(f"--- Step 2: Read off center and radius ---")
        print(f"  Center: ({a}, {b})")
        print(f"  Radius: √{r_sq} = {r:.4f}")

    else:
        print(f"  Invalid choice.")
        return

    print(f"\n--- Position of a point relative to the circle ---")
    print(f"  Any point in the plane falls in exactly one of three cases:")
    print(f"  · inside  → distance from center < r")
    print(f"  · on      → distance from center = r")
    print(f"  · outside → distance from center > r")
    print(f"  We just compute the distance and compare.")
    print(f"")
    px = float(input("  Point x: "))
    py = float(input("  Point y: "))

    dist = math.sqrt((px-a)**2 + (py-b)**2)
    print(f"")
    print(f"  d = √(({px}-{a})² + ({py}-{b})²)")
    print(f"    = √({(px-a)**2:.4f} + {(py-b)**2:.4f})")
    print(f"    = {dist:.6f}")
    print(f"  r = {r:.6f}")
    print(f"")

    if abs(dist - r) < 1e-9:
        print(f"  d = r → the point is ON the circle.")
    elif dist < r:
        print(f"  d < r → the point is INSIDE the circle.")
        print(f"  Distance from the circle: {r - dist:.6f}")
    else:
        print(f"  d > r → the point is OUTSIDE the circle.")
        print(f"  Distance from the circle: {dist - r:.6f}")

    plot_circle(a, b, r, points=[(px, py)])


def plot_circle(a, b, r, points=None):
    fig, ax = plt.subplots(figsize=(7, 7))

    theta  = np.linspace(0, 2*np.pi, 400)
    x_circ = a + r * np.cos(theta)
    y_circ = b + r * np.sin(theta)

    ax.plot(x_circ, y_circ, color="crimson", linewidth=2,
            label=f"circle: center=({a},{b}), r={r:.2f}")
    ax.plot(a, b, "o", color="crimson", markersize=8)
    ax.annotate(f"  center ({a},{b})", (a, b), fontsize=10)
    ax.plot([a, a+r], [b, b], color="gray", linewidth=1.5, linestyle="--")
    ax.text(a + r/2, b + 0.2, f"r={r:.2f}", ha="center", fontsize=10)

    if points:
        for px, py in points:
            dist = math.sqrt((px-a)**2 + (py-b)**2)
            color = "green" if abs(dist-r) < 1e-9 else \
                    "steelblue" if dist < r else "orange"
            ax.plot(px, py, "o", color=color, markersize=10)
            ax.annotate(f"  ({px},{py})", (px, py), fontsize=10)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    lim = max(abs(a)+r+2, abs(b)+r+2, 5)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_title("Circle in the coordinate plane", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def analyze_parabola():
    print(f"\n{'='*50}")
    print(f"THE PARABOLA")
    print(f"{'='*50}")
    print(f"")
    print(f"  A parabola has a geometric definition that most")
    print(f"  people never see in school — and it's beautiful.")
    print(f"  It's the set of all points equidistant from:")
    print(f"  · a fixed point called the FOCUS")
    print(f"  · a fixed line called the DIRECTRIX")
    print(f"")
    print(f"  Every point on the parabola is exactly halfway")
    print(f"  between the focus and the directrix.")
    print(f"  This definition is what gives the parabola its")
    print(f"  reflecting property — parallel rays aimed at a")
    print(f"  parabolic mirror all converge at the focus.")
    print(f"  That's why satellite dishes, car headlights, and")
    print(f"  telescope mirrors are all parabolic.")
    print(f"")
    print(f"  The algebraic equation you already know:")
    print(f"      y = ax² + bx + c")
    print(f"  and the vertex form — the most informative:")
    print(f"      y = a(x - h)² + k   where (h,k) is the vertex")
    print(f"")
    print(f"  The sign of a:")
    print(f"  · a > 0 → opens upward, vertex is a minimum")
    print(f"  · a < 0 → opens downward, vertex is a maximum")
    print(f"  · |a| large → narrow · |a| small → wide")
    print(f"")

    a = float(input("  Enter a: "))
    b = float(input("  Enter b: "))
    c = float(input("  Enter c: "))

    print(f"\n--- The parabola: y = {a}x² + {b}x + {c} ---")
    print(f"")

    print(f"--- Step 1: Find the vertex ---")
    print(f"  The vertex x-coordinate: h = -b / 2a")
    print(f"  This comes from completing the square —")
    print(f"  it's the x value that minimizes (or maximizes) the parabola.")
    print(f"")
    h = -b / (2*a)
    k = a*h**2 + b*h + c
    print(f"  h = -({b}) / (2·{a}) = {h:.4f}")
    print(f"  k = {a}·({h:.4f})² + {b}·({h:.4f}) + {c} = {k:.4f}")
    print(f"  Vertex: ({h:.4f}, {k:.4f})")
    print(f"")
    if a > 0:
        print(f"  a > 0 → this is a MINIMUM point.")
        print(f"  The parabola never goes below y = {k:.4f}.")
    else:
        print(f"  a < 0 → this is a MAXIMUM point.")
        print(f"  The parabola never goes above y = {k:.4f}.")

    print(f"\n--- Step 2: Vertex form ---")
    print(f"  y = {a}(x - {h:.4f})² + {k:.4f}")
    print(f"  This form makes the vertex obvious at a glance.")

    print(f"\n--- Step 3: Axis of symmetry ---")
    print(f"  The parabola is perfectly symmetric about x = {h:.4f}.")
    print(f"  Any two points at equal distance from this line")
    print(f"  have the same y value.")

    print(f"\n--- Step 4: Focus and directrix ---")
    print(f"  Parameter p = 1/(4a) — the distance from vertex to focus.")
    p = 1 / (4*a)
    focus     = (h, k + p)
    directrix = k - p
    print(f"  p = 1/(4·{a}) = {p:.4f}")
    print(f"  Focus:     ({focus[0]:.4f}, {focus[1]:.4f})")
    print(f"  Directrix: y = {directrix:.4f}")
    print(f"")
    print(f"  Every point on the parabola is exactly {abs(p):.4f} units")
    print(f"  from both the focus and the directrix — simultaneously.")

    print(f"\n--- Step 5: Intersections with the axes ---")
    print(f"  y-intercept: x=0 → y = {c}  →  point (0, {c})")
    print(f"")
    print(f"  x-intercepts: solve {a}x² + {b}x + {c} = 0")
    delta = b**2 - 4*a*c
    print(f"  Δ = {b}² - 4·{a}·{c} = {delta:.4f}")
    print(f"")

    x_intercepts = []
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print(f"  Δ > 0 → two x-intercepts:")
        print(f"  x₁ = {x1:.4f},  x₂ = {x2:.4f}")
        x_intercepts = [(x1, 0), (x2, 0)]
    elif delta == 0:
        x1 = -b / (2*a)
        print(f"  Δ = 0 → one x-intercept (tangent to x-axis):")
        print(f"  x = {x1:.4f}")
        x_intercepts = [(x1, 0)]
    else:
        print(f"  Δ < 0 → no x-intercepts.")
        print(f"  The parabola lives entirely above (or below) the x-axis.")

    plot_parabola(a, b, c, h, k, focus, directrix, x_intercepts)


def plot_parabola(a, b, c, h, k, focus, directrix, x_intercepts):
    spread = max(abs(h) + 5, 6)
    x_vals = np.linspace(h - spread, h + spread, 400)
    y_vals = a*x_vals**2 + b*x_vals + c

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(x_vals, y_vals, color="crimson", linewidth=2,
            label=f"y = {a}x² + {b}x + {c}")
    ax.plot(h, k, "o", color="steelblue", markersize=10,
            label=f"Vertex ({h:.2f}, {k:.2f})")
    ax.annotate(f"  vertex ({h:.2f}, {k:.2f})", (h, k), fontsize=10)
    ax.plot(focus[0], focus[1], "^", color="green", markersize=10,
            label=f"Focus ({focus[0]:.2f}, {focus[1]:.2f})")
    x_dir = np.linspace(h - spread, h + spread, 100)
    ax.plot(x_dir, [directrix]*100, color="orange", linewidth=1.5,
            linestyle="--", label=f"Directrix y={directrix:.2f}")
    ax.axvline(h, color="gray", linewidth=1, linestyle=":",
               label=f"Axis x={h:.2f}")
    for xi, yi in x_intercepts:
        ax.plot(xi, yi, "o", color="purple", markersize=8)
        ax.annotate(f"  ({xi:.2f}, 0)", (xi, yi), fontsize=9)
    ax.plot(0, c, "o", color="brown", markersize=8)
    ax.annotate(f"  (0, {c})", (0, c), fontsize=9)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    y_range = max(abs(a) * spread**2, 5)
    ax.set_ylim(k - y_range, k + y_range)
    ax.set_xlim(h - spread, h + spread)
    ax.set_title(f"Parabola: y = {a}x² + {b}x + {c}", fontsize=14)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def analyze_distances():
    print(f"\n{'='*50}")
    print(f"DISTANCES AND INTERSECTIONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  Once you have coordinates, you can measure everything.")
    print(f"  Distances, midpoints, intersections — all become")
    print(f"  algebraic computations. That's the power of")
    print(f"  Descartes' idea: geometry becomes calculation.")
    print(f"")
    print(f"  What do you want to compute?")
    print(f"  1 — Distance between two points")
    print(f"  2 — Midpoint of a segment")
    print(f"  3 — Intersection of two lines")
    print(f"  4 — Intersection of a line and a circle")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        print(f"\n  DISTANCE BETWEEN TWO POINTS")
        print(f"")
        print(f"  Formula: d = √((x₂-x₁)² + (y₂-y₁)²)")
        print(f"  This is the Pythagorean theorem applied to")
        print(f"  the right triangle formed by the two points.")
        print(f"  The horizontal leg is |x₂-x₁|,")
        print(f"  the vertical leg is |y₂-y₁|,")
        print(f"  and the distance is the hypotenuse.")
        print(f"")
        x1 = float(input("  x₁: "))
        y1 = float(input("  y₁: "))
        x2 = float(input("  x₂: "))
        y2 = float(input("  y₂: "))

        dx = x2 - x1
        dy = y2 - y1
        d  = math.sqrt(dx**2 + dy**2)

        print(f"\n  d = √(({x2}-{x1})² + ({y2}-{y1})²)")
        print(f"    = √({dx}² + {dy}²)")
        print(f"    = √({dx**2} + {dy**2})")
        print(f"    = √{dx**2 + dy**2}")
        print(f"    = {d:.6f}")

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.plot([x1, x2], [y1, y2], color="crimson", linewidth=2,
                label=f"d = {d:.4f}")
        ax.plot([x1, x2], [y1, y1], color="gray", linewidth=1,
                linestyle="--", label=f"|Δx| = {abs(dx)}")
        ax.plot([x2, x2], [y1, y2], color="steelblue", linewidth=1,
                linestyle="--", label=f"|Δy| = {abs(dy)}")
        ax.plot(x1, y1, "o", color="black", markersize=10)
        ax.plot(x2, y2, "o", color="black", markersize=10)
        ax.annotate(f"  ({x1},{y1})", (x1, y1), fontsize=10)
        ax.annotate(f"  ({x2},{y2})", (x2, y2), fontsize=10)
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.3,
                f"d = {d:.4f}", ha="center", fontsize=11, color="crimson")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_aspect("equal")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title("Distance between two points", fontsize=14)
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        print(f"\n  MIDPOINT OF A SEGMENT")
        print(f"")
        print(f"  Formula: M = ((x₁+x₂)/2, (y₁+y₂)/2)")
        print(f"  The midpoint is simply the average of the coordinates.")
        print(f"  Average x gives the horizontal center,")
        print(f"  average y gives the vertical center.")
        print(f"")
        x1 = float(input("  x₁: "))
        y1 = float(input("  y₁: "))
        x2 = float(input("  x₂: "))
        y2 = float(input("  y₂: "))

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        print(f"\n  M = (({x1}+{x2})/2, ({y1}+{y2})/2)")
        print(f"    = ({x1+x2}/2, {y1+y2}/2)")
        print(f"    = ({mx:.4f}, {my:.4f})")
        print(f"")
        print(f"  The midpoint divides the segment into two")
        print(f"  equal halves — each of length {math.sqrt((x2-x1)**2+(y2-y1)**2)/2:.4f}.")

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.plot([x1, x2], [y1, y2], color="crimson", linewidth=2)
        ax.plot(x1, y1, "o", color="steelblue", markersize=10)
        ax.plot(x2, y2, "o", color="steelblue", markersize=10)
        ax.plot(mx, my, "o", color="green", markersize=12,
                label=f"Midpoint ({mx:.2f}, {my:.2f})")
        ax.annotate(f"  ({x1},{y1})", (x1, y1), fontsize=10)
        ax.annotate(f"  ({x2},{y2})", (x2, y2), fontsize=10)
        ax.annotate(f"  M({mx:.2f},{my:.2f})", (mx, my), fontsize=10)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_aspect("equal")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title("Midpoint of a segment", fontsize=14)
        plt.tight_layout()
        plt.show()

    elif choice == "3":
        print(f"\n  INTERSECTION OF TWO LINES")
        print(f"")
        print(f"  Two lines in the plane have exactly three possibilities:")
        print(f"  · they intersect at one point  (different slopes)")
        print(f"  · they are parallel            (same slope, different q)")
        print(f"  · they are identical           (same slope, same q)")
        print(f"")
        print(f"  To find the intersection, set the two equations equal")
        print(f"  and solve for x. Then substitute back to find y.")
        print(f"")
        m1 = float(input("  m₁: "))
        q1 = float(input("  q₁: "))
        m2 = float(input("  m₂: "))
        q2 = float(input("  q₂: "))

        print(f"\n--- Setting equal ---")
        print(f"  {m1}x + {q1} = {m2}x + {q2}")
        print(f"  ({m1}-{m2})x = {q2}-{q1}")
        print(f"  {m1-m2}x = {q2-q1}")

        if m1 == m2:
            if q1 == q2:
                print(f"\n  0 = 0 — the lines are identical.")
                print(f"  Every point on one line is on the other.")
                print(f"  Infinitely many intersections.")
            else:
                print(f"\n  0 = {q2-q1} — impossible.")
                print(f"  The lines are parallel — they never meet.")
            return

        xi = (q2 - q1) / (m1 - m2)
        yi = m1 * xi + q1

        print(f"  x = {q2-q1} / {m1-m2} = {xi:.4f}")
        print(f"  y = {m1}·{xi:.4f} + {q1} = {yi:.4f}")
        print(f"")
        print(f"  Intersection: ({xi:.4f}, {yi:.4f})")

        x_vals = np.linspace(xi - 5, xi + 5, 400)
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.plot(x_vals, m1*x_vals + q1, color="crimson", linewidth=2,
                label=f"y = {m1}x + {q1}")
        ax.plot(x_vals, m2*x_vals + q2, color="steelblue", linewidth=2,
                label=f"y = {m2}x + {q2}")
        ax.plot(xi, yi, "o", color="green", markersize=12,
                label=f"Intersection ({xi:.2f}, {yi:.2f})")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_aspect("equal")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title("Intersection of two lines", fontsize=14)
        plt.tight_layout()
        plt.show()

    elif choice == "4":
        print(f"\n  INTERSECTION OF A LINE AND A CIRCLE")
        print(f"")
        print(f"  Strategy: substitute the line into the circle equation.")
        print(f"  You get a quadratic in x — and its discriminant")
        print(f"  tells you immediately how many intersections exist:")
        print(f"  · Δ > 0  → two points (secant line)")
        print(f"  · Δ = 0  → one point  (tangent line)")
        print(f"  · Δ < 0  → no points  (external line)")
        print(f"")
        print(f"  Interesting theorem — tangent-radius perpendicularity:")
        print(f"  When a line is tangent to a circle, it is always")
        print(f"  perpendicular to the radius at the point of tangency.")
        print(f"  Always. This is a fundamental theorem of circle geometry.")
        print(f"")
        m = float(input("  Line slope m: "))
        q = float(input("  Line intercept q: "))
        a = float(input("  Circle center x (a): "))
        b = float(input("  Circle center y (b): "))
        r = float(input("  Circle radius r: "))

        print(f"\n--- Substituting y = {m}x + {q} into the circle ---")
        print(f"  (x-{a})² + ({m}x+{q}-{b})² = {r}²")
        print(f"")

        A = 1 + m**2
        B = -2*a + 2*m*(q-b)
        C = a**2 + (q-b)**2 - r**2

        print(f"  Expanding and collecting terms:")
        print(f"  {A}x² + {B:.4f}x + {C:.4f} = 0")
        print(f"")

        delta = B**2 - 4*A*C
        print(f"  Δ = {B:.4f}² - 4·{A:.4f}·{C:.4f} = {delta:.4f}")
        print(f"")

        fig, ax = plt.subplots(figsize=(7, 7))
        theta = np.linspace(0, 2*np.pi, 400)
        ax.plot(a + r*np.cos(theta), b + r*np.sin(theta),
                color="steelblue", linewidth=2,
                label=f"circle: center=({a},{b}), r={r}")
        x_vals = np.linspace(a-r-2, a+r+2, 400)
        ax.plot(x_vals, m*x_vals+q, color="crimson", linewidth=2,
                label=f"y = {m}x + {q}")

        if delta < 0:
            print(f"  Δ < 0 → no intersection.")
            print(f"  The line misses the circle entirely.")
            print(f"  It's an external line.")
        elif abs(delta) < 1e-9:
            x1 = -B / (2*A)
            y1 = m*x1 + q
            print(f"  Δ = 0 → tangent line.")
            print(f"  The line just grazes the circle at one point.")
            print(f"  Tangent point: ({x1:.4f}, {y1:.4f})")
            print(f"  At this point, the radius to ({x1:.4f},{y1:.4f})")
            print(f"  is perpendicular to the line — as the theorem says.")
            ax.plot(x1, y1, "o", color="green", markersize=12,
                    label=f"Tangent ({x1:.2f}, {y1:.2f})")
        else:
            x1 = (-B + math.sqrt(delta)) / (2*A)
            x2 = (-B - math.sqrt(delta)) / (2*A)
            y1 = m*x1 + q
            y2 = m*x2 + q
            print(f"  Δ > 0 → two intersections (secant line).")
            print(f"  P₁ = ({x1:.4f}, {y1:.4f})")
            print(f"  P₂ = ({x2:.4f}, {y2:.4f})")
            chord = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            print(f"  Length of the chord: {chord:.4f}")
            ax.plot(x1, y1, "o", color="green", markersize=12,
                    label=f"P₁ ({x1:.2f}, {y1:.2f})")
            ax.plot(x2, y2, "o", color="orange", markersize=12,
                    label=f"P₂ ({x2:.2f}, {y2:.2f})")

        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_aspect("equal")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title("Line and circle intersection", fontsize=14)
        plt.tight_layout()
        plt.show()

    else:
        print(f"  Invalid choice.")


def analytic_geometry():
    print(f"\n{'='*50}")
    print(f"ANALYTIC GEOMETRY")
    print(f"{'='*50}")
    print(f"")
    print(f"  In the 1600s, René Descartes had an idea that changed")
    print(f"  mathematics forever: assign a pair of numbers to every")
    print(f"  point in the plane. Suddenly, geometry and algebra")
    print(f"  became the same thing.")
    print(f"")
    print(f"  A line is an equation. A circle is an equation.")
    print(f"  Finding where two curves meet becomes solving a system.")
    print(f"  Distances become calculations.")
    print(f"  The visual and the algebraic are unified.")
    print(f"")
    print(f"  This is analytic geometry — and it's the foundation")
    print(f"  of everything that comes after: calculus, linear algebra,")
    print(f"  differential equations, physics, engineering.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — The line")
    print(f"  2 — The circle")
    print(f"  3 — The parabola")
    print(f"  4 — Distances and intersections")
    print(f"")
    choice = input("  Enter 1, 2, 3, or 4: ")

    if choice == "1":
        analyze_line()
    elif choice == "2":
        analyze_circle()
    elif choice == "3":
        analyze_parabola()
    elif choice == "4":
        analyze_distances()
    else:
        print(f"  Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    analytic_geometry()