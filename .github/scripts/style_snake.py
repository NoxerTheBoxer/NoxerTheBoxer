"""Restyle Platane/snk output: flag-colored card background, glowing gold snake, rounded cells.

Usage: python style_snake.py <in.svg> <out.svg> <light|dark>
"""
import re
import sys

THEMES = {
    "light": {"bg1": "#ffffff", "bg2": "#e3f8fc", "edge": "#00abc9"},
    "dark": {"bg1": "#0d1117", "bg2": "#002f38", "edge": "#00abc9"},
}


def main(src, dst, theme):
    t = THEMES[theme]
    svg = open(src, encoding="utf-8").read()
    vb = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', svg)
    if not vb:
        sys.exit(f"no viewBox in {src}")
    x, y, w, h = (float(v) for v in vb.groups())

    defs = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#bg)" stroke="{t['edge']}" stroke-width="2"/>
<rect x="{x + 24}" y="{y + h - 8}" width="{w - 48}" height="5" rx="2.5" fill="#FFC72C"/>"""
    extra_css = ".c{rx:3px;ry:3px}.s{filter:url(#glow)}"

    svg = re.sub(r"(<svg[^>]*>)", r"\1" + defs.replace("\\", "\\\\"), svg, count=1)
    svg = svg.replace("</style>", extra_css + "</style>", 1)
    open(dst, "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    main(*sys.argv[1:4])
