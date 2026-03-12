"""
Room 9 Floor Texture — "Nirvana" (Ethereal Garden Path)
Transcendent pleasure garden floor: marble + gold mosaic + flower petals + inner glow.
256x256 tileable pixel art.

Approach: Use a tileable geometric tile (64x64 repeated 4x4) for the gold inlay,
with marble base, scattered petals, and luminous glow all using modular arithmetic.
"""

import numpy as np
from PIL import Image
import math
import random

random.seed(42)
np.random.seed(42)

SIZE = 256
TILE = 64  # geometric pattern repeats every 64px (divides 256 evenly)
img = np.zeros((SIZE, SIZE, 3), dtype=np.float64)

# --- Palette ---
MARBLE_BASE = np.array([235, 230, 220], dtype=np.float64)
MARBLE_DARK = np.array([225, 218, 205], dtype=np.float64)
MARBLE_WARM = np.array([238, 232, 218], dtype=np.float64)
GOLD_VEIN = np.array([195, 175, 115], dtype=np.float64)
GOLD_INLAY = np.array([205, 185, 105], dtype=np.float64)
GOLD_BRIGHT = np.array([220, 200, 125], dtype=np.float64)
PETAL_PINK = np.array([225, 160, 175], dtype=np.float64)
PETAL_LAVENDER = np.array([185, 165, 215], dtype=np.float64)
PETAL_YELLOW = np.array([235, 225, 165], dtype=np.float64)
GLOW_WHITE = np.array([248, 244, 232], dtype=np.float64)
GREEN_ACCENT = np.array([165, 188, 135], dtype=np.float64)


def blend(base, overlay, alpha):
    """Alpha blend overlay onto base."""
    return base * (1.0 - alpha) + overlay * alpha


# ============================================================
# Step 1: Marble base with tileable veining
# ============================================================
# Use sine waves with frequencies that divide SIZE for perfect tiling
for y in range(SIZE):
    for x in range(SIZE):
        # Multi-scale tileable marble
        v = 0.0
        # Large-scale warm/cool variation
        v += math.sin(2 * math.pi * 2 * x / SIZE) * 0.3
        v += math.sin(2 * math.pi * 3 * y / SIZE + 0.5) * 0.25
        v += math.sin(2 * math.pi * 4 * (x + y) / SIZE + 1.2) * 0.15
        v += math.sin(2 * math.pi * 5 * (x - y) / SIZE + 2.8) * 0.1

        # Marble vein pattern: sharp veins from sine distortion
        vein_raw = math.sin(
            2 * math.pi * 3 * x / SIZE
            + math.sin(2 * math.pi * 2 * y / SIZE) * 1.5
            + math.sin(2 * math.pi * 5 * y / SIZE) * 0.5
        )
        # Sharpen into thin veins
        vein = max(0, 1.0 - abs(vein_raw) * 4.0)  # thin bright lines where sine crosses zero
        vein2_raw = math.sin(
            2 * math.pi * 2 * y / SIZE
            + math.sin(2 * math.pi * 3 * x / SIZE) * 1.2
            + math.sin(2 * math.pi * 4 * x / SIZE) * 0.4
        )
        vein2 = max(0, 1.0 - abs(vein2_raw) * 5.0)

        combined_vein = min(1.0, vein * 0.5 + vein2 * 0.35)

        # Base color: blend between warm and cool marble
        t = (v + 1.0) / 2.0  # normalize to 0-1
        base_color = MARBLE_BASE * t + MARBLE_DARK * (1.0 - t)
        # Warm spots
        warm = math.sin(2 * math.pi * 1 * x / SIZE + 0.3) * math.sin(2 * math.pi * 1 * y / SIZE + 0.7)
        warm = max(0, warm) * 0.15
        base_color = blend(base_color, MARBLE_WARM, warm)

        # Apply gold veining
        base_color = blend(base_color, GOLD_VEIN, combined_vein * 0.6)

        img[y, x] = base_color

# ============================================================
# Step 2: Sacred geometry gold inlay — tileable 64x64 pattern
# ============================================================
# Draw within a TILE-sized pattern, repeated across the texture
TC = TILE // 2  # center of tile = 32

