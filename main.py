#!/usr/bin/env python3
"""Deterministic news summary image for make.fun bounty news-image-20261120.

Generates an SVG summarizing the world news of 20 November 2026 and renders it
to PNG. Pure standard library: writes the SVG always, and the PNG when
cairosvg is importable (the committed PNG is copied to the output directory
otherwise, so the run always produces both files).
"""
import os
import shutil
import sys

W, H = 1600, 1000
HEADER = 140
BG = "#0d1321"
PANEL = "#16213a"
INK = "#e8ecf7"
MUTED = "#9aa7c7"
GOLD = "#f0b429"
ACCENTS = {"diplomacy": "#5b8cff", "justice": "#e4572e", "economy": "#2ec4b6",
           "conflict": "#ff6b6b", "climate": "#7bc96f", "society": "#c77dff"}

NEWS = [
    ("diplomacy", "TRILATERAL SUMMIT IN SHENZHEN",
     "Trump, Xi and Putin held the first-ever US-China-Russia "
     "three-way summit on the sidelines of APEC, issuing a joint "
     "\u201cpeace declaration\u201d: nuclear-risk dialogue, UN reform "
     "and pledges to expand fuel supplies."),
    ("justice", "ICJ: MYANMAR COMMITTED GENOCIDE",
     "The International Court of Justice found Myanmar responsible "
     "for genocide against the Rohingya \u2014 the first such ruling "
     "against a state in the court's history."),
    ("economy", "ANTHROPIC IPO \u2014 LARGEST EVER",
     "Anthropic's debut valued it at $1.5T, topping SpaceX's record; "
     "shares spiked above $111, then an AI-bubble sell-off dragged "
     "markets \u2014 Japan's Nikkei fell 4.8%."),
    ("diplomacy", "UK\u2013EU RESET SUMMIT IN BRUSSELS",
     "A decade after Brexit, PM Andy Burnham met Costa and von der "
     "Leyen; deals on trade, food standards and youth mobility aim "
     "to rebuild ties."),
    ("conflict", "HOUTHI MISSILE HITS RIYADH TOWER",
     "A missile struck a skyscraper in Riyadh's financial district; "
     "Saudi Arabia intercepted more drones and carried out air "
     "strikes across Houthi-held Yemen."),
    ("conflict", "11-NATION DRILL IN POLAND",
     "Led by France and the UK, the 'Coalition of the Willing' "
     "trained in southeast Poland for a potential postwar Ukraine "
     "mission \u2014 anti-drone and trench warfare."),
    ("society", "ITALY GENERAL STRIKE",
     "Tens of thousands joined the CGIL's nationwide strike over "
     "wages and public services; Amnesty later flagged police "
     "excesses during protests."),
    ("climate", "COP31 TALKS STALL",
     "Climate diplomacy stalled in Turkey as the draft agreement "
     "left fossil fuels unmentioned, drawing outrage from activists "
     "and delegations."),
    ("society", "GOOD NEWS, TWO KINDS",
     "Kenya discharged its last Ebola patient 37 days after the "
     "first case \u2014 and Denmark approved a security deal keeping "
     "Greenland Danish while the US expands its Arctic presence."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, limit):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= limit:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build_svg():
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif">')
    p.append(f'<defs><linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="#1a2b5e"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    # header
    p.append(f'<rect width="{W}" height="{HEADER}" fill="url(#hdr)"/>')
    p.append(f'<rect y="{HEADER}" width="{W}" height="4" fill="{GOLD}"/>')
    p.append(f'<text x="60" y="62" fill="{GOLD}" font-size="22" letter-spacing="6">'
             'WORLD BRIEFING</text>')
    p.append(f'<text x="60" y="112" fill="{INK}" font-size="44" font-weight="bold">'
             'The World in One Frame \u2014 20 November 2026</text>')
    p.append(f'<text x="{W-60}" y="68" fill="{MUTED}" font-size="18" text-anchor="end">'
             'A daily digest \u00b7 9 stories \u00b7 sources: Reuters, AP, CS Monitor,'
             ' Euronews</text>')
    # grid: 2 columns x 5 rows
    gx, gy, gw, gh, gap = 60, 182, 730, 140, 12
    for i, (cat, head, body) in enumerate(NEWS):
        col, row = i % 2, i // 2
        x = gx + col * (gw + gap)
        y = gy + row * (gh + gap)
        ac = ACCENTS[cat]
        p.append(f'<rect x="{x}" y="{y}" width="{gw}" height="{gh}" rx="10" fill="{PANEL}"/>')
        p.append(f'<rect x="{x}" y="{y}" width="7" height="{gh}" rx="3" fill="{ac}"/>')
        p.append(f'<text x="{x+30}" y="{y+36}" fill="{ac}" font-size="16" '
                 f'letter-spacing="3">{esc(cat.upper())}</text>')
        p.append(f'<text x="{x+30}" y="{y+68}" fill="{INK}" font-size="25" '
                 f'font-weight="bold">{esc(head)}</text>')
        for j, ln in enumerate(wrap(body, 78)[:3]):
            p.append(f'<text x="{x+30}" y="{y+94+j*19}" fill="{MUTED}" '
                     f'font-size="16">{esc(ln)}</text>')
    # footer
    fy = gy + 5 * (gh + gap)
    p.append(f'<text x="{gx}" y="{fy+28}" fill="{GOLD}" font-size="20" letter-spacing="2">'
             'MOOD OF THE DAY: UNEASY \u2014 DIPLOMACY OPENS DOORS, MARKETS HOLD'
             ' THEIR BREATH</text>')
    p.append(f'<text x="{W-60}" y="{fy+52}" fill="{MUTED}" font-size="16" '
             'text-anchor="end">Compiled 2026-11-20 \u00b7 make.fun bounty'
             ' news-image-20261120</text>')
    p.append('</svg>')
    return "\n".join(p)


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out, exist_ok=True)
    except OSError:
        out = "."
    svg = build_svg()
    svg_path = os.path.join(out, "world-news-2026-11-20.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    png_path = os.path.join(out, "world-news-2026-11-20.png")
    rendered = False
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                         write_to=png_path, output_width=W, output_height=H)
        rendered = True
    except Exception:
        committed = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "world-news-2026-11-20.png")
        if os.path.exists(committed) and os.path.getmtime(committed):
            shutil.copyfile(committed, png_path)
    print(f"written: {svg_path} ({os.path.getsize(svg_path)} bytes)")
    if os.path.exists(png_path):
        print(f"written: {png_path} ({os.path.getsize(png_path)} bytes)"
              f" [{'rendered' if rendered else 'copied'}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
