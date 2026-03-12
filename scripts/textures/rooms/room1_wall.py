"""
Room 1 Wall Texture — "The Container Store"
Generates a tileable 256x256 pixel art wall texture depicting retail shelving
with organized containers/bins under fluorescent lighting.

v3: Complete rewrite for clear retail shelving read. Each 64x64 bay has:
fluorescent strip, wall gap, two shelves with bins, bottom shelf with price strip.
"""

import numpy as np
from PIL import Image
import os

SIZE = 256
UNIT = 64
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.png")

# --- Palette ---
WALL = np.array([220, 215, 210], dtype=np.uint8)
SHELF_DARK = np.array([100, 90, 80], dtype=np.uint8)
SHELF_HIGHLIGHT = np.array([180, 170, 160], dtype=np.uint8)
FLUORESCENT = np.array([240, 240, 220], dtype=np.uint8)
UPRIGHT_COLOR = np.array([150, 145, 140], dtype=np.uint8)
PRICE_STRIP = np.array([255, 165, 50], dtype=np.uint8)
SHADOW_DARK = np.array([60, 55, 50], dtype=np.uint8)

CONTAINER_COLORS = [
    np.array([190, 210, 225], dtype=np.uint8),
    np.array([200, 200, 210], dtype=np.uint8),
    np.array([225, 220, 210], dtype=np.uint8),
    np.array([210, 215, 220], dtype=np.uint8),
    np.array([180, 195, 210], dtype=np.uint8),
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


def draw_shelf_bar(img, ox, oy, y_start):
    """Draw a horizontal shelf bar: 2px dark + 1px highlight below."""
    for dx in range(2, UNIT - 2):  # Leave room for uprights
        img[(oy + y_start) % SIZE, (ox + dx) % SIZE] = SHELF_DARK
        img[(oy + y_start + 1) % SIZE, (ox + dx) % SIZE] = SHELF_DARK
        img[(oy + y_start + 2) % SIZE, (ox + dx) % SIZE] = SHELF_HIGHLIGHT


def draw_container(img, ox, oy, cx, cy, width, height, color):
    """
    Draw a single container/bin with 3D shading.
    cx, cy are relative to the bay origin (ox, oy).
    Container sits with its BOTTOM at cy+height.

    Structure top to bottom:
    - 3px top face (lighter, open bin top catching light)
    - front face (main color)
    - 1px left highlight, 1px right shadow on edges
    - 1px dark bottom (contact shadow on shelf)
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
                # Top face - open bin top
                c = top_color
                # Slightly darker at edges of top face
                if dx == 0:
                    c = lighten(color, 25)
                elif dx == width - 1:
                    c = lighten(color, 15)
            elif dy == height - 1:
                # Bottom contact shadow
                c = bottom_shadow
            else:
                # Front face
                if dx == 0:
                    c = left_color
                elif dx == width - 1:
                    c = right_color
                else:
                    c = front_color

            img[py, px] = c


def draw_containers_on_shelf(img, ox, oy, shelf_top_y, shelf_bar_y, col, row, shelf_idx):
    """
    Draw 2-3 containers sitting on a shelf.
    Containers rest on the shelf bar, so their bottom is at shelf_bar_y.
    shelf_top_y is the first row available for containers.
    """
    available_h = shelf_bar_y - shelf_top_y
    inner_left = 3  # After 2px upright + 1px gap
    inner_right = UNIT - 3
    inner_w = inner_right - inner_left

    # Determine number of containers (2 or 3)
    n_containers = 2 + (hash_val(col, row, shelf_idx + 100) % 2)

    gap = 2
    total_gap = gap * (n_containers - 1)

    # Generate widths
    widths = []
    remaining_w = inner_w - total_gap
    for i in range(n_containers):
        if i == n_containers - 1:
            w = remaining_w
        else:
            min_w = max(8, remaining_w // (n_containers - i) - 6)
            max_w = remaining_w // (n_containers - i) + 4
            max_w = min(max_w, remaining_w - 8 * (n_containers - i - 1))
            w = min_w + (hash_val(col, row, shelf_idx * 10 + i + 200) % max(1, max_w - min_w))
            remaining_w -= w
        widths.append(w)

    # Draw each container
    cx = inner_left
    for i in range(n_containers):
        w = widths[i]
        # Vary height slightly
        h_variation = hash_val(col, row, shelf_idx * 10 + i + 300) % 5
        h = available_h - h_variation
        if h < 5:
            h = 5

        # Container top is offset down if shorter
        container_y = shelf_top_y + (available_h - h)

        # Pick color
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

            # === Fluorescent light strip (rows 0-4) ===
            for dy in range(5):
                if dy <= 2:
                    # Core bright strip
                    brightness = [1.0, 0.9, 0.7][dy]
                    c = blend(WALL, FLUORESCENT, brightness)
                else:
                    # Glow fade
                    brightness = [0.4, 0.15][dy - 3]
                    c = blend(WALL, FLUORESCENT, brightness)
                for dx in range(UNIT):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = c

            # === Wall background (rows 5-10) ===
            # Already WALL color from initialization, just ensure it
            for dy in range(5, 11):
                for dx in range(UNIT):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = WALL

            # === Shelf 1 (rows 11-30) ===
            # Shelf bar at rows 28-30 (2px dark + 1px highlight)
            shelf1_bar_y = 28
            draw_shelf_bar(img, ox, oy, shelf1_bar_y)
            # Containers above shelf 1: rows 11 to 28
            draw_containers_on_shelf(img, ox, oy, 11, shelf1_bar_y, col, row, 0)

            # === Shelf 2 (rows 31-50) ===
            shelf2_bar_y = 48
            draw_shelf_bar(img, ox, oy, shelf2_bar_y)
            # Containers above shelf 2: rows 31 to 48
            draw_containers_on_shelf(img, ox, oy, 31, shelf2_bar_y, col, row, 1)

            # === Bottom shelf edge + price strip (rows 51-60) ===
            # Small shelf bar at 51-53
            draw_shelf_bar(img, ox, oy, 51)
            # Small containers rows 54-57
            draw_containers_on_shelf(img, ox, oy, 54, 58, col, row, 2)
            # Price strip at rows 59-60
            for dy in [59, 60]:
                for dx in range(3, UNIT - 3):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = PRICE_STRIP

            # === Gap/shadow (rows 61-63) ===
            for dy in range(61, 64):
                t = (dy - 61) / 3.0  # 0 to ~1, dark to lighter
                c = blend(SHADOW_DARK, WALL, t * 0.6)
                for dx in range(UNIT):
                    img[(oy + dy) % SIZE, (ox + dx) % SIZE] = c

            # === Metal shelf uprights (2px wide at left and right edges) ===
            # Draw these LAST so they overlay everything
            for dy in range(UNIT):
                py = (oy + dy) % SIZE
                # Left upright: x=0 and x=1
                img[py, (ox + 0) % SIZE] = darken(UPRIGHT_COLOR, 10)
                img[py, (ox + 1) % SIZE] = UPRIGHT_COLOR
                # Right upright: x=62 and x=63
                img[py, (ox + UNIT - 2) % SIZE] = UPRIGHT_COLOR
                img[py, (ox + UNIT - 1) % SIZE] = darken(UPRIGHT_COLOR, 10)

    # --- Subtle noise for texture ---
    rng = np.random.RandomState(42)
    tile_noise = rng.randint(-2, 3, size=(UNIT, UNIT, 3))
    noise = np.tile(tile_noise, (ROWS, COLS, 1))
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    out = Image.fromarray(img, 'RGB')
    out.save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    generate()
