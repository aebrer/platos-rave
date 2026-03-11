# CLAUDE.md - Plato's Rave

**Project**: Plato's Rave — Dungeon-crawler-aesthetic incremental idle game
**Developer**: Drew Brereton (aebrer) - Python/generative art background
**Inspiration**: MBMBaM Episode 674 — the longest single bit in podcast history
**Repo**: `https://github.com/aebrer/platos-rave` (private during dev)
**PR**: `https://github.com/aebrer/platos-rave/pull/1`

General working style, communication preferences, debugging process, and commit conventions
are in the global `~/CLAUDE.md`. This file covers Plato's Rave-specific context only.

---

## Concept

A 10-room incremental idle game based on the Plato's Rave bit from My Brother, My Brother
and Me. You are IN a room. You dance. You generate Vibe. You move through rooms of
escalating absurdity inside a Container Store.

**This is NOT a cookie clicker.** It's a dungeon crawler where:
- The room fills the viewport — you're standing in it
- Your character dances (idle animation + tap bursts)
- Each room has NPC attendees, ambient flavor text, and spawning lore items
- Navigation is spatial (move between rooms), not a shop/list UI
- Pressure & Pulse internal stats determine which room is optimal for you

Prestige mechanic: dethrone the kandi king in Room 10, restart from Room 1 with
meta-currency ("Kandi") for permanent upgrades and cosmetics.

See `design/game-design.md` for the full design document and `reference/episode-notes.md`
for source material from the podcast. Full searchable transcript at `reference/transcript.md`.

---

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS — no frameworks, no build step
- **Hosting**: GitHub Pages via `docs/` folder (prod), Tailscale for mobile testing
- **Assets**: Python-based procedural texture generation via `/generate-texture` skill
  - Room textures live at `docs/assets/rooms/` (wall + floor per room)
  - Placeholder textures generated with ImageMagick for now
  - Real textures will use the Deep Yellow creator→critic→revision cycle
- **Save System**: LocalStorage with versioned JSON schema (currently v3)
- **Testing**: QA checklist in `design/qa-checklist.md` — Claude runs this before PRs

---

## Project Structure

```
/home/drew/projects/platos-rave/
├── CLAUDE.md
├── README.md
├── docs/                  # GitHub Pages prod — game lives here
│   ├── index.html
│   ├── style.css
│   ├── game.js
│   ├── about.html         # Credits, MBMBaM info, fan project disclaimer
│   └── assets/
│       └── rooms/         # Room textures (wall + floor PNGs)
├── design/                # Game design docs
│   ├── game-design.md
│   └── qa-checklist.md
├── reference/             # Source material (not published)
│   ├── episode-notes.md
│   └── transcript.md      # Full 89-page searchable transcript
├── scripts/               # Python asset generation scripts (future)
└── .githooks/             # Pre-commit hooks
```

---

## Current State (v0.1.0)

### What's Built
- Full-viewport dungeon crawler layout (mobile-first)
- Tap-to-dance mechanic with floating +Vibe feedback
- 2 rooms: Container Store and Cloister of Confidence
- Pressure & Pulse stats with per-room optimal ranges and multipliers
- Optimal range indicators on stat bars (always visible, expand with items)
- Room navigation with unlock mechanic
- NPC rave attendees (per-room colors, staggered dance animations)
- Ambient flavor: onomatopoeia, emojis, NPC quotes from the episode
- Purchasable room items that spawn as bobbing emojis with price tags
  - 6 items per room (vibeRate, clickPower, comfyRange effects)
  - Items stack, cost scales 1.3x per copy, persist in room inventory
  - Tap inventory slots to see item details
- 3-node room map centered on current position (mystery "?" hints at loop)
- LocalStorage save/load with offline catch-up (24h cap)
- About page with MBMBaM credits and fan project disclaimer
- Placeholder room textures (ImageMagick plasma, loaded as tiling PNGs)

### What's Not Built Yet
- Rooms 3-10
- Prestige / Kandi system
- Real procedural textures (use `/generate-texture` skill when ready)
- 300-key drop event
- Sound / music
- Metaversal variant rooms
- Achievements, stats page, save export

---

## Development Workflow

**Mobile-First Design**
- Design for phone screens first, inherit desktop layout naturally
- Test on mobile via Tailscale: `http://atwood.tail6160db.ts.net:8080`
- Use `nohup python3 -m http.server 8080 --bind 0.0.0.0 &` for persistent local preview

**Texture Generation**
- Use the `/generate-texture` skill to create room textures
- Textures go to `docs/assets/rooms/` as `roomN_wall.png` and `roomN_floor.png`
- CSS loads them via `background-image` on `#back-wall` and `#floor-plane` elements
- Each room has a CSS class (e.g., `room-1`) that selects its textures
- No CSS gradient placeholders — use actual image files or nothing

**Testing Protocol**
- Claude runs the QA checklist (`design/qa-checklist.md`) before every PR
- Drew handles visual/interactive testing on mobile via Tailscale
- "Ready for testing" means QA checklist passed AND local server running

**Save System**
- LocalStorage key: `platos-rave-save`
- JSON schema with a `version` field — bump version to wipe incompatible saves
- Currently version 3 (added inventory system)
- Early development: breaking save compatibility is acceptable
- Post-release: migrations required, version field drives this

---

## Key Design Principles

**Dungeon Crawler Aesthetic, Not Flat Web App**
- The room is the game — it fills the screen
- Go big, go bold, monospace font, rave glow
- Never compress or abbreviate UI labels — spell things out
- When in doubt, make it MORE visible, not less

**Room-Centric Gameplay**
- You choose which room to stand in — that IS the strategy
- Items belong to rooms, not to the player globally
- NPC attendees and ambient flavor are per-room and lore-driven
- Each room has its own personality from the episode

**Humor First**
- The game is a comedy vehicle — mechanics serve jokes
- Room descriptions, item names, NPC quotes are the content
- Reference the podcast but make it accessible to non-listeners

**No Monetization**
- Free game, open source (after initial private dev)
- No ads, no microtransactions, no premium currency

---

## Conventions

- File naming: `snake_case` for everything
- JS: vanilla, no modules/build step/transpilation
- CSS: mobile-first responsive, monospace font (`Courier New`)
- Room textures: `docs/assets/rooms/roomN_wall.png`, `roomN_floor.png`
- Commits: detailed messages per `~/CLAUDE.md` conventions
- Versioning: semantic (v0.1.0 for first playable, v1.0.0 for public release)
- No innerHTML — use DOM creation methods (security hook enforced)
