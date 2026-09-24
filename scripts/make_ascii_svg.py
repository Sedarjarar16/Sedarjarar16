from pathlib import Path
from PIL import Image

INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

WIDTH = 100
HEIGHT = 53

RAMP = " .`:-=+*cs#%@"

img = Image.open(INPUT).convert("L")

# Keep the portrait proportions while compensating for terminal character height
img.thumbnail((WIDTH, HEIGHT))

# White canvas
canvas = Image.new("L", (WIDTH, HEIGHT), 255)

x = (WIDTH - img.width) // 2
y = (HEIGHT - img.height) // 2
canvas.paste(img, (x, y))

pixels = canvas.load()

svg_lines = [
    '<svg xmlns="http://www.w3.org/2000/svg"',
    '     viewBox="0 0 1000 530"',
    '     width="1000" height="530"',
    '     role="img">',
    '<rect width="1000" height="530" fill="white"/>',
    '<style>',
    '.ascii {',
    '  font-family: monospace;',
    '  font-size: 10px;',
    '  fill: #666;',
    '}',
    '</style>',
]

for row in range(HEIGHT):
    text = ""

    for col in range(WIDTH):
        brightness = pixels[col, row]

        index = int(
            brightness / 255 * (len(RAMP) - 1)
        )

        text += RAMP[index]

    svg_lines.append(
        f'<text class="ascii" x="0" y="{(row + 1) * 10}">'
        f'{text.replace("&", "&amp;").replace("<", "&lt;")}'
        f'</text>'
    )

svg_lines += [
    """
    <style>
      text {
        opacity: 0;
        animation: reveal 0.04s linear forwards;
      }

      @keyframes reveal {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    </style>
    """,
    "</svg>",
]

OUTPUT.write_text("\n".join(svg_lines), encoding="utf-8")

print(f"Created: {OUTPUT}")
