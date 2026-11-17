#!/usr/bin/env python3
"""Generate aquarium.svg for @iaanne from the public repo list.

Every repository becomes a fish. Starred repos are the big labelled ones,
recent work is medium, the rest fill the tank as a school.
Run: python3 gen_aquarium.py
"""
import html
import json
import math
import random

W, H = 1200, 620
random.seed(7)

LANG_COLOR = {
    "Python": "#3fa08e",
    "TypeScript": "#3f7fd0",
    "Jupyter Notebook": "#e08a4b",
    "Shell": "#8fd46a",
    "QML": "#7fc46b",
    "JavaScript": "#e8d66b",
    "PHP": "#9b8fd6",
    "Blade": "#f2726a",
    "HTML": "#e8765f",
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
    "None": "plain",
}
# short labels for the projects worth naming in a crowded tank
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
ROWS = [96, 168, 240, 312, 384, 452]


def fish_body(kind, color):
    dark = "#08131c"
    if kind == "round":
        body = f'<ellipse rx="30" ry="21" fill="{color}"/><ellipse rx="30" ry="21" fill="#fff" opacity=".08"/>'
        fin_top = f'<path d="M-4 -19 Q6 -34 16 -16 Z" fill="{color}" opacity=".75"/>'
        fin_side = f'<path d="M-2 18 Q8 30 14 16 Z" fill="{color}" opacity=".6"/>'
    elif kind == "pair":
        body = f'<ellipse rx="34" ry="17" fill="{color}"/><ellipse rx="34" ry="17" fill="#fff" opacity=".07"/>'
        fin_top = f'<path d="M-8 -15 Q2 -30 12 -13 Z" fill="{color}" opacity=".8"/>'
        fin_side = f'<path d="M-6 14 Q4 26 12 13 Z" fill="{color}" opacity=".6"/>'
    elif kind == "torpedo":
        body = (f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="{color}"/>'
                f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="#fff" opacity=".07"/>')
        fin_top = f'<path d="M-2 -11 Q4 -22 12 -10 Z" fill="{color}" opacity=".8"/>'
        fin_side = f'<path d="M2 11 Q8 20 14 10 Z" fill="{color}" opacity=".55"/>'
    elif kind == "angelfish":
        body = (f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="{color}"/>'
                f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="#fff" opacity=".06"/>')
        fin_top = f'<path d="M-10 -20 L2 -44 L10 -18 Z" fill="{color}" opacity=".7"/>'
        fin_side = f'<path d="M-10 20 L2 42 L10 18 Z" fill="{color}" opacity=".5"/>'
    else:
        body = f'<ellipse rx="26" ry="15" fill="{color}"/><ellipse rx="26" ry="15" fill="#fff" opacity=".07"/>'
        fin_top = f'<path d="M-4 -13 Q4 -24 12 -12 Z" fill="{color}" opacity=".75"/>'
        fin_side = f'<path d="M-2 12 Q6 22 12 11 Z" fill="{color}" opacity=".55"/>'
    return (
        f'<g class="tail"><path d="M-30 0 L-52 -16 L-46 0 L-52 16 Z" fill="{color}" opacity=".85"/></g>'
        + fin_top + fin_side + body
        + f'<circle cx="18" cy="-4" r="4" fill="#f7fbfd"/><circle cx="18.8" cy="-4" r="2" fill="{dark}"/>'
        + f'<path d="M16 -11 q 9 3 0 7" stroke="{dark}" stroke-width="1.1" fill="none" opacity=".45"/>'
        + f'<path d="M30 6 q 6 -3 0 -5" stroke="{dark}" stroke-width="1.1" fill="none" opacity=".4"/>'
    )


def coral(x, base, color, scale=1.0):
    """A branching coral, drawn as strokes so it stays light."""
    parts = [f'<ellipse cx="{x}" cy="{base - 4}" rx="{20 * scale}" ry="{8 * scale}" fill="{color}" opacity=".55"/>']
    for i, (dx, dy, w) in enumerate([(-18, -54, 7), (0, -74, 8), (16, -48, 7)]):
        parts.append(
            f'<path d="M{x} {base} Q{x + dx * 0.4} {base + dy * 0.6} {x + dx} {base + dy}" '
            f'stroke="{color}" stroke-width="{w * scale}" fill="none" stroke-linecap="round"/>'
        )
        parts.append(
            f'<path d="M{x + dx * 0.6} {base + dy * 0.55} Q{x + dx * 0.9} {base + dy * 0.75} {x + dx * 1.25} {base + dy * 0.7}" '
            f'stroke="{color}" stroke-width="{w * 0.6 * scale}" fill="none" stroke-linecap="round" opacity=".8"/>'
        )
    return "".join(parts)


def build():
    repos = json.load(open("repos.json"))
    repos = [r for r in repos if r["name"] != "iaanne"]
    repos.sort(key=lambda r: (-r["stargazers_count"], r["pushed_at"]), reverse=False)
    repos.sort(key=lambda r: (r["stargazers_count"] > 0, r["pushed_at"]), reverse=True)

    slots = []
    for ry in ROWS:
        for i in range(6):
            slots.append((100 + i * 196 + random.randint(-26, 26), ry + random.randint(-10, 10)))

    fish_svg, deco_svg = [], []
    for idx, repo in enumerate(repos[:36]):
        bx, by = slots[idx]
        facing = 1 if idx % 2 == 0 else -1
        stars = repo["stargazers_count"]
        label = LABELS.get(repo["name"])
        if stars:
            s = 1.0
        elif repo["pushed_at"] >= "2026-09":
            s = 0.72
        else:
            s = 0.5
        color = LANG_COLOR.get(repo["language"] or "None", LANG_COLOR["None"])
        kind = KIND.get(repo["language"] or "None", "plain")
        dur = 24 + (idx * 7) % 22
        bob = 5.0 + (idx * 0.37) % 3
        delay = -(idx * 2.6) % 40
        key = f"f{idx}"
        label_svg = (
            f'<text class="tag" y="{30 + 10 * s}">{html.escape(label)}</text>' if label else ""
        )
        opacity = "1" if label or stars else ".72"
        fish_svg.append(f"""
  <g transform="translate({bx} {by})" opacity="{opacity}">
    <g class="swim" style="animation-name:{key};animation-duration:{dur}s;animation-delay:{delay}s">
      <g class="bob" style="animation-duration:{bob}s;animation-delay:{delay / 2}s">
        <g transform="scale({s * facing} {s})" filter="url(#soft)">{fish_body(kind, color)}</g>
        {label_svg}
      </g>
    </g>
  </g>
  <style>@keyframes {key} {{ from {{ transform: translateX(-{int(40 + 60 * s)}px) }} to {{ transform: translateX({int(40 + 60 * s)}px) }} }}</style>""")

    # a tight school of the smallest fish, drifting together
    for i in range(6):
        x = 596 + (i % 3) * 32 + random.randint(-4, 4)
        y = 484 + (i // 3) * 20 + random.randint(-3, 3)
        col = LANG_COLOR["None"]
        deco_svg.append(f"""
  <g transform="translate({x} {y})" opacity=".45">
    <g class="bob" style="animation-duration:{4.5 + i * 0.3}s;animation-delay:-{i}s">
      <g transform="scale(-0.26 0.26)">
        <g class="tail"><path d="M-30 0 L-48 -14 L-43 0 L-48 14 Z" fill="{col}"/></g>
        <ellipse rx="26" ry="15" fill="{col}"/>
        <circle cx="16" cy="-4" r="3.2" fill="#08131c" opacity=".5"/>
      </g>
    </g>
  </g>""")

    weeds = []
    for i, (x, h, col, w) in enumerate([
        (60, 150, "#2f7d5b", 7), (96, 104, "#37986a", 6), (132, 168, "#2b6f52", 8),
        (188, 92, "#37986a", 5), (250, 126, "#2f7d5b", 6), (352, 78, "#2b6f52", 5),
        (905, 132, "#2f7d5b", 7), (948, 96, "#37986a", 5), (1000, 158, "#2b6f52", 8),
        (1050, 110, "#37986a", 6), (1100, 140, "#2f7d5b", 7), (1150, 88, "#2b6f52", 5),
        (620, 66, "#2f7d5b", 5), (700, 84, "#37986a", 5),
    ]):
        weeds.append(f"""
  <g class="weed" style="animation-duration:{5 + (i % 5)}s;animation-delay:-{i * 0.6}s">
    <path d="M{x} 540 C{x - 14} {540 - h * 0.4} {x + 16} {540 - h * 0.72} {x - 4} {540 - h}"
          stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>
  </g>""")

    bubbles = []
    for i in range(20):
        x = 40 + i * 59 + random.randint(-10, 10)
        bubbles.append(
            f'<circle class="bubble" cx="{x}" cy="540" r="{2 + (i % 4) * 0.7:.1f}" fill="#bfe9ff" opacity=".3" '
            f'style="animation-duration:{11 + i % 7}s;animation-delay:-{i * 1.7:.1f}s"/>'
        )

    corals = "".join([
        coral(300, 540, "#c96f7a", 1.1),
        coral(760, 540, "#c98a6f", 0.9),
        coral(1120, 540, "#a87ac9", 1.0),
    ])
    def star(cx, cy, r_out, r_in, color):
        pts = []
        for k in range(10):
            r = r_out if k % 2 == 0 else r_in
            a = math.radians(-90 + k * 36)
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'

    starfish = (
        '<g opacity=".92">' + star(880, 566, 18, 7, "#e0836f") + star(1128, 590, 13, 5, "#e0a06f") + "</g>"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Aquarium of @iaanne's repositories">
  <title>Aquarium: every repository is a fish, bigger fish have more stars</title>
  <defs>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d4c6b"/><stop offset="45%" stop-color="#0a3450"/><stop offset="100%" stop-color="#05192a"/>
    </linearGradient>
    <linearGradient id="sand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c9b48a"/><stop offset="100%" stop-color="#7f7052"/>
    </linearGradient>
    <linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#bfe9ff" stop-opacity=".2"/><stop offset="100%" stop-color="#bfe9ff" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="#00121c" flood-opacity=".4"/>
    </filter>
  </defs>

  <style>
    .swim {{ animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }}
    .bob {{ animation-name: bob; animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }}
    .weed {{ animation-name: sway; animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; transform-origin: bottom center; transform-box: fill-box; }}
    .bubble {{ animation-name: rise; animation-timing-function: linear; animation-iteration-count: infinite; }}
    .tail {{ animation: wiggle 1.1s ease-in-out infinite alternate; transform-origin: -28px 0; transform-box: fill-box; }}
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10px; fill: #e8f6ff; fill-opacity: .5; text-anchor: middle; letter-spacing: .3px; }}
    .frame {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; fill: #dff1ff; fill-opacity: .28; letter-spacing: 2px; }}
    @keyframes bob {{ from {{ transform: translateY(-6px) }} to {{ transform: translateY(6px) }} }}
    @keyframes sway {{ from {{ transform: rotate(-4deg) }} to {{ transform: rotate(4deg) }} }}
    @keyframes rise {{ from {{ transform: translateY(0); opacity: 0 }} 12% {{ opacity: .32 }} to {{ transform: translateY(-500px); opacity: 0 }} }}
    @keyframes wiggle {{ from {{ transform: rotate(-9deg) }} to {{ transform: rotate(9deg) }} }}
    .rays {{ animation: pulse 9s ease-in-out infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: .55 }} to {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .swim, .bob, .weed, .bubble, .tail, .rays {{ animation: none !important; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#water)"/>
  <g class="rays">
    <path d="M110 0 L300 0 L470 540 L320 540 Z" fill="url(#ray)"/>
    <path d="M430 0 L600 0 L740 540 L610 540 Z" fill="url(#ray)" opacity=".8"/>
    <path d="M770 0 L890 0 L975 540 L860 540 Z" fill="url(#ray)" opacity=".6"/>
    <path d="M1010 0 L1110 0 L1160 540 L1075 540 Z" fill="url(#ray)" opacity=".45"/>
  </g>
  <g fill="#dff1ff">
    <circle cx="1050" cy="62" r="1.6" opacity=".3"/><circle cx="975" cy="118" r="1.1" opacity=".24"/>
    <circle cx="180" cy="54" r="1.3" opacity=".2"/><circle cx="660" cy="70" r="1.0" opacity=".22"/>
    <circle cx="320" cy="140" r="1.2" opacity=".18"/><circle cx="1120" cy="200" r="1.1" opacity=".2"/>
  </g>

  <text class="frame" x="28" y="38">AQUARIUM — @IAANNE</text>
  <text class="frame" x="{W - 28}" y="38" text-anchor="end">FISH = REPOS · SIZE = STARS</text>
{"".join(fish_svg)}
{"".join(deco_svg)}
{"".join(weeds)}
  <path d="M0 540 Q 200 522 400 536 T 800 532 T {W} 540 L{W} {H} L0 {H} Z" fill="url(#sand)"/>
  <path d="M0 540 Q 200 522 400 536 T 800 532 T {W} 540 L{W} 549 L0 549 Z" fill="#e0cfa6" opacity=".32"/>
{corals}
{starfish}
  <g fill="#6f6045" opacity=".5">
    <ellipse cx="230" cy="578" rx="26" ry="9"/><ellipse cx="520" cy="592" rx="17" ry="6"/>
    <ellipse cx="700" cy="572" rx="21" ry="7"/><ellipse cx="1020" cy="588" rx="30" ry="10"/>
  </g>
{"".join(bubbles)}
  <text class="frame" x="28" y="{H - 14}">FISH SWIM ON THEIR OWN · NO DATA LEAVES THIS TANK</text>
</svg>
"""


if __name__ == "__main__":
    open("aquarium.svg", "w").write(build())
    print("wrote aquarium.svg")
