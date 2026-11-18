import json, datetime
from common import *
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
try:
    data = json.load(open("../data/contributions.json"))
except Exception:
    data = {"total": 0, "current_streak": 0, "longest_streak": 0, "days": []}
days = data["days"]
if not days:
    start = datetime.date.today() - datetime.timedelta(days=370)
    start -= datetime.timedelta(days=(start.weekday() + 1) % 7)
    days = [{"date": str(start + datetime.timedelta(days=i)), "level": 0, "count": 0} for i in range(371)]
CELL, STEP, LEFT, TOP = 12, 15, 40, 64
first = datetime.date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7
cells, labels, last = [], [], -1
meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
for i, d in enumerate(days):
    idx = i + offset
    wk, dow = idx // 7, idx % 7
    x, y = LEFT + wk * STEP, TOP + dow * STEP
    delay = round((wk + dow) * 0.03, 3)
    cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[min(d["level"],4)]}" opacity="0">'
                 f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay}s" fill="freeze"/>'
                 f'<title>{d["date"]}: {d["count"]}</title></rect>')
    dt = datetime.date.fromisoformat(d["date"])
    if dt.month != last and dt.day <= 7:
        labels.append(f'<text x="{x}" y="{TOP-10}" font-family="{FONT}" font-size="10" fill="{MUTED}">{meses[dt.month-1]}</text>')
        last = dt.month
W, H = 860, TOP + 7 * STEP + 56
legend = "".join(f'<rect x="{W-170+i*17}" y="{H-30}" width="12" height="12" rx="3" fill="{c}"/>' for i, c in enumerate(PALETTE))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{GREEN_DIM}" stroke-width="1.5"/>
<text x="24" y="30" font-family="{FONT}" font-size="14" fill="{GREEN}">royer@github ~ $ ./contribuciones.sh</text>
{''.join(labels)}
{''.join(cells)}
<text x="24" y="{H-20}" font-family="{FONT}" font-size="12" fill="{TEXT}">{data["total"]} contribuciones en el último año · racha actual {data["current_streak"]} · mejor racha {data["longest_streak"]}</text>
<text x="{W-182}" y="{H-20}" text-anchor="end" font-family="{FONT}" font-size="10" fill="{MUTED}">Menos</text>
{legend}
<text x="{W-80}" y="{H-20}" font-family="{FONT}" font-size="10" fill="{MUTED}">Más</text>
</svg>'''
open("../contrib-heatmap.svg", "w", encoding="utf-8").write(svg)
print("contrib-heatmap.svg ok")
