"""
Room 10 Wall Texture — "The Candy King" (Dark Throne Room)

Near-total darkness with a warm spotlight cone and vivid candy sparkles
scattered in the void. Ominous, dramatic, final boss energy.
Pixel art style, 256x256, seamless/tileable.
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 1010

rng = np.random.default_rng(SEED)

# --- Palette ---
VOID_COLORS = np.array([
    [8, 5, 12],
    [12, 8, 15],
    [6, 4, 10],
], dtype=np.float64)

STONE_COLOR = np.array([15, 12, 18], dtype=np.float64)

# Candy sparkle colors (vivid)
CANDY_COLORS = np.array([
    [255, 50, 50],    # red
    [255, 200, 50],   # yellow
    [50, 255, 50],    # green
    [50, 150, 255],   # blue
    [200, 50, 255],   # purple
    [255, 150, 50],   # orange
], dtype=np.float64)


def make_tileable_noise(size, scale, rng):
    """Generate tileable Perlin-like noise using modular sine-hash approach."""
    # Use overlapping octaves of tiled noise
    arr = np.zeros((size, size), dtype=np.float64)
    grid = scale
    # Create a random grid that tiles
    rand_grid = rng.random((grid, grid))

    y_coords = np.arange(size)
    x_coords = np.arange(size)
    yy, xx = np.meshgrid(y_coords, x_coords, indexing='ij')

    # Map pixel coords to grid coords
    gy = (yy / size) * grid
    gx = (xx / size) * grid

    # Bilinear interpolation with wrapping
    gy0 = np.floor(gy).astype(int) % grid
    gx0 = np.floor(gx).astype(int) % grid
    gy1 = (gy0 + 1) % grid
    gx1 = (gx0 + 1) % grid

    fy = gy - np.floor(gy)
    fx = gx - np.floor(gx)

    # Smoothstep
    fy = fy * fy * (3 - 2 * fy)
    fx = fx * fx * (3 - 2 * fx)

    v00 = rand_grid[gy0, gx0]
    v10 = rand_grid[gy1, gx0]
    v01 = rand_grid[gy0, gx1]
    v11 = rand_grid[gy1, gx1]

    arr = v00 * (1 - fx) * (1 - fy) + v01 * fx * (1 - fy) + v10 * (1 - fx) * fy + v11 * fx * fy
    return arr


def make_fbm_noise(size, octaves, rng):
    """Fractal Brownian motion from tileable noise octaves."""
    result = np.zeros((size, size), dtype=np.float64)
    amplitude = 1.0
    total_amp = 0.0
    for i in range(octaves):
        scale = 4 * (2 ** i)  # 4, 8, 16, 32, ...
        if scale > size:
            scale = size
        result += amplitude * make_tileable_noise(size, scale, rng)
        total_amp += amplitude
        amplitude *= 0.5
    return result / total_amp


# --- 1. Base void texture ---
img = np.zeros((SIZE, SIZE, 3), dtype=np.float64)

# Fill with random void colors per pixel
void_indices = rng.integers(0, len(VOID_COLORS), size=(SIZE, SIZE))
for i, vc in enumerate(VOID_COLORS):
    mask = void_indices == i
    img[mask] = vc


# --- 2. Subtle stone wall texture (barely visible dark-on-dark) ---
stone_noise = make_fbm_noise(SIZE, 4, rng)
# Normalize to 0-1
stone_noise = (stone_noise - stone_noise.min()) / (stone_noise.max() - stone_noise.min() + 1e-9)

# Very subtle stone pattern: blend toward STONE_COLOR with low opacity
stone_strength = stone_noise * 0.15  # very faint
for c in range(3):
    img[:, :, c] += stone_strength * (STONE_COLOR[c] - img[:, :, c])

# Add a second layer of coarser stone "blocks" pattern (tileable)
block_noise = make_tileable_noise(SIZE, 16, rng)  # 16 divides 256
block_noise = (block_noise - block_noise.min()) / (block_noise.max() - block_noise.min() + 1e-9)
# Threshold to create faint mortar lines
mortar = (block_noise < 0.15).astype(np.float64) * 0.08
for c in range(3):
    img[:, :, c] = img[:, :, c] * (1.0 - mortar) + (STONE_COLOR[c] * 0.5) * mortar


# --- 3. Spotlight cone ---
# Warm spotlight from upper-center area, creates a cone of light
# For tileability: the spotlight is broad and fades at edges using a tileable falloff

# Center the spotlight at roughly (SIZE*0.5, SIZE*0.35) — upper center
spot_cx, spot_cy = SIZE * 0.5, SIZE * 0.30

yy, xx = np.meshgrid(np.arange(SIZE), np.arange(SIZE), indexing='ij')

# Tileable distance: use modulo wrapping for distance calc
dx = np.abs(xx - spot_cx)
dx = np.minimum(dx, SIZE - dx)  # wrap horizontally
dy = np.abs(yy - spot_cy)
dy = np.minimum(dy, SIZE - dy)  # wrap vertically

# Elliptical spotlight (wider than tall), cone shape
dist = np.sqrt((dx / 90.0) ** 2 + (dy / 70.0) ** 2)

# Spotlight intensity: smooth falloff
spot_intensity = np.clip(1.0 - dist, 0.0, 1.0)
spot_intensity = spot_intensity ** 2.5  # sharper falloff for cone feel

# Spotlight color gradient: warm golden at center, dimmer at edges
# Brightest: (60, 45, 20), edge: (20, 15, 8)
spot_bright = np.array([60, 45, 20], dtype=np.float64)
spot_dim = np.array([20, 15, 8], dtype=np.float64)

for c in range(3):
    spot_color = spot_dim[c] + (spot_bright[c] - spot_dim[c]) * spot_intensity
    img[:, :, c] += spot_color * spot_intensity * 0.7

# Add a faint secondary warm glow at the bottom (reflected from candy/crown)
spot2_cy = SIZE * 0.85
dy2 = np.abs(yy - spot2_cy)
dy2 = np.minimum(dy2, SIZE - dy2)
dx2 = np.abs(xx - spot_cx)
dx2 = np.minimum(dx2, SIZE - dx2)
dist2 = np.sqrt((dx2 / 120.0) ** 2 + (dy2 / 40.0) ** 2)
glow2 = np.clip(1.0 - dist2, 0.0, 1.0) ** 3.0

for c in range(3):
    golden = np.array([35, 25, 10], dtype=np.float64)
    img[:, :, c] += golden[c] * glow2 * 0.3


# --- 4. Candy sparkles ---
# Scatter bright candy-colored pixels, more concentrated in the spotlight area
num_sparkles = 180

# For tileability, we place sparkles with tileable positions
sparkle_x = rng.integers(0, SIZE, size=num_sparkles)
sparkle_y = rng.integers(0, SIZE, size=num_sparkles)

# Weight toward spotlight: sparkles near spotlight are brighter
for i in range(num_sparkles):
    sx, sy = int(sparkle_x[i]) % SIZE, int(sparkle_y[i]) % SIZE

    # Distance from spotlight center (tileable)
    sdx = min(abs(sx - spot_cx), SIZE - abs(sx - spot_cx))
    sdy = min(abs(sy - spot_cy), SIZE - abs(sy - spot_cy))
    sdist = np.sqrt(sdx**2 + sdy**2)

    # Sparkle brightness depends on proximity to spotlight
    # Sparkles in darkness are dimmer but still visible
    if sdist < 80:
        brightness = rng.uniform(0.6, 1.0)
    elif sdist < 140:
        brightness = rng.uniform(0.2, 0.6)
    else:
        brightness = rng.uniform(0.05, 0.25)

    # Pick a random candy color
    color_idx = rng.integers(0, len(CANDY_COLORS))
    color = CANDY_COLORS[color_idx]

    # Place the sparkle (1-2px)
    sparkle_size = rng.integers(1, 3)  # 1 or 2

    for dy_off in range(sparkle_size):
        for dx_off in range(sparkle_size):
            px = (sx + dx_off) % SIZE
            py = (sy + dy_off) % SIZE
            # Additive blend for glow effect
            for c in range(3):
                img[py, px, c] = img[py, px, c] + color[c] * brightness

    # Add a faint 1px glow halo around brighter sparkles
    if brightness > 0.4:
        halo_brightness = brightness * 0.15
        for dy_off in range(-1, sparkle_size + 1):
            for dx_off in range(-1, sparkle_size + 1):
                # Skip the sparkle center pixels
                if 0 <= dy_off < sparkle_size and 0 <= dx_off < sparkle_size:
                    continue
                px = (sx + dx_off) % SIZE
                py = (sy + dy_off) % SIZE
                for c in range(3):
                    img[py, px, c] = img[py, px, c] + color[c] * halo_brightness


# --- 5. Faint golden edge glow (reflected candy crown light) ---
# Very subtle warm border glow along top/bottom edges (tileable)
edge_glow_top = np.exp(-((yy / SIZE) * 8.0)) * 0.03
edge_glow_bot = np.exp(-(((SIZE - yy) / SIZE) * 8.0)) * 0.02

for c in range(3):
    warm = np.array([40, 30, 12], dtype=np.float64)
    img[:, :, c] += warm[c] * (edge_glow_top + edge_glow_bot)


# --- 6. Final noise dither for pixel art feel ---
dither = rng.integers(-2, 3, size=(SIZE, SIZE, 3)).astype(np.float64)
img += dither


# --- Clamp and save ---
img = np.clip(img, 0, 255).astype(np.uint8)

output = Image.fromarray(img, 'RGB')
output.save('../../docs/assets/rooms/room10_wall.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
