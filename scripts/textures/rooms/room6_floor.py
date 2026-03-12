"""
Room 6 Floor Texture — "Sauce on Six" greasy kitchen floor.

Commercial kitchen quarry tile: terracotta red, anti-slip bumps,
greasy grout lines, sauce spills and grease patches.
256x256, seamless/tileable.
"""

import numpy as np
from PIL import Image

SEED = 6006
SIZE = 256
TILE_SIZE = 16  # divides 256 evenly (16 tiles per row/col)
GROUT_WIDTH = 1

# Palette
TILE_COLORS = [
    (150, 90, 70),
    (140, 85, 65),
    (160, 95, 75),
    (145, 88, 68),
    (155, 92, 72),
]
GROUT_COLOR = np.array([60, 50, 40], dtype=np.uint8)
GREASE_GROUT = np.array([100, 85, 50], dtype=np.uint8)
SAUCE_COLORS = [
    (170, 60, 30),
    (180, 70, 25),
    (165, 55, 35),
]
GREASE_TILE = np.array([120, 100, 60], dtype=np.uint8)

rng = np.random.default_rng(SEED)

# Start with blank canvas
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

# --- Step 1: Fill tiles and grout ---
for y in range(SIZE):
    for x in range(SIZE):
        # Position within tile cell (with wrapping)
        cell_y = y % TILE_SIZE
        cell_x = x % TILE_SIZE

        # Determine if this pixel is grout
        is_grout = cell_y < GROUT_WIDTH or cell_x < GROUT_WIDTH

        if is_grout:
            img[y, x] = GROUT_COLOR
        else:
            # Pick tile color based on tile index (deterministic variation)
            tile_row = y // TILE_SIZE
            tile_col = x // TILE_SIZE
            color_idx = (tile_row * 7 + tile_col * 13 + tile_row * tile_col * 3) % len(TILE_COLORS)
            img[y, x] = TILE_COLORS[color_idx]

# --- Step 2: Non-slip bump texture on tiles ---
# Small dots slightly lighter than base, in a regular sub-grid pattern
for y in range(SIZE):
    for x in range(SIZE):
        cell_y = y % TILE_SIZE
        cell_x = x % TILE_SIZE

        # Skip grout pixels
        if cell_y < GROUT_WIDTH or cell_x < GROUT_WIDTH:
            continue

        # Bump dots every 3 pixels within tile, offset from grout
        inner_y = cell_y - GROUT_WIDTH
        inner_x = cell_x - GROUT_WIDTH

        if inner_y % 3 == 1 and inner_x % 3 == 1:
            # Add slight brightness variation to bumps for realism
            tile_row = y // TILE_SIZE
            tile_col = x // TILE_SIZE
            bump_var = ((tile_row * 11 + tile_col * 17 + inner_y * 5 + inner_x * 7) % 3) - 1
            base = img[y, x].astype(np.int16)
            bump = base + 18 + bump_var * 3
            img[y, x] = np.clip(bump, 0, 255).astype(np.uint8)

# --- Step 3: Greasy grout lines ---
# Some grout intersections and stretches get amber grease buildup
# Pre-generate which tile corners get grease
num_tiles = SIZE // TILE_SIZE
grease_corners = rng.random((num_tiles, num_tiles)) < 0.35

for ty in range(num_tiles):
    for tx in range(num_tiles):
        if not grease_corners[ty, tx]:
            continue

        # Grease around the top-left corner of this tile cell
        corner_y = ty * TILE_SIZE
        corner_x = tx * TILE_SIZE

        # Spread grease 2-3 pixels around the corner
        spread = rng.integers(2, 5)
        for dy in range(-spread, spread + 1):
            for dx in range(-spread, spread + 1):
                py = (corner_y + dy) % SIZE
                px = (corner_x + dx) % SIZE

                dist = abs(dy) + abs(dx)
                if dist > spread:
                    continue

                cell_y = py % TILE_SIZE
                cell_x = px % TILE_SIZE
                is_grout = cell_y < GROUT_WIDTH or cell_x < GROUT_WIDTH

                if is_grout:
                    # Grease on grout — amber color
                    blend = max(0.0, 1.0 - dist / (spread + 1))
                    base = img[py, px].astype(np.float32)
                    target = GREASE_GROUT.astype(np.float32)
                    img[py, px] = np.clip(base * (1 - blend) + target * blend, 0, 255).astype(np.uint8)
                elif dist <= 1:
                    # Slight grease on adjacent tile pixels
                    base = img[py, px].astype(np.float32)
                    target = GREASE_TILE.astype(np.float32)
                    img[py, px] = np.clip(base * 0.8 + target * 0.2, 0, 255).astype(np.uint8)

