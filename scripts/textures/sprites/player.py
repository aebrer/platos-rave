"""
Generate player character sprites for Plato's Rave.
Tiny pixel-art sprites of a raver attending an escalating rave in a Container Store.

Output: docs/assets/sprites/player/
  - head.png (20x20)
  - torso.png (16x28)
  - leg_left.png (5x16)
  - leg_right.png (5x16)
  - shadow.png (40x8)
  - dance_burst.png (48x48)
"""

import os
import numpy as np
from PIL import Image

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../docs/assets/sprites/player")

# Palette
SKIN = (220, 185, 155, 255)
HAIR = (180, 50, 200, 255)
HAIR_DARK = (140, 30, 160, 255)
SHIRT = (40, 35, 50, 255)
NEON_STRIPE = (0, 255, 200, 255)
GLOW_STICK = (0, 255, 150, 255)
GLOW_DIM = (0, 200, 120, 180)
PANTS = (50, 45, 60, 255)
SHOES = (80, 70, 90, 255)
EYE = (30, 25, 40, 255)
MOUTH = (200, 100, 100, 255)
CLEAR = (0, 0, 0, 0)


def make_image(w, h):
    """Create a blank RGBA image as a numpy array."""
    return np.zeros((h, w, 4), dtype=np.uint8)


def px(img, x, y, color):
    """Set a pixel, bounds-checked."""
    h, w = img.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        img[y, x] = color


def save(img, name):
    """Save numpy array as PNG."""
    path = os.path.join(OUTPUT_DIR, name)
    Image.fromarray(img, "RGBA").save(path)
    print(f"  Saved: {path} ({img.shape[1]}x{img.shape[0]})")


def generate_head():
    """20x20 head with spiky purple hair, simple face, warm skin."""
    img = make_image(20, 20)

    # Hair spikes (top rows, irregular for that messy raver look)
    spikes = [
        # (x, y) positions for hair spikes going upward
        (7, 0), (8, 0), (12, 0), (13, 0),
        (6, 1), (7, 1), (8, 1), (9, 1), (11, 1), (12, 1), (13, 1),
        (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2),
        (10, 0), (15, 1),  # extra spike tips
    ]
    for (x, y) in spikes:
        px(img, x, y, HAIR)

    # Hair band / top of head (rows 3-5)
    for y in range(3, 6):
        for x in range(4, 16):
            px(img, x, y, HAIR)
    # Darker hair highlights
    for x in [5, 9, 14]:
        px(img, x, 3, HAIR_DARK)
    for x in [6, 11]:
        px(img, x, 4, HAIR_DARK)

    # Face - oval shape (rows 6-16)
    face_widths = {
        6: (5, 15),
        7: (4, 16),
        8: (4, 16),
        9: (4, 16),
        10: (4, 16),
        11: (4, 16),
        12: (4, 16),
        13: (4, 16),
        14: (5, 15),
        15: (5, 15),
        16: (6, 14),
        17: (7, 13),
    }
    for y, (x_start, x_end) in face_widths.items():
        for x in range(x_start, x_end):
            px(img, x, y, SKIN)

    # Hair on sides of face (sideburns)
    for y in range(6, 10):
        px(img, 4, y, HAIR)
        px(img, 15, y, HAIR)

    # Eyes (row 10-11)
    px(img, 7, 10, EYE)
    px(img, 8, 10, EYE)
    px(img, 12, 10, EYE)
    px(img, 13, 10, EYE)
    # Eye shine
    px(img, 7, 10, (60, 55, 80, 255))

    # Grin (row 14)
    for x in range(8, 13):
        px(img, x, 14, MOUTH)
    # Grin corners slightly up
    px(img, 7, 13, MOUTH)
    px(img, 13, 13, MOUTH)

    # Chin / jaw definition
    px(img, 6, 17, (200, 165, 135, 255))
    px(img, 13, 17, (200, 165, 135, 255))

    save(img, "head.png")


