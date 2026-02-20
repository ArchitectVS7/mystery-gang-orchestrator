# Mystery Gang Orchestrator

**Transform boring agent orchestration into an entertaining cartoon adventure!**

🎭 Character-driven AI agents • 6 fun themes • Real-time group chat • Translation toggle

---

## 🎯 What Is This?

Instead of seeing raw technical output like:
```
Created API endpoint
Fixed null pointer exception
Deployed to production
```

You get cartoon-style team communication like:
```
🚨 [ALARM SOUNDS]

FRED: Alright gang, let's tackle this systematically!
VELMA: Jinkies! I found the solution in the docs!
  🔧 Neutralized the spectral null anomaly
DAPHNE: Safety first, gang!
  🔧 Added extra safety nets for when things go wrong
SCOOBY: Scooby-Dooby-Doo! All tests passing!
  Fred: 🎉
  Velma: 🎉
  Daphne: 🎉

✅ MYSTERY SOLVED!
```

---

## ✨ Features

✅ **5 Unique Characters** - Fred (Architect), Velma (Specialist), Daphne (QA), Shaggy (DevRel), Scooby (Bug Hunter)  
✅ **6 Themes** - Scooby-Doo, Star Trek, Ghostbusters, Superhero, Pirates, Wizards  
✅ **Dynamic Team Selection** - Different tasks = different team compositions  
✅ **Technobabble Translation** - Technical output → Cartoon lingo  
✅ **Translation Toggle** - Switch between cartoon/raw/both modes anytime  
✅ **Real-time Group Chat** - Live emoji reactions and character dialogue  
✅ **78 Tests** - 100% passing, full TDD coverage  

---

## 🚀 Quick Start

### Run the Group Chat Demo

```bash
# Default (Scooby theme)
python3 demo/group_chat_demo.py

# Try different themes
python3 demo/group_chat_demo.py --theme star_trek
python3 demo/group_chat_demo.py --theme ghostbusters
python3 demo/group_chat_demo.py --theme pirates
python3 demo/group_chat_demo.py --theme wizards

# Toggle translation modes
python3 demo/group_chat_demo.py --raw        # Technical output only
python3 demo/group_chat_demo.py --both       # Show both translated + raw

# Custom task
python3 demo/group_chat_demo.py --task "Fix critical bug in payment system"
```

### Run Tests

```bash
python3 -m pytest tests/ -v

# Test specific modules
python3 -m pytest tests/test_character.py -v       # 25 tests
python3 -m pytest tests/test_assembly.py -v        # 23 tests
python3 -m pytest tests/test_technobabble.py -v    # 30 tests
```

---

## 🎭 The 6 Themes

### 1. 🐕 Scooby-Doo Mystery Gang
- **Team:** Mystery Inc.
- **Vehicle:** The Mystery Machine
- **Victory:** "Scooby-Dooby-Doo!"
- **Example:** "Neutralized the spectral null anomaly"

### 2. 🚀 Star Trek
- **Team:** USS Enterprise Crew
- **Vehicle:** USS Enterprise
- **Victory:** "Engage!"
- **Example:** "Reconfigured the reverse flux decoupling system"

### 3. 👻 Ghostbusters
- **Team:** Ghostbusters
- **Vehicle:** Ecto-1
- **Victory:** "We came, we saw, we kicked it!"
- **Example:** "Contained the negative energy entity"

### 4. 🦸 Superhero Team
- **Team:** The Avengers
- **Vehicle:** Quinjet
- **Victory:** "Avengers, assemble!"
- **Example:** "Stabilized the quantum vulnerability field"

### 5. 🏴‍☠️ Pirate Crew
- **Team:** The Black Pearl Crew
- **Vehicle:** The Black Pearl
- **Victory:** "The treasure is ours, arrr!"
- **Example:** "Plugged the leak in me hull, arrr!"

### 6. 🧙 Wizard Academy
- **Team:** The Order
- **Vehicle:** Flying Carriage
- **Victory:** "The magic flows strong!"
- **Example:** "Banished the void spirit from the code"

---

## 📂 Project Structure

```
mystery-gang-orchestrator/
├── src/
│   ├── character.py          # Character engine (dialogue, personalities)
│   ├── assembly.py            # Task analysis, team selection
│   └── technobabble.py        # Translation engine with theme support
├── data/
│   └── characters.json        # Character definitions (5 characters, 10+ catchphrases each)
├── tests/
│   ├── test_character.py      # 25 tests
│   ├── test_assembly.py       # 23 tests
│   └── test_technobabble.py   # 30 tests
├── demo/
│   └── group_chat_demo.py     # Real-time group chat simulator
├── docs/
│   ├── PRD-mystery-gang-orchestrator.md    # Complete product spec
│   └── future-animation-plans.md           # Animation roadmap
└── README.md
```

---

## 🧪 Test Coverage

**Total: 78/78 tests passing (100%)**

### Character System (25 tests)
- Character definitions with required fields
- Model assignments (Fred → Claude, Velma → Qwen, etc.)
- Dialogue generation with personality
- Catchphrase variety and context-awareness
- CharacterEngine functionality

