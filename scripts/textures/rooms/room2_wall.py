"""
Room 2 Wall Texture — "The Cloister of Confidence" (Container Store Warehouse)
Industrial warehouse behind Room 1's retail showroom.
Heavy-duty metal shelving, cardboard boxes, plastic bins, dim fluorescents.
256x256, tileable, pixel art dungeon-crawler aesthetic.
"""

import numpy as np
from PIL import Image

W, H = 256, 256
BAY = 64  # each bay is 64x64

# Palette
SHELF_UPRIGHT = (80, 85, 80)
SHELF_UPRIGHT_HI = (95, 100, 95)
SHELF_UPRIGHT_LO = (60, 65, 60)
SHELF_BEAM = (90, 85, 80)
SHELF_BEAM_HI = (105, 100, 95)
SHELF_BEAM_LO = (70, 65, 60)
CARDBOARD_1 = (165, 140, 100)
CARDBOARD_2 = (155, 130, 90)
CARDBOARD_3 = (175, 150, 110)
CARDBOARD_DARK = (130, 110, 75)
CARDBOARD_TAPE = (190, 175, 130)
BIN_1 = (70, 80, 95)
BIN_2 = (60, 70, 85)
BIN_LID = (80, 90, 105)
CONCRETE_BASE = (110, 108, 105)
CONCRETE_LIGHT = (118, 116, 113)
CONCRETE_DARK = (95, 93, 90)
CONCRETE_MORTAR = (125, 122, 118)
LIGHT_STRIP = (200, 190, 150)
LIGHT_GLOW = (180, 172, 140)
LIGHT_DIM = (160, 153, 125)
FLOOR_SHADOW = (50, 50, 48)

img = np.zeros((H, W, 3), dtype=np.uint8)


def set_px(arr, x, y, color):
    arr[y % H, x % W] = color


def fill_rect(arr, x0, y0, w, h, color):
    for dy in range(h):
        for dx in range(w):
            set_px(arr, x0 + dx, y0 + dy, color)


