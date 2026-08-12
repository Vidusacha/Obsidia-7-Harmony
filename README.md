# Obsidia-7 Harmony ⚙️⚡

> A 3D thermodynamic mechanical evolution simulator set in a riveting-punk junkyard universe.

[![Repository](https://img.shields.io/badge/GitHub-Vidusacha%2FObsidia--7--Harmony-gold)](https://github.com/Vidusacha/Obsidia-7-Harmony)

---

## 📜 Documentation Sitemap

- [**`concept.md`**](concept.md): General strategy, narrative lore (Helios-Omega, Junkyard, Inventors), and core pillars.
- [**`design.md`**](design.md): "Riveting-Punk" visual aesthetics, PBR materials, 14-face truncated octahedron specs, and UI gauges.
- [**`gameplay.md`**](gameplay.md): Laws of physics, Kirchhoff graph solver ($L \cdot V = I$), Joule heating ($I^2 R$), gas reactivity, and survival rules.
- [**`development_plan.md`**](development_plan.md): Milestone progress checklist and current status.
- [**`audit.md`**](audit.md): Architectural Decision Records (ADRs) and context distillation log.
- [**`architecture.md`**](architecture.md): Technical subsystem breakdown, BCC lattice math, and local Ollama API integration.

---

## 🧪 Interactive Visualizer Demos

We have prepared 3 distinct technology stack demos to evaluate engine candidates:

### Demo 1: Web 3D Stack (Three.js / WebGL / PBR & Gauges)
- **Path**: [`demos/demo1_web_threejs/index.html`](demos/demo1_web_threejs/index.html)
- **Features**: Interactive 3D truncated octahedron with polished brass & weathered copper PBR materials, glowing vacuum filaments, live Kirchhoff voltage node animation, and brass analog HUD gauges.
- **Launch**: Open `demos/demo1_web_threejs/index.html` in any modern web browser or serve locally.

### Demo 2: Python Native Stack (3D BCC Lattice & Kirchhoff Matrix Solver)
- **Path**: [`demos/demo2_python_native/demo_py.py`](demos/demo2_python_native/demo_py.py)
- **Features**: Interactive 3D multi-block creature graph rendered on BCC spatial lattice, real-time Kirchhoff matrix solver visualizer, and thermal Joule heating color gradient.
- **Launch**: Run `python demos/demo2_python_native/demo_py.py` in terminal.

### Demo 3: Headless Core + Local Ollama Generative Evolution Showcase
- **Path**: [`demos/demo3_ollama_headless/demo_ollama.py`](demos/demo3_ollama_headless/demo_ollama.py)
- **Features**: Headless simulation cycle running $n=m$ thermodynamic growth & decay, communicating with local Ollama (`http://localhost:11434`) to generate procedural creature blueprints and species evolutionary lore.
- **Launch**: Run `python demos/demo3_ollama_headless/demo_ollama.py` in terminal.

---

## 🛠️ Automated Repository Rules
This repository enforces automated pre-push documentation updates via `.agents/rules/git_documentation_update.md`.
