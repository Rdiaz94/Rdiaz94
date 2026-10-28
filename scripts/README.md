# Scripts del perfil animado

- `fetch_contributions.py`: obtiene el calendario público de contribuciones de GitHub sin token.
- `render_heatmap_svg.py`: genera un SVG animado desde los datos descargados.
- `make_info_card.py`: genera una tarjeta terminal SVG animada.

Para probar localmente:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/make_info_card.py
```

El retrato ASCII está provisional hasta que se proporcione una fotografía y se añada el generador dedicado.