"""Generates the animated SVG assets for the GitHub profile README.

Palette is taken from the original evening banner.
"""
import math
import random
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])
(OUT / "projects").mkdir(parents=True, exist_ok=True)

INK = "#050a18"
DEEP = "#0b1430"
WINE = "#1c2a52"
RUST = "#8a1c34"
EMBER = "#c8283c"
AMBER = "#ff5a4e"
GOLD = "#ffb199"
CREAM = "#ffe9e0"
MUTED = "#a3b3d6"
DIM = "#5a6a90"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', 'Courier New', monospace"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

rnd = random.Random(7)


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n")
    print("wrote", name, len(svg), "bytes")


# --------------------------------------------------------------------------
# shapes
# --------------------------------------------------------------------------

def ridge(width, base, amp, seed, step, valley=0.0, valley_w=380):
    """Jagged mountain ridge across the width; `valley` lowers peaks around the centre."""
    r = random.Random(seed)
    d = f"M0 {base + 200}"
    x, peak = 0.0, False
    while x <= width + step:
        env = 1 - valley * max(0.0, 1 - abs(x - width / 2) / valley_w)
        y = base - (amp * (0.55 + 0.45 * r.random()) if peak else amp * 0.15 * r.random()) * env
        d += f" L{x:.1f} {y:.1f}"
        x += step * (0.7 + 0.6 * r.random())
        peak = not peak
    return d + f" L{x:.1f} {base + 200} Z"


def pine(x, ground, h, w):
    """Layered pine silhouette."""
    parts = []
    tiers = 4
    for i in range(tiers):
        top = ground - h + i * h * 0.2
        bottom = top + h * 0.38
        half = w * (0.45 + i * 0.18)
        parts.append(f"M{x:.1f} {top:.1f} L{x - half:.1f} {bottom:.1f} L{x + half:.1f} {bottom:.1f} Z")
    parts.append(f"M{x - w * 0.07:.1f} {ground - h * 0.25:.1f} h{w * 0.14:.1f} V{ground} h{-w * 0.14:.1f} Z")
    return " ".join(parts)


# --------------------------------------------------------------------------
# banner
# --------------------------------------------------------------------------

