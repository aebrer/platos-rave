# QA Checklist — Plato's Rave

This checklist is run by Claude before every PR. Drew handles visual/interactive testing
on mobile via Tailscale.

---

## Pre-PR Checklist (Claude Executes)

### 1. Page Load
- [ ] `docs/index.html` loads without JS errors (check via headless browser or node)
- [ ] No 404s for CSS, JS, or asset files
- [ ] Game state initializes correctly on fresh load (no existing save)

### 2. Save System
- [ ] Fresh load creates a valid save in LocalStorage
- [ ] Save contains `version` field matching current schema
- [ ] Game auto-saves on interval (verify save timestamp updates)
- [ ] Page reload preserves game state (Vibe count, unlocked rooms, generator levels)
- [ ] Offline catch-up: simulate elapsed time, verify Vibe calculation is correct
  - Set a save with `lastSaved` in the past, reload, check earned Vibe
- [ ] Offline cap enforced (doesn't award infinite Vibe for long absences)
- [ ] Corrupted/missing save handled gracefully (starts fresh, no crash)

### 3. Core Mechanics
- [ ] Clicking generates Vibe (correct amount based on upgrades)
- [ ] Vibe display updates in real-time
- [ ] Large numbers formatted correctly (K, M, B, T)
- [ ] Generator passive income calculated correctly (Vibe/sec)
- [ ] Room unlock thresholds enforced (can't unlock without enough Vibe)
- [ ] Room unlock deducts correct Vibe cost
- [ ] Generator upgrades increase output correctly
- [ ] Generator cost scaling works (each level costs more)

### 4. Game Math Verification
- [ ] Income rates match what's displayed in UI
- [ ] No NaN, Infinity, or negative values in game state
- [ ] Number formatting handles edge cases (0, very large, decimals)
- [ ] Cost calculations don't overflow or go negative

### 5. Responsive Layout
- [ ] No horizontal scroll on mobile viewport (375px width)
- [ ] Touch targets are at least 44x44px
- [ ] Text is readable without zooming
- [ ] UI elements don't overlap on small screens

### 6. Code Quality
- [ ] No `console.log` left in production code (use `console.debug` if needed)
- [ ] No hardcoded test values or debug shortcuts
- [ ] All JS files parse without syntax errors
- [ ] CSS validates (no broken rules)

---

## How Claude Runs This

### Automated Checks (via Bash/Node)
```bash
# Check for JS syntax errors
node --check docs/game.js

# Check for 404s (all referenced files exist)
# Parse index.html for src/href, verify each file exists

# Run game math tests (when test file exists)
node tests/game_math.test.js
```

### Manual Inspection (via Read tool)
- Read the save state JSON structure and verify schema
- Read game.js and trace income calculations
- Check CSS for mobile-first patterns (min-width media queries, not max-width)
- Verify number formatting function handles edge cases

### What Claude CANNOT Test
- Visual rendering (Drew tests on mobile)
- Touch/click feel (Drew tests)
- Animation smoothness (Drew tests)
- Sound (future)
- Cross-browser compatibility (Drew tests Safari/Chrome)

---

## Post-Merge Verification

After merging to main:
- [ ] GitHub Pages build succeeds
- [ ] Live site loads and plays correctly
- [ ] Save from previous version migrates correctly (post-v1)

---

## Version-Specific Additions

### V1 Proof of Concept
- [ ] Room 1 unlocked by default
- [ ] Room 2 unlockable by earning enough Vibe
- [ ] At least one generator per room
- [ ] Offline catch-up shows "Welcome back" summary
- [ ] Mobile layout is usable on a phone screen
