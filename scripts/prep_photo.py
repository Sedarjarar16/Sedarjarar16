from pathlib import Path
from rembg import remove
from PIL import Image
import cv2
import numpy as np

INPUT = Path("source.jpg")
OUTPUT = Path("source-prepped.png")

# Remove the background
input_image = Image.open(INPUT).convert("RGBA")
no_bg = remove(input_image)

# White background
background = Image.new("RGBA", no_bg.size, "white")
composite = Image.alpha_composite(background, no_bg).convert("RGB")

# Convert to OpenCV
img = np.array(composite)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Improve local contrast
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

l = clahe.apply(l)

enhanced = cv2.merge((l, a, b))
enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

# Save
cv2.imwrite(str(OUTPUT), enhanced)

print(f"Created: {OUTPUT}")
