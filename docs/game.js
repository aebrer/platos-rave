// Plato's Rave — Game Engine (v0.1.0)
// You're IN a room. You dance. You generate vibes.

// ============================================================
// Room Data
// ============================================================

const ROOMS = {
  1: {
    name: "The Container Store",
    flavor: "Welcome to the Container Store. You don't know it yet, but you're already at the rave.",
    unlockCost: 0,
    baseVibeRate: 1,
    clickMultiplier: 1,
    pressureEffect: -0.5,
    optimalPressure: [0, 25],
    optimalPulse: [0, 30],
    artClass: "room-1",
  },
  2: {
    name: "The Cloister of Confidence",
    flavor: "Room two is the warehouse. People are gonna say, 'Please go. This is not the rave.' But you have to keep raving through that.",
    unlockCost: 50,
    baseVibeRate: 3,
    clickMultiplier: 2,
    pressureEffect: 1,
    optimalPressure: [15, 45],
    optimalPulse: [20, 50],
    artClass: "room-2",
  },
};


// ============================================================
// Room Ambient Flavor + NPC Config — onomatopoeia, emojis, NPC quotes, NPC appearance
// ============================================================

const ROOM_FLAVOR = {
  1: {
    sounds: [
      "UNTZ", "untz untz", "THUD", "*click*", "*snap*",
      "*shuffle*", "CLACK", "*beep*", "BONK",
    ],
    emojis: [
      "\u{1F4E6}", "\u{1F9F9}", "\u{1F3B6}", "\u{1F3B5}", "\u{1F50A}",
      "\u{2728}", "\u{1F6D2}", "\u{1F4A1}",
    ],
    quotes: [
      "Is this... the rave?",
      "I came for storage bins",
      "Why is the music so loud?",
      "These bins are so organized",
      "Do I hear a bass drop?",
      "The vibes are immaculate",
      "I think I'm in the wrong aisle",
      "This Container Store slaps",
      "Excuse me, where's aisle 7?",
      "Sir this is a retail establishment",
      "I feel something awakening",
    ],
    npcColors: ["#66aaff", "#88cc88", "#ffaa66", "#cc88cc"],
    npcCount: 3,
  },
  2: {
    sounds: [
      "UNTZ UNTZ", "BOOM", "WUBWUB", "*footsteps*", "CRASH",
      "*whisper*", "THUMP", "BASS", "*creak*",
    ],
    emojis: [
      "\u{1F3AD}", "\u{1F4AA}", "\u{1F525}", "\u{1F47B}", "\u{1F6AA}",
      "\u{1F440}", "\u{1F910}", "\u{26A0}\u{FE0F}",
    ],
    quotes: [
      "Please leave. This is not the rave.",
      "KEEP GOING",
      "They can't stop all of us",
      "I work here and I'm confused",
      "The confidence... it's building",
      "DON'T MAKE EYE CONTACT",
      "Just act like you belong",
      "Security is a construct",
      "I've been in this warehouse for days",
      "The rave is through the doubt",
      "You don't have clearance for this",
      "EMPLOYEE ONLY means EMPLOYEE ALSO",
    ],
    npcColors: ["#ff6688", "#aa88ff", "#ffcc44", "#44dddd"],
    npcCount: 4,
  },
};

// How often ambient flavor spawns (ms)
var AMBIENT_INTERVAL_MIN = 1200;
var AMBIENT_INTERVAL_MAX = 3000;

// ============================================================
// Room Items — purchasable lore objects
// ============================================================

