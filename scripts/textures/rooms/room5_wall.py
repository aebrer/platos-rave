"""
Room 5 Wall Texture — "Barometric Pressure"
Submarine/pressure chamber aesthetic: riveted steel panels, pipes, condensation,
hazard stripes, emergency lighting. Deep blue-green underwater feel.
256x256, tileable/seamless, pixel art dungeon-crawler style.
"""

import numpy as np
from PIL import Image

SIZE = 256
PANEL = 64  # panel size — divides 256 evenly

rng = np.random.RandomState(42)

# Initialize canvas
img = np.zeros((SIZE, SIZE, 3), dtype=np.float64)


def wrap(v, mod=SIZE):
    return v % mod


def draw_pixel(img, x, y, color, alpha=1.0):
    """Draw a single pixel with alpha blending, wrapping coordinates."""
    wx, wy = wrap(x), wrap(y)
    img[wy, wx] = img[wy, wx] * (1 - alpha) + np.array(color, dtype=np.float64) * alpha


def draw_rect(img, x, y, w, h, color, alpha=1.0):
    """Draw a filled rectangle with wrapping."""
    for dy in range(h):
        for dx in range(w):
            draw_pixel(img, x + dx, y + dy, color, alpha)


def draw_hline(img, x, y, length, color, alpha=1.0):
    for dx in range(length):
        draw_pixel(img, x + dx, y, color, alpha)


def draw_vline(img, x, y, length, color, alpha=1.0):
    for dy in range(length):
        draw_pixel(img, x, y + dy, color, alpha)


def draw_circle_outline(img, cx, cy, r, color, alpha=1.0):
    """Midpoint circle algorithm with wrapping."""
    x, y = r, 0
    d = 1 - r
    while x >= y:
        for px, py in [(cx+x, cy+y), (cx-x, cy+y), (cx+x, cy-y), (cx-x, cy-y),
                        (cx+y, cy+x), (cx-y, cy+x), (cx+y, cy-x), (cx-y, cy-x)]:
            draw_pixel(img, px, py, color, alpha)
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1


def draw_filled_circle(img, cx, cy, r, color, alpha=1.0):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                draw_pixel(img, cx + dx, cy + dy, color, alpha)


