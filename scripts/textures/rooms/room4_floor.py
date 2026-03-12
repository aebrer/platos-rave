"""
Room 4 Floor Texture — "The Best Rave of Your Life" dance floor.

LED dance floor with neon-lit panel grid, glowing tiles, and laser reflections.
256x256, seamless/tileable, pixel art dungeon-crawler aesthetic.
"""

import numpy as np
from PIL import Image

SEED = 42
SIZE = 256
PANEL_SIZE = 32  # 8x8 grid of panels
NUM_PANELS = SIZE // PANEL_SIZE

rng = np.random.RandomState(SEED)

# Output array (H, W, 3) uint8
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

# Base color for all panels — very dark purple-black
BASE = np.array([15, 10, 25], dtype=np.float64)

# Neon palette for panel tints and edges
NEON_COLORS = [
    np.array([255, 20, 147]),   # hot pink
    np.array([0, 255, 255]),    # cyan
    np.array([180, 0, 255]),    # purple
    np.array([0, 255, 100]),    # neon green
    np.array([255, 0, 100]),    # magenta-red
    np.array([100, 0, 255]),    # blue-violet
    np.array([255, 100, 0]),    # neon orange
    np.array([0, 200, 255]),    # electric blue
]

# Assign a neon tint to each panel (deterministic per panel for tileability)
panel_tints = np.zeros((NUM_PANELS, NUM_PANELS, 3), dtype=np.float64)
panel_active = np.zeros((NUM_PANELS, NUM_PANELS), dtype=bool)
panel_edge_color_idx = np.zeros((NUM_PANELS, NUM_PANELS), dtype=int)

for py in range(NUM_PANELS):
    for px in range(NUM_PANELS):
        idx = rng.randint(0, len(NEON_COLORS))
        panel_tints[py, px] = NEON_COLORS[idx]
        panel_edge_color_idx[py, px] = rng.randint(0, len(NEON_COLORS))
        # ~25% of panels are "active" LED tiles
        panel_active[py, px] = rng.random() < 0.25


def smooth_glow(cx, cy, x, y, radius):
    """Compute smooth radial falloff from center, returns 0..1."""
    dx = x - cx
    dy = y - cy
    dist_sq = dx * dx + dy * dy
    r_sq = radius * radius
    if dist_sq >= r_sq:
        return 0.0
    t = 1.0 - dist_sq / r_sq
    return t * t  # quadratic falloff


# --- Fill panels ---
for py in range(NUM_PANELS):
    for px in range(NUM_PANELS):
        y0 = py * PANEL_SIZE
        x0 = px * PANEL_SIZE
        tint = panel_tints[py, px]
        edge_color = NEON_COLORS[panel_edge_color_idx[py, px]]
        is_active = panel_active[py, px]

        for ly in range(PANEL_SIZE):
            for lx in range(PANEL_SIZE):
                gy = (y0 + ly) % SIZE
                gx = (x0 + lx) % SIZE

                # Start with base + subtle tint
                color = BASE.copy() + tint * 0.06

                # Panel edge glow (1px bright edge lines)
                is_edge = (ly == 0 or ly == PANEL_SIZE - 1 or
                           lx == 0 or lx == PANEL_SIZE - 1)
                is_inner_edge = (ly == 1 or ly == PANEL_SIZE - 2 or
                                 lx == 1 or lx == PANEL_SIZE - 2)

                if is_edge:
                    # Bright neon edge
                    color = color * 0.3 + edge_color * 0.55
                elif is_inner_edge:
                    # Softer glow next to edge
                    color = color * 0.7 + edge_color * 0.18

                # Active LED panel: center glow
                if is_active and not is_edge:
                    cx = PANEL_SIZE / 2.0
                    cy = PANEL_SIZE / 2.0
                    glow = smooth_glow(cx, cy, lx, ly, PANEL_SIZE * 0.42)
                    if glow > 0:
                        # Bright center with tint color
                        brightness = glow * 0.6
                        color = color * (1 - brightness) + tint * brightness

                img[gy, gx] = np.clip(color, 0, 255).astype(np.uint8)

# --- Add subtle per-panel noise for texture ---
noise = rng.randint(-4, 5, size=(SIZE, SIZE, 3)).astype(np.int16)
img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# --- Laser reflection spots (bright small dots scattered on floor) ---
LASER_COLORS = [
    np.array([255, 50, 180]),   # pink
    np.array([0, 255, 255]),    # cyan
    np.array([50, 255, 100]),   # green
    np.array([255, 255, 80]),   # yellow
    np.array([200, 50, 255]),   # purple
]

num_laser_spots = 40
for _ in range(num_laser_spots):
    sx = rng.randint(0, SIZE)
    sy = rng.randint(0, SIZE)
    spot_color = LASER_COLORS[rng.randint(0, len(LASER_COLORS))]
    radius = rng.randint(2, 5)

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            px_x = (sx + dx) % SIZE
            px_y = (sy + dy) % SIZE
            glow = smooth_glow(sx, sy, sx + dx, sy + dy, radius)
            if glow > 0:
                existing = img[px_y, px_x].astype(np.float64)
                blended = existing + spot_color * glow * 0.7
                img[px_y, px_x] = np.clip(blended, 0, 255).astype(np.uint8)

# --- Additional: faint cross-hatch pattern inside panels for pixel art feel ---
for y in range(SIZE):
    for x in range(SIZE):
        ly = y % PANEL_SIZE
        lx = x % PANEL_SIZE
        # Every 4th pixel, slightly darken for a subtle grid texture
        if (ly % 4 == 0 or lx % 4 == 0) and ly > 1 and ly < PANEL_SIZE - 2 and lx > 1 and lx < PANEL_SIZE - 2:
            img[y, x] = np.clip(img[y, x].astype(np.int16) - 3, 0, 255).astype(np.uint8)

# --- Save output ---
output = Image.fromarray(img, mode='RGB')
output.save('../../docs/assets/rooms/room4_floor.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