var ROOM_ITEMS = {
  1: [
    {
      id: "bluetooth_speaker",
      emoji: "\u{1F50A}",
      name: "Bluetooth Speaker",
      desc: "Smuggled in under a stack of bins. Boosts base vibe rate.",
      baseCost: 15,
      effect: { type: "vibeRate", value: 0.5 },
    },
    {
      id: "premium_bins",
      emoji: "\u{1F4E6}",
      name: "Premium Bins",
      desc: "The good ones with the lids that actually click. Boosts click power.",
      baseCost: 25,
      effect: { type: "clickPower", value: 1 },
    },
    {
      id: "mood_lighting",
      emoji: "\u{1F4A1}",
      name: "Mood Lighting",
      desc: "LED strips taped under the shelving units. Nobody's asked about them yet.",
      baseCost: 40,
      effect: { type: "vibeRate", value: 1 },
    },
    {
      id: "employee_playlist",
      emoji: "\u{1F3B5}",
      name: "Employee Playlist",
      desc: "Someone changed the store music. It's subtle but it slaps.",
      baseCost: 60,
      effect: { type: "vibeRate", value: 2 },
    },
    {
      id: "storage_ottoman",
      emoji: "\u{1F6CB}\u{FE0F}",
      name: "Storage Ottoman",
      desc: "Dual purpose: seating AND storage. Peak Container Store.",
      baseCost: 35,
      effect: { type: "clickPower", value: 2 },
    },
    {
      id: "aromatherapy_diffuser",
      emoji: "\u{1F9F4}",
      name: "Aromatherapy Diffuser",
      desc: "Lavender and bass. Widens the range of vibes that feel right in here.",
      baseCost: 45,
      effect: { type: "comfyRange", value: 5 },
    },
  ],
  2: [
    {
      id: "fake_badge",
      emoji: "\u{1FAA7}",
      name: "Fake Badge",
      desc: "Says 'MANAGER' in Comic Sans. The employees are confused enough to let you pass.",
      baseCost: 80,
      effect: { type: "vibeRate", value: 2 },
    },
    {
      id: "dark_hoodie",
      emoji: "\u{1F9E5}",
      name: "Dark Hoodie",
      desc: "Warehouse chic. Dance harder with less scrutiny.",
      baseCost: 60,
      effect: { type: "clickPower", value: 3 },
    },
    {
      id: "clipboard",
      emoji: "\u{1F4CB}",
      name: "Clipboard",
      desc: "Holding a clipboard makes you look official. Passive vibe just radiates.",
      baseCost: 100,
      effect: { type: "vibeRate", value: 3 },
    },
    {
      id: "confidence_juice",
      emoji: "\u{1F9C3}",
      name: "Confidence Juice",
      desc: "It's just water, but the label says 'CONFIDENCE JUICE' and that's enough.",
      baseCost: 50,
      effect: { type: "clickPower", value: 2 },
    },
    {
      id: "bribed_security",
      emoji: "\u{1F46E}",
      name: "Bribed Security",
      desc: "The guard nods and looks the other way. Professional courtesy.",
      baseCost: 150,
      effect: { type: "vibeRate", value: 5 },
    },
    {
      id: "warehouse_zen",
      emoji: "\u{1F9D8}",
      name: "Warehouse Zen",
      desc: "A meditation corner behind the pallets. Your comfort zone expands.",
      baseCost: 80,
      effect: { type: "comfyRange", value: 5 },
    },
  ],
};

// Item spawning config
var ITEM_SPAWN_MIN = 8000;   // ms between item spawns
var ITEM_SPAWN_MAX = 20000;
var ITEM_LINGER_TIME = 45000; // ms an item stays before vanishing
var ITEM_COST_SCALE = 1.3;    // price multiplier per copy owned

// ============================================================
// Constants
// ============================================================

const BASE_CLICK_VIBE = 1;
const SAVE_KEY = "platos-rave-save";
const SAVE_INTERVAL_MS = 30000;
const OFFLINE_CAP_SECONDS = 86400;

const PULSE_PER_CLICK = 5;
const PULSE_DECAY_RATE = 2;

const OPTIMAL_BONUS = 2.0;
const PENALTY_FLOOR = 0.5;

// ============================================================
// State
// ============================================================

function createDefaultState() {
  return {
    version: 3,
    lastSaved: Date.now(),
    vibe: 0,
    totalVibeEarned: 0,
    kandi: 0,
    prestigeCount: 0,
    currentRoom: 1,
    pressure: 10,
    pulse: 10,
    rooms: {
      1: { unlocked: true, level: 1 },
      2: { unlocked: false, level: 0 },
    },
    // Per-room inventory: { "1": { "bluetooth_speaker": 2, "premium_bins": 1 }, ... }
    inventory: {},
    stats: {
      totalClicks: 0,
      totalVibeAllTime: 0,
    },
  };
}

let state = createDefaultState();

// ============================================================
// Save / Load
// ============================================================

function saveGame() {
  state.lastSaved = Date.now();
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(state));
  } catch (e) { console.warn("Save failed:", e); }
}

function loadGame() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return null;
    const saved = JSON.parse(raw);
    if (saved && saved.version === 3) return saved;
    // Wipe incompatible saves
    localStorage.removeItem(SAVE_KEY);
    return null;
  } catch (e) {
    console.warn("Load failed:", e);
    return null;
  }
}

