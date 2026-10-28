"""Fetch public GitHub contribution days without a personal access token."""
import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv("GITHUB_USERNAME", "Rdiaz94")
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "contributions.json"
URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    response = requests.get(URL, headers={"User-Agent": "Rdiaz94-profile-art/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("td[data-date][data-level]"):
        try:
            day = date.fromisoformat(cell["data-date"])
            level = max(0, min(4, int(cell["data-level"])))
        except (KeyError, ValueError, TypeError):
            continue

        raw_count = cell.get("data-count")
        if raw_count is None:
            tooltip = cell.get("aria-label", "")
            match = re.search(r"(\d[\d,]*) contribution", tooltip, re.IGNORECASE)
            raw_count = match.group(1).replace(",", "") if match else "0"
        try:
            count = int(str(raw_count).replace(",", ""))
        except ValueError:
            count = 0
        days.append({"date": day.isoformat(), "level": level, "count": max(0, count)})

    if not days:
        raise RuntimeError("No se encontraron celdas de contribución; no se escribirán datos vacíos.")
    days.sort(key=lambda item: item["date"])
    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Guardadas {len(days)} fechas de contribución en {OUTPUT}")


if __name__ == "__main__":
    main()
