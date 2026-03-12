"""
Room 7 Wall Texture — "Traps" (Gothic Circus)
Gothic circus aesthetic: dark velvet curtains with gold trim,
gargoyle-like carvings, theatrical spotlight lighting.
256x256 tileable pixel art for dungeon-crawler.
"""

import numpy as np
from PIL import Image
import math

SIZE = 256
img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

# --- Palette ---
CURTAIN_DARK = np.array([45, 10, 20])
CURTAIN_MID = np.array([60, 15, 25])
CURTAIN_LIGHT = np.array([80, 20, 30])
PURPLE_DARK = np.array([50, 20, 50])
PURPLE_LIGHT = np.array([70, 25, 60])
GOLD_DARK = np.array([140, 120, 50])
GOLD_MID = np.array([180, 150, 60])
GOLD_LIGHT = np.array([200, 170, 80])
BLACK_SHADOW = np.array([15, 5, 10])
SPOTLIGHT_WARM = np.array([120, 80, 40])


def lerp_color(c1, c2, t):
    t = np.clip(t, 0.0, 1.0)
    return (c1 * (1 - t) + c2 * t).astype(np.uint8)


def seamless_noise(x, y, size, scale):
    """Simple value noise that tiles seamlessly using sin/cos mapping onto a torus."""
    # Map to angles
    ax = (x / size) * 2 * math.pi
    ay = (y / size) * 2 * math.pi
    # Project onto torus in 4D, sample with simple hash
    nx = math.cos(ax) * scale
    ny = math.sin(ax) * scale
    nz = math.cos(ay) * scale
    nw = math.sin(ay) * scale
    # Simple pseudo-random hash
    val = math.sin(nx * 12.9898 + ny * 78.233 + nz * 45.164 + nw * 93.989) * 43758.5453
    return val - math.floor(val)


# Precompute noise layers for fabric texture
noise1 = np.zeros((SIZE, SIZE))
noise2 = np.zeros((SIZE, SIZE))
for py in range(SIZE):
    for px in range(SIZE):
        noise1[py, px] = seamless_noise(px, py, SIZE, 2.0)
        noise2[py, px] = seamless_noise(px, py, SIZE, 5.0)

# --- Step 1: Curtain folds (vertical draping) ---
# Use a repeating sine pattern for fold geometry (tileable with period dividing 256)
NUM_FOLDS = 8  # 256 / 8 = 32px per fold
fold_period = SIZE // NUM_FOLDS

