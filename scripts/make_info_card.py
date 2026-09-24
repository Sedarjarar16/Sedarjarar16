from pathlib import Path

OUTPUT = Path("info-card.svg")

rows = [
    ("Now", "Computer Engineering Student"),
    ("Prev", "Digital Systems • AI • Web"),
    ("Stack", "Python • C++ • Verilog • Git"),
    ("Highlights", "RISC-V • AI • Energy Systems"),
]

WIDTH = 490
HEIGHT = 230

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
    '<rect width="490" height="230" rx="12" fill="#0d1117"/>',
    '<rect x="1" y="1" width="488" height="228" rx="11" fill="none" stroke="#30363d"/>',

    # Terminal title bar
    '<circle cx="20" cy="20" r="5" fill="#ff5f56"/>',
    '<circle cx="38" cy="20" r="5" fill="#ffbd2e"/>',
    '<circle cx="56" cy="20" r="5" fill="#27c93f"/>',

    '<text x="245" y="24" text-anchor="middle" '
    'font-family="monospace" font-size="11" fill="#8b949e">'
    'sedar@github ~</text>',

    '<style>',
    '.label { font-family: monospace; font-size: 14px; font-weight: bold; fill: #58a6ff; }',
    '.value { font-family: monospace; font-size: 13px; fill: #c9d1d9; }',
    '.prompt { font-family: monospace; font-size: 13px; fill: #7ee787; }',
    '.row { opacity: 0; animation: appear 0.5s ease forwards; }',
    '@keyframes appear { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: translateX(0); } }',
    '</style>',
]

start_y = 65

for i, (label, value) in enumerate(rows):
    y = start_y + i * 38
    delay = i * 0.25

    svg.append(
        f'<g class="row" style="animation-delay:{delay}s">'
        f'<text class="prompt" x="25" y="{y}">$</text>'
        f'<text class="label" x="45" y="{y}">{label}:</text>'
        f'<text class="value" x="125" y="{y}">{value}</text>'
        f'</g>'
    )

svg.append("</svg>")

OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print(f"Created: {OUTPUT}")
