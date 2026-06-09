import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import style


# ── Plot helpers ──────────────────────────────────────────────────────────────

def styled_ax(ax, fig):
    fig.patch.set_facecolor("#fdfaf5")
    ax.set_facecolor("#fdfaf5")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color("#e0d8cc")
    ax.spines["left"].set_color("#e0d8cc")
    ax.tick_params(colors="#4a4540", labelsize=8.5)
    ax.axhline(0, color="#1a1814", linewidth=0.6)
    ax.axvline(0, color="#1a1814", linewidth=0.6)
    ax.grid(True, alpha=0.2, color="#e0d8cc")


# ── LINE ─────────────────────────────────────────────────────────────────────

def solve_line(mode, **kw):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    add("The line",
        """A line is the simplest object in the coordinate plane —
a constant direction forever.<br><br>
<span class="mf">y = mx + q</span><br><br>
<strong>m</strong> is the slope (steepness and direction).<br>
<strong>q</strong> is the y-intercept (where it crosses the y-axis).<br><br>
m &gt; 0 → rising &nbsp;·&nbsp; m &lt; 0 → falling &nbsp;·&nbsp;
m = 0 → horizontal &nbsp;·&nbsp; m undefined → vertical<br><br>
<em>Note: m = tan(θ) where θ is the angle with the x-axis —
trigonometry and geometry, connected.</em>""",
        "warm")

    m = q = None

    if mode == "mq":
        m, q = kw["m"], kw["q"]
        direction = "rises" if m > 0 else "falls" if m < 0 else "is horizontal"
        body = (f"<span class='mf'>y = {m:g}x + {q:g}</span><br><br>"
                f"Slope = {m:g} → the line {direction} from left to right.<br>"
                f"y-intercept: (0, {q:g})")
        if m != 0:
            xi = -q / m
            body += f"<br>x-intercept: ({xi:.4f}, 0)"
        add("The line", body)

    elif mode == "two_points":
        x1, y1, x2, y2 = kw["x1"], kw["y1"], kw["x2"], kw["y2"]
        if x2 == x1:
            add("Vertical line",
                f"x₁ = x₂ = {x1:g} → <strong>vertical line: x = {x1:g}</strong><br>"
                "Vertical lines have undefined slope and cannot be written as y = mx + q.",
                "sage")
            return {"steps": steps, "m": None, "q": None, "vertical": x1,
                    "points": [(x1,y1),(x2,y2)]}
        m = (y2 - y1) / (x2 - x1)
        q = y1 - m * x1
        add("Step 1 — Compute the slope",
            f"m = (y₂ − y₁) / (x₂ − x₁) = ({y2:g} − {y1:g}) / ({x2:g} − {x1:g})"
            f" = <strong>{m:.4f}</strong>")
        add("Step 2 — Find q",
            f"Plug ({x1:g}, {y1:g}) into y = mx + q:<br>"
            f"{y1:g} = {m:.4f}·{x1:g} + q &nbsp;→ &nbsp;q = <strong>{q:.4f}</strong>")
        add("Result", f"<span class='mf'>y = {m:.4f}x + {q:.4f}</span>", "sage")

    elif mode == "point_slope":
        x1, y1, m = kw["x1"], kw["y1"], kw["m"]
        q = y1 - m * x1
        add("Point-slope form",
            f"y − y₁ = m(x − x₁)<br>"
            f"y − {y1:g} = {m:g}(x − {x1:g})<br>"
            f"y = {m:g}x + {q:.4f}", "sage")

    if m is not None:
        add("Parallel and perpendicular",
            f"<strong>Parallel</strong> lines have the same slope: m = {m:.4f}<br><br>"
            + (f"<strong>Perpendicular</strong> slope: m⊥ = −1/m = {-1/m:.4f}<br>"
               "Because rotating a direction 90° inverts and negates the slope."
               if m != 0 else
               "The perpendicular to a horizontal line is vertical."))

    return {"steps": steps, "m": m, "q": q, "vertical": None,
            "points": list(kw.get("extra_points", []))}


