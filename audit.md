# Obsidia-7 Harmony — Audit Log & Context Distillation

## Architectural Decision Records (ADRs)

### ADR-001: BCC Lattice Discrete Geometry for 14-Face Truncated Octahedra
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Truncated octahedra have 14 faces (8 hexagons, 6 squares). Continuous 3D rigid body constraints lead to floating-point drift and heavy physics solver overhead.
- **Decision**: Docking positions will map to a Body-Centered Cubic (BCC) spatial grid with discrete quaternions for the 14 face normals. 3D physics engines will handle macro collisions and hydrodynamics only.

### ADR-002: Kirchhoff Electrical Network Solver ($L \cdot V = I$)
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Simple graph distance (Dijkstra) ignores parallel electrical paths across multiple intake nodes.
- **Decision**: Model electrical conduction as a Kirchhoff Laplacian circuit ($L \cdot V = I$), calculating exact node voltage potentials and $I^2 R$ Joule heating. Overloaded edges visually glow orange-red.

### ADR-003: Decoupled Headless Simulation Core
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: Need high-speed evolutionary simulation without rendering overhead.
- **Decision**: Decouple the core engine (`ObsidiaEngine`) into a pure Python data model that can run headless for fast evolution or connect to 3D visualizers.

### ADR-004: Local Ollama LLM Integration (`http://localhost:11434`)
- **Date**: 2026-08-12
- **Status**: Approved
- **Context**: User requested using local Ollama anytime to save API tokens and generate evolutionary content.
- **Decision**: Use local Ollama (`qwen:latest` / `qwen3.5-abliterated:27b`) for offline YAML configuration synthesis, procedural creature blueprint generation, and species evolutionary journal generation.

### ADR-005: Visualizer Engine Stack Selection — Web3D (Three.js / WebGL)
- **Date**: 2026-08-12
- **Status**: Approved by EV
- **Context**: Evaluated 3 technology stack demos (Web3D Three.js, Python Native ASCII/Plot, Headless Ollama).
- **Decision**: Formally selected **Web3D (Three.js / WebGL + HTML5/CSS Gauges HUD)** for primary rendering. Connects to Python Headless Core and Local Ollama via local HTTP/WebSocket bridge.

---

## User Requests & Context Notes
- **User**: EV (male), GitHub user `Vidusacha`. Repository: `https://github.com/Vidusacha/Obsidia-7-Harmony`.
- **Language Policy**: Russian for explanatory discussions, English for code, comments, and file names.
- **Automated Maintenance**: Enforced via `.agents/rules/git_documentation_update.md` before all git pushes.
