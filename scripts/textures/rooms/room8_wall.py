"""
Room 8 Wall Texture — "The Final Deception" (The Cantainer Store)
Generates a tileable 256x256 pixel art wall texture that TRIES to look like
Room 1's retail shelving but fails in unsettling, uncanny ways.

Based on Room 1's structure but with subtle wrongness:
- Sickly yellow-green color shift across everything
- Some shelves slightly tilted (not perfectly horizontal)
- Wrong-colored bins (red, purple) among the normal ones
- Price strips teal-green instead of orange
- Fluorescent light uneven/flickery
- Overall slightly darker — older, tired lighting
"""

import numpy as np
from PIL import Image
import os

SIZE = 256
UNIT = 64
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../docs/assets/rooms/room8_wall.png")

# --- Palette (Room 1 but shifted wrong) ---
WALL = np.array([215, 215, 200], dtype=np.uint8)  # slightly yellow vs Room 1's (220, 215, 210)
SHELF_DARK = np.array([95, 95, 75], dtype=np.uint8)  # green-gray instead of warm gray
SHELF_HIGHLIGHT = np.array([170, 170, 150], dtype=np.uint8)  # matching green shift
FLUORESCENT = np.array([230, 235, 200], dtype=np.uint8)  # green-tinted instead of clean white
UPRIGHT_COLOR = np.array([145, 145, 135], dtype=np.uint8)  # slightly off
PRICE_STRIP = np.array([80, 180, 120], dtype=np.uint8)  # teal-green instead of orange
SHADOW_DARK = np.array([55, 55, 45], dtype=np.uint8)  # greenish shadow

# Normal containers — same blues/grays but with a yellow-green tint
CONTAINER_COLORS = [
    np.array([185, 208, 215], dtype=np.uint8),  # slightly off blue
    np.array([198, 200, 195], dtype=np.uint8),  # gray with green tint
    np.array([220, 218, 200], dtype=np.uint8),  # yellowed cream
    np.array([205, 212, 210], dtype=np.uint8),  # muted blue-gray
    np.array([175, 192, 200], dtype=np.uint8),  # dusty blue
]

# WRONG containers — these should NOT be here
WRONG_COLORS = [
    np.array([180, 50, 50], dtype=np.uint8),   # alarming red
    np.array([140, 60, 160], dtype=np.uint8),   # unsettling purple
]


def blend(c1, c2, t):
    t = float(np.clip(t, 0.0, 1.0))
    return (c1.astype(np.float64) * (1.0 - t) + c2.astype(np.float64) * t).astype(np.uint8)


def lighten(c, amount=30):
    return np.clip(c.astype(np.int16) + amount, 0, 255).astype(np.uint8)


def darken(c, amount=30):
    return np.clip(c.astype(np.int16) - amount, 0, 255).astype(np.uint8)


def hash_val(a, b, seed=0):
    n = a * 374761393 + b * 668265263 + seed * 1274126177
    n = (n ^ (n >> 13)) * 1274126177
    n = n ^ (n >> 16)
    return n & 0xFFFFFF


def draw_shelf_bar(img, ox, oy, y_start, col, row, shelf_idx):
    """Draw a horizontal shelf bar — but sometimes slightly tilted."""
    # Determine if this shelf is crooked (about 1 in 3 shelves)
    tilt = 0
    h = hash_val(col, row, shelf_idx + 777)
    if h % 3 == 0:
        tilt = 1 if (h % 2 == 0) else -1  # 1px tilt across the bay

    for dx in range(2, UNIT - 2):
        # Calculate tilt offset: linearly interpolate across the shelf width
        t = dx / float(UNIT)
        tilt_offset = int(round(tilt * (t - 0.5)))

        y = y_start + tilt_offset
        img[(oy + y) % SIZE, (ox + dx) % SIZE] = SHELF_DARK
        img[(oy + y + 1) % SIZE, (ox + dx) % SIZE] = SHELF_DARK
        img[(oy + y + 2) % SIZE, (ox + dx) % SIZE] = SHELF_HIGHLIGHT


def draw_container(img, ox, oy, cx, cy, width, height, color):
    """
    Draw a single container/bin with 3D shading.
    Same structure as Room 1 but the colors come from the shifted palette.
    """
    if width < 3 or height < 5:
        return

    top_color = lighten(color, 40)
    front_color = color
    left_color = lighten(color, 20)
    right_color = darken(color, 25)
    bottom_shadow = darken(color, 50)

    for dy in range(height):
        for dx in range(width):
            px = (ox + cx + dx) % SIZE
            py = (oy + cy + dy) % SIZE

            if dy < 3:
                c = top_color
                if dx == 0:
                    c = lighten(color, 25)
                elif dx == width - 1:
                    c = lighten(color, 15)
            elif dy == height - 1:
                c = bottom_shadow
            else:
                if dx == 0:
                    c = left_color
                elif dx == width - 1:
                    c = right_color
                else:
                    c = front_color

            img[py, px] = c


