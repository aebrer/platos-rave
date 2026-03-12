"""
Generate NPC sprites for Plato's Rave rooms 6-10.

Each room gets 3 PNGs: head (14x14), torso (10x20), legs (8x12).
All sprites are RGBA with transparent backgrounds, pixel art at 1x scale.

Room 6: Sauce-Splattered Cooks/DoorDash Workers
Room 7: Gothic Circus Performers
Room 8: Actor-Employees (Fake Container Store, uncanny)
Room 9: Transcendent Archivists/Enlightened Ravers
Room 10: The Candy King (Boss NPC)
"""

import numpy as np
from PIL import Image
import os

OUTPUT_BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "docs", "assets", "sprites", "npcs"
)


def save_sprite(pixels, folder, filename):
    """Save a numpy RGBA array as a PNG."""
    path = os.path.join(OUTPUT_BASE, folder, filename)
    img = Image.fromarray(pixels.astype(np.uint8), "RGBA")
    img.save(path)
    print(f"  Saved {path}")


def px(img, x, y, color):
    """Set a pixel with bounds checking."""
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        img[y, x] = color


def rect(img, x0, y0, w, h, color):
    """Draw a filled rectangle."""
    for dy in range(h):
        for dx in range(w):
            px(img, x0 + dx, y0 + dy, color)


def line_h(img, x0, y, length, color):
    """Horizontal line."""
    for dx in range(length):
        px(img, x0 + dx, y, color)


def line_v(img, x, y0, length, color):
    """Vertical line."""
    for dy in range(length):
        px(img, x, y0 + dy, color)


# ─── Colors (RGBA tuples) ───

T = (0, 0, 0, 0)  # transparent

# Room 6
CHEF_WHITE = (235, 230, 225, 255)
SAUCE = (200, 80, 30, 255)
SAUCE_LIGHT = (220, 110, 50, 255)
KITCHEN_PANTS = (50, 50, 55, 255)
SKIN_6 = (210, 180, 140, 255)
HAT_WHITE = (245, 240, 235, 255)
SHOE_BLACK = (30, 30, 30, 255)

# Room 7
CRIMSON = (140, 20, 40, 255)
GOTH_BLACK = (25, 20, 30, 255)
GOLD = (200, 170, 50, 255)
DARK_PURPLE = (60, 20, 50, 255)
SKIN_7 = (200, 190, 180, 255)
HAT_BAND = (100, 15, 30, 255)

# Room 8
UNCANNY_SKIN = (210, 200, 155, 255)
WRONG_BLUE = (80, 160, 140, 255)
OFF_KHAKI = (185, 170, 160, 255)
NAMETAG = (220, 60, 60, 255)
EYE_WHITE = (250, 250, 245, 255)
PUPIL = (20, 20, 20, 255)
SMILE = (180, 50, 50, 255)

# Room 9
LUM_WHITE = (240, 235, 220, 255)
GOLD_9 = (210, 190, 110, 255)
AURA = (255, 245, 200, 255)
HALO = (255, 240, 180, 255)
SKIN_9 = (220, 210, 190, 255)
SCROLL = (180, 160, 120, 255)

# Room 10
ROYAL_PURPLE = (80, 30, 100, 255)
CANDY_RED = (255, 50, 50, 255)
CANDY_YELLOW = (255, 220, 50, 255)
CANDY_GREEN = (50, 255, 80, 255)
CANDY_BLUE = (50, 150, 255, 255)
GOLD_TRIM = (220, 200, 80, 255)
DARK_ROYAL = (50, 15, 65, 255)
SKIN_10 = (200, 170, 130, 255)
CAPE_EDGE = (100, 40, 120, 255)


# ═══════════════════════════════════════════════════════
# ROOM 6 — Sauce-Splattered Cooks
# ═══════════════════════════════════════════════════════