for py in range(SIZE):
    for px in range(SIZE):
        # Fold shape: sine wave giving highlight on ridges, dark in valleys
        fold_phase = (px % SIZE) / fold_period * 2 * math.pi
        fold_val = math.sin(fold_phase)  # -1 to 1

        # Add slight vertical variation for gathered look
        gather_phase = (py % SIZE) / SIZE * 2 * math.pi
        gather = math.sin(gather_phase * 3) * 0.1
        fold_val += gather

        # Normalize to 0..1
        t = (fold_val + 1.1) / 2.2
        t = np.clip(t, 0, 1)

        # Base curtain color: dark to light crimson based on fold
        if t < 0.5:
            base = lerp_color(BLACK_SHADOW, CURTAIN_DARK, t * 2)
        else:
            base = lerp_color(CURTAIN_DARK, CURTAIN_LIGHT, (t - 0.5) * 2)

        # Mix in purple on alternating folds
        fold_index = (px // fold_period) % NUM_FOLDS
        if fold_index % 3 == 1:
            purple_t = t
            if purple_t < 0.5:
                purple = lerp_color(BLACK_SHADOW, PURPLE_DARK, purple_t * 2)
            else:
                purple = lerp_color(PURPLE_DARK, PURPLE_LIGHT, (purple_t - 0.5) * 2)
            base = lerp_color(base, purple, 0.6)

        # Add fabric noise texture
        n = noise1[py, px] * 0.15 + noise2[py, px] * 0.08
        base = np.clip(base.astype(float) * (0.85 + n), 0, 255).astype(np.uint8)

        img[py, px] = base

# --- Step 2: Gothic pointed arch tracery pattern in fabric ---
# Repeat every 64px horizontally, 128px vertically (divides 256)
ARCH_W = 64
ARCH_H = 128

for py in range(SIZE):
    for px in range(SIZE):
        lx = px % ARCH_W
        ly = py % ARCH_H

        # Pointed arch shape: two arcs meeting at a point
        cx = ARCH_W // 2
        # Arch starts at ly=ARCH_H-20 (bottom), peaks at ly=10 (top)
        arch_bottom = ARCH_H - 20
        arch_top = 15
        arch_width = 26

        if arch_top < ly < arch_bottom:
            # Calculate arch edge position at this height
            progress = (ly - arch_top) / (arch_bottom - arch_top)  # 0 at top, 1 at bottom
            # Pointed arch: width grows then stays
            if progress < 0.3:
                half_w = arch_width * (progress / 0.3)
            else:
                half_w = arch_width

            dist_from_center = abs(lx - cx)

            # Draw arch outline (2px thick)
            if abs(dist_from_center - half_w) < 2.5:
                # Arch border line in dark gold / shadow
                t_gold = 0.3 + noise1[py, px] * 0.2
                arch_color = lerp_color(CURTAIN_DARK, GOLD_DARK, t_gold)
                img[py, px] = lerp_color(img[py, px], arch_color, 0.5)

            # Inner tracery: vertical line at center
            if dist_from_center < 1.5 and progress > 0.15 and progress < 0.85:
                img[py, px] = lerp_color(img[py, px], GOLD_DARK, 0.25)

            # Trefoil near top of arch
            if progress < 0.4 and progress > 0.15:
                # Small circles for trefoil
                trefoil_y = arch_top + int(0.25 * (arch_bottom - arch_top))
                for ox, oy in [(-8, 0), (8, 0), (0, -8)]:
                    dx = lx - (cx + ox)
                    dy = ly - (trefoil_y + oy)
                    r = math.sqrt(dx * dx + dy * dy)
                    if 4 < r < 6:
                        img[py, px] = lerp_color(img[py, px], GOLD_DARK, 0.3)

# --- Step 3: Gold trim border strips ---
# Two horizontal bands: top and bottom. 16px tall each.
TRIM_H = 16
TRIM_POSITIONS = [0, SIZE - TRIM_H]  # top and bottom (seamless: top of next tile meets bottom)

for trim_y in TRIM_POSITIONS:
    for py in range(trim_y, trim_y + TRIM_H):
        wy = py % SIZE
        for px in range(SIZE):
            # Gold gradient: brighter in center of strip
            strip_pos = (py - trim_y) / TRIM_H  # 0 to 1
            brightness = 1.0 - abs(strip_pos - 0.5) * 2  # peak at center

            # Repeating filigree pattern along strip (period 32, divides 256)
            pat_x = px % 32
            pat_center = 16

            # Diamond / lozenge pattern
            dx = abs(pat_x - pat_center)
            dy = abs(strip_pos - 0.5) * TRIM_H
            diamond = dx + dy

            if diamond < 10:
                if diamond < 3:
                    gold = lerp_color(GOLD_MID, GOLD_LIGHT, brightness)
                elif diamond < 6:
                    gold = lerp_color(GOLD_DARK, GOLD_MID, brightness)
                else:
                    gold = lerp_color(CURTAIN_DARK, GOLD_DARK, brightness * 0.7)
                img[wy, px] = gold
            else:
                # Edge of trim: dark gold border
                if strip_pos < 0.15 or strip_pos > 0.85:
                    img[wy, px] = lerp_color(img[wy, px], GOLD_DARK, 0.6)
                else:
                    img[wy, px] = lerp_color(img[wy, px], GOLD_DARK, 0.3)

            # Small dots between diamonds
            if diamond > 12 and diamond < 14 and abs(strip_pos - 0.5) < 0.15:
                img[wy, px] = lerp_color(img[wy, px], GOLD_LIGHT, 0.5)

# --- Step 4: Tassels hanging from bottom trim ---
TASSEL_SPACING = 16  # divides 256
TASSEL_LENGTH = 20
tassel_start_y = TRIM_H  # just below top trim (which wraps to be bottom of tile above)

for px in range(SIZE):
    tassel_x = px % TASSEL_SPACING
    tassel_center = TASSEL_SPACING // 2

    if abs(tassel_x - tassel_center) < 3:
        for dy in range(TASSEL_LENGTH):
            py = (tassel_start_y + dy) % SIZE
            # Tassel gets thinner toward bottom
            max_width = 3.0 * (1.0 - dy / TASSEL_LENGTH)
            if abs(tassel_x - tassel_center) <= max_width:
                t = dy / TASSEL_LENGTH
                tassel_color = lerp_color(GOLD_MID, GOLD_DARK, t)
                # Add some swing variation
                swing = math.sin(px * 0.5 + dy * 0.3) * 0.15
                tassel_color = np.clip(tassel_color.astype(float) * (1.0 + swing), 0, 255).astype(np.uint8)
                img[py, px] = lerp_color(img[py, px], tassel_color, 0.7)

# --- Step 5: Gargoyle/grotesque face suggestions (subtle) ---
# Place at intersection points of arch pattern, very subtle
FACE_POSITIONS = []
for fx in range(0, SIZE, ARCH_W):
    for fy in range(0, SIZE, ARCH_H):
        FACE_POSITIONS.append((fx + ARCH_W // 2, fy + ARCH_H - 25))

for face_cx, face_cy in FACE_POSITIONS:
    # Simple gargoyle suggestion: dark circular face with eye hollows and mouth
    for dy in range(-10, 11):
        for dx in range(-8, 9):
            px = (face_cx + dx) % SIZE
            py = (face_cy + dy) % SIZE
            r = math.sqrt(dx * dx + dy * dy)

            if r > 10:
                continue

            # Face outline
            face_shade = 0.0
            if 8 < r < 10:
                face_shade = 0.3  # subtle edge

            # Eye hollows
            for eye_ox in [-4, 4]:
                ex = dx - eye_ox
                ey = dy + 2
                er = math.sqrt(ex * ex + ey * ey)
                if er < 2:
                    face_shade = 0.5

            # Mouth
            if abs(dy - 4) < 1.5 and abs(dx) < 3:
                face_shade = 0.4

            # Horns / pointed ears
            if abs(dx) > 5 and dy < -6 and r < 12:
                face_shade = 0.25

            if face_shade > 0:
                dark = lerp_color(img[py, px], BLACK_SHADOW, face_shade)
                img[py, px] = dark

# --- Step 6: Theatrical spotlight from above ---
# Central spotlight beam, seamless horizontally (centered, fades to edges)
spotlight_cx = SIZE // 2
spotlight_width = SIZE * 0.35  # wide enough to look natural

for py in range(SIZE):
    for px in range(SIZE):
        # Distance from center column, wrapping
        dx = px - spotlight_cx
        if dx > SIZE // 2:
            dx -= SIZE
        elif dx < -SIZE // 2:
            dx += SIZE

        # Spotlight intensity: strongest at top-center, fading down and to sides
        horiz_falloff = math.exp(-(dx * dx) / (2 * spotlight_width * spotlight_width))
        # Vertical: brighter near top (y=0)
        vert_factor = 1.0 - (py / SIZE) * 0.6
        intensity = horiz_falloff * vert_factor * 0.2  # subtle

        if intensity > 0.01:
            lit = lerp_color(img[py, px], SPOTLIGHT_WARM, intensity)
            # Also slightly brighten
            bright = np.clip(lit.astype(float) * (1.0 + intensity * 0.3), 0, 255).astype(np.uint8)
            img[py, px] = bright

# --- Step 7: Final dithering pass for pixel art feel ---
# Add ordered dither (Bayer 4x4) to reduce banding
BAYER_4 = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
], dtype=float) / 16.0 - 0.5  # range -0.5 to 0.5

for py in range(SIZE):
    for px in range(SIZE):
        bayer = BAYER_4[py % 4, px % 4]
        pixel = img[py, px].astype(float) + bayer * 6  # subtle dither
        img[py, px] = np.clip(pixel, 0, 255).astype(np.uint8)

# --- Save ---
output_path = "../../docs/assets/rooms/room7_wall.png"
result = Image.fromarray(img, 'RGB')
result.save(output_path)
print(f"Saved {output_path}")
print(f"Size: {result.size}")
