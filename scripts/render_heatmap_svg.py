"""Render a self-contained animated SVG heatmap from contribution JSON."""
import json
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "assets" / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main():
    if not DATA.exists():
        raise FileNotFoundError("Falta data/contributions.json; ejecuta fetch_contributions.py.")
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_date = {item["date"]: item for item in payload.get("days", [])}
    if not by_date:
        raise RuntimeError("El JSON no contiene días de contribución.")

    today = date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    days = [start + timedelta(days=i) for i in range((today - start).days + 1)]
    cell, gap, left, top = 11, 4, 42, 35
    cols = (len(days) + 6) // 7
    width, height = left + cols * (cell + gap) + 16, 145
    rects, months = [], []
    previous_month = None

    for idx, day in enumerate(days):
        if day > today:
            continue
        col, row = idx // 7, idx % 7
        x, y = left + col * (cell + gap), top + row * (cell + gap)
        item = by_date.get(day.isoformat(), {"level": 0, "count": 0})
        level = max(0, min(4, int(item.get("level", 0))))
        count = int(item.get("count", 0))
        delay = min(1.8, col * 0.012 + row * 0.035)
        rects.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
            f'fill="{PALETTE[level]}" opacity="0"><title>{count} contributions on {day.isoformat()}</title>'
            f'<animate attributeName="opacity" values="0;1" dur="0.28s" '
            f'begin="{delay:.3f}s" fill="freeze"/></rect>'
        )
        if day.month != previous_month and day.day <= 7:
            months.append(f'<text x="{x}" y="19" fill="#8b949e" font-size="10">{day.strftime("%b")}</text>')
            previous_month = day.month

    cutoff = (today - timedelta(days=364)).isoformat()
    total = sum(int(item.get("count", 0)) for key, item in by_date.items()
                if cutoff <= key <= today.isoformat())
    legend_x = width - 160
    legend = "".join(
        f'<rect x="{legend_x + i*15}" y="{height-19}" width="10" height="10" rx="2" fill="{color}"/>'
        for i, color in enumerate(PALETTE)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Calendario de contribuciones de GitHub</title>
<desc id="desc">Datos públicos de contribuciones de {escape(payload.get("username", "Rdiaz94"))}.</desc>
<rect width="100%" height="100%" rx="8" fill="#0d1117"/>
<text x="14" y="19" fill="#c9d1d9" font-size="11">{escape(payload.get("username", "Rdiaz94"))} · {total:,} contribuciones en el último año</text>
{''.join(months)}
{''.join(rects)}
<text x="14" y="{height-11}" fill="#8b949e" font-size="10">Menos</text>
{legend}
<text x="{legend_x+82}" y="{height-11}" fill="#8b949e" font-size="10">Más</text>
</svg>'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"SVG generado en {OUTPUT}")


if __name__ == "__main__":
    main()
