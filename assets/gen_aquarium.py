#!/usr/bin/env python3
"""Generate aquarium.svg for @iaanne from the public repo list.

Every repository is a fish, the size follows its stars. The scene matches
the aquarium layout: light shafts, swaying weeds, bubbles, and a sand bar
carrying the caption. Run: python3 gen_aquarium.py
"""
import html
import json
import os
import random

W, H = 1200, 620
SAND = 556
random.seed(11)

LANG_COLOR = {
    "Python": "#3f7fa6",
    "TypeScript": "#3f7fd0",
    "Jupyter Notebook": "#e08a4b",
    "Shell": "#8fd46a",
    "QML": "#7fc46b",
    "JavaScript": "#e8d66b",
    "PHP": "#9b8fd6",
    "Blade": "#e0706a",
    "HTML": "#e8765f",
    "CSS": "#8f7fd0",
    "C++": "#c96f7a",
    "None": "#93b3c7",
}
KIND = {
    "TypeScript": "pair",
    "Python": "round",
    "Jupyter Notebook": "pair",
    "Shell": "torpedo",
    "QML": "angelfish",
    "JavaScript": "torpedo",
    "PHP": "round",
    "Blade": "angelfish",
    "HTML": "plain",
    "CSS": "plain",
    "C++": "pair",
    "None": "plain",
}
DISPLAY = {"Jupyter Notebook": "Jupyter", "C++": "C++", "CSS": "CSS"}
LABELS = {
    "rsi-penugasan4-kelompok1": "rsi-penugasan4",
    "rsi-penugasan2-kelompok1": "rsi-penugasan2",
    "rsi-penugasan1-kelompok1": "rsi-penugasan1",
    "ml-bisindo-multimodal-keypoint-caption": "ml-bisindo",
    "dabd-eurointellegence": "dabd-eurointellegence",
    "bi-olist-crm-dashboard": "bi-olist-crm",
    "cloud-usgs-earthquake": "cloud-usgs-earthquake",
    "midnight-shell": "midnight-shell",
    "kbr-notaris-triage-kelompok3": "kbr-notaris-triage",
    "nlp-rag-kelompok6": "nlp-rag",
}

# simple-icons python glyph, CC0
PYTHON_PATH = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "python_path.txt")).read().strip()

# six rows, jittered so the tank never looks like a grid
ROWS = [
    (86, 34, 62), (166, 30, 52), (250, 34, 58),
    (334, 30, 48), (418, 34, 46), (498, 26, 40),
]


