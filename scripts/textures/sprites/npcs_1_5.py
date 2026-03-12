"""
Generate NPC sprites for Plato's Rave rooms 1-5.

Each room gets 3 PNGs: head (14x14), torso (10x20), legs (8x12).
All sprites are RGBA with transparent backgrounds, pixel art at 1x scale.
"""

from PIL import Image
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../docs/assets/sprites/npcs")


def make_image(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def p(img, x, y, color):
    """Set pixel if in bounds. Color is (r,g,b) or (r,g,b,a)."""
    if 0 <= x < img.width and 0 <= y < img.height:
        if len(color) == 3:
            color = color + (255,)
        img.putpixel((x, y), color)


def rect(img, x0, y0, w, h, color):
    for yy in range(y0, y0 + h):
        for xx in range(x0, x0 + w):
            p(img, xx, yy, color)


def hline(img, x0, x1, y, color):
    for xx in range(x0, x1 + 1):
        p(img, xx, y, color)


def vline(img, x, y0, y1, color):
    for yy in range(y0, y1 + 1):
        p(img, x, yy, color)


# =============================================================================
# Room 1 — Container Store Shoppers
# =============================================================================
def room1():
    khaki = (195, 180, 150)
    beige = (210, 195, 170)
    light_blue = (150, 175, 200)
    skin = (220, 190, 160)
    hair = (140, 110, 80)
    eye = (60, 50, 40)
    shoe = (120, 100, 80)

    # HEAD 14x14
    img = make_image(14, 14)
    # Hair (short, clean-cut) - top of head
    rect(img, 4, 0, 6, 2, hair)
    rect(img, 3, 1, 8, 2, hair)
    # Face
    rect(img, 4, 3, 6, 7, skin)
    rect(img, 3, 4, 8, 5, skin)
    # Headband
    hline(img, 3, 10, 3, light_blue)
    hline(img, 4, 9, 2, light_blue)
    # Eyes
    p(img, 5, 6, eye)
    p(img, 8, 6, eye)
    # Mouth
    hline(img, 6, 7, 9, (180, 130, 110))
    # Ears
    p(img, 3, 6, skin)
    p(img, 10, 6, skin)
    # Chin
    rect(img, 5, 10, 4, 1, skin)
    # Neck
    rect(img, 5, 11, 4, 3, skin)
    img.save(os.path.join(OUTPUT_DIR, "room1", "head.png"))

    # TORSO 10x20
    img = make_image(10, 20)
    # Polo shirt body
    rect(img, 1, 0, 8, 16, light_blue)
    # Collar
    rect(img, 3, 0, 4, 2, beige)
    p(img, 4, 1, light_blue)
    p(img, 5, 1, light_blue)
    # Sleeves
    rect(img, 0, 2, 2, 5, light_blue)
    rect(img, 8, 2, 2, 5, light_blue)
    # Arms below sleeve
    rect(img, 0, 7, 2, 4, skin)
    rect(img, 8, 7, 2, 4, skin)
    # Shopping bag (right hand)
    rect(img, 8, 11, 2, 7, khaki)
    hline(img, 8, 9, 11, (170, 155, 130))
    # Bottom hem
    hline(img, 1, 8, 16, (130, 155, 180))
    # Belt area
    rect(img, 1, 16, 8, 1, (160, 140, 110))
    # Top of pants visible
    rect(img, 1, 17, 8, 3, khaki)
    img.save(os.path.join(OUTPUT_DIR, "room1", "torso.png"))

    # LEGS 8x12
    img = make_image(8, 12)
    # Left leg
    rect(img, 0, 0, 3, 9, khaki)
    # Right leg
    rect(img, 5, 0, 3, 9, khaki)
    # Shoes
    rect(img, 0, 9, 3, 3, shoe)
    rect(img, 5, 9, 3, 3, shoe)
    # Shoe detail
    hline(img, 0, 2, 9, (100, 80, 60))
    hline(img, 5, 7, 9, (100, 80, 60))
    img.save(os.path.join(OUTPUT_DIR, "room1", "legs.png"))


# =============================================================================
# Room 2 — Warehouse Employees
# =============================================================================
def room2():
    hi_vis = (255, 165, 50)
    stripe = (250, 250, 220)
    dark_pants = (60, 60, 70)
    yellow = (240, 220, 60)
    skin = (200, 170, 140)
    eye = (50, 40, 30)
    boot = (50, 45, 40)

    # HEAD 14x14 — hard hat
    img = make_image(14, 14)
    # Hard hat (yellow)
    rect(img, 3, 0, 8, 3, yellow)
    rect(img, 2, 2, 10, 2, yellow)
    # Hat brim
    hline(img, 1, 12, 4, (220, 200, 50))
    # Face
    rect(img, 4, 5, 6, 5, skin)
    rect(img, 3, 6, 8, 3, skin)
    # Eyes
    p(img, 5, 7, eye)
    p(img, 8, 7, eye)
    # Mouth
    hline(img, 6, 7, 9, (170, 130, 110))
    # Chin
    rect(img, 5, 10, 4, 1, skin)
    # Neck
    rect(img, 5, 11, 4, 3, skin)
    img.save(os.path.join(OUTPUT_DIR, "room2", "head.png"))

    # TORSO 10x20 — hi-vis vest
    img = make_image(10, 20)
    # Base shirt (dark)
    rect(img, 1, 0, 8, 17, (80, 80, 90))
    # Hi-vis vest overlay
    rect(img, 2, 1, 6, 14, hi_vis)
    # Reflective stripes
    hline(img, 1, 8, 5, stripe)
    hline(img, 1, 8, 6, stripe)
    hline(img, 1, 8, 11, stripe)
    hline(img, 1, 8, 12, stripe)
    # Vest opening (dark center line)
    vline(img, 5, 1, 14, (80, 80, 90))
    # Sleeves
    rect(img, 0, 2, 2, 5, (80, 80, 90))
    rect(img, 8, 2, 2, 5, (80, 80, 90))
    # Arms
    rect(img, 0, 7, 2, 5, skin)
    rect(img, 8, 7, 2, 5, skin)
    # Belt
    hline(img, 1, 8, 16, (90, 80, 50))
    # Top of pants
    rect(img, 1, 17, 8, 3, dark_pants)
    img.save(os.path.join(OUTPUT_DIR, "room2", "torso.png"))

    # LEGS 8x12
    img = make_image(8, 12)
    # Left leg
    rect(img, 0, 0, 3, 8, dark_pants)
    # Right leg
    rect(img, 5, 0, 3, 8, dark_pants)
    # Steel-toe boots (chunkier)
    rect(img, 0, 8, 4, 4, boot)
    rect(img, 4, 8, 4, 4, boot)
    # Steel toe cap
    hline(img, 0, 3, 8, (100, 95, 90))
    hline(img, 4, 7, 8, (100, 95, 90))
    img.save(os.path.join(OUTPUT_DIR, "room2", "legs.png"))


# =============================================================================
# Room 3 — Wing-Eating Bar Patrons
# =============================================================================
def room3():
    jersey_red = (200, 50, 40)
    denim = (80, 80, 110)
    sauce = (220, 130, 50)
    cap_color = (50, 80, 150)
    skin = (210, 180, 150)
    eye = (50, 40, 30)
    sneaker = (200, 200, 200)

    # HEAD 14x14 — baseball cap
    img = make_image(14, 14)
    # Cap crown
    rect(img, 3, 0, 8, 3, cap_color)
    rect(img, 2, 1, 10, 2, cap_color)
    # Cap brim (extends forward)
    rect(img, 2, 3, 8, 2, (40, 65, 130))
    # Face
    rect(img, 4, 5, 6, 5, skin)
    rect(img, 3, 6, 8, 3, skin)
    # Eyes
    p(img, 5, 7, eye)
    p(img, 8, 7, eye)
    # Mouth / sauce stain on chin area
    hline(img, 6, 7, 9, sauce)
    p(img, 5, 10, sauce)
    p(img, 7, 10, sauce)
    # Clean chin
    rect(img, 5, 10, 4, 1, skin)
    p(img, 6, 10, sauce)  # just a dab of sauce
    # Neck
    rect(img, 5, 11, 4, 3, skin)
    img.save(os.path.join(OUTPUT_DIR, "room3", "head.png"))

    # TORSO 10x20 — sports jersey
    img = make_image(10, 20)
    # Jersey body
    rect(img, 1, 0, 8, 15, jersey_red)
    # Jersey number (white stripe pattern)
    white = (240, 235, 230)
    # Number "7" approximation
    hline(img, 4, 6, 5, white)
    vline(img, 6, 5, 10, white)
    # Collar
    rect(img, 3, 0, 4, 1, white)
    # Sleeve edges
    hline(img, 0, 1, 2, jersey_red)
    hline(img, 8, 9, 2, jersey_red)
    rect(img, 0, 2, 2, 5, jersey_red)
    rect(img, 8, 2, 2, 5, jersey_red)
    # Napkin tucked in (white at collar)
    rect(img, 4, 1, 2, 3, white)
    # Arms
    rect(img, 0, 7, 2, 5, skin)
    rect(img, 8, 7, 2, 5, skin)
    # Sauce on hand
    p(img, 9, 10, sauce)
    p(img, 9, 11, sauce)
    # Belt/waist
    hline(img, 1, 8, 15, (70, 70, 100))
    # Jeans start
    rect(img, 1, 16, 8, 4, denim)
    img.save(os.path.join(OUTPUT_DIR, "room3", "torso.png"))

    # LEGS 8x12
    img = make_image(8, 12)
    # Left leg (jeans)
    rect(img, 0, 0, 3, 9, denim)
    # Right leg (jeans)
    rect(img, 5, 0, 3, 9, denim)
    # Sneakers
    rect(img, 0, 9, 3, 3, sneaker)
    rect(img, 5, 9, 3, 3, sneaker)
    # Sneaker stripe
    hline(img, 0, 2, 10, jersey_red)
    hline(img, 5, 7, 10, jersey_red)
    img.save(os.path.join(OUTPUT_DIR, "room3", "legs.png"))


# =============================================================================
# Room 4 — Peak Ravers
# =============================================================================
def room4():
    neon_pink = (255, 50, 200)
    electric_blue = (50, 150, 255)
    acid_green = (100, 255, 50)
    black_base = (20, 15, 30)
    dark_skin = (180, 150, 130)
    eye = (200, 200, 255)

    # HEAD 14x14 — wild neon hair + face paint
    img = make_image(14, 14)
    # Wild neon hair (spiked up)
    p(img, 5, 0, neon_pink)
    p(img, 7, 0, acid_green)
    p(img, 9, 0, electric_blue)
    rect(img, 4, 1, 7, 2, neon_pink)
    p(img, 6, 1, acid_green)
    p(img, 8, 1, electric_blue)
    rect(img, 3, 2, 8, 2, neon_pink)
    p(img, 5, 2, electric_blue)
    p(img, 9, 2, acid_green)
    # LED headband
    hline(img, 3, 10, 4, electric_blue)
    p(img, 4, 4, acid_green)
    p(img, 6, 4, neon_pink)
    p(img, 8, 4, acid_green)
    # Face
    rect(img, 4, 5, 6, 5, dark_skin)
    rect(img, 3, 6, 8, 3, dark_skin)
    # Face paint streaks
    p(img, 3, 6, neon_pink)
    p(img, 10, 6, electric_blue)
    p(img, 4, 8, acid_green)
    p(img, 9, 8, neon_pink)
    # Eyes (bright/wide)
    p(img, 5, 7, eye)
    p(img, 8, 7, eye)
    # Mouth (grinning)
    hline(img, 5, 8, 9, (220, 180, 160))
    # Neck
    rect(img, 5, 11, 4, 3, dark_skin)
    img.save(os.path.join(OUTPUT_DIR, "room4", "head.png"))

    # TORSO 10x20 — fishnet/mesh over dark base, glow sticks
    img = make_image(10, 20)
    # Dark base
    rect(img, 1, 0, 8, 17, black_base)
    # Fishnet pattern (alternating dots of neon)
    for y in range(1, 16, 2):
        for x in range(1, 9, 2):
            colors = [neon_pink, electric_blue, acid_green]
            c = colors[(x + y) % 3]
            p(img, x, y, c)
    # Mesh lines (semi-transparent neon)
    for y in range(0, 16, 3):
        for x in range(1, 9):
            c = [neon_pink, electric_blue, acid_green][(y // 3) % 3]
            p(img, x, y, (c[0], c[1], c[2], 120))
    # Glow stick necklace
    hline(img, 2, 7, 2, acid_green)
    hline(img, 3, 6, 3, acid_green)
    # Arms (with glow bracelets)
    rect(img, 0, 2, 1, 9, black_base)
    rect(img, 9, 2, 1, 9, black_base)
    p(img, 0, 7, neon_pink)
    p(img, 0, 8, neon_pink)
    p(img, 9, 7, electric_blue)
    p(img, 9, 8, electric_blue)
    # Waist
    hline(img, 1, 8, 16, neon_pink)
    # Pants start
    rect(img, 1, 17, 8, 3, black_base)
    # Neon stripe on pants
    vline(img, 2, 17, 19, acid_green)
    vline(img, 7, 17, 19, electric_blue)
    img.save(os.path.join(OUTPUT_DIR, "room4", "torso.png"))

    # LEGS 8x12 — baggy rave pants with neon, platforms
    img = make_image(8, 12)
    # Left leg (baggy)
    rect(img, 0, 0, 4, 8, black_base)
    # Right leg (baggy)
    rect(img, 4, 0, 4, 8, black_base)
    # Neon stripes down sides
    vline(img, 0, 0, 7, neon_pink)
    vline(img, 3, 0, 7, acid_green)
    vline(img, 4, 0, 7, electric_blue)
    vline(img, 7, 0, 7, neon_pink)
    # Platform shoes (tall, chunky)
    rect(img, 0, 8, 4, 4, (40, 30, 50))
    rect(img, 4, 8, 4, 4, (40, 30, 50))
    # Platform soles (thick, neon)
    hline(img, 0, 3, 11, neon_pink)
    hline(img, 4, 7, 11, electric_blue)
    img.save(os.path.join(OUTPUT_DIR, "room4", "legs.png"))


# =============================================================================
# Room 5 — Pressure-Suited Divers
# =============================================================================
def room5():
    suit = (60, 70, 90)
    glass = (100, 150, 180)
    panel = (80, 90, 100)
    rim = (45, 50, 60)
    flipper = (50, 60, 50)
    hose = (70, 75, 85)
    glass_hi = (130, 180, 210, 180)  # semi-transparent highlight

    # HEAD 14x14 — diving helmet with glass dome
    img = make_image(14, 14)
    # Helmet outer rim
    rect(img, 2, 1, 10, 11, rim)
    # Helmet body
    rect(img, 3, 0, 8, 11, suit)
    rect(img, 2, 2, 10, 8, suit)
    # Glass dome (round)
    rect(img, 4, 2, 6, 8, glass)
    rect(img, 3, 3, 8, 6, glass)
    # Glass highlight
    p(img, 5, 3, glass_hi)
    p(img, 4, 4, glass_hi)
    p(img, 5, 4, glass_hi)
    # Face behind glass (dim)
    face = (160, 130, 110, 140)
    rect(img, 5, 5, 4, 4, face)
    # Eyes behind glass
    p(img, 5, 6, (40, 35, 30))
    p(img, 8, 6, (40, 35, 30))
    # Helmet bolts
    p(img, 2, 5, (120, 120, 110))
    p(img, 11, 5, (120, 120, 110))
    # Neck seal
    rect(img, 4, 11, 6, 3, rim)
    rect(img, 5, 11, 4, 3, suit)
    img.save(os.path.join(OUTPUT_DIR, "room5", "head.png"))

    # TORSO 10x20 — pressure suit with chest panel and hose
    img = make_image(10, 20)
    # Suit body
    rect(img, 1, 0, 8, 18, suit)
    # Shoulders
    rect(img, 0, 1, 10, 3, suit)
    # Chest panel (lighter rectangle)
    rect(img, 3, 4, 4, 5, panel)
    # Panel details (gauges/buttons)
    p(img, 4, 5, (150, 160, 170))
    p(img, 6, 5, (200, 60, 50))  # red indicator
    p(img, 4, 7, (100, 200, 100))  # green indicator
    p(img, 6, 7, (150, 160, 170))
    # Oxygen hose (runs from panel up-right)
    vline(img, 8, 0, 6, hose)
    p(img, 7, 6, hose)
    p(img, 7, 5, hose)
    # Arms (suit material)
    rect(img, 0, 4, 1, 8, suit)
    rect(img, 9, 4, 1, 8, suit)
    # Gloves
    rect(img, 0, 12, 1, 2, (50, 55, 65))
    rect(img, 9, 12, 1, 2, (50, 55, 65))
    # Belt/weight belt
    hline(img, 1, 8, 14, (90, 85, 70))
    hline(img, 1, 8, 15, (90, 85, 70))
    # Buckle
    p(img, 4, 14, (180, 170, 100))
    p(img, 5, 14, (180, 170, 100))
    # Lower suit
    rect(img, 1, 16, 8, 4, suit)
    img.save(os.path.join(OUTPUT_DIR, "room5", "torso.png"))

    # LEGS 8x12 — wetsuit legs with flippers
    img = make_image(8, 12)
    # Left leg
    rect(img, 0, 0, 3, 8, suit)
    # Right leg
    rect(img, 5, 0, 3, 8, suit)
    # Suit seam detail
    vline(img, 1, 0, 7, (50, 60, 80))
    vline(img, 6, 0, 7, (50, 60, 80))
    # Flippers (wider than legs, extend out)
    rect(img, 0, 8, 4, 4, flipper)
    rect(img, 4, 8, 4, 4, flipper)
    # Flipper tips (extend and taper)
    hline(img, 0, 3, 8, (60, 75, 60))
    hline(img, 4, 7, 8, (60, 75, 60))
    # Flipper texture
    p(img, 1, 10, (40, 50, 40))
    p(img, 2, 9, (40, 50, 40))
    p(img, 5, 10, (40, 50, 40))
    p(img, 6, 9, (40, 50, 40))
    img.save(os.path.join(OUTPUT_DIR, "room5", "legs.png"))


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print("Generating NPC sprites for rooms 1-5...")
    room1()
    print("  Room 1 (Container Store Shoppers) - done")
    room2()
    print("  Room 2 (Warehouse Employees) - done")
    room3()
    print("  Room 3 (Wing-Eating Bar Patrons) - done")
    room4()
    print("  Room 4 (Peak Ravers) - done")
    room5()
    print("  Room 5 (Pressure-Suited Divers) - done")
    print(f"\nAll sprites saved to: {OUTPUT_DIR}")