def banner():
    W, H = 1200, 400
    horizon = 318

    stars = []
    for i in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(6, 170) ** 1.05
        r = rnd.choice([0.6, 0.8, 1.0, 1.0, 1.3, 1.7])
        dur = rnd.uniform(2.5, 6)
        delay = rnd.uniform(0, 6)
        stars.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="star" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s"/>'
        )

    shooting = (
        '<g class="shoot"><line x1="0" y1="0" x2="90" y2="0" stroke="url(#trail)" stroke-width="1.6" '
        'stroke-linecap="round"/></g>'
    )

    clouds = []
    for i, (y, s, dur, delay, op) in enumerate(
        [(120, 1.0, 95, 0, 0.16), (165, 1.4, 130, 40, 0.12), (92, 0.8, 110, 70, 0.10)]
    ):
        clouds.append(
            f'<g class="cloud" style="animation-duration:{dur}s;animation-delay:-{delay}s;opacity:{op}">'
            f'<g transform="translate(0 {y}) scale({s})">'
            f'<ellipse cx="0" cy="0" rx="90" ry="9" fill="{GOLD}"/>'
            f'<ellipse cx="40" cy="-6" rx="55" ry="8" fill="{GOLD}"/>'
            f'<ellipse cx="-35" cy="4" rx="60" ry="6" fill="{GOLD}"/></g></g>'
        )

    far = ridge(W, 262, 110, 3, 60, valley=0.75)
    mid = ridge(W, 292, 85, 11, 50, valley=0.8)
    near = ridge(W, 312, 46, 23, 40, valley=0.85)

    trees_l = [(30, 120, 54), (80, 160, 66), (135, 128, 54), (185, 96, 44), (232, 70, 34), (270, 52, 26)]
    trees_r = [(W - x, h, w) for x, h, w in trees_l]
    trees = " ".join(pine(x, horizon + 6, h, w) for x, h, w in trees_l + trees_r)
    trees_back = " ".join(
        pine(x, horizon + 4, h, w)
        for x, h, w in [(58, 92, 40), (110, 110, 46), (160, 84, 36), (W - 58, 92, 40), (W - 110, 110, 46),
                        (W - 160, 84, 36), (310, 38, 20), (W - 310, 38, 20)]
    )

    ripples = []
    for i, (w, y, op, dur) in enumerate([(150, 330, 0.55, 3.2), (110, 340, 0.4, 3.8), (78, 350, 0.3, 4.4),
                                         (46, 360, 0.22, 5.0), (190, 334, 0.12, 4.0)]):
        ripples.append(
            f'<rect x="{W / 2 - w / 2}" y="{y}" width="{w}" height="1.6" rx="0.8" fill="{GOLD}" '
            f'opacity="{op}" class="ripple" style="animation-duration:{dur}s;animation-delay:-{i * 0.7:.1f}s"/>'
        )

    flies = []
    for i in range(16):
        x = rnd.uniform(60, W - 60)
        y = rnd.uniform(horizon - 40, horizon + 30)
        dur = rnd.uniform(6, 11)
        delay = rnd.uniform(0, 11)
        dx = rnd.uniform(-30, 30)
        flies.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([1.1, 1.4, 1.8])}" class="fly" '
            f'style="--dx:{dx:.0f}px;animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s"/>'
        )

    subtitle = "turning coffee into code since 2020"
    n = len(subtitle)
    sub_w = 500
    sub_x = W / 2 - sub_w / 2
    sub_y = 222
    step = sub_w / n
    # typewriter: clip rect slides right one char at a time, cursor follows
    type_vals = ";".join(f"{(i * step):.2f} 0" for i in range(n + 1))
    key_times = ";".join(f"{i / n:.4f}" for i in range(n + 1))

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Piyush — turning coffee into code since 2020">
  <title>Piyush — turning coffee into code since 2020</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#040817"/>
      <stop offset="0.22" stop-color="#0d1a3f"/>
      <stop offset="0.38" stop-color="#3a1a4f"/>
      <stop offset="0.5" stop-color="#9a1f3c"/>
      <stop offset="0.62" stop-color="{EMBER}"/>
      <stop offset="0.75" stop-color="{AMBER}"/>
      <stop offset="1" stop-color="#ff7a5c"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#ff7a5c" stop-opacity="0.7"/>
      <stop offset="0.35" stop-color="#ff6a50" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#b3263a" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff1e6"/>
      <stop offset="0.6" stop-color="{GOLD}"/>
      <stop offset="1" stop-color="{AMBER}"/>
    </linearGradient>
    <linearGradient id="far" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2a3570"/><stop offset="1" stop-color="#101a3c"/>
    </linearGradient>
    <linearGradient id="mid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#18234e"/><stop offset="1" stop-color="#0a1129"/>
    </linearGradient>
    <linearGradient id="near" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0e1636"/><stop offset="1" stop-color="#060b1e"/>
    </linearGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c1530"/><stop offset="1" stop-color="{INK}"/>
    </linearGradient>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CREAM}" stop-opacity="0"/><stop offset="1" stop-color="{CREAM}"/>
    </linearGradient>
    <linearGradient id="name" y1="0" y2="0" gradientUnits="userSpaceOnUse" x1="-400" x2="400">
      <stop offset="0" stop-color="{CREAM}"/>
      <stop offset="0.45" stop-color="{CREAM}"/>
      <stop offset="0.5" stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="{CREAM}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1600 0" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <clipPath id="above"><rect width="{W}" height="{horizon}"/></clipPath>
    <clipPath id="typed">
      <rect x="{sub_x - sub_w:.2f}" y="{sub_y - 20}" width="{sub_w}" height="30">
        <animateTransform attributeName="transform" type="translate" values="{type_vals}" keyTimes="{key_times}" calcMode="discrete" dur="2.6s" begin="1.4s" fill="freeze"/>
      </rect>
    </clipPath>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>
    <filter id="haze" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <style>
    .star {{ fill: {CREAM}; animation: twinkle ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity: .15 }} 50% {{ opacity: .95 }} }}
    .shoot {{ animation: shoot 9s ease-in 3s infinite; opacity: 0; }}
    @keyframes shoot {{
      0% {{ transform: translate(820px, 30px) rotate(160deg); opacity: 0 }}
      2% {{ opacity: 1 }}
      9% {{ transform: translate(560px, 125px) rotate(160deg); opacity: 0 }}
      100% {{ transform: translate(560px, 125px) rotate(160deg); opacity: 0 }}
    }}
    .cloud {{ animation: drift linear infinite; }}
    @keyframes drift {{ from {{ transform: translateX(-260px) }} to {{ transform: translateX({W + 260}px) }} }}
    .glow {{ transform-origin: {W / 2}px {horizon}px; animation: breathe 6s ease-in-out infinite; }}
    @keyframes breathe {{ 0%,100% {{ transform: scale(1); opacity: .85 }} 50% {{ transform: scale(1.12); opacity: 1 }} }}
    .sun {{ animation: sink 14s ease-in-out infinite; }}
    @keyframes sink {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(10px) }} }}
    .ripple {{ transform-box: fill-box; transform-origin: center; animation: shimmer ease-in-out infinite; }}
    @keyframes shimmer {{ 0%,100% {{ transform: scaleX(1) }} 50% {{ transform: scaleX(.6) }} }}
    .fly {{ fill: {GOLD}; filter: url(#soft); animation: float ease-in-out infinite; opacity: 0; }}
    @keyframes float {{
      0% {{ transform: translate(0, 0); opacity: 0 }}
      30% {{ opacity: .9 }}
      70% {{ opacity: .6 }}
      100% {{ transform: translate(var(--dx), -60px); opacity: 0 }}
    }}
    .title {{ animation: rise 1.4s cubic-bezier(.2,.7,.2,1) both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); letter-spacing: 34px }} to {{ opacity: 1; transform: none }} }}
    .rule {{ transform-origin: {W / 2}px 0; animation: grow 1.2s .9s cubic-bezier(.2,.7,.2,1) both; }}
    @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    <g>{''.join(stars)}</g>
    {shooting}
    <g clip-path="url(#above)">
      <ellipse class="glow" cx="{W / 2}" cy="{horizon}" rx="340" ry="210" fill="url(#glow)"/>
      <g class="sun"><circle cx="{W / 2}" cy="{horizon - 40}" r="54" fill="url(#sun)"/></g>
      {''.join(clouds)}
      <path d="{far}" fill="url(#far)"/>
      <path d="{mid}" fill="url(#mid)"/>
      <path d="{near}" fill="url(#near)"/>
      <rect y="{horizon - 40}" width="{W}" height="60" fill="{AMBER}" opacity="0.08" filter="url(#haze)"/>
    </g>
    <rect y="{horizon}" width="{W}" height="{H - horizon}" fill="url(#water)"/>
    <ellipse cx="{W / 2}" cy="{horizon + 4}" rx="140" ry="10" fill="{GOLD}" opacity="0.18" filter="url(#haze)"/>
    {''.join(ripples)}
    <path d="{trees_back}" fill="#0a1128"/>
    <path d="{trees}" fill="#03060f"/>
    <g>{''.join(flies)}</g>

    <g text-anchor="middle">
      <text class="title" x="{W / 2}" y="168" font-family="{SERIF}" font-size="76" font-weight="700" letter-spacing="18" fill="url(#name)">PIYUSH</text>
      <rect class="rule" x="{W / 2 - 70}" y="188" width="140" height="1.5" fill="{AMBER}" opacity="0.8"/>
    </g>
    <g clip-path="url(#typed)">
      <text x="{sub_x:.2f}" y="{sub_y}" font-family="{MONO}" font-size="15" textLength="{sub_w}" lengthAdjust="spacingAndGlyphs" fill="{GOLD}" opacity="0.92">{subtitle}</text>
    </g>
    <rect class="cursor" x="{sub_x + 2:.2f}" y="{sub_y - 14}" width="8" height="17" fill="{AMBER}">
      <animateTransform attributeName="transform" type="translate" values="{type_vals}" keyTimes="{key_times}" calcMode="discrete" dur="2.6s" begin="1.4s" fill="freeze"/>
    </rect>
  </g>
