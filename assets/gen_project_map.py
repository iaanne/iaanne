#!/usr/bin/env python3
"""Generate project_map.svg: repositories as a drifting force graph.

Size is stars, colour is language, lines join projects that share a
language or a topic. Run: python3 gen_project_map.py
"""
import base64
import html
import json
import os

W, H = 1200, 620
GRAPH_TOP = 108

LANG_COLOR = {
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "Jupyter Notebook": "#DA5B0B",
    "Shell": "#89e051",
    "QML": "#44a51c",
    "JavaScript": "#f1e05a",
    "PHP": "#4F5D95",
    "Blade": "#f7523f",
    "HTML": "#e34c26",
    "None": "#8b949e",
}

# hand-placed on a 1200x620 canvas; the avatar sits in the middle
NODES = {
    # big hubs
    "rsi-penugasan1-kelompok1": (330, 300, 27),
    "rsi-penugasan4-kelompok1": (330, 445, 27),
    "rsi-penugasan2-kelompok1": (835, 285, 27),
    # second ring, labelled
    "RSI_Learning_Platform_Website": (475, 215, 14),
    "dabd-servingapi-kelompok1": (470, 375, 11),
    "nlp-rag-kelompok6": (735, 185, 13),
    "dabd-eurointellegence": (900, 158, 12),
    "ml-bisindo-multimodal-keypoint-caption": (665, 255, 11),
    "bi-olist-crm-dashboard": (800, 415, 13),
    "citra-deteksi-titik-garis-dan-tepi-kelompok4": (790, 525, 12),
    "kbr-notaris-triage-kelompok3": (955, 358, 11),
    "cloud-usgs-earthquake": (595, 455, 11),
    "midnight-shell": (1012, 245, 10),
    "imdb-showfy": (1030, 505, 9),
    # small satellites
    "ipbd-handson1": (550, 158, 7),
    "ipbd-tbp-kelompok7": (625, 130, 6.5),
    "kda-project-kelompok1": (700, 118, 6.5),
    "caelestian": (950, 132, 7),
    "praktikum-kda01": (1075, 330, 6.5),
    "komter-sinkronisasi-kelompok4": (1088, 540, 6.5),
    "komter-project-kelompok5": (900, 560, 7),
    "project_pkl": (995, 598, 6),
    "dm-finalproject-kelompok4": (700, 585, 7),
    "daa-kelompok6-kelasb": (474, 575, 6.5),
    "rosbd-finalproject-kelompok4": (385, 555, 6.5),
    "ipbd-casemethod-kelompok4": (270, 540, 6.5),
    "L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum": (220, 425, 7),
    "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS": (200, 325, 6.5),
    "citra-input-ref-kelompok4": (230, 215, 7.5),
    "citra-aritlogic-kelompok4": (300, 160, 6.5),
    "profil": (415, 140, 6.5),
    "instagram": (355, 185, 5.5),
    "izardaffa": (158, 515, 6),
    "komikloversV2": (158, 258, 6),
    "try": (528, 336, 6),
}

LABELS = {
    "rsi-penugasan1-kelompok1": "rsi-penugasan1-kelompok1",
    "rsi-penugasan4-kelompok1": "rsi-penugasan4-kelompok1",
    "rsi-penugasan2-kelompok1": "rsi-penugasan2-kelompok1",
    "nlp-rag-kelompok6": "nlp-rag-kelompok6",
    "dabd-eurointellegence": "dabd-eurointellegence",
    "ml-bisindo-multimodal-keypoint-caption": "ml-bisindo-multimodal",
    "bi-olist-crm-dashboard": "bi-olist-crm-dashboard",
    "citra-deteksi-titik-garis-dan-tepi-kelompok4": "citra-deteksi-titik-garis",
    "kbr-notaris-triage-kelompok3": "kbr-notaris-triage",
    "cloud-usgs-earthquake": "cloud-usgs-earthquake",
    "citra-input-ref-kelompok4": "citra-input-ref-kelompok4",
    "try": "try",
}

