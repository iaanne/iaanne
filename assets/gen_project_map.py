#!/usr/bin/env python3
"""Generate project_map.svg: repositories as a metro-style route map.

Run: python3 gen_project_map.py   (reads repos.json next to it)
"""
import html
import json

W = 1200
PAD_L, LINE_X = 28, 210
CHIP_H, CHIP_GAP, ROW_H = 26, 10, 36
CHIP_FONT = 10
CHAR_W = 5.9

COLORS = {
    "WEB": "#3f7fd0",
    "DATA": "#3fa08e",
    "NOTEBOOK": "#e08a4b",
    "PHP": "#9b8fd6",
    "SYSTEMS": "#8fd46a",
    "OTHER": "#93b3c7",
}

GROUPS = [
    ("WEB", "web & interfaces", [
        "rsi-penugasan1-kelompok1", "rsi-penugasan4-kelompok1", "RSI_Learning_Platform_Website",
        "dabd-servingapi-kelompok1", "profil", "instagram", "komikloversV2", "izardaffa", "try",
    ]),
    ("DATA", "data & machine learning", [
        "ml-bisindo-multimodal-keypoint-caption", "dabd-eurointellegence", "bi-olist-crm-dashboard",
        "kbr-notaris-triage-kelompok3", "nlp-rag-kelompok6", "citra-deteksi-titik-garis-dan-tepi-kelompok4",
        "citra-aritlogic-kelompok4", "citra-input-ref-kelompok4", "ipbd-handson1",
        "ipbd-casemethod-kelompok4", "ipbd-tbp-kelompok7", "kda-project-kelompok1",
        "rosbd-finalproject-kelompok4", "project_pkl", "rsi-penugasan2-kelompok1",
    ]),
    ("NOTEBOOK", "campus notebooks", [
        "L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum", "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS",
        "daa-kelompok6-kelasb", "dm-finalproject-kelompok4",
    ]),
    ("PHP", "php & blade", ["imdb-showfy", "komter-project-kelompok5"]),
    ("SYSTEMS", "shell, desktop, infra", [
        "midnight-shell", "caelestian", "cloud-usgs-earthquake", "praktikum-kda01",
        "komter-sinkronisasi-kelompok4",
    ]),
]

SHORT = {
    "ml-bisindo-multimodal-keypoint-caption": "ml-bisindo",
    "citra-deteksi-titik-garis-dan-tepi-kelompok4": "citra-deteksi-titik",
    "kbr-notaris-triage-kelompok3": "kbr-notaris-triage",
    "dabd-eurointellegence": "dabd-eurointellegence",
    "rsi-penugasan1-kelompok1": "rsi-penugasan1",
    "rsi-penugasan2-kelompok1": "rsi-penugasan2",
    "rsi-penugasan4-kelompok1": "rsi-penugasan4",
    "L0224040_AdrianFarrelAzizYatyoga_UTSPraktikum": "L0224040 UTS",
    "L0224040_B_Adrian-Farrel-Aziz-Yatyoga_ResponsiUAS": "L0224040 UAS",
    "ipbd-casemethod-kelompok4": "ipbd-casemethod",
    "rosbd-finalproject-kelompok4": "rosbd-final",
    "dm-finalproject-kelompok4": "dm-final",
    "komter-sinkronisasi-kelompok4": "komter-sinkronisasi",
    "RSI_Learning_Platform_Website": "rsi-learning-platform",
    "dabd-servingapi-kelompok1": "dabd-servingapi",
    "kda-project-kelompok1": "kda-project",
    "komter-project-kelompok5": "komter-project",
    "citra-aritlogic-kelompok4": "citra-aritlogic",
    "citra-input-ref-kelompok4": "citra-input-ref",
    "ipbd-tbp-kelompok7": "ipbd-tbp",
    "bi-olist-crm-dashboard": "bi-olist-crm",
    "cloud-usgs-earthquake": "cloud-usgs-earthquake",
    "daa-kelompok6-kelasb": "daa-kelas-b",
}


def chip(label, x, y, color, dot=True):
    w = len(label) * CHAR_W + 20
    body = f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{CHIP_H}" rx="{CHIP_H / 2}" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".55"/>'
    text = (f'<text x="{x + w / 2:.1f}" y="{y + CHIP_H / 2 + 3.4}" text-anchor="middle" '
            f'font-size="{CHIP_FONT}" fill="#dbe9f2" fill-opacity=".85" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{html.escape(label)}</text>')
    return body + text, w


