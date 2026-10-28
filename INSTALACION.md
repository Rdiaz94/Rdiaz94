# Perfil animado de Rdiaz94

Implementación basada en la arquitectura del artículo:
https://www.avivashishta.com/blog/build-animated-github-profile-readme

## Incluye
- README con composición tipo terminal y banner existente.
- Tarjeta SVG estilo neofetch, animada línea por línea.
- Calendario SVG basado en contribuciones públicas reales.
- GitHub Actions para actualizar el calendario diariamente.
- Panel ASCII provisional, pendiente de una fotografía para personalizarlo.

## Comprobación
1. Abre la pestaña **Actions** del repositorio.
2. Ejecuta manualmente **Refresh animated profile art**.
3. Comprueba que se generen/actualicen `data/contributions.json` y `assets/contrib-heatmap.svg`.
4. Revisa que los SVG se carguen en el README.
5. El parser depende del HTML público de GitHub; si cambia el formato, el job falla en vez de guardar datos vacíos.
6. No se necesita un Personal Access Token para consultar el calendario público.
