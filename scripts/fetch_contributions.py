import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Sedarjarar16"
URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for rect in soup.select("td.ContributionCalendar-day"):
    date = rect.get("data-date")
    level = rect.get("data-level")

    if date and level:
        days.append({
            "date": date,
            "level": int(level)
        })

# Fallback for GitHub's newer markup
if not days:
    for element in soup.select("[data-date][data-level]"):
        date = element.get("data-date")
        level = element.get("data-level")

        if date and level:
            days.append({
                "date": date,
                "level": int(level)
            })

# Remove duplicates
unique = {}

for day in days:
    unique[day["date"]] = day["level"]

days = [
    {"date": date, "level": level}
    for date, level in sorted(unique.items())
]

# Calculate streaks
current_streak = 0
longest_streak = 0
running_streak = 0

for day in days:
    if day["level"] > 0:
        running_streak += 1
        longest_streak = max(longest_streak, running_streak)
    else:
        running_streak = 0

for day in reversed(days):
    if day["level"] > 0:
        current_streak += 1
    else:
        break

best_day = None

if days:
    best = max(days, key=lambda x: x["level"])
    best_day = best

data = {
    "username": USERNAME,
    "days": days,
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "best_day": best_day,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(f"Fetched {len(days)} contribution days")
print(f"Created: {OUTPUT}")