def build():
    repos = [r["name"] for r in json.load(open("repos.json")) if r["name"] != "iaanne"]
    seen = set()
    rows = []
    y = 96
    for key, subtitle, names in GROUPS:
        color = COLORS[key]
        present = [n for n in names if n in repos]
        seen.update(present)
        x = LINE_X
        line_y = y + CHIP_H / 2
        start_x = LINE_X
        parts = []
        for n in present:
            label = SHORT.get(n, n)
            w = len(label) * CHAR_W + 20
            if x + w > W - PAD_L:
                x = LINE_X
                line_y += ROW_H
            c, w = chip(label, x, line_y - CHIP_H / 2, color)
            parts.append(c)
            x += w + CHIP_GAP
        rows.append({
            "key": key, "subtitle": subtitle, "color": color,
            "y0": y + CHIP_H / 2, "y1": line_y,
            "chips": "".join(parts),
        })
        y = line_y + CHIP_H / 2 + 30

    leftover = [n for n in repos if n not in seen]
    if leftover:
        color = COLORS["OTHER"]
        x, line_y = LINE_X, y + CHIP_H / 2
        parts = []
        for n in leftover:
            label = SHORT.get(n, n)
            w = len(label) * CHAR_W + 20
            if x + w > W - PAD_L:
                x, line_y = LINE_X, line_y + ROW_H
            c, w = chip(label, x, line_y - CHIP_H / 2, color)
            parts.append(c)
            x += w + CHIP_GAP
        rows.append({"key": "OTHER", "subtitle": "other repos", "color": color,
                     "y0": y + CHIP_H / 2, "y1": line_y, "chips": "".join(parts)})
        y = line_y + CHIP_H / 2 + 30

    H = y + 34
    lines = []
    for r in rows:
        c = r["color"]
        # vertical stub from the spine, then the route through its stops
        lines.append(
            f'<path d="M148 {r["y0"] - 26} L148 {r["y0"]} L{LINE_X - 26} {r["y0"]}" '
            f'stroke="{c}" stroke-width="3" fill="none" stroke-opacity=".55" stroke-linecap="round"/>'
        )
        if r["y1"] != r["y0"]:
            lines.append(
                f'<path d="M{LINE_X - 26} {r["y0"]} L{LINE_X - 26} {r["y1"]} L{LINE_X - 12} {r["y1"]}" '
                f'stroke="{c}" stroke-width="3" fill="none" stroke-opacity=".3" stroke-linecap="round"/>'
            )
        else:
            lines.append(f'<line x1="{LINE_X - 26}" y1="{r["y0"]}" x2="{LINE_X - 12}" y2="{r["y0"]}" stroke="{c}" stroke-width="3" stroke-opacity=".55"/>')
        lines.append(f'<circle cx="{LINE_X - 26}" cy="{r["y0"]}" r="4.5" fill="{c}"/>')
        if r["y1"] != r["y0"]:
            lines.append(
                f'<line x1="{LINE_X - 12}" y1="{r["y1"]}" x2="{W - PAD_L}" y2="{r["y1"]}" '
                f'stroke="{c}" stroke-width="2" stroke-opacity=".16" stroke-dasharray="2 6"/>'
            )

    labels = []
    for r in rows:
        labels.append(
            f'<text x="{PAD_L}" y="{r["y0"] - 4}" font-size="12" font-weight="700" letter-spacing="1.4" '
            f'fill="{r["color"]}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{r["key"]}</text>'
        )
        labels.append(
            f'<text x="{PAD_L}" y="{r["y0"] + 14}" font-size="10" fill="#9fb6c6" fill-opacity=".75" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{html.escape(r["subtitle"])}</text>'
        )

    spine_top, spine_bottom = rows[0]["y0"] - 26, rows[-1]["y0"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Project map of @iaanne">
  <title>Project map: every repository grouped by the work it belongs to</title>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .chip {{ transition: none; }}
  </style>
  <rect width="{W}" height="{H}" fill="#0d1117"/>
  <path d="M148 {spine_top} L148 {spine_bottom}" stroke="#30363d" stroke-width="3" fill="none"/>
  <text x="{PAD_L}" y="46" font-size="11" fill="#8b98a5" letter-spacing="2.6">PROJECT MAP — @IAANNE</text>
  <text x="{W - PAD_L}" y="46" text-anchor="end" font-size="11" fill="#8b98a5" letter-spacing="2.6">{len(repos)} REPOSITORIES · 5 ROUTES</text>
  <line x1="{PAD_L}" y1="62" x2="{W - PAD_L}" y2="62" stroke="#30363d"/>
{"".join(lines)}
{"".join(labels)}
{"".join(r["chips"] for r in rows)}
  <text x="{PAD_L}" y="{H - 10}" font-size="10" fill="#8b98a5" fill-opacity=".7" letter-spacing="1.6">EVERY STOP IS A REPOSITORY · ROUTES GROUP THEM BY THE WORK THEY BELONG TO</text>
</svg>
"""


if __name__ == "__main__":
    open("project_map.svg", "w").write(build())
    print("wrote project_map.svg")
