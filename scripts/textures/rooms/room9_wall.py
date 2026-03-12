"""
Room 9 Wall Texture — "Nirvana" (Transcendence / Pleasure Garden)
Ethereal, dreamy, luminous crystalline walls with sacred geometry,
aurora colors, and divine golden light. Tileable 256x256 pixel art.
"""

import numpy as np
from PIL import Image

SIZE = 256
SEED = 9999

rng = np.random.RandomState(SEED)

# --- Palette ---
BASE_WARM_1 = np.array([220, 200, 150], dtype=np.float64)
BASE_WARM_2 = np.array([200, 190, 160], dtype=np.float64)
BASE_COOL_1 = np.array([180, 170, 210], dtype=np.float64)
BASE_COOL_2 = np.array([170, 180, 200], dtype=np.float64)
CRYSTAL_HIGHLIGHT = np.array([255, 250, 220], dtype=np.float64)
CRYSTAL_FACET = np.array([200, 220, 240], dtype=np.float64)
SACRED_GOLD = np.array([200, 180, 100], dtype=np.float64)
STAR_BRIGHT = np.array([255, 255, 240], dtype=np.float64)
GARDEN_GREEN = np.array([150, 180, 120], dtype=np.float64)
LIGHT_RAY = np.array([240, 230, 190], dtype=np.float64)


def tileable_noise(size, scale, rng):
    """Generate tileable Perlin-like noise using seamless sine combinations."""
    x = np.arange(size, dtype=np.float64)
    y = np.arange(size, dtype=np.float64)
    xx, yy = np.meshgrid(x, y)
    noise = np.zeros((size, size), dtype=np.float64)
    for i in range(1, scale + 1):
        freq = 2 * np.pi * i / size
        phase_x = rng.uniform(0, 2 * np.pi)
        phase_y = rng.uniform(0, 2 * np.pi)
        noise += np.sin(xx * freq + phase_x) * np.cos(yy * freq + phase_y) / i
        phase_x2 = rng.uniform(0, 2 * np.pi)
        phase_y2 = rng.uniform(0, 2 * np.pi)
        noise += np.cos(xx * freq + phase_x2) * np.sin(yy * freq + phase_y2) / i
    # Normalize to 0..1
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-10)
    return noise


def blend(color_a, color_b, t):
    """Blend two colors by factor t (can be array)."""
    if isinstance(t, np.ndarray):
        t = t[..., np.newaxis]
    return color_a * (1 - t) + color_b * t


# Initialize canvas
canvas = np.zeros((SIZE, SIZE, 3), dtype=np.float64)

# --- 1. Base gradient: warm gold <-> cool lavender, tileable ---
grad_noise = tileable_noise(SIZE, 4, rng)
# Secondary noise for variation
grad_noise2 = tileable_noise(SIZE, 2, rng)

# Mix warm colors
warm = blend(BASE_WARM_1, BASE_WARM_2, grad_noise2)
# Mix cool colors
cool = blend(BASE_COOL_1, BASE_COOL_2, grad_noise2)
# Blend warm/cool based on main gradient
canvas = blend(warm, cool, grad_noise)

# --- 2. Crystal / gem facets ---
# Create angular Voronoi-like facets using tileable approach
NUM_CRYSTAL_CENTERS = 16
# Place centers on a grid that tiles
crystal_cx = rng.randint(0, SIZE, NUM_CRYSTAL_CENTERS)
crystal_cy = rng.randint(0, SIZE, NUM_CRYSTAL_CENTERS)

x = np.arange(SIZE, dtype=np.float64)
y = np.arange(SIZE, dtype=np.float64)
xx, yy = np.meshgrid(x, y)

# Compute tileable distance to nearest crystal center
min_dist = np.full((SIZE, SIZE), 1e9)
second_dist = np.full((SIZE, SIZE), 1e9)
nearest_id = np.zeros((SIZE, SIZE), dtype=np.int32)

for i in range(NUM_CRYSTAL_CENTERS):
    # Tileable distance: wrap around
    dx = np.abs(xx - crystal_cx[i])
    dx = np.minimum(dx, SIZE - dx)
    dy = np.abs(yy - crystal_cy[i])
    dy = np.minimum(dy, SIZE - dy)
    # Use Chebyshev distance for angular/faceted look
    dist = np.maximum(dx, dy) + np.minimum(dx, dy) * 0.4
    mask = dist < min_dist
    # Update second closest
    second_dist = np.where(mask, min_dist, np.where(dist < second_dist, dist, second_dist))
    nearest_id = np.where(mask, i, nearest_id)
    min_dist = np.minimum(min_dist, dist)

# Edge detection: where min_dist is close to second_dist
edge_factor = np.clip(1.0 - (second_dist - min_dist) / 8.0, 0, 1)

# Facet coloring: subtle tint per crystal
facet_noise = tileable_noise(SIZE, 6, rng)
facet_tint = facet_noise * 0.15  # subtle

# Apply crystal facet coloring
crystal_blend = np.clip(facet_tint + edge_factor * 0.3, 0, 1)
canvas = blend(canvas, CRYSTAL_FACET, crystal_blend * 0.25)

