"""
Room 10 Floor Texture — "The Candy King" Dark Throne Room Floor

Nearly black polished obsidian floor with:
- Subtle tile grid (barely visible)
- Faint reflective polish sheen
- Warm golden spotlight pool near center
- Barely visible radial medallion pattern
- Scattered bright candy dots (fallen from the king's crown)
- Fully tileable/seamless
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 42

rng = np.random.default_rng(SEED)

# --- Palette ---
BASE = np.array([10, 8, 15], dtype=np.float64)
GRID_COLOR = np.array([14, 12, 18], dtype=np.float64)
POLISH = np.array([18, 15, 22], dtype=np.float64)
SPOTLIGHT = np.array([40, 30, 15], dtype=np.float64)

CANDY_COLORS = [
    (220, 40, 40),    # red
    (240, 200, 30),   # yellow
    (40, 200, 60),    # green
    (50, 80, 220),    # blue
    (180, 50, 200),   # purple
    (240, 130, 30),   # orange
    (230, 80, 150),   # pink
]

# --- Base canvas ---
pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
pixels[:] = BASE

# --- Subtle noise for stone variation ---
noise = rng.normal(0, 1.5, (SIZE, SIZE))
for c in range(3):
    pixels[:, :, c] += noise

# --- Tile grid (barely visible, 32px tiles) ---
TILE = 32
for y in range(SIZE):
    for x in range(SIZE):
        # Grid lines at tile boundaries
        gx = x % TILE
        gy = y % TILE
        if gx == 0 or gy == 0:
            t = 0.3  # very subtle
            pixels[y, x] = pixels[y, x] * (1 - t) + GRID_COLOR * t

# --- Radial medallion pattern (barely visible, tileable via wrapping) ---
# Create a faint circular pattern centered at 128,128
cx, cy = SIZE // 2, SIZE // 2
for y in range(SIZE):
    for x in range(SIZE):
        # Use wrapped distance for tileability — take min distance across tiled copies
        dx = min(abs(x - cx), SIZE - abs(x - cx))
        dy = min(abs(y - cy), SIZE - abs(y - cy))
        dist = np.sqrt(dx * dx + dy * dy)

        # Concentric rings
        ring_val = np.sin(dist * 0.12) * 0.5 + 0.5
        # Radial lines (8-fold symmetry)
        angle = np.arctan2(dy, dx)
        radial_val = (np.sin(angle * 8) * 0.5 + 0.5)

        # Combine — very faint
        medallion = ring_val * 0.4 + radial_val * 0.6
        intensity = medallion * 2.0  # very subtle brightness bump

        # Fade out toward edges (using wrapped dist)
        fade = max(0, 1.0 - dist / (SIZE * 0.45))
        fade = fade ** 2

        pixels[y, x] += intensity * fade

# --- Polish sheen (subtle lighter patches) ---
# Use low-frequency noise for broad reflective areas
sheen_scale = 64
sheen_noise = rng.normal(0, 1, (SIZE // sheen_scale + 2, SIZE // sheen_scale + 2))

for y in range(SIZE):
    for x in range(SIZE):
        # Bilinear sample from low-res noise
        fx = (x / sheen_scale) % (SIZE // sheen_scale)
        fy = (y / sheen_scale) % (SIZE // sheen_scale)
        ix, iy = int(fx), int(fy)
        fx -= ix
        fy -= iy
        ix2 = (ix + 1) % (SIZE // sheen_scale)
        iy2 = (iy + 1) % (SIZE // sheen_scale)

        val = (sheen_noise[iy, ix] * (1 - fx) * (1 - fy) +
               sheen_noise[iy, ix2] * fx * (1 - fy) +
               sheen_noise[iy2, ix] * (1 - fx) * fy +
               sheen_noise[iy2, ix2] * fx * fy)

        if val > 0.3:
            t = (val - 0.3) * 0.15  # very subtle
            pixels[y, x] = pixels[y, x] * (1 - t) + POLISH * t

# --- Warm spotlight pool (golden glow near center, tileable) ---
for y in range(SIZE):
    for x in range(SIZE):
        dx = min(abs(x - cx), SIZE - abs(x - cx))
        dy = min(abs(y - cy), SIZE - abs(y - cy))
        dist = np.sqrt(dx * dx + dy * dy)

        # Gaussian-ish falloff
        radius = SIZE * 0.3
        if dist < radius:
            intensity = np.exp(-dist * dist / (2 * (radius * 0.35) ** 2))
            # Add warm golden light
            pixels[y, x] += SPOTLIGHT * intensity * 0.6

# --- Candy scatter (15-25 bright tiny dots, tileable) ---
num_candy = rng.integers(18, 26)
candy_positions = []

for i in range(num_candy):
    cx_c = rng.integers(0, SIZE)
    cy_c = rng.integers(0, SIZE)
    color = CANDY_COLORS[rng.integers(0, len(CANDY_COLORS))]
    size = rng.integers(1, 4)  # 1-3 px

    candy_positions.append((cx_c, cy_c, color, size))

    if size == 1:
        pixels[cy_c % SIZE, cx_c % SIZE] = color
    elif size == 2:
        for dy in range(2):
            for dx in range(2):
                pixels[(cy_c + dy) % SIZE, (cx_c + dx) % SIZE] = color
    else:
        # 3px: cross shape for a more candy-like look
        pixels[cy_c % SIZE, cx_c % SIZE] = color
        pixels[(cy_c - 1) % SIZE, cx_c % SIZE] = color
        pixels[(cy_c + 1) % SIZE, cx_c % SIZE] = color
        pixels[cy_c % SIZE, (cx_c - 1) % SIZE] = color
        pixels[cy_c % SIZE, (cx_c + 1) % SIZE] = color
        # Slightly darker center for depth
        pixels[cy_c % SIZE, cx_c % SIZE] = tuple(int(c * 0.85) for c in color)

# --- Add tiny specular highlights on some candy ---
for cx_c, cy_c, color, size in candy_positions:
    if rng.random() > 0.4:
        # White-ish highlight pixel offset by 1
        hx = (cx_c + (1 if size > 1 else 0)) % SIZE
        hy = (cy_c - (1 if size > 1 else 0)) % SIZE
        highlight = tuple(min(255, int(c * 1.4 + 60)) for c in color)
        pixels[hy, hx] = highlight

# --- Final pixel-art dithering pass (subtle) ---
# Add sparse single-pixel noise for texture
dither_mask = rng.random((SIZE, SIZE)) > 0.97
dither_vals = rng.choice([-2, -1, 1, 2], size=(SIZE, SIZE))
for c in range(3):
    pixels[:, :, c] += dither_mask * dither_vals

# --- Clamp and export ---
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

img = Image.fromarray(pixels, 'RGB')
img.save('../../docs/assets/rooms/room10_floor.png')
print(f"Saved output.png ({img.size[0]}x{img.size[1]})")