for y in range(SIZE):
    for x in range(SIZE):
        tx = x % TILE  # position within tile
        ty = y % TILE
        # Distance from tile center
        dx = tx - TC
        dy = ty - TC
        d = math.sqrt(dx * dx + dy * dy)
        angle = math.atan2(dy, dx)

        gold_strength = 0.0

        # --- Concentric circle rings ---
        for radius in [8, 16, 24, 30]:
            ring_dist = abs(d - radius)
            if ring_dist < 1.2:
                s = (1.0 - ring_dist / 1.2)
                gold_strength = max(gold_strength, s * 0.85)

        # --- 8-pointed radial star ---
        if d > 3 and d < 31:
            for n_points in [8]:
                star_angle = (angle * n_points / (2 * math.pi)) % 1.0
                star_dist = min(star_angle, 1.0 - star_angle) * 2.0
                if star_dist < 0.07:
                    s = (1.0 - star_dist / 0.07) * 0.9
                    gold_strength = max(gold_strength, s)

            # Secondary 8-pointed star rotated 22.5 degrees
            angle2 = angle + math.pi / 8
            star_angle2 = (angle2 * 8 / (2 * math.pi)) % 1.0
            star_dist2 = min(star_angle2, 1.0 - star_angle2) * 2.0
            if star_dist2 < 0.05 and d > 6 and d < 28:
                s = (1.0 - star_dist2 / 0.05) * 0.6
                gold_strength = max(gold_strength, s)

        # --- Small center dot ---
        if d < 3:
            gold_strength = max(gold_strength, 0.9 * (1.0 - d / 3))

        # --- Corner diamonds (at tile corners = where 4 tiles meet) ---
        # Distance from nearest corner
        corner_dx = min(tx, TILE - tx)
        corner_dy = min(ty, TILE - ty)
        corner_d = corner_dx + corner_dy  # Manhattan distance for diamond shape
        if corner_d < 6:
            s = (1.0 - corner_d / 6) * 0.7
            gold_strength = max(gold_strength, s)
        # Diamond outline
        if abs(corner_d - 8) < 1.0:
            s = (1.0 - abs(corner_d - 8)) * 0.5
            gold_strength = max(gold_strength, s)

        # --- Outer border square (tile edges) ---
        edge_dist = min(tx, ty, TILE - 1 - tx, TILE - 1 - ty)
        if edge_dist < 1:
            gold_strength = max(gold_strength, 0.5)

        if gold_strength > 0.01:
            gc = blend(GOLD_INLAY, GOLD_BRIGHT, gold_strength * 0.4)
            img[y, x] = blend(img[y, x], gc, gold_strength)

# ============================================================
# Step 3: Inner luminous glow — per tile, brighter near center
# ============================================================
for y in range(SIZE):
    for x in range(SIZE):
        tx = x % TILE
        ty = y % TILE
        dx = tx - TC
        dy = ty - TC
        d = math.sqrt(dx * dx + dy * dy)

        # Soft glow near tile center
        glow = math.exp(-(d * d) / (12 * 12)) * 0.2
        # Ring glow at the mid-ring
        glow += math.exp(-((d - 16) ** 2) / (4 * 4)) * 0.08

        if glow > 0.01:
            img[y, x] = blend(img[y, x], GLOW_WHITE, glow)

# ============================================================
# Step 4: Flower petals — scattered 2-3px clusters, tileable grid
# ============================================================
petal_colors = [PETAL_PINK, PETAL_LAVENDER, PETAL_YELLOW, PETAL_PINK, PETAL_LAVENDER]
petal_grid = 32  # must divide 256

# Pre-generate petal cluster positions per grid cell
petal_clusters = []
for gy in range(0, SIZE, petal_grid):
    for gx in range(0, SIZE, petal_grid):
        if random.random() < 0.45:
            px = (gx + random.randint(4, petal_grid - 5)) % SIZE
            py = (gy + random.randint(4, petal_grid - 5)) % SIZE
            color = random.choice(petal_colors)
            n_pixels = random.randint(3, 6)
            petal_clusters.append((px, py, color, n_pixels))

for px, py, color, n_pixels in petal_clusters:
    for _ in range(n_pixels):
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        if abs(dx) + abs(dy) > 3:
            continue  # keep clusters compact
        fx = (px + dx) % SIZE
        fy = (py + dy) % SIZE
        strength = 0.55 + random.random() * 0.35
        img[fy, fx] = blend(img[fy, fx], color, strength)

# ============================================================
# Step 5: Green accent dots — subtle plant hints near tile edges
# ============================================================
green_grid = 32
for gy in range(0, SIZE, green_grid):
    for gx in range(0, SIZE, green_grid):
        # Only place near tile border areas
        tx = gx % TILE
        ty = gy % TILE
        edge = min(tx, ty, TILE - 1 - tx, TILE - 1 - ty)
        if edge < 10 and random.random() < 0.3:
            for _ in range(random.randint(1, 3)):
                fx = (gx + random.randint(-2, 2)) % SIZE
                fy = (gy + random.randint(-2, 2)) % SIZE
                strength = 0.25 + random.random() * 0.2
                img[fy, fx] = blend(img[fy, fx], GREEN_ACCENT, strength)

# ============================================================
# Step 6: Subtle dithering for pixel art feel
# ============================================================
noise = np.random.randint(-3, 4, size=(SIZE, SIZE, 3)).astype(np.float64)
img = np.clip(img + noise, 0, 255)

# ============================================================
# Save
# ============================================================
output = Image.fromarray(img.astype(np.uint8), 'RGB')
output.save('../../docs/assets/rooms/room9_floor.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