# ============================================================
# STEP 1: Base steel panel fill with brushed metal texture
# ============================================================
# Fill with base steel color + subtle horizontal streaks
for y in range(SIZE):
    for x in range(SIZE):
        # Base steel with blue-green tint
        base = np.array([62, 72, 85], dtype=np.float64)
        # Brushed metal: subtle horizontal streaks
        streak = rng.randint(-4, 5)
        # Slight variation per-pixel for grit
        grit = rng.randint(-3, 4)
        val = base + streak + grit
        # Add very subtle large-scale variation (per panel position)
        panel_var = ((x // PANEL + y // PANEL) % 3 - 1) * 3
        val = val + panel_var
        img[y, x] = np.clip(val, 0, 255)


# ============================================================
# STEP 2: Panel seams — dark recessed lines every PANEL pixels
# ============================================================
seam_color = (30, 35, 40)
seam_highlight = (85, 95, 108)  # subtle light edge next to seam

for i in range(SIZE // PANEL):
    pos = i * PANEL
    # Horizontal seams
    draw_hline(img, 0, wrap(pos), SIZE, seam_color)
    draw_hline(img, 0, wrap(pos + 1), SIZE, seam_color)
    draw_hline(img, 0, wrap(pos + 2), SIZE, seam_highlight, 0.3)  # light edge below
    draw_hline(img, 0, wrap(pos - 1), SIZE, (20, 25, 30), 0.5)   # shadow above
    # Vertical seams
    draw_vline(img, wrap(pos), 0, SIZE, seam_color)
    draw_vline(img, wrap(pos + 1), 0, SIZE, seam_color)
    draw_vline(img, wrap(pos + 2), 0, SIZE, seam_highlight, 0.3)
    draw_vline(img, wrap(pos - 1), 0, SIZE, (20, 25, 30), 0.5)


# ============================================================
# STEP 3: Rivets along panel edges
# ============================================================
rivet_color = (120, 130, 140)
rivet_shadow = (45, 50, 58)
rivet_spacing = 10

for panel_row in range(SIZE // PANEL):
    for panel_col in range(SIZE // PANEL):
        px0 = panel_col * PANEL
        py0 = panel_row * PANEL
        # Rivets along top edge of each panel
        for rx in range(rivet_spacing // 2, PANEL, rivet_spacing):
            # Top edge rivets (3px below seam)
            ry_top = py0 + 4
            draw_pixel(img, px0 + rx, ry_top, rivet_shadow)
            draw_pixel(img, px0 + rx + 1, ry_top, rivet_shadow)
            draw_pixel(img, px0 + rx, ry_top - 1, rivet_color)
            draw_pixel(img, px0 + rx + 1, ry_top - 1, rivet_color)
            # Bright highlight on rivet
            draw_pixel(img, px0 + rx, ry_top - 1, (140, 150, 160), 0.5)

            # Bottom edge rivets
            ry_bot = py0 + PANEL - 5
            draw_pixel(img, px0 + rx, ry_bot, rivet_shadow)
            draw_pixel(img, px0 + rx + 1, ry_bot, rivet_shadow)
            draw_pixel(img, px0 + rx, ry_bot + 1, rivet_color)
            draw_pixel(img, px0 + rx + 1, ry_bot + 1, rivet_color)
            draw_pixel(img, px0 + rx, ry_bot + 1, (140, 150, 160), 0.5)

        # Rivets along left and right edges
        for ry in range(rivet_spacing // 2, PANEL, rivet_spacing):
            # Left edge
            rx_left = px0 + 4
            draw_pixel(img, rx_left, py0 + ry, rivet_shadow)
            draw_pixel(img, rx_left, py0 + ry + 1, rivet_shadow)
            draw_pixel(img, rx_left - 1, py0 + ry, rivet_color)
            draw_pixel(img, rx_left - 1, py0 + ry + 1, rivet_color)

            # Right edge
            rx_right = px0 + PANEL - 5
            draw_pixel(img, rx_right, py0 + ry, rivet_shadow)
            draw_pixel(img, rx_right, py0 + ry + 1, rivet_shadow)
            draw_pixel(img, rx_right + 1, py0 + ry, rivet_color)
            draw_pixel(img, rx_right + 1, py0 + ry + 1, rivet_color)


# ============================================================
# STEP 4: Horizontal pipe/conduit — runs across specific panels
# ============================================================
# Place a pipe at y=96 (between panel rows 1 and 2 area), spanning full width
pipe_y = 96
pipe_radius = 4
pipe_body = (50, 55, 60)
pipe_highlight = (90, 100, 110)
pipe_shadow = (30, 33, 38)

for x in range(SIZE):
    for dy in range(-pipe_radius, pipe_radius + 1):
        py = wrap(pipe_y + dy)
        dist = abs(dy)
        if dist <= pipe_radius:
            if dy <= -pipe_radius + 1:
                draw_pixel(img, x, py, pipe_highlight, 0.9)
            elif dy >= pipe_radius - 1:
                draw_pixel(img, x, py, pipe_shadow, 0.9)
            else:
                # Gradient from highlight to shadow
                t = (dy + pipe_radius) / (2 * pipe_radius)
                c = tuple(int(pipe_highlight[i] * (1 - t) + pipe_body[i] * t) for i in range(3))
                draw_pixel(img, x, py, c, 0.95)

# Pipe bracket/clamp every 64px
for bx in range(0, SIZE, 64):
    draw_rect(img, bx + 28, pipe_y - pipe_radius - 2, 8, 2, (75, 80, 88))
    draw_rect(img, bx + 28, pipe_y + pipe_radius + 1, 8, 2, (75, 80, 88))
    # Bracket bolt
    draw_pixel(img, bx + 32, pipe_y - pipe_radius - 3, rivet_color)
    draw_pixel(img, bx + 32, pipe_y + pipe_radius + 3, rivet_color)


# ============================================================
# STEP 5: Second pipe — vertical, offset for visual interest
# ============================================================
vpipe_x = 192
vpipe_radius = 3

for y in range(SIZE):
    for dx in range(-vpipe_radius, vpipe_radius + 1):
        px = wrap(vpipe_x + dx)
        dist = abs(dx)
        if dist <= vpipe_radius:
            if dx <= -vpipe_radius + 1:
                draw_pixel(img, px, y, pipe_highlight, 0.85)
            elif dx >= vpipe_radius - 1:
                draw_pixel(img, px, y, pipe_shadow, 0.85)
            else:
                t = (dx + vpipe_radius) / (2 * vpipe_radius)
                c = tuple(int(pipe_highlight[i] * (1 - t) + pipe_body[i] * t) for i in range(3))
                draw_pixel(img, px, y, c, 0.9)

# Vertical pipe brackets
for by in range(0, SIZE, 64):
    draw_rect(img, vpipe_x - vpipe_radius - 2, by + 28, 2, 8, (75, 80, 88))
    draw_rect(img, vpipe_x + vpipe_radius + 1, by + 28, 2, 8, (75, 80, 88))


# ============================================================
# STEP 6: Pressure gauge / porthole
# ============================================================
# Place in panel (1,1) center — at (96, 160) for visual balance
gauge_cx, gauge_cy = 32, 160
gauge_r = 10

# Outer ring
draw_circle_outline(img, gauge_cx, gauge_cy, gauge_r, (90, 100, 110))
draw_circle_outline(img, gauge_cx, gauge_cy, gauge_r + 1, (50, 55, 62))
draw_circle_outline(img, gauge_cx, gauge_cy, gauge_r - 1, (80, 90, 100))

# Fill inner with dark (deep porthole look)
draw_filled_circle(img, gauge_cx, gauge_cy, gauge_r - 2, (15, 25, 35))

# Glass reflection — small bright arc
for angle_idx in range(4):
    rx = gauge_cx - 3 + angle_idx
    ry = gauge_cy - 4
    draw_pixel(img, rx, ry, (100, 120, 140), 0.6)

# Pressure indicator line (needle)
for dy in range(-5, 2):
    draw_pixel(img, gauge_cx + 1, gauge_cy + dy, (160, 50, 40), 0.7)

# Small tick marks around gauge
for tick in range(8):
    import math
    angle = tick * math.pi / 4
    tx = int(gauge_cx + (gauge_r - 3) * math.cos(angle))
    ty = int(gauge_cy + (gauge_r - 3) * math.sin(angle))
    draw_pixel(img, tx, ty, (110, 120, 130), 0.5)

# Second gauge on opposite side of texture for tileability
gauge2_cx, gauge2_cy = 160, 32
gauge2_r = 8
draw_circle_outline(img, gauge2_cx, gauge2_cy, gauge2_r, (85, 95, 105))
draw_circle_outline(img, gauge2_cx, gauge2_cy, gauge2_r + 1, (48, 53, 60))
draw_filled_circle(img, gauge2_cx, gauge2_cy, gauge2_r - 2, (18, 28, 38))
# Glass highlight
for i in range(3):
    draw_pixel(img, gauge2_cx - 2 + i, gauge2_cy - 3, (95, 115, 135), 0.5)


# ============================================================
# STEP 7: Hazard stripes — diagonal yellow/black bands
# ============================================================
# Place a hazard stripe band near the bottom of one panel row
hazard_y = 224  # in the bottom panel row
hazard_height = 8
hazard_yellow = (180, 160, 40)
hazard_black = (40, 40, 40)
stripe_width = 8

for y in range(hazard_height):
    for x in range(SIZE):
        hy = wrap(hazard_y + y)
        # Diagonal stripes: use (x + y) to create diagonal
        stripe_phase = ((x + y) // stripe_width) % 2
        color = hazard_yellow if stripe_phase == 0 else hazard_black
        draw_pixel(img, x, hy, color, 0.85)

# Border lines for hazard stripe
draw_hline(img, 0, wrap(hazard_y - 1), SIZE, (30, 30, 30))
draw_hline(img, 0, wrap(hazard_y + hazard_height), SIZE, (30, 30, 30))

# Second hazard stripe segment — shorter, on a vertical pipe area
# Small vertical hazard warning near vertical pipe
for y in range(12):
    for x in range(8):
        hx = wrap(vpipe_x + pipe_radius + 4 + x)
        hy = wrap(140 + y)
        stripe_phase = ((x + y) // 4) % 2
        color = hazard_yellow if stripe_phase == 0 else hazard_black
        draw_pixel(img, hx, hy, color, 0.8)


# ============================================================
# STEP 8: Condensation drops — scattered bright specks
# ============================================================
condensation_color = (130, 150, 170)
num_drops = 180

for _ in range(num_drops):
    cx = rng.randint(0, SIZE)
    cy = rng.randint(0, SIZE)
    # Avoid drawing on seams (near panel edges)
    local_x = cx % PANEL
    local_y = cy % PANEL
    if local_x < 3 or local_x > PANEL - 3 or local_y < 3 or local_y > PANEL - 3:
        continue
    # Small drop: 1-2 pixels
    drop_size = rng.choice([1, 1, 1, 2])
    alpha = rng.uniform(0.2, 0.5)
    draw_pixel(img, cx, cy, condensation_color, alpha)
    if drop_size == 2:
        # Drip trail below
        draw_pixel(img, cx, wrap(cy + 1), (110, 130, 150), alpha * 0.6)
        # Sometimes a longer drip
        if rng.random() < 0.3:
            draw_pixel(img, cx, wrap(cy + 2), (100, 120, 140), alpha * 0.3)


# ============================================================
# STEP 9: Emergency lighting — blue-green glow from top
# ============================================================
emergency_color = np.array([40, 80, 100], dtype=np.float64)

for y in range(SIZE):
    # Stronger at top (y=0) and bottom (y=255) for tiling continuity
    dist_from_edge = min(y, SIZE - 1 - y)
    # Exponential falloff from edges
    intensity = np.exp(-dist_from_edge / 30.0) * 0.25
    for x in range(SIZE):
        img[y, x] = img[y, x] * (1 - intensity) + emergency_color * intensity

# Also add a subtle point light near the gauge
for y in range(SIZE):
    for x in range(SIZE):
        dx = x - gauge_cx
        dy = y - gauge_cy
        # Wrap-aware distance
        dx = min(abs(dx), SIZE - abs(dx))
        dy = min(abs(dy), SIZE - abs(dy))
        dist = np.sqrt(dx * dx + dy * dy)
        if dist < 30:
            intensity = np.exp(-dist / 12.0) * 0.08
            glow = np.array([50, 90, 110], dtype=np.float64)
            img[y, x] = img[y, x] * (1 - intensity) + glow * intensity


# ============================================================
# STEP 10: Overall blue-green underwater tint
# ============================================================
tint = np.array([0, 10, 20], dtype=np.float64)
img = img + tint
img = np.clip(img, 0, 255)


# ============================================================
# STEP 11: Subtle vignette for claustrophobic feel
# ============================================================
for y in range(SIZE):
    for x in range(SIZE):
        # Distance from center, wrapped for tiling
        dx = min(abs(x - SIZE // 2), SIZE - abs(x - SIZE // 2))
        dy = min(abs(y - SIZE // 2), SIZE - abs(y - SIZE // 2))
        dist = np.sqrt(dx * dx + dy * dy) / (SIZE * 0.5)
        darken = max(0, dist - 0.5) * 0.15
        img[y, x] = img[y, x] * (1 - darken)


# ============================================================
# SAVE
# ============================================================
img = np.clip(img, 0, 255).astype(np.uint8)
output = Image.fromarray(img, 'RGB')
output.save('../../docs/assets/rooms/room5_wall.png')
print(f"Saved output.png: {output.size[0]}x{output.size[1]}")
