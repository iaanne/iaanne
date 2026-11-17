#!/usr/bin/env python3
"""Generate aquarium.svg: an animated GitHub-profile tank for @iaanne.

Fish = repositories, sized by stars. Run: python3 gen_aquarium.py
"""
import html

W, H = 1200, 560

LANG_COLOR = {
    "Python": "#3fa08e",
    "TypeScript": "#3f7fd0",
    "Jupyter Notebook": "#e08a4b",
    "Shell": "#8fd46a",
    "QML": "#6fbf73",
    "JavaScript": "#e8d66b",
    "PHP": "#8f8fd6",
    "Blade": "#f2726a",
    "HTML": "#e8765f",
    "None": "#93b3c7",
}

# (repo, label, language, stars, base x, base y, facing 1=right -1=left, swim s, bob s, delay s)
FISH = [
    ("rsi-penugasan4-kelompok1", "rsi-penugasan4", "TypeScript", 1, 250, 128,  1, 30, 6.5, -12),
    ("rsi-penugasan2-kelompok1", "rsi-penugasan2", "Python",     1, 640, 236, -1, 36, 7.5, -30),
    ("rsi-penugasan1-kelompok1", "rsi-penugasan1", "TypeScript", 1, 390, 348,  1, 28, 6.0, -55),
    ("ml-bisindo-multimodal-keypoint-caption", "ml-bisindo", "None", 0, 980, 196, -1, 42, 8.0, -8),
    ("dabd-eurointellegence", "dabd-eurointellegence", "Python", 0, 880, 300,  1, 34, 7.0, -40),
    ("bi-olist-crm-dashboard", "bi-olist-crm", "Python", 0, 200, 402, -1, 38, 8.5, -62),
    ("cloud-usgs-earthquake", "cloud-usgs-earthquake", "Shell", 0, 700, 424,  1, 40, 9.0, -20),
    ("midnight-shell", "midnight-shell", "QML", 0, 760, 152, -1, 32, 7.2, -70),
    ("kbr-notaris-triage-kelompok3", "kbr-notaris-triage", "None", 0, 180, 268,  1, 44, 8.2, -48),
    ("nlp-rag-kelompok6", "nlp-rag", "None", 0, 1020, 372, 1, 33, 7.8, -5),
]

AMP = 130  # how far a fish drifts from its home position

KIND = {
    "TypeScript": "pair",
    "Python": "round",
    "Shell": "torpedo",
    "QML": "angelfish",
    "None": "plain",
}

SCALE_STAR = {1: 1.0, 0: 0.62}


def fish_paths(kind, color):
    """Return the body markup for one fish style (facing right, origin at body centre)."""
    dark = "#0a1620"
    if kind == "round":
        body = (
            f'<ellipse rx="30" ry="21" fill="{color}"/>'
            f'<ellipse rx="30" ry="21" fill="#ffffff" opacity=".08"/>'
        )
        fin_top = f'<path d="M-4 -19 Q6 -34 16 -16 Z" fill="{color}" opacity=".75"/>'
        fin_side = f'<path d="M-2 18 Q8 30 14 16 Z" fill="{color}" opacity=".6"/>'
    elif kind == "pair":
        body = (
            f'<ellipse rx="34" ry="17" fill="{color}"/>'
            f'<ellipse rx="34" ry="17" fill="#ffffff" opacity=".07"/>'
        )
        fin_top = f'<path d="M-8 -15 Q2 -30 12 -13 Z" fill="{color}" opacity=".8"/>'
        fin_side = f'<path d="M-6 14 Q4 26 12 13 Z" fill="{color}" opacity=".6"/>'
    elif kind == "torpedo":
        body = (
            f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="{color}"/>'
            f'<path d="M-36 0 Q-8 -16 26 -11 Q38 -6 40 0 Q38 6 26 11 Q-8 16 -36 0 Z" fill="#ffffff" opacity=".07"/>'
        )
        fin_top = f'<path d="M-2 -11 Q4 -22 12 -10 Z" fill="{color}" opacity=".8"/>'
        fin_side = f'<path d="M2 11 Q8 20 14 10 Z" fill="{color}" opacity=".55"/>'
    elif kind == "angelfish":
        body = (
            f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="{color}"/>'
            f'<path d="M-26 0 Q-14 -32 4 -30 Q26 -26 30 0 Q26 26 4 30 Q-14 32 -26 0 Z" fill="#ffffff" opacity=".06"/>'
            f'<path d="M-10 -20 L2 -46 L10 -18 Z" fill="{color}" opacity=".7"/>'
        )
        fin_top = ""
        fin_side = f'<path d="M-10 20 L2 44 L10 18 Z" fill="{color}" opacity=".5"/>'
    else:
        body = f'<ellipse rx="26" ry="15" fill="{color}"/><ellipse rx="26" ry="15" fill="#ffffff" opacity=".07"/>'
        fin_top = f'<path d="M-4 -13 Q4 -24 12 -12 Z" fill="{color}" opacity=".75"/>'
        fin_side = f'<path d="M-2 12 Q6 22 12 11 Z" fill="{color}" opacity=".55"/>'

    tail = (
        f'<g class="tail"><path d="M-30 0 L-52 -16 L-46 0 L-52 16 Z" fill="{color}" opacity=".85"/></g>'
    )
    eye_x = 18
    eye = (
        f'<circle cx="{eye_x}" cy="-4" r="4" fill="#f7fbfd"/>'
        f'<circle cx="{eye_x + 0.8}" cy="-4" r="2" fill="{dark}"/>'
        f'<path d="M{eye_x - 2} -11 q 9 3 0 7" stroke="{dark}" stroke-width="1.1" fill="none" opacity=".45"/>'
        f'<path d="M{eye_x + 12} 6 q 6 -3 0 -5" stroke="{dark}" stroke-width="1.1" fill="none" opacity=".4"/>'
    )
    return tail + fin_top + fin_side + body + eye


