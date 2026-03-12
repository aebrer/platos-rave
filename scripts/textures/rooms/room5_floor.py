"""
Room 5 Floor Texture: "Barometric Pressure"
Submarine/pressure chamber industrial metal grating floor.
Diamond plate pattern with bolt heads and standing water in recesses.
256x256, tileable/seamless, pixel art dungeon-crawler aesthetic.
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 42

# Palette
METAL_BASE = np.array([75, 80, 90])
METAL_LIGHT = np.array([95, 100, 110])
GROOVE_DARK = np.array([35, 40, 50])
BOLT_COLOR = np.array([110, 115, 125])
BOLT_HIGHLIGHT = np.array([130, 135, 145])
WATER_COLOR = np.array([20, 30, 45])
WATER_HIGHLIGHT = np.array([30, 45, 65])
SCRATCH_COLOR = np.array([90, 95, 105])

rng = np.random.RandomState(SEED)

img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

# Fill with base metal color
img[:, :] = METAL_BASE

# --- Diamond plate pattern ---
# Classic diamond plate: raised diamonds in a staggered grid
# Each diamond cell is 16x16, staggered every other row
CELL = 16
HALF = CELL // 2

# Create the diamond plate across the whole texture
for cy in range(0, SIZE, HALF):
    for cx in range(0, SIZE, CELL):
        # Stagger every other row
        offset = HALF if (cy // HALF) % 2 == 1 else 0
        center_x = (cx + offset) % SIZE
        center_y = cy % SIZE

        # Draw a small raised diamond (about 10x5 pixels, elongated horizontally)
        diamond_w = 5
        diamond_h = 3

        for dy in range(-diamond_h, diamond_h + 1):
            for dx in range(-diamond_w, diamond_w + 1):
                # Diamond shape: |dx|/w + |dy|/h <= 1
                if abs(dx) / diamond_w + abs(dy) / diamond_h <= 1.0:
                    px = (center_x + dx) % SIZE
                    py = (center_y + dy) % SIZE

                    # Raised part - lighter
                    if abs(dx) / diamond_w + abs(dy) / diamond_h <= 0.7:
                        # Top highlight
                        if dy <= -1:
                            color = METAL_LIGHT + np.array([8, 8, 8])
                        else:
                            color = METAL_LIGHT
                    else:
                        # Edge - slightly darker than light, gives bevel
                        if dy >= 1:
                            color = METAL_BASE - np.array([5, 5, 5])
                        else:
                            color = METAL_LIGHT - np.array([5, 5, 5])

                    img[py, px] = np.clip(color, 0, 255)

# --- Groove lines (grid pattern between diamond clusters) ---
# Major grooves every 32 pixels - these are the grating seams
GROOVE_SPACING = 32

for y in range(SIZE):
    for x in range(SIZE):
        gx = x % GROOVE_SPACING
        gy = y % GROOVE_SPACING

        # Horizontal grooves (2px wide)
        if gy == 0 or gy == 1:
            img[y, x] = GROOVE_DARK
        # Vertical grooves (2px wide)
        if gx == 0 or gx == 1:
            img[y, x] = GROOVE_DARK

# --- Standing water in groove intersections ---
# Water pools at the intersections of grooves and in some groove segments
WATER_POOL_RADIUS = 4

for gy in range(0, SIZE, GROOVE_SPACING):
    for gx in range(0, SIZE, GROOVE_SPACING):
        # Water pool at each intersection
        for dy in range(-WATER_POOL_RADIUS, WATER_POOL_RADIUS + 1):
            for dx in range(-WATER_POOL_RADIUS, WATER_POOL_RADIUS + 1):
                dist = abs(dx) + abs(dy)  # Manhattan distance for pixel art feel
                if dist <= WATER_POOL_RADIUS:
                    px = (gx + dx) % SIZE
                    py = (gy + dy) % SIZE
                    if dist <= 2:
                        # Deep water center
                        img[py, px] = WATER_COLOR
                    elif dist <= 3:
                        img[py, px] = WATER_COLOR + np.array([5, 8, 10])
                    else:
                        # Water edge blending with groove
                        img[py, px] = GROOVE_DARK + np.array([0, 3, 5])

        # Small water reflection highlight (1-2 pixels)
        hx = (gx + 1) % SIZE
        hy = (gy - 1) % SIZE
        img[hy, hx] = WATER_HIGHLIGHT

# Also add water along some groove segments (not all - makes it look natural)
for gy in range(0, SIZE, GROOVE_SPACING):
    for gx in range(0, SIZE, GROOVE_SPACING):
        # Horizontal water segments (random selection based on position)
        seg_hash = (gx * 7 + gy * 13) % 5
        if seg_hash < 2:
            # Water along horizontal groove
            seg_start = gx + WATER_POOL_RADIUS + 1
            seg_end = gx + GROOVE_SPACING - WATER_POOL_RADIUS
            for sx in range(seg_start, seg_end):
                px = sx % SIZE
                for row_off in range(2):
                    py = (gy + row_off) % SIZE
                    # Vary the water color slightly
                    noise = rng.randint(-3, 4)
                    wc = np.clip(WATER_COLOR + np.array([noise, noise + 2, noise + 3]), 0, 255)
                    img[py, px] = wc

        if seg_hash == 3:
            # Water along vertical groove
            seg_start = gy + WATER_POOL_RADIUS + 1
            seg_end = gy + GROOVE_SPACING - WATER_POOL_RADIUS
            for sy in range(seg_start, seg_end):
                py = sy % SIZE
                for col_off in range(2):
                    px = (gx + col_off) % SIZE
                    noise = rng.randint(-3, 4)
                    wc = np.clip(WATER_COLOR + np.array([noise, noise + 2, noise + 3]), 0, 255)
                    img[py, px] = wc

# --- Bolt heads at regular intervals (every 64px) ---
BOLT_SPACING = 64
BOLT_RADIUS = 3

for by in range(BOLT_SPACING // 2, SIZE, BOLT_SPACING):
    for bx in range(BOLT_SPACING // 2, SIZE, BOLT_SPACING):
        for dy in range(-BOLT_RADIUS, BOLT_RADIUS + 1):
            for dx in range(-BOLT_RADIUS, BOLT_RADIUS + 1):
                dist_sq = dx * dx + dy * dy
                if dist_sq <= BOLT_RADIUS * BOLT_RADIUS:
                    px = (bx + dx) % SIZE
                    py = (by + dy) % SIZE

                    if dist_sq <= 1:
                        # Center - slot mark (dark line)
                        img[py, px] = GROOVE_DARK + np.array([10, 10, 10])
                    elif dy < 0 and dist_sq <= (BOLT_RADIUS - 1) ** 2:
                        # Top half highlight
                        img[py, px] = BOLT_HIGHLIGHT
                    elif dy >= 0 and dist_sq <= (BOLT_RADIUS - 1) ** 2:
                        # Bottom half shadow
                        img[py, px] = BOLT_COLOR - np.array([10, 10, 10])
                    else:
                        # Rim
                        img[py, px] = BOLT_COLOR

        # Bolt slot (horizontal line through center)
        for sdx in range(-1, 2):
            spx = (bx + sdx) % SIZE
            img[by, spx] = GROOVE_DARK + np.array([15, 15, 15])

# --- Surface scratches ---
NUM_SCRATCHES = 40

for _ in range(NUM_SCRATCHES):
    sx = rng.randint(0, SIZE)
    sy = rng.randint(0, SIZE)
    length = rng.randint(4, 16)
    # Mostly horizontal or diagonal scratches
    angle_choice = rng.choice([0, 1, 2])  # 0=horizontal, 1=diagonal-down, 2=diagonal-up

    for step in range(length):
        if angle_choice == 0:
            px = (sx + step) % SIZE
            py = sy % SIZE
        elif angle_choice == 1:
            px = (sx + step) % SIZE
            py = (sy + step) % SIZE
        else:
            px = (sx + step) % SIZE
            py = (sy - step) % SIZE

        # Only scratch on metal surface (not on grooves/water)
        current = img[py, px]
        brightness = int(current[0]) + int(current[1]) + int(current[2])
        if brightness > 180:  # Only scratch raised/metal areas
            img[py, px] = SCRATCH_COLOR

# --- Subtle noise/texture on metal surfaces ---
noise = rng.randint(-4, 5, size=(SIZE, SIZE, 3))
for y in range(SIZE):
    for x in range(SIZE):
        current = img[y, x]
        brightness = int(current[0]) + int(current[1]) + int(current[2])
        # Only add noise to metal surfaces, not grooves/water
        if brightness > 180:
            img[y, x] = np.clip(current.astype(np.int16) + noise[y, x], 0, 255).astype(np.uint8)

# --- Additional smaller grating holes (rectangular cutouts showing void) ---
# Between the major grooves, add smaller rectangular holes in the grating
HOLE_SIZE = 4

for gy_start in range(0, SIZE, GROOVE_SPACING):
    for gx_start in range(0, SIZE, GROOVE_SPACING):
        # Place 2 small holes in each cell
        for hi in range(2):
            hx_off = 10 + hi * 12
            hy_off = 10 + hi * 8

            for dy in range(HOLE_SIZE):
                for dx in range(HOLE_SIZE + 2):
                    px = (gx_start + hx_off + dx) % SIZE
                    py = (gy_start + hy_off + dy) % SIZE

                    # Check we're not overlapping a bolt
                    near_bolt = False
                    for by_check in range(BOLT_SPACING // 2, SIZE, BOLT_SPACING):
                        for bx_check in range(BOLT_SPACING // 2, SIZE, BOLT_SPACING):
                            if abs((px - bx_check) % SIZE) < 5 and abs((py - by_check) % SIZE) < 5:
                                near_bolt = True

                    if not near_bolt:
                        if dx == 0 or dx == HOLE_SIZE + 1 or dy == 0 or dy == HOLE_SIZE - 1:
                            # Hole edge
                            img[py, px] = GROOVE_DARK + np.array([5, 5, 5])
                        else:
                            # Void beneath - very dark with slight water tint
                            darkness = rng.randint(0, 3)
                            img[py, px] = np.clip(
                                np.array([15 + darkness, 18 + darkness, 28 + darkness]),
                                0, 255
                            )

# Save output
output = Image.fromarray(img, 'RGB')
output.save('../../docs/assets/rooms/room5_floor.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
