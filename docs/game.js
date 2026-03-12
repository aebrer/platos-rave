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
  3: {
    name: "Dry Rub Wings",
    flavor: "We DoorDashed in Buffalo Wild Wings for room three. Dry rub only. Dry rub sauce comes in room six.",
    unlockCost: 200,
    baseVibeRate: 7,
    clickMultiplier: 2,
    pressureEffect: -1,
    optimalPressure: [10, 40],
    optimalPulse: [10, 40],
    artClass: "room-3",
  },
  4: {
    name: "The Best Rave of Your Life",
    flavor: "Fucking out of control. The best, fucking hardest rave you've ever been to in your whole life.",
    unlockCost: 600,
    baseVibeRate: 18,
    clickMultiplier: 4,
    pressureEffect: 3,
    optimalPressure: [40, 70],
    optimalPulse: [50, 80],
    artClass: "room-4",
  },
  5: {
    name: "Barometric Pressure",
    flavor: "You're gonna feel the pressure on your body. Your ears are gonna pop. It's like you're lowering down in the ocean.",
    unlockCost: 1500,
    baseVibeRate: 14,
    clickMultiplier: 3,
    pressureEffect: 5,
    optimalPressure: [55, 85],
    optimalPulse: [30, 60],
    artClass: "room-5",
  },
  6: {
    name: "Sauce on Six",
    flavor: "The sauce brings you back from the intense barotrauma. After the barotrauma, they're gonna taste like the best fuckin' wings.",
    unlockCost: 4000,
    baseVibeRate: 30,
    clickMultiplier: 3,
    pressureEffect: -3,
    optimalPressure: [20, 55],
    optimalPulse: [15, 50],
    artClass: "room-6",
  },
  7: {
    name: "Traps",
    flavor: "All traps. Trap music. Trap drums. People with big trap muscles watching you. Trapezes to swing over the traps. Gothic circus. You'll love it.",
    unlockCost: 10000,
    baseVibeRate: 50,
    clickMultiplier: 5,
    pressureEffect: 2.5,
    optimalPressure: [35, 65],
    optimalPulse: [40, 75],
    artClass: "room-7",
  },
  8: {
    name: "The Final Deception",
    flavor: "The Container Store again. They want you to think you failed. There is no level eight, nine or ten. This is all we've made.",
    unlockCost: 25000,
    baseVibeRate: 55,
    clickMultiplier: 3,
    pressureEffect: 0,
    optimalPressure: [25, 75],
    optimalPulse: [25, 75],
    artClass: "room-8",
  },
  9: {
    name: "Nirvana",
    flavor: "Nine is nirvana, baby. Nine is the best, objectively the best layer. Nine is the best rave. You don't want to leave.",
    unlockCost: 75000,
    baseVibeRate: 80,
    clickMultiplier: 4,
    pressureEffect: -2,
    optimalPressure: [20, 60],
    optimalPulse: [20, 60],
    artClass: "room-9",
  },
  10: {
    name: "The Candy King",
    flavor: "A dark room. One man. Candy crown of beads. Just hard candy regalia. A single spotlight. He looks down at you.",
    unlockCost: 200000,
    baseVibeRate: 10,
    clickMultiplier: 10,
    pressureEffect: 0,
    optimalPressure: [0, 100],
    optimalPulse: [0, 100],
    artClass: "room-10",
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
  3: {
    sounds: [
      "*crunch*", "*munch*", "CHOMP", "*sizzle*", "*snap*",
      "NOM", "*lick*", "CRACKLE", "*burp*",
    ],
    emojis: [
      "\u{1F357}", "\u{1F356}", "\u{1F525}", "\u{1F9C2}", "\u{1F37A}",
      "\u{1F9FB}", "\u{1F4A8}", "\u{1F60B}",
    ],
    quotes: [
      "Dry rub is so smart, by the way",
      "You're gonna want to pace that out",
      "Best wings in town, honestly",
      "No sauce for me, thanks",
      "I came for the wings and I'm leaving",
      "Is there a non-pressurized exit?",
      "We got vegan options too, right?",
      "I like Impossible Nuggets a lot",
      "Six wings, how fast can you drain 'em?",
      "These are the checkpoints",
      "You earned these free buffalo wings",
      "Sir this is a DoorDash order",
      "I'm spending some time here",
    ],
    npcColors: ["#ff8844", "#ffcc33", "#ee5533", "#ffaa77"],
    npcCount: 4,
  },
  4: {
    sounds: [
      "UNTZ UNTZ UNTZ", "BASS DROP", "WOOOOO", "THUMP THUMP",
      "*screaming*", "WUBWUBWUB", "BOOM BOOM", "YEAHHH", "LETS GOOO",
    ],
    emojis: [
      "\u{1F525}", "\u{1F4A5}", "\u{1F31F}", "\u{26A1}", "\u{1F680}",
      "\u{1F3B6}", "\u{1F4AB}", "\u{1F389}",
    ],
    quotes: [
      "I CAN'T GET BETTER THAN THIS",
      "Your consciousness is going to exist on a level that is UNTHINKABLE",
      "We've been here for three hours and I don't care",
      "The normal sort of id and ego don't apply here",
      "You might get froze up here",
      "I'm going to tell my family I went to a movie",
      "THIS IS THE PEAK",
      "Don't ascend too quickly. That's hubris.",
      "Two hours. Let's say two hours.",
      "By definition, the best rave of my life can't last longer than 45 minutes",
      "UNTS UNTS UNTS",
      "I never want to leave this room",
      "Is it getting louder or am I ascending?",
    ],
    npcColors: ["#ff00ff", "#00ffff", "#ffff00", "#ff4444", "#44ff44"],
    npcCount: 6,
  },
  5: {
    sounds: [
      "*pop*", "*creak*", "HISSSSS", "*groan*", "CLANK",
      "*whoosh*", "*drip*", "PRESSURE", "*ears ringing*",
    ],
    emojis: [
      "\u{1F30A}", "\u{1F4A7}", "\u{2693}", "\u{1F6E2}\u{FE0F}", "\u{1F300}",
      "\u{1F9CA}", "\u{1FAE7}", "\u{1F6DF}",
    ],
    quotes: [
      "My ears just popped",
      "It's like you're lowering down in the ocean",
      "I'm gonna be crying at movies, just like on a plane",
      "We just pressurize it, like you do on planes",
      "I have a sudden desire for ginger ale",
      "IS IT STILL PRESSURIZED?!",
      "Layers five through ten are pressurized",
      "We need an airlock. The bathroom is an airlock.",
      "I don't want you doing traps with a mind not addled by intense barometric trauma",
      "The barotrauma is part of the experience",
      "My whole brain chemistry is different now",
      "If anyone opens a window, everyone gets launched out",
    ],
    npcColors: ["#4466aa", "#6688cc", "#335588", "#7799dd", "#2244aa"],
    npcCount: 5,
  },
  6: {
    sounds: [
      "*slurp*", "*drip*", "SAUCE", "*splash*", "*sizzle*",
      "NOM NOM", "*squelch*", "GLORIOUS", "*chomp*",
    ],
    emojis: [
      "\u{1F357}", "\u{1F525}", "\u{1F4A6}", "\u{1F37A}", "\u{1F92E}",
      "\u{1F924}", "\u{1F60B}", "\u{1F973}",
    ],
    quotes: [
      "SAUCE ON SIX",
      "The sauce brings you back",
      "After the barotrauma, these taste like the best fuckin' wings",
      "The wet wings are SO MUCH FASTER for some reason",
      "There are real wild folks who come here just for the sauced wings",
      "We don't know how drugs would interact with sauce",
      "You could just have dry rub but you chose barometric trauma instead",
      "This is also a ghost kitchen",
      "There's barely water. Barely water.",
      "Travis is right on this one. We have to respect the genius.",
      "Don't try to ration them for the later layers",
      "If we want the sauces to taste right, we needed the barotrauma",
      "I came for the exit on six and I'm not ashamed",
    ],
    npcColors: ["#ff6633", "#ff9944", "#cc4411", "#ffbb55", "#ee7722"],
    npcCount: 5,
  },
  7: {
    sounds: [
      "SNAP", "*clang*", "WHOOSH", "*twang*", "CRASH",
      "*swing*", "THWACK", "*creak*", "WUBWUB",
    ],
    emojis: [
      "\u{1F3AA}", "\u{1FA78}", "\u{2694}\u{FE0F}", "\u{1F52E}", "\u{1F3AD}",
      "\u{1F4AA}", "\u{1FA84}", "\u{1F6A8}",
    ],
    quotes: [
      "There are traps all the way down",
      "You do need the trapezes to get past the traps",
      "Everyone's dressed like the first Panic at the Disco album",
      "People are gonna be so fucked up and bedraggled by room seven",
      "If you already speak Latin, this goes faster",
      "Did you bring a prism? You should have brought a prism.",
      "Maybe you're strong. Maybe you just run across the traps.",
      "Get the ruby out of the gargoyle's eye socket",
      "Can you charm the dudes with big traps to help you out?",
      "The bathroom ain't trapped. We need to make that SO CLEAR.",
      "Is that Trapt? Why is Trapt here?",
      "Staind-brand earplugs to block out Trapt's music",
      "We don't need more distractions in here",
      "Maybe forever, if you're killed by a trap",
    ],
    npcColors: ["#880044", "#cc0066", "#990033", "#aa2255", "#660033"],
    npcCount: 5,
  },
  8: {
    sounds: [
      "*beep*", "*ding*", "*scanner*", "*shuffle*", "*rustle*",
      "*receipt printing*", "EXCUSE ME", "*intercom*", "*muzak*",
    ],
    emojis: [
      "\u{1F4E6}", "\u{1F6D2}", "\u{1F9FE}", "\u{1F50D}", "\u{1F3AD}",
      "\u{2753}", "\u{1F914}", "\u{1F440}",
    ],
    quotes: [
      "Welcome to The Container Store! Can I help you find anything?",
      "There is no level eight, nine or ten",
      "This is all we've made at this point",
      "Why would there be two Container Stores so close to each other?",
      "These are actors. Selling containers. To actors.",
      "It's a can't-tainer store",
      "There's one receipt in one till. Find it.",
      "We're deep underground at this point",
      "Is this part of the deception?",
      "I have never been to The Container Store",
      "I could use some 'tainers",
      "We have so many containers. So many different kinds.",
      "What do they ship the containers in? It's gonna fuck you up.",
      "Get the fuck out! Quit telling people we're doing raves here!",
    ],
    npcColors: ["#6688aa", "#88aa88", "#aa8866", "#8888aa", "#77aa77"],
    npcCount: 5,
  },
  9: {
    sounds: [
      "*bliss*", "ahhhhh", "*chime*", "*harp*", "*sigh*",
      "ohhhhm", "*bells*", "*wind*", "*birdsong*",
    ],
    emojis: [
      "\u{2728}", "\u{1F31F}", "\u{1F54A}\u{FE0F}", "\u{1F338}", "\u{1F3B6}",
      "\u{1F9D8}", "\u{1F30C}", "\u{1F49C}",
    ],
    quotes: [
      "Nine is nirvana, baby",
      "This is the transcendent experience you wanted",
      "You can't get out of nine until you don't want to go to ten",
      "You can't get to ten unless you're perfectly happy being in nine",
      "I really feel like there needs to be an archivist wing",
      "They've eschewed raving and devoted themselves to scholarship",
      "There's a long tunnel with pictures of your life",
      "Your highest moments. Your greatest times.",
      "The wisdom you bring from being ready to leave nine",
      "This is a level nine slapper, folks",
      "My Life Is Better With You",
      "The eternal afterlife pleasure garden",
      "I never want to leave",
      "Maybe you don't want to leave nine. And that's okay.",
    ],
    npcColors: ["#ffcc88", "#ffd700", "#ffee99", "#ffbb44", "#fff4cc"],
    npcCount: 6,
  },
  10: {
    sounds: [
      "...", "*silence*", "*heartbeat*", "*spotlight hum*", "*breath*",
      "*footstep*", "...", "*crackle*", "*echo*",
    ],
    emojis: [
      "\u{1F451}", "\u{1F36C}", "\u{1F506}", "\u{1FA91}", "\u{2B50}",
      "\u{1F480}", "\u{1F52E}", "\u{1F31F}",
    ],
    quotes: [
      "Not yet.",
      "Only one person in room ten at a time",
      "You better be raving harder than they are",
      "Or you're dead. I mean, not dead.",
      "He disintegrates. You become him.",
      "You become a Plato's Rave franchisee",
      "You're the candy king of Buffalo, New York",
      "Get on up there",
      "That's how they get a new Skrillex",
      "The candy king says nothing. He just looks.",
      "A single spotlight illuminates you",
      "Fuzzy boots. Candy crown. Hard candy regalia.",
    ],
    npcColors: ["#ffd700"],
    npcCount: 1,
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
  3: [
    {
      id: "classic_dry_rub",
      emoji: "\u{1F357}",
      name: "Classic Dry Rub Wings",
      desc: "The standard. Dry rub is so smart, by the way, with the evening they're gonna have.",
      baseCost: 100,
      effect: { type: "vibeRate", value: 2 },
    },
    {
      id: "boneless_dry_rub",
      emoji: "\u{1F356}",
      name: "Boneless Dry Rub",
      desc: "They got boneless! Same dry rub, less bone. You're filling up too much but you don't care.",
      baseCost: 150,
      effect: { type: "clickPower", value: 3 },
    },
    {
      id: "lemon_pepper_dry",
      emoji: "\u{1F34B}",
      name: "Lemon Pepper (Dry)",
      desc: "A controversial choice. No sauce allowed until room six, so this is the citrus loophole.",
      baseCost: 180,
      effect: { type: "vibeRate", value: 4 },
    },
    {
      id: "impossible_nuggets",
      emoji: "\u{1F966}",
      name: "Impossible Nuggets",
      desc: "Vegan options, of course. KFC used to have these and they were great.",
      baseCost: 200,
      effect: { type: "vibeRate", value: 5 },
    },
    {
      id: "domestic_beer",
      emoji: "\u{1F37A}",
      name: "Domestic Beer",
      desc: "Well drink tickets provided. No drugs at all. Barely water. But beer? Beer's fine. Calms the nerves.",
      baseCost: 250,
      effect: { type: "pulseDampen", value: 1 },
    },
    {
      id: "doordash_window",
      emoji: "\u{1F6D2}",
      name: "DoorDash Window",
      desc: "It's a ghost kitchen. We're not making the best wings in town and only giving them to eight people a night.",
      baseCost: 350,
      effect: { type: "comfyRange", value: 6 },
    },
  ],
  4: [
    {
      id: "subwoofer_stack",
      emoji: "\u{1F50A}",
      name: "Subwoofer Stack",
      desc: "The bass is now a physical force. Your ribcage vibrates. This is correct.",
      baseCost: 400,
      effect: { type: "vibeRate", value: 6 },
    },
    {
      id: "glow_sticks",
      emoji: "\u{1FA84}",
      name: "Glow Sticks",
      desc: "Crack, shake, throw. The universal rave language. Your dance moves hit different when you're trailing light.",
      baseCost: 350,
      effect: { type: "clickPower", value: 5 },
    },
    {
      id: "fog_machine",
      emoji: "\u{1F32B}\u{FE0F}",
      name: "Fog Machine",
      desc: "Can't see the walls. Can't see the ceiling. Can't see the exit. Perfect.",
      baseCost: 500,
      effect: { type: "vibeRate", value: 8 },
    },
    {
      id: "laser_array",
      emoji: "\u{1F4A0}",
      name: "Laser Array",
      desc: "Green, purple, white. Cutting through the fog in geometric patterns. Your consciousness is ascending.",
      baseCost: 600,
      effect: { type: "vibeRate", value: 10 },
    },
    {
      id: "well_drinks",
      emoji: "\u{1F378}",
      name: "Well Drink Tickets",
      desc: "Domestic beer and well drinks provided. No drugs at all. Like really, no drugs at all.",
      baseCost: 450,
      effect: { type: "clickPower", value: 6 },
    },
    {
      id: "bass_throne",
      emoji: "\u{1FA91}",
      name: "Bass Throne",
      desc: "A chair that vibrates at 40Hz. You sit on it between dances and your bones hum. Peak comfort in chaos.",
      baseCost: 700,
      effect: { type: "comfyRange", value: 7 },
    },
  ],
  5: [
    {
      id: "pressure_gauge",
      emoji: "\u{1F4CA}",
      name: "Pressure Gauge",
      desc: "Monitoring the descent. The needle keeps going. This is fine.",
      baseCost: 400,
      effect: { type: "vibeRate", value: 7 },
    },
    {
      id: "dive_helmet",
      emoji: "\u{1FA7C}",
      name: "Dive Helmet",
      desc: "For the rapid descent. Your ears thank you. Your brain does not.",
      baseCost: 500,
      effect: { type: "clickPower", value: 7 },
    },
    {
      id: "ginger_ale",
      emoji: "\u{1F9CB}",
      name: "Ginger Ale",
      desc: "You have a sudden desire for ginger ale. Just like on a plane. Settles your whole situation.",
      baseCost: 300,
      effect: { type: "pulseDampen", value: 1.5 },
    },
    {
      id: "airlock_upgrade",
      emoji: "\u{1F6AA}",
      name: "Airlock Upgrade",
      desc: "The bathroom between four and five, improved. Better seal. Smoother pressurization. No blow-outs.",
      baseCost: 600,
      effect: { type: "comfyRange", value: 8 },
    },
    {
      id: "submarine_porthole",
      emoji: "\u{1F6F8}",
      name: "Submarine Porthole",
      desc: "A window to the deep. Don't open it — if anyone opens a window, everyone gets launched out.",
      baseCost: 750,
      effect: { type: "vibeMultiplier", value: 0.15 },
    },
    {
      id: "ear_plugs",
      emoji: "\u{1F9F7}",
      name: "Pressure Ear Plugs",
      desc: "Not for noise — for equalization. Your eardrums were never designed for this.",
      baseCost: 450,
      effect: { type: "clickPower", value: 8 },
    },
  ],
  6: [
    {
      id: "buffalo_sauce_wings",
      emoji: "\u{1F357}",
      name: "Buffalo Sauce Wings",
      desc: "Finally. SAUCE. The sauce brings you back from the intense barotrauma.",
      baseCost: 800,
      effect: { type: "vibeRate", value: 10 },
    },
    {
      id: "mango_habanero",
      emoji: "\u{1F96D}",
      name: "Mango Habanero",
      desc: "Sweet heat. Your taste buds are so scrambled from the pressure that this tastes like enlightenment.",
      baseCost: 1200,
      effect: { type: "vibeRate", value: 12 },
    },
    {
      id: "garlic_parm_wet",
      emoji: "\u{1F9C4}",
      name: "Garlic Parmesan (Wet)",
      desc: "The sophisticated choice. You've earned this. You survived barometric trauma for this.",
      baseCost: 1000,
      effect: { type: "clickPower", value: 10 },
    },
    {
      id: "honey_bbq",
      emoji: "\u{1F36F}",
      name: "Honey BBQ",
      desc: "Sticky. Messy. Perfect. The wet wings go SO MUCH FASTER for some reason.",
      baseCost: 900,
      effect: { type: "clickPower", value: 8 },
    },
    {
      id: "ghost_kitchen_pass",
      emoji: "\u{1F47B}",
      name: "Ghost Kitchen Pass",
      desc: "DoorDash window, underground. We're not making the best wings in town and only giving them to eight people a night.",
      baseCost: 1500,
      effect: { type: "vibeMultiplier", value: 0.15 },
    },
    {
      id: "decompression_booth",
      emoji: "\u{1F6CB}\u{FE0F}",
      name: "Decompression Booth",
      desc: "A pressurized recovery pod. The sauce alone brings you back, but this helps too.",
      baseCost: 1800,
      effect: { type: "comfyRange", value: 10 },
    },
  ],
  7: [
    {
      id: "trapeze_rig",
      emoji: "\u{1F3AA}",
      name: "Trapeze Rig",
      desc: "Trapezes above. Having some fun. But oh man, you do need the trapezes to get past the traps.",
      baseCost: 1500,
      effect: { type: "vibeRate", value: 12 },
    },
    {
      id: "prism",
      emoji: "\u{1F52E}",
      name: "Prism",
      desc: "If you brought a prism, you can get out of here in a few minutes. Otherwise, gargoyle eye socket. Whole thing.",
      baseCost: 3500,
      effect: { type: "vibeMultiplier", value: 0.2 },
    },
    {
      id: "staind_earplugs",
      emoji: "\u{1F3B5}",
      name: "Staind-Brand Earplugs",
      desc: "Special Staind-brand earplugs to block out Trapt's music. We'll know.",
      baseCost: 2000,
      effect: { type: "clickPower", value: 10 },
    },
    {
      id: "gothic_ringmaster_hat",
      emoji: "\u{1F3A9}",
      name: "Gothic Ringmaster Hat",
      desc: "Now it's feeling like Eyes Wide Shut and that bores the shit out of me. But the hat stays.",
      baseCost: 2500,
      effect: { type: "clickPower", value: 12 },
    },
    {
      id: "latin_phrasebook",
      emoji: "\u{1F4D6}",
      name: "Latin Phrasebook",
      desc: "If you already speak Latin, this room goes faster. If not, start studying. Carpe trappem.",
      baseCost: 3000,
      effect: { type: "vibeRate", value: 15 },
    },
    {
      id: "trap_padding",
      emoji: "\u{1F9E4}",
      name: "Trap Padding",
      desc: "Maybe you're strong. Maybe you just run across the traps and you get a little bit hurt. Less hurt now.",
      baseCost: 2800,
      effect: { type: "comfyRange", value: 10 },
    },
  ],
  8: [
    {
      id: "magnifying_glass",
      emoji: "\u{1F50D}",
      name: "Magnifying Glass",
      desc: "For reading receipts. One of them says 'The Cantainer Store.' That's your golden ticket.",
      baseCost: 2000,
      effect: { type: "vibeRate", value: 14 },
    },
    {
      id: "fake_name_tag",
      emoji: "\u{1F4DB}",
      name: "Fake Name Tag",
      desc: "It says 'ASSOCIATE' and no one questions it. You are also a Container Store employee, sort of legally, for tax reasons.",
      baseCost: 4000,
      effect: { type: "vibeMultiplier", value: 0.2 },
    },
    {
      id: "actor_headshot",
      emoji: "\u{1F4F8}",
      name: "Actor's Headshot",
      desc: "Dropped by one of the actors selling containers to actors. Proof this isn't real.",
      baseCost: 2500,
      effect: { type: "clickPower", value: 12 },
    },
    {
      id: "suspicious_container",
      emoji: "\u{1F4E6}",
      name: "Suspicious Container",
      desc: "What do they ship the containers in? Other containers. It's containers all the way down.",
      baseCost: 3500,
      effect: { type: "clickPower", value: 15 },
    },
    {
      id: "cantainer_receipt",
      emoji: "\u{1F9FE}",
      name: "Cantainer Store Receipt",
      desc: "You found it. One receipt. One till. 'The Cantainer Store.' Boom. You solved it. You're ready.",
      baseCost: 5000,
      effect: { type: "vibeMultiplier", value: 0.2 },
    },
    {
      id: "employee_handbook",
      emoji: "\u{1F4D5}",
      name: "Employee Handbook",
      desc: "The training videos teach you to stay calm. Breathe. Smile. Sell containers. Your pulse steadies.",
      baseCost: 4500,
      effect: { type: "pulseDampen", value: 2 },
    },
  ],
  9: [
    {
      id: "archivist_robes",
      emoji: "\u{1F9D9}",
      name: "Archivist's Robes",
      desc: "They've eschewed raving and devoted themselves to scholarship. You look the part now.",
      baseCost: 3000,
      effect: { type: "vibeRate", value: 20 },
    },
    {
      id: "tunnel_photos",
      emoji: "\u{1F5BC}\u{FE0F}",
      name: "Tunnel Photos",
      desc: "Pictures of your life. Your highest moments. Your greatest times. The long tunnel to room ten.",
      baseCost: 6000,
      effect: { type: "vibeMultiplier", value: 0.25 },
    },
    {
      id: "nirvana_snacks",
      emoji: "\u{1F370}",
      name: "Nirvana Snacks",
      desc: "Third snack checkpoint. These aren't wings. These are transcendent. You've earned this.",
      baseCost: 4000,
      effect: { type: "clickPower", value: 18 },
    },
    {
      id: "montaigne_vinyl",
      emoji: "\u{1F3B6}",
      name: "My Life Is Better With You",
      desc: "A level nine slapper by Montaigne. It will be featured at Plato's Rave. That's a guarantee.",
      baseCost: 8000,
      effect: { type: "vibeMultiplier", value: 0.2 },
    },
    {
      id: "archivist_journal",
      emoji: "\u{1F4D3}",
      name: "Archivist's Journal",
      desc: "If people aren't cataloging the events of the rave, what are we even doing? Important scholarship.",
      baseCost: 5000,
      effect: { type: "clickPower", value: 20 },
    },
    {
      id: "pleasure_garden_bench",
      emoji: "\u{1FAB7}",
      name: "Pleasure Garden Bench",
      desc: "The eternal afterlife pleasure garden. You sit, you breathe, your pulse barely registers the dancing.",
      baseCost: 7000,
      effect: { type: "pulseDampen", value: 2.5 },
    },
  ],
  10: [
    {
      id: "candy_bracelet",
      emoji: "\u{1F4FF}",
      name: "Candy Bracelet",
      desc: "Kandi, in rave parlance. The king's currency. Each one brings you closer to the throne.",
      baseCost: 5000,
      effect: { type: "clickPower", value: 25 },
    },
    {
      id: "fuzzy_boots",
      emoji: "\u{1F97E}",
      name: "Fuzzy Boots",
      desc: "The king wears them. One man, dressed all wild. Fuzzy boots. You need a pair.",
      baseCost: 8000,
      effect: { type: "clickPower", value: 30 },
    },
    {
      id: "spotlight_bulb",
      emoji: "\u{1F4A1}",
      name: "Spotlight Bulb",
      desc: "A single spotlight illuminates you when you walk in. A brighter bulb means a brighter moment.",
      baseCost: 10000,
      effect: { type: "vibeRate", value: 20 },
    },
    {
      id: "franchise_papers",
      emoji: "\u{1F4C4}",
      name: "Franchise Papers",
      desc: "When you make it to room ten, you become a Plato's Rave franchisee. Sign here.",
      baseCost: 15000,
      effect: { type: "vibeMultiplier", value: 0.25 },
    },
    {
      id: "candy_crown",
      emoji: "\u{1F451}",
      name: "Candy Crown of Beads",
      desc: "Just hard candy regalia. The crown sits heavy. You know what it means to wear it.",
      baseCost: 20000,
      effect: { type: "vibeMultiplier", value: 0.3 },
    },
    {
      id: "throne_cushion",
      emoji: "\u{1FA91}",
      name: "Throne Cushion",
      desc: "The king's throne is beautiful but uncomfortable. This helps. You're going to be here a while.",
      baseCost: 12000,
      effect: { type: "comfyRange", value: 20 },
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
    version: 4,
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
      3: { unlocked: false, level: 0 },
      4: { unlocked: false, level: 0 },
      5: { unlocked: false, level: 0 },
      6: { unlocked: false, level: 0 },
      7: { unlocked: false, level: 0 },
      8: { unlocked: false, level: 0 },
      9: { unlocked: false, level: 0 },
      10: { unlocked: false, level: 0 },
    },
    // Per-room inventory: { "1": { "bluetooth_speaker": 2, "premium_bins": 1 }, ... }
    inventory: {},
    loveMult: 1,
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

var saveFailWarned = false;

function saveGame() {
  state.lastSaved = Date.now();
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(state));
    saveFailWarned = false;
  } catch (e) {
    console.warn("Save failed:", e);
    if (!saveFailWarned) {
      saveFailWarned = true;
      showSaveWarning();
    }
  }
}

function showSaveWarning() {
  var el = document.createElement("div");
  el.className = "save-warning";
  el.textContent = "Save failed — progress may be lost if you close this tab";
  document.getElementById("game").appendChild(el);
  setTimeout(function() { el.remove(); }, 8000);
}

function loadGame() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return null;
    const saved = JSON.parse(raw);
    if (saved && saved.version === 4) return saved;
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

// Multiplier from pressure/pulse fitness relative to room's optimal ranges (0.5x–2.0x)
function getRoomFitMultiplier(roomNum) {
  var room = ROOMS[roomNum];
  if (!room) return 1;
  var pRange = getEffectiveOptimalRange(roomNum, "pressure");
  var sRange = getEffectiveOptimalRange(roomNum, "pulse");
  var pFit = statFitness(state.pressure, pRange);
  var sFit = statFitness(state.pulse, sRange);
  var fit = (pFit + sFit) / 2;
  return PENALTY_FLOOR + fit * (OPTIMAL_BONUS - PENALTY_FLOOR);
}

// Total room multiplier: stat fitness * vibeMultiplier item bonuses * love (room 10 only)
function getRoomMultiplier(roomNum) {
  var mult = getRoomFitMultiplier(roomNum) * (1 + getItemBonus(roomNum, "vibeMultiplier"));
  if (roomNum === 10) mult *= (state.loveMult || 1);
  return mult;
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

// Kandi prestige bonus: +10% global VPS per kandi
function getKandiMultiplier() {
  return 1 + (state.kandi || 0) * 0.1;
}

function getCurrentVibeRate() {
  var room = ROOMS[state.currentRoom];
  if (!room) return 0;
  var rs = state.rooms[state.currentRoom];
  var level = (rs && rs.level) ? rs.level : 1;
  var base = room.baseVibeRate * level;
  var itemBonus = getItemBonus(state.currentRoom, "vibeRate");
  return (base + itemBonus) * getRoomMultiplier(state.currentRoom) * getKandiMultiplier();
}

function getVibeRateForRoom(roomNum) {
  var room = ROOMS[roomNum];
  if (!room) return 0;
  var rs = state.rooms[roomNum];
  if (!rs || !rs.unlocked) return 0;
  var level = rs.level || 1;
  var base = room.baseVibeRate * level;
  var itemBonus = getItemBonus(roomNum, "vibeRate");
  return (base + itemBonus) * getRoomMultiplier(roomNum) * getKandiMultiplier();
}

function getClickValue() {
  var room = ROOMS[state.currentRoom];
  if (!room) return BASE_CLICK_VIBE;
  var mult = getRoomMultiplier(state.currentRoom);
  var itemBonus = getItemBonus(state.currentRoom, "clickPower");
  return Math.max(1, Math.floor((BASE_CLICK_VIBE * room.clickMultiplier + itemBonus) * mult * getKandiMultiplier()));
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
  if (n === Infinity) return "\u221E";
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
  breakdownBase: document.getElementById("breakdown-base"),
  breakdownItems: document.getElementById("breakdown-items"),
  breakdownMult: document.getElementById("breakdown-mult"),
  breakdownClick: document.getElementById("breakdown-click"),
  breakdownPressure: document.getElementById("breakdown-pressure"),
  navLeftVps: document.getElementById("nav-left-vps"),
  navRightVps: document.getElementById("nav-right-vps"),
  kandiDisplay: document.getElementById("kandi-display"),
};

// ============================================================
// Rendering
// ============================================================

function renderStats() {
  dom.vibeCount.textContent = formatNumber(state.vibe);
  dom.vibePerSec.textContent = formatNumber(getCurrentVibeRate());

  // Kandi display
  if (state.kandi > 0) {
    dom.kandiDisplay.classList.remove("hidden");
    dom.kandiDisplay.textContent = "\u{1F4FF} " + state.kandi + " Kandi (" + getKandiMultiplier().toFixed(1) + "x)";
  } else {
    dom.kandiDisplay.classList.add("hidden");
  }

  var p = clamp(state.pressure, 0, 100);
  var s = clamp(state.pulse, 0, 100);
  dom.pressureFill.style.width = p + "%";
  dom.pulseFill.style.width = s + "%";
  dom.pressureValue.textContent = Math.floor(p);
  dom.pulseValue.textContent = Math.floor(s);

  // Rate breakdown
  var room = ROOMS[state.currentRoom];
  if (room) {
    var rs = state.rooms[state.currentRoom];
    var level = (rs && rs.level) ? rs.level : 1;
    var base = room.baseVibeRate * level;
    var itemBonus = getItemBonus(state.currentRoom, "vibeRate");
    var fitMult = getRoomFitMultiplier(state.currentRoom);
    var itemMult = 1 + getItemBonus(state.currentRoom, "vibeMultiplier");
    var loveMult = (state.currentRoom === 10) ? (state.loveMult || 1) : 1;
    var totalMult = fitMult * itemMult * loveMult * getKandiMultiplier();
    dom.breakdownBase.textContent = formatNumber(base) + "/s";
    dom.breakdownItems.textContent = "+" + formatNumber(itemBonus) + "/s";
    var multText = isFinite(totalMult) ? totalMult.toFixed(1) + "x" : "\u221Ex";
    dom.breakdownMult.textContent = multText;
    dom.breakdownMult.className = totalMult >= 1 ? "bonus" : "penalty";
    dom.breakdownClick.textContent = formatNumber(getClickValue()) + "/tap";
    var pe = room.pressureEffect;
    var pressureText = pe < 0 ? "Calming" : pe === 0 ? "Neutral" : "Intense";
    if (Math.abs(pe) >= 3) pressureText = pe < 0 ? "Very Calming" : "Very Intense";
    dom.breakdownPressure.textContent = pressureText;
  }

  // Spread the love: enabled when 10% of vibes rounds to at least 1
  dom.spreadLoveBtn.disabled = Math.floor(state.vibe * 0.1) < 1;
  if (state.currentRoom === 10) {
    dom.spreadLoveBtn.textContent = "Spread the Love (" + formatNumber(state.loveMult || 1) + "x)";
  } else {
    dom.spreadLoveBtn.textContent = "Spread the Love";
  }
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


// Returns arrow indicating whether otherVps is higher/lower/equal vs currentVps
function vpsArrow(otherVps, currentVps) {
  if (otherVps > currentVps) return "\u25B2";   // ▲ higher vps
  if (otherVps < currentVps) return "\u25BC";   // ▼ lower vps
  return "\u2014";                              // — same
}

function renderNav() {
  var prevRoom = state.currentRoom - 1;
  dom.navLeft.disabled = prevRoom < 1 || !state.rooms[prevRoom] || !state.rooms[prevRoom].unlocked;

  var nextRoom = state.currentRoom + 1;
  var nextExists = !!ROOMS[nextRoom];
  var nextUnlocked = state.rooms[nextRoom] && state.rooms[nextRoom].unlocked;

  dom.navRight.disabled = !nextUnlocked;

  // VPS preview on nav buttons
  var currentVps = getVibeRateForRoom(state.currentRoom);

  if (!dom.navLeft.disabled && ROOMS[prevRoom]) {
    var prevVps = getVibeRateForRoom(prevRoom);
    dom.navLeftVps.textContent = formatNumber(prevVps) + "/s " + vpsArrow(prevVps, currentVps);
  } else {
    dom.navLeftVps.textContent = "";
  }

  if (!dom.navRight.disabled && ROOMS[nextRoom]) {
    var nextVps = getVibeRateForRoom(nextRoom);
    dom.navRightVps.textContent = formatNumber(nextVps) + "/s " + vpsArrow(nextVps, currentVps);
  } else {
    dom.navRightVps.textContent = "";
  }

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

    var roomNum = state.currentRoom;
    var spritePath = "assets/sprites/npcs/room" + roomNum + "/";
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
    head.style.backgroundImage = "url(" + spritePath + "head.png)";

    // Body
    var body = document.createElement("div");
    body.className = "npc-body";
    body.style.backgroundImage = "url(" + spritePath + "torso.png)";

    // Legs
    var legs = document.createElement("div");
    legs.className = "npc-legs";
    legs.style.backgroundImage = "url(" + spritePath + "legs.png)";

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

  // Random position across the room, shift anchor to avoid right-edge cutoff
  var xPos = 5 + Math.random() * 90;
  var yPos = 20 + Math.random() * 60;
  el.style.left = xPos + "%";
  el.style.top = yPos + "%";
  el.style.setProperty("--x-shift", "-" + Math.round(xPos) + "%");

  container.appendChild(el);
  el.addEventListener("animationend", function() { el.remove(); });

  // Schedule next — kandi speeds up ambient flavor
  var kandiSpeed = 1 / (1 + (state.kandi || 0) * 0.15);
  var nextDelay = (AMBIENT_INTERVAL_MIN +
    Math.random() * (AMBIENT_INTERVAL_MAX - AMBIENT_INTERVAL_MIN)) * kandiSpeed;
  ambientTimer = setTimeout(spawnAmbientText, nextDelay);
}

function startAmbient() {
  if (ambientTimer) clearTimeout(ambientTimer);
  var kandiSpeed = 1 / (1 + (state.kandi || 0) * 0.15);
  var delay = (AMBIENT_INTERVAL_MIN +
    Math.random() * (AMBIENT_INTERVAL_MAX - AMBIENT_INTERVAL_MIN)) * kandiSpeed;
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

var activePopupCost = null;

function showItemPopup(data) {
  var overlay = document.getElementById("item-popup");
  var owned = 0;
  if (state.inventory[data.roomNum]) {
    owned = state.inventory[data.roomNum][data.item.id] || 0;
  }
  var cost = data.cost;
  activePopupCost = cost;
  var effectDesc = "";
  if (data.item.effect.type === "vibeRate") {
    effectDesc = "+" + data.item.effect.value + " Vibe/s in this room";
  } else if (data.item.effect.type === "vibeMultiplier") {
    effectDesc = "+" + Math.round(data.item.effect.value * 100) + "% Vibe multiplier in this room";
  } else if (data.item.effect.type === "pulseDampen") {
    effectDesc = "-" + data.item.effect.value + " pulse per tap in this room";
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
    activePopupCost = null;
    overlay.classList.add("hidden");
    renderStats();
    renderOptimalRanges();
  
    renderNav();
    renderInventory();
  };

  document.getElementById("item-popup-dismiss").onclick = function() {
    activePopupCost = null;
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
  } else if (item.effect.type === "vibeMultiplier") {
    effectDesc = "+" + Math.round(total * 100) + "% Vibe multiplier (" + Math.round(item.effect.value * 100) + "% each)";
  } else if (item.effect.type === "pulseDampen") {
    effectDesc = "-" + total + " pulse per tap (" + item.effect.value + " each)";
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
  activePopupCost = null;
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
  var pulseDampen = getItemBonus(state.currentRoom, "pulseDampen");
  state.pulse = clamp(state.pulse + Math.max(0, PULSE_PER_CLICK - pulseDampen), 0, 100);

  var clientX = e.clientX;
  var clientY = e.clientY;
  spawnClickPop(value, clientX, clientY);
  triggerDanceAnimation();

  renderStats();

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

  if (state.currentRoom === 10) {
    // In the throne room, love amplifies your vibe — squaring each time
    if (!state.loveMult || state.loveMult <= 1) {
      state.loveMult = 2;
    } else {
      state.loveMult = state.loveMult * state.loveMult;
    }
    renderStats();
    renderNav();
    // Check for transcendence — when love overwhelms all finite measurement
    if (!isFinite(state.loveMult)) {
      triggerTranscendence();
    }
  } else {
    state.pressure = clamp(state.pressure * 0.9, 0, 100);
    renderStats();
    renderNav();
  }
}

function triggerTranscendence() {
  var overlay = document.getElementById("transcendence");
  var emoji = document.getElementById("transcendence-emoji");
  var title = document.getElementById("transcendence-title");
  var message = document.getElementById("transcendence-message");
  var stats = document.getElementById("transcendence-stats");
  var btn = document.getElementById("transcendence-dismiss");

  emoji.textContent = "\u{1F451}";
  title.textContent = "The Candy King Disintegrates";
  message.textContent = "He looks down at you. The spotlight trembles. " +
    "Your love is infinite. His candy crown crumbles to dust. " +
    "You are the Candy King now. You are a Plato's Rave franchisee.";
  var nextKandi = (state.kandi || 0) + 1;
  var nextMult = 1 + nextKandi * 0.1;
  var freeRooms = Math.min(nextKandi + 1, 10);
  stats.textContent = "+1 Kandi \u2022 " + nextMult.toFixed(1) + "x global multiplier \u2022 " +
    freeRooms + " rooms unlocked \u2022 faster pulse decay \u2022 more flavor";
  btn.textContent = "Enter Room 11";
  overlay.classList.remove("hidden");

  btn.onclick = function() {
    overlay.classList.add("hidden");
    performPrestige();
  };
}

function performPrestige() {
  state.prestigeCount++;
  state.kandi += 1;
  // Reset everything except prestige/kandi/all-time stats
  var keepPrestige = state.prestigeCount;
  var keepKandi = state.kandi;
  var keepAllTime = state.stats.totalVibeAllTime;
  state = createDefaultState();
  state.prestigeCount = keepPrestige;
  state.kandi = keepKandi;
  state.stats.totalVibeAllTime = keepAllTime;
  // Kandi unlocks rooms: you remember the way
  var freeRooms = Math.min(keepKandi + 1, 10);
  for (var r = 2; r <= freeRooms; r++) {
    state.rooms[r] = { unlocked: true, level: 1 };
  }
  vibeSnapshots = [];
  saveGame();
  renderAll();
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

// Rolling real VPS tracker (measures actual vibe income over a window)
var REAL_VPS_WINDOW = 15; // seconds
var vibeSnapshots = []; // { time, earned }
var realVpsEl = document.getElementById("real-vps-value");

function updateRealVps(now) {
  vibeSnapshots.push({ time: now, earned: state.totalVibeEarned });
  var cutoff = now - REAL_VPS_WINDOW * 1000;
  while (vibeSnapshots.length > 1 && vibeSnapshots[0].time < cutoff) {
    vibeSnapshots.shift();
  }
  if (vibeSnapshots.length < 2) {
    realVpsEl.textContent = "0";
    return;
  }
  var first = vibeSnapshots[0];
  var last = vibeSnapshots[vibeSnapshots.length - 1];
  var elapsed = (last.time - first.time) / 1000;
  if (elapsed < 1) {
    realVpsEl.textContent = "0";
    return;
  }
  var realVps = (last.earned - first.earned) / elapsed;
  realVpsEl.textContent = formatNumber(Math.max(0, realVps));
}

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
    var pulseDecay = PULSE_DECAY_RATE * (1 + (state.kandi || 0) * 0.2);
    state.pulse = clamp(state.pulse - pulseDecay * dt, 0, 100);
  }

  renderStats();
  updateRealVps(now);

  renderNav();

  // Update buy button if item popup is open
  if (activePopupCost !== null) {
    var buyBtn = document.getElementById("item-popup-buy");
    if (buyBtn && buyBtn.style.display !== "none") {
      buyBtn.disabled = state.vibe < activePopupCost;
    }
  }

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
