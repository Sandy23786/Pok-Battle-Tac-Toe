# ⚡ PokéBattle Tac-Toe

A futuristic Pokémon-themed Tic-Tac-Toe powered by **Pollinations AI** — neon cyberpunk aesthetics, glassmorphism UI, and live AI commentary.

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Flask (`pip install flask`)

### Run
```bash
python app.py
```
Then open → **http://localhost:5000**

---

## 🎮 Features

- **VS AI** — Easy / Medium / Hard (Minimax + Pollinations AI commentary)
- **Local 2-Player** — Pass-and-play on one device
- **6 Pokémon matchups** — Pikachu, Charmander, Mewtwo, and more
- **Live AI narrator** — Pollinations AI generates battle commentary
- **Animated board** — Pop-in effects, glow pulses, win flash
- **Confetti celebration** — Particle burst on every win
- **Fully responsive** — Desktop, tablet, and mobile

---

## 🧠 Pollinations AI

Used via free public API (`https://text.pollinations.ai/`) — no API key needed.

Generates:
- Pokémon-flavored match commentary
- Battle narration after each move

Falls back to built-in commentary if unreachable.

---

## 📁 Structure

```
pokemon-tictactoe/
├── app.py              # Flask backend + AI logic
├── templates/
│   └── index.html      # Full frontend (HTML/CSS/JS)
└── README.md
```

---

## 🎨 Design

- **Theme**: Dark Cyberpunk / Neon Glassmorphism
- **Fonts**: Orbitron (headers) + Rajdhani (body)
- **Colors**: Neon Blue `#00d4ff`, Neon Purple `#b44fff`, Electric Cyan `#00ffee`
- **Sprites**: PokéAPI official pixel art sprites
