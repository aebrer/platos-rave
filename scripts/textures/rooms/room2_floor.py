"""
Room 2 Floor Texture — "The Cloister of Confidence" (Container Store Warehouse floor)
Industrial warehouse concrete floor with cracks, oil stains, tire marks, and faded safety lines.
256x256, tileable, pixel art dungeon-crawler aesthetic.
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 42

rng = np.random.default_rng(SEED)

# --- Color palette ---
BASE_CONCRETE = np.array([148, 143, 138], dtype=np.float64)  # darker base
STAIN_COLOR = np.array([125, 118, 112], dtype=np.float64)  # brown-tinted stains
CRACK_COLOR = np.array([95, 90, 85], dtype=np.float64)
SAFETY_YELLOW = np.array([175, 165, 95], dtype=np.float64)  # more muted yellow
TIRE_MARK_COLOR = np.array([128, 123, 118], dtype=np.float64)


def make_tileable_noise_fast(size, scale, rng):
    """Vectorized tileable value noise with cosine interpolation."""
    grid = scale
    vals = rng.random((grid, grid))
    # Extend by 1 in each direction for interpolation, wrapping
    vals_ext = np.zeros((grid + 1, grid + 1))
    vals_ext[:grid, :grid] = vals
    vals_ext[grid, :grid] = vals[0, :]
    vals_ext[:grid, grid] = vals[:, 0]
    vals_ext[grid, grid] = vals[0, 0]

    cell_size = size / grid
    xs = np.arange(size, dtype=np.float64)
    ys = np.arange(size, dtype=np.float64)
    gx = xs / cell_size
    gy = ys / cell_size

    ix = np.floor(gx).astype(int) % grid
    iy = np.floor(gy).astype(int) % grid
    fx = gx - np.floor(gx)
    fy = gy - np.floor(gy)
    fx = (1 - np.cos(fx * np.pi)) / 2
    fy = (1 - np.cos(fy * np.pi)) / 2

    iy2d = iy[:, None]
    ix2d = ix[None, :]
    fy2d = fy[:, None]
    fx2d = fx[None, :]

    v00 = vals_ext[iy2d, ix2d]
    v10 = vals_ext[iy2d, ix2d + 1]
    v01 = vals_ext[iy2d + 1, ix2d]
    v11 = vals_ext[iy2d + 1, ix2d + 1]

    v0 = v00 * (1 - fx2d) + v10 * fx2d
    v1 = v01 * (1 - fx2d) + v11 * fx2d
    out = v0 * (1 - fy2d) + v1 * fy2d
    return out


def multi_octave_noise(size, base_scale, octaves, rng):
    """Multi-octave tileable noise for natural-looking variation."""
    result = np.zeros((size, size), dtype=np.float64)
    amplitude = 1.0
    total_amp = 0.0
    for i in range(octaves):
        scale = base_scale * (2 ** i)
        if scale > size:
            scale = size
        noise = make_tileable_noise_fast(size, scale, rng)
        result += noise * amplitude
        total_amp += amplitude
        amplitude *= 0.5
    return result / total_amp


def make_tileable_grain(size, rng):
    """Create tileable pixel grain by generating random values on a grid
    that divides size evenly (1:1 means every pixel is independent but
    we ensure perfect tiling by using modular indexing)."""
    # For true per-pixel grain that tiles, just generate SIZE x SIZE
    # and it tiles perfectly since each pixel is independent
    return rng.random((size, size))


# --- Base concrete with multi-octave noise ---
print("Generating base concrete noise...")
concrete_noise = multi_octave_noise(SIZE, 4, 5, rng)

# Secondary noise layer for color variation (slight warm/cool shifts)
color_shift_noise = make_tileable_noise_fast(SIZE, 6, rng)

pixels = np.zeros((SIZE, SIZE, 3), dtype=np.float64)
for c in range(3):
    pixels[:, :, c] = BASE_CONCRETE[c] + (concrete_noise - 0.5) * 25

# Add slight warm/cool color shifts across the surface
pixels[:, :, 0] += (color_shift_noise - 0.5) * 6   # red channel shifts
pixels[:, :, 2] -= (color_shift_noise - 0.5) * 4   # blue channel counter-shifts

# --- Fine grain texture (tileable) ---
print("Adding grain texture...")
grain = make_tileable_grain(SIZE, rng)
grain_strength = 8.0
pixels += (grain[:, :, None] - 0.5) * grain_strength

# --- Large dark patches (water damage / general grime) ---
print("Adding grime patches...")
grime_noise = make_tileable_noise_fast(SIZE, 3, rng)
grime_mask = np.clip((grime_noise - 0.4) * 2.5, 0, 1)
pixels -= grime_mask[:, :, None] * 12  # darken grime areas

# --- Oil stains / dark patches ---
print("Adding oil stains...")
stain_noise = make_tileable_noise_fast(SIZE, 8, rng)
stain_mask = np.clip((stain_noise - 0.55) * 4, 0, 1)

# Concentrated stain spots with wrapped distance for tileability
num_stains = 7
ys_grid, xs_grid = np.mgrid[0:SIZE, 0:SIZE]
for _ in range(num_stains):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    radius = rng.integers(10, 35)
    dx = np.minimum(np.abs(xs_grid - cx), SIZE - np.abs(xs_grid - cx))
    dy = np.minimum(np.abs(ys_grid - cy), SIZE - np.abs(ys_grid - cy))
    dist = np.sqrt(dx**2 + dy**2)
    # Irregular shape using noise
    irregularity = make_tileable_noise_fast(SIZE, 16, rng)
    adjusted_dist = dist - irregularity * radius * 0.3
    spot = np.clip(1.0 - adjusted_dist / radius, 0, 1) ** 1.5
    stain_mask = np.maximum(stain_mask, spot * 0.7)

for c in range(3):
    pixels[:, :, c] = pixels[:, :, c] * (1 - stain_mask) + STAIN_COLOR[c] * stain_mask

# --- Scuff marks (small random darker patches) ---
print("Adding scuff marks...")
for _ in range(20):
    cx = rng.integers(0, SIZE)
    cy = rng.integers(0, SIZE)
    w = rng.integers(3, 12)
    h = rng.integers(2, 6)
    angle = rng.random() * np.pi
    intensity = 0.15 + rng.random() * 0.2
    for i in range(w):
        for j in range(h):
            rx = int(cx + i * np.cos(angle) - j * np.sin(angle)) % SIZE
            ry = int(cy + i * np.sin(angle) + j * np.cos(angle)) % SIZE
            pixels[ry, rx] = pixels[ry, rx] * (1 - intensity) + CRACK_COLOR * intensity

# --- Cracks ---
print("Adding cracks...")


def draw_crack_tileable(pixels, start_x, start_y, length, direction, rng, width_chance=0.3):
    """Draw a wandering crack line that wraps around for tileability."""
    x, y = float(start_x), float(start_y)
    dx, dy = direction
    for step in range(length):
        ix = int(x) % SIZE
        iy = int(y) % SIZE
        # Fade at start and end
        fade = min(step / 4.0, (length - step) / 4.0, 1.0)
        blend = 0.7 + rng.random() * 0.3
        blend *= fade
        for c in range(3):
            pixels[iy, ix, c] = pixels[iy, ix, c] * (1 - blend) + (CRACK_COLOR[c] + rng.random() * 10) * blend
        # Occasionally widen
        if rng.random() < width_chance:
            ix2 = (ix + 1) % SIZE
            for c in range(3):
                pixels[iy, ix2, c] = pixels[iy, ix2, c] * 0.7 + CRACK_COLOR[c] * 0.3 * fade
        # Shadow edge (lighter pixel on one side for depth)
        if rng.random() < 0.4:
            iy2 = (iy - 1) % SIZE
            for c in range(3):
                pixels[iy2, ix, c] = min(255, pixels[iy2, ix, c] + 4 * fade)
        # Wander
        x += dx + rng.random() * 1.2 - 0.6
        y += dy + rng.random() * 1.2 - 0.6
        if rng.random() < 0.08:
            dx += rng.random() * 0.5 - 0.25
            dy += rng.random() * 0.5 - 0.25


# Major cracks
for _ in range(8):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    angle = rng.random() * 2 * np.pi
    dx = np.cos(angle) * 1.1
    dy = np.sin(angle) * 1.1
    length = rng.integers(50, 140)
    draw_crack_tileable(pixels, sx, sy, length, (dx, dy), rng)
    # Branch cracks
    if rng.random() < 0.5:
        branch_start = rng.integers(10, max(11, length - 10))
        bx = (sx + dx * branch_start) % SIZE
        by = (sy + dy * branch_start) % SIZE
        b_angle = angle + rng.random() * 1.0 - 0.5
        bdx = np.cos(b_angle) * 0.7
        bdy = np.sin(b_angle) * 0.7
        draw_crack_tileable(pixels, bx, by, rng.integers(15, 40), (bdx, bdy), rng, width_chance=0.15)

# Minor cracks
for _ in range(15):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    angle = rng.random() * 2 * np.pi
    dx = np.cos(angle) * 0.7
    dy = np.sin(angle) * 0.7
    length = rng.integers(8, 30)
    draw_crack_tileable(pixels, sx, sy, length, (dx, dy), rng, width_chance=0.15)

# --- Tire marks ---
print("Adding tire marks...")


def draw_tire_mark(pixels, start_x, start_y, length, direction, width, rng):
    """Draw a subtle tire mark streak with tread texture."""
    x, y = float(start_x), float(start_y)
    dx, dy = direction
    norm = np.sqrt(dx**2 + dy**2)
    if norm == 0:
        return
    ndx, ndy = dx / norm, dy / norm
    perp_x, perp_y = -ndy, ndx

    for i in range(length):
        # Fade at ends
        fade = min(i / 8.0, (length - i) / 8.0, 1.0)
        # Tread pattern: alternating light/dark every few pixels
        tread = 0.7 + 0.3 * (1 if (i // 3) % 2 == 0 else 0)
        blend = 0.25 * fade * tread

        for w in range(-width // 2, width // 2 + 1):
            px = int(x + perp_x * w) % SIZE
            py = int(y + perp_y * w) % SIZE
            # Edges of tire mark are fainter
            edge_fade = 1.0 - abs(w) / (width / 2 + 1) * 0.5
            b = blend * edge_fade
            for c in range(3):
                pixels[py, px, c] = pixels[py, px, c] * (1 - b) + TIRE_MARK_COLOR[c] * b

        x += dx + rng.random() * 0.2 - 0.1
        y += dy + rng.random() * 0.2 - 0.1


for _ in range(5):
    sx = rng.integers(0, SIZE)
    sy = rng.integers(0, SIZE)
    if rng.random() < 0.5:
        dx, dy = 1.0, rng.random() * 0.2 - 0.1
    else:
        dx, dy = rng.random() * 0.2 - 0.1, 1.0
    length = rng.integers(80, 200)
    width = rng.integers(4, 8)
    draw_tire_mark(pixels, sx, sy, length, (dx, dy), width, rng)

# --- Faded yellow safety line fragments ---
print("Adding safety line markings...")


def draw_safety_line(pixels, start_x, start_y, length, horizontal, rng):
    """Draw a very faded, worn yellow safety line fragment."""
    width = rng.integers(3, 5)
    x, y = start_x, start_y

    # Pre-generate a wear pattern for this line
    wear_base = rng.random(length) * 0.25 + 0.1  # 10-35% base visibility — very worn

    for i in range(length):
        # Fade at edges
        edge_fade = 1.0
        if i < 8:
            edge_fade = i / 8.0
        elif i > length - 8:
            edge_fade = (length - i) / 8.0

        # Some sections are nearly gone
        if rng.random() < 0.15:
            continue  # skip pixel entirely — paint chipped off

        for w in range(width):
            if horizontal:
                px = (x + i) % SIZE
                py = (y + w) % SIZE
            else:
                px = (x + w) % SIZE
                py = (y + i) % SIZE

            # Edge of line is more worn
            edge_w = 1.0 if (w > 0 and w < width - 1) else 0.5
            wear = wear_base[i] * edge_fade * edge_w
            # Add per-pixel noise
            wear *= (0.7 + rng.random() * 0.6)
            wear = min(wear, 0.35)  # cap blending — these are FADED

            for c in range(3):
                pixels[py, px, c] = pixels[py, px, c] * (1 - wear) + SAFETY_YELLOW[c] * wear


# Partial safety line fragments — as if the warehouse had markings that have been
# worn down by years of forklift traffic
draw_safety_line(pixels, rng.integers(0, SIZE), rng.integers(50, 90), rng.integers(60, 110), True, rng)
draw_safety_line(pixels, rng.integers(0, SIZE), rng.integers(170, 220), rng.integers(45, 85), True, rng)
draw_safety_line(pixels, rng.integers(90, 160), rng.integers(0, SIZE), rng.integers(35, 65), False, rng)

# --- Concrete joint lines (subtle control joints) ---
print("Adding control joints...")
# Warehouses have scored/cut joints in the concrete at regular intervals
# These should be subtle — just slightly darker lines
joint_spacing = 64  # divides 256 evenly
for jx in range(0, SIZE, joint_spacing):
    for y in range(SIZE):
        # Slight wobble
        offset = int(rng.random() * 0.8)
        px = (jx + offset) % SIZE
        blend = 0.15 + rng.random() * 0.1
        for c in range(3):
            pixels[y, px, c] = pixels[y, px, c] * (1 - blend) + CRACK_COLOR[c] * blend
        # Adjacent highlight (concrete lip)
        px2 = (jx + offset + 1) % SIZE
        for c in range(3):
            pixels[y, px2, c] = min(255, pixels[y, px2, c] + 3)

for jy in range(0, SIZE, joint_spacing):
    for x in range(SIZE):
        offset = int(rng.random() * 0.8)
        py = (jy + offset) % SIZE
        blend = 0.15 + rng.random() * 0.1
        for c in range(3):
            pixels[py, x, c] = pixels[py, x, c] * (1 - blend) + CRACK_COLOR[c] * blend
        py2 = (jy + offset + 1) % SIZE
        for c in range(3):
            pixels[py2, x, c] = min(255, pixels[py2, x, c] + 3)

# --- Final adjustments ---
# Darken overall to ensure gritty warehouse feel
pixels *= 0.93

# Clamp
pixels = np.clip(pixels, 0, 255).astype(np.uint8)

# Pixel art quantization (step of 4 for retro feel)
pixels = (pixels // 4) * 4

# --- Save ---
print("Saving output.png...")
img = Image.fromarray(pixels, mode='RGB')
img.save('../../docs/assets/rooms/room2_floor.png')
print(f"Done! Output: {img.size[0]}x{img.size[1]} pixels")
