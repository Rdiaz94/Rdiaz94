from common import *

GLYPHS = {
 "R": ["11110","10001","10001","11110","10100","10010","10001"],
 "O": ["01110","10001","10001","10001","10001","10001","01110"],
 "Y": ["10001","10001","01010","00100","00100","00100","00100"],
 "E": ["11111","10000","10000","11110","10000","10000","11111"],
}
WORD = "ROYER"
PX, GAP = 13, 1
W, H = 860, 300
cols = len(WORD) * 5 + (len(WORD) - 1) * GAP
x0 = (W - cols * PX) // 2
y0 = 48

rects = []
col = 0
for ch in WORD:
    for r, row in enumerate(GLYPHS[ch]):
        for c, v in enumerate(row):
            if v == "1":
                x = x0 + (col + c) * PX
                y = y0 + r * PX
                delay = round(0.15 + (col + c) * 0.07 + r * 0.015, 3)
                rects.append(
                    f'<rect x="{x}" y="{y}" width="{PX-2}" height="{PX-2}" rx="2" fill="{GREEN}" opacity="0">'
                    f'<animate attributeName="opacity" values="0;1;0.55;1" keyTimes="0;0.2;0.5;1" dur="0.6s" begin="{delay}s" fill="freeze"/></rect>'
                )
    col += 5 + GAP

lines = [
    ("> Ingeniería de Sistemas Computacionales", GREEN, 2.6),
    ("> Python · Java · SQL Server · Servidores · Virtualización", TEXT, 4.4),
]
text_svg = []
ty = 188
last_ty = ty
for t, color, start in lines:
    n = len(t)
    cw = 9.6
    wpx = n * cw
    cid = f"c{int(start*10)}"
    dur = round(n * 0.035, 2)
    vals = ";".join(str(round(wpx * i / n, 1)) for i in range(n + 1))
    kt = ";".join(str(round(i / n, 4)) for i in range(n + 1))
    text_svg.append(f'''<clipPath id="{cid}"><rect x="{(W-wpx)/2}" y="{ty-18}" width="0" height="26">
<animate attributeName="width" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="{start}s" fill="freeze"/></rect></clipPath>
<text x="{W/2}" y="{ty}" text-anchor="middle" font-family="{FONT}" font-size="16" fill="{color}" clip-path="url(#{cid})" xml:space="preserve">{t}</text>''')
    last_ty = ty
    ty += 34

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity="0.03"/></pattern>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{GREEN_DIM}" stroke-width="1.5"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#scan)"/>
<circle cx="24" cy="22" r="5.5" fill="#ff5f56"/><circle cx="44" cy="22" r="5.5" fill="#ffbd2e"/><circle cx="64" cy="22" r="5.5" fill="#27c93f"/>
<text x="{W-24}" y="26" text-anchor="end" font-family="{FONT}" font-size="12" fill="{MUTED}">PLAYER 1 · READY</text>
<g filter="url(#glow)">{''.join(rects)}</g>
{''.join(text_svg)}
<rect x="{W/2 + 4}" y="{last_ty-16}" width="10" height="20" fill="{GREEN}" opacity="0">
<animate attributeName="opacity" values="0;1;0;1;0;1" dur="1s" begin="7s" repeatCount="indefinite"/>
</rect>
<text x="{W/2}" y="{H-20}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{MUTED}" letter-spacing="3">INSERT COIN TO CONTINUE</text>
</svg>'''
open("../hero.svg", "w", encoding="utf-8").write(svg)
print("hero.svg ok")
