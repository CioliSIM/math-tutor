import math
import matplotlib.pyplot as plt
import numpy as np


def fmt_angle(deg):
    return f"{deg:.2f}°"


def plot_complex_plane(numbers, labels, title="Complex Plane"):
    pass  # not needed here


def triangle_analyzer():
    print(f"\n{'='*50}")
    print(f"TRIANGLES")
    print(f"{'='*50}")
    print(f"")
    print(f"  The triangle is the simplest polygon — and the most")
    print(f"  fundamental. Every other polygon can be cut into triangles.")
    print(f"  Every geometric proof eventually reduces to triangles.")
    print(f"  Master triangles and you understand geometry.")
    print(f"")
    print(f"  The one rule that never changes:")
    print(f"  The three interior angles always sum to 180°.")
    print(f"  No exceptions. For any triangle, anywhere.")
    print(f"")
    print(f"  Why? Draw a line through one vertex parallel to")
    print(f"  the opposite side. The three angles at that vertex")
    print(f"  are alternate interior angles with the triangle's angles.")
    print(f"  Together they form a straight line — 180°.")
    print(f"")
    print(f"  Classification by sides:")
    print(f"  · Scalene     — all sides different")
    print(f"  · Isosceles   — two sides equal (base angles equal too)")
    print(f"  · Equilateral — all sides equal, all angles 60°")
    print(f"")
    print(f"  Classification by angles:")
    print(f"  · Acute   — all angles < 90°")
    print(f"  · Right   — one angle = 90°  (Pythagoras applies directly)")
    print(f"  · Obtuse  — one angle > 90°")
    print(f"")

    a = float(input("  Side a: "))
    b = float(input("  Side b: "))
    c = float(input("  Side c: "))

    print(f"\n--- Step 1: Triangle inequality ---")
    print(f"  For three lengths to form a triangle, each side")
    print(f"  must be strictly less than the sum of the other two.")
    print(f"  This isn't just a rule — it's a geometric necessity.")
    print(f"  If one side equals the sum of the others, the triangle")
    print(f"  collapses into a straight line.")
    print(f"")
    c1 = a+b > c
    c2 = a+c > b
    c3 = b+c > a
    print(f"  a+b > c:  {a}+{b} = {a+b} > {c}?  {'✓' if c1 else '✗'}")
    print(f"  a+c > b:  {a}+{c} = {a+c} > {b}?  {'✓' if c2 else '✗'}")
    print(f"  b+c > a:  {b}+{c} = {b+c} > {a}?  {'✓' if c3 else '✗'}")

    if not (c1 and c2 and c3):
        print(f"\n  These lengths cannot form a triangle.")
        return

    print(f"\n--- Step 2: Classify by sides ---")
    if a == b == c:
        side_type = "Equilateral — all sides equal, all angles exactly 60°"
    elif a == b or b == c or a == c:
        side_type = "Isosceles — two sides equal, two base angles equal"
    else:
        side_type = "Scalene — all sides different, all angles different"
    print(f"  {side_type}")

    print(f"\n--- Step 3: Find the angles (law of cosines) ---")
    print(f"  The law of cosines generalizes Pythagoras to any triangle:")
    print(f"  c² = a² + b² - 2ab·cos(C)")
    print(f"  Rearranging: cos(C) = (a²+b²-c²) / (2ab)")
    print(f"")

    cos_A = (b**2+c**2-a**2) / (2*b*c)
    cos_B = (a**2+c**2-b**2) / (2*a*c)
    cos_C = (a**2+b**2-c**2) / (2*a*b)

    A = math.degrees(math.acos(max(-1, min(1, cos_A))))
    B = math.degrees(math.acos(max(-1, min(1, cos_B))))
    C = math.degrees(math.acos(max(-1, min(1, cos_C))))

    print(f"  Angle A (opposite a={a}): {A:.4f}°")
    print(f"  Angle B (opposite b={b}): {B:.4f}°")
    print(f"  Angle C (opposite c={c}): {C:.4f}°")
    print(f"  Sum: {A+B+C:.6f}° ✓")

    print(f"\n--- Step 4: Classify by angles ---")
    max_a = max(A, B, C)
    if abs(max_a - 90) < 1e-6:
        angle_type = "Right triangle — one angle is exactly 90°"
    elif max_a < 90:
        angle_type = "Acute triangle — all angles less than 90°"
    else:
        angle_type = "Obtuse triangle — one angle greater than 90°"
    print(f"  {angle_type}")

    print(f"\n--- Step 5: Pythagorean theorem check ---")
    s1, s2, hyp = sorted([a, b, c])
    print(f"  Sorting sides: {s1} ≤ {s2} ≤ {hyp}")
    print(f"  If right triangle: {s1}² + {s2}² should equal {hyp}²")
    print(f"  {s1}² + {s2}² = {s1**2+s2**2:.6f}")
    print(f"  {hyp}²        = {hyp**2:.6f}")
    diff = s1**2 + s2**2 - hyp**2
    if abs(diff) < 1e-6:
        print(f"  Equal ✓ — confirmed right triangle.")
        print(f"  Pythagoras: {s1}² + {s2}² = {hyp}²")
    elif diff > 0:
        print(f"  a²+b² > c² → acute triangle (confirmed)")
    else:
        print(f"  a²+b² < c² → obtuse triangle (confirmed)")
    print(f"")
    print(f"  This inverse of Pythagoras is just as useful as the theorem itself.")
    print(f"  It lets you classify any triangle from just three lengths.")

    print(f"\n--- Step 6: Area and perimeter ---")
    s    = (a+b+c) / 2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    perim = a+b+c

    print(f"  Perimeter = {a} + {b} + {c} = {perim:.4f}")
    print(f"")
    print(f"  Area — Heron's formula:")
    print(f"  s = (a+b+c)/2 = {s:.4f}  (semi-perimeter)")
    print(f"  Area = √(s·(s-a)·(s-b)·(s-c))")
    print(f"       = √({s:.4f}·{s-a:.4f}·{s-b:.4f}·{s-c:.4f})")
    print(f"       = {area:.4f}")
    print(f"")
    print(f"  Heron's formula works for ANY triangle — no height needed.")
    print(f"  Just the three sides. Incredibly practical.")

    print(f"\n--- Step 7: Circumradius and inradius ---")
    R = (a*b*c) / (4*area)
    r = area / s
    print(f"  Circumradius R = abc / (4·Area) = {R:.4f}")
    print(f"  The circumscribed circle passes through all three vertices.")
    print(f"")
    print(f"  Inradius r = Area / s = {r:.4f}")
    print(f"  The inscribed circle touches all three sides from inside.")
    print(f"")
    print(f"  Euler's formula for triangles: OI² = R(R-2r)")
    print(f"  where O is the circumcenter and I is the incenter.")
    OI_sq = R*(R - 2*r)
    if OI_sq >= 0:
        print(f"  OI = √(R(R-2r)) = √({R:.4f}·{R-2*r:.4f}) = {math.sqrt(OI_sq):.4f}")
    print(f"  Note: R ≥ 2r always (Euler's inequality)")
    print(f"  Equality holds only for the equilateral triangle.")

    plot_triangle(a, b, c, A, B, C, area, R, r)