def plot_line(r):
    fig, ax = plt.subplots(figsize=(6, 6))
    styled_ax(ax, fig)
    ax.set_aspect("equal")

    if r["vertical"] is not None:
        ax.axvline(r["vertical"], color="#e8602a", linewidth=2.2,
                   label=f"x = {r['vertical']:g}")
    elif r["m"] is not None:
        x_v = np.linspace(-10, 10, 400)
        ax.plot(x_v, r["m"]*x_v + r["q"], color="#e8602a", linewidth=2.2,
                label=f"y = {r['m']:.4g}x + {r['q']:.4g}")

    for px, py in r.get("points", []):
        ax.plot(px, py, "o", color="#c8a96e", markersize=9, zorder=5)
        ax.annotate(f"  ({px:g},{py:g})", (px, py), fontsize=9,
                    color="#4a4540", fontfamily="serif")

    ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


# ── CIRCLE ────────────────────────────────────────────────────────────────────

def solve_circle(mode, **kw):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    add("The circle",
        """A circle is the set of all points at the same distance from a fixed centre.<br><br>
<span class="mf">(x − a)² + (y − b)² = r²</span><br><br>
This is just the Pythagorean theorem — the distance from any point (x,y)
on the circle to the centre (a,b) must equal r.<br><br>
<em>Thales' theorem: take any diameter and any other point on the circle —
the angle at that point is always exactly 90°. Always.</em>""",
        "warm")

    a = b = r = None

    if mode == "center_radius":
        a, b, r = kw["a"], kw["b"], kw["r"]
        if r <= 0:
            add("Error", "Radius must be positive.", "error")
            return {"steps": steps, "a": 0, "b": 0, "r": 1, "points": []}
        d_coeff, e_coeff = -2*a, -2*b
        f_coeff = a**2 + b**2 - r**2
        add("The circle",
            f"<span class='mf'>(x − {a:g})² + (y − {b:g})² = {r:g}² = {r**2:g}</span><br><br>"
            f"Centre: ({a:g}, {b:g}) &nbsp;·&nbsp; Radius: {r:g}<br>"
            f"Circumference: 2πr = {2*math.pi*r:.4f}<br>"
            f"Area: πr² = {math.pi*r**2:.4f}<br><br>"
            f"General form: x² + y² + {d_coeff:g}x + {e_coeff:g}y + {f_coeff:g} = 0", "sage")

    elif mode == "general":
        d, e, f = kw["d"], kw["e"], kw["f"]
        a, b = -d/2, -e/2
        r_sq = a**2 + b**2 - f
        add("Step 1 — Complete the square",
            f"x² + {d:g}x + y² + {e:g}y = {-f:g}<br><br>"
            f"For x: add ({d/2:g})² = {(d/2)**2:g} to both sides.<br>"
            f"For y: add ({e/2:g})² = {(e/2)**2:g} to both sides.<br><br>"
            f"(x − {a:g})² + (y − {b:g})² = {r_sq:g}")
        if r_sq < 0:
            add("No real circle", "r² &lt; 0 — this equation has no real solution.", "error")
            return {"steps": steps, "a": 0, "b": 0, "r": 1, "points": []}
        r = math.sqrt(r_sq)
        add("Step 2 — Centre and radius",
            f"Centre: <strong>({a:g}, {b:g})</strong> &nbsp;·&nbsp; "
            f"Radius: √{r_sq:g} = <strong>{r:.4f}</strong>", "sage")

    # point position
    px, py = kw.get("px", a+r+1), kw.get("py", b)
    dist = math.sqrt((px-a)**2 + (py-b)**2)
    if abs(dist-r) < 1e-9:
        pos = "ON the circle"; pos_var = "sage"
    elif dist < r:
        pos = f"INSIDE the circle &nbsp;(distance from boundary: {r-dist:.4f})"; pos_var = ""
    else:
        pos = f"OUTSIDE the circle &nbsp;(distance from boundary: {dist-r:.4f})"; pos_var = ""

    add(f"Position of ({px:g}, {py:g})",
        f"d = √(({px:g}−{a:g})² + ({py:g}−{b:g})²) = {dist:.6f}<br>"
        f"r = {r:.6f}<br><br>"
        f"→ <strong>{pos}</strong>", pos_var)

    return {"steps": steps, "a": a, "b": b, "r": r, "points": [(px, py)]}