def room6_head():
    """14x14 chef head: tall white hat, sauce-splattered face."""
    img = np.zeros((14, 14, 4), dtype=np.uint8)

    # Chef hat - tall and white
    rect(img, 4, 0, 6, 2, HAT_WHITE)       # hat top
    rect(img, 3, 2, 8, 3, HAT_WHITE)       # hat body
    # Hat puff top
    px(img, 5, 0, CHEF_WHITE)
    px(img, 8, 0, CHEF_WHITE)

    # Face
    rect(img, 4, 5, 6, 6, SKIN_6)          # face block
    rect(img, 3, 6, 8, 4, SKIN_6)          # wider cheeks
    # Eyes
    px(img, 5, 7, (40, 30, 20, 255))
    px(img, 8, 7, (40, 30, 20, 255))
    # Mouth
    line_h(img, 5, 9, 4, (160, 100, 80, 255))

    # Sauce splatters on face
    px(img, 3, 7, SAUCE)
    px(img, 9, 6, SAUCE_LIGHT)
    px(img, 6, 10, SAUCE)

    # Sauce on hat
    px(img, 5, 2, SAUCE)
    px(img, 7, 3, SAUCE_LIGHT)

    # Neck
    rect(img, 5, 11, 4, 2, SKIN_6)
    # Collar hint
    px(img, 4, 12, CHEF_WHITE)
    px(img, 9, 12, CHEF_WHITE)

    return img


def room6_torso():
    """10x20 chef torso: white coat with sauce splatters."""
    img = np.zeros((20, 10, 4), dtype=np.uint8)

    # Chef coat body
    rect(img, 1, 0, 8, 18, CHEF_WHITE)
    # Collar
    rect(img, 2, 0, 6, 2, (245, 242, 238, 255))

    # Buttons down center
    for y in [3, 6, 9, 12, 15]:
        px(img, 5, y, (180, 175, 170, 255))

    # Arms
    rect(img, 0, 2, 2, 12, CHEF_WHITE)     # left arm
    rect(img, 8, 2, 2, 12, CHEF_WHITE)     # right arm

    # Sauce splatters!
    px(img, 2, 4, SAUCE)
    px(img, 3, 5, SAUCE)
    px(img, 7, 3, SAUCE_LIGHT)
    px(img, 6, 8, SAUCE)
    px(img, 2, 11, SAUCE_LIGHT)
    px(img, 8, 7, SAUCE)
    px(img, 4, 14, SAUCE)
    px(img, 1, 9, SAUCE)

    # Apron strings hint
    px(img, 3, 16, (200, 195, 190, 255))
    px(img, 6, 16, (200, 195, 190, 255))

    # Hands
    px(img, 0, 14, SKIN_6)
    px(img, 9, 14, SKIN_6)

    return img


def room6_legs():
    """8x12 chef legs: black kitchen pants, non-slip shoes."""
    img = np.zeros((12, 8, 4), dtype=np.uint8)

    # Left leg
    rect(img, 1, 0, 3, 9, KITCHEN_PANTS)
    # Right leg
    rect(img, 4, 0, 3, 9, KITCHEN_PANTS)

    # Shoes - chunky non-slip
    rect(img, 0, 9, 4, 3, SHOE_BLACK)
    rect(img, 4, 9, 4, 3, SHOE_BLACK)
    # Shoe soles
    line_h(img, 0, 11, 4, (60, 60, 60, 255))
    line_h(img, 4, 11, 4, (60, 60, 60, 255))

    # Sauce drip on pants
    px(img, 2, 3, SAUCE)
    px(img, 5, 6, SAUCE_LIGHT)

    return img


# ═══════════════════════════════════════════════════════
# ROOM 7 — Gothic Circus Performers
# ═══════════════════════════════════════════════════════

def room7_head():
    """14x14 ringmaster head: top hat, dramatic face."""
    img = np.zeros((14, 14, 4), dtype=np.uint8)

    # Top hat
    rect(img, 4, 0, 6, 5, GOTH_BLACK)      # hat body
    rect(img, 3, 5, 8, 1, GOTH_BLACK)      # hat brim
    # Hat band
    line_h(img, 4, 4, 6, HAT_BAND)
    # Gold buckle on hat
    px(img, 7, 4, GOLD)

    # Face - pale gothic
    rect(img, 4, 6, 6, 5, SKIN_7)
    rect(img, 5, 6, 4, 6, SKIN_7)
    # Dark eyes
    px(img, 5, 8, DARK_PURPLE)
    px(img, 8, 8, DARK_PURPLE)
    # Eye liner / shadow
    px(img, 4, 8, GOTH_BLACK)
    px(img, 9, 8, GOTH_BLACK)
    # Thin dramatic mouth
    line_h(img, 5, 10, 4, CRIMSON)

    # Neck
    rect(img, 5, 12, 4, 2, SKIN_7)
    # Collar/bowtie hint
    px(img, 6, 13, CRIMSON)
    px(img, 7, 13, CRIMSON)

    return img