def plot_triangle(a, b, c, A, B, C, area, R, r_in):
    A_rad = math.radians(A)
    x0, y0 = 0, 0
    x1, y1 = c, 0
    x2 = b * math.cos(A_rad)
    y2 = b * math.sin(A_rad)

    fig, ax = plt.subplots(figsize=(9, 7))

    tri = plt.Polygon([(x0,y0),(x1,y1),(x2,y2)],
                      fill=True, facecolor="steelblue",
                      alpha=0.12, edgecolor="steelblue", linewidth=2)
    ax.add_patch(tri)

    # circumscribed circle
    cx = (x0+x1+x2)/3
    cy = (y0+y1+y2)/3
    t  = np.linspace(0, 2*np.pi, 400)

    # circumcenter
    D  = 2*(x0*(y1-y2) + x1*(y2-y0) + x2*(y0-y1))
    if abs(D) > 1e-10:
        ux = ((x0**2+y0**2)*(y1-y2) + (x1**2+y1**2)*(y2-y0) +
              (x2**2+y2**2)*(y0-y1)) / D
        uy = ((x0**2+y0**2)*(x2-x1) + (x1**2+y1**2)*(x0-x2) +
              (x2**2+y2**2)*(x1-x0)) / D
        ax.plot(ux+R*np.cos(t), uy+R*np.sin(t),
                color="orange", linewidth=1, linestyle="--",
                alpha=0.6, label=f"Circumcircle R={R:.2f}")
        ax.plot(ux, uy, "^", color="orange", markersize=8)

    # incircle
    ix = (a*x0 + b*x1 + c*x2)/(a+b+c)
    iy = (a*y0 + b*y1 + c*y2)/(a+b+c)
    ax.plot(ix+r_in*np.cos(t), iy+r_in*np.sin(t),
            color="green", linewidth=1, linestyle="--",
            alpha=0.6, label=f"Incircle r={r_in:.2f}")
    ax.plot(ix, iy, "s", color="green", markersize=8)

    # vertices
    for (x,y), lbl in [((x0,y0),"A"),((x1,y1),"B"),((x2,y2),"C")]:
        ax.plot(x, y, "o", color="crimson", markersize=10)
        offset = (-0.3, -0.2)
        ax.annotate(f"{lbl}", (x+offset[0], y+offset[1]),
                    fontsize=13, fontweight="bold", color="crimson")

    # side labels
    ax.text((x0+x1)/2, -0.25, f"c={c:.2f}",
            ha="center", fontsize=10, color="steelblue")
    ax.text((x0+x2)/2-0.3, (y0+y2)/2,
            f"b={b:.2f}", ha="right", fontsize=10, color="steelblue")
    ax.text((x1+x2)/2+0.1, (y1+y2)/2,
            f"a={a:.2f}", ha="left", fontsize=10, color="steelblue")

    # angle labels
    ax.text(0.25, 0.12, f"{A:.1f}°", fontsize=9, color="green")
    ax.text(c-0.5, 0.12, f"{B:.1f}°", fontsize=9, color="green")
    ax.text(x2+0.05, y2-0.2, f"{C:.1f}°", fontsize=9, color="green")

    lim = max(x1, x2, y2, R) + 1
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-1, lim)
    ax.set_aspect("equal")
    ax.set_title(f"Triangle  —  Area={area:.4f},  Perimeter={a+b+c:.4f}",
                 fontsize=13)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def thales_theorem():
    print(f"\n{'='*50}")
    print(f"THALES' THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  Thales of Miletus — 6th century BC — was one of the")
    print(f"  first mathematicians to prove geometric results.")
    print(f"  His theorem comes in two versions, both fundamental.")
    print(f"")
    print(f"  VERSION 1 — Parallel lines divide proportionally:")
    print(f"  If DE ∥ BC in triangle ABC, then:")
    print(f"")
    print(f"      AD/DB = AE/EC")
    print(f"")
    print(f"  The parallel line cuts the two sides in the same ratio.")
    print(f"  This means triangle ADE is similar to triangle ABC —")
    print(f"  same shape, scaled down by factor k = AD/AB.")
    print(f"  Every corresponding measurement scales by k.")
    print(f"")
    print(f"  VERSION 2 — Angle in a semicircle:")
    print(f"  If AB is a diameter and C is any point on the circle,")
    print(f"  then angle ACB = 90°. Always. No matter where C is.")
    print(f"")
    print(f"  Why? The central angle for a diameter is 180°.")
    print(f"  The inscribed angle theorem says the inscribed angle")
    print(f"  is always half the central angle.")
    print(f"  180°/2 = 90°. Always.")
    print(f"")
    print(f"  Which version?")
    print(f"  1 — Proportional segments")
    print(f"  2 — Angle in semicircle")
    print(f"")
    choice = input("  Enter 1 or 2: ")

    if choice == "1":
        print(f"\n--- Thales — proportional segments ---")
        print(f"  Triangle ABC with DE ∥ BC.")
        print(f"")
        AD = float(input("  AD: "))
        DB = float(input("  DB: "))
        AE = float(input("  AE: "))

        AB    = AD + DB
        ratio = AD / DB
        EC    = AE / ratio
        AC    = AE + EC
        k     = AD / AB

        print(f"\n  AD/DB = {AD}/{DB} = {ratio:.4f}")
        print(f"  By Thales: AE/EC must equal the same ratio.")
        print(f"  EC = AE / ratio = {AE} / {ratio:.4f} = {EC:.4f}")
        print(f"  AC = AE + EC = {AE} + {EC:.4f} = {AC:.4f}")
        print(f"")
        print(f"  Verify: AE/EC = {AE}/{EC:.4f} = {AE/EC:.4f}")
        print(f"          AD/DB = {AD}/{DB} = {ratio:.4f}  ✓")
        print(f"")
        print(f"  Similarity ratio: k = AD/AB = {AD}/{AB} = {k:.4f}")
        print(f"  Triangle ADE is similar to ABC with ratio {k:.4f}.")
        print(f"  Every side of ADE is {k:.4f} times the corresponding side of ABC.")
        print(f"  Every area scales by k² = {k**2:.4f}.")

        plot_thales_parallel(AD, DB, AE, EC)

    elif choice == "2":
        print(f"\n--- Thales — angle in semicircle ---")
        print(f"")
        r         = float(input("  Circle radius: "))
        angle_deg = float(input("  Position of C on circle (degrees, 1-179): "))

        if not 0 < angle_deg < 180:
            print(f"  Angle must be strictly between 0° and 180°.")
            return

        angle_rad = math.radians(angle_deg)
        Cx = r * math.cos(angle_rad)
        Cy = r * math.sin(angle_rad)
        Ax, Ay = -r, 0
        Bx, By =  r, 0

        vCA   = (Ax-Cx, Ay-Cy)
        vCB   = (Bx-Cx, By-Cy)
        dot   = vCA[0]*vCB[0] + vCA[1]*vCB[1]
        magCA = math.sqrt(vCA[0]**2 + vCA[1]**2)
        magCB = math.sqrt(vCB[0]**2 + vCB[1]**2)
        acb   = math.degrees(math.acos(dot/(magCA*magCB)))

        print(f"\n  C is at {angle_deg}° on the circle.")
        print(f"  C = ({Cx:.4f}, {Cy:.4f})")
        print(f"  A = ({Ax}, {Ay})  B = ({Bx}, {By})")
        print(f"")
        print(f"  Angle ACB = {acb:.6f}°")
        print(f"  {'= 90° ✓ — Thales confirmed' if abs(acb-90)<1e-4 else '✗ something went wrong'}")
        print(f"")
        print(f"  Try any angle between 0° and 180° — it's always 90°.")
        print(f"  This is the power of the theorem: it works everywhere")
        print(f"  on the semicircle, not just at special points.")

        plot_thales_circle(r, Cx, Cy, Ax, Ay, Bx, By)

    else:
        print(f"  Invalid choice.")