function calculateOfflineEarnings(savedState) {
  if (!savedState.lastSaved || isNaN(savedState.lastSaved)) return 0;
  var elapsed = Math.min(
    (Date.now() - savedState.lastSaved) / 1000,
    OFFLINE_CAP_SECONDS
  );
  if (elapsed < 5 || isNaN(elapsed)) return 0;
  // Temporarily swap state so getCurrentVibeRate() uses saved inventory/items
  var prevState = state;
  state = savedState;
  var rate;
  try {
    rate = getCurrentVibeRate();
  } catch (e) {
    console.warn("Offline rate calc failed:", e);
    rate = 0;
  } finally {
    state = prevState;
  }
  return Math.floor(rate * elapsed);
}

// ============================================================
// Economy
// ============================================================

function clamp(val, min, max) {
  return Math.max(min, Math.min(max, val));
}

function statFitness(value, range) {
  if (value >= range[0] && value <= range[1]) return 1;
  var dist = value < range[0] ? range[0] - value : value - range[1];
  return Math.max(0, 1 - dist / 50);
}

function getRoomMultiplier(roomNum) {
  var room = ROOMS[roomNum];
  if (!room) return 1;
  var pRange = getEffectiveOptimalRange(roomNum, "pressure");
  var sRange = getEffectiveOptimalRange(roomNum, "pulse");
  var pFit = statFitness(state.pressure, pRange);
  var sFit = statFitness(state.pulse, sRange);
  var fit = (pFit + sFit) / 2;
  return PENALTY_FLOOR + fit * (OPTIMAL_BONUS - PENALTY_FLOOR);
}

function getEffectiveOptimalRange(roomNum, stat) {
  var room = ROOMS[roomNum];
  if (!room) return [0, 100];
  var base = stat === "pressure" ? room.optimalPressure : room.optimalPulse;
  var expand = getItemBonus(roomNum, "comfyRange");
  return [
    Math.max(0, base[0] - expand),
    Math.min(100, base[1] + expand),
  ];
}

function getItemBonus(roomNum, effectType) {
  var inv = state.inventory[roomNum];
  if (!inv) return 0;
  var items = ROOM_ITEMS[roomNum];
  if (!items) return 0;
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var count = inv[item.id] || 0;
    if (count > 0 && item.effect.type === effectType) {
      total += item.effect.value * count;
    }
  }
  return total;
}

function getCurrentVibeRate() {
  var room = ROOMS[state.currentRoom];
  if (!room) return 0;
  var rs = state.rooms[state.currentRoom];
  var level = (rs && rs.level) ? rs.level : 1;
  var base = room.baseVibeRate * level;
  var itemBonus = getItemBonus(state.currentRoom, "vibeRate");
  return (base + itemBonus) * getRoomMultiplier(state.currentRoom);
}

function getClickValue() {
  var room = ROOMS[state.currentRoom];
  if (!room) return BASE_CLICK_VIBE;
  var mult = getRoomMultiplier(state.currentRoom);
  var itemBonus = getItemBonus(state.currentRoom, "clickPower");
  return Math.max(1, Math.floor((BASE_CLICK_VIBE * room.clickMultiplier + itemBonus) * mult));
}

function getItemCost(roomNum, itemId) {
  var items = ROOM_ITEMS[roomNum];
  if (!items) return Infinity;
  var inv = state.inventory[roomNum] || {};
  for (var i = 0; i < items.length; i++) {
    if (items[i].id === itemId) {
      var owned = inv[itemId] || 0;
      return Math.floor(items[i].baseCost * Math.pow(ITEM_COST_SCALE, owned));
    }
  }
  return Infinity;
}

function addVibe(amount) {
  state.vibe += amount;
  state.totalVibeEarned += amount;
  state.stats.totalVibeAllTime += amount;
}

// ============================================================
// Number Formatting
// ============================================================

function formatNumber(n) {
  if (!isFinite(n)) return "0";
  if (n < 1000) return Math.floor(n).toString();
  var suffixes = ["", "K", "M", "B", "T", "Qa", "Qi"];
  var tier = Math.floor(Math.log10(Math.abs(n)) / 3);
  if (tier === 0) return Math.floor(n).toString();
  var suffix = suffixes[tier] || ("e" + tier * 3);
  var scaled = n / Math.pow(10, tier * 3);
  return scaled.toFixed(1) + suffix;
}

// ============================================================
// DOM
// ============================================================