# (a, b, colour, width, flow)
EDGES = [
    # web & TypeScript cluster
    ("rsi-penugasan1-kelompok1", "rsi-penugasan4-kelompok1", "#4f8fd6", 1.4, True),
    ("rsi-penugasan1-kelompok1", "RSI_Learning_Platform_Website", "#4f8fd6", 1.1, False),
    ("rsi-penugasan4-kelompok1", "RSI_Learning_Platform_Website", "#4f8fd6", 1.1, False),
    ("RSI_Learning_Platform_Website", "dabd-servingapi-kelompok1", "#4f8fd6", 1.0, False),
    ("rsi-penugasan4-kelompok1", "dabd-servingapi-kelompok1", "#4f8fd6", 1.0, False),
    ("rsi-penugasan1-kelompok1", "citra-input-ref-kelompok4", "#4f8fd6", 0.8, False),
    ("rsi-penugasan4-kelompok1", "citra-input-ref-kelompok4", "#4f8fd6", 0.8, False),
    ("RSI_Learning_Platform_Website", "profil", "#4f8fd6", 0.7, False),
    # python data cluster
    ("rsi-penugasan2-kelompok1", "nlp-rag-kelompok6", "#3f7fd0", 1.2, False),
    ("rsi-penugasan2-kelompok1", "dabd-eurointellegence", "#3f7fd0", 1.1, False),
    ("rsi-penugasan2-kelompok1", "ml-bisindo-multimodal-keypoint-caption", "#3f7fd0", 1.2, False),
    ("rsi-penugasan2-kelompok1", "bi-olist-crm-dashboard", "#e08a4b", 2.0, True),
    ("rsi-penugasan2-kelompok1", "kbr-notaris-triage-kelompok3", "#3f7fd0", 1.2, False),
    ("nlp-rag-kelompok6", "dabd-eurointellegence", "#3f7fd0", 1.0, False),
    ("nlp-rag-kelompok6", "ml-bisindo-multimodal-keypoint-caption", "#3f7fd0", 1.1, True),
    ("bi-olist-crm-dashboard", "citra-deteksi-titik-garis-dan-tepi-kelompok4", "#3f7fd0", 1.0, False),
    ("bi-olist-crm-dashboard", "kbr-notaris-triage-kelompok3", "#3f7fd0", 0.9, False),
    ("kbr-notaris-triage-kelompok3", "praktikum-kda01", "#3f7fd0", 0.6, False),
    ("cloud-usgs-earthquake", "bi-olist-crm-dashboard", "#3f7fd0", 0.9, False),
    ("cloud-usgs-earthquake", "rsi-penugasan2-kelompok1", "#3f7fd0", 0.7, False),
    ("ml-bisindo-multimodal-keypoint-caption", "cloud-usgs-earthquake", "#3f7fd0", 0.8, False),
    ("try", "ml-bisindo-multimodal-keypoint-caption", "#8b949e", 0.7, False),
    ("RSI_Learning_Platform_Website", "rsi-penugasan2-kelompok1", "#3f7fd0", 0.6, False),
    # notebooks & campus
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS", "#DA5B0B", 0.8, False),
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "daa-kelompok6-kelasb", "#DA5B0B", 0.7, False),
    ("L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "rsi-penugasan4-kelompok1", "#30363d", 0.6, False),
    ("rosbd-finalproject-kelompok4", "ipbd-casemethod-kelompok4", "#3f7fd0", 0.7, False),
    ("rosbd-finalproject-kelompok4", "rsi-penugasan4-kelompok1", "#30363d", 0.6, False),
    ("dm-finalproject-kelompok4", "citra-deteksi-titik-garis-dan-tepi-kelompok4", "#DA5B0B", 0.7, False),
    ("citra-aritlogic-kelompok4", "citra-input-ref-kelompok4", "#3f7fd0", 0.7, False),
    ("ipbd-handson1", "ipbd-tbp-kelompok7", "#3f7fd0", 0.8, False),
    ("ipbd-tbp-kelompok7", "kda-project-kelompok1", "#3f7fd0", 0.8, False),
    ("kda-project-kelompok1", "nlp-rag-kelompok6", "#3f7fd0", 0.7, False),
    ("kda-project-kelompok1", "caelestian", "#30363d", 0.6, False),
    # desktop & php
    ("caelestian", "midnight-shell", "#44a51c", 1.0, True),
    ("midnight-shell", "kbr-notaris-triage-kelompok3", "#44a51c", 0.6, False),
    ("komter-project-kelompok5", "komter-sinkronisasi-kelompok4", "#4F5D95", 0.8, False),
    ("komter-project-kelompok5", "imdb-showfy", "#f7523f", 0.8, False),
    ("komter-sinkronisasi-kelompok4", "project_pkl", "#4F5D95", 0.7, False),
    ("profil", "instagram", "#e34c26", 0.6, False),
    ("instagram", "izardaffa", "#30363d", 0.5, False),
    ("izardaffa", "komikloversV2", "#30363d", 0.5, False),
    ("komikloversV2", "citra-input-ref-kelompok4", "#30363d", 0.5, False),
]


def esc(text):
    return html.escape(text)


def short(label, limit=24):
    return label if len(label) <= limit else label[: limit - 3] + "..."


