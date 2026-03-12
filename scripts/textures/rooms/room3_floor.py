"""
Room 3 Floor Texture — "Dry Rub Wings" Sports Bar Floor

Dark hardwood planks with a grimy, sticky sports-bar feel.
Horizontal planks with staggered joints, wood grain, and wear/spill patches.
256x256, tileable/seamless, pixel art dungeon-crawler aesthetic.
"""

import numpy as np
from PIL import Image

SEED = 42
SIZE = 256
rng = np.random.default_rng(SEED)

# --- Palette ---
PLANK_COLORS = [
    (90, 65, 40),
    (85, 60, 35),
    (95, 70, 45),
    (88, 62, 38),
    (92, 68, 42),
]
SEAM_COLOR = np.array([50, 35, 20], dtype=np.float64)
WEAR_COLOR = np.array([75, 55, 30], dtype=np.float64)

# --- Plank layout ---
# Each plank is 32px tall (8 planks fit exactly in 256)
PLANK_HEIGHT = 32
NUM_PLANKS = SIZE // PLANK_HEIGHT  # 8

# Assign a base color to each plank row
plank_base = np.array([PLANK_COLORS[rng.integers(0, len(PLANK_COLORS))] for _ in range(NUM_PLANKS)], dtype=np.float64)

# Staggered joint offsets per plank row (where vertical seams fall)
# Plank segments are 64-96px wide, staggered row to row
joint_positions = []
for row in range(NUM_PLANKS):
    joints = []
    x = rng.integers(20, 60)  # first joint offset for stagger
    while x < SIZE:
        joints.append(x % SIZE)
        x += rng.integers(64, 97)
    joint_positions.append(sorted(joints))

# --- Build texture ---
pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)

for y in range(SIZE):
    plank_idx = (y // PLANK_HEIGHT) % NUM_PLANKS
    y_in_plank = y % PLANK_HEIGHT
    base = plank_base[plank_idx].copy()

    for x in range(SIZE):
        color = base.copy()

        # --- Wood grain: horizontal streaks ---
        # Use a deterministic noise based on position
        grain_seed = (y * 7 + x * 3 + plank_idx * 13) % 1000
        grain_val = np.sin(x * 0.15 + y * 0.5 + grain_seed * 0.01) * 4
        grain_val += np.sin(x * 0.03 + plank_idx * 5.0) * 3
        # Add per-pixel jitter for texture
        grain_val += rng.uniform(-2, 2)
        color = color + grain_val

        # --- Plank horizontal seam (top and bottom edge of each plank) ---
        if y_in_plank == 0 or y_in_plank == PLANK_HEIGHT - 1:
            color = SEAM_COLOR.copy() + rng.uniform(-3, 3)

        # --- Vertical joint seams ---
        joints = joint_positions[plank_idx]
        for jx in joints:
            if x == jx % SIZE or x == (jx + 1) % SIZE:
                # Draw a 2px wide vertical seam, but not on horizontal seam lines
                if y_in_plank > 1 and y_in_plank < PLANK_HEIGHT - 2:
                    color = SEAM_COLOR.copy() + rng.uniform(-3, 3)

        pixels[y, x] = color

# --- Seamless wood grain detail pass (modulo-wrapped) ---
# Add knot-like darker patches at fixed positions
num_knots = 12
knot_xs = rng.integers(0, SIZE, size=num_knots)
knot_ys = rng.integers(0, SIZE, size=num_knots)
knot_radii = rng.integers(3, 8, size=num_knots)
for kx, ky, kr in zip(knot_xs, knot_ys, knot_radii):
    for dy in range(-kr, kr + 1):
        for dx in range(-kr, kr + 1):
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= kr:
                px = (kx + dx) % SIZE
                py = (ky + dy) % SIZE
                fade = 1.0 - (dist / kr) * 0.6
                pixels[py, px] = pixels[py, px] * (0.85 * fade + 0.15)

# --- Wear / sticky patches (larger, subtle darkening) ---
num_wear = 18
wear_xs = rng.integers(0, SIZE, size=num_wear)
wear_ys = rng.integers(0, SIZE, size=num_wear)
wear_radii = rng.integers(8, 24, size=num_wear)
wear_intensity = rng.uniform(0.04, 0.12, size=num_wear)
for wx, wy, wr, wi in zip(wear_xs, wear_ys, wear_radii, wear_intensity):
    for dy in range(-wr, wr + 1):
        for dx in range(-wr, wr + 1):
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= wr:
                px = (wx + dx) % SIZE
                py = (wy + dy) % SIZE
                fade = 1.0 - (dist / wr)
                # Darken and shift toward wear color
                pixels[py, px] = pixels[py, px] * (1.0 - wi * fade) + WEAR_COLOR * (wi * fade * 0.5)

# --- Spill stains (very subtle, slightly darker splotches) ---
num_stains = 8
stain_xs = rng.integers(0, SIZE, size=num_stains)
stain_ys = rng.integers(0, SIZE, size=num_stains)
stain_radii = rng.integers(5, 15, size=num_stains)
for sx, sy, sr in zip(stain_xs, stain_ys, stain_radii):
    for dy in range(-sr, sr + 1):
        for dx in range(-sr, sr + 1):
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= sr:
                px = (sx + dx) % SIZE
                py = (sy + dy) % SIZE
                # Slightly glossy/sticky look: darken + slight reddish tint (wing sauce)
                fade = (1.0 - dist / sr) * 0.08
                pixels[py, px, 0] = pixels[py, px, 0] * (1.0 - fade) + 60 * fade
                pixels[py, px, 1] = pixels[py, px, 1] * (1.0 - fade * 1.2)
                pixels[py, px, 2] = pixels[py, px, 2] * (1.0 - fade * 1.5)

# --- Pixel art quantization: reduce color depth slightly ---
pixels = np.round(pixels / 4.0) * 4.0

# --- Clamp and convert ---
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

img = Image.fromarray(pixels, 'RGB')
img.save('../../docs/assets/rooms/room3_floor.png')
print(f"Saved output.png: {img.size[0]}x{img.size[1]}")