var dom = {
  vibeCount: document.getElementById("vibe-count"),
  vibePerSec: document.getElementById("vibe-per-sec"),
  pressureFill: document.getElementById("pressure-fill"),
  pulseFill: document.getElementById("pulse-fill"),
  pressureOptimal: document.getElementById("pressure-optimal"),
  pulseOptimal: document.getElementById("pulse-optimal"),
  pressureValue: document.getElementById("pressure-value"),
  pulseValue: document.getElementById("pulse-value"),
  roomView: document.getElementById("room-view"),
  roomSpace: document.getElementById("room-space"),
  dancer: document.getElementById("dancer"),
  clickFeedback: document.getElementById("click-feedback"),
  multiplier: document.getElementById("multiplier"),
  multiplierValue: document.getElementById("multiplier-value"),
  navLeft: document.getElementById("nav-left"),
  navRight: document.getElementById("nav-right"),
  roomTitle: document.getElementById("room-title"),
  roomFlavor: document.getElementById("room-flavor"),
  unlockPrompt: document.getElementById("unlock-prompt"),
  unlockText: document.getElementById("unlock-text"),
  unlockButton: document.getElementById("unlock-button"),
  roomMap: document.getElementById("room-map"),
  welcomeBack: document.getElementById("welcome-back"),
  welcomeMessage: document.getElementById("welcome-message"),
  welcomeDismiss: document.getElementById("welcome-dismiss"),
  spreadLoveBtn: document.getElementById("spread-love-btn"),
};

// ============================================================
// Rendering
// ============================================================

function renderStats() {
  dom.vibeCount.textContent = formatNumber(state.vibe);
  dom.vibePerSec.textContent = formatNumber(getCurrentVibeRate());

  var p = clamp(state.pressure, 0, 100);
  var s = clamp(state.pulse, 0, 100);
  dom.pressureFill.style.width = p + "%";
  dom.pulseFill.style.width = s + "%";
  dom.pressureValue.textContent = Math.floor(p);
  dom.pulseValue.textContent = Math.floor(s);

  // Spread the love: enabled when you have at least 1 vibe to spend
  dom.spreadLoveBtn.disabled = Math.floor(state.vibe * 0.1) < 1;
}

function renderOptimalRanges() {
  var room = ROOMS[state.currentRoom];
  if (!room) return;

  var pRange = getEffectiveOptimalRange(state.currentRoom, "pressure");
  var sRange = getEffectiveOptimalRange(state.currentRoom, "pulse");

  dom.pressureOptimal.style.left = pRange[0] + "%";
  dom.pressureOptimal.style.width = (pRange[1] - pRange[0]) + "%";
  dom.pulseOptimal.style.left = sRange[0] + "%";
  dom.pulseOptimal.style.width = (sRange[1] - sRange[0]) + "%";
}

function renderRoom() {
  var room = ROOMS[state.currentRoom];
  if (!room) return;
  dom.roomTitle.textContent = "Room " + state.currentRoom + " \u2014 " + room.name;
  dom.roomFlavor.textContent = room.flavor;

  // Set room art class
  dom.roomSpace.className = room.artClass;
}

function renderMultiplier() {
  var mult = getRoomMultiplier(state.currentRoom);
  if (Math.abs(mult - 1) < 0.05) {
    dom.multiplier.classList.add("hidden");
    return;
  }
  dom.multiplier.classList.remove("hidden");
  dom.multiplierValue.textContent = mult.toFixed(1) + "x";
  dom.multiplier.classList.remove("bonus", "penalty");
  dom.multiplier.classList.add(mult >= 1 ? "bonus" : "penalty");
}

function renderNav() {
  var prevRoom = state.currentRoom - 1;
  dom.navLeft.disabled = prevRoom < 1 || !state.rooms[prevRoom] || !state.rooms[prevRoom].unlocked;

  var nextRoom = state.currentRoom + 1;
  var nextExists = !!ROOMS[nextRoom];
  var nextUnlocked = state.rooms[nextRoom] && state.rooms[nextRoom].unlocked;

  dom.navRight.disabled = !nextUnlocked;

  if (nextExists && !nextUnlocked) {
    var cost = ROOMS[nextRoom].unlockCost;
    dom.unlockPrompt.classList.remove("hidden");
    dom.unlockText.textContent = formatNumber(cost) + " Vibe";
    dom.unlockButton.disabled = state.vibe < cost;
  } else {
    dom.unlockPrompt.classList.add("hidden");
  }
}