def generate_torso():
    """16x28 torso with dark graphic tee, neon stripe, glow stick necklace."""
    img = make_image(16, 28)

    # Neck (rows 0-2, narrow)
    for y in range(0, 3):
        for x in range(6, 10):
            px(img, x, y, SKIN)

    # Shoulders and shirt body (rows 3-25)
    torso_widths = {
        3: (3, 13),
        4: (2, 14),
        5: (1, 15),
        6: (1, 15),
        7: (1, 15),
    }
    for y in range(3, 8):
        x_start, x_end = torso_widths.get(y, (1, 15))
        for x in range(x_start, x_end):
            px(img, x, y, SHIRT)

    for y in range(8, 26):
        for x in range(2, 14):
            px(img, x, y, SHIRT)

    # Slight taper at bottom
    for x in range(3, 13):
        px(img, x, 26, SHIRT)
    for x in range(3, 13):
        px(img, x, 27, SHIRT)

    # Glow stick necklace (curved, rows 4-6)
    glow_pixels = [
        (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
        (4, 5), (11, 5),
        (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6),
    ]
    for (x, y) in glow_pixels:
        px(img, x, y, GLOW_STICK)
    # Dimmer glow halo around necklace
    glow_halo = [(3, 5), (12, 5), (5, 3), (10, 3)]
    for (x, y) in glow_halo:
        px(img, x, y, GLOW_DIM)

    # Neon stripe across chest (row 12-13)
    for x in range(3, 13):
        px(img, x, 12, NEON_STRIPE)
    # Second stripe, slightly different
    stripe2 = (0, 220, 180, 200)
    for x in range(4, 12):
        px(img, x, 13, stripe2)

    # Small graphic element on shirt (abstract squiggle, rows 16-20)
    graphic = (0, 200, 160, 180)
    graphic_pixels = [
        (5, 16), (6, 16),
        (7, 17), (8, 17),
        (6, 18), (7, 18),
        (8, 19), (9, 19),
        (7, 20), (8, 20),
    ]
    for (x, y) in graphic_pixels:
        px(img, x, y, graphic)

    # Arms/sleeves hint at edges (skin showing below sleeve)
    for y in range(8, 12):
        px(img, 1, y, SKIN)
        px(img, 14, y, SKIN)

    save(img, "torso.png")


def generate_leg(name, mirror=False):
    """5x16 leg with dark pants and shoe at bottom."""
    img = make_image(5, 16)

    # Pants (rows 0-11)
    for y in range(0, 12):
        if y < 2:
            # Slightly wider at top
            for x in range(0, 5):
                px(img, x, y, PANTS)
        else:
            for x in range(1, 4):
                px(img, x, y, PANTS)
            # Subtle highlight on one side
            highlight = (60, 55, 70, 255)
            if not mirror:
                px(img, 1, y, highlight)
            else:
                px(img, 3, y, highlight)

    # Shoe (rows 12-15)
    shoe_bright = (100, 90, 110, 255)
    for y in range(12, 16):
        for x in range(0, 5):
            px(img, x, y, SHOES)
    # Shoe sole (bottom row, slightly darker)
    sole = (60, 50, 70, 255)
    for x in range(0, 5):
        px(img, x, 15, sole)
    # Shoe accent (small neon lace dot)
    px(img, 2, 12, NEON_STRIPE)

    if mirror:
        img = img[:, ::-1, :].copy()

    save(img, name)


def generate_shadow():
    """40x8 elliptical shadow, semi-transparent with soft edges."""
    img = make_image(40, 8)

    cx, cy = 20, 4
    rx, ry = 18, 3.5

    for y in range(8):
        for x in range(40):
            # Ellipse distance
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = (dx * dx + dy * dy) ** 0.5

            if dist < 1.0:
                # Fade from center to edge
                alpha = int(100 * (1.0 - dist) ** 1.5)
                alpha = max(0, min(255, alpha))
                img[y, x] = (0, 0, 0, alpha)

    save(img, "shadow.png")


def generate_dance_burst():
    """48x48 radial burst with neon sparkles and emanating lines."""
    img = make_image(48, 48)

    cx, cy = 24, 24
    neon_colors = [
        (0, 255, 255),   # cyan
        (255, 0, 255),   # magenta
        (255, 255, 0),   # yellow
        (0, 255, 200),   # teal
        (255, 100, 255), # pink
    ]

    # Radial lines emanating from center
    import math
    num_rays = 12
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        color = neon_colors[i % len(neon_colors)]

        for r in range(6, 22):
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            # Fade alpha with distance
            alpha = int(220 * (1.0 - (r - 6) / 16.0))
            alpha = max(0, min(255, alpha))
            px(img, x, y, (*color, alpha))

    # Inner glow ring
    for angle_deg in range(0, 360, 3):
        angle = math.radians(angle_deg)
        for r in [4, 5]:
            x = int(cx + r * math.cos(angle))
            y = int(cy + r * math.sin(angle))
            alpha = 180 if r == 4 else 120
            c = neon_colors[(angle_deg // 30) % len(neon_colors)]
            px(img, x, y, (*c, alpha))

    # Sparkle dots at ray tips and mid-points
    sparkle_positions = []
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        # Tips
        r = 20
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        sparkle_positions.append((x, y))
        # Mid sparkles (offset angle)
        angle2 = angle + math.pi / num_rays
        r2 = 14
        x2 = int(cx + r2 * math.cos(angle2))
        y2 = int(cy + r2 * math.sin(angle2))
        sparkle_positions.append((x2, y2))

    for idx, (sx, sy) in enumerate(sparkle_positions):
        c = neon_colors[idx % len(neon_colors)]
        # Small cross sparkle
        px(img, sx, sy, (*c, 255))
        px(img, sx - 1, sy, (*c, 180))
        px(img, sx + 1, sy, (*c, 180))
        px(img, sx, sy - 1, (*c, 180))
        px(img, sx, sy + 1, (*c, 180))

    # Outer scattered dots
    np.random.seed(42)
    for _ in range(20):
        angle = np.random.uniform(0, 2 * math.pi)
        r = np.random.uniform(15, 22)
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        c = neon_colors[np.random.randint(0, len(neon_colors))]
        alpha = np.random.randint(100, 220)
        px(img, x, y, (*c, alpha))

    save(img, "dance_burst.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating player sprites for Plato's Rave...")
    print()

    generate_head()
    generate_torso()
    generate_leg("leg_left.png", mirror=False)
    generate_leg("leg_right.png", mirror=True)
    generate_shadow()
    generate_dance_burst()

    print()
    print("Done! All sprites saved to:")
    print(f"  {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
