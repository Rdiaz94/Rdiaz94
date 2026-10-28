"""Turn the public GitHub avatar into a monochrome, self-typing ASCII SVG."""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

import requests
from PIL import Image, ImageEnhance, ImageOps

USERNAME = "Rdiaz94"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "royer-ascii.svg"
RAMP = " .`:-=+*cs#%@"


def main():
    url = f"https://github.com/{USERNAME}.png?size=512"
    response = requests.get(url, headers={"User-Agent": "Rdiaz94-profile-art/1.0"}, timeout=30)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content)).convert("RGB")
    image = ImageOps.fit(image, (72, 40))
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.5)
    pixels = list(image.getdata())

    rows = []
    for y in range(image.height):
        line = []
        for x in range(image.width):
            brightness = pixels[y * image.width + x]
            line.append(RAMP[min(len(RAMP) - 1, brightness * len(RAMP) // 256)])
        rows.append("".join(line).rstrip())

    cell_w, cell_h = 5.2, 5.5
    width, height = 390, 250
    clips, rendered = [], []
    for index, line in enumerate(rows):
        y = 28 + (index + 1) * cell_h
        clip_id = f"line{index}"
        delay = index * 0.045 + 0.01
        clips.append(
            f'<clipPath id="{clip_id}"><rect x="10" y="{y-cell_h+1}" width="0" height="{cell_h+1}">'
            f'<animate attributeName="width" values="0;{len(line)*cell_w:.1f}" dur="0.65s" '
            f'begin="{delay:.3f}s" fill="freeze"/></rect></clipPath>'
        )
        rendered.append(
            f'<text x="10" y="{y:.1f}" clip-path="url(#{clip_id})" '
            f'font-family="monospace" font-size="6.2" xml:space="preserve">{escape(line)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">Animated ASCII rendering of the public GitHub avatar for {USERNAME}</title>
<rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>
<text x="10" y="17" fill="#8b949e" font-family="monospace" font-size="9">royer@github ~ $ whoami</text>
<defs>{''.join(clips)}</defs>
<g fill="#c9d1d9">{''.join(rendered)}</g>
</svg>'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"ASCII SVG generado desde el avatar público: {OUTPUT}")


if __name__ == "__main__":
    main()
