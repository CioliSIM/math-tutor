import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp
import streamlit as st
import style

x = sp.Symbol('x')

# ── Palette helper ────────────────────────────────────────────────────────────
def _pal(dark):
    return {
        "bg":   "#0f0e0c" if dark else "#f9f6f0",
        "bg2":  "#181510" if dark else "#f2ede4",
        "ink":  "#e8e0d4" if dark else "#1a1814",
        "ink2": "#9e9080" if dark else "#4a4540",
        "warm": "#d4703a" if dark else "#c8602a",
        "sage": "#4a8070" if dark else "#2d5a4e",
        "sand": "#b89848" if dark else "#a8893e",
        "bdr":  "#2a2620" if dark else "#ddd5c8",
        "card": "#161410" if dark else "#ffffff",
    }

def _ax(ax, fig, p):
    fig.patch.set_facecolor(p["bg"])
    ax.set_facecolor(p["bg"])
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["bottom"].set_color(p["bdr"])
    ax.spines["left"].set_color(p["bdr"])
    ax.tick_params(colors=p["ink2"], labelsize=8.5)
    ax.grid(True, alpha=0.15, color=p["bdr"])
    ax.axhline(0, color=p["ink2"], linewidth=0.5, alpha=0.5)

# ── Section: hook ─────────────────────────────────────────────────────────────
def section_hook(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:2.5rem;">
  <p style="font-family:'Fraunces',serif;font-size:1.45rem;font-weight:400;
            color:{p['ink']};line-height:1.55;margin:0 0 1.2rem;">
    In 1666, Isaac Newton was 23 years old and hiding from the plague.<br>
    Cambridge was closed. He had nothing to do but think.<br>
    What he thought changed physics forever.
  </p>
  <p style="font-size:1rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1rem;">
    The question he was obsessed with: planets move. Their speed changes constantly.
    How fast is a planet moving at <em>this exact moment</em> — not on average,
    not approximately, but right now, at this precise instant?
  </p>
  <p style="font-size:1rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0;">
    Average speed is easy — distance divided by time.
    But instantaneous speed? That's dividing by zero.
    And yet the tachometer in your car shows it. It's real.
    How do you compute something that involves dividing by zero?
  </p>
</div>
<div style="width:48px;height:2px;background:{p['warm']};margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── Section: from average to instantaneous ────────────────────────────────────
def section_average_to_instant(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The speedometer problem.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    Say your position at time t is f(t) = t² metres.
    Average speed over the interval [1, 1+h] is:
  </p>
  <div style="font-family:'Fraunces',serif;font-size:1.15rem;color:{p['ink']};
              background:{p['bg2']};border-radius:8px;padding:0.9rem 1.2rem;
              margin-bottom:1rem;border-left:3px solid {p['warm']};">
    [f(1+h) − f(1)] / h &nbsp;=&nbsp; [(1+h)² − 1] / h &nbsp;=&nbsp; 2 + h
  </div>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1.2rem;">
    Watch what happens as h gets smaller and smaller:
  </p>
</div>
""", unsafe_allow_html=True)

    # Live table
    rows = ""
    for exp in [0, -1, -2, -3, -4, -6]:
        h    = 10**exp
        rate = 2 + h
        rows += f"""
<tr>
  <td style="font-family:'DM Mono',monospace;padding:0.4rem 1rem;color:{p['sand']};">{h:g}</td>
  <td style="font-family:'DM Mono',monospace;padding:0.4rem 1rem;color:{p['ink2']};">{rate:.8f}</td>
  <td style="padding:0.4rem 1rem;color:{''+p['sage'] if exp<=-4 else p['ink2']};font-size:0.85rem;">
    {"→ converges to <strong>2</strong>" if exp<=-4 else ""}
  </td>
</tr>"""

    st.markdown(f"""
<div style="max-width:500px;margin-bottom:2rem;">
  <table style="border-collapse:collapse;width:100%;">
    <thead>
      <tr style="border-bottom:1px solid {p['bdr']};">
        <th style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;
                   text-transform:uppercase;color:{p['sand']};padding:0.4rem 1rem;text-align:left;">h</th>
        <th style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;
                   text-transform:uppercase;color:{p['sand']};padding:0.4rem 1rem;text-align:left;">average speed</th>
        <th></th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>
<div style="max-width:680px;margin-bottom:2.5rem;">
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    As h→0, the average speed approaches <strong style="color:{p['ink']};">exactly 2</strong>.
    That limiting value is the <strong style="color:{p['warm']};">derivative</strong> of f at t=1.
    Written f'(1) = 2.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0;">
    This is not an approximation. It's an exact limit — the slope of the curve
    at a single point, computed by approaching that point from both sides
    until the answer stabilises.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Section: geometric picture ────────────────────────────────────────────────
def section_geometry(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.2rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The geometric picture.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.8rem;">
    Draw the curve y=x². Draw a line through two points on the curve —
    that's the <em>secant</em>. Its slope is the average rate of change.
    As the two points get closer, the secant approaches the
    <strong style="color:{p['warm']};">tangent line</strong> at that point.
    The slope of the tangent is the derivative.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1.2rem;">
    In one sentence: <strong style="color:{p['ink']};">the derivative at a point is the slope of the 
    tangent to the curve at that point.</strong>
  </p>
</div>
""", unsafe_allow_html=True)

    # Plot: three secants converging to tangent
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    fig.patch.set_facecolor(p["bg"])
    xr = np.linspace(-0.2, 2.5, 300)

    for ax, h in zip(axes, [1.5, 0.5, 0.05]):
        _ax(ax, fig, p)
        ax.plot(xr, xr**2, color=p["sage"], linewidth=2.5, label="y = x²")
        x0, y0 = 1.0, 1.0
        x1, y1 = 1+h, (1+h)**2
        slope   = (y1-y0)/h
        xs = np.linspace(0.2, 1+h+0.2, 100)
        ax.plot(xs, y0+slope*(xs-x0), color=p["warm"], linewidth=2,
                linestyle="--", label=f"Secant (h={h})\nslope={slope:.2f}")
        xt = np.linspace(0.3, 1.7, 100)
        ax.plot(xt, y0+2*(xt-x0), color=p["sand"], linewidth=1.5,
                linestyle=":", alpha=0.8, label="Tangent (slope=2)")
        ax.plot(x0, y0, "o", color=p["ink"], markersize=8, zorder=5)
        ax.plot(x1, y1, "o", color=p["warm"], markersize=7, zorder=5)
        ax.set_xlim(-0.1, 2.5); ax.set_ylim(-0.3, 5)
        ax.set_title(f"h = {h}", fontsize=10, color=p["ink2"])
        ax.legend(fontsize=7.5, framealpha=0.8,
                  facecolor=p["bg2"], edgecolor=p["bdr"], loc="upper left")
        ax.set_xlabel("x", color=p["ink2"], fontsize=9)

    fig.suptitle("As h→0, the secant becomes the tangent",
                 fontsize=11, color=p["ink2"])
    plt.tight_layout()
    st.pyplot(fig); plt.close(fig)

    st.markdown(f"""
<div style="max-width:680px;margin:1.2rem 0 2.5rem;">
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0;">
    Watch the third panel — h=0.05. The secant and tangent are almost identical.
    At h=0 exactly, they coincide. That's the moment the derivative is born.
  </p>
</div>
<div style="width:48px;height:2px;background:{p['warm']};margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── Section: the definition ───────────────────────────────────────────────────
def section_definition(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The formal definition.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1rem;">
    Now that the idea is clear, the formula is just a precise way to write it:
  </p>
  <div style="font-family:'Fraunces',serif;font-size:1.3rem;color:{p['ink']};
              background:{p['bg2']};border-radius:8px;padding:1rem 1.4rem;
              margin-bottom:1.2rem;border-left:3px solid {p['warm']};line-height:1.8;">
    f'(x) = lim<sub>h→0</sub> [f(x+h) − f(x)] / h
  </div>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    Other notations — all mean exactly the same thing:
  </p>
  <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-bottom:1.2rem;">
    <div style="background:{p['bg2']};border:1px solid {p['bdr']};border-radius:8px;
                padding:0.7rem 1.1rem;text-align:center;">
      <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['ink']};">f'(x)</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;color:{p['sand']};
                  margin-top:0.2rem;letter-spacing:0.1em;text-transform:uppercase;">Lagrange</div>
    </div>
    <div style="background:{p['bg2']};border:1px solid {p['bdr']};border-radius:8px;
                padding:0.7rem 1.1rem;text-align:center;">
      <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['ink']};">df/dx</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;color:{p['sand']};
                  margin-top:0.2rem;letter-spacing:0.1em;text-transform:uppercase;">Leibniz</div>
    </div>
    <div style="background:{p['bg2']};border:1px solid {p['bdr']};border-radius:8px;
                padding:0.7rem 1.1rem;text-align:center;">
      <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['ink']};">ẋ</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.55rem;color:{p['sand']};
                  margin-top:0.2rem;letter-spacing:0.1em;text-transform:uppercase;">Newton</div>
    </div>
  </div>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 2.5rem;">
    Newton and Leibniz invented calculus independently in the 1660s-70s.
    They had a bitter dispute over priority that divided mathematics for decades.
    Today we use Leibniz's notation — it turns out to be more powerful,
    especially when working with functions of multiple variables.
  </p>
</div>
<div style="width:48px;height:2px;background:{p['warm']};margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── Section: rules ────────────────────────────────────────────────────────────
def section_rules(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The rules — discovered, not invented.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1.2rem;">
    Computing derivatives from the limit definition every time would take forever.
    Mathematicians derived general rules that work for any function.
    Each rule has a reason — not just a formula to memorize.
  </p>
</div>
""", unsafe_allow_html=True)

    rules = [
        ("Power rule", "xⁿ → n·xⁿ⁻¹",
         "Bring the exponent down, reduce by 1. Works for any real n — positive, negative, fractional. x²→2x, x³→3x², √x→1/(2√x)."),
        ("The miracle of eˣ", "eˣ → eˣ",
         "eˣ is its own derivative. The only function that grows at exactly the rate it currently has. This is not a coincidence — it's the defining property of e."),
        ("Product rule", "(f·g)' = f'g + fg'",
         "Think of area: f and g are sides of a rectangle. When both grow, the area grows by f'·g + f·g'. The tiny corner f'·g'·(dx)² vanishes."),
        ("Chain rule", "(f(g(x)))' = f'(g(x))·g'(x)",
         "Like gears: if gear A turns 3× as fast as your hand, and B turns 2× as fast as A, then B turns 6× as fast. Rates multiply."),
        ("sin and cos", "sin x → cos x → −sin x → −cos x → sin x",
         "A cycle of period 4. sin is its own fourth derivative. This is why oscillations — pendulums, waves, springs — all involve sin and cos."),
    ]

    for title, formula, note in rules:
        st.markdown(f"""
<div style="background:{p['card']};border:1px solid {p['bdr']};border-left:3px solid {p['warm']};
            border-radius:0 10px 10px 0;padding:1.1rem 1.4rem;margin-bottom:0.9rem;">
  <div style="font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.14em;
              text-transform:uppercase;color:{p['sand']};margin-bottom:0.4rem;">{title}</div>
  <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['ink']};
              margin-bottom:0.5rem;">{formula}</div>
  <div style="font-size:0.85rem;font-weight:300;color:{p['ink2']};line-height:1.7;">{note}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f'<div style="width:48px;height:2px;background:{p["warm"]};margin:2rem 0 2.5rem;"></div>',
                unsafe_allow_html=True)

