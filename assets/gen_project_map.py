#!/usr/bin/env python3
"""Generate project_map.svg: repositories as a drifting force graph.

Size is stars, colour is language, lines join projects that share a
language or a topic. The map itself stays still; small dots travel along
every line so the README shows motion without zooming. Run: python3 gen_project_map.py
"""
import html
import json
import os
import re

W, H = 1200, 620
GRAPH_TOP = 108
HERE = os.path.dirname(os.path.abspath(__file__))

LANG_COLOR = {
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "Jupyter Notebook": "#DA5B0B",
    "Shell": "#3fb950",
    "QML": "#44a51c",
    "JavaScript": "#d9c93a",
    "PHP": "#4F5D95",
    "Blade": "#f7523f",
    "HTML": "#e34c26",
    "CSS": "#663399",
    "C++": "#f34b7d",
    "None": "#8b949e",
}

# simple-icons slugs, drawn white inside the coloured node
ICON = {
    "Python": "python",
    "TypeScript": "typescript",
    "Jupyter Notebook": "jupyter",
    "Shell": "gnubash",
    "JavaScript": "javascript",
    "QML": "qt",
    "PHP": "php",
    "Blade": "laravel",
    "HTML": "html5",
    "CSS": "css",
    "C++": "cplusplus",
}

# hand-placed on a 1200x620 canvas; the avatar sits in the middle
NODES = {
    # big hubs
    "rsi-penugasan1-kelompok1": (330, 300, 27),
    "rsi-penugasan4-kelompok1": (330, 445, 27),
    "rsi-penugasan2-kelompok1": (835, 285, 27),
    # second ring, labelled
    "portfolio": (1105, 430, 18),
    "RSI_Learning_Platform_Website": (475, 215, 14),
    "dabd-servingapi-kelompok1": (470, 375, 11),
    "nlp-rag-LLMMenuMasakanIndonesia": (735, 185, 13),
    "dabd-eurointellegence": (900, 158, 12),
    "ml-bisindo-multimodal-keypoint-caption": (665, 255, 11),
    "bi-olist-crm-dashboard": (800, 415, 13),
    "citra-deteksi-titik-garis-dan-tepi-kelompok4": (786, 512, 12),
    "kbr-notaristriage": (955, 358, 11),
    "cloud-usgs-earthquake": (595, 455, 11),
    "midnight-shell": (1012, 245, 10),
    "imdb-showfy": (1040, 495, 9),
    # small satellites
    "ipbd-handson1": (550, 158, 7),
    "ipbd-tbp-kelompok7": (625, 130, 6.5),
    "kda-project-kelompok1": (700, 118, 6.5),
    "caelestian": (950, 132, 7),
    "praktikum-kda01": (1075, 330, 6.5),
    "komter-sinkronisasi-kelompok4": (1080, 520, 6.5),
    "komter-project-kelompok5": (912, 545, 7),
    "project_pkl": (995, 560, 6),
    "dm-finalproject-kelompok4": (700, 556, 7),
    "daa-kelompok6-kelasb": (474, 560, 6.5),
    "rosbd-finalproject-kelompok4": (390, 545, 6.5),
    "ipbd-casemethod-kelompok4": (268, 530, 6.5),
    "L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum": (220, 425, 7),
    "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS": (200, 325, 6.5),
    "citra-input-ref-kelompok4": (230, 215, 7.5),
    "citra-aritlogic-kelompok4": (300, 160, 6.5),
    "profil": (415, 140, 6.5),
    "instagram": (355, 185, 5.5),
    "izardaffa": (150, 505, 6),
    "komikloversV2": (158, 258, 6),
    "try": (528, 336, 6),
}

LABELS = {
    "rsi-penugasan1-kelompok1": "rsi-penugasan1-kelompok1",
    "rsi-penugasan4-kelompok1": "rsi-penugasan4-kelompok1",
    "rsi-penugasan2-kelompok1": "rsi-penugasan2-kelompok1",
    "nlp-rag-LLMMenuMasakanIndonesia": "nlp-rag",
    "dabd-eurointellegence": "dabd-eurointellegence",
    "ml-bisindo-multimodal-keypoint-caption": "ml-bisindo-multimodal",
    "bi-olist-crm-dashboard": "bi-olist-crm-dashboard",
    "citra-deteksi-titik-garis-dan-tepi-kelompok4": "citra-deteksi-titik-garis",
    "kbr-notaristriage": "kbr-notaristriage",
    "cloud-usgs-earthquake": "cloud-usgs-earthquake",
    "citra-input-ref-kelompok4": "citra-input-ref-kelompok4",
    "portfolio": "portfolio · live",
    "try": "try",
}

