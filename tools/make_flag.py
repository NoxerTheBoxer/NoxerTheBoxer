"""Generate assets/flag.svg: a Bahamas flag waving in the wind.

The flag is cut into thin vertical strips. Each strip bobs up and down a little later
than the one before it (so a wave travels away from the pole), and strips farther
from the pole move more. A shadow overlay on each strip darkens and lightens a quarter
beat out of step, which reads as folds in the fabric.

Run: python tools/make_flag.py
"""
from pathlib import Path

AQUA, GOLD, BLACK = "#00ABC9", "#FFC72C", "#000000"
FLAG_W, FLAG_H = 480, 240          # official 1:2 ratio
STRIPS = 60
PERIOD = 2.6                       # seconds per wave
WAVES_ACROSS = 1.3                 # how many waves fit across the flag
MAX_AMP, MIN_AMP = 11.0, 1.0       # px of vertical movement at the fly end / at the pole
OX, OY = 34, 36                    # flag origin (top-left, at the pole)
W, H = OX + FLAG_W + 20, 340


def main():
    strip_w = FLAG_W / STRIPS
    tip = FLAG_H * 0.866           # equilateral chevron depth
    css, clips, body = [], [], []
    for i in range(STRIPS):
        t = i / (STRIPS - 1)
        amp = MIN_AMP + (MAX_AMP - MIN_AMP) * t
        delay = -PERIOD * WAVES_ACROSS * (1 - t)  # strips farther out lag behind

        css.append(
            f"@keyframes w{i}{{0%,100%{{transform:translateY({-amp:.2f}px)}}50%{{transform:translateY({amp:.2f}px)}}}}"
            f".w{i}{{animation:w{i} {PERIOD}s ease-in-out {delay:.3f}s infinite}}"
            f".h{i}{{animation:shade {PERIOD}s ease-in-out {delay - PERIOD / 4:.3f}s infinite}}"
        )
        x = OX + i * strip_w
        clips.append(f'<clipPath id="c{i}"><rect x="{x:.2f}" y="0" width="{strip_w + 0.6:.2f}" height="{H}"/></clipPath>')
        body.append(
            f'<g class="w{i}"><g clip-path="url(#c{i})"><use href="#flag"/>'
            f'<rect class="h{i}" x="{x:.2f}" y="{OY}" width="{strip_w + 0.6:.2f}" height="{FLAG_H}" fill="#000"/></g></g>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Flag of The Bahamas waving">
<style>
@keyframes shade{{0%,100%{{opacity:0}}50%{{opacity:.24}}}}
{''.join(css)}
@media (prefers-reduced-motion: reduce){{g[class^="w"],rect[class^="h"]{{animation:none}}}}
</style>
<defs>
<g id="flag">
  <rect x="{OX}" y="{OY}" width="{FLAG_W}" height="{FLAG_H / 3}" fill="{AQUA}"/>
  <rect x="{OX}" y="{OY + FLAG_H / 3}" width="{FLAG_W}" height="{FLAG_H / 3}" fill="{GOLD}"/>
  <rect x="{OX}" y="{OY + 2 * FLAG_H / 3}" width="{FLAG_W}" height="{FLAG_H / 3}" fill="{AQUA}"/>
  <path d="M{OX} {OY} L{OX + tip:.1f} {OY + FLAG_H / 2} L{OX} {OY + FLAG_H} Z" fill="{BLACK}"/>
</g>
{''.join(clips)}
<linearGradient id="pole" x1="0" x2="1"><stop offset="0" stop-color="#8a8f98"/><stop offset=".45" stop-color="#e6e9ee"/><stop offset="1" stop-color="#6b7079"/></linearGradient>
</defs>
<rect x="{OX - 10}" y="22" width="8" height="{H - 30}" rx="3" fill="url(#pole)"/>
<circle cx="{OX - 6}" cy="20" r="8" fill="{GOLD}"/>
{''.join(body)}
</svg>
"""
    out = Path(__file__).resolve().parent.parent / "assets" / "flag.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out} ({len(svg) // 1024} KB)")


if __name__ == "__main__":
    main()
