"""
Generate a tileable retail store floor texture (256x256).
Light gray polished concrete / commercial tile look.
"""

import numpy as np
from PIL import Image
import os

SEED = 42
SIZE = 256
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.png")

rng = np.random.default_rng(SEED)

# --- Base color with subtle warm gray ---
base_r, base_g, base_b = 195, 192, 188

# Start with base color
pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
pixels[:, :, 0] = base_r
pixels[:, :, 1] = base_g
pixels[:, :, 2] = base_b

# --- Tileable fine speckle noise ---
# Use a simple approach: generate noise that tiles by mirroring isn't needed
# if we just use uniform random per-pixel (it tiles naturally since there's no structure)
speckle = rng.uniform(-8, 8, (SIZE, SIZE))
for c in range(3):
    pixels[:, :, c] += speckle

# --- Tileable low-frequency variation (subtle mottling) ---
# Create tileable smooth variation using tiled frequency-domain approach
# Use a few octaves of seamlessly-tiling cosine waves
for _ in range(6):
    freq_x = rng.integers(1, 5) * 1  # integer freqs tile perfectly over SIZE
    freq_y = rng.integers(1, 5) * 1
    phase_x = rng.uniform(0, 2 * np.pi)
    phase_y = rng.uniform(0, 2 * np.pi)
    amplitude = rng.uniform(1.5, 4.0)

    x = np.arange(SIZE)
    y = np.arange(SIZE)
    xx, yy = np.meshgrid(x, y)

    wave = amplitude * np.cos(2 * np.pi * freq_x * xx / SIZE + phase_x) * \
           np.cos(2 * np.pi * freq_y * yy / SIZE + phase_y)

    for c in range(3):
        pixels[:, :, c] += wave

# --- Grout lines (tile grid) ---
# 2-3 large tiles visible means tile size ~85-128px. Use 128 (divides 256 evenly).
TILE_SIZE = 128
GROUT_WIDTH = 2
grout_r, grout_g, grout_b = 175, 172, 168

for axis_pos in range(SIZE):
    in_grout = (axis_pos % TILE_SIZE) < GROUT_WIDTH

    if in_grout:
        # Horizontal grout lines
        pixels[axis_pos, :, 0] = grout_r
        pixels[axis_pos, :, 1] = grout_g
        pixels[axis_pos, :, 2] = grout_b
        # Vertical grout lines
        pixels[:, axis_pos, 0] = grout_r
        pixels[:, axis_pos, 1] = grout_g
        pixels[:, axis_pos, 2] = grout_b

# Add slight noise to grout lines so they're not perfectly flat
for axis_pos in range(SIZE):
    if (axis_pos % TILE_SIZE) < GROUT_WIDTH:
        grout_noise = rng.uniform(-3, 3, SIZE)
        pixels[axis_pos, :, 0] += grout_noise
        pixels[axis_pos, :, 1] += grout_noise * 0.9
        pixels[axis_pos, :, 2] += grout_noise * 0.85
        grout_noise = rng.uniform(-3, 3, SIZE)
        pixels[:, axis_pos, 0] += grout_noise
        pixels[:, axis_pos, 1] += grout_noise * 0.9
        pixels[:, axis_pos, 2] += grout_noise * 0.85

# --- Very faint polish/sheen highlights ---
# Scattered subtle bright spots (like light reflecting off polished concrete)
num_highlights = 30
for _ in range(num_highlights):
    hx = rng.integers(0, SIZE)
    hy = rng.integers(0, SIZE)
    radius = rng.integers(3, 8)
    brightness = rng.uniform(4, 10)

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = np.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                falloff = 1.0 - (dist / radius)
                px = (hx + dx) % SIZE  # modulo wrapping for tileability
                py = (hy + dy) % SIZE
                # Skip grout pixels
                if (px % TILE_SIZE) < GROUT_WIDTH or (py % TILE_SIZE) < GROUT_WIDTH:
                    continue
                for c in range(3):
                    pixels[py, px, c] += brightness * falloff

# --- Tiny dark speckles (aggregate in concrete) ---
num_dark_specks = 200
for _ in range(num_dark_specks):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    # Skip grout
    if (sx % TILE_SIZE) < GROUT_WIDTH or (sy % TILE_SIZE) < GROUT_WIDTH:
        continue
    darkening = rng.uniform(8, 18)
    for c in range(3):
        pixels[sy, sx, c] -= darkening
    # Sometimes make it 2px
    if rng.random() < 0.3:
        nx = (sx + 1) % SIZE
        if (nx % TILE_SIZE) >= GROUT_WIDTH:
            for c in range(3):
                pixels[sy, nx, c] -= darkening * 0.7

# --- Clamp and convert ---
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

# --- Save ---
img = Image.fromarray(pixels, 'RGB')
img.save(OUTPUT)
print(f"Saved {OUTPUT} ({img.size[0]}x{img.size[1]})")