</svg>
"""


# --------------------------------------------------------------------------
# terminal "about" card
# --------------------------------------------------------------------------

def terminal():
    W = 900
    lines = [
        ("cmd", "whoami"),
        ("out", [("Piyush", CREAM), (" — full-stack developer · web & mobile", MUTED)]),
        ("gap", None),
        ("cmd", "cat about.txt"),
        ("out", [("I build things for the web and mobile — from APIs to production-grade", MUTED)]),
        ("out", [("systems, mostly in ", MUTED), ("TypeScript", AMBER), (" and sometimes ", MUTED), ("Python", AMBER), (".", MUTED)]),
        ("out", [("Coding was the hobby before it became the career. ", MUTED), ("Music", GOLD), (" is the other one.", MUTED)]),
        ("gap", None),
        ("cmd", "echo $STATUS"),
        ("out", [("●", "#7bd88f"), (" shipping things · open to interesting problems", MUTED)]),
    ]
    top = 74
    lh = 26
    char_w = 8.6
    body = []
    t = 0.5
    y = top
    for kind, val in lines:
        if kind == "gap":
            y += lh * 0.55
            continue
        if kind == "cmd":
            n = len(val)
            dur = max(0.35, n * 0.055)
            body.append(
                f'<g class="ln" style="animation-delay:{t:.2f}s">'
                f'<text x="34" y="{y}" fill="{AMBER}">❯</text>'
                f'<text x="56" y="{y}" fill="{CREAM}" class="typed" '
                f'style="--w:{n * char_w + 4:.0f}px;animation-delay:{t:.2f}s;animation-duration:{dur:.2f}s;'
                f'animation-timing-function:steps({n})">{escape(val)}</text></g>'
            )
            t += dur + 0.25
        else:
            spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in val)
            body.append(
                f'<text x="56" y="{y}" class="ln" style="animation-delay:{t:.2f}s">{spans}</text>'
            )
            t += 0.12
        y += lh
    # trailing prompt with blinking cursor
    body.append(
        f'<g class="ln" style="animation-delay:{t:.2f}s"><text x="34" y="{y}" fill="{AMBER}">❯</text>'
        f'<rect class="cursor" x="56" y="{y - 14}" width="9" height="18" fill="{CREAM}"/></g>'
    )
    H = y + 36

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="about me terminal">
  <title>about --me</title>
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0.55"/>
      <stop offset="0.5" stop-color="{WINE}" stop-opacity="0.6"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0.25"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#111b38"/><stop offset="1" stop-color="#0d152d"/>
    </linearGradient>
    <radialGradient id="warm" cx="1" cy="0" r="1">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0.10"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
  </defs>
  <style>
    text {{ font-family: {MONO}; font-size: 15px; white-space: pre; }}
    .ln {{ opacity: 0; animation: show .25s ease-out forwards; }}
    @keyframes show {{ from {{ opacity: 0; transform: translateY(4px) }} to {{ opacity: 1; transform: none }} }}
    .typed {{ clip-path: inset(0 100% 0 0); animation-name: type; animation-fill-mode: both; }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0) }} to {{ clip-path: inset(0 0 0 0) }} }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
  </style>
  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="#080e21"/>
    <rect width="{W}" height="{H}" fill="url(#warm)"/>
    <rect width="{W}" height="40" fill="url(#bar)"/>
    <rect y="40" width="{W}" height="1" fill="{WINE}"/>
    <circle cx="24" cy="20" r="6" fill="#ff5f57"/>
    <circle cx="44" cy="20" r="6" fill="#febc2e"/>
    <circle cx="64" cy="20" r="6" fill="#28c840"/>
    <text x="{W / 2}" y="25" text-anchor="middle" fill="{DIM}" style="font-size:13px">piyush@dev: ~</text>
    {''.join(body)}
  </g>
  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
</svg>
"""


