# Texture & Sprite Generators

Procedural Python scripts that generate all game textures and sprites. Each script outputs directly to `docs/assets/`.

## Requirements

- Python 3.8+
- Pillow (`pip install Pillow`)
- NumPy (`pip install numpy`)

## Room Textures

`rooms/` contains one script per texture (wall + floor for each of the 10 rooms). Each generates a 256x256 tileable PNG.

```bash
# Generate a single texture
python scripts/textures/rooms/room4_wall.py

# Regenerate all room textures
for f in scripts/textures/rooms/*.py; do python "$f"; done
```

Output: `docs/assets/rooms/roomN_wall.png` and `docs/assets/rooms/roomN_floor.png`

### Room Reference

| Room | Theme | Wall | Floor |
|------|-------|------|-------|
| 1 | The Container Store | Retail shelving, fluorescent | Polished gray tile |
| 2 | Cloister of Confidence | Warehouse shelving, industrial | Cracked concrete |
| 3 | Dry Rub Wings | Brick + dark wood, chalkboard | Dark hardwood planks |
| 4 | Best Rave of Your Life | Neon lasers, UV glow | LED dance floor |
| 5 | Barometric Pressure | Riveted steel, pipes, gauges | Diamond plate grating |
| 6 | Sauce on Six | Stainless steel + sauce splatters | Terracotta quarry tile |
| 7 | Traps | Gothic velvet curtains, gold trim | Stage wood, sawdust |
| 8 | The Final Deception | Fake Container Store (wrong colors) | Yellowed, cracked tile |
| 9 | Nirvana | Luminous crystal, sacred geometry | White marble, gold inlay |
| 10 | The Candy King | Near-black void, candy sparkles | Dark void, spotlight |

## Sprites

`sprites/` contains generators for the player character and per-room NPCs.

```bash
# Player character (6 sprites: head, torso, legs, shadow, dance burst)
python scripts/textures/sprites/player.py

# NPC sprites rooms 1-5 (3 sprites each: head, torso, legs)
python scripts/textures/sprites/npcs_1_5.py

# NPC sprites rooms 6-10
python scripts/textures/sprites/npcs_6_10.py
```

Output: `docs/assets/sprites/player/` and `docs/assets/sprites/npcs/roomN/`
