# Obsidia-7 Harmony — System Architecture & Specification

## High-Level Architecture Overview

```
+-------------------------------------------------------------------+
|                        Obsidia-7 Harmony                          |
+-------------------------------------------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+-------------------------------+               +-----------------------+
|  ObsidiaEngine (Headless Core)|               | Local Ollama LLM      |
|  - BCC Lattice Kinematics     | <-----------> | - Blueprint Gen       |
|  - Kirchhoff Solver (L*V=I)   |   REST API    | - YAML Config Synth   |
|  - Joule Heating (I^2*R)      |   (Port 11434)| - Evolution Lore      |
|  - Thermodynamic n=m Sync     |               +-----------------------+
+-------------------------------+
                 |
                 | HTTP / WebSockets
                 v
+-------------------------------+
|  ObsidiaVis (Web3D Three.js)  |
|  - Riveting-Punk PBR Shaders  |
|  - Polished Brass / Copper    |
|  - Glowing Vacuum Filament    |
|  - Analog Gauge UI HUD        |
+-------------------------------+
```

## Component Breakdown

### 1. `ObsidiaEngine` (Headless Core)
Written in pure Python 3.12.
- **`BCCGrid`**: Computes 3D coordinates on Body-Centered Cubic lattice $(x, y, z) \in \mathbb{Z}^3$. Handles 14 face docking quaternions.
- **`KirchhoffSolver`**: Builds conductance matrix $L$, solves $L \cdot V = I$, and computes edge dissipation $P_{ij} = (V_i - V_j)^2 \cdot g_{ij}$.
- **`ThermodynamicsEngine`**: Tracks block synthesis rate $n$ vs decay rate $m$, updating creature size and energy balance.
- **`ConfigLoader`**: Parses external YAML/JSON configuration files.

### 2. Local Ollama Bridge (`OllamaBridge`)
Interfaces with Ollama running at `http://localhost:11434/api/generate`.
- Sends creature state JSON prompts to `qwen:latest` or `qwen3.5-abliterated:27b`.
- Receives structured blueprint mutations or evolutionary lore narratives.

### 3. `ObsidiaVis` (Web3D Renderer — Primary Frontend)
Built with Three.js / WebGL and HTML5/CSS Canvas HUD.
- Renders 14-face truncated octahedra with PBR polished brass and weathered copper materials.
- Displays animated analog gauges for Charge ($V$) and Pressure/Entropy ($BAR$).
- Highlights electrical node potentials and Joule heating overloads ($I^2 R$) with glowing filaments.
