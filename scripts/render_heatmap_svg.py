import json
from pathlib import Path

DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

data = json.loads(DATA.read_text(encoding="utf-8"))
days = data["days"]

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

CELL = 13
GAP = 3
LEFT = 20
TOP = 20

WIDTH = LEFT + 53 * (CELL + GAP) + 20
HEIGHT = TOP + 7 * (CELL + GAP) + 35

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}">',

    f'<rect width="{WIDTH}" height="{HEIGHT}" rx="10" fill="#0d1117"/>',

    '<style>',
    '.cell { animation: appear 0.7s ease forwards; opacity: 0; }',
    '@keyframes appear {',
    '  from { opacity: 0; transform: translateY(-5px); }',
    '  to { opacity: 1; transform: translateY(0); }',
    '}',
    '.text { font-family: monospace; fill: #8b949e; font-size: 11px; }',
    '</style>',
]

# Use the latest 371 days
days = days[-371:]

# Pad to 371 days
while len(days) < 371:
    days.insert(0, {"date": "", "level": 0})

for i, day in enumerate(days):
    week = i // 7
    row = i % 7

    x = LEFT + week * (CELL + GAP)
    y = TOP + row * (CELL + GAP)

    level = max(0, min(5, int(day["level"])))

    delay = (week + row) * 0.015

    svg.append(
        f'<rect class="cell" '
        f'x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" '
        f'rx="3" fill="{COLORS[level]}" '
        f'style="animation-delay:{delay}s">'
        f'<title>{day["date"]}</title>'
        f'</rect>'
    )

svg.append(
    f'<text class="text" x="{LEFT}" y="{HEIGHT - 10}">'
    f'Less</text>'
)

for i, color in enumerate(COLORS):
    x = WIDTH - 115 + i * 16

    svg.append(
        f'<rect x="{x}" y="{HEIGHT - 19}" '
        f'width="11" height="11" rx="2" fill="{color}"/>'
    )

svg.append(
    f'<text class="text" x="{WIDTH - 8}" '
    f'y="{HEIGHT - 10}" text-anchor="end">More</text>'
)

svg.append("</svg>")

OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print(f"Created: {OUTPUT}")