# ── Section: interactive differentiation ─────────────────────────────────────
def section_interactive(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.2rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 0.8rem;">Try it.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 1rem;">
    Enter any function and see its derivative — along with the tangent at any point.
  </p>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        expr_str = st.text_input("f(x) =", value="x**3 - 3*x",
                                  key="d21_expr", label_visibility="visible")
    with col2:
        x_val = st.number_input("Evaluate at x =", value=1.0, step=0.5,
                                 key="d21_xval", label_visibility="visible")

    if expr_str.strip():
        try:
            expr   = sp.sympify(expr_str)
            deriv  = sp.simplify(sp.diff(expr, x))
            deriv2 = sp.simplify(sp.diff(deriv, x))
            val    = float(deriv.subs(x, x_val))
            f_val  = float(expr.subs(x, x_val))

            st.markdown(f"""
<div style="display:flex;gap:0;background:{p['ink']};border-radius:10px;
            overflow:hidden;margin:0.8rem 0 1.2rem;">
  <div style="flex:1;padding:0.9rem 1.2rem;border-right:1px solid rgba(255,255,255,0.06);">
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.14em;
                text-transform:uppercase;color:{p['sand']};margin-bottom:0.3rem;">f'(x)</div>
    <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['bg']};line-height:1.2;">{deriv}</div>
  </div>
  <div style="flex:1;padding:0.9rem 1.2rem;border-right:1px solid rgba(255,255,255,0.06);">
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.14em;
                text-transform:uppercase;color:{p['sand']};margin-bottom:0.3rem;">f''(x)</div>
    <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['bg']};line-height:1.2;">{deriv2}</div>
  </div>
  <div style="flex:1;padding:0.9rem 1.2rem;">
    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.14em;
                text-transform:uppercase;color:{p['sand']};margin-bottom:0.3rem;">slope at x={x_val}</div>
    <div style="font-family:'Fraunces',serif;font-size:1.1rem;color:{p['bg']};line-height:1.2;">{val:.4f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

            # Plot
            f_n  = sp.lambdify(x, expr,  "numpy")
            df_n = sp.lambdify(x, deriv, "numpy")
            x_r  = np.linspace(x_val-3, x_val+3, 400)
            y_f  = np.array(f_n(x_r),  dtype=float)
            y_df = np.array(df_n(x_r), dtype=float)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.patch.set_facecolor(p["bg"])
            for ax in [ax1, ax2]: _ax(ax, fig, p)

            ax1.plot(x_r, np.where(np.isfinite(y_f),y_f,np.nan),
                     color=p["sage"], linewidth=2.5, label="f(x)")
            tan = f_val + val*(x_r-x_val)
            ax1.plot(x_r, tan, color=p["warm"], linewidth=1.8,
                     linestyle="--", label=f"Tangent at x={x_val}")
            ax1.plot(x_val, f_val, "o", color=p["warm"], markersize=9, zorder=5)
            y_fin = y_f[np.isfinite(y_f)]
            if len(y_fin): ax1.set_ylim(np.percentile(y_fin,2), np.percentile(y_fin,98))
            ax1.legend(fontsize=8.5, framealpha=0.8,
                       facecolor=p["bg2"], edgecolor=p["bdr"])
            ax1.set_xlabel("x", color=p["ink2"], fontsize=9)
            ax1.set_title("Function and tangent", fontsize=10, color=p["ink2"])

            ax2.plot(x_r, np.where(np.isfinite(y_df),y_df,np.nan),
                     color=p["sand"], linewidth=2.5, label="f'(x)")
            ax2.axvline(x_val, color=p["warm"], linewidth=1.5,
                        linestyle="--", alpha=0.7)
            ax2.plot(x_val, val, "o", color=p["warm"], markersize=9, zorder=5,
                     label=f"f'({x_val}) = {val:.3f}")
            y_df_fin = y_df[np.isfinite(y_df)]
            if len(y_df_fin): ax2.set_ylim(np.percentile(y_df_fin,2), np.percentile(y_df_fin,98))
            ax2.legend(fontsize=8.5, framealpha=0.8,
                       facecolor=p["bg2"], edgecolor=p["bdr"])
            ax2.set_xlabel("x", color=p["ink2"], fontsize=9)
            ax2.set_title("Derivative", fontsize=10, color=p["ink2"])

            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

        except Exception as e:
            st.markdown(f'<div style="font-size:0.82rem;color:{p["warm"]};margin-top:0.5rem;">Could not compute: {e}</div>',
                        unsafe_allow_html=True)

    st.markdown(f'<div style="width:48px;height:2px;background:{p["warm"]};margin:2rem 0 2.5rem;"></div>',
                unsafe_allow_html=True)

# ── Section: critical points ──────────────────────────────────────────────────
def section_critical(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">Where does the function turn?</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    At a maximum or minimum, the tangent is horizontal — slope zero.
    So f'(x)=0 at every local extremum. These are the <em>critical points</em>.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    The second derivative tells you which kind: f''&gt;0 means the curve bends upward ∪ (minimum), 
    f''&lt;0 means it bends downward ∩ (maximum).
    Think of it as: is the slope increasing or decreasing?
  </p>
</div>
""", unsafe_allow_html=True)

    expr_str = st.text_input("Analyze f(x) =", value="x**3 - 3*x",
                              key="d21_crit", label_visibility="visible")

    if expr_str.strip():
        try:
            expr   = sp.sympify(expr_str)
            df     = sp.diff(expr, x)
            d2f    = sp.diff(df, x)
            crits  = [c for c in sp.solve(df, x) if c.is_real]

            if crits:
                for cp in crits:
                    fv  = float(expr.subs(x, cp))
                    d2v = float(d2f.subs(x, cp))
                    verdict = ("LOCAL MAXIMUM ∩" if d2v<0
                               else "LOCAL MINIMUM ∪" if d2v>0
                               else "Inconclusive")
                    vcolor  = p["warm"] if "MAX" in verdict else p["sage"] if "MIN" in verdict else p["sand"]
                    st.markdown(f"""
<div style="background:{p['card']};border:1px solid {p['bdr']};border-left:3px solid {vcolor};
            border-radius:0 8px 8px 0;padding:0.85rem 1.1rem;margin-bottom:0.65rem;">
  <div style="font-family:'Fraunces',serif;font-size:1rem;color:{p['ink']};margin-bottom:0.3rem;">
    x = {float(cp):.4f} &nbsp;→&nbsp; <span style="color:{vcolor};">{verdict}</span>
  </div>
  <div style="font-size:0.83rem;color:{p['ink2']};">
    f({float(cp):.4f}) = {fv:.4f} &nbsp;·&nbsp; f''({float(cp):.4f}) = {d2v:.4f}
  </div>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:0.87rem;color:{p["ink2"]};">No real critical points found.</div>',
                            unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div style="font-size:0.82rem;color:{p["warm"]};">Could not analyze: {e}</div>',
                        unsafe_allow_html=True)

    st.markdown(f'<div style="width:48px;height:2px;background:{p["warm"]};margin:2rem 0 2.5rem;"></div>',
                unsafe_allow_html=True)

# ── Section: theorems ─────────────────────────────────────────────────────────
def section_theorems(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The mean value theorems.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    Three theorems, one idea: a continuous, differentiable function
    cannot change without its derivative witnessing it.
  </p>
</div>
""", unsafe_allow_html=True)

    theorems = [
        ("Rolle's Theorem", p["sage"],
         "If f is continuous on [a,b], differentiable on (a,b), and f(a)=f(b) — then somewhere in between, f'(c)=0.",
         "Intuition: if you start and end at the same height, you must have turned around at least once. At the turning point, the tangent is horizontal."),
        ("Lagrange's Theorem (MVT)", p["warm"],
         "If f is continuous on [a,b] and differentiable on (a,b) — then somewhere, f'(c) = [f(b)−f(a)]/(b−a).",
         "Intuition: the instantaneous speed must equal the average speed at some moment. On every car journey, your speedometer reads exactly your average speed at least once."),
        ("Cauchy's Theorem", p["sand"],
         "For f and g satisfying the hypotheses, ∃c: [f(b)−f(a)]/[g(b)−g(a)] = f'(c)/g'(c).",
         "This is the theorem behind de L'Hôpital's rule. Lagrange is the special case g(x)=x."),
    ]

    for title, color, statement, intuition in theorems:
        st.markdown(f"""
<div style="background:{p['card']};border:1px solid {p['bdr']};border-top:2px solid {color};
            border-radius:10px;padding:1.2rem 1.4rem;margin-bottom:1rem;">
  <div style="font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.14em;
              text-transform:uppercase;color:{color};margin-bottom:0.6rem;">{title}</div>
  <div style="font-size:0.95rem;color:{p['ink']};line-height:1.7;margin-bottom:0.6rem;">{statement}</div>
  <div style="font-size:0.85rem;font-weight:300;color:{p['ink2']};line-height:1.7;
              font-style:italic;">{intuition}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f'<div style="width:48px;height:2px;background:{p["warm"]};margin:2rem 0 2.5rem;"></div>',
                unsafe_allow_html=True)

# ── Section: the miracle ──────────────────────────────────────────────────────
def section_miracle(p):
    st.markdown(f"""
<div style="max-width:680px;margin-bottom:1.5rem;">
  <h2 style="font-family:'Fraunces',serif;font-size:1.7rem;font-weight:400;
             color:{p['ink']};margin:0 0 1rem;">The most remarkable fact in calculus.</h2>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    Every function changes under differentiation. Polynomials drop a degree.
    Sin becomes cos. Logarithms become reciprocals.
    But one function is completely unchanged:
  </p>
  <div style="font-family:'Fraunces',serif;font-size:1.6rem;color:{p['ink']};
              text-align:center;padding:1.2rem;background:{p['bg2']};
              border-radius:10px;margin-bottom:1rem;">
    (eˣ)' = eˣ
  </div>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    eˣ is its own derivative. It grows at exactly the rate it currently has.
    This self-referential property makes it appear everywhere in nature —
    radioactive decay, population growth, compound interest, cooling,
    electrical circuits, probability distributions.
  </p>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0 0 0.9rem;">
    And Euler connected it to something even stranger:
  </p>
  <div style="font-family:'Fraunces',serif;font-size:1.4rem;color:{p['ink']};
              text-align:center;padding:1rem;background:{p['bg2']};
              border-radius:10px;margin-bottom:1rem;">
    e^(iπ) + 1 = 0
  </div>
  <p style="font-size:0.97rem;font-weight:300;color:{p['ink2']};line-height:1.8;margin:0;">
    Five fundamental constants — e, i, π, 1, 0 — in one equation.
    Richard Feynman called it "the most remarkable formula in mathematics."
    It follows directly from the properties of eˣ and the derivative.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Public entry point ────────────────────────────────────────────────────────
def render(n, name, subtitle, category):
    dark = st.session_state.get("dark", False)
    p    = _pal(dark)
    style.module_header(category, n, name, subtitle)

    section_hook(p)
    section_average_to_instant(p)
    section_geometry(p)
    section_definition(p)
    section_rules(p)
    section_interactive(p)
    section_critical(p)
    section_theorems(p)
    section_miracle(p)