def build():
    fish_svg = []
    for name, label, lang, stars, x, y, facing, dur, bob, delay in FISH:
        color = LANG_COLOR.get(lang, LANG_COLOR["None"])
        kind = KIND.get(lang, "plain")
        s = SCALE_STAR.get(stars, 0.62)
        key = f"{label[:6]}-{y}".replace("_", "")
        fish_svg.append(f"""
  <g transform="translate({x} {y})">
    <g class="swim" style="animation-name:swim-{key};animation-duration:{dur}s;animation-delay:{delay}s">
      <g class="bob" style="animation-duration:{bob}s;animation-delay:{delay / 2}s">
        <g transform="scale({s * facing} {s})" filter="url(#soft)">
          {fish_paths(kind, color)}
        </g>
        <text class="tag" y="{28 + 9 * s}">{html.escape(label)}</text>
      </g>
    </g>
  </g>
  <style>@keyframes swim-{key} {{ from {{ transform: translateX(-{AMP}px) }} to {{ transform: translateX({AMP}px) }} }}</style>""")

    # small unlabelled fish: the rest of the repos, kept vague on purpose
    decor = []
    for i, (x, y, facing, dur, delay) in enumerate([
        (120, 190, 1, 26, -4), (330, 92, -1, 31, -17), (540, 430, 1, 24, -9),
        (860, 96, 1, 29, -22), (1090, 300, -1, 27, -13), (460, 196, -1, 33, -6),
    ]):
        col = "#7fb3c9"
        key = f"deco-{i}"
        decor.append(f"""
  <g transform="translate({x} {y})" opacity=".38">
    <g class="swim" style="animation-name:swim-{key};animation-duration:{dur}s;animation-delay:{delay}s">
      <g class="bob" style="animation-duration:{5 + i * 0.4}s">
        <g transform="scale({0.34 * facing} 0.34)">
          <g class="tail"><path d="M-30 0 L-50 -15 L-44 0 L-50 15 Z" fill="{col}"/></g>
          <ellipse rx="26" ry="15" fill="{col}"/>
          <circle cx="16" cy="-4" r="3.4" fill="#0a1620" opacity=".55"/>
        </g>
      </g>
    </g>
  </g>
  <style>@keyframes swim-{key} {{ from {{ transform: translateX(-90px) }} to {{ transform: translateX(90px) }} }}</style>""")

    weeds = []
    for i, (x, h, col) in enumerate([
        (70, 120, "#2f7d5b"), (105, 88, "#37986a"), (150, 140, "#2b6f52"),
        (930, 110, "#2f7d5b"), (985, 150, "#37986a"), (1030, 96, "#2b6f52"),
        (1085, 130, "#2f7d5b"), (760, 74, "#2b6f52"), (520, 62, "#2f7d5b"),
    ]):
        weeds.append(f"""
  <g class="weed" style="animation-duration:{6 + (i % 4)}s;animation-delay:-{i * 0.7}s">
    <path d="M{x} 470 C{x - 14} {470 - h * 0.4} {x + 14} {470 - h * 0.7} {x - 4} {470 - h}"
          stroke="{col}" stroke-width="{7 - (i % 3)}" fill="none" stroke-linecap="round"/>
  </g>""")

    bubbles = []
    for i, (x, r, dur, delay) in enumerate([
        (200, 3.5, 15, -2), (250, 2.4, 19, -9), (330, 4.2, 13, -5),
        (430, 2.8, 17, -12), (600, 3.2, 16, -7), (700, 4.6, 12, -3),
        (820, 2.6, 20, -14), (880, 3.8, 14, -6), (960, 2.2, 18, -11),
    ]):
        bubbles.append(f"""
  <circle class="bubble" cx="{x}" cy="470" r="{r}" fill="#bfe9ff" opacity=".35"
          style="animation-duration:{dur}s;animation-delay:{delay}s"/>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Aquarium of @iaanne's repositories">
  <title>Aquarium: each fish is a repository, bigger fish have more stars</title>
  <defs>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d4c6b"/>
      <stop offset="45%" stop-color="#0a3450"/>
      <stop offset="100%" stop-color="#061c2b"/>
    </linearGradient>
    <linearGradient id="sand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c9b48a"/>
      <stop offset="100%" stop-color="#8a7a58"/>
    </linearGradient>
    <linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#bfe9ff" stop-opacity=".22"/>
      <stop offset="100%" stop-color="#bfe9ff" stop-opacity="0"/>
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
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10px; fill: #e8f6ff; fill-opacity: .52; text-anchor: middle; letter-spacing: .3px; }}
    .frame {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; fill: #dff1ff; fill-opacity: .3; letter-spacing: 2px; }}
    @keyframes bob {{ from {{ transform: translateY(-6px) }} to {{ transform: translateY(6px) }} }}
    @keyframes sway {{ from {{ transform: rotate(-4deg) }} to {{ transform: rotate(4deg) }} }}
    @keyframes rise {{ from {{ transform: translateY(0); opacity: 0 }} 12% {{ opacity: .35 }} to {{ transform: translateY(-430px); opacity: 0 }} }}
    @keyframes wiggle {{ from {{ transform: rotate(-9deg) }} to {{ transform: rotate(9deg) }} }}
    .rays {{ animation: pulse 9s ease-in-out infinite alternate; }}
    @keyframes pulse {{ from {{ opacity: .5 }} to {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .swim, .bob, .weed, .bubble, .tail, .rays {{ animation: none !important; }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#water)"/>

  <g class="rays">
    <path d="M120 0 L300 0 L470 470 L330 470 Z" fill="url(#ray)"/>
    <path d="M430 0 L600 0 L740 470 L620 470 Z" fill="url(#ray)" opacity=".8"/>
    <path d="M760 0 L880 0 L960 470 L850 470 Z" fill="url(#ray)" opacity=".6"/>
  </g>

  <circle cx="1050" cy="70" r="1.6" fill="#dff1ff" opacity=".3"/>
  <circle cx="980" cy="120" r="1.1" fill="#dff1ff" opacity=".25"/>
  <circle cx="180" cy="60" r="1.3" fill="#dff1ff" opacity=".2"/>

  <text class="frame" x="28" y="38">AQUARIUM — @IAANNE</text>
  <text class="frame" x="{W - 28}" y="38" text-anchor="end">FISH = REPOS · SIZE = STARS</text>
{"".join(fish_svg)}
{"".join(decor)}
{"".join(weeds)}

  <path d="M0 470 Q 200 452 400 466 T 800 462 T {W} 470 L{W} {H} L0 {H} Z" fill="url(#sand)"/>
  <path d="M0 470 Q 200 452 400 466 T 800 462 T {W} 470 L{W} 478 L0 478 Z" fill="#e0cfa6" opacity=".35"/>
  <ellipse cx="250" cy="500" rx="26" ry="9" fill="#6f6045" opacity=".55"/>
  <ellipse cx="520" cy="516" rx="16" ry="6" fill="#6f6045" opacity=".5"/>
  <ellipse cx="700" cy="494" rx="20" ry="7" fill="#6f6045" opacity=".45"/>
  <ellipse cx="1010" cy="512" rx="30" ry="10" fill="#6f6045" opacity=".5"/>
{"".join(bubbles)}

  <text class="frame" x="28" y="{H - 16}">FISH SWIM ON THEIR OWN · NO DATA LEAVES THIS TANK</text>
</svg>
"""


if __name__ == "__main__":
    open("aquarium.svg", "w").write(build())
    print("wrote aquarium.svg")