# Crystal highlights along edges
highlight_mask = edge_factor * facet_noise
canvas = blend(canvas, CRYSTAL_HIGHLIGHT, np.clip(highlight_mask * 0.4, 0, 1))

# --- 3. Sacred geometry: concentric mandala circles with radial lines ---
cx, cy = SIZE / 2, SIZE / 2
# Tileable center positions (we draw from all 9 tile neighbors)
mandala_layer = np.zeros((SIZE, SIZE), dtype=np.float64)

for ox in [-SIZE, 0, SIZE]:
    for oy in [-SIZE, 0, SIZE]:
        dx = xx - (cx + ox)
        dy = yy - (cy + oy)
        r = np.sqrt(dx * dx + dy * dy)
        theta = np.arctan2(dy, dx)

        # Concentric rings at radii 16, 32, 48, 64, 80, 96, 112, 128
        for radius in range(16, SIZE // 2 + 1, 16):
            ring = np.exp(-((r - radius) ** 2) / 2.0)  # thin line
            mandala_layer = np.maximum(mandala_layer, ring)

        # Radial lines every 30 degrees
        for angle_deg in range(0, 360, 30):
            angle = np.radians(angle_deg)
            # Distance from the radial line
            line_dist = np.abs(np.sin(theta - angle)) * r
            radial = np.exp(-(line_dist ** 2) / 1.5) * np.clip(r / 20, 0, 1)
            mandala_layer = np.maximum(mandala_layer, radial * 0.7)

# Apply sacred geometry as thin gold lines
mandala_layer = np.clip(mandala_layer, 0, 1)
canvas = blend(canvas, SACRED_GOLD, mandala_layer * 0.35)

# --- 4. Light rays: diagonal warm beams ---
ray_layer = np.zeros((SIZE, SIZE), dtype=np.float64)
# Multiple rays at different angles, tileable via sine
for i in range(3):
    angle = np.radians(30 + i * 25)
    freq = 2 * np.pi * (2 + i) / SIZE
    projected = xx * np.cos(angle) + yy * np.sin(angle)
    ray = (np.sin(projected * freq) + 1) / 2  # 0..1
    ray = ray ** 4  # sharpen to thin beams
    ray_layer += ray * (0.6 - i * 0.15)

ray_layer = np.clip(ray_layer, 0, 1)
canvas = blend(canvas, LIGHT_RAY, ray_layer * 0.2)

# --- 5. Star / sparkle points ---
num_stars = 40
star_x = rng.randint(0, SIZE, num_stars)
star_y = rng.randint(0, SIZE, num_stars)
star_brightness = rng.uniform(0.3, 1.0, num_stars)

star_layer = np.zeros((SIZE, SIZE), dtype=np.float64)
for i in range(num_stars):
    for ox in [-SIZE, 0, SIZE]:
        for oy in [-SIZE, 0, SIZE]:
            dx = xx - (star_x[i] + ox)
            dy = yy - (star_y[i] + oy)
            dist = np.sqrt(dx * dx + dy * dy)
            # Small bright core + soft glow
            core = np.exp(-(dist ** 2) / 1.5) * star_brightness[i]
            glow = np.exp(-(dist ** 2) / 8.0) * star_brightness[i] * 0.4
            # Cross shape for sparkle
            cross = (np.exp(-(dx ** 2) / 0.8) * np.exp(-(dy ** 2) / 6.0) +
                     np.exp(-(dx ** 2) / 6.0) * np.exp(-(dy ** 2) / 0.8)) * star_brightness[i] * 0.5
            star_layer = np.maximum(star_layer, core + glow + cross)

star_layer = np.clip(star_layer, 0, 1)
canvas = blend(canvas, STAR_BRIGHT, star_layer * 0.7)

# --- 6. Garden / vine hints ---
vine_layer = np.zeros((SIZE, SIZE), dtype=np.float64)
# Organic curves using sine combinations (tileable)
for i in range(4):
    freq_x = 2 * np.pi * (1 + i) / SIZE
    freq_y = 2 * np.pi * (2 + i) / SIZE
    phase = rng.uniform(0, 2 * np.pi)
    # Vine path: thin organic curves
    vine_path = np.sin(xx * freq_x + np.sin(yy * freq_y * 0.5 + phase) * 3)
    vine_thin = np.exp(-(vine_path ** 2) / 0.02)  # very thin line
    vine_layer += vine_thin * 0.3

vine_layer = np.clip(vine_layer, 0, 1)
canvas = blend(canvas, GARDEN_GREEN, vine_layer * 0.15)

# --- 7. Overall warm golden glow (vignette-free since tileable) ---
glow_noise = tileable_noise(SIZE, 3, rng)
canvas = blend(canvas, CRYSTAL_HIGHLIGHT, glow_noise * 0.08)

# --- 8. Slight dithering for pixel art feel ---
dither = rng.uniform(-3, 3, (SIZE, SIZE, 3))
canvas += dither

# Clamp and convert
canvas = np.clip(canvas, 0, 255).astype(np.uint8)

# Save
img = Image.fromarray(canvas, mode='RGB')
img.save('../../docs/assets/rooms/room9_wall.png')
print(f"Saved output.png: {img.size[0]}x{img.size[1]}")
