# Obsidia-7 Harmony — Development Plan & Progress Tracking

## Development Milestones Checklist

### Milestone 1: Foundations & Architecture Setup
- [x] Consolidate system prompt, lore, and visual design requirements.
- [x] Create project documentation ecosystem (`concept.md`, `design.md`, `gameplay.md`, `development_plan.md`, `audit.md`, `architecture.md`, `README.md`).
- [x] Create `.agents/rules/git_documentation_update.md` agent rule for git pre-push doc updates.
- [x] Implement 3 technology stack visualizer/engine demos (`demos/demo1_web_threejs`, `demos/demo2_python_native`, `demos/demo3_ollama_headless`).
- [x] Evaluate demo options with EV: Selected **Web3D (Three.js)** for renderer & **Local Ollama + Headless Python Engine** for core simulation.

### Milestone 2: Core Headless Simulation Engine (`ObsidiaEngine`) & Web Integration
- [ ] Implement pure Python/C++ BCC spatial lattice grid system for 14-face truncated octahedra.
- [ ] Implement Kirchhoff Conductive Graph solver ($L \cdot V = I$) with $I^2 R$ Joule heating calculations.
- [ ] Implement Gas Intake & Exhaust chemical reaction formulas (G-- to G++ scale).
- [ ] Implement thermodynamic $n=m$ synthesis/decay kinetics and thermal entropy dissipation.
- [ ] Build WebSocket / HTTP bridge between Python Headless Core and Web3D Three.js frontend.
- [ ] Implement JSON/YAML external configuration loader for all physics constants.

### Milestone 3: Organism Genetics, Mutation & Local Ollama Bridge
- [ ] Implement Body Graph serialization format (JSON/YAML blueprint schema).
- [ ] Implement mutation engine (10% block addition, block specialization swap, Turbo-Exhaust mutation).
- [ ] Implement REST API connector to local Ollama (`qwen:latest` / `qwen3.5-abliterated`) for generative species lore and AI evolutionary decisions.

### Milestone 4: 3D Web Renderer Polish & Analog HUD
- [ ] Implement Riveting-Punk PBR shaders in Three.js (polished brass, weathered copper patina, oil ocean reflections).
- [ ] Build interactive analog UI HUD (gauges with trembling needles for Charge and Pressure, schematic node diagnostic view).
- [ ] Add 14-face docking port mesh details and glowing filament wireframes to module geometry.

### Milestone 5: Ecosystem Simulation & Multi-Agent Evolution
- [ ] Implement multi-organism world simulation with oil currents and volumetric gas clouds.
- [ ] Implement organism interaction mechanics (predation collision, parasitic docking, symbiotic sharing).
- [ ] Implement Supernova Doom Clock meta-progression (3M-year countdown, planetary shield / space travel achievement goals).

---

## Current Status
- **Current Phase**: Milestone 1 COMPLETE | Milestone 2 IN PROGRESS.
- **Decision**: Web3D (Three.js) selected for frontend; Python + Local Ollama selected for backend engine.