# (a, b, colour, width)
EDGES = [
    # web & TypeScript cluster
    ("rsi-penugasan1-kelompok1", "rsi-penugasan4-kelompok1", "#4f8fd6", 1.4),
    ("rsi-penugasan1-kelompok1", "RSI_Learning_Platform_Website", "#4f8fd6", 1.1),
    ("rsi-penugasan4-kelompok1", "RSI_Learning_Platform_Website", "#4f8fd6", 1.1),
    ("RSI_Learning_Platform_Website", "dabd-servingapi-kelompok1", "#4f8fd6", 1.0),
    ("rsi-penugasan4-kelompok1", "dabd-servingapi-kelompok1", "#4f8fd6", 1.0),
    ("rsi-penugasan1-kelompok1", "citra-input-ref-kelompok4", "#4f8fd6", 0.8),
    ("rsi-penugasan4-kelompok1", "citra-input-ref-kelompok4", "#4f8fd6", 0.8),
    ("RSI_Learning_Platform_Website", "profil", "#4f8fd6", 0.7),
    ("portfolio", "rsi-penugasan4-kelompok1", "#4f8fd6", 1.2),
    ("portfolio", "rsi-penugasan1-kelompok1", "#4f8fd6", 1.0),
    ("portfolio", "kbr-notaristriage", "#4f8fd6", 0.8),
    # python data cluster
    ("rsi-penugasan2-kelompok1", "nlp-rag-LLMMenuMasakanIndonesia", "#3f7fd0", 1.2),
    ("rsi-penugasan2-kelompok1", "dabd-eurointellegence", "#3f7fd0", 1.1),
    ("rsi-penugasan2-kelompok1", "ml-bisindo-multimodal-keypoint-caption", "#3f7fd0", 1.2),
    ("rsi-penugasan2-kelompok1", "bi-olist-crm-dashboard", "#e08a4b", 2.0),
    ("rsi-penugasan2-kelompok1", "kbr-notaristriage", "#3f7fd0", 1.2),
    ("nlp-rag-LLMMenuMasakanIndonesia", "dabd-eurointellegence", "#3f7fd0", 1.0),
    ("nlp-rag-LLMMenuMasakanIndonesia", "ml-bisindo-multimodal-keypoint-caption", "#3f7fd0", 1.1),
    ("bi-olist-crm-dashboard", "citra-deteksi-titik-garis-dan-tepi-kelompok4", "#3f7fd0", 1.0),
    ("bi-olist-crm-dashboard", "kbr-notaristriage", "#3f7fd0", 0.9),
    ("kbr-notaristriage", "praktikum-kda01", "#3f7fd0", 0.6),
    ("cloud-usgs-earthquake", "bi-olist-crm-dashboard", "#3f7fd0", 0.9),
    ("cloud-usgs-earthquake", "rsi-penugasan2-kelompok1", "#3f7fd0", 0.7),
    ("ml-bisindo-multimodal-keypoint-caption", "cloud-usgs-earthquake", "#3f7fd0", 0.8),
    ("try", "ml-bisindo-multimodal-keypoint-caption", "#8b949e", 0.7),
    ("RSI_Learning_Platform_Website", "rsi-penugasan2-kelompok1", "#3f7fd0", 0.6),
    # notebooks & campus
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS", "#DA5B0B", 0.8),
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "daa-kelompok6-kelasb", "#DA5B0B", 0.7),
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "rsi-penugasan4-kelompok1", "#30363d", 0.6),
    ("rosbd-finalproject-kelompok4", "ipbd-casemethod-kelompok4", "#3f7fd0", 0.7),
    ("rosbd-finalproject-kelompok4", "rsi-penugasan4-kelompok1", "#30363d", 0.6),
    ("dm-finalproject-kelompok4", "citra-deteksi-titik-garis-dan-tepi-kelompok4", "#DA5B0B", 0.7),
    ("citra-aritlogic-kelompok4", "citra-input-ref-kelompok4", "#3f7fd0", 0.7),
    ("ipbd-handson1", "ipbd-tbp-kelompok7", "#3f7fd0", 0.8),
    ("ipbd-tbp-kelompok7", "kda-project-kelompok1", "#3f7fd0", 0.8),
    ("kda-project-kelompok1", "nlp-rag-LLMMenuMasakanIndonesia", "#3f7fd0", 0.7),
    ("kda-project-kelompok1", "caelestian", "#30363d", 0.6),
    # desktop & php
    ("caelestian", "midnight-shell", "#44a51c", 1.0),
    ("midnight-shell", "kbr-notaristriage", "#44a51c", 0.6),
    ("komter-project-kelompok5", "komter-sinkronisasi-kelompok4", "#4F5D95", 0.8),
    ("komter-project-kelompok5", "imdb-showfy", "#f7523f", 0.8),
    ("komter-sinkronisasi-kelompok4", "project_pkl", "#4F5D95", 0.7),
    ("profil", "instagram", "#e34c26", 0.6),
    ("instagram", "izardaffa", "#30363d", 0.5),
    ("izardaffa", "komikloversV2", "#30363d", 0.5),
    ("komikloversV2", "citra-input-ref-kelompok4", "#30363d", 0.5),
]


