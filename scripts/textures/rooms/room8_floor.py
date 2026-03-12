"""
Generate a tileable "fake Container Store" floor texture (256x256).
Room 8 — "The Final Deception": looks like Room 1's retail floor
but subtly WRONG. Slightly too warm/yellow, grout lines wobble,
one tile is off-shade, hairline cracks, a coffee stain.
Uncanny valley retail floor.
"""

import numpy as np
from PIL import Image, ImageDraw
import os

SEED = 808
SIZE = 256
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.png")

rng = np.random.default_rng(SEED)

# --- Base color: yellowish gray (shifted from Room 1's clean gray) ---
base_r, base_g, base_b = 195, 195, 180

pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
pixels[:, :, 0] = base_r
pixels[:, :, 1] = base_g
pixels[:, :, 2] = base_b

# --- Tileable fine speckle noise (slightly more than Room 1) ---
speckle = rng.uniform(-10, 10, (SIZE, SIZE))
for c in range(3):
    pixels[:, :, c] += speckle

# --- Tileable low-frequency mottling (more pronounced, slightly green-shifted) ---
for _ in range(8):
    freq_x = rng.integers(1, 5)
    freq_y = rng.integers(1, 5)
    phase_x = rng.uniform(0, 2 * np.pi)
    phase_y = rng.uniform(0, 2 * np.pi)
    amplitude = rng.uniform(2.0, 5.0)

    x = np.arange(SIZE)
    y = np.arange(SIZE)
    xx, yy = np.meshgrid(x, y)

    wave = amplitude * np.cos(2 * np.pi * freq_x * xx / SIZE + phase_x) * \
           np.cos(2 * np.pi * freq_y * yy / SIZE + phase_y)

    for c in range(3):
        pixels[:, :, c] += wave
    # Extra green channel push for uncanny tint
    pixels[:, :, 1] += wave * 0.15

# --- One quadrant slightly different shade ---
# Bottom-right quadrant (128:256, 128:256) is slightly warmer/darker
quad_mask = np.zeros((SIZE, SIZE), dtype=np.float64)
# Smooth transition using tileable cosine blend
x = np.arange(SIZE)
y = np.arange(SIZE)
xx, yy = np.meshgrid(x, y)
# Use a single-period cosine that peaks in the bottom-right quadrant
quad_blend = (0.5 - 0.5 * np.cos(2 * np.pi * xx / SIZE)) * \
             (0.5 - 0.5 * np.cos(2 * np.pi * yy / SIZE))
pixels[:, :, 0] += quad_blend * 4   # warmer
pixels[:, :, 1] += quad_blend * 2
pixels[:, :, 2] -= quad_blend * 3   # less blue

# --- Grout lines with WOBBLE (the key "wrong" detail) ---
TILE_SIZE = 128
GROUT_WIDTH = 2
grout_r, grout_g, grout_b = 170, 168, 155  # slightly off grout color

# Pre-generate wobble offsets (tileable: same value at 0 and SIZE)
# Use a few sine waves with integer frequencies for seamless tiling
def make_wobble(size, rng_local):
    """Generate tileable wobble pattern (1-2px deviation)."""
    wobble = np.zeros(size, dtype=np.float64)
    for _ in range(3):
        freq = rng_local.integers(2, 8)
        phase = rng_local.uniform(0, 2 * np.pi)
        amp = rng_local.uniform(0.3, 0.8)
        wobble += amp * np.sin(2 * np.pi * freq * np.arange(size) / size + phase)
    return wobble

h_wobble = make_wobble(SIZE, rng)  # wobble for horizontal grout lines
v_wobble = make_wobble(SIZE, rng)  # wobble for vertical grout lines

# Draw grout lines with wobble
for grout_center in range(0, SIZE, TILE_SIZE):
    for pos in range(SIZE):
        # Horizontal grout line at row=grout_center, wobbled by h_wobble[pos]
        for gw in range(GROUT_WIDTH):
            row = (grout_center + gw + int(round(h_wobble[pos]))) % SIZE
            pixels[row, pos, 0] = grout_r
            pixels[row, pos, 1] = grout_g
            pixels[row, pos, 2] = grout_b

        # Vertical grout line at col=grout_center, wobbled by v_wobble[pos]
        for gw in range(GROUT_WIDTH):
            col = (grout_center + gw + int(round(v_wobble[pos]))) % SIZE
            pixels[pos, col, 0] = grout_r
            pixels[pos, col, 1] = grout_g
            pixels[pos, col, 2] = grout_b

# Add noise to grout lines
for grout_center in range(0, SIZE, TILE_SIZE):
    for pos in range(SIZE):
        for gw in range(GROUT_WIDTH):
            row = (grout_center + gw + int(round(h_wobble[pos]))) % SIZE
            noise_val = rng.uniform(-4, 4)
            pixels[row, pos, 0] += noise_val
            pixels[row, pos, 1] += noise_val * 0.9
            pixels[row, pos, 2] += noise_val * 0.8

            col = (grout_center + gw + int(round(v_wobble[pos]))) % SIZE
            noise_val = rng.uniform(-4, 4)
            pixels[pos, col, 0] += noise_val
            pixels[pos, col, 1] += noise_val * 0.9
            pixels[pos, col, 2] += noise_val * 0.8