### Team Assembly (23 tests)
- Task type analysis (7 types: backend, frontend, debugging, etc.)
- Dynamic team selection based on task
- Assembly scene generation
- Context-aware character responses

### Technobabble Translation (30 tests)
- Dictionary with 84+ mappings (14 phrases × 6 themes)
- Theme support for all 6 themes
- Translation toggle (raw/both/translated modes)
- Integration workflows

---

## 🎮 How It Works

### 1. Task Analysis
```python
task = "Create REST API with authentication"
analysis = analyzer.analyze(task)
# → Type: backend, Keywords: [api, rest, auth], Confidence: 60%
```

### 2. Team Assembly
```python
team = selector.select(task)
# → ["fred", "velma", "daphne", "shaggy", "scooby"]
# Backend tasks prioritize Velma (specialist)
```

### 3. Assembly Scene
```
🚨 [ALARM SOUNDS]

FRED: Alright gang, let's tackle this systematically!
VELMA: Jinkies! Let me analyze the requirements...
DAPHNE: Safety first, gang!
SHAGGY: Like, let's get this over with...
SCOOBY: Rello! Ready to find some rugs!

🚐 THE MYSTERY MACHINE IS EN ROUTE!
```

### 4. Work Session with Translation
```python
# Technical output
technical = "Fixed null pointer exception"

# Translated (Scooby theme)
translated = translator.translate(technical)
# → "Neutralized the spectral null anomaly"

# Star Trek theme
translator.set_theme(Theme.STAR_TREK)
translated = translator.translate(technical)
# → "Reconfigured the reverse flux decoupling system"
```

### 5. Victory Celebration
```
✅ MISSION COMPLETE!
Scooby-Dooby-Doo!

📦 DELIVERABLES:
✓ resonance chamber calibrated
✓ security protocols engaged
✓ all traps sprung successfully
✓ spectral anomaly neutralized
```

---

## 🔧 Translation Toggle

**Three modes:**

### Default: Translated Only
```python
translate("Created API endpoint")
# → "Calibrated the mystery detection chamber"
```

### Raw: Technical Only
```python
translate("Created API endpoint", mode="raw")
# → "Created API endpoint"
```

### Both: Side-by-Side
```python
translate("Created API endpoint", mode="both")
# → "Calibrated the mystery detection chamber"
#
# [Technical]
# Created API endpoint
```

**Can toggle anytime mid-session!**

---

## 🛠️ Technology Stack

- **Python 3.8+**
- **pytest** for testing
- **dataclasses** for structured data
- **Enums** for type safety
- **Character definitions:** JSON
- **CLI demo:** Standard library (no external dependencies for core)

---

## 📊 Development Stats

- **Lines of Code:** ~62KB
- **Tests:** 78 (100% passing)
- **Characters:** 5 (each with 10+ unique catchphrases)
- **Themes:** 6 (fully implemented)
- **Translation Mappings:** 84+ (14 phrases × 6 themes)
- **Development Time:** ~6 hours (Phases 1-3 + demo)

---

## 🎯 Roadmap

### Phase 1: Character System ✅
- Character definitions
- Dialogue generation
- Personality injection

### Phase 2: Team Assembly ✅
- Task type analysis
- Dynamic team selection
- Assembly scene generation

### Phase 3: Technobabble Translator ✅
- 6 theme support
- Translation toggle
- Technobabble dictionary

### Phase 3.5: Group Chat Demo ✅
- Real-time chat simulation
- Emoji reactions
- Live translation
- All themes working

### Phase 4: Canvas Visualization 🚧
- Static character sprites
- Clubhouse view
- Mission progress display
- Victory celebration

### Phase 5: Mission Control 📋
- Queue management
- Status tracking
- Summary generation

### Phase 6: OpenClaw Integration 📋
- Agent spawn hook
- Model routing
- Output formatting

---

## 🎨 Future Plans

See `docs/future-animation-plans.md` for detailed animation roadmap:

- **Phase 4:** Static Canvas visualization (6-8 hours)
- **Phase 5:** Basic animations (8-10 hours)
- **Phase 6:** 3D/WebGL (40+ hours, aspirational)

---

## 🤝 Contributing

This is a **proof-of-concept** demonstrating character-driven agent orchestration.

Contributions welcome! Areas for expansion:
- Additional themes (Cowboy, Ninja, Cyberpunk, etc.)
- More character catchphrases
- Additional technical → cartoon mappings
- Theme-specific visual styles
- Sound effects
- Voice acting (TTS integration)

---

## 📄 License

MIT License

---

## 🎉 Credits

**Concept:** VS7  
**Implementation:** LG2 (OpenClaw agent)  
**Inspired by:** Scooby-Doo, Star Trek, Ghostbusters, and the joy of making technical work fun

---

## 💡 Philosophy

> "Why should agent orchestration be boring? Code reviews don't have to read like autopsy reports. Let's make software development feel like a Saturday morning cartoon!"

**Not a game. Not just visualization. A fundamentally different way to experience agent collaboration.**

---

**Ready to solve some mysteries?** 🐕🔍

Try the demo: `python3 demo/group_chat_demo.py`