def plot_thales_parallel(AD, DB, AE, EC):
    AB = AD + DB
    k  = AD / AB

    Ax, Ay =  0, AB
    Bx, By = -1,  0
    Cx, Cy =  1,  0
    Dx = Ax + k*(Bx-Ax)
    Dy = Ay + k*(By-Ay)
    Ex = Ax + k*(Cx-Ax)
    Ey = Ay + k*(Cy-Ay)

    fig, ax = plt.subplots(figsize=(7, 9))

    tri = plt.Polygon([(Ax,Ay),(Bx,By),(Cx,Cy)],
                      fill=True, facecolor="steelblue",
                      alpha=0.1, edgecolor="steelblue", linewidth=2)
    ax.add_patch(tri)

    ax.plot([Dx,Ex],[Dy,Ey], color="crimson", linewidth=2.5,
            label=f"DE ∥ BC  (ratio {AD/DB:.3f})")

    for (x,y), lbl in [((Ax,Ay),"A"),((Bx,By),"B"),
                        ((Cx,Cy),"C"),((Dx,Dy),"D"),((Ex,Ey),"E")]:
        ax.plot(x, y, "o", color="steelblue", markersize=9)
        ax.annotate(f"  {lbl}", (x,y), fontsize=12, fontweight="bold")

    ax.text((Ax+Dx)/2-0.2, (Ay+Dy)/2,
            f"AD={AD:.2f}", fontsize=9, color="green")
    ax.text((Dx+Bx)/2-0.2, (Dy+By)/2,
            f"DB={DB:.2f}", fontsize=9, color="green")
    ax.text((Ax+Ex)/2+0.05, (Ay+Ey)/2,
            f"AE={AE:.2f}", fontsize=9, color="orange")
    ax.text((Ex+Cx)/2+0.05, (Ey+Cy)/2,
            f"EC={EC:.2f}", fontsize=9, color="orange")

    ax.set_title(f"Thales' Theorem — AD/DB = AE/EC = {AD/DB:.4f}", fontsize=13)
    ax.set_aspect("equal")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_thales_circle(r, Cx, Cy, Ax, Ay, Bx, By):
    fig, ax = plt.subplots(figsize=(8, 8))

    t = np.linspace(0, 2*np.pi, 400)
    ax.plot(r*np.cos(t), r*np.sin(t),
            color="steelblue", linewidth=2, label="Circle")
    ax.plot([Ax,Bx],[Ay,By], color="black", linewidth=2.5,
            label="Diameter AB")

    tri = plt.Polygon([(Ax,Ay),(Cx,Cy),(Bx,By)],
                      fill=True, facecolor="steelblue",
                      alpha=0.12, edgecolor="crimson", linewidth=1.5)
    ax.add_patch(tri)

    # right angle marker at C
    size = r * 0.09
    vCA  = np.array([Ax-Cx, Ay-Cy])
    vCB  = np.array([Bx-Cx, By-Cy])
    vCA  = vCA / np.linalg.norm(vCA) * size
    vCB  = vCB / np.linalg.norm(vCB) * size
    sq   = np.array([[Cx, Cy],
                     [Cx+vCA[0], Cy+vCA[1]],
                     [Cx+vCA[0]+vCB[0], Cy+vCA[1]+vCB[1]],
                     [Cx+vCB[0], Cy+vCB[1]]])
    ax.plot(np.append(sq[:,0],sq[0,0]),
            np.append(sq[:,1],sq[0,1]),
            color="crimson", linewidth=2)

    for (x,y), lbl in [((Ax,Ay),"A"),((Bx,By),"B"),((Cx,Cy),"C")]:
        ax.plot(x, y, "o", color="crimson", markersize=10)
        ax.annotate(f"  {lbl}", (x,y), fontsize=12,
                    fontweight="bold", color="crimson")

    ax.plot(0, 0, "o", color="gray", markersize=7)
    ax.annotate("  O", (0,0), fontsize=10, color="gray")

    ax.set_xlim(-r-0.6, r+0.6)
    ax.set_ylim(-r-0.6, r+0.6)
    ax.set_aspect("equal")
    ax.set_title("Thales on circle — angle ACB = 90° always", fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def circle_geometry():
    print(f"\n{'='*50}")
    print(f"CIRCLE GEOMETRY")
    print(f"{'='*50}")
    print(f"")
    print(f"  A circle is the simplest curve — equidistant from one point.")
    print(f"  Yet it generates an enormous amount of geometry.")
    print(f"")
    print(f"  The most important theorem about angles in circles:")
    print(f"")
    print(f"  INSCRIBED ANGLE THEOREM:")
    print(f"  The central angle is exactly twice the inscribed angle")
    print(f"  when both subtend the same arc.")
    print(f"  This single theorem explains almost everything about")
    print(f"  angles in circles — including Thales' semicircle result.")
    print(f"")
    print(f"  Consequences:")
    print(f"  · All inscribed angles on the same arc are equal")
    print(f"  · Angle in semicircle = 90° (Thales)")
    print(f"  · Opposite angles of a cyclic quadrilateral sum to 180°")
    print(f"")
    print(f"  CHORD PROPERTIES:")
    print(f"  · Equal chords are equidistant from the center")
    print(f"  · Perpendicular bisector of any chord passes through center")
    print(f"  · Intersecting chords: PA·PB = PC·PD")
    print(f"")
    print(f"  TANGENT PROPERTIES:")
    print(f"  · Tangent is perpendicular to radius at tangency point")
    print(f"  · Two tangents from an external point are equal in length")
    print(f"")

    r = float(input("  Circle radius: "))

    print(f"\n--- Basic measurements ---")
    print(f"  Radius:        r = {r:.4f}")
    print(f"  Diameter:      d = {2*r:.4f}")
    print(f"  Circumference: C = 2πr = {2*math.pi*r:.4f}")
    print(f"  Area:          A = πr² = {math.pi*r**2:.4f}")

    print(f"\n--- Central angle and inscribed angle ---")
    central   = float(input("  Central angle (degrees): "))
    inscribed = central / 2
    print(f"")
    print(f"  Central angle:   {central:.2f}°")
    print(f"  Inscribed angle: {central:.2f}° / 2 = {inscribed:.2f}°")
    print(f"")
    print(f"  Any inscribed angle on the same arc = {inscribed:.2f}°")
    print(f"  They're all equal — no matter where on the arc.")
    if abs(central - 180) < 1e-6:
        print(f"  Central angle = 180° → this is a diameter.")
        print(f"  Inscribed angle = 90° — Thales' theorem!")

    print(f"\n--- Intersecting chords theorem ---")
    print(f"  Two chords intersect at P inside the circle.")
    print(f"  PA·PB = PC·PD  — always.")
    print(f"  Enter three of the four segments to find the fourth:")
    PA = float(input("  PA: "))
    PB = float(input("  PB: "))
    PC = float(input("  PC: "))
    PD = PA * PB / PC
    print(f"")
    print(f"  PA·PB = {PA}·{PB} = {PA*PB:.4f}")
    print(f"  PD = PA·PB / PC = {PA*PB:.4f} / {PC} = {PD:.4f}")
    print(f"  PC·PD = {PC}·{PD:.4f} = {PC*PD:.4f}  ✓")
    print(f"")
    print(f"  This theorem works even when the chords are secants")
    print(f"  from an external point — the product still holds.")

    plot_circle_geometry(r, central)


def plot_circle_geometry(r, central_deg):
    fig, ax = plt.subplots(figsize=(8, 8))

    t = np.linspace(0, 2*np.pi, 400)
    ax.plot(r*np.cos(t), r*np.sin(t),
            color="steelblue", linewidth=2, alpha=0.7)
    ax.plot(0, 0, "o", color="black", markersize=6)
    ax.annotate("  O", (0,0), fontsize=11, fontweight="bold")

    half = math.radians(central_deg/2)
    A    = (r*math.cos(-half), r*math.sin(-half))
    B    = (r*math.cos(half),  r*math.sin(half))

    ax.plot([0,A[0]], [0,A[1]], color="crimson", linewidth=2.5)
    ax.plot([0,B[0]], [0,B[1]], color="crimson", linewidth=2.5,
            label=f"Central angle = {central_deg:.1f}°")

    C_ang = math.radians(central_deg/2 + 130)
    C     = (r*math.cos(C_ang), r*math.sin(C_ang))
    ax.plot([C[0],A[0]], [C[1],A[1]], color="green", linewidth=2)
    ax.plot([C[0],B[0]], [C[1],B[1]], color="green", linewidth=2,
            label=f"Inscribed angle = {central_deg/2:.1f}°")

    for pt, lbl in [(A,"A"),(B,"B"),(C,"C")]:
        ax.plot(pt[0], pt[1], "o", color="crimson", markersize=10)
        ax.annotate(f"  {lbl}", pt, fontsize=11, fontweight="bold")

    arc_t = np.linspace(-half, half, 100)
    arc_r = r * 0.28
    ax.plot(arc_r*np.cos(arc_t), arc_r*np.sin(arc_t),
            color="crimson", linewidth=2)
    ax.text(arc_r*0.65, 0, f"{central_deg:.0f}°",
            ha="center", fontsize=10, color="crimson")

    ax.set_xlim(-r-0.6, r+0.6)
    ax.set_ylim(-r-0.6, r+0.6)
    ax.set_aspect("equal")
    ax.set_title("Inscribed angle = Central angle / 2", fontsize=13)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def olympiad_theorems():
    print(f"\n{'='*50}")
    print(f"OLYMPIAD THEOREMS")
    print(f"{'='*50}")
    print(f"")
    print(f"  These three results are rarely in school textbooks")
    print(f"  but appear constantly in math olympiads.")
    print(f"  They're elegant, not hard — and once you know them,")
    print(f"  you'll spot opportunities to use them everywhere.")
    print(f"")
    print(f"  1 — Ceva's Theorem      (when three cevians meet)")
    print(f"  2 — Menelaus' Theorem   (when three points are collinear)")
    print(f"  3 — Triangle inequality (and olympiad applications)")
    print(f"")
    choice = input("  Enter 1, 2, or 3: ")

    if choice == "1":
        ceva_theorem()
    elif choice == "2":
        menelaus_theorem()
    elif choice == "3":
        triangle_inequality()
    else:
        print(f"  Invalid choice.")


def ceva_theorem():
    print(f"\n{'='*50}")
    print(f"CEVA'S THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  A cevian is a line segment from a vertex of a triangle")
    print(f"  to a point on the opposite side (or its extension).")
    print(f"  Medians, altitudes, angle bisectors — all cevians.")
    print(f"")
    print(f"  Ceva's theorem (Giovanni Ceva, 1678):")
    print(f"  Three cevians AD, BE, CF are concurrent")
    print(f"  (all pass through the same point) if and only if:")
    print(f"")
    print(f"      (AF/FB) · (BD/DC) · (CE/EA) = 1")
    print(f"")
    print(f"  This one condition replaces pages of coordinate geometry.")
    print(f"  It works for any three cevians — you just check the product.")
    print(f"")
    print(f"  Famous applications:")
    print(f"  · Medians: each divides the opposite side 1:1")
    print(f"    (1/1)·(1/1)·(1/1) = 1 ✓ → medians are concurrent")
    print(f"    They meet at the centroid (center of mass).")
    print(f"")
    print(f"  · Angle bisectors: each divides opposite side in ratio")
    print(f"    of the adjacent sides (angle bisector theorem).")
    print(f"    The product still equals 1 ✓ → concurrent at incenter.")
    print(f"")
    print(f"  · Altitudes: a bit less obvious, but the product = 1.")
    print(f"    They meet at the orthocenter.")
    print(f"")
    print(f"  Enter the six segments:")

    AF = float(input("  AF: "))
    FB = float(input("  FB: "))
    BD = float(input("  BD: "))
    DC = float(input("  DC: "))
    CE = float(input("  CE: "))
    EA = float(input("  EA: "))

    product = (AF/FB) * (BD/DC) * (CE/EA)

    print(f"\n--- Ceva's condition ---")
    print(f"  (AF/FB) · (BD/DC) · (CE/EA)")
    print(f"  = ({AF}/{FB}) · ({BD}/{DC}) · ({CE}/{EA})")
    print(f"  = {AF/FB:.4f} · {BD/DC:.4f} · {CE/EA:.4f}")
    print(f"  = {product:.6f}")
    print(f"")
    if abs(product - 1) < 1e-6:
        print(f"  = 1 ✓ — the three cevians ARE concurrent.")
        print(f"  All three meet at a single point.")
    else:
        print(f"  ≠ 1 — the three cevians are NOT concurrent.")
        print(f"  They form a small triangle (called the cevian triangle).")
        print(f"  How far from concurrent: {abs(product-1):.6f}")


def menelaus_theorem():
    print(f"\n{'='*50}")
    print(f"MENELAUS' THEOREM")
    print(f"{'='*50}")
    print(f"")
    print(f"  Menelaus' theorem is the companion to Ceva's.")
    print(f"  Instead of asking when cevians are concurrent,")
    print(f"  it asks when three points on the sides are collinear.")
    print(f"")
    print(f"  If D, E, F lie on sides BC, CA, AB")
    print(f"  (or their extensions), they are collinear if and only if:")
    print(f"")
    print(f"      |AF/FB| · |BD/DC| · |CE/EA| = 1")
    print(f"  with an odd number of the three points on extensions.")
    print(f"")
    print(f"  The contrast with Ceva is beautiful:")
    print(f"  · Ceva:     product = 1,  even number on extensions")
    print(f"  · Menelaus: product = 1,  odd number on extensions")
    print(f"  Same equation, different geometry.")
    print(f"")
    print(f"  Menelaus is powerful for proving collinearity —")
    print(f"  one of the hardest things to show in olympiad geometry.")
    print(f"")

    AF = float(input("  AF: "))
    FB = float(input("  FB: "))
    BD = float(input("  BD: "))
    DC = float(input("  DC: "))
    CE = float(input("  CE: "))
    EA = float(input("  EA: "))

    product = (AF/FB) * (BD/DC) * (CE/EA)

    print(f"\n--- Menelaus' condition ---")
    print(f"  |AF/FB| · |BD/DC| · |CE/EA|")
    print(f"  = {AF/FB:.4f} · {BD/DC:.4f} · {CE/EA:.4f}")
    print(f"  = {product:.6f}")
    print(f"")
    if abs(product - 1) < 1e-6:
        print(f"  = 1 ✓ — D, E, F ARE collinear.")
        print(f"  The three points lie on a single straight line.")
    else:
        print(f"  ≠ 1 — D, E, F are NOT collinear.")
        print(f"  They form a triangle, not a line.")
        print(f"  Distance from 1: {abs(product-1):.6f}")


def triangle_inequality():
    print(f"\n{'='*50}")
    print(f"TRIANGLE INEQUALITY")
    print(f"{'='*50}")
    print(f"")
    print(f"  The triangle inequality is one of the most used")
    print(f"  results in all of mathematics — not just geometry.")
    print(f"")
    print(f"  For any triangle with sides a, b, c:")
    print(f"      a < b + c,   b < a + c,   c < a + b")
    print(f"  Or more compactly: |a-b| < c < a+b")
    print(f"")
    print(f"  Geometrically: the straight-line path between two points")
    print(f"  is always shorter than any detour via a third point.")
    print(f"  It's the most intuitive theorem in geometry.")
    print(f"")
    print(f"  In olympiads it appears in three ways:")
    print(f"")
    print(f"  1. EXISTENCE: show that three expressions can form a triangle")
    print(f"     → then use properties of that triangle")
    print(f"")
    print(f"  2. BOUNDING: if a,b,c are sides, then")
    print(f"     each side is bounded by the sum of the other two")
    print(f"")
    print(f"  3. METRIC SPACE: in any distance, d(A,C) ≤ d(A,B)+d(B,C)")
    print(f"     This generalizes to vectors, functions, and beyond.")
    print(f"")

    a = float(input("  Side a: "))
    b = float(input("  Side b: "))
    c = float(input("  Side c: "))

    print(f"\n--- Checking the three inequalities ---")
    t1 = a+b > c
    t2 = a+c > b
    t3 = b+c > a
    print(f"  a+b > c:  {a+b:.4f} > {c}?  {'✓' if t1 else '✗'}")
    print(f"  a+c > b:  {a+c:.4f} > {b}?  {'✓' if t2 else '✗'}")
    print(f"  b+c > a:  {b+c:.4f} > {a}?  {'✓' if t3 else '✗'}")
    print(f"")

    if t1 and t2 and t3:
        s    = (a+b+c)/2
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        print(f"  Valid triangle ✓  Area = {area:.4f}")
        print(f"")
        margins = [a+b-c, a+c-b, b+c-a]
        min_m   = min(margins)
        print(f"  Margins (how far from degenerate):")
        print(f"  a+b-c = {margins[0]:.4f}")
        print(f"  a+c-b = {margins[1]:.4f}")
        print(f"  b+c-a = {margins[2]:.4f}")
        print(f"  Smallest margin: {min_m:.4f}")
        if min_m < 0.05 * max(a,b,c):
            print(f"  Very close to degenerate — nearly collinear.")
        else:
            print(f"  Comfortably a proper triangle.")
    else:
        print(f"  Not a valid triangle.")
        if a+b == c or a+c == b or b+c == a:
            print(f"  Degenerate case: the points are collinear.")
        else:
            print(f"  The longest side exceeds the sum of the other two.")


def polygons():
    print(f"\n{'='*50}")
    print(f"POLYGONS")
    print(f"{'='*50}")
    print(f"")
    print(f"  A polygon is any closed figure made of straight sides.")
    print(f"  The key insight: every polygon can be cut into triangles.")
    print(f"  An n-gon can be divided into (n-2) triangles.")
    print(f"  Each triangle contributes 180°.")
    print(f"  So the interior angle sum is always (n-2)·180°.")
    print(f"")
    print(f"  For a REGULAR polygon (all sides and angles equal):")
    print(f"  · Each interior angle = (n-2)·180° / n")
    print(f"  · Each exterior angle = 360° / n")
    print(f"  · Exterior angles always sum to 360° — for any polygon.")
    print(f"    This is because walking around the polygon you turn")
    print(f"    a full circle — exactly 360°.")
    print(f"")

    n = int(input("  Number of sides n: "))

    if n < 3:
        print(f"  A polygon needs at least 3 sides.")
        return

    angle_sum     = (n-2) * 180
    each_interior = angle_sum / n
    each_exterior = 360 / n

    names = {3:"Triangle", 4:"Quadrilateral", 5:"Pentagon",
             6:"Hexagon", 7:"Heptagon", 8:"Octagon",
             9:"Nonagon", 10:"Decagon", 12:"Dodecagon"}
    name = names.get(n, f"{n}-gon")

    print(f"\n--- {name} ---")
    print(f"  Interior angle sum: ({n}-2)·180° = {angle_sum}°")
    print(f"  Each interior angle (regular): {each_interior:.4f}°")
    print(f"  Each exterior angle (regular): {each_exterior:.4f}°")
    print(f"  Exterior angle sum: {n}·{each_exterior:.4f}° = 360° ✓")

    print(f"\n--- Diagonals ---")
    diagonals = n*(n-3)//2
    print(f"  Number of diagonals = n(n-3)/2 = {diagonals}")
    print(f"  Each vertex connects to n-3={n-3} non-adjacent vertices.")
    print(f"  (n-1 other vertices, minus 2 adjacent = n-3)")

    print(f"\n--- Area of regular {name} ---")
    s    = float(input("  Side length s: "))
    area = (n * s**2) / (4 * math.tan(math.pi/n))
    perim = n * s
    print(f"  Area = (n·s²) / (4·tan(π/n))")
    print(f"       = ({n}·{s}²) / (4·tan(π/{n}))")
    print(f"       = {area:.4f}")
    print(f"  Perimeter = {n}·{s} = {perim:.4f}")
    print(f"")
    print(f"  As n → ∞, the regular polygon approaches a circle.")
    print(f"  Its area approaches πr² and perimeter approaches 2πr.")
    print(f"  This is one way to understand π geometrically.")

    plot_polygon(n, s)


def plot_polygon(n, s):
    R      = s / (2 * math.sin(math.pi/n))
    angles = [2*math.pi*k/n - math.pi/2 for k in range(n)]
    xs     = [R*math.cos(a) for a in angles]
    ys     = [R*math.sin(a) for a in angles]

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.fill(xs, ys, alpha=0.15, color="steelblue")
    ax.plot(xs+[xs[0]], ys+[ys[0]],
            color="steelblue", linewidth=2)

    for i in range(n):
        ax.plot(xs[i], ys[i], "o", color="crimson", markersize=8)

    # diagonals (lightly)
    for i in range(n):
        for j in range(i+2, n):
            if not (i == 0 and j == n-1):
                ax.plot([xs[i],xs[j]], [ys[i],ys[j]],
                        color="gray", linewidth=0.5,
                        linestyle="--", alpha=0.35)

    # circumscribed circle
    t = np.linspace(0, 2*np.pi, 400)
    ax.plot(R*np.cos(t), R*np.sin(t),
            color="orange", linewidth=1, linestyle=":",
            alpha=0.6, label=f"Circumcircle R={R:.2f}")

    ax.set_aspect("equal")
    ax.set_title(f"Regular {n}-gon  (side={s:.2f},  R={R:.2f})", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def euclidean_geometry():
    print(f"\n{'='*50}")
    print(f"EUCLIDEAN GEOMETRY")
    print(f"{'='*50}")
    print(f"")
    print(f"  Euclidean geometry is the mathematics of shapes in the")
    print(f"  flat plane — the geometry you see around you every day.")
    print(f"  Euclid systematized it around 300 BC in his Elements,")
    print(f"  one of the most read books in history after the Bible.")
    print(f"  For 2000 years it was THE model of rigorous reasoning.")
    print(f"")
    print(f"  Everything follows from five simple postulates.")
    print(f"  The fifth — about parallel lines — turned out to be")
    print(f"  independent of the others. When mathematicians tried")
    print(f"  to prove it from the first four, they instead discovered")
    print(f"  entirely new geometries: spherical, hyperbolic.")
    print(f"  The universe itself turns out to be non-Euclidean.")
    print(f"  But for everyday flat geometry: Euclid is still king.")
    print(f"")
    print(f"  What would you like to explore?")
    print(f"  1 — Triangles       Pythagoras, Heron, Euler's formula")
    print(f"  2 — Thales theorem  proportions and semicircle angle")
    print(f"  3 — Circle geometry angles, chords, tangents")
    print(f"  4 — Polygons        angle sums, regular polygons, diagonals")
    print(f"  5 — Olympiad theorems  Ceva, Menelaus, triangle inequality")
    print(f"")
    choice = input("  Enter 1, 2, 3, 4, or 5: ")

    if choice == "1":
        triangle_analyzer()
    elif choice == "2":
        thales_theorem()
    elif choice == "3":
        circle_geometry()
    elif choice == "4":
        polygons()
    elif choice == "5":
        olympiad_theorems()
    else:
        print(f"  Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    euclidean_geometry()