# --------------------------------------------------------------------------
# project cards
# --------------------------------------------------------------------------

LANG = {"TypeScript": "#3178c6", "C": "#a8b9cc", "JavaScript": "#f1e05a"}


def card(slug, title, kicker, desc_lines, lang, tags, delay):
    W, H = 440, 200
    per = 2 * (W + H) - 4 * 14 + 2 * math.pi * 14  # rounded-rect perimeter
    desc = "".join(
        f'<text x="26" y="{98 + i * 21}" class="d">{escape(l)}</text>' for i, l in enumerate(desc_lines)
    )
    tag_svg = []
    x = 26 + 18 + len(lang) * 7.2 + 16
    for t in tags:
        w = len(t) * 6.6 + 18
        tag_svg.append(
            f'<rect x="{x:.1f}" y="164" width="{w:.1f}" height="20" rx="10" fill="{AMBER}" fill-opacity="0.08" '
            f'stroke="{AMBER}" stroke-opacity="0.3"/>'
            f'<text x="{x + w / 2:.1f}" y="178" text-anchor="middle" class="tag">{escape(t)}</text>'
        )
        x += w + 8
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1633"/><stop offset="1" stop-color="#070c1d"/>
    </linearGradient>
    <radialGradient id="warm" cx="1" cy="0" r="0.9">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0.16"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
      <stop offset="1" stop-color="{GOLD}"/>
    </linearGradient>
  </defs>
  <style>
    .k {{ font: 600 11px {MONO}; letter-spacing: 2px; fill: {AMBER}; }}
    .t {{ font: 700 21px {SANS}; fill: {CREAM}; }}
    .d {{ font: 400 13.5px {SANS}; fill: {MUTED}; }}
    .l {{ font: 500 12px {MONO}; fill: {MUTED}; }}
    .tag {{ font: 500 11px {MONO}; fill: {GOLD}; }}
    .run {{ stroke-dasharray: 90 {per - 90:.1f}; animation: run 6s linear infinite; animation-delay: -{delay}s; }}
    @keyframes run {{ to {{ stroke-dashoffset: -{per:.1f} }} }}
    .in {{ animation: in .7s cubic-bezier(.2,.7,.2,1) both; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(8px) }} to {{ opacity: 1; transform: none }} }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .5; transform: scale(1) }} 50% {{ opacity: 1; transform: scale(1.35) }} }}
  </style>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#bg)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="url(#warm)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{WINE}" stroke-width="1.2"/>
  <rect class="run" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-linecap="round" opacity="0.85"/>
  <g class="in">
    <text x="26" y="40" class="k">{escape(kicker)}</text>
    <text x="26" y="70" class="t">{escape(title)}</text>
    <text x="{W - 26}" y="40" text-anchor="end" class="k" style="fill:{DIM}">↗</text>
    {desc}
    <circle class="pulse" cx="32" cy="174" r="5" fill="{LANG.get(lang, AMBER)}"/>
    <text x="44" y="178" class="l">{escape(lang)}</text>
    {''.join(tag_svg)}
  </g>
