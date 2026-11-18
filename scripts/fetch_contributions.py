import json, re, requests
from bs4 import BeautifulSoup
USER = "Rdiaz94"
html = requests.get(f"https://github.com/users/{USER}/contributions",
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")
tips = {}
for t in soup.find_all("tool-tip"):
    m = re.match(r"(\d+|No) contribution", t.get_text(strip=True))
    if m and t.get("for"):
        tips[t["for"]] = 0 if m.group(1) == "No" else int(m.group(1))
days = [{"date": td["data-date"], "level": int(td.get("data-level", 0)), "count": tips.get(td.get("id"), 0)}
        for td in soup.select("td[data-date]")]
days.sort(key=lambda d: d["date"])
total = sum(d["count"] for d in days)
longest = run = 0
for d in days:
    run = run + 1 if d["count"] > 0 else 0
    longest = max(longest, run)
cur = 0
for i, d in enumerate(reversed(days)):
    if d["count"] > 0: cur += 1
    elif i == 0: continue
    else: break
json.dump({"user": USER, "total": total, "current_streak": cur, "longest_streak": longest, "days": days},
          open("../data/contributions.json", "w"))
print(f"{len(days)} días, {total} contribuciones")