# --- Step 4: Grease along some grout lines (longer streaks) ---
for ty in range(num_tiles):
    for tx in range(num_tiles):
        # Horizontal grout grease streaks
        if rng.random() < 0.2:
            gy = ty * TILE_SIZE
            length = rng.integers(4, TILE_SIZE)
            start_x = tx * TILE_SIZE + rng.integers(0, TILE_SIZE // 2)
            for dx in range(length):
                px = (start_x + dx) % SIZE
                for dgy in range(GROUT_WIDTH):
                    py = (gy + dgy) % SIZE
                    base = img[py, px].astype(np.float32)
                    target = GREASE_GROUT.astype(np.float32)
                    blend = 0.6
                    img[py, px] = np.clip(base * (1 - blend) + target * blend, 0, 255).astype(np.uint8)

        # Vertical grout grease streaks
        if rng.random() < 0.2:
            gx = tx * TILE_SIZE
            length = rng.integers(4, TILE_SIZE)
            start_y = ty * TILE_SIZE + rng.integers(0, TILE_SIZE // 2)
            for dy in range(length):
                py = (start_y + dy) % SIZE
                for dgx in range(GROUT_WIDTH):
                    px = (gx + dgx) % SIZE
                    base = img[py, px].astype(np.float32)
                    target = GREASE_GROUT.astype(np.float32)
                    blend = 0.6
                    img[py, px] = np.clip(base * (1 - blend) + target * blend, 0, 255).astype(np.uint8)

# --- Step 5: Sauce spills ---
# Scatter sauce splotches across multiple tiles, seamless-safe
num_spills = 12
for _ in range(num_spills):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    sauce_color = np.array(SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))], dtype=np.float32)
    radius = rng.integers(3, 9)

    # Irregular shape via random angle offsets
    shape_noise = rng.random(8) * 0.5 + 0.5  # per-octant radius multiplier

    for dy in range(-radius - 1, radius + 2):
        for dx in range(-radius - 1, radius + 2):
            py = (cy + dy) % SIZE
            px = (cx + dx) % SIZE

            # Skip grout pixels (sauce sits on tiles)
            cell_y = py % TILE_SIZE
            cell_x = px % TILE_SIZE
            if cell_y < GROUT_WIDTH or cell_x < GROUT_WIDTH:
                continue

            dist = np.sqrt(dy * dy + dx * dx)

            # Irregular edge via octant
            angle = np.arctan2(dy, dx)
            octant = int((angle + np.pi) / (np.pi / 4)) % 8
            effective_radius = radius * shape_noise[octant]

            if dist > effective_radius:
                continue

            # Blend: stronger in center, fade at edge
            blend = max(0.0, 1.0 - (dist / effective_radius) ** 1.5) * 0.7

            base = img[py, px].astype(np.float32)
            img[py, px] = np.clip(base * (1 - blend) + sauce_color * blend, 0, 255).astype(np.uint8)

# --- Step 6: Small sauce drips/drops ---
num_drips = 20
for _ in range(num_drips):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    sauce_color = np.array(SAUCE_COLORS[rng.integers(0, len(SAUCE_COLORS))], dtype=np.float32)

    # Single pixel or 2-pixel drip
    for dy in range(rng.integers(1, 3)):
        for dx in range(rng.integers(1, 3)):
            py = (cy + dy) % SIZE
            px = (cx + dx) % SIZE
            cell_y = py % TILE_SIZE
            cell_x = px % TILE_SIZE
            if cell_y < GROUT_WIDTH or cell_x < GROUT_WIDTH:
                continue
            base = img[py, px].astype(np.float32)
            img[py, px] = np.clip(base * 0.35 + sauce_color * 0.65, 0, 255).astype(np.uint8)

# --- Step 7: Subtle per-tile color variation (wear/age) ---
for ty in range(num_tiles):
    for tx in range(num_tiles):
        # Slight random darkening/lightening per tile
        shift = rng.integers(-8, 9)
        if shift == 0:
            continue
        for dy in range(GROUT_WIDTH, TILE_SIZE):
            for dx in range(GROUT_WIDTH, TILE_SIZE):
                py = ty * TILE_SIZE + dy
                px = tx * TILE_SIZE + dx
                if py >= SIZE or px >= SIZE:
                    continue
                base = img[py, px].astype(np.int16)
                img[py, px] = np.clip(base + shift, 0, 255).astype(np.uint8)

# --- Step 8: Dark corner grime (where tiles meet, extra grime near grout) ---
for ty in range(num_tiles):
    for tx in range(num_tiles):
        if rng.random() < 0.5:
            continue
        # Darken the 1-2 pixels adjacent to grout inside the tile
        base_y = ty * TILE_SIZE
        base_x = tx * TILE_SIZE
        darken = rng.integers(8, 20)

        for d in range(1, 3):
            # Along top edge (below grout)
            if GROUT_WIDTH + d - 1 < TILE_SIZE:
                row = (base_y + GROUT_WIDTH + d - 1) % SIZE
                for dx in range(GROUT_WIDTH, TILE_SIZE):
                    col = (base_x + dx) % SIZE
                    fade = darken // d
                    base = img[row, col].astype(np.int16)
                    img[row, col] = np.clip(base - fade, 0, 255).astype(np.uint8)

            # Along left edge (right of grout)
            if GROUT_WIDTH + d - 1 < TILE_SIZE:
                col = (base_x + GROUT_WIDTH + d - 1) % SIZE
                for dy in range(GROUT_WIDTH, TILE_SIZE):
                    row = (base_y + dy) % SIZE
                    fade = darken // d
                    base = img[row, col].astype(np.int16)
                    img[row, col] = np.clip(base - fade, 0, 255).astype(np.uint8)

# --- Save output ---
output = Image.fromarray(img, 'RGB')
output.save('../../docs/assets/rooms/room6_floor.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
