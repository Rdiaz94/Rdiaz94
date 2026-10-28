"""Generate a neofetch-style SVG profile card."""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "info-card.svg"
ROWS = [
    ("name", "Royer Diaz Montoya"),
    ("role", "Systems Engineering student"),
    ("location", "Cajamarca, Peru"),
    ("focus", "Software / Data / Systems"),
    ("stack", "Python / Java / SQL Server"),
    ("learning", "Linux / Cloud / AI / Security"),
    ("goal", "Useful, maintainable software"),
]


def main():
    row_svg = []
    for index, (key, value) in enumerate(ROWS):
        y = 93 + index * 29
        delay = 0.12 + index * 0.15
        row_svg.append(
            f'<g opacity="0"><text x="24" y="{y}" fill="#79c0ff" font-size="12">{escape(key)}</text>'
            f'<text x="115" y="{y}" fill="#c9d1d9" font-size="12">{escape(value)}</text>'
            f'<animate attributeName="opacity" values="0;1" dur="0.25s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</g>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="315" viewBox="0 0 500 315" role="img" aria-labelledby="title">
<title id="title">Tarjeta de perfil de Royer Diaz</title>
<rect width="500" height="315" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M10 0H490Q500 0 500 10V42H0V10Q0 0 10 0Z" fill="#161b22"/>
<circle cx="20" cy="21" r="5" fill="#ff7b72"/><circle cx="38" cy="21" r="5" fill="#d29922"/><circle cx="56" cy="21" r="5" fill="#3fb950"/>
<text x="78" y="25" fill="#8b949e" font-size="12" font-family="monospace">royer@github — neofetch</text>
<text x="24" y="67" fill="#3fb950" font-size="14" font-family="monospace">profile.json</text>
{''.join(row_svg)}
<text x="24" y="294" fill="#8b949e" font-size="10">PROFILE DETAILS · EDIT scripts/make_info_card.py</text>
</svg>'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"SVG generado en {OUTPUT}")


if __name__ == "__main__":
    main()