def draw_containers_on_shelf(img, ox, oy, shelf_top_y, shelf_bar_y, col, row, shelf_idx):
    """
    Draw 2-3 containers on a shelf.
    One container per bay has a chance of being a WRONG color.
    Some containers are slightly misshapen (irregular widths).
    """
    available_h = shelf_bar_y - shelf_top_y
    inner_left = 3
    inner_right = UNIT - 3
    inner_w = inner_right - inner_left

    n_containers = 2 + (hash_val(col, row, shelf_idx + 100) % 2)

    gap = 2
    total_gap = gap * (n_containers - 1)

    # Generate widths — slightly more irregular than Room 1
    widths = []
    remaining_w = inner_w - total_gap
    for i in range(n_containers):
        if i == n_containers - 1:
            w = remaining_w
        else:
            min_w = max(6, remaining_w // (n_containers - i) - 8)  # more variation
            max_w = remaining_w // (n_containers - i) + 6
            max_w = min(max_w, remaining_w - 6 * (n_containers - i - 1))
            w = min_w + (hash_val(col, row, shelf_idx * 10 + i + 200) % max(1, max_w - min_w))
            remaining_w -= w
        widths.append(w)

    # Decide which container (if any) is WRONG in this bay
    wrong_idx = -1
    wrong_hash = hash_val(col, row, shelf_idx + 500)
    # About 1 in 3 bays gets a wrong-colored container
    if wrong_hash % 3 == 0:
        wrong_idx = wrong_hash % n_containers

    cx = inner_left
    for i in range(n_containers):
        w = widths[i]
        h_variation = hash_val(col, row, shelf_idx * 10 + i + 300) % 7  # more height variation
        h = available_h - h_variation
        if h < 5:
            h = 5

        container_y = shelf_top_y + (available_h - h)

        # Pick color — wrong color for the chosen container
        if i == wrong_idx:
            color = WRONG_COLORS[hash_val(col, row, shelf_idx + i + 600) % len(WRONG_COLORS)]
        else:
            color_idx = (col * 3 + row * 7 + shelf_idx * 5 + i) % len(CONTAINER_COLORS)
            color = CONTAINER_COLORS[color_idx]

        draw_container(img, ox, oy, cx, container_y, w, h, color)

        cx += w + gap


def generate():
    img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    img[:, :] = WALL

    COLS = SIZE // UNIT
    ROWS = SIZE // UNIT

    for row in range(ROWS):
        for col in range(COLS):
            ox = col * UNIT
            oy = row * UNIT

            # === Fluorescent light strip (rows 0-4) — uneven/flickery ===
            flicker_hash = hash_val(col, row, 999)
            # Some bays have dimmer lights, some have brighter spots
            brightness_mod = 1.0
            if flicker_hash % 4 == 0:
                brightness_mod = 0.6  # dim section — bulb going bad
            elif flicker_hash % 4 == 1:
                brightness_mod = 1.15  # slightly too bright

            for dy in range(5):
                if dy <= 2:
                    brightness = [1.0, 0.9, 0.7][dy] * brightness_mod
                else:
                    brightness = [0.4, 0.15][dy - 3] * brightness_mod
                brightness = min(brightness, 1.0)
                c = blend(WALL, FLUORESCENT, brightness)

                # Add per-pixel flicker within the strip
                for dx in range(UNIT):
                    pixel_hash = hash_val(dx + col * UNIT, dy + row * UNIT, 888)
                    flicker = (pixel_hash % 5) - 2  # -2 to +2
                    fc = np.clip(c.astype(np.int16) + flicker, 0, 255).astype(np.uint8)
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = fc

            # === Wall background (rows 5-10) ===
            for dy in range(5, 11):
                for dx in range(UNIT):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = WALL

            # === Shelf 1 (rows 11-30) — possibly tilted ===
            shelf1_bar_y = 28
            draw_shelf_bar(img, ox, oy, shelf1_bar_y, col, row, 0)
            draw_containers_on_shelf(img, ox, oy, 11, shelf1_bar_y, col, row, 0)

            # === Shelf 2 (rows 31-50) — possibly tilted ===
            shelf2_bar_y = 48
            draw_shelf_bar(img, ox, oy, shelf2_bar_y, col, row, 1)
            draw_containers_on_shelf(img, ox, oy, 31, shelf2_bar_y, col, row, 1)

            # === Bottom shelf edge + price strip (rows 51-60) ===
            draw_shelf_bar(img, ox, oy, 51, col, row, 2)
            draw_containers_on_shelf(img, ox, oy, 54, 58, col, row, 2)

            # Price strip — teal-green instead of orange
            for dy in [59, 60]:
                for dx in range(3, UNIT - 3):
                    # Slight color variation along the strip (uneven printing)
                    ph = hash_val(dx + col * UNIT, dy, 444)
                    variation = (ph % 7) - 3
                    pc = np.clip(PRICE_STRIP.astype(np.int16) + variation, 0, 255).astype(np.uint8)
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = pc

            # === Gap/shadow (rows 61-63) ===
            for dy in range(61, 64):
                t = (dy - 61) / 3.0
                c = blend(SHADOW_DARK, WALL, t * 0.6)
                for dx in range(UNIT):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = c

            # === Metal shelf uprights — same structure but slightly off color ===
            for dy in range(UNIT):
                py = (oy + dy) % SIZE
                img[py, (ox + 0) % SIZE] = darken(UPRIGHT_COLOR, 10)
                img[py, (ox + 1) % SIZE] = UPRIGHT_COLOR
                img[py, (ox + UNIT - 2) % SIZE] = UPRIGHT_COLOR
                img[py, (ox + UNIT - 1) % SIZE] = darken(UPRIGHT_COLOR, 10)

    # --- Noise — slightly more than Room 1 for that grungy feel ---
    rng = np.random.RandomState(87)  # different seed than Room 1
    tile_noise = rng.randint(-3, 4, size=(UNIT, UNIT, 3))  # -3 to +3 vs Room 1's -2 to +2
    noise = np.tile(tile_noise, (ROWS, COLS, 1))
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # --- Overall darkening pass — lights are older here ---
    img = np.clip(img.astype(np.int16) - 8, 0, 255).astype(np.uint8)

    out = Image.fromarray(img, 'RGB')
    out.save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    generate()
