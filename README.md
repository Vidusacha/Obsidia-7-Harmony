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

## ⚡ Native 3D GPU Engine Demos (144+ FPS Desktop Windows)

We have built 2 high-performance native desktop GPU engine demos to compare against web browser rendering:

### 🟢 Native Demo A: ModernGL OpenGL 3.3 GPU Engine (144+ FPS)
- **Path**: [`demos/native_demo_moderngl/run_moderngl_demo.py`](demos/native_demo_moderngl/run_moderngl_demo.py)
- **Features**: Direct GPU hardware rendering via ModernGL & GLSL PBR shaders (Golden Brass & Copper Patina specular highlights), orbiting 3D camera, zero network latency.
- **Launch**: Run `python demos/native_demo_moderngl/run_moderngl_demo.py` in terminal.

### 🟢 Native Demo B: Pygame 3D Particle Engine (120+ FPS)
- **Path**: [`demos/native_demo_pygame3d/run_pygame3d_demo.py`](demos/native_demo_pygame3d/run_pygame3d_demo.py)
- **Features**: Autonomous evolution of 4 distinct species (Brass, Copper, Steel, Bronze), Out-G thrust bubble particles, live FPS counter, HUD telemetry overlay.
- **Launch**: Run `python demos/native_demo_pygame3d/run_pygame3d_demo.py` in terminal.

---

## 🛠️ Automated Repository Rules
This repository enforces automated pre-push documentation updates via `.agents/rules/git_documentation_update.md`.