function renderMap() {
  // 3 slots centered on current room
  // Room 0 = mystery "?" (the loop hint), always locked
  var center = state.currentRoom;
  var slots = [center - 1, center, center + 1];

  for (var i = 0; i < 3; i++) {
    var roomNum = slots[i];
    var node = document.getElementById("map-slot-" + i);
    var edge = document.getElementById("map-edge-" + i);

    node.className = "map-node";

    if (roomNum === 0) {
      // Mystery room — the loop
      node.classList.add("locked");
      node.textContent = "?";
    } else if (roomNum < 0) {
      // Off the map
      node.classList.add("locked");
      node.textContent = "";
      node.style.visibility = "hidden";
      if (edge) edge.style.visibility = "hidden";
      continue;
    } else if (ROOMS[roomNum]) {
      var rs = state.rooms[roomNum];
      var unlocked = rs && rs.unlocked;
      if (unlocked) {
        node.classList.add("unlocked");
        node.textContent = String(roomNum);
      } else {
        node.classList.add("locked");
        node.textContent = "?";
      }
    } else {
      // Beyond defined rooms
      node.classList.add("locked");
      node.textContent = "?";
    }

    if (roomNum === state.currentRoom) {
      node.classList.add("current");
    }

    node.style.visibility = "";
    if (edge) edge.style.visibility = "";
  }
}

function renderDancerState() {
  var rate = getCurrentVibeRate();
  if (rate > 0) {
    dom.dancer.classList.add("vibing");
  } else {
    dom.dancer.classList.remove("vibing");
  }
}

function renderAll() {
  renderStats();
  renderOptimalRanges();
  renderRoom();
  renderMultiplier();
  renderNav();
  renderMap();
  renderDancerState();
  spawnNPCs();
  startAmbient();
  removeActiveItem();
  startItemSpawner();
  renderInventory();
}

// ============================================================
// Click Feedback
// ============================================================

function spawnClickPop(value, x, y) {
  var pop = document.createElement("div");
  pop.className = "click-pop";
  pop.textContent = "+" + formatNumber(value);

  var rect = dom.clickFeedback.getBoundingClientRect();
  pop.style.left = (x - rect.left + (Math.random() - 0.5) * 40) + "px";
  pop.style.top = (y - rect.top - 10) + "px";

  dom.clickFeedback.appendChild(pop);
  pop.addEventListener("animationend", function() { pop.remove(); });
}

function triggerDanceAnimation() {
  dom.dancer.classList.remove("dancing", "vibing");
  void dom.dancer.offsetWidth; // force reflow to restart animation
  dom.dancer.classList.add("dancing");
  // Return to vibing after the dance burst
  setTimeout(function() {
    dom.dancer.classList.remove("dancing");
    renderDancerState();
  }, 250);
}

// ============================================================
// NPC Rave Attendees
// ============================================================

var activeNPCs = [];

function spawnNPCs() {
  // Clear existing
  for (var i = 0; i < activeNPCs.length; i++) {
    if (activeNPCs[i].parentNode) activeNPCs[i].parentNode.removeChild(activeNPCs[i]);
  }
  activeNPCs = [];

  var flavor = ROOM_FLAVOR[state.currentRoom];
  if (!flavor) return;

  var container = document.getElementById("room-space");

  for (var n = 0; n < flavor.npcCount; n++) {
    var npc = document.createElement("div");
    npc.className = "npc-dancer";

    var color = flavor.npcColors[n % flavor.npcColors.length];
    // Random position on the "floor" area
    var xPos = 10 + Math.random() * 80; // 10-90% horizontal
    var yPos = 45 + Math.random() * 35; // 45-80% vertical (floor area)
    var scale = 0.5 + (yPos - 45) / 70; // Closer to bottom = larger (perspective)
    var animDuration = 0.4 + Math.random() * 0.4; // Varied dance speed
    var animDelay = Math.random() * -2; // Staggered

    npc.style.cssText =
      "position:absolute;" +
      "left:" + xPos + "%;" +
      "top:" + yPos + "%;" +
      "--npc-scale:" + scale.toFixed(2) + ";" +
      "z-index:" + Math.floor(yPos) + ";" +
      "animation:npc-dance " + animDuration.toFixed(2) + "s ease-in-out " + animDelay.toFixed(2) + "s infinite;";

    // Head
    var head = document.createElement("div");
    head.className = "npc-head";
    head.style.background = color;
    head.style.boxShadow = "0 0 8px " + color + "44";

    // Body
    var body = document.createElement("div");
    body.className = "npc-body";
    body.style.background = color;
    body.style.boxShadow = "0 0 6px " + color + "44";

    // Legs
    var legs = document.createElement("div");
    legs.className = "npc-legs";
    var legL = document.createElement("div");
    legL.className = "npc-leg";
    legL.style.background = color;
    legL.style.opacity = "0.7";
    var legR = document.createElement("div");
    legR.className = "npc-leg";
    legR.style.background = color;
    legR.style.opacity = "0.7";
    legs.appendChild(legL);
    legs.appendChild(legR);

    npc.appendChild(head);
    npc.appendChild(body);
    npc.appendChild(legs);

    container.appendChild(npc);
    activeNPCs.push(npc);
  }
}