</svg>
"""


PROJECTS = [
    ("dating-app", "Dating App", "MOBILE · iOS & ANDROID",
     ["Full-fledged dating app with matching, stories,", "chat, voice & video calling and Razorpay",
      "autopay subscriptions."], "TypeScript", ["calls", "payments"]),
    ("geofenced-erp", "Geofenced Face-ID ERP", "WEB · EDTECH",
     ["Location & face-aware attendance for institutes.", "Teachers open short windows; students mark",
      "attendance only when on campus and verified."], "TypeScript", ["face-id", "geofence"]),
    ("pdb", "pDB", "SYSTEMS · DATABASE",
     ["A lightweight NoSQL document database written", "entirely in C — exploring storage engines and",
      "low-level database internals."], "C", ["storage", "nosql"]),
    ("linkedin-autopilot", "LinkedIn Autopilot", "AUTOMATION · AI",
     ["Server-only system that picks trending topics,", "writes curated posts, generates matching AI",
      "visuals and publishes them daily."], "TypeScript", ["ai", "cron"]),
]


# --------------------------------------------------------------------------
# divider + footer
# --------------------------------------------------------------------------

def divider():
    W, H = 1200, 24
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="spark" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CREAM}"/><stop offset="0.4" stop-color="{GOLD}" stop-opacity="0.6"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <style>
    .spark {{ animation: sweep 5s cubic-bezier(.45,0,.55,1) infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(200px); opacity: 0 }} 15%,85% {{ opacity: 1 }} 100% {{ transform: translateX(1000px); opacity: 0 }} }}
  </style>
  <rect x="0" y="{H / 2 - 0.5}" width="{W}" height="1" fill="url(#line)"/>
  <ellipse class="spark" cx="0" cy="{H / 2}" rx="60" ry="3" fill="url(#spark)"/>
  <circle cx="{W / 2}" cy="{H / 2}" r="3" fill="{AMBER}" opacity="0.8"/>
</svg>
"""