def build():
    repos = {r["name"]: r for r in json.load(open("repos.json"))}
    repos.pop("iaanne", None)
    missing = [n for n in repos if n not in NODES]
    if missing:
        raise SystemExit("no position for: " + ", ".join(missing))

    out = []
    out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Project map of @iaanne">
  <title>Project map: every repository as a node, size is stars, lines join related work</title>
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1f6feb" stop-opacity=".20"/>
      <stop offset="100%" stop-color="#1f6feb" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="avatar"><circle cx="600" cy="330" r="30"/></clipPath>
    <style>
      .nodetext {{ font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
      .drift {{ animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }}
      .edge {{ animation: dash 14s linear infinite; }}
      @keyframes dash {{ to {{ stroke-dashoffset: -160; }} }}
      .halo {{ animation: halo 4s ease-in-out infinite alternate; }}
      @keyframes halo {{ from {{ opacity: .18 }} to {{ opacity: .5 }} }}
      /* camera push: the map eases in and back out, the way the graph
         zooms under the pointer on a hover-capable viewer */
      #cam {{ animation: camera 18s ease-in-out infinite; }}
      @keyframes camera {{
        0%, 52% {{ transform: scale(1); }}
        66%, 80% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
      }}
      #hoverzoom {{ transition: transform .55s cubic-bezier(.25,.6,.3,1); }}
      svg:hover #hoverzoom {{ transform: scale(1.05); }}
      @media (prefers-reduced-motion: reduce) {{
        .drift, .edge, .halo, #cam {{ animation: none !important; }}
        #hoverzoom {{ transition: none; }}
      }}
    </style>
  </defs>
  <rect width="{W}" height="{H}" fill="#0d1117"/>
  <circle cx="600" cy="330" r="330" fill="url(#glow)"/>
  <text x="36" y="34" font-size="11" font-weight="700" letter-spacing="3" fill="#3fb950"
        font-family="ui-monospace, SFMono-Regular, Menlo, monospace">PROJECT MAP</text>
  <text x="36" y="66" font-size="23" font-weight="700" fill="#e6edf3" class="nodetext">Everything I build, and how it connects</text>
  <text x="36" y="88" font-size="12.5" fill="#8b949e" class="nodetext">Size is stars. Lines join projects that share a language or topics.</text>
  <g transform="translate(600 325)"><g id="cam"><g id="hoverzoom"><g transform="translate(-600 -325)">
''')

    # edges first, under the nodes
    for i, (a, b, colour, width, flow) in enumerate(EDGES):
        ax, ay, _ = NODES[a]
        bx, by, _ = NODES[b]
        dash = ' stroke-dasharray="3 9"' if flow else ""
        out.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{colour}" '
            f'stroke-width="{width}" stroke-opacity="{0.55 if flow else 0.32}" '
            f'stroke-linecap="round"{dash} class="edge" style="animation-delay:-{i * 1.7:.1f}s"/>'
        )

    # the avatar sits at the centre of the map
    avatar = base64.b64encode(open(os.path.join(os.path.dirname(__file__), "avatar.png"), "rb").read()).decode()
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
        lang = repo.get("language") or "None"
        colour = LANG_COLOR.get(lang, LANG_COLOR["None"])
        stars = repo["stargazers_count"]
        label = LABELS.get(name)
        dx = 2.2 + (idx % 4) * 0.9
        dy = 2.6 + (idx % 5) * 0.8
        dur = 5.4 + (idx % 7) * 0.7
        delay = -(idx * 1.13) % 9

        parts = [f'  <g transform="translate({x} {y})">',
                 f'    <g class="drift" style="animation-name:d{idx};animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">']

        if not label:
            parts.append(f'      <circle r="{r}" fill="{colour}" fill-opacity=".55"/>')
        elif lang == "TypeScript" and r >= 20:
            parts.append(f'      <circle r="{r}" fill="{colour}"/>')
            parts.append(f'      <circle r="{r}" fill="#fff" fill-opacity=".07"/>')
            parts.append(f'      <text y="6" text-anchor="middle" font-size="18" font-weight="700" fill="#ffffff" '
                         f'font-family="ui-sans-serif, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif">TS</text>')
        elif lang == "Python" and r >= 20:
            parts.append(f'      <circle r="{r}" fill="#f0f6fc"/>')
            parts.append(f'      <g transform="translate(0 0) scale({r / 16:.2f}) translate(-12 -12)">')
            parts.append(f'        <path fill="#3572A5" d="{PYTHON_PATH}"/>')
            parts.append('      </g>')
        else:
            parts.append(f'      <circle r="{r}" fill="{colour}"/>')
            parts.append(f'      <circle r="{r}" fill="#fff" fill-opacity=".08"/>')

        if label:
            # halo under the text keeps labels readable where a line crosses
            ly = r + 21
            parts.append(f'      <text y="{ly}" text-anchor="middle" font-size="11.5" fill="#e6edf3" class="nodetext" '
                         f'stroke="#0d1117" stroke-width="3.2" stroke-opacity=".85" paint-order="stroke">{esc(short(label))}</text>')
            parts.append(f'      <text y="{ly + 14}" text-anchor="middle" font-size="9.5" fill="#8b949e" class="nodetext">'
                         f'★ {stars}</text>')

        parts.append("    </g>")
        parts.append("  </g>")
        out.append("\n".join(parts))
        out.append(f'  <style>@keyframes d{idx} {{ from {{ transform: translate(-{dx:.1f}px, {dy:.1f}px) }} '
                   f'to {{ transform: translate({dx:.1f}px, -{dy:.1f}px) }} }}</style>')

    out.append("</g></g></g></g>")
    out.append("</svg>\n")
    return "\n".join(out)


# simple-icons python glyph, CC0
PYTHON_PATH = (
    'M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z'
)


if __name__ == "__main__":
    open("project_map.svg", "w").write(build())
    print("wrote project_map.svg")
