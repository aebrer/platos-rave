# CLAUDE.md - Plato's Rave

**Project**: Plato's Rave — Incremental idle game with clicking mechanics
**Developer**: Drew Brereton (aebrer) - Python/generative art background
**Inspiration**: MBMBaM Episode 674 — the longest single bit in podcast history

General working style, communication preferences, debugging process, and commit conventions
are in the global `~/CLAUDE.md`. This file covers Plato's Rave-specific context only.

---

## Concept

A 10-room incremental idle game based on the Plato's Rave bit from My Brother, My Brother
and Me. Players click to generate "Vibe" and progress through rooms of escalating absurdity
inside a Container Store. Prestige mechanic: dethrone the kandi king in Room 10, restart
from Room 1 with meta-currency ("Kandi") for permanent upgrades and cosmetics.

See `design/game-design.md` for the full design document and `reference/episode-notes.md`
for source material from the podcast.

---

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS — no frameworks, keep it portable
- **Hosting**: GitHub Pages via `docs/` folder (prod), Tailscale for mobile testing
- **Assets**: Python-based procedural texture/asset generation (same workflow as Deep Yellow)
- **Save System**: LocalStorage with versioned JSON schema
- **Testing**: QA checklist in `design/qa-checklist.md` — Claude runs this before PRs

---

## Project Structure

```
/home/drew/projects/platos-rave/
├── CLAUDE.md
├── README.md
├── docs/              # GitHub Pages prod — game lives here
│   ├── index.html
│   ├── style.css
│   ├── game.js
│   └── assets/        # Generated textures and art
├── design/            # Game design docs
│   ├── game-design.md
│   └── qa-checklist.md
├── reference/         # Source material (not published)
│   └── episode-notes.md
├── scripts/           # Python asset generation scripts
└── .githooks/         # Pre-commit hooks
```

---

## Development Workflow

**Mobile-First Design**
- Design for phone screens first, inherit desktop layout naturally
- Test on mobile via Tailscale: `http://atwood.tail6160db.ts.net:8080`
- Use `nohup python3 -m http.server 8080 --bind 0.0.0.0 &` for persistent local preview

**Asset Generation (Deep Yellow Pattern)**
- Python scripts in `scripts/` for procedural textures and art
- Scripts run in project venv: `scripts/venv/` (create as needed)
- Generated assets go to `docs/assets/`
- Use the texture generation cycle: creator → critic → revision

**Testing Protocol**
- Claude runs the QA checklist (`design/qa-checklist.md`) before every PR
- This includes loading the page in a headless context, checking LocalStorage behavior,
  verifying game math, and inspecting the DOM
- Drew handles visual/interactive testing on mobile via Tailscale
- "Ready for testing" means QA checklist passed AND local server running

**Save System**
- LocalStorage key: `platos-rave-save`
- JSON schema with a `version` field for migrations
- Offline catch-up: on page load, compute elapsed time since last save and simulate
  production at saved rates (with configurable cap)
- Early development: breaking save compatibility is acceptable
- Post-release: migrations required, version field drives this

---

## Key Design Principles

**Incremental Idle + Clicker Hybrid**
- Clicking generates base currency ("Vibe")
- Automation unlocks per-room reduce need for clicking over time
- Prestige (Room 10 cycle) is the meta-progression layer

**Offline Progression**
- Game catches up on missed time when page reopens
- No penalty for closing the tab — this is a core feature
- Cap offline earnings to prevent absurd numbers on long absences

**Humor First**
- The game is a comedy vehicle — mechanics serve jokes
- Room descriptions, upgrade names, and flavor text are the content
- Reference the podcast but make it accessible to non-listeners

**No Monetization**
- Free game, open source (after initial private dev)
- No ads, no microtransactions, no premium currency
- Published on itch.io

---

## Conventions

- File naming: `snake_case` for everything
- JS: vanilla ES modules, no build step, no transpilation
- CSS: mobile-first responsive, system fonts initially
- Commits: detailed messages per `~/CLAUDE.md` conventions
- Versioning: semantic (v0.1.0 for first playable, v1.0.0 for public release)
