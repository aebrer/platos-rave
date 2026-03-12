"""
Room 7 Floor Texture — "Traps" (Gothic Circus ring floor)
Dark polished wood stage floor with painted circus ring markings,
trapdoor outlines, sawdust scatter, and gothic theatrical flair.
256x256 tileable pixel art.
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 7777

rng = np.random.RandomState(SEED)

# Palette
WOOD_DARK = np.array([55, 35, 20], dtype=np.uint8)
WOOD_MID = np.array([65, 40, 25], dtype=np.uint8)
WOOD_LIGHT = np.array([50, 30, 18], dtype=np.uint8)
PLANK_SEAM = np.array([30, 18, 10], dtype=np.uint8)
GOLD_PAINT = np.array([180, 150, 60], dtype=np.uint8)
GOLD_DIM = np.array([140, 115, 45], dtype=np.uint8)
SAWDUST = np.array([170, 150, 110], dtype=np.uint8)
TRAPDOOR_SEAM = np.array([25, 15, 8], dtype=np.uint8)
HINGE = np.array([100, 90, 70], dtype=np.uint8)
SCUFF = np.array([75, 50, 30], dtype=np.uint8)

img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)


# --- Helper: tileable noise via wrapping ---
def wrap(v):
    return v % SIZE


def tileable_noise(size, scale, seed=0):
    """Generate tileable Perlin-ish noise using cosine interpolation."""
    r = np.random.RandomState(seed)
    grid = scale
    base = r.rand(grid, grid)
    # Tile the base so interpolation wraps
    base_tiled = np.tile(base, (2, 2))
    out = np.zeros((size, size), dtype=np.float64)
    for y in range(size):
        for x in range(size):
            fx = (x / size) * grid
            fy = (y / size) * grid
            ix = int(fx) % grid
            iy = int(fy) % grid
            dx = fx - int(fx)
            dy = fy - int(fy)
            # Cosine interpolation
            dx = (1 - np.cos(dx * np.pi)) / 2
            dy = (1 - np.cos(dy * np.pi)) / 2
            v00 = base_tiled[iy, ix]
            v10 = base_tiled[iy, ix + 1]
            v01 = base_tiled[iy + 1, ix]
            v11 = base_tiled[iy + 1, ix + 1]
            v0 = v00 * (1 - dx) + v10 * dx
            v1 = v01 * (1 - dx) + v11 * dx
            out[y, x] = v0 * (1 - dy) + v1 * dy
    return out


# --- 1. Wood plank base ---
# Horizontal planks, ~32px tall each (8 planks = 256)
PLANK_H = 32
NUM_PLANKS = SIZE // PLANK_H

# Generate wood grain noise (tileable)
grain_noise = tileable_noise(SIZE, 16, seed=100)
color_noise = tileable_noise(SIZE, 8, seed=200)

# Wood colors per plank (cycle through dark shades)
plank_colors = [WOOD_DARK, WOOD_MID, WOOD_LIGHT, WOOD_DARK, WOOD_MID, WOOD_DARK, WOOD_LIGHT, WOOD_MID]

for py in range(NUM_PLANKS):
    y0 = py * PLANK_H
    base_col = plank_colors[py % len(plank_colors)].astype(np.float64)
    for y in range(y0, y0 + PLANK_H):
        for x in range(SIZE):
            yw = wrap(y)
            xw = wrap(x)
            # Wood grain: horizontal streaks
            grain = grain_noise[yw, xw]
            variation = (grain - 0.5) * 20
            # Color variation per plank
            cv = (color_noise[yw, xw] - 0.5) * 10
            c = base_col + variation + cv
            img[yw, xw] = np.clip(c, 0, 255).astype(np.uint8)

# --- 2. Plank seams (horizontal lines) ---
for py in range(NUM_PLANKS):
    y_seam = (py * PLANK_H) % SIZE
    for x in range(SIZE):
        # Main seam line
        img[y_seam, x] = PLANK_SEAM
        # Slight shadow below
        y_below = wrap(y_seam + 1)
        c = img[y_below, x].astype(np.float64) * 0.7
        img[y_below, x] = np.clip(c, 0, 255).astype(np.uint8)

# --- 3. Vertical plank stagger (offset joins) ---
# Each plank row has a vertical join at a staggered position
plank_joins = [64, 192, 96, 160, 48, 208, 128, 80]
for py in range(NUM_PLANKS):
    x_join = plank_joins[py % len(plank_joins)]
    y0 = py * PLANK_H
    for dy in range(1, PLANK_H - 1):  # skip seam rows
        y = wrap(y0 + dy)
        img[y, wrap(x_join)] = PLANK_SEAM


# --- 4. Circus ring marking (curved gold arc) ---
# Ring center is at tile center — since we tile, we draw the arc segment
# that appears in this tile. Ring radius ~200px (larger than tile, so we
# see an arc segment).
CX, CY = SIZE // 2, SIZE // 2
RING_R = 200
RING_W = 4  # line width

for y in range(SIZE):
    for x in range(SIZE):
        # Distance from center
        dx = x - CX
        dy = y - CY
        dist = np.sqrt(dx * dx + dy * dy)
        # Ring border
        if abs(dist - RING_R) < RING_W:
            # Slight variation for worn look
            fade = 0.7 + 0.3 * grain_noise[y, x]
            c = GOLD_PAINT.astype(np.float64) * fade
            img[y, x] = np.clip(c, 0, 255).astype(np.uint8)
        # Inner decorative ring (thinner)
        elif abs(dist - (RING_R - 12)) < 1.5:
            fade = 0.6 + 0.4 * grain_noise[y, x]
            c = GOLD_DIM.astype(np.float64) * fade
            img[y, x] = np.clip(c, 0, 255).astype(np.uint8)


# --- 5. Trapdoor outlines ---
# Two trapdoors: rectangular seams in the wood
trapdoors = [
    (24, 48, 80, 56),    # (x, y, w, h) — left trapdoor
    (152, 160, 72, 48),  # right trapdoor
]

for tx, ty, tw, th in trapdoors:
    # Draw rectangular seam
    for i in range(tw):
        # Top edge
        img[wrap(ty), wrap(tx + i)] = TRAPDOOR_SEAM
        img[wrap(ty + 1), wrap(tx + i)] = TRAPDOOR_SEAM
        # Bottom edge
        img[wrap(ty + th), wrap(tx + i)] = TRAPDOOR_SEAM
        img[wrap(ty + th - 1), wrap(tx + i)] = TRAPDOOR_SEAM
    for j in range(th):
        # Left edge
        img[wrap(ty + j), wrap(tx)] = TRAPDOOR_SEAM
        img[wrap(ty + j), wrap(tx + 1)] = TRAPDOOR_SEAM
        # Right edge
        img[wrap(ty + j), wrap(tx + tw)] = TRAPDOOR_SEAM
        img[wrap(ty + j), wrap(tx + tw - 1)] = TRAPDOOR_SEAM

    # Recessed interior (slightly darker)
    for j in range(2, th - 2):
        for i in range(2, tw - 2):
            yy = wrap(ty + j)
            xx = wrap(tx + i)
            c = img[yy, xx].astype(np.float64) * 0.85
            img[yy, xx] = np.clip(c, 0, 255).astype(np.uint8)

    # Hinges (2 per trapdoor, on one long edge)
    hinge_positions = [tw // 3, 2 * tw // 3]
    for hx in hinge_positions:
        for ddy in range(-2, 3):
            for ddx in range(-1, 2):
                yy = wrap(ty + ddy)
                xx = wrap(tx + hx + ddx)
                img[yy, xx] = HINGE
        # Hinge pin (bright dot)
        img[wrap(ty), wrap(tx + hx)] = np.array([130, 120, 95], dtype=np.uint8)

    # Handle/pull ring on trapdoor (small circle)
    handle_cx = tx + tw // 2
    handle_cy = ty + th // 2
    for ddy in range(-3, 4):
        for ddx in range(-3, 4):
            d = np.sqrt(ddy * ddy + ddx * ddx)
            if 2 < d < 3.5:
                yy = wrap(handle_cy + ddy)
                xx = wrap(handle_cx + ddx)
                img[yy, xx] = HINGE


# --- 6. Painted star marking ---
# Small 5-pointed star in gold, near center
STAR_CX, STAR_CY = 128, 128
STAR_R_OUTER = 16
STAR_R_INNER = 7

def point_in_star(px, py, cx, cy, r_outer, r_inner, points=5):
    """Check if point is inside a star polygon."""
    dx = px - cx
    dy = py - cy
    angle = np.arctan2(dy, dx)
    dist = np.sqrt(dx * dx + dy * dy)
    # Angle of the nearest star arm
    seg_angle = 2 * np.pi / points
    half_seg = seg_angle / 2
    rel_angle = angle % seg_angle
    # Interpolate between outer and inner radius
    if rel_angle < half_seg:
        t = rel_angle / half_seg
    else:
        t = (seg_angle - rel_angle) / half_seg
    threshold = r_inner + (r_outer - r_inner) * t
    return dist < threshold

for y in range(STAR_CY - STAR_R_OUTER - 2, STAR_CY + STAR_R_OUTER + 2):
    for x in range(STAR_CX - STAR_R_OUTER - 2, STAR_CX + STAR_R_OUTER + 2):
        yw = wrap(y)
        xw = wrap(x)
        if point_in_star(x, y, STAR_CX, STAR_CY, STAR_R_OUTER, STAR_R_INNER):
            fade = 0.75 + 0.25 * grain_noise[yw, xw]
            c = GOLD_PAINT.astype(np.float64) * fade
            img[yw, xw] = np.clip(c, 0, 255).astype(np.uint8)


# --- 7. Directional arrows ---
# Small painted arrows pointing toward trapdoors
def draw_arrow(img, cx, cy, direction, length=12, color=GOLD_DIM):
    """Draw a simple pixel arrow. direction: 'up','down','left','right'"""
    dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[direction]
    # Shaft
    for i in range(length):
        yy = wrap(cy + dy * i)
        xx = wrap(cx + dx * i)
        img[yy, xx] = color
        # Thicken shaft
        if dx == 0:
            img[yy, wrap(xx + 1)] = color
        else:
            img[wrap(yy + 1), xx] = color
    # Arrowhead
    tip_x = cx + dx * length
    tip_y = cy + dy * length
    for s in range(5):
        if dx == 0:  # vertical arrow
            img[wrap(tip_y), wrap(tip_x - s)] = color
            img[wrap(tip_y), wrap(tip_x + s)] = color
            img[wrap(tip_y + dy), wrap(tip_x - max(0, s - 1))] = color
            img[wrap(tip_y + dy), wrap(tip_x + max(0, s - 1))] = color
        else:  # horizontal arrow
            img[wrap(tip_y - s), wrap(tip_x)] = color
            img[wrap(tip_y + s), wrap(tip_x)] = color
            img[wrap(tip_y - max(0, s - 1)), wrap(tip_x + dx)] = color
            img[wrap(tip_y + max(0, s - 1)), wrap(tip_x + dx)] = color

draw_arrow(img, 60, 36, 'down')   # pointing at left trapdoor
draw_arrow(img, 188, 148, 'down')  # pointing at right trapdoor


# --- 8. "TRAP" warning text (pixel-style) ---
# Small blocky warning marks near trapdoors — just simple "!" marks
def draw_exclamation(img, cx, cy, color=GOLD_PAINT):
    """Draw a small pixel exclamation mark."""
    for dy in range(6):
        img[wrap(cy + dy), wrap(cx)] = color
        img[wrap(cy + dy), wrap(cx + 1)] = color
    # dot
    img[wrap(cy + 8), wrap(cx)] = color
    img[wrap(cy + 8), wrap(cx + 1)] = color

draw_exclamation(img, 108, 52)
draw_exclamation(img, 230, 164)


# --- 9. Sawdust scatter ---
num_sawdust = 1800
sawdust_x = rng.randint(0, SIZE, num_sawdust)
sawdust_y = rng.randint(0, SIZE, num_sawdust)
for i in range(num_sawdust):
    x = sawdust_x[i]
    y = sawdust_y[i]
    # Vary the sawdust color slightly
    variation = rng.randint(-15, 15, 3)
    c = np.clip(SAWDUST.astype(np.int16) + variation, 0, 255).astype(np.uint8)
    # Some are single pixels, some are 2px clusters
    img[y, x] = c
    if rng.random() < 0.3:
        img[y, wrap(x + 1)] = c
    if rng.random() < 0.15:
        img[wrap(y + 1), x] = c


# --- 10. Scuff marks ---
num_scuffs = 40
for _ in range(num_scuffs):
    sx = rng.randint(0, SIZE)
    sy = rng.randint(0, SIZE)
    length = rng.randint(4, 16)
    angle = rng.uniform(0, 2 * np.pi)
    for t in range(length):
        xx = wrap(sx + int(t * np.cos(angle)))
        yy = wrap(sy + int(t * np.sin(angle)))
        # Blend scuff with existing color
        c = img[yy, xx].astype(np.float64) * 0.6 + SCUFF.astype(np.float64) * 0.4
        img[yy, xx] = np.clip(c, 0, 255).astype(np.uint8)


# --- 11. Gothic border decorations ---
# Small repeating gothic arch pattern along edges (tileable)
ARCH_SPACING = 32
ARCH_H = 10

for ax in range(0, SIZE, ARCH_SPACING):
    # Top edge arches
    for dx in range(ARCH_SPACING):
        x = wrap(ax + dx)
        # Gothic pointed arch shape
        center = ARCH_SPACING // 2
        dist_from_center = abs(dx - center)
        arch_y = int(ARCH_H * (1 - (dist_from_center / center) ** 0.7))
        if arch_y > 0:
            for dy in range(arch_y):
                if dy == arch_y - 1 or dx == 0 or dx == ARCH_SPACING - 1:
                    # Only draw the outline
                    yy = wrap(dy)
                    fade = 0.5 + 0.5 * grain_noise[yy, x]
                    c = GOLD_DIM.astype(np.float64) * fade * 0.7
                    img[yy, x] = np.clip(c, 0, 255).astype(np.uint8)

    # Bottom edge arches (inverted)
    for dx in range(ARCH_SPACING):
        x = wrap(ax + dx)
        center = ARCH_SPACING // 2
        dist_from_center = abs(dx - center)
        arch_y = int(ARCH_H * (1 - (dist_from_center / center) ** 0.7))
        if arch_y > 0:
            for dy in range(arch_y):
                if dy == arch_y - 1 or dx == 0 or dx == ARCH_SPACING - 1:
                    yy = wrap(SIZE - 1 - dy)
                    fade = 0.5 + 0.5 * grain_noise[yy, x]
                    c = GOLD_DIM.astype(np.float64) * fade * 0.7
                    img[yy, x] = np.clip(c, 0, 255).astype(np.uint8)


# --- Save ---
out = Image.fromarray(img, 'RGB')
out.save('../../docs/assets/rooms/room7_floor.png')
print(f"Saved output.png: {out.size[0]}x{out.size[1]}")
