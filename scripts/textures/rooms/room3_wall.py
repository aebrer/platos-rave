"""
Room 3 Wall Texture — "Dry Rub Wings" (Buffalo Wild Wings snack checkpoint)
Sports bar aesthetic: dark wood paneling bottom, exposed brick top, chair rail,
neon glow patches, warm amber lighting from above.
256x256 tileable texture.
"""

import numpy as np
from PIL import Image

SEED = 42
WIDTH, HEIGHT = 256, 256

rng = np.random.default_rng(SEED)

# --- Palette ---
WOOD_COLORS = np.array([
    [75, 55, 35],
    [85, 65, 45],
    [65, 45, 25],
    [80, 60, 40],
], dtype=np.float64)

BRICK_COLORS = np.array([
    [120, 60, 50],
    [110, 55, 45],
    [100, 50, 40],
    [115, 58, 48],
    [105, 52, 42],
], dtype=np.float64)

MORTAR_COLOR = np.array([90, 80, 70], dtype=np.float64)
CHAIR_RAIL_COLOR = np.array([100, 80, 55], dtype=np.float64)
CHAIR_RAIL_HIGHLIGHT = np.array([120, 95, 65], dtype=np.float64)

# Pre-generate tileable noise using a wrapped approach
def tileable_noise(w, h, scale, rng_inst):
    """Generate tileable 2D noise by sampling from a periodic grid."""
    sw = max(1, w // scale)
    sh = max(1, h // scale)
    base = rng_inst.random((sh, sw))
    # Bilinear upsample with wrapping
    out = np.zeros((h, w), dtype=np.float64)
    for y in range(h):
        for x in range(w):
            fx = (x / scale) % sw
            fy = (y / scale) % sh
            ix0 = int(fx) % sw
            iy0 = int(fy) % sh
            ix1 = (ix0 + 1) % sw
            iy1 = (iy0 + 1) % sh
            dx = fx - int(fx)
            dy = fy - int(fy)
            v = (base[iy0, ix0] * (1 - dx) * (1 - dy) +
                 base[iy0, ix1] * dx * (1 - dy) +
                 base[iy1, ix0] * (1 - dx) * dy +
                 base[iy1, ix1] * dx * dy)
            out[y, x] = v
    return out


# Faster tileable noise using vectorized operations
def tileable_noise_fast(w, h, scale, rng_inst):
    """Generate tileable 2D noise via vectorized bilinear interpolation."""
    sw = max(1, w // scale)
    sh = max(1, h // scale)
    base = rng_inst.random((sh, sw))

    xs = np.arange(w, dtype=np.float64)
    ys = np.arange(h, dtype=np.float64)
    fx = (xs / scale) % sw
    fy = (ys / scale) % sh

    ix0 = fx.astype(int) % sw
    iy0 = fy.astype(int) % sh
    ix1 = (ix0 + 1) % sw
    iy1 = (iy0 + 1) % sh

    dx = fx - fx.astype(int)
    dy = fy - fy.astype(int)

    # Build 2D grid
    ix0_2d = np.tile(ix0, (h, 1))
    ix1_2d = np.tile(ix1, (h, 1))
    iy0_2d = np.tile(iy0.reshape(-1, 1), (1, w))
    iy1_2d = np.tile(iy1.reshape(-1, 1), (1, w))
    dx_2d = np.tile(dx, (h, 1))
    dy_2d = np.tile(dy.reshape(-1, 1), (1, w))

    v00 = base[iy0_2d, ix0_2d]
    v10 = base[iy0_2d, ix1_2d]
    v01 = base[iy1_2d, ix0_2d]
    v11 = base[iy1_2d, ix1_2d]

    out = (v00 * (1 - dx_2d) * (1 - dy_2d) +
           v10 * dx_2d * (1 - dy_2d) +
           v01 * (1 - dx_2d) * dy_2d +
           v11 * dx_2d * dy_2d)
    return out


# --- Build the texture ---
img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float64)

# Layout zones (tileable vertically):
# 0..95: brick zone (upper)
# 96..103: chair rail (8px)
# 104..255: wood paneling (lower)
BRICK_TOP = 0
BRICK_BOTTOM = 95
RAIL_TOP = 96
RAIL_BOTTOM = 103
WOOD_TOP = 104
WOOD_BOTTOM = 255

# --- 1. EXPOSED BRICK (upper section) ---
BRICK_W = 32  # brick width in pixels
BRICK_H = 16  # brick height in pixels
MORTAR_W = 2  # mortar thickness

# Pre-generate per-brick color indices (tileable)
bricks_cols = WIDTH // BRICK_W
bricks_rows = (BRICK_BOTTOM - BRICK_TOP + 1) // BRICK_H + 1
brick_color_idx = rng.integers(0, len(BRICK_COLORS), size=(bricks_rows * 2, bricks_cols))
brick_variation = rng.uniform(-8, 8, size=(bricks_rows * 2, bricks_cols, 3))

for y in range(BRICK_TOP, BRICK_BOTTOM + 1):
    for x in range(WIDTH):
        local_y = y - BRICK_TOP
        row = local_y // BRICK_H
        # Offset every other row by half a brick
        offset = (BRICK_W // 2) * (row % 2)
        bx = (x + offset) % WIDTH
        col = bx // BRICK_W
        # Position within the brick
        in_brick_x = bx % BRICK_W
        in_brick_y = local_y % BRICK_H

        # Mortar lines
        is_mortar = (in_brick_x < MORTAR_W or in_brick_y < MORTAR_W)

        if is_mortar:
            color = MORTAR_COLOR.copy()
            color += rng.uniform(-3, 3, size=3)
        else:
            cidx = brick_color_idx[row % brick_color_idx.shape[0], col % bricks_cols]
            color = BRICK_COLORS[cidx].copy()
            color += brick_variation[row % brick_color_idx.shape[0], col % bricks_cols]
            # Subtle per-pixel noise
            color += rng.uniform(-4, 4, size=3)

        img[y, x] = color

# --- 2. CHAIR RAIL ---
for y in range(RAIL_TOP, RAIL_BOTTOM + 1):
    rel = y - RAIL_TOP
    thickness = RAIL_BOTTOM - RAIL_TOP + 1
    # Simple molding profile: highlight at top, shadow at bottom, base in middle
    if rel <= 1:
        base = CHAIR_RAIL_HIGHLIGHT.copy()
    elif rel >= thickness - 2:
        base = CHAIR_RAIL_COLOR * 0.7
    else:
        base = CHAIR_RAIL_COLOR.copy()
    for x in range(WIDTH):
        color = base.copy()
        color += rng.uniform(-2, 2, size=3)
        img[y, x] = color

# --- 3. DARK WOOD PANELING (lower section) ---
# Horizontal grain lines with panel divisions
PANEL_W = 64  # vertical panel width
GRAIN_SCALE = 4  # grain line spacing

# Generate tileable grain noise
grain_noise = tileable_noise_fast(WIDTH, HEIGHT, 8, rng)
grain_fine = tileable_noise_fast(WIDTH, HEIGHT, 2, rng)

for y in range(WOOD_TOP, WOOD_BOTTOM + 1):
    for x in range(WIDTH):
        # Panel index
        panel = x // PANEL_W
        in_panel_x = x % PANEL_W

        # Panel edge (vertical groove between panels)
        is_groove = (in_panel_x == 0 or in_panel_x == PANEL_W - 1)

        if is_groove:
            color = np.array([45, 32, 18], dtype=np.float64)
            color += rng.uniform(-2, 2, size=3)
        else:
            # Pick base wood color with some variation per panel
            base_idx = (panel + (y // 32)) % len(WOOD_COLORS)
            color = WOOD_COLORS[base_idx].copy()

            # Horizontal grain: darken/lighten based on y
            grain_val = grain_noise[y % HEIGHT, x % WIDTH]
            grain_fine_val = grain_fine[y % HEIGHT, x % WIDTH]
            grain_effect = (grain_val - 0.5) * 15 + (grain_fine_val - 0.5) * 8
            color += grain_effect

            # Subtle knot simulation: occasional darker spots
            # (use a deterministic pattern for tileability)
            kx = (x * 7 + y * 13) % 256
            if kx < 3:
                color *= 0.85

            # Per-pixel noise
            color += rng.uniform(-3, 3, size=3)

        img[y, x] = color

# --- 4. NEON GLOW PATCHES ---
# Place a few glow sources on the brick area to simulate neon signs out of frame

def add_glow(img, cx, cy, radius, color_tint, intensity):
    """Add a soft radial glow, wrapping around edges for tileability."""
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = np.sqrt(dx * dx + dy * dy)
            if dist > radius:
                continue
            falloff = 1.0 - (dist / radius)
            falloff = falloff ** 2  # softer falloff
            px = (cx + dx) % WIDTH
            py = (cy + dy) % HEIGHT
            # Only affect brick zone mainly, but can bleed a bit
            glow_strength = falloff * intensity
            img[py, px] += np.array(color_tint, dtype=np.float64) * glow_strength


# Red neon glow (left side)
add_glow(img, 48, 40, 35, [40, 8, 8], 0.8)
# Blue neon glow (right side)
add_glow(img, 192, 45, 30, [8, 8, 45], 0.7)
# Small green glow (center-ish, like a beer sign)
add_glow(img, 128, 35, 20, [8, 30, 10], 0.5)

# Secondary glows on the opposite side for tileability balance
add_glow(img, 48 + 128, 50, 25, [30, 10, 5], 0.4)  # warm accent

# --- 5. CHALKBOARD / MENU BOARD ---
# A dark rectangle on the brick area suggesting a menu board
BOARD_X = 80
BOARD_Y = 15
BOARD_W = 48
BOARD_H = 55

for y in range(BOARD_Y, BOARD_Y + BOARD_H):
    for x in range(BOARD_X, BOARD_X + BOARD_W):
        py = y % HEIGHT
        px = x % WIDTH
        # Dark chalkboard base
        if y == BOARD_Y or y == BOARD_Y + BOARD_H - 1 or x == BOARD_X or x == BOARD_X + BOARD_W - 1:
            # Frame
            color = np.array([60, 45, 30], dtype=np.float64)
        else:
            # Chalkboard surface
            color = np.array([30, 35, 30], dtype=np.float64)
            color += rng.uniform(-3, 3, size=3)

            # Colored chalk marks (horizontal lines suggesting menu items)
            rel_y = y - BOARD_Y
            rel_x = x - BOARD_X
            if 8 <= rel_y <= 10 and 5 <= rel_x <= 38:
                color += np.array([30, 25, 15])  # yellowish "title"
            elif rel_y in (18, 19) and 5 <= rel_x <= 30:
                color += np.array([20, 15, 10])  # text line
            elif rel_y in (24, 25) and 5 <= rel_x <= 34:
                color += np.array([20, 15, 10])
            elif rel_y in (30, 31) and 5 <= rel_x <= 28:
                color += np.array([20, 15, 10])
            # Price column
            if rel_y in (18, 19, 24, 25, 30, 31) and 35 <= rel_x <= 42:
                color += np.array([15, 25, 10])  # green-ish prices
            # Red "special" highlight
            if 38 <= rel_y <= 42 and 5 <= rel_x <= 25:
                color += np.array([35, 8, 8])

        img[py, px] = color

# --- 6. WARM AMBER LIGHTING FROM ABOVE ---
# Gradient: stronger at top, fading down
for y in range(HEIGHT):
    # Amber wash strongest at top of brick, fading through chair rail, minimal on wood
    if y <= BRICK_BOTTOM:
        strength = 1.0 - (y / (BRICK_BOTTOM + 1)) * 0.6
    elif y <= RAIL_BOTTOM:
        strength = 0.3
    else:
        # Wood section: very subtle top-down light
        rel = (y - WOOD_TOP) / (WOOD_BOTTOM - WOOD_TOP + 1)
        strength = 0.15 * (1.0 - rel * 0.7)

    amber_tint = np.array([18, 10, 2], dtype=np.float64) * strength
    img[y, :] += amber_tint

# Also add a couple of spotlight pools from above (circular warm patches)
def add_spotlight(img, cx, top_y, spread_x, spread_y, intensity):
    """Add a warm spotlight cone from above."""
    for dy in range(-spread_y, spread_y + 1):
        for dx in range(-spread_x, spread_x + 1):
            # Elliptical falloff
            nx = dx / spread_x
            ny = dy / spread_y
            dist = np.sqrt(nx * nx + ny * ny)
            if dist > 1.0:
                continue
            falloff = (1.0 - dist) ** 1.5
            px = (cx + dx) % WIDTH
            py = (top_y + dy) % HEIGHT
            amber = np.array([20, 12, 3], dtype=np.float64) * falloff * intensity
            img[py, px] += amber


add_spotlight(img, 64, 10, 40, 25, 0.7)
add_spotlight(img, 200, 8, 35, 20, 0.6)

# --- 7. CLAMP AND QUANTIZE ---
img = np.clip(img, 0, 255).astype(np.uint8)

# --- 8. SAVE ---
output = Image.fromarray(img, 'RGB')
output.save('../../docs/assets/rooms/room3_wall.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