def draw_concrete_bg(arr, x0, y0, bw, bh):
    """Draw subtle concrete block pattern in a region."""
    # Fill base
    fill_rect(arr, x0, y0, bw, bh, CONCRETE_BASE)
    # Concrete block pattern: blocks are ~16x8 with mortar lines
    block_w, block_h = 16, 8
    for by in range(bh // block_h + 1):
        for bx in range(bw // block_w + 1):
            px = x0 + bx * block_w
            py = y0 + by * block_h
            # Offset every other row
            offset = (block_w // 2) if (by % 2 == 1) else 0
            px += offset
            # Mortar lines (horizontal)
            for dx in range(block_w):
                set_px(arr, px + dx, py, CONCRETE_MORTAR)
            # Mortar lines (vertical)
            for dy in range(block_h):
                set_px(arr, px, py + dy, CONCRETE_MORTAR)
            # Slight variation in block color
            rng_val = ((bx * 7 + by * 13) % 3)
            if rng_val == 0:
                block_col = CONCRETE_LIGHT
            elif rng_val == 1:
                block_col = CONCRETE_DARK
            else:
                block_col = CONCRETE_BASE
            fill_rect(arr, px + 1, py + 1, block_w - 2, block_h - 2, block_col)


def draw_cardboard_box(arr, x, y, w, h, variant=0):
    """Draw a cardboard box with tape and shading."""
    colors = [CARDBOARD_1, CARDBOARD_2, CARDBOARD_3]
    base = colors[variant % 3]
    fill_rect(arr, x, y, w, h, base)
    # Top edge highlight
    darker = (max(0, base[0] - 25), max(0, base[1] - 25), max(0, base[2] - 20))
    for dx in range(w):
        set_px(arr, x + dx, y, darker)
        set_px(arr, x + dx, y + h - 1, darker)
    for dy in range(h):
        set_px(arr, x, y + dy, darker)
        set_px(arr, x + w - 1, y + dy, darker)
    # Tape strip across top (horizontal)
    if h > 6:
        tape_y = y + 2
        for dx in range(1, w - 1):
            set_px(arr, x + dx, tape_y, CARDBOARD_TAPE)
            set_px(arr, x + dx, tape_y + 1, CARDBOARD_TAPE)
    # Center seam
    if w > 6:
        cx = x + w // 2
        for dy in range(1, h - 1):
            set_px(arr, cx, y + dy, darker)


def draw_bin(arr, x, y, w, h, variant=0):
    """Draw a plastic storage bin."""
    colors = [BIN_1, BIN_2]
    base = colors[variant % 2]
    fill_rect(arr, x, y, w, h, base)
    # Lid
    fill_rect(arr, x, y, w, 2, BIN_LID)
    # Border
    lighter = (min(255, base[0] + 15), min(255, base[1] + 15), min(255, base[2] + 15))
    darker = (max(0, base[0] - 20), max(0, base[1] - 20), max(0, base[2] - 20))
    for dx in range(w):
        set_px(arr, x + dx, y + h - 1, darker)
    for dy in range(h):
        set_px(arr, x, y + dy, darker)
        set_px(arr, x + w - 1, y + dy, darker)
    # Handle cutout
    if w > 8:
        hx = x + w // 2 - 2
        hy = y + h // 2
        for dx in range(4):
            set_px(arr, hx + dx, hy, lighter)


def draw_cross_brace(arr, x0, y0, x1, y1, color):
    """Draw a diagonal cross-brace line using Bresenham's."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    cx, cy = x0, y0
    while True:
        set_px(arr, cx, cy, color)
        if cx == x1 and cy == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            cx += sx
        if e2 < dx:
            err += dx
            cy += sy


def draw_bay(arr, bx, by):
    """Draw one 64x64 bay of warehouse shelving."""
    ox = bx * BAY
    oy = by * BAY

    # --- Concrete wall background ---
    draw_concrete_bg(arr, ox, oy, BAY, BAY)

    # --- Light strip at top ---
    fill_rect(arr, ox, oy, BAY, 3, LIGHT_DIM)
    fill_rect(arr, ox + 4, oy, BAY - 8, 2, LIGHT_GLOW)
    fill_rect(arr, ox + 12, oy, BAY - 24, 1, LIGHT_STRIP)

    # --- Shelf uprights (4px wide, at edges of bay) ---
    upright_w = 4
    # Left upright
    for dy in range(3, BAY):
        fill_rect(arr, ox, oy + dy, upright_w, 1, SHELF_UPRIGHT)
        set_px(arr, ox, oy + dy, SHELF_UPRIGHT_LO)
        set_px(arr, ox + upright_w - 1, oy + dy, SHELF_UPRIGHT_HI)
    # Right upright (will overlap with next bay's left, creating seamless tiling)
    for dy in range(3, BAY):
        fill_rect(arr, ox + BAY - upright_w, oy + dy, upright_w, 1, SHELF_UPRIGHT)
        set_px(arr, ox + BAY - upright_w, oy + dy, SHELF_UPRIGHT_LO)
        set_px(arr, ox + BAY - 1, oy + dy, SHELF_UPRIGHT_HI)

    # Upright holes (industrial patterning)
    for dy in range(8, BAY, 6):
        set_px(arr, ox + 1, oy + dy, SHELF_UPRIGHT_LO)
        set_px(arr, ox + 2, oy + dy, SHELF_UPRIGHT_LO)
        set_px(arr, ox + BAY - 3, oy + dy, SHELF_UPRIGHT_LO)
        set_px(arr, ox + BAY - 2, oy + dy, SHELF_UPRIGHT_LO)

    # --- Cross-bracing between uprights (diagonal) ---
    brace_color = (75, 78, 75)
    # X-brace in the back, behind items (draw before shelves/items)
    draw_cross_brace(arr, ox + upright_w, oy + 5, ox + BAY - upright_w - 1, oy + BAY - 2, brace_color)
    draw_cross_brace(arr, ox + BAY - upright_w - 1, oy + 5, ox + upright_w, oy + BAY - 2, brace_color)

    # --- Horizontal shelf beams ---
    beam_h = 3
    shelf_ys = [14, 30, 46]  # three shelf levels within 64px bay

    for sy in shelf_ys:
        fill_rect(arr, ox + upright_w, oy + sy, BAY - 2 * upright_w, beam_h, SHELF_BEAM)
        # Highlight top edge
        for dx in range(upright_w, BAY - upright_w):
            set_px(arr, ox + dx, oy + sy, SHELF_BEAM_HI)
        # Shadow bottom edge
        for dx in range(upright_w, BAY - upright_w):
            set_px(arr, ox + dx, oy + sy + beam_h - 1, SHELF_BEAM_LO)

    # --- Items on shelves ---
    # Deterministic pseudo-random based on bay position
    seed = bx * 7 + by * 13

    # Shelf regions: between beam tops
    # Region 1: oy+3 to oy+14 (top to first shelf)
    # Region 2: oy+17 to oy+30 (after first shelf to second)
    # Region 3: oy+33 to oy+46 (after second to third)
    # Region 4: oy+49 to oy+62 (after third to bottom)

    regions = [
        (oy + 4, 10),    # above first shelf
        (oy + 17, 13),   # between first and second
        (oy + 33, 13),   # between second and third
        (oy + 49, 13),   # below third shelf
    ]

    item_x_start = ox + upright_w + 1
    item_width = BAY - 2 * upright_w - 2  # available width

    for ri, (ry, rh) in enumerate(regions):
        item_seed = seed + ri * 3
        # Place 2-3 items per shelf
        item_count = 2 + (item_seed % 2)
        cx = item_x_start
        remaining_w = item_width

        for ii in range(item_count):
            if remaining_w < 8:
                break
            iw = min(remaining_w, 10 + (item_seed + ii * 5) % 12)
            ih = min(rh - 1, 7 + (item_seed + ii * 3) % 5)
            iy = ry + (rh - ih)  # sit on shelf

            # Alternate boxes and bins
            if (item_seed + ii) % 3 == 0:
                draw_bin(arr, cx, iy, iw, ih, variant=(item_seed + ii))
            else:
                draw_cardboard_box(arr, cx, iy, iw, ih, variant=(item_seed + ii))

            cx += iw + 1
            remaining_w -= (iw + 1)

    # --- Shadow gradient at bottom ---
    for dx in range(upright_w, BAY - upright_w):
        set_px(arr, ox + dx, oy + BAY - 2, FLOOR_SHADOW)
        set_px(arr, ox + dx, oy + BAY - 1, FLOOR_SHADOW)


# --- Generate all bays ---
for by in range(H // BAY):
    for bx in range(W // BAY):
        draw_bay(img, bx, by)

# --- Add overall dim lighting effect (subtle vignette per bay) ---
# Darken edges slightly to enhance warehouse feel
for y in range(H):
    for x in range(W):
        # Local position within bay
        lx = x % BAY
        ly = y % BAY
        # Distance from center of bay (normalized)
        dx = abs(lx - BAY // 2) / (BAY // 2)
        dy = abs(ly - BAY // 2) / (BAY // 2)
        # Subtle edge darkening
        edge_factor = max(0, (dx * 0.15 + dy * 0.1) - 0.05)
        r, g, b = img[y, x]
        img[y, x] = (
            max(0, int(r * (1 - edge_factor))),
            max(0, int(g * (1 - edge_factor))),
            max(0, int(b * (1 - edge_factor))),
        )

# --- Add noise/grit ---
rng = np.random.RandomState(42)
noise = rng.randint(-8, 9, size=(H, W, 3))
img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# --- Save ---
out = Image.fromarray(img, 'RGB')
out.save('../../docs/assets/rooms/room2_wall.png')
print(f"Saved output.png: {out.size[0]}x{out.size[1]}")