// ============================================================
// Ambient Flavor Text System
// ============================================================

var ambientTimer = null;

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function spawnAmbientText() {
  var flavor = ROOM_FLAVOR[state.currentRoom];
  if (!flavor) return;

  var container = dom.clickFeedback; // reuse click-feedback layer (same positioning/z-index)
  var roll = Math.random();
  var text;
  var cssClass;

  if (roll < 0.35) {
    // Onomatopoeia
    text = pickRandom(flavor.sounds);
    cssClass = "ambient-sound";
  } else if (roll < 0.55) {
    // Emoji
    text = pickRandom(flavor.emojis);
    cssClass = "ambient-emoji";
  } else {
    // NPC quote
    text = "\u201C" + pickRandom(flavor.quotes) + "\u201D";
    cssClass = "ambient-quote";
  }

  var el = document.createElement("div");
  el.className = "ambient-pop " + cssClass;
  el.textContent = text;

  // Random position across the room
  var xPos = 5 + Math.random() * 90;
  var yPos = 20 + Math.random() * 60;
  el.style.left = xPos + "%";
  el.style.top = yPos + "%";

  container.appendChild(el);
  el.addEventListener("animationend", function() { el.remove(); });

  // Schedule next
  var nextDelay = AMBIENT_INTERVAL_MIN +
    Math.random() * (AMBIENT_INTERVAL_MAX - AMBIENT_INTERVAL_MIN);
  ambientTimer = setTimeout(spawnAmbientText, nextDelay);
}

function startAmbient() {
  if (ambientTimer) clearTimeout(ambientTimer);
  var delay = AMBIENT_INTERVAL_MIN +
    Math.random() * (AMBIENT_INTERVAL_MAX - AMBIENT_INTERVAL_MIN);
  ambientTimer = setTimeout(spawnAmbientText, delay);
}

// ============================================================
// Item Spawning System
// ============================================================

var itemSpawnTimer = null;
var activeItemEl = null;
var activeItemData = null;
var activeItemLingerTimer = null;

function startItemSpawner() {
  if (itemSpawnTimer) clearTimeout(itemSpawnTimer);
  var delay = ITEM_SPAWN_MIN + Math.random() * (ITEM_SPAWN_MAX - ITEM_SPAWN_MIN);
  itemSpawnTimer = setTimeout(spawnItem, delay);
}

function spawnItem() {
  // Don't spawn if one's already there
  if (activeItemEl) {
    startItemSpawner();
    return;
  }

  var items = ROOM_ITEMS[state.currentRoom];
  if (!items || items.length === 0) {
    startItemSpawner();
    return;
  }

  var item = pickRandom(items);
  var cost = getItemCost(state.currentRoom, item.id);

  activeItemData = { roomNum: state.currentRoom, item: item, cost: cost };

  var el = document.createElement("div");
  el.className = "room-item";

  var emojiSpan = document.createElement("span");
  emojiSpan.className = "room-item-emoji";
  emojiSpan.textContent = item.emoji;
  el.appendChild(emojiSpan);

  var priceTag = document.createElement("span");
  priceTag.className = "room-item-price";
  priceTag.textContent = formatNumber(cost);
  el.appendChild(priceTag);

  // Random position on the floor area
  var xPos = 15 + Math.random() * 70;
  var yPos = 40 + Math.random() * 30;
  el.style.left = xPos + "%";
  el.style.top = yPos + "%";
  el.style.zIndex = Math.floor(yPos + 1);

  el.addEventListener("pointerdown", function(e) {
    e.stopPropagation();
    e.preventDefault();
    if (activeItemData) showItemPopup(activeItemData);
  });

  document.getElementById("room-space").appendChild(el);
  activeItemEl = el;

  // Item vanishes after linger time
  activeItemLingerTimer = setTimeout(removeActiveItem, ITEM_LINGER_TIME);

  // Schedule next spawn
  startItemSpawner();
}

function removeActiveItem() {
  if (activeItemLingerTimer) {
    clearTimeout(activeItemLingerTimer);
    activeItemLingerTimer = null;
  }
  if (activeItemEl && activeItemEl.parentNode) {
    activeItemEl.parentNode.removeChild(activeItemEl);
  }
  activeItemEl = null;
  activeItemData = null;
}

// ============================================================
// Item Purchase Popup
// ============================================================

