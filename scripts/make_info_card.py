import os
from common import *
STATIC = os.environ.get("STATIC") == "1"
W, H = 490, 330
rows = [
 ("OS",        "Ingeniería de Sistemas Computacionales", GREEN),
 ("Rol",       "Estudiante · Dev y SysAdmin en formación", GREEN),
 ("Código",    "Python · Java · Spring Boot · Angular", CYAN),
 ("Datos",     "SQL Server · Big Data", CYAN),
 ("Infra",     "Windows Server 2025 · CentOS · Kali", AMBER),
 ("Servicios", "Zimbra · Samba · Virtualización", AMBER),
 ("IDE",       "VS Code · Visual Studio", GREEN),
 ("Estudio",   "Big Data · Seguridad · Arquitectura", GREEN),
 ("Estado",    "● online · construyendo cosas", GREEN),
]
out = []
y = 82
for i, (k, v, col) in enumerate(rows):
    d = 0.4 + i * 0.28
    anim = "" if STATIC else (
        f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{d}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" dur="0.35s" begin="{d}s" fill="freeze"/>')
    op = "1" if STATIC else "0"
    out.append(f'<g opacity="{op}">{anim}'
               f'<text x="24" y="{y}" font-family="{FONT}" font-size="13" font-weight="bold" fill="{col}">{k}</text>'
               f'<text x="112" y="{y}" font-family="{FONT}" font-size="13" fill="{TEXT}">{v}</text></g>')
    y += 24
pal = "".join(f'<rect x="{24+i*26}" y="{y+4}" width="22" height="14" rx="2" fill="{c}"/>'
              for i, c in enumerate(["#ff5f56", AMBER, GREEN, CYAN, "#bc8cff", TEXT, MUTED]))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{GREEN_DIM}" stroke-width="1.5"/>
<rect x="1" y="1" width="{W-2}" height="36" rx="13" fill="#161b22"/><rect x="1" y="22" width="{W-2}" height="15" fill="#161b22"/>
<circle cx="22" cy="19" r="5" fill="#ff5f56"/><circle cx="40" cy="19" r="5" fill="#ffbd2e"/><circle cx="58" cy="19" r="5" fill="#27c93f"/>
<text x="{W/2}" y="23" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{MUTED}">royer@sistemas: ~</text>
<text x="24" y="60" font-family="{FONT}" font-size="13" fill="{GREEN}">$ neofetch --royer</text>
{''.join(out)}
{pal}
</svg>'''
open("../info-card.svg", "w", encoding="utf-8").write(svg)
print("info-card.svg ok")