def plot_circle(r_data):
    a, b, r = r_data["a"], r_data["b"], r_data["r"]
    fig, ax = plt.subplots(figsize=(6, 6))
    styled_ax(ax, fig)
    ax.set_aspect("equal")

    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(a + r*np.cos(theta), b + r*np.sin(theta),
            color="#e8602a", linewidth=2.2,
            label=f"centre=({a:g},{b:g}), r={r:.2f}")
    ax.plot(a, b, "o", color="#e8602a", markersize=8)
    ax.plot([a, a+r], [b, b], color="#c8a96e", linewidth=1.5, linestyle="--")
    ax.text(a+r/2, b+0.2, f"r={r:.2f}", ha="center", fontsize=9, color="#4a4540")

    for px, py in r_data.get("points", []):
        dist = math.sqrt((px-a)**2 + (py-b)**2)
        col = "#3d6b5e" if abs(dist-r)<1e-9 else "#c8a96e" if dist<r else "#e8602a"
        ax.plot(px, py, "o", color=col, markersize=9, zorder=5)
        ax.annotate(f"  ({px:g},{py:g})", (px, py), fontsize=9,
                    color="#4a4540", fontfamily="serif")

    lim = max(abs(a)+r+2, abs(b)+r+2, 5)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.legend(fontsize=8.5, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc")
    plt.tight_layout()
    return fig


# ── PARABOLA ──────────────────────────────────────────────────────────────────

def solve_parabola(a, b, c):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    add("The parabola",
        f"""<span class="mf" style="display:block;text-align:center;
font-size:1.2rem;padding:0.5rem;background:var(--bg2);border-radius:6px;">
  y = {a:g}x² + {b:g}x + {c:g}
</span><br>
A parabola is the set of all points equidistant from a fixed point (focus)
and a fixed line (directrix). This is what gives it the reflecting property —
satellite dishes, headlights, and telescope mirrors are all parabolic.""",
        "warm")

    h = -b / (2*a)
    k = a*h**2 + b*h + c
    extremum = "minimum" if a > 0 else "maximum"
    add("Step 1 — Vertex",
        f"h = −b / 2a = −{b:g} / {2*a:g} = <strong>{h:.4f}</strong><br>"
        f"k = {a:g}·{h:.4f}² + {b:g}·{h:.4f} + {c:g} = <strong>{k:.4f}</strong><br><br>"
        f"Vertex: <strong>({h:.4f}, {k:.4f})</strong> — this is a <strong>{extremum}</strong>.<br>"
        f"Vertex form: y = {a:g}(x − {h:.4f})² + {k:.4f}")

    p = 1 / (4*a)
    focus = (h, k+p)
    directrix = k - p
    add("Step 2 — Focus and directrix",
        f"p = 1/(4a) = 1/(4·{a:g}) = {p:.4f}<br><br>"
        f"Focus: <strong>({focus[0]:.4f}, {focus[1]:.4f})</strong><br>"
        f"Directrix: <span class='mf'>y = {directrix:.4f}</span><br><br>"
        f"Every point on the parabola is exactly {abs(p):.4f} units from both.")

    delta = b**2 - 4*a*c
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        intercepts_body = f"Δ = {delta:.4f} &gt; 0 → two x-intercepts:<br>x₁ = <strong>{x1:.4f}</strong>, x₂ = <strong>{x2:.4f}</strong>"
        x_pts = [(x1,0),(x2,0)]
    elif delta == 0:
        x1 = -b / (2*a)
        intercepts_body = f"Δ = 0 → one x-intercept (tangent to x-axis): x = <strong>{x1:.4f}</strong>"
        x_pts = [(x1,0)]
    else:
        intercepts_body = f"Δ = {delta:.4f} &lt; 0 → no x-intercepts. The parabola stays entirely {'above' if a>0 else 'below'} the x-axis."
        x_pts = []

    add("Step 3 — Intercepts",
        f"y-intercept: (0, {c:g})<br><br>{intercepts_body}", "sage")

    return {"steps": steps, "a": a, "b": b, "c": c,
            "h": h, "k": k, "focus": focus, "directrix": directrix,
            "x_pts": x_pts}


def plot_parabola(r):
    a, b, c = r["a"], r["b"], r["c"]
    h, k    = r["h"], r["k"]
    spread  = max(abs(h)+5, 6)

    x_v = np.linspace(h-spread, h+spread, 400)
    y_v = a*x_v**2 + b*x_v + c

    fig, ax = plt.subplots(figsize=(7, 6))
    styled_ax(ax, fig)

    ax.plot(x_v, y_v, color="#e8602a", linewidth=2.2,
            label=f"y = {a:g}x² + {b:g}x + {c:g}")
    ax.plot(h, k, "o", color="#c8a96e", markersize=10, zorder=5,
            label=f"Vertex ({h:.2f}, {k:.2f})")
    ax.plot(*r["focus"], "^", color="#3d6b5e", markersize=9, zorder=5,
            label=f"Focus ({r['focus'][0]:.2f}, {r['focus'][1]:.2f})")
    x_dir = np.linspace(h-spread, h+spread, 100)
    ax.plot(x_dir, [r["directrix"]]*100, color="#7b6fb0", linewidth=1.5,
            linestyle="--", label=f"Directrix y={r['directrix']:.2f}")
    ax.axvline(h, color="#b0a090", linewidth=0.8, linestyle=":")
    for xi, yi in r["x_pts"]:
        ax.plot(xi, yi, "o", color="#c8a96e", markersize=8, zorder=5)
    ax.plot(0, c, "o", color="#4a4540", markersize=7, zorder=5)

    y_range = max(abs(a)*spread**2, 5)
    ax.set_ylim(k-y_range, k+y_range)
    ax.set_xlim(h-spread, h+spread)
    ax.legend(fontsize=8, framealpha=0.7,
              facecolor="#fdfaf5", edgecolor="#e0d8cc", loc="upper right")
    plt.tight_layout()
    return fig


# ── DISTANCES ─────────────────────────────────────────────────────────────────

def solve_distance(mode, **kw):
    steps = []
    def add(label, body, variant=""):
        steps.append((label, body, variant))

    if mode == "distance":
        x1,y1,x2,y2 = kw["x1"],kw["y1"],kw["x2"],kw["y2"]
        dx, dy = x2-x1, y2-y1
        d = math.sqrt(dx**2+dy**2)
        add("Distance formula",
            "The distance formula is the Pythagorean theorem applied to coordinates.<br>"
            "The horizontal leg is |Δx|, the vertical leg is |Δy|, "
            "and the distance is the hypotenuse.",
            "warm")
        add("Computation",
            f"d = √((x₂−x₁)² + (y₂−y₁)²)<br>"
            f"  = √(({x2:g}−{x1:g})² + ({y2:g}−{y1:g})²)<br>"
            f"  = √({dx:g}² + {dy:g}²)<br>"
            f"  = √{dx**2+dy**2:g}<br>"
            f"  = <strong>{d:.6f}</strong>", "sage")
        return {"steps": steps, "mode": mode,
                "pts": [(x1,y1),(x2,y2)], "d": d}

    elif mode == "midpoint":
        x1,y1,x2,y2 = kw["x1"],kw["y1"],kw["x2"],kw["y2"]
        mx, my = (x1+x2)/2, (y1+y2)/2
        add("Midpoint formula",
            "The midpoint is simply the average of the coordinates.",
            "warm")
        add("Computation",
            f"M = (({x1:g}+{x2:g})/2, ({y1:g}+{y2:g})/2)<br>"
            f"  = <strong>({mx:.4f}, {my:.4f})</strong>", "sage")
        return {"steps": steps, "mode": mode,
                "pts": [(x1,y1),(x2,y2)], "mx": mx, "my": my}

    elif mode == "two_lines":
        m1,q1,m2,q2 = kw["m1"],kw["q1"],kw["m2"],kw["q2"]
        add("Intersection of two lines",
            "Set the two equations equal, solve for x, then find y.",
            "warm")
        if m1 == m2:
            verdict = ("The lines are <strong>identical</strong> — infinite intersections."
                       if q1==q2 else
                       "The lines are <strong>parallel</strong> — no intersection.")
            add("Result", verdict, "error")
            return {"steps": steps, "mode": mode,
                    "m1":m1,"q1":q1,"m2":m2,"q2":q2, "xi":None,"yi":None}
        xi = (q2-q1)/(m1-m2)
        yi = m1*xi+q1
        add("Computation",
            f"{m1:g}x + {q1:g} = {m2:g}x + {q2:g}<br>"
            f"({m1:g}−{m2:g})x = {q2:g}−{q1:g}<br>"
            f"x = {q2-q1:g}/{m1-m2:g} = <strong>{xi:.4f}</strong><br>"
            f"y = {m1:g}·{xi:.4f} + {q1:g} = <strong>{yi:.4f}</strong>", "sage")
        return {"steps": steps, "mode": mode,
                "m1":m1,"q1":q1,"m2":m2,"q2":q2,"xi":xi,"yi":yi}

    elif mode == "line_circle":
        m,q,a,b,r = kw["m"],kw["q"],kw["a"],kw["b"],kw["r"]
        A = 1+m**2
        B = -2*a+2*m*(q-b)
        C = a**2+(q-b)**2-r**2
        delta = B**2-4*A*C
        add("Strategy",
            "Substitute y = mx+q into the circle equation.<br>"
            "You get a quadratic in x — its discriminant tells the story:<br>"
            "Δ&gt;0 secant · Δ=0 tangent · Δ&lt;0 external",
            "warm")
        add("The quadratic",
            f"After substitution: <span class='mf'>{A:.4g}x² + {B:.4g}x + {C:.4g} = 0</span><br>"
            f"Δ = {delta:.4f}")

        pts = []
        if delta < 0:
            add("Result", "Δ &lt; 0 → <strong>no intersection</strong>. The line misses the circle.", "error")
        elif abs(delta) < 1e-9:
            xi = -B/(2*A); yi = m*xi+q
            pts = [(xi,yi)]
            add("Result",
                f"Δ = 0 → <strong>tangent</strong>. Tangent point: ({xi:.4f}, {yi:.4f})<br>"
                "At this point the radius is perpendicular to the line — a fundamental theorem.",
                "sage")
        else:
            x1=(-B+math.sqrt(delta))/(2*A); y1=m*x1+q
            x2=(-B-math.sqrt(delta))/(2*A); y2=m*x2+q
            pts = [(x1,y1),(x2,y2)]
            chord = math.sqrt((x2-x1)**2+(y2-y1)**2)
            add("Result",
                f"Δ &gt; 0 → <strong>secant</strong>. Two intersection points:<br>"
                f"P₁ = ({x1:.4f}, {y1:.4f})<br>"
                f"P₂ = ({x2:.4f}, {y2:.4f})<br>"
                f"Chord length: {chord:.4f}", "sage")

        return {"steps": steps, "mode": mode,
                "m":m,"q":q,"a":a,"b":b,"r":r, "pts":pts}


def plot_distances(r):
    mode = r["mode"]
    fig, ax = plt.subplots(figsize=(7, 6))
    styled_ax(ax, fig)
    ax.set_aspect("equal")

    if mode == "distance":
        (x1,y1),(x2,y2) = r["pts"]
        ax.plot([x1,x2],[y1,y2], color="#e8602a", linewidth=2.2,
                label=f"d = {r['d']:.4f}")
        ax.plot([x1,x2],[y1,y1], color="#c8a96e", linewidth=1.5, linestyle="--")
        ax.plot([x2,x2],[y1,y2], color="#3d6b5e", linewidth=1.5, linestyle="--")
        for px,py in r["pts"]:
            ax.plot(px,py,"o",color="#1a1814",markersize=9,zorder=5)
            ax.annotate(f"  ({px:g},{py:g})",(px,py),fontsize=9,color="#4a4540")

    elif mode == "midpoint":
        (x1,y1),(x2,y2) = r["pts"]
        ax.plot([x1,x2],[y1,y2],color="#e8602a",linewidth=2.2)
        ax.plot(r["mx"],r["my"],"o",color="#3d6b5e",markersize=11,zorder=5,
                label=f"M ({r['mx']:.2f}, {r['my']:.2f})")
        for px,py in r["pts"]:
            ax.plot(px,py,"o",color="#c8a96e",markersize=9,zorder=5)
            ax.annotate(f"  ({px:g},{py:g})",(px,py),fontsize=9,color="#4a4540")

    elif mode == "two_lines":
        x_v = np.linspace(-10,10,400)
        ax.plot(x_v, r["m1"]*x_v+r["q1"], color="#e8602a", linewidth=2.2,
                label=f"y={r['m1']:g}x+{r['q1']:g}")
        ax.plot(x_v, r["m2"]*x_v+r["q2"], color="#3d6b5e", linewidth=2.2,
                label=f"y={r['m2']:g}x+{r['q2']:g}")
        if r["xi"] is not None:
            ax.plot(r["xi"],r["yi"],"o",color="#c8a96e",markersize=11,zorder=5,
                    label=f"({r['xi']:.2f},{r['yi']:.2f})")
        ax.set_xlim(-10,10); ax.set_ylim(-10,10)

    elif mode == "line_circle":
        m,q,a,b,r_c = r["m"],r["q"],r["a"],r["b"],r["r"]
        theta = np.linspace(0,2*np.pi,400)
        ax.plot(a+r_c*np.cos(theta),b+r_c*np.sin(theta),
                color="#3d6b5e",linewidth=2.2,label=f"circle r={r_c:g}")
        x_v = np.linspace(a-r_c-2,a+r_c+2,400)
        ax.plot(x_v,m*x_v+q,color="#e8602a",linewidth=2.2,
                label=f"y={m:g}x+{q:g}")
        for i,(px,py) in enumerate(r["pts"]):
            col = "#c8a96e" if i==0 else "#7b6fb0"
            ax.plot(px,py,"o",color=col,markersize=10,zorder=5)
        lim=max(abs(a)+r_c+3,abs(b)+r_c+3,6)
        ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)

    ax.legend(fontsize=8.5,framealpha=0.7,
              facecolor="#fdfaf5",edgecolor="#e0d8cc")
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
            ["Line", "Circle", "Parabola", "Distances & Intersections"],
            key="ag_topic")

        if topic == "Line":
            mode = st.selectbox("Define by", ["Slope & intercept","Two points","Point & slope"], key="ag_lm")
            if mode == "Slope & intercept":
                m = st.number_input("Slope m", value=2.0, step=0.5, format="%.4g", key="ag_m")
                q = st.number_input("y-intercept q", value=-1.0, step=0.5, format="%.4g", key="ag_q")
                kw = dict(m=m, q=q)
            elif mode == "Two points":
                c1,c2 = st.columns(2)
                x1=c1.number_input("x₁",value=0.0,step=1.0,key="ag_x1"); y1=c2.number_input("y₁",value=1.0,step=1.0,key="ag_y1")
                x2=c1.number_input("x₂",value=2.0,step=1.0,key="ag_x2"); y2=c2.number_input("y₂",value=5.0,step=1.0,key="ag_y2")
                kw = dict(x1=x1,y1=y1,x2=x2,y2=y2)
            else:
                x1=st.number_input("x",value=1.0,step=1.0,key="ag_px"); y1=st.number_input("y",value=3.0,step=1.0,key="ag_py")
                m=st.number_input("Slope m",value=2.0,step=0.5,key="ag_pm")
                kw = dict(x1=x1,y1=y1,m=m)
            lm = {"Slope & intercept":"mq","Two points":"two_points","Point & slope":"point_slope"}[mode]

        elif topic == "Circle":
            mode = st.selectbox("Define by", ["Centre & radius","General form ax²+bx+..."], key="ag_cm")
            if mode == "Centre & radius":
                a=st.number_input("Centre x",value=0.0,step=1.0,key="ag_ca"); b=st.number_input("Centre y",value=0.0,step=1.0,key="ag_cb")
                r=st.number_input("Radius r",value=3.0,step=0.5,key="ag_cr")
                px=st.number_input("Test point x",value=1.0,step=1.0,key="ag_cpx"); py=st.number_input("Test point y",value=1.0,step=1.0,key="ag_cpy")
                ckw = dict(a=a,b=b,r=r,px=px,py=py); cm = "center_radius"
            else:
                d=st.number_input("d",value=-4.0,step=1.0,key="ag_cd"); e=st.number_input("e",value=6.0,step=1.0,key="ag_ce"); f=st.number_input("f",value=4.0,step=1.0,key="ag_cf")
                px=st.number_input("Test point x",value=1.0,step=1.0,key="ag_cpx2"); py=st.number_input("Test point y",value=1.0,step=1.0,key="ag_cpy2")
                ckw = dict(d=d,e=e,f=f,px=px,py=py); cm = "general"

        elif topic == "Parabola":
            a=st.number_input("a",value=1.0,step=0.5,format="%.4g",key="ag_pa")
            b=st.number_input("b",value=-4.0,step=0.5,format="%.4g",key="ag_pb")
            c=st.number_input("c",value=3.0,step=0.5,format="%.4g",key="ag_pc")

        else:  # Distances
            dm = st.selectbox("Compute",
                ["Distance between points","Midpoint","Intersect two lines","Line ∩ Circle"],
                key="ag_dm")
            if dm == "Distance between points":
                c1,c2=st.columns(2)
                x1=c1.number_input("x₁",value=0.0,key="ag_d1"); y1=c2.number_input("y₁",value=0.0,key="ag_d2")
                x2=c1.number_input("x₂",value=3.0,key="ag_d3"); y2=c2.number_input("y₂",value=4.0,key="ag_d4")
                dkw=dict(x1=x1,y1=y1,x2=x2,y2=y2); dm_mode="distance"
            elif dm == "Midpoint":
                c1,c2=st.columns(2)
                x1=c1.number_input("x₁",value=0.0,key="ag_m1"); y1=c2.number_input("y₁",value=0.0,key="ag_m2")
                x2=c1.number_input("x₂",value=4.0,key="ag_m3"); y2=c2.number_input("y₂",value=6.0,key="ag_m4")
                dkw=dict(x1=x1,y1=y1,x2=x2,y2=y2); dm_mode="midpoint"
            elif dm == "Intersect two lines":
                m1=st.number_input("m₁",value=2.0,step=0.5,key="ag_2m1"); q1=st.number_input("q₁",value=-1.0,step=0.5,key="ag_2q1")
                m2=st.number_input("m₂",value=-1.0,step=0.5,key="ag_2m2"); q2=st.number_input("q₂",value=5.0,step=0.5,key="ag_2q2")
                dkw=dict(m1=m1,q1=q1,m2=m2,q2=q2); dm_mode="two_lines"
            else:
                m=st.number_input("Line slope m",value=1.0,step=0.5,key="ag_lc_m"); q=st.number_input("Line q",value=0.0,step=0.5,key="ag_lc_q")
                a=st.number_input("Circle cx",value=0.0,key="ag_lc_a"); b=st.number_input("Circle cy",value=0.0,key="ag_lc_b"); r=st.number_input("Circle r",value=3.0,step=0.5,key="ag_lc_r")
                dkw=dict(m=m,q=q,a=a,b=b,r=r); dm_mode="line_circle"

        solve_btn = st.button("Analyze →", key="ag_solve")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="hint-panel">
  <div class="hint-label">Try these</div>
  <div class="hint-body">
    Line: <code>m=2, q=−1</code><br>
    Circle: <code>(0,0), r=3</code><br>
    Parabola: <code>1, −4, 3</code> → roots at 1,3<br>
    Line∩Circle: <code>m=1,q=0, (0,0),r=3</code>
  </div>