function showItemPopup(data) {
  var overlay = document.getElementById("item-popup");
  var owned = 0;
  if (state.inventory[data.roomNum]) {
    owned = state.inventory[data.roomNum][data.item.id] || 0;
  }
  var cost = data.cost;
  var effectDesc = "";
  if (data.item.effect.type === "vibeRate") {
    effectDesc = "+" + data.item.effect.value + " Vibe/s in this room";
  } else if (data.item.effect.type === "clickPower") {
    effectDesc = "+" + data.item.effect.value + " click power in this room";
  } else if (data.item.effect.type === "comfyRange") {
    effectDesc = "+" + data.item.effect.value + " comfort zone in this room";
  }

  document.getElementById("item-popup-emoji").textContent = data.item.emoji;
  document.getElementById("item-popup-name").textContent = data.item.name;
  document.getElementById("item-popup-desc").textContent = data.item.desc;
  document.getElementById("item-popup-effect").textContent = effectDesc;
  document.getElementById("item-popup-owned").textContent = owned > 0 ? "Owned: " + owned : "";
  var buyBtn = document.getElementById("item-popup-buy");
  buyBtn.textContent = "Buy \u2014 " + formatNumber(cost) + " Vibe";
  buyBtn.disabled = state.vibe < cost;
  buyBtn.style.display = "";

  buyBtn.onclick = function() {
    if (state.vibe < cost) return;
    state.vibe -= cost;
    if (!state.inventory[data.roomNum]) state.inventory[data.roomNum] = {};
    state.inventory[data.roomNum][data.item.id] = (state.inventory[data.roomNum][data.item.id] || 0) + 1;
    removeActiveItem();
    overlay.classList.add("hidden");
    renderStats();
    renderOptimalRanges();
    renderMultiplier();
    renderNav();
    renderInventory();
  };

  document.getElementById("item-popup-dismiss").onclick = function() {
    overlay.classList.add("hidden");
  };

  overlay.classList.remove("hidden");
}

// ============================================================
// Room Inventory Display
// ============================================================

function renderInventory() {
  var container = document.getElementById("room-inventory");
  container.replaceChildren();

  var inv = state.inventory[state.currentRoom];
  if (!inv) return;

  var items = ROOM_ITEMS[state.currentRoom];
  if (!items) return;

  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var count = inv[item.id] || 0;
    if (count === 0) continue;

    var slot = document.createElement("button");
    slot.className = "inv-slot";
    slot.setAttribute("data-item-id", item.id);
    slot.setAttribute("data-room", String(state.currentRoom));

    var emojiEl = document.createElement("span");
    emojiEl.className = "inv-emoji";
    emojiEl.textContent = item.emoji;
    slot.appendChild(emojiEl);

    if (count > 1) {
      var countEl = document.createElement("span");
      countEl.className = "inv-count";
      countEl.textContent = "x" + count;
      slot.appendChild(countEl);
    }

    slot.addEventListener("pointerdown", (function(itm, cnt, rm) {
      return function(e) {
        e.stopPropagation();
        e.preventDefault();
        showInventoryDetail(itm, cnt, rm);
      };
    })(item, count, state.currentRoom));

    container.appendChild(slot);
  }
}

function showInventoryDetail(item, count, roomNum) {
  var effectDesc = "";
  var total = item.effect.value * count;
  if (item.effect.type === "vibeRate") {
    effectDesc = "+" + total + " Vibe/s (" + item.effect.value + " each)";
  } else if (item.effect.type === "clickPower") {
    effectDesc = "+" + total + " click power (" + item.effect.value + " each)";
  } else if (item.effect.type === "comfyRange") {
    effectDesc = "+" + total + " comfort zone (" + item.effect.value + " each)";
  }

  document.getElementById("item-popup-emoji").textContent = item.emoji;
  document.getElementById("item-popup-name").textContent = item.name;
  document.getElementById("item-popup-desc").textContent = item.desc;
  document.getElementById("item-popup-effect").textContent = effectDesc;
  document.getElementById("item-popup-owned").textContent = "Owned: " + count;
  // Hide buy button for inventory detail view

  var buyBtn = document.getElementById("item-popup-buy");
  buyBtn.style.display = "none";

  document.getElementById("item-popup-dismiss").onclick = function() {
    document.getElementById("item-popup").classList.add("hidden");
    buyBtn.style.display = "";
  };

  document.getElementById("item-popup").classList.remove("hidden");
}

// ============================================================
// Actions
// ============================================================

function handleTap(e) {
  e.preventDefault();

  var value = getClickValue();
  addVibe(value);
  state.stats.totalClicks++;
  state.pulse = clamp(state.pulse + PULSE_PER_CLICK, 0, 100);

  var clientX = e.clientX;
  var clientY = e.clientY;
  spawnClickPop(value, clientX, clientY);
  triggerDanceAnimation();

  renderStats();
  renderMultiplier();
  renderNav();
}