def footer():
    W, H = 1200, 170
    horizon = 120
    text = "// still compiling... check back later"
    n = len(text)
    tw = n * 9.6
    tx = W / 2 - tw / 2
    step = tw / n
    vals = ";".join(f"{i * step:.2f} 0" for i in range(n + 1))
    kt = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    hills = ridge(W, horizon + 4, 26, 5, 40, valley=0.9, valley_w=260)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{text}">
  <title>{text}</title>
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0.22"/>
    </linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff1e6"/><stop offset="1" stop-color="{AMBER}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0.5"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.15" stop-color="#fff"/>
      <stop offset="0.85" stop-color="#fff"/><stop offset="1" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
    <mask id="sides"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
    <clipPath id="sky"><rect width="{W}" height="{horizon}"/></clipPath>
    <clipPath id="typed">
      <rect x="{tx - tw:.2f}" y="0" width="{tw:.2f}" height="60">
        <animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="2.8s" begin="0.4s" fill="freeze"/>
      </rect>
    </clipPath>
  </defs>
  <style>
    .sun {{ animation: set 10s ease-in-out infinite; }}
    @keyframes set {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(16px) }} }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
  </style>
  <g mask="url(#sides)">
    <rect y="{horizon - 70}" width="{W}" height="70" fill="url(#fade)"/>
    <g clip-path="url(#sky)">
      <ellipse cx="{W / 2}" cy="{horizon}" rx="160" ry="70" fill="url(#glow)"/>
      <circle class="sun" cx="{W / 2}" cy="{horizon - 4}" r="30" fill="url(#sun)"/>
      <path d="{hills}" fill="#141e44"/>
    </g>
    <rect y="{horizon}" width="{W}" height="1.2" fill="{AMBER}" opacity="0.6"/>
  </g>
  <g clip-path="url(#typed)">
    <text x="{tx:.2f}" y="38" font-family="{MONO}" font-size="16" textLength="{tw:.2f}" lengthAdjust="spacingAndGlyphs" fill="{MUTED}">{text}</text>
  </g>
  <rect class="cursor" x="{tx + 2:.2f}" y="24" width="8" height="18" fill="{AMBER}">
    <animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="2.8s" begin="0.4s" fill="freeze"/>
  </rect>
</svg>
"""


write("banner.svg", banner())
write("about.svg", terminal())
write("divider.svg", divider())
write("footer.svg", footer())
for i, (slug, *rest) in enumerate(PROJECTS):
    write(f"projects/{slug}.svg", card(slug, *rest, delay=i * 1.5))