# --- Hairline cracks (Room 1 doesn't have these) ---
# Draw a few tileable cracks using random walks that wrap
def draw_crack(pixels, start_x, start_y, length, rng_local, color=(140, 138, 125)):
    """Draw a thin crack using a random walk with modulo wrapping."""
    cx, cy = start_x, start_y
    for _ in range(length):
        pixels[cy % SIZE, cx % SIZE, 0] = color[0] + rng_local.uniform(-5, 5)
        pixels[cy % SIZE, cx % SIZE, 1] = color[1] + rng_local.uniform(-5, 5)
        pixels[cy % SIZE, cx % SIZE, 2] = color[2] + rng_local.uniform(-5, 5)
        # Mostly move in one direction with slight deviation
        cx += rng_local.choice([-1, 0, 1], p=[0.15, 0.15, 0.7])
        cy += rng_local.choice([-1, 0, 1], p=[0.1, 0.8, 0.1])

# A few cracks scattered across tiles
for _ in range(4):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    crack_len = rng.integers(15, 45)
    draw_crack(pixels, sx, sy, crack_len, rng)

# One longer diagonal crack
sx = rng.integers(0, SIZE)
sy = rng.integers(0, SIZE)
cx, cy = sx, sy
for _ in range(60):
    pixels[cy % SIZE, cx % SIZE, 0] = 140 + rng.uniform(-5, 5)
    pixels[cy % SIZE, cx % SIZE, 1] = 138 + rng.uniform(-5, 5)
    pixels[cy % SIZE, cx % SIZE, 2] = 125 + rng.uniform(-5, 5)
    cx += rng.choice([0, 1], p=[0.2, 0.8])
    cy += rng.choice([0, 1], p=[0.3, 0.7])

# --- Coffee ring stain ---
# A subtle circular stain mark
stain_cx, stain_cy = 80, 170
stain_radius = 14
stain_thickness = 2
stain_color = np.array([180, 178, 165], dtype=np.float64)

for dy in range(-stain_radius - 2, stain_radius + 3):
    for dx in range(-stain_radius - 2, stain_radius + 3):
        dist = np.sqrt(dx * dx + dy * dy)
        # Ring shape: darken pixels near the radius
        ring_dist = abs(dist - stain_radius)
        if ring_dist < stain_thickness:
            px = (stain_cx + dx) % SIZE
            py = (stain_cy + dy) % SIZE
            falloff = 1.0 - (ring_dist / stain_thickness)
            darken = 8 * falloff
            pixels[py, px, 0] -= darken
            pixels[py, px, 1] -= darken * 0.9
            pixels[py, px, 2] -= darken * 1.2  # slightly blue-brown
        # Fill inside ring with very subtle darkening
        if dist < stain_radius - stain_thickness:
            px = (stain_cx + dx) % SIZE
            py = (stain_cy + dy) % SIZE
            pixels[py, px, 0] -= 2
            pixels[py, px, 1] -= 2
            pixels[py, px, 2] -= 3

# --- Faint polish/sheen highlights (slightly fewer and dimmer than Room 1) ---
num_highlights = 20
for _ in range(num_highlights):
    hx = rng.integers(0, SIZE)
    hy = rng.integers(0, SIZE)
    radius = rng.integers(3, 7)
    brightness = rng.uniform(3, 7)

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = np.sqrt(dx * dx + dy * dy)
            if dist <= radius:
                falloff = 1.0 - (dist / radius)
                px = (hx + dx) % SIZE
                py = (hy + dy) % SIZE
                for c in range(3):
                    pixels[py, px, c] += brightness * falloff

# --- Dark speckles (more than Room 1 — dirtier floor) ---
num_dark_specks = 350
for _ in range(num_dark_specks):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    darkening = rng.uniform(10, 22)
    for c in range(3):
        pixels[sy, sx, c] -= darkening
    if rng.random() < 0.4:
        nx = (sx + 1) % SIZE
        for c in range(3):
            pixels[sy, nx, c] -= darkening * 0.6

# --- Overall slight green tint (uncanny) ---
pixels[:, :, 1] += 2  # push green channel slightly

# --- Subtle overall dirtiness: darken edges of tiles slightly ---
# Use tileable gradient that darkens near grout lines
for axis in range(SIZE):
    tile_pos = axis % TILE_SIZE
    # Distance from nearest grout line (0 at grout, TILE_SIZE/2 at center)
    dist_from_grout = min(tile_pos, TILE_SIZE - tile_pos)
    if dist_from_grout < 8:
        edge_darken = (1.0 - dist_from_grout / 8.0) * 3
        pixels[axis, :, :] -= edge_darken * 0.5
        pixels[:, axis, :] -= edge_darken * 0.5

# --- Clamp and convert ---
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

# --- Save ---
img = Image.fromarray(pixels, 'RGB')
img.save(OUTPUT)
print(f"Saved {OUTPUT} ({img.size[0]}x{img.size[1]})")