function navigateRoom(direction) {
  var target = state.currentRoom + direction;
  if (!ROOMS[target]) return;
  var rs = state.rooms[target];
  if (!rs || !rs.unlocked) return;
  state.currentRoom = target;
  renderAll();
}

function spreadTheLove() {
  var cost = Math.floor(state.vibe * 0.1);
  if (cost < 1) return;
  state.vibe -= cost;
  state.pressure = clamp(state.pressure * 0.9, 0, 100);
  renderStats();
  renderMultiplier();
  renderNav();
}

function unlockNextRoom() {
  var nextRoom = state.currentRoom + 1;
  if (!ROOMS[nextRoom]) return;
  var cost = ROOMS[nextRoom].unlockCost;
  if (state.vibe < cost) return;

  state.vibe -= cost;
  state.rooms[nextRoom] = { unlocked: true, level: 1 };
  state.currentRoom = nextRoom;
  renderAll();
}

// ============================================================
// Game Loop
// ============================================================

var lastTick = Date.now();

function gameTick() {
  var now = Date.now();
  var dt = (now - lastTick) / 1000;
  lastTick = now;

  // Passive vibe from current room
  var vibeRate = getCurrentVibeRate();
  if (vibeRate > 0) {
    addVibe(vibeRate * dt);
  }

  // Pressure drifts based on room
  var room = ROOMS[state.currentRoom];
  if (room) {
    state.pressure = clamp(state.pressure + room.pressureEffect * dt, 0, 100);
  }

  // Pulse decays
  if (state.pulse > 0) {
    state.pulse = clamp(state.pulse - PULSE_DECAY_RATE * dt, 0, 100);
  }

  renderStats();
  renderMultiplier();
  renderNav();

  requestAnimationFrame(gameTick);
}

// ============================================================
// Events
// ============================================================

dom.roomView.addEventListener("pointerdown", handleTap);

dom.navLeft.addEventListener("click", function(e) { e.stopPropagation(); navigateRoom(-1); });
dom.navRight.addEventListener("click", function(e) { e.stopPropagation(); navigateRoom(1); });
dom.unlockButton.addEventListener("click", function(e) { e.stopPropagation(); unlockNextRoom(); });
dom.spreadLoveBtn.addEventListener("click", function(e) { e.stopPropagation(); spreadTheLove(); });

// Prevent bottom panel and popup taps from triggering room tap
document.getElementById("bottom-panel").addEventListener("pointerdown", function(e) {
  e.stopPropagation();
});
document.getElementById("item-popup").addEventListener("pointerdown", function(e) {
  e.stopPropagation();
});

dom.welcomeDismiss.addEventListener("click", function() {
  dom.welcomeBack.classList.add("hidden");
});

setInterval(saveGame, SAVE_INTERVAL_MS);
window.addEventListener("beforeunload", saveGame);

// ============================================================
// Init
// ============================================================

function init() {
  var saved = loadGame();

  if (saved) {
    // Merge saved onto defaults so any missing fields get safe values
    var defaults = createDefaultState();
    for (var key in defaults) {
      if (saved[key] === undefined) saved[key] = defaults[key];
    }
    if (!saved.stats) saved.stats = defaults.stats;
    if (!saved.inventory) saved.inventory = defaults.inventory;

    var offlineEarnings = calculateOfflineEarnings(saved);
    state = saved;

    if (offlineEarnings > 0) {
      addVibe(offlineEarnings);
      var elapsed = Math.min(
        (Date.now() - saved.lastSaved) / 1000,
        OFFLINE_CAP_SECONDS
      );
      var hours = Math.floor(elapsed / 3600);
      var minutes = Math.floor((elapsed % 3600) / 60);
      var timeStr = "";
      if (hours > 0) timeStr += hours + "h ";
      timeStr += minutes + "m";

      dom.welcomeMessage.textContent =
        "You were gone for " + timeStr +
        ". Your dancer earned " + formatNumber(offlineEarnings) +
        " Vibe while you were away.";
      dom.welcomeBack.classList.remove("hidden");
    }
  }

  // Ensure all rooms exist in state
  for (var roomNum in ROOMS) {
    if (!state.rooms[roomNum]) {
      state.rooms[roomNum] = { unlocked: false, level: 0 };
    }
  }

  renderAll();
  lastTick = Date.now();
  requestAnimationFrame(gameTick);
}

init();