def esc(text):
    return html.escape(text)


def short(label, limit=24):
    return label if len(label) <= limit else label[: limit - 3] + "..."


def icon_symbols():
    out = []
    for lang, slug in ICON.items():
        raw = open(os.path.join(HERE, "si", slug + ".svg")).read()
        paths = re.findall(r'<path[^>]*d="([^"]+)"', raw)
        out.append(
            f'<symbol id="mi-{slug}" viewBox="0 0 24 24">'
            + "".join(f'<path fill="#ffffff" d="{d}"/>' for d in paths)
            + "</symbol>"
        )
    return "".join(out)


def build():
    repos = {r["name"]: r for r in json.load(open(os.path.join(HERE, "repos.json")))}
    repos.pop("iaanne", None)
    missing = [n for n in repos if n not in NODES]
    if missing:
        raise SystemExit("no position for: " + ", ".join(missing))
    stale = [n for n in NODES if n not in repos]
    if stale:
        raise SystemExit("position for missing repo: " + ", ".join(stale))

    counts = {}
    for name in repos:
        lang = primary_lang(repos[name])
        counts[lang] = counts.get(lang, 0) + 1

    out = []
    out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Project map of @iaanne">
  <title>Project map: every repository as a node, size is stars, dots travel between related work</title>
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1f6feb" stop-opacity=".20"/>
      <stop offset="100%" stop-color="#1f6feb" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="avatar"><circle cx="600" cy="330" r="30"/></clipPath>
    <style>
      .nodetext {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
      .halo {{ animation: halo 4s ease-in-out infinite alternate; }}
      @keyframes halo {{ from {{ opacity: .18 }} to {{ opacity: .5 }} }}
      @media (prefers-reduced-motion: reduce) {{
        .halo, .dot {{ animation: none !important; visibility: hidden; }}
      }}
    </style>
    {icon_symbols()}
  </defs>
  <rect width="{W}" height="{H}" fill="#0d1117"/>
  <circle cx="600" cy="330" r="330" fill="url(#glow)"/>
  <text x="36" y="34" font-size="11" font-weight="700" letter-spacing="3" fill="#3fb950"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">PROJECT MAP</text>
  <text x="36" y="66" font-size="23" font-weight="700" fill="#e6edf3" class="nodetext">Everything I build, and how it connects</text>
  <text x="36" y="88" font-size="12.5" fill="#8b949e" class="nodetext">Size is stars. Dots travel along lines that join projects sharing a language or topics.</text>
''')

    # edges first, under the nodes
    for i, (a, b, colour, width) in enumerate(EDGES):
        ax, ay, _ = NODES[a]
        bx, by, _ = NODES[b]
        out.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{colour}" '
            f'stroke-width="{width}" stroke-opacity="0.28" stroke-linecap="round"/>'
        )

    # the avatar sits at the centre of the map
    import base64
    avatar = base64.b64encode(open(os.path.join(HERE, "avatar.png"), "rb").read()).decode()
    out.append(f'''  <g>
    <circle cx="600" cy="330" r="34" fill="#1f6feb" opacity=".16" class="halo"/>
    <circle cx="600" cy="330" r="31" fill="none" stroke="#7ee787" stroke-opacity=".35"/>
    <image href="data:image/png;base64,{avatar}" x="570" y="300" width="60" height="60" clip-path="url(#avatar)" preserveAspectRatio="xMidYMid slice"/>
    <circle cx="600" cy="330" r="30" fill="none" stroke="#0d1117" stroke-width="2"/>
  </g>
''')

    # nodes
    for idx, (name, (x, y, r)) in enumerate(NODES.items()):
        repo = repos[name]
        lang = primary_lang(repo)
        colour = LANG_COLOR.get(lang, LANG_COLOR["None"])
        stars = repo["stargazers_count"]
        label = LABELS.get(name)
        slug = ICON.get(lang)

        parts = [f'  <g transform="translate({x} {y})">',
                 f'    <circle r="{r}" fill="{colour}"/>',
                 f'    <circle r="{r}" fill="#fff" fill-opacity=".07"/>']
        if slug and r >= 8.5:
            inner = r * 1.26
            parts.append(
                f'    <use href="#mi-{slug}" xlink:href="#mi-{slug}" x="{-inner / 2:.1f}" y="{-inner / 2:.1f}" '
                f'width="{inner:.1f}" height="{inner:.1f}"/>'
            )
        if label:
            # halo under the text keeps labels readable where a line crosses
            ly = r + 21
            parts.append(f'    <text y="{ly}" text-anchor="middle" font-size="11.5" fill="#e6edf3" class="nodetext" '
                         f'stroke="#0d1117" stroke-width="3.2" stroke-opacity=".85" paint-order="stroke">{esc(short(label))}</text>')
            parts.append(f'    <text y="{ly + 14}" text-anchor="middle" font-size="9.5" fill="#8b949e" class="nodetext">'
                         f'★ {stars}</text>')
        parts.append("  </g>")
        out.append("\n".join(parts))

    # moving dots, two per edge, staggered so they never march in step
    for i, (a, b, colour, width) in enumerate(EDGES):
        ax, ay, _ = NODES[a]
        bx, by, _ = NODES[b]
        dur = 5.6 + (i % 5) * 1.3
        dot_colour = "#8b949e" if colour == "#30363d" else colour
        for k in range(2):
            begin = -((i * 1.7 + k * dur / 2) % dur)
            out.append(
                f'  <g class="dot"><circle r="3" fill="{dot_colour}">'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.82;1" '
                f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
                f'<animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite" '
                f'path="M{ax},{ay} L{bx},{by}"/></circle></g>'
            )

    # legend at the bottom
    order = [k for k in LANG_COLOR if k in counts]
    lx = 36.0
    for lang in order:
        colour = LANG_COLOR[lang]
        out.append(f'<g transform="translate({lx:.1f} {H - 16})">'
                   f'<circle cx="3" cy="-4" r="4" fill="{colour}"/>'
                   f'<text x="13" y="0" font-size="12" fill="#8b949e" class="nodetext">{esc(lang)}'
                   f'<tspan fill="#484f58"> · {counts[lang]}</tspan></text></g>')
        lx += 32 + len(lang) * 7.1
    out.append(f'<text x="{W - 36}" y="{H - 16}" text-anchor="end" font-size="12" fill="#484f58" class="nodetext">'
               f'{len(repos)} repos · {len(EDGES)} links</text>')
    out.append("</svg>\n")
    return "\n".join(out)


def primary_lang(repo):
    langs = repo.get("languages") or {}
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    return ranked[0][0] if ranked else (repo.get("language") or "None")


if __name__ == "__main__":
    open(os.path.join(HERE, "project_map.svg"), "w").write(build())
    print("wrote project_map.svg")
