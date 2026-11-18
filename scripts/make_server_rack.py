from common import *
W, H = 370, 330
units = [("WIN-SRV-2025", GREEN), ("CENTOS · ZIMBRA", AMBER), ("KALI · LAB", CYAN)]
out = []
y = 56
for i, (name, col) in enumerate(units):
    out.append(f'<rect x="24" y="{y}" width="322" height="64" rx="6" fill="#161b22" stroke="{GREEN_DIM}" stroke-width="1"/>')
    for s in range(5):
        out.append(f'<rect x="40" y="{y+10+s*9}" width="150" height="3" rx="1" fill="#0d1117"/>')
    out.append(f'<text x="206" y="{y+24}" font-family="{FONT}" font-size="11" fill="{col}">{name}</text>')
    out.append(f'<text x="206" y="{y+40}" font-family="{FONT}" font-size="10" fill="{MUTED}">VM · online</text>')
    for l in range(4):
        d = round(0.3 + i * 0.35 + l * 0.2, 2)
        c = col if l < 3 else "#ff5f56"
        out.append(f'<circle cx="{206+l*18}" cy="{y+52}" r="4" fill="{c}"><animate attributeName="opacity" values="1;0.15;1" dur="{round(1.1+l*0.3,1)}s" begin="{d}s" repeatCount="indefinite"/></circle>')
    y += 82
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{GREEN_DIM}" stroke-width="1.5"/>
<text x="24" y="34" font-family="{FONT}" font-size="13" fill="{GREEN}">$ ./homelab.sh --status</text>
{''.join(out)}
</svg>'''
open("../server-rack.svg", "w", encoding="utf-8").write(svg)
print("server-rack.svg ok")