def logo(lang, r):
    """White badge with the language mark, like the reference fish."""
    if lang == "TypeScript":
        return (f'<circle r="{r}" cy="0" fill="#f7fbfd" fill-opacity=".92"/>'
                f'<text y="{r * 0.34:.1f}" text-anchor="middle" font-size="{r * 0.95:.1f}" font-weight="700" '
                f'fill="#2f6fb5" font-family="ui-sans-serif, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif">TS</text>')
    if lang == "Python":
        s = r / 10.0
        return (f'<circle r="{r}" cy="0" fill="#f7fbfd" fill-opacity=".94"/>'
                f'<g transform="scale({s:.2f}) translate(-12 -12)"><path fill="#3572A5" d="{PYTHON_PATH}"/></g>')
    code = {"Jupyter Notebook": "JN", "Shell": "SH", "QML": "QM", "JavaScript": "JS",
            "PHP": "PHP", "Blade": "BL", "HTML": "H"}.get(lang)
    if code:
        return (f'<circle r="{r}" cy="0" fill="#f7fbfd" fill-opacity=".9"/>'
                f'<text y="{r * 0.34:.1f}" text-anchor="middle" font-size="{r * 0.78:.1f}" font-weight="700" '
                f'fill="{LANG_COLOR.get(lang, "#6b7f8f")}" '
                f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{code}</text>')
    return ""


def fish_body(kind, color, lang, facing=1):
    dark = "#08131c"
    badge = logo(lang, 14.5)
    if kind == "round":
        body = f'<ellipse rx="30" ry="21" fill="{color}"/><ellipse rx="30" ry="21" fill="#fff" opacity=".08"/>'
        fins = (f'<path d="M-4 -19 Q6 -34 16 -16 Z" fill="{color}" opacity=".75"/>'
                f'<path d="M-2 18 Q8 30 14 16 Z" fill="{color}" opacity=".6"/>')
        eye = '<circle cx="21" cy="-5" r="4" fill="#f7fbfd"/><circle cx="21.8" cy="-5" r="2" fill="#08131c"/>'
        mouth = '<path d="M27 5 q 6 -3 0 -5" stroke="#08131c" stroke-width="1.1" fill="none" opacity=".4"/>'
        badge_x = -8
    elif kind == "pair":
        body = f'<ellipse rx="34" ry="17" fill="{color}"/><ellipse rx="34" ry="17" fill="#fff" opacity=".07"/>'
        fins = (f'<path d="M-8 -15 Q2 -30 12 -13 Z" fill="{color}" opacity=".8"/>'
                f'<path d="M-6 14 Q4 26 12 13 Z" fill="{color}" opacity=".6"/>')
        eye = '<circle cx="23" cy="-4" r="4" fill="#f7fbfd"/><circle cx="23.8" cy="-4" r="2" fill="#08131c"/>'
        mouth = '<path d="M28 6 q 6 -3 0 -5" stroke="#08131c" stroke-width="1.1" fill="none" opacity=".4"/>'
        badge_x = -9
    elif kind == "torpedo":
        body = (f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="{color}"/>'
                f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="#fff" opacity=".07"/>')
        fins = (f'<path d="M-2 -11 Q4 -22 12 -10 Z" fill="{color}" opacity=".8"/>'
                f'<path d="M2 11 Q8 20 14 10 Z" fill="{color}" opacity=".55"/>')
        eye = '<circle cx="23" cy="-3" r="3.6" fill="#f7fbfd"/><circle cx="23.7" cy="-3" r="1.8" fill="#08131c"/>'
        mouth = '<path d="M28 5 q 5 -2 0 -4" stroke="#08131c" stroke-width="1" fill="none" opacity=".4"/>'
        badge_x = -6
    elif kind == "angelfish":
        body = (f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="{color}"/>'
                f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="#fff" opacity=".06"/>')
        fins = (f'<path d="M-10 -20 L2 -44 L10 -18 Z" fill="{color}" opacity=".7"/>'
                f'<path d="M-10 20 L2 42 L10 18 Z" fill="{color}" opacity=".5"/>')
        eye = '<circle cx="19" cy="-5" r="3.6" fill="#f7fbfd"/><circle cx="19.7" cy="-5" r="1.8" fill="#08131c"/>'
        mouth = '<path d="M24 6 q 5 -2 0 -4" stroke="#08131c" stroke-width="1" fill="none" opacity=".4"/>'
        badge_x = -4
    else:
        body = f'<ellipse rx="26" ry="15" fill="{color}"/><ellipse rx="26" ry="15" fill="#fff" opacity=".07"/>'
        fins = (f'<path d="M-4 -13 Q4 -24 12 -12 Z" fill="{color}" opacity=".75"/>'
                f'<path d="M-2 12 Q6 22 12 11 Z" fill="{color}" opacity=".55"/>')
        eye = '<circle cx="18" cy="-3" r="3.6" fill="#f7fbfd"/><circle cx="18.7" cy="-3" r="1.8" fill="#08131c"/>'
        mouth = '<path d="M23 6 q 5 -2 0 -4" stroke="#08131c" stroke-width="1" fill="none" opacity=".4"/>'
        badge_x = -4
    return (
        f'<g class="tail"><path d="M-30 0 L-52 -16 L-46 0 L-52 16 Z" fill="{color}" opacity=".85"/></g>'
        + fins + body
        + (f'<g transform="translate({badge_x} 0) scale({-1 if facing < 0 else 1} 1)">{badge}</g>' if badge else "")
        + eye + mouth
    )


def build():
    repos = {r["name"]: r for r in json.load(open("repos.json")) if r["name"] != "iaanne"}

    # hand-placed so every label has clean water under it
    placed = [
        ("rsi-penugasan4-kelompok1", 240, 82, 1.05, 1),
        ("rsi-penugasan1-kelompok1", 760, 96, 0.95, -1),
        ("rsi-penugasan2-kelompok1", 1012, 96, 1.0, -1),
        ("dabd-eurointellegence", 480, 152, 0.7, 1),
        ("midnight-shell", 1078, 214, 0.62, -1),
        ("ml-bisindo-multimodal-keypoint-caption", 600, 256, 0.7, -1),
        ("bi-olist-crm-dashboard", 330, 300, 0.74, 1),
        ("cloud-usgs-earthquake", 842, 292, 0.7, -1),
        ("nlp-rag-kelompok6", 150, 392, 0.66, 1),
        ("kbr-notaris-triage-kelompok3", 1058, 392, 0.62, -1),
    ]
    free_slots = [
        (382, 72), (556, 62), (622, 136), (60, 116), (118, 216), (56, 302),
        (216, 190), (462, 366), (560, 402), (682, 382), (742, 456), (862, 432),
        (960, 326), (1122, 322), (1130, 472), (1002, 500), (880, 522), (762, 540),
        (640, 506), (520, 472), (424, 434), (302, 432), (216, 472), (122, 472),
        (64, 512),
    ]

    fish_svg, keys = [], []
    used = set()

    def draw(name, bx, by, scale, facing, label):
        repo = repos[name]
        used.add(name)
        stars = repo["stargazers_count"]
        langs = repo.get("languages") or {}
        ranked = sorted(langs.items(), key=lambda kv: -kv[1])
        lang = ranked[0][0] if ranked else (repo["language"] or "None")
        total = sum(v for _, v in ranked) or 1
        top = [k for k, v in ranked[:2] if v >= total * 0.1]
        stack = " · ".join(DISPLAY.get(k, k) for k in top) if top else "not detected"
        color = LANG_COLOR.get(lang, LANG_COLOR["None"])
        kind = KIND.get(lang, "plain")
        idx = len(fish_svg)
        dur = 26 + (idx * 7) % 22
        bob = 5.0 + (idx * 0.37) % 3
        delay = -(idx * 2.6) % 40
        key = f"f{idx}"
        keys.append(f"@keyframes {key} {{ from {{ transform: translateX(-{int(36 + 54 * scale)}px) }} "
                    f"to {{ transform: translateX({int(36 + 54 * scale)}px) }} }}")
        label_svg = ""
        if label:
            label_svg = (f'<text class="tag" y="{34 + 13 * scale:.0f}">{html.escape(label)}</text>'
                         f'<text class="tag stack" y="{34 + 13 * scale + 17:.0f}">{html.escape(stack)}</text>')
        fish_svg.append(f"""
  <g transform="translate({bx} {by})" opacity="{1 if label else 0.8}">
    <g class="swim" style="animation-name:{key};animation-duration:{dur}s;animation-delay:{delay}s">
      <g class="bob" style="animation-duration:{bob:.1f}s;animation-delay:{delay / 2:.1f}s">
        <g transform="scale({scale * facing:.2f} {scale:.2f})" filter="url(#soft)">{fish_body(kind, color, lang if label else "", facing)}</g>
        {label_svg}
      </g>
    </g>
  </g>""")

    for name, bx, by, scale, facing in placed:
        draw(name, bx, by, scale, facing, LABELS.get(name, name))

    rest = [n for n in repos if n not in used]
    rest.sort(key=lambda n: repos[n]["pushed_at"], reverse=True)
    for i, name in enumerate(rest):
        bx, by = free_slots[i % len(free_slots)]
        facing = 1 if i % 2 == 0 else -1
        scale = 0.44 + (i % 3) * 0.05
        draw(name, bx, by, scale, facing, None)

    # thin weeds rooted in the sand
    weed_spec = [
        (48, 150, 4.0), (74, 108, 3.2), (100, 176, 4.4), (128, 122, 3.0),
        (172, 92, 2.6), (214, 148, 4.2), (246, 104, 3.0), (288, 72, 2.4),
        (352, 132, 3.6), (392, 86, 2.6), (438, 112, 3.2), (500, 68, 2.4),
        (556, 96, 2.8), (622, 120, 3.4), (688, 78, 2.6), (742, 146, 4.0),
        (786, 102, 3.0), (846, 166, 4.4), (892, 118, 3.4), (940, 88, 2.8),
        (996, 154, 4.2), (1042, 114, 3.2), (1088, 172, 4.4), (1132, 96, 2.8),
        (1166, 136, 3.6),
    ]
    weeds = []
    for i, (x, h, w) in enumerate(weed_spec):
        col = ["#2f7d5b", "#37986a", "#2b6f52"][i % 3]
        weeds.append(f"""
  <g class="weed" style="animation-duration:{4.6 + (i % 5) * 0.9:.1f}s;animation-delay:-{i * 0.47:.1f}s">
    <path d="M{x} {SAND + 4} C{x - 13} {SAND + 4 - h * 0.38} {x + 14} {SAND + 4 - h * 0.72} {x - 3} {SAND + 4 - h}"
          stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>
  </g>""")

    # small plants sprouting straight out of the sand
    plants = []
    for i, x in enumerate([36, 58, 148, 196, 262, 322, 410, 470, 528, 604, 668, 726,
                           806, 866, 926, 968, 1030, 1074, 1118, 1156]):
        h = 10 + (i * 5) % 12
        plant = [f'<path d="M{x} {SAND + 2} q -2 -{h * 0.55:.0f} -3 -{h}" stroke="#3f8f63" stroke-width="2.4" fill="none" stroke-linecap="round"/>']
        plant.append(f'<path d="M{x + 3} {SAND + 2} q 2 -{h * 0.4:.0f} 4 -{h * 0.72:.0f}" stroke="#59a578" stroke-width="2" fill="none" stroke-linecap="round"/>')
        plant.append(f'<path d="M{x - 3} {SAND + 2} q -3 -{h * 0.3:.0f} -6 -{h * 0.55:.0f}" stroke="#4a9a6c" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
        plants.append("  <g>" + "".join(plant) + "</g>")

    legend = []
    items = [("Python", "#3f7fa6"), ("Jupyter", "#e08a4b"), ("TypeScript", "#3f7fd0"),
             ("PHP", "#9b8fd6"), ("JavaScript", "#e8d66b"), ("Shell", "#8fd46a"),
             ("QML", "#7fc46b"), ("Blade", "#e0706a"), ("HTML", "#e8765f"),
             ("not detected", "#93b3c7")]
    lx = 0.0
    for name, col in items:
        legend.append(f'<g transform="translate({lx:.1f} 0)"><circle cx="4" cy="-3.4" r="3.6" fill="{col}"/>'
                      f'<text class="legend" x="14" y="0">{name}</text></g>')
        lx += 16 + len(name) * 7.5 + 24
    legend_width = lx - 22

    bubbles = []
    for i in range(16):
        x = 52 + i * 72 + random.randint(-12, 12)
        bubbles.append(
            f'<circle class="bubble" cx="{x}" cy="{SAND - 6}" r="{1.6 + (i % 3) * 0.7:.1f}" fill="none" '
            f'stroke="#cfeaff" stroke-width="1" opacity=".3" '
            f'style="animation-duration:{13 + i % 6}s;animation-delay:-{i * 1.9:.1f}s"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Aquarium of @iaanne's repositories">
  <title>Aquarium: every repository is a fish, bigger fish have more stars</title>
  <defs>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d4864"/><stop offset="48%" stop-color="#082f47"/><stop offset="100%" stop-color="#041a29"/>
    </linearGradient>
    <linearGradient id="sand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#b7a380"/><stop offset="100%" stop-color="#8b7c5e"/>
    </linearGradient>
    <linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#bfe9ff" stop-opacity=".16"/><stop offset="100%" stop-color="#bfe9ff" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#00121c" flood-opacity=".35"/>
    </filter>
  </defs>

  <style>
    .swim {{ animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }}
    .bob {{ animation-name: bob; animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }}
    .weed {{ animation-name: sway; animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; transform-origin: bottom center; transform-box: fill-box; }}
    .bubble {{ animation-name: rise; animation-timing-function: linear; animation-iteration-count: infinite; }}
    .tail {{ animation: wiggle 1.1s ease-in-out infinite alternate; transform-origin: -28px 0; transform-box: fill-box; }}
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 15px; fill: #e8f6ff; fill-opacity: .55; text-anchor: middle; letter-spacing: .3px; }}
    .tag.stack {{ font-size: 12.5px; fill-opacity: .62; letter-spacing: .2px; }}
    .frame {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; fill: #dff1ff; fill-opacity: .26; letter-spacing: 2px; }}
    .foot {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10.5px; fill: #f3e7c9; fill-opacity: .55; letter-spacing: 1.1px; }}
    .legend {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12.5px; fill: #f3e7c9; fill-opacity: .6; letter-spacing: .6px; }}
    @keyframes bob {{ from {{ transform: translateY(-5px) }} to {{ transform: translateY(5px) }} }}
    @keyframes sway {{ from {{ transform: rotate(-4deg) }} to {{ transform: rotate(4deg) }} }}
    @keyframes rise {{ from {{ transform: translateY(0); opacity: 0 }} 12% {{ opacity: .3 }} to {{ transform: translateY(-480px); opacity: 0 }} }}
    @keyframes wiggle {{ from {{ transform: rotate(-9deg) }} to {{ transform: rotate(9deg) }} }}
    .rays {{ animation: pulse 9s ease-in-out infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: .6 }} to {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .swim, .bob, .weed, .bubble, .tail, .rays {{ animation: none !important; }}
    }}
    
{"".join(keys)}
  </style>

  <rect width="{W}" height="{H}" fill="url(#water)"/>
  <g class="rays">
    <path d="M120 0 L290 0 L430 {SAND} L300 {SAND} Z" fill="url(#ray)"/>
    <path d="M430 0 L580 0 L700 {SAND} L580 {SAND} Z" fill="url(#ray)" opacity=".75"/>
    <path d="M760 0 L870 0 L950 {SAND} L850 {SAND} Z" fill="url(#ray)" opacity=".55"/>
    <path d="M1010 0 L1105 0 L1150 {SAND} L1070 {SAND} Z" fill="url(#ray)" opacity=".4"/>
  </g>

  <text class="frame" x="30" y="38">AQUARIUM · @IAANNE</text>
  <text class="frame" x="{W - 30}" y="38" text-anchor="end">FISH = REPOS · SIZE = STARS</text>

{"".join(weeds)}
{"".join(fish_svg)}
{"".join(bubbles)}

  <path d="M0 {SAND} Q 200 {SAND - 8} 400 {SAND - 2} T 800 {SAND - 4} T {W} {SAND} L{W} {H} L0 {H} Z" fill="url(#sand)"/>
  <path d="M0 {SAND} Q 200 {SAND - 8} 400 {SAND - 2} T 800 {SAND - 4} T {W} {SAND} L{W} {SAND + 5} L0 {SAND + 5} Z" fill="#e6d3a8" opacity=".35"/>
{"".join(plants)}
  <text class="foot" x="30" y="{H - 22}">@IAANNE</text>
  <g transform="translate({(W - legend_width) / 2:.1f} {H - 22})">
{"".join(legend)}
  </g>
</svg>
"""


if __name__ == "__main__":
    open("aquarium.svg", "w").write(build())
    print("wrote aquarium.svg")