def room7_torso():
    """10x20 circus torso: red/black striped costume, gold buttons."""
    img = np.zeros((20, 10, 4), dtype=np.uint8)

    # Striped body - alternating crimson and black
    for y in range(18):
        color = CRIMSON if (y // 2) % 2 == 0 else GOTH_BLACK
        rect(img, 2, y, 6, 1, color)

    # Arms - also striped
    for y in range(2, 15):
        color = CRIMSON if (y // 2) % 2 == 0 else GOTH_BLACK
        px(img, 0, y, color)
        px(img, 1, y, color)
        px(img, 8, y, color)
        px(img, 9, y, color)

    # Gold buttons down center
    for y in [2, 5, 8, 11, 14]:
        px(img, 5, y, GOLD)

    # Gold trim at top (epaulettes)
    line_h(img, 1, 0, 8, GOLD)
    px(img, 0, 1, GOLD)
    px(img, 9, 1, GOLD)

    # Collar
    px(img, 3, 0, GOTH_BLACK)
    px(img, 6, 0, GOTH_BLACK)

    # Gold trim at waist
    line_h(img, 2, 17, 6, GOLD)

    # Hands - pale
    px(img, 0, 15, SKIN_7)
    px(img, 9, 15, SKIN_7)

    return img


def room7_legs():
    """8x12 circus legs: striped tight-fitting, pointed boots."""
    img = np.zeros((12, 8, 4), dtype=np.uint8)

    # Striped legs
    for y in range(8):
        color = GOTH_BLACK if (y // 2) % 2 == 0 else CRIMSON
        rect(img, 1, y, 3, 1, color)   # left
        rect(img, 4, y, 3, 1, color)   # right

    # Pointed boots
    rect(img, 1, 8, 3, 3, GOTH_BLACK)      # left boot
    rect(img, 4, 8, 3, 3, GOTH_BLACK)      # right boot
    # Pointed toes
    px(img, 0, 10, GOTH_BLACK)              # left point
    px(img, 7, 10, GOTH_BLACK)              # right point
    # Gold trim on boots
    line_h(img, 1, 8, 3, GOLD)
    line_h(img, 4, 8, 3, GOLD)

    return img


# ═══════════════════════════════════════════════════════
# ROOM 8 — Actor-Employees (Uncanny Container Store)
# ═══════════════════════════════════════════════════════

def room8_head():
    """14x14 uncanny employee head: wrong skin tone, too-wide eyes, weird smile."""
    img = np.zeros((14, 14, 4), dtype=np.uint8)

    # Hair - slightly off brown
    rect(img, 3, 0, 8, 3, (100, 90, 60, 255))
    rect(img, 4, 0, 6, 2, (90, 80, 55, 255))

    # Face - uncanny greenish-yellow skin
    rect(img, 3, 3, 8, 7, UNCANNY_SKIN)
    rect(img, 4, 2, 6, 9, UNCANNY_SKIN)

    # Too-wide eyes - spread apart, slightly large
    # Left eye
    rect(img, 3, 5, 3, 2, EYE_WHITE)
    px(img, 4, 5, PUPIL)
    px(img, 4, 6, PUPIL)
    # Right eye
    rect(img, 8, 5, 3, 2, EYE_WHITE)
    px(img, 9, 5, PUPIL)
    px(img, 9, 6, PUPIL)

    # Uncanny wide smile - too wide, too red
    line_h(img, 4, 8, 6, SMILE)
    line_h(img, 5, 9, 4, SMILE)
    # Teeth showing
    line_h(img, 5, 8, 4, EYE_WHITE)

    # Neck
    rect(img, 5, 11, 4, 3, UNCANNY_SKIN)

    return img


def room8_torso():
    """10x20 wrong-color polo with nametag."""
    img = np.zeros((20, 10, 4), dtype=np.uint8)

    # Polo body - wrong teal/green instead of proper blue
    rect(img, 1, 0, 8, 18, WRONG_BLUE)

    # Collar
    rect(img, 2, 0, 6, 2, (70, 145, 125, 255))
    # Collar V
    px(img, 4, 2, UNCANNY_SKIN)
    px(img, 5, 2, UNCANNY_SKIN)
    px(img, 4, 1, UNCANNY_SKIN)
    px(img, 5, 1, UNCANNY_SKIN)

    # Arms
    rect(img, 0, 2, 2, 10, WRONG_BLUE)
    rect(img, 8, 2, 2, 10, WRONG_BLUE)

    # Nametag - just a colored rectangle (unsettling)
    rect(img, 6, 5, 3, 2, NAMETAG)
    px(img, 7, 5, (255, 255, 255, 255))  # tiny "text" mark

    # Hands - uncanny skin
    px(img, 0, 12, UNCANNY_SKIN)
    px(img, 9, 12, UNCANNY_SKIN)

    # Belt line
    line_h(img, 1, 17, 8, (140, 130, 120, 255))

    return img


def room8_legs():
    """8x12 off-khaki pants - slightly purple-tinted."""
    img = np.zeros((12, 8, 4), dtype=np.uint8)

    # Left leg - off-khaki
    rect(img, 1, 0, 3, 9, OFF_KHAKI)
    # Right leg
    rect(img, 4, 0, 3, 9, OFF_KHAKI)

    # Shoes - slightly wrong shade
    rect(img, 0, 9, 4, 3, (90, 75, 80, 255))
    rect(img, 4, 9, 4, 3, (90, 75, 80, 255))

    # Subtle purple tint marks on pants
    px(img, 2, 3, (175, 155, 165, 255))
    px(img, 5, 5, (175, 155, 165, 255))

    return img


# ═══════════════════════════════════════════════════════
# ROOM 9 — Transcendent Archivists
# ═══════════════════════════════════════════════════════

def room9_head():
    """14x14 serene face with glowing halo, closed peaceful eyes."""
    img = np.zeros((14, 14, 4), dtype=np.uint8)

    # Halo - ring of gold/light above head
    line_h(img, 4, 0, 6, HALO)
    px(img, 3, 1, HALO)
    px(img, 10, 1, HALO)
    px(img, 3, 2, HALO)
    px(img, 10, 2, HALO)
    line_h(img, 4, 3, 6, HALO)
    # Aura glow around halo
    px(img, 2, 1, (255, 245, 200, 128))
    px(img, 11, 1, (255, 245, 200, 128))

    # Face - serene, slightly luminous
    rect(img, 4, 4, 6, 6, SKIN_9)
    rect(img, 3, 5, 8, 4, SKIN_9)

    # Closed peaceful eyes - just horizontal lines
    line_h(img, 4, 7, 3, (160, 150, 130, 255))
    line_h(img, 7, 7, 3, (160, 150, 130, 255))

    # Serene slight smile
    px(img, 6, 9, (190, 170, 150, 255))
    px(img, 7, 9, (190, 170, 150, 255))

    # Neck flowing into robe
    rect(img, 5, 10, 4, 4, LUM_WHITE)
    rect(img, 4, 12, 6, 2, LUM_WHITE)

    return img


def room9_torso():
    """10x20 flowing white/gold robes, luminous, book/scroll mark."""
    img = np.zeros((20, 10, 4), dtype=np.uint8)

    # Flowing robe body
    rect(img, 1, 0, 8, 20, LUM_WHITE)

    # Gold trim at neckline
    line_h(img, 2, 0, 6, GOLD_9)
    line_h(img, 2, 1, 6, GOLD_9)

    # Robe folds/draping - subtle darker lines
    fold = (225, 220, 205, 255)
    line_v(img, 3, 3, 15, fold)
    line_v(img, 6, 4, 14, fold)

    # Sleeves - wide flowing
    rect(img, 0, 2, 2, 12, LUM_WHITE)
    rect(img, 8, 2, 2, 12, LUM_WHITE)

    # Gold trim on sleeves
    px(img, 0, 2, GOLD_9)
    px(img, 1, 2, GOLD_9)
    px(img, 8, 2, GOLD_9)
    px(img, 9, 2, GOLD_9)

    # Scroll/book mark at waist
    rect(img, 2, 10, 3, 2, SCROLL)
    px(img, 2, 10, (160, 140, 100, 255))

    # Aura shimmer - scattered light pixels
    px(img, 1, 5, AURA)
    px(img, 8, 8, AURA)
    px(img, 2, 15, AURA)
    px(img, 7, 3, AURA)

    # Hands tucked in sleeves
    px(img, 0, 13, SKIN_9)
    px(img, 9, 13, SKIN_9)

    # Gold band at bottom
    line_h(img, 1, 19, 8, GOLD_9)

    return img


def room9_legs():
    """8x12 flowing robe bottom, barely visible feet, gold-white gradient."""
    img = np.zeros((12, 8, 4), dtype=np.uint8)

    # Robe bottom - wide flowing
    rect(img, 0, 0, 8, 10, LUM_WHITE)

    # Gradient toward gold at bottom
    line_h(img, 0, 7, 8, (235, 228, 200, 255))
    line_h(img, 0, 8, 8, (228, 220, 180, 255))
    line_h(img, 0, 9, 8, (220, 210, 160, 255))

    # Robe fold lines
    line_v(img, 2, 0, 9, (225, 220, 205, 255))
    line_v(img, 5, 0, 9, (225, 220, 205, 255))

    # Barely visible feet peeking out
    px(img, 2, 10, (200, 190, 170, 255))
    px(img, 3, 10, (200, 190, 170, 255))
    px(img, 5, 10, (200, 190, 170, 255))
    px(img, 6, 10, (200, 190, 170, 255))

    # Gold hem
    line_h(img, 0, 9, 8, GOLD_9)

    return img


# ═══════════════════════════════════════════════════════
# ROOM 10 — The Candy King (Boss NPC)
# ═══════════════════════════════════════════════════════

def room10_head():
    """14x14 Candy King head: candy crown is the KEY feature."""
    img = np.zeros((14, 14, 4), dtype=np.uint8)

    # Candy crown! Ring of colored candy beads
    # Crown base
    line_h(img, 3, 3, 8, GOLD_TRIM)
    # Crown points with candy dots
    px(img, 3, 2, CANDY_RED)
    px(img, 5, 1, CANDY_YELLOW)
    px(img, 7, 0, CANDY_GREEN)
    px(img, 9, 1, CANDY_BLUE)
    px(img, 10, 2, CANDY_RED)
    # Crown structure
    px(img, 4, 2, GOLD_TRIM)
    px(img, 6, 1, GOLD_TRIM)
    px(img, 7, 1, GOLD_TRIM)
    px(img, 8, 2, GOLD_TRIM)
    # More candy beads on crown
    px(img, 5, 2, CANDY_GREEN)
    px(img, 7, 2, CANDY_YELLOW)
    px(img, 4, 1, CANDY_BLUE)

    # Face
    rect(img, 4, 4, 6, 6, SKIN_10)
    rect(img, 3, 5, 8, 4, SKIN_10)

    # Wild eyes - expressive
    px(img, 5, 6, (255, 255, 240, 255))  # eye whites
    px(img, 8, 6, (255, 255, 240, 255))
    px(img, 5, 7, (30, 20, 40, 255))     # pupils
    px(img, 8, 7, (30, 20, 40, 255))
    # Eyebrows raised
    line_h(img, 4, 5, 3, (80, 60, 40, 255))
    line_h(img, 7, 5, 3, (80, 60, 40, 255))

    # Wild grin
    line_h(img, 5, 9, 4, (180, 60, 60, 255))

    # Neck
    rect(img, 5, 10, 4, 3, SKIN_10)
    # Royal collar hint
    px(img, 4, 12, ROYAL_PURPLE)
    px(img, 9, 12, ROYAL_PURPLE)
    px(img, 5, 12, GOLD_TRIM)
    px(img, 8, 12, GOLD_TRIM)

    return img


def room10_torso():
    """10x20 regal outfit: dark purple/black with candy gem accents, cape."""
    img = np.zeros((20, 10, 4), dtype=np.uint8)

    # Cape behind (edges)
    rect(img, 0, 0, 2, 20, CAPE_EDGE)
    rect(img, 8, 0, 2, 20, CAPE_EDGE)

    # Royal body
    rect(img, 2, 0, 6, 18, ROYAL_PURPLE)

    # Dark royal center panel
    rect(img, 3, 2, 4, 14, DARK_ROYAL)

    # Gold trim at collar
    line_h(img, 2, 0, 6, GOLD_TRIM)
    line_h(img, 1, 1, 8, GOLD_TRIM)

    # Candy gem accents down the front
    px(img, 5, 4, CANDY_RED)
    px(img, 4, 7, CANDY_YELLOW)
    px(img, 5, 10, CANDY_GREEN)
    px(img, 4, 13, CANDY_BLUE)

    # Gold buttons/trim
    px(img, 3, 4, GOLD_TRIM)
    px(img, 6, 4, GOLD_TRIM)
    px(img, 3, 10, GOLD_TRIM)
    px(img, 6, 10, GOLD_TRIM)

    # Cape drape
    px(img, 0, 3, DARK_ROYAL)
    px(img, 9, 3, DARK_ROYAL)

    # Mantle/shoulder pads
    rect(img, 0, 0, 3, 3, ROYAL_PURPLE)
    rect(img, 7, 0, 3, 3, ROYAL_PURPLE)
    px(img, 0, 0, GOLD_TRIM)
    px(img, 9, 0, GOLD_TRIM)

    # Hands on throne arms
    px(img, 0, 14, SKIN_10)
    px(img, 1, 14, SKIN_10)
    px(img, 8, 14, SKIN_10)
    px(img, 9, 14, SKIN_10)

    # Belt with candy buckle
    line_h(img, 2, 16, 6, GOLD_TRIM)
    px(img, 4, 16, CANDY_RED)
    px(img, 5, 16, CANDY_YELLOW)

    return img


def room10_legs():
    """8x12 royal legs: seated on throne, dark with gold trim."""
    img = np.zeros((12, 8, 4), dtype=np.uint8)

    # Seated legs - crossed/angled
    # Left leg
    rect(img, 0, 0, 4, 8, ROYAL_PURPLE)
    # Right leg - crossed over
    rect(img, 3, 0, 4, 8, DARK_ROYAL)

    # Gold trim on legs
    line_h(img, 0, 0, 4, GOLD_TRIM)
    line_h(img, 3, 0, 4, GOLD_TRIM)

    # Royal shoes/boots
    rect(img, 0, 8, 4, 4, (40, 15, 50, 255))
    rect(img, 4, 8, 4, 4, (40, 15, 50, 255))
    # Gold shoe trim
    line_h(img, 0, 8, 4, GOLD_TRIM)
    line_h(img, 4, 8, 4, GOLD_TRIM)
    # Candy accent on shoes
    px(img, 1, 10, CANDY_RED)
    px(img, 6, 10, CANDY_BLUE)

    # Cape draping down behind legs
    px(img, 0, 3, CAPE_EDGE)
    px(img, 7, 3, CAPE_EDGE)
    px(img, 0, 6, CAPE_EDGE)
    px(img, 7, 6, CAPE_EDGE)

    return img


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    rooms = {
        "room6": ("Sauce-Splattered Cooks", room6_head, room6_torso, room6_legs),
        "room7": ("Gothic Circus Performers", room7_head, room7_torso, room7_legs),
        "room8": ("Actor-Employees (Uncanny)", room8_head, room8_torso, room8_legs),
        "room9": ("Transcendent Archivists", room9_head, room9_torso, room9_legs),
        "room10": ("The Candy King", room10_head, room10_torso, room10_legs),
    }

    for folder, (name, head_fn, torso_fn, legs_fn) in rooms.items():
        print(f"\n--- {name} ({folder}) ---")
        save_sprite(head_fn(), folder, "head.png")
        save_sprite(torso_fn(), folder, "torso.png")
        save_sprite(legs_fn(), folder, "legs.png")

    print("\nDone! All 15 NPC sprites generated.")


if __name__ == "__main__":
    main()