</div>
""", unsafe_allow_html=True)

    with right:
        if solve_btn:
            if topic == "Line":
                r_data = solve_line(lm, **kw)
                for label, body, variant in r_data["steps"]:
                    style.step(label, body, variant)
                st.markdown('<div class="graph-label">Graph</div>', unsafe_allow_html=True)
                st.pyplot(plot_line(r_data)); plt.close()

            elif topic == "Circle":
                r_data = solve_circle(cm, **ckw)
                for label, body, variant in r_data["steps"]:
                    style.step(label, body, variant)
                st.markdown('<div class="graph-label">Graph</div>', unsafe_allow_html=True)
                st.pyplot(plot_circle(r_data)); plt.close()

            elif topic == "Parabola":
                if a == 0:
                    st.error("a cannot be zero.")
                else:
                    r_data = solve_parabola(a, b, c)
                    for label, body, variant in r_data["steps"]:
                        style.step(label, body, variant)
                    style.result_band(
                        ("Vertex",    f"({r_data['h']:.3f}, {r_data['k']:.3f})"),
                        ("Focus",     f"({r_data['focus'][0]:.3f}, {r_data['focus'][1]:.3f})"),
                        ("Directrix", f"y = {r_data['directrix']:.3f}"),
                    )
                    st.markdown('<div class="graph-label">Graph</div>', unsafe_allow_html=True)
                    st.pyplot(plot_parabola(r_data)); plt.close()

            else:
                r_data = solve_distance(dm_mode, **dkw)
                for label, body, variant in r_data["steps"]:
                    style.step(label, body, variant)
                st.markdown('<div class="graph-label">Graph</div>', unsafe_allow_html=True)
                st.pyplot(plot_distances(r_data)); plt.close()
        else:
            style.empty_state("xy")