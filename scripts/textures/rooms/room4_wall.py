"""
Room 4 Wall Texture — "The Best Rave of Your Life"

Peak rave intensity. Dark walls drenched in neon laser light, UV glow,
and strobe flashes. The wall should scream energy.

Output: 256x256 seamless/tileable PNG
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 42

# Palette
BASE = np.array([20, 10, 35], dtype=np.float64)
NEON_PINK = np.array([255, 50, 150], dtype=np.float64)
NEON_CYAN = np.array([50, 255, 255], dtype=np.float64)
NEON_GREEN = np.array([50, 255, 80], dtype=np.float64)
UV_PURPLE = np.array([150, 50, 255], dtype=np.float64)
UV_PINK = np.array([255, 100, 200], dtype=np.float64)
STROBE_WHITE = np.array([200, 200, 220], dtype=np.float64)

rng = np.random.default_rng(SEED)

# Start with base color
texture = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
texture[:, :] = BASE


# --- Subtle brick texture in the dark base ---
BRICK_W = 32
BRICK_H = 16
MORTAR = 2

for y in range(SIZE):
    for x in range(SIZE):
        row = y % BRICK_H
        col = x % BRICK_W
        # Offset every other row by half a brick width
        brick_row = y // BRICK_H
        offset = (BRICK_W // 2) * (brick_row % 2)
        col = (x + offset) % BRICK_W

        # Mortar lines (slightly darker than base)
        is_mortar = (row < MORTAR) or (col < MORTAR)
        if is_mortar:
            texture[y, x] = BASE * 0.6
        else:
            # Slight per-brick variation
            brick_seed = (brick_row * 17 + ((x + offset) // BRICK_W) * 31) % 100
            variation = 0.85 + (brick_seed / 100.0) * 0.3
            texture[y, x] = BASE * variation


# --- UV glow splotches (radial falloff, seamless via wrapping) ---
uv_splotches = [
    # (cx, cy, radius, color, intensity)
    (40, 60, 35, UV_PURPLE, 0.9),
    (180, 30, 28, UV_PINK, 0.7),
    (120, 180, 40, UV_PURPLE, 0.8),
    (220, 140, 32, UV_PINK, 0.75),
    (80, 220, 25, UV_PURPLE, 0.65),
    (160, 100, 22, UV_PINK, 0.6),
    (30, 150, 30, UV_PURPLE, 0.7),
    (200, 230, 26, UV_PINK, 0.8),
    (250, 50, 20, UV_PURPLE, 0.55),
    (100, 40, 18, UV_PINK, 0.5),
]

for cx, cy, radius, color, intensity in uv_splotches:
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = np.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                falloff = 1.0 - (dist / radius)
                falloff = falloff ** 1.5  # sharper falloff
                px = (cx + dx) % SIZE
                py = (cy + dy) % SIZE
                texture[py, px] += color * falloff * intensity


# --- Paint splatters (irregular UV-reactive blobs) ---
splatter_points = [
    (70, 90, UV_PURPLE, 0.6),
    (190, 170, UV_PINK, 0.5),
    (130, 50, NEON_GREEN * 0.4, 0.4),
    (50, 200, UV_PURPLE, 0.5),
    (240, 80, UV_PINK, 0.45),
    (160, 240, NEON_PINK * 0.5, 0.4),
]

for sx, sy, color, intensity in splatter_points:
    # Create irregular splatter with multiple overlapping circles
    num_drops = rng.integers(5, 12)
    for _ in range(num_drops):
        ox = rng.integers(-8, 9)
        oy = rng.integers(-8, 9)
        r = rng.integers(2, 7)
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                dist = np.sqrt(dx * dx + dy * dy)
                if dist <= r:
                    falloff = 1.0 - (dist / r)
                    px = (sx + ox + dx) % SIZE
                    py = (sy + oy + dy) % SIZE
                    texture[py, px] += color * falloff * intensity * 0.6


# --- Laser lines (diagonal and horizontal, seamless) ---

def draw_laser_line(texture, y_intercept, slope, color, width, intensity):
    """Draw a seamless laser line across the texture with glow."""
    for x in range(SIZE):
        center_y = (y_intercept + slope * x) % SIZE
        # Draw the line with glow extending a few pixels
        glow_range = width + 4
        for dy in range(-glow_range, glow_range + 1):
            py = int(center_y + dy) % SIZE
            dist = abs(dy)
            if dist <= width / 2.0:
                # Core of the laser: full brightness
                texture[py, x] += color * intensity
            elif dist <= width / 2.0 + 2:
                # Inner glow
                falloff = 1.0 - (dist - width / 2.0) / 2.0
                texture[py, x] += color * intensity * falloff * 0.6
            elif dist <= glow_range:
                # Outer glow
                falloff = 1.0 - (dist - width / 2.0 - 2) / 2.0
                if falloff > 0:
                    texture[py, x] += color * intensity * falloff * 0.2


# Horizontal lasers
draw_laser_line(texture, 64, 0, NEON_PINK, 2, 1.0)
draw_laser_line(texture, 192, 0, NEON_CYAN, 2, 0.9)
draw_laser_line(texture, 128, 0, NEON_GREEN, 1, 0.6)

# Diagonal lasers (slope chosen so they wrap seamlessly: slope * SIZE = multiple of SIZE)
# slope = 1.0 means exactly 256 rise over 256 run -> seamless
draw_laser_line(texture, 0, 1.0, NEON_PINK, 1, 0.7)
draw_laser_line(texture, 128, 1.0, NEON_CYAN, 1, 0.6)
draw_laser_line(texture, 0, -1.0, NEON_GREEN, 1, 0.5)
draw_laser_line(texture, 80, 0.5, NEON_PINK, 1, 0.5)  # slope=0.5 -> 128 rise, seamless
draw_laser_line(texture, 200, -0.5, NEON_CYAN, 1, 0.45)

# A couple of steep diagonals
draw_laser_line(texture, 30, 2.0, NEON_GREEN, 1, 0.4)  # slope=2 -> 512 rise = 0 mod 256, seamless
draw_laser_line(texture, 170, -2.0, NEON_PINK, 1, 0.35)


# --- Strobe flicker patches ---
strobe_zones = [
    (100, 50, 45, 0.3),
    (200, 180, 35, 0.25),
    (30, 130, 30, 0.2),
    (160, 20, 25, 0.15),
    (240, 240, 40, 0.28),
]

for sx, sy, radius, intensity in strobe_zones:
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = np.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                falloff = 1.0 - (dist / radius)
                falloff = falloff ** 2.0
                px = (sx + dx) % SIZE
                py = (sy + dy) % SIZE
                texture[py, px] += STROBE_WHITE * falloff * intensity


# --- Additional scattered neon specks (like dust in UV light) ---
num_specks = 200
speck_colors = [NEON_PINK, NEON_CYAN, NEON_GREEN, UV_PURPLE]
for _ in range(num_specks):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    color = speck_colors[rng.integers(0, len(speck_colors))]
    intensity = rng.uniform(0.2, 0.6)
    texture[sy % SIZE, sx % SIZE] += color * intensity
    # Small glow around speck
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            texture[(sy + dy) % SIZE, (sx + dx) % SIZE] += color * intensity * 0.3


# --- Clamp to 0-255 and save ---
texture = np.clip(texture, 0, 255).astype(np.uint8)

img = Image.fromarray(texture, 'RGB')
img.save('../../docs/assets/rooms/room4_wall.png')
print(f"Saved output.png: {img.size[0]}x{img.size[1]}")
