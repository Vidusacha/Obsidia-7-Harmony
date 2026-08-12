# Obsidia-7 Harmony — Audit Log & Context Distillation

## Architectural Decision Records (ADRs)

### ADR-001: BCC Lattice Discrete Geometry for 14-Face Truncated Octahedra
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Truncated octahedra have 14 faces (8 hexagons, 6 squares). Continuous 3D rigid body constraints lead to floating-point drift and heavy physics solver overhead.
- **Decision**: Docking positions map to Body-Centered Cubic (BCC) spatial grid with discrete quaternions for 14 face normals.

### ADR-002: Kirchhoff Electrical Network Solver ($L \cdot V = I$)
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Simple graph distance (Dijkstra) ignores parallel electrical paths across multiple intake nodes.
- **Decision**: Model electrical conduction as Kirchhoff Laplacian circuit ($L \cdot V = I$), calculating node voltages and $I^2 R$ Joule heating. Overloaded edges visually glow orange-red.

### ADR-003: Decoupled Headless Simulation Core
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Need high-speed evolutionary simulation without rendering overhead.
- **Decision**: Decouple core engine (`ObsidiaEngine`) into pure Python data model that can run headless for fast evolution or connect to 3D visualizers.

### ADR-004: Local Ollama LLM Integration (`http://localhost:11434`)
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: User requested using local Ollama anytime to save API tokens and generate evolutionary content.
- **Decision**: Use local Ollama (`qwen:latest`) for offline YAML configuration synthesis, procedural creature blueprint generation, and species evolutionary journal generation.

### ADR-005: Visualizer Engine Stack Selection — Web3D (Three.js / WebGL)
- **Date**: 2026-08-12
- **Status**: Replaced by Native Engine (ADR-008)
- **Context**: Web browser HTTP polling produced 10 FPS lag.

### ADR-006: Concept Shift — Autonomous Ecosystem Spectator Mode (God Mode / Digital Aquarium)
- **Date**: 2026-08-12
- **Status**: Approved by EV
- **Context**: Shifted from manual player steering to a pure autonomous evolution simulator where 2 (and 4) distinct species interact, hunt, symbiose, and evolve automatically.
- **Decision**: Implemented 4 distinct species visual identities (Brass, Copper, Steel, Bronze), autonomous navigation, predation mechanics, tracking camera, and God Overseer controls.

### ADR-007: Native Desktop GPU Engine Candidates (144+ FPS)
- **Date**: 2026-08-12
- **Status**: Completed
- **Context**: EV requested high-speed native 3D rendering without browser/HTTP latency. Built Native Demo A (ModernGL) and Native Demo B (Pygame 3D).

### ADR-008: Master Engine Selection — Native Pygame 3D Desktop Engine (120+ FPS)
- **Date**: 2026-08-12
- **Status**: Approved by EV
- **Context**: EV evaluated native demos side-by-side and selected Pygame 3D for the master desktop application (`src/engine_native_3d.py`).
- **Decision**: Formally adopted **Native Pygame 3D Desktop Engine** as the official primary application launcher. Renders 4 species, 3D particle systems, analog HUD gauges, tracking camera, and local Ollama REST bridge at 120+ FPS directly on Windows.

---

## User Requests & Context Notes
- **User**: EV (male), GitHub user `Vidusacha`. Repository: `https://github.com/Vidusacha/Obsidia-7-Harmony`.
- **Language Policy**: Russian for explanatory discussions, English for code, comments, and file names.
- **Automated Maintenance**: Enforced via `.agents/rules/git_documentation_update.md` before all git pushes.
