"""
Room 6 Wall Texture — "Sauce on Six" (Ghost Kitchen / DoorDash wing joint)
Stainless steel backsplash with wing sauce splatters, grease drips,
service window, and heat lamp glow. Tileable 256x256 pixel art.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SEED = 606
SIZE = 256
rng = np.random.default_rng(SEED)

# Output array (RGB float for blending)
pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)

# --- Palette ---
STEEL_COLORS = [
    (160, 165, 170),
    (170, 175, 180),
    (150, 155, 160),
    (155, 160, 165),
]
GROUT = (120, 122, 125)
SAUCE_COLORS = [
    (180, 60, 30),
    (200, 80, 20),
    (160, 50, 25),
    (190, 70, 25),
    (170, 55, 20),
]
GREASE = (180, 160, 100)
HEAT_GLOW = (200, 120, 60)
WINDOW_DARK = (40, 35, 30)
WINDOW_SHELF = (100, 95, 85)


def wrap(v):
    return v % SIZE


# --- 1. Base stainless steel fill with subtle noise ---
for y in range(SIZE):
    for x in range(SIZE):
        base = STEEL_COLORS[0]
        noise = rng.integers(-6, 7, size=3)
        pixels[y, x] = np.clip(np.array(base) + noise, 0, 255)


# --- 2. Stainless steel subway tiles (rectangular, horizontal) ---
TILE_W = 64  # tile width — divides 256 evenly
TILE_H = 32  # tile height — divides 256 evenly
GROUT_W = 2  # grout line width

for y in range(SIZE):
    for x in range(SIZE):
        row = y // TILE_H
        # Offset every other row by half a tile width for brick pattern
        offset = (row % 2) * (TILE_W // 2)
        local_x = (x + offset) % TILE_W
        local_y = y % TILE_H

        # Grout lines
        if local_x < GROUT_W or local_y < GROUT_W:
            noise = rng.integers(-3, 4, size=3)
            pixels[y, x] = np.clip(np.array(GROUT) + noise, 0, 255)
        else:
            # Pick steel color based on tile index for variety
            tile_col = ((x + offset) // TILE_W) % 4
            tile_idx = (row * 7 + tile_col * 3) % len(STEEL_COLORS)
            base = np.array(STEEL_COLORS[tile_idx], dtype=np.float64)
            # Brushed steel effect: horizontal streaks
            streak = rng.integers(-4, 5)
            base += streak
            # Slight vertical gradient within tile (lighter at top = reflection)
            frac = local_y / TILE_H
            base += (1.0 - frac) * 8 - 4
            noise = rng.integers(-3, 4, size=3)
            pixels[y, x] = np.clip(base + noise, 0, 255)

# --- 3. Brushed steel horizontal lines (subtle) ---
for y in range(SIZE):
    if rng.random() < 0.3:
        intensity = rng.integers(-5, 6)
        pixels[y, :, :] += intensity

pixels = np.clip(pixels, 0, 255)


# --- 4. Service window / pass-through (smaller, off-center) ---
WIN_X, WIN_Y = 88, 72
WIN_W, WIN_H = 72, 40
SHELF_H = 5
FRAME_W = 3

for y in range(WIN_Y - FRAME_W, WIN_Y + WIN_H + SHELF_H + FRAME_W):
    for x in range(WIN_X - FRAME_W, WIN_X + WIN_W + FRAME_W):
        wy = wrap(y)
        wx = wrap(x)
        rel_x = x - WIN_X
        rel_y = y - WIN_Y

        in_frame = (
            (WIN_X - FRAME_W <= x < WIN_X or WIN_X + WIN_W <= x < WIN_X + WIN_W + FRAME_W)
            and WIN_Y - FRAME_W <= y < WIN_Y + WIN_H + SHELF_H + FRAME_W
        ) or (
            (WIN_Y - FRAME_W <= y < WIN_Y or WIN_Y + WIN_H <= y < WIN_Y + WIN_H + SHELF_H + FRAME_W)
            and WIN_X - FRAME_W <= x < WIN_X + WIN_W + FRAME_W
        )

        if 0 <= rel_x < WIN_W and 0 <= rel_y < WIN_H:
            # Dark window interior with slight depth gradient
            depth_noise = rng.integers(-5, 6, size=3)
            # Slightly lighter near edges (ambient bounce)
            edge_dist = min(rel_x, WIN_W - rel_x, rel_y, WIN_H - rel_y)
            bounce = max(0, 8 - edge_dist) * 2
            pixels[wy, wx] = np.clip(np.array(WINDOW_DARK) + depth_noise + bounce, 0, 255)
        elif 0 <= rel_x < WIN_W and WIN_H <= rel_y < WIN_H + SHELF_H:
            # Shelf
            shelf_noise = rng.integers(-4, 5, size=3)
            highlight = 18 if rel_y == WIN_H else (8 if rel_y == WIN_H + 1 else 0)
            pixels[wy, wx] = np.clip(np.array(WINDOW_SHELF) + shelf_noise + highlight, 0, 255)
        elif in_frame:
            # Steel frame — brighter than wall
            frame_col = np.array([185, 190, 195], dtype=np.float64)
            frame_col += rng.integers(-3, 4, size=3)
            pixels[wy, wx] = np.clip(frame_col, 0, 255)


# --- 5. Sauce splatters (organic blobs using filled circles + secondary drops) ---
def draw_blob(cx, cy, radius, color, rng, alpha_base=0.75):
    """Draw an organic sauce blob using overlapping filled circles."""
    color = np.array(color, dtype=np.float64)

    # Main blob: several overlapping circles for irregular shape
    num_circles = max(3, radius // 2)
    for _ in range(num_circles):
        # Offset each sub-circle from center
        ox = int(rng.normal(0, radius * 0.3))
        oy = int(rng.normal(0, radius * 0.3))
        sub_r = int(radius * rng.uniform(0.4, 0.9))

        for dy in range(-sub_r, sub_r + 1):
            for dx in range(-sub_r, sub_r + 1):
                dist_sq = dx * dx + dy * dy
                if dist_sq <= sub_r * sub_r:
                    px = wrap(cx + ox + dx)
                    py = wrap(cy + oy + dy)
                    # Softer edges
                    dist = np.sqrt(dist_sq)
                    edge_fade = 1.0 if dist < sub_r * 0.7 else (1.0 - (dist - sub_r * 0.7) / (sub_r * 0.3 + 0.01))
                    alpha = alpha_base * edge_fade * rng.uniform(0.8, 1.0)
                    noise = rng.integers(-6, 7, size=3)
                    old = pixels[py, px].copy()
                    new_col = color + noise
                    pixels[py, px] = np.clip(old * (1 - alpha) + new_col * alpha, 0, 255)

    # Secondary satellite drops around the main blob
    num_drops = rng.integers(2, 6)
    for _ in range(num_drops):
        angle = rng.uniform(0, 2 * np.pi)
        drop_dist = radius * rng.uniform(1.1, 2.0)
        drop_x = int(cx + drop_dist * np.cos(angle))
        drop_y = int(cy + drop_dist * np.sin(angle))
        drop_r = rng.integers(1, max(2, radius // 3))

        for dy in range(-drop_r, drop_r + 1):
            for dx in range(-drop_r, drop_r + 1):
                if dx * dx + dy * dy <= drop_r * drop_r:
                    px = wrap(drop_x + dx)
                    py = wrap(drop_y + dy)
                    alpha = alpha_base * 0.8
                    noise = rng.integers(-6, 7, size=3)
                    old = pixels[py, px].copy()
                    new_col = color + noise
                    pixels[py, px] = np.clip(old * (1 - alpha) + new_col * alpha, 0, 255)


# Medium splatters scattered everywhere
for _ in range(25):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    radius = rng.integers(4, 12)
    color = SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))]
    draw_blob(cx, cy, radius, color, rng)

# A few big dramatic splatters
for _ in range(5):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    radius = rng.integers(12, 22)
    color = SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))]
    draw_blob(cx, cy, radius, color, rng, alpha_base=0.8)

# Tiny sauce flecks
for _ in range(40):
    fx = rng.integers(0, SIZE)
    fy = rng.integers(0, SIZE)
    color = np.array(SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))], dtype=np.float64)
    noise = rng.integers(-8, 9, size=3)
    pixels[fy, fx] = np.clip(color + noise, 0, 255)
    # Sometimes a 2-pixel fleck
    if rng.random() < 0.5:
        pixels[wrap(fy + 1), fx] = np.clip(color + rng.integers(-8, 9, size=3), 0, 255)


# --- 6. Sauce drip trails running down from some splatters ---
num_drips = 16
for _ in range(num_drips):
    dx_start = rng.integers(0, SIZE)
    dy_start = rng.integers(0, SIZE)
    drip_len = rng.integers(15, 55)
    color = np.array(SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))], dtype=np.float64)
    width = rng.integers(1, 4)
    cur_x = dx_start

    for step in range(drip_len):
        y_pos = wrap(dy_start + step)
        # Drip narrows and fades as it goes down
        fade = 1.0 - (step / drip_len) * 0.7
        cur_width = max(1, int(width * fade))
        # Slight lateral wobble
        if rng.random() < 0.12:
            cur_x = wrap(cur_x + rng.choice([-1, 1]))
        for w in range(-cur_width // 2, cur_width // 2 + 1):
            x_pos = wrap(cur_x + w)
            alpha = 0.55 * fade
            old = pixels[y_pos, x_pos].copy()
            pixels[y_pos, x_pos] = np.clip(
                old * (1 - alpha) + color * alpha, 0, 255
            )
        # Drip bead at the bottom (slightly wider last few pixels)
        if step >= drip_len - 3 and width > 1:
            for w in [-(cur_width // 2 + 1), cur_width // 2 + 1]:
                x_pos = wrap(cur_x + w)
                alpha = 0.3 * fade
                old = pixels[y_pos, x_pos].copy()
                pixels[y_pos, x_pos] = np.clip(
                    old * (1 - alpha) + color * alpha, 0, 255
                )


# --- 7. Grease streaks / drips (amber, translucent) ---
num_grease = 14
for _ in range(num_grease):
    gx = rng.integers(0, SIZE)
    gy = rng.integers(0, SIZE)
    grease_len = rng.integers(20, 70)
    grease_col = np.array(GREASE, dtype=np.float64)

    for step in range(grease_len):
        y_pos = wrap(gy + step)
        fade = 1.0 - (step / grease_len) * 0.5
        alpha = 0.18 * fade
        wobble = 1 if rng.random() < 0.12 else (-1 if rng.random() < 0.12 else 0)
        gx = wrap(gx + wobble)
        old = pixels[y_pos, gx].copy()
        noise = rng.integers(-5, 6, size=3)
        pixels[y_pos, gx] = np.clip(
            old * (1 - alpha) + (grease_col + noise) * alpha, 0, 255
        )
        # Wider at top
        if step < grease_len * 0.3:
            for w in [-1, 1]:
                nx = wrap(gx + w)
                old2 = pixels[y_pos, nx].copy()
                pixels[y_pos, nx] = np.clip(
                    old2 * (1 - alpha * 0.5) + (grease_col + noise) * alpha * 0.5, 0, 255
                )


# --- 8. Heat lamp glow from above (warm orange tint at top) ---
glow_col = np.array(HEAT_GLOW, dtype=np.float64)
for y in range(SIZE):
    # Tileable: glow near top and bottom edges (since they tile together)
    dist_from_top = min(y, SIZE - y)
    if dist_from_top < 50:
        strength = (1.0 - dist_from_top / 50.0) ** 1.5 * 0.22
        for x in range(SIZE):
            old = pixels[y, x].copy()
            pixels[y, x] = np.clip(
                old * (1 - strength) + glow_col * strength + old * strength * 0.3,
                0, 255
            )

# Heat lamp hotspot near top-center
LAMP_CX, LAMP_CY = 128, 10
LAMP_R = 35
for y in range(SIZE):
    for x in range(SIZE):
        dx = min(abs(x - LAMP_CX), SIZE - abs(x - LAMP_CX))
        dy = min(abs(y - LAMP_CY), SIZE - abs(y - LAMP_CY))
        dist = np.sqrt(dx * dx + dy * dy)
        if dist < LAMP_R:
            strength = (1.0 - dist / LAMP_R) ** 2 * 0.18
            old = pixels[y, x].copy()
            pixels[y, x] = np.clip(old + glow_col * strength, 0, 255)


# --- 9. Pixel art quantize (reduce to limited palette feel) ---
pixels = (pixels // 4) * 4
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

# --- 10. Grime spots (tileable darkening) ---
num_grime = 18
for _ in range(num_grime):
    gx = rng.integers(0, SIZE)
    gy = rng.integers(0, SIZE)
    gr = rng.integers(2, 5)
    for dy in range(-gr, gr + 1):
        for dx in range(-gr, gr + 1):
            if dx * dx + dy * dy <= gr * gr:
                wx, wy = wrap(gx + dx), wrap(gy + dy)
                darken = rng.uniform(0.87, 0.95)
                pixels[wy, wx] = np.clip(
                    pixels[wy, wx].astype(np.float64) * darken, 0, 255
                ).astype(np.uint8)


# --- Save ---
img = Image.fromarray(pixels, 'RGB')
img.save('../../docs/assets/rooms/room6_wall.png')
print(f"Saved output.png: {img.size[0]}x{img.size[1]}")
