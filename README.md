# Obsidia-7 Harmony ⚙️⚡

> A 3D thermodynamic mechanical evolution simulator & spectator ecosystem set in a riveting-punk junkyard universe.

[![Repository](https://img.shields.io/badge/GitHub-Vidusacha%2FObsidia--7--Harmony-gold)](https://github.com/Vidusacha/Obsidia-7-Harmony)

---

## ⚡ Master Native Application Launcher (120+ FPS)

Launch the full **Native Pygame 3D Autonomous Ecosystem Simulator** directly on Windows:

```powershell
python src/engine_native_3d.py
```

### Key Application Features:
- **4 Distinct Riveting-Punk Species**: *Brass-Aurum* (Golden Brass), *Copper-Rubrum* (Weathered Copper), *Steel-Azure* (Steel Zinc), and *Bronze-Purpura* (Vintage Bronze).
- **GPU Particles & VFX**: Out-G thrust bubble trails, welding sparks on module synthesis ($n$), glowing Kirchhoff Joule heating overloads ($I^2 R$).
- **Cinematic Tracking Camera**: Press `C` to smoothly lock camera focus onto any evolving species in 3D space.
- **Overseer God Controls**:
  - `1` / `2`: Toggle 2 vs 4 Active Species.
  - `S`: Cycle Simulation Speed ($1\times, 2\times, 4\times$).
  - `G`: Toggle Atmospheric Gas Storm (G0 Safe $\to$ G-- Storm).
  - `O`: Query local Ollama LLM (`http://localhost:11434`) for species adaptation reports.
  - `SPACE`: Pause / Resume simulation.

---

## 📜 Documentation Sitemap

- [**`concept.md`**](concept.md): Strategy, narrative lore (Helios-Omega, Junkyard, Inventors), and core pillars.
- [**`design.md`**](design.md): "Riveting-Punk" visual aesthetics, PBR materials, 14-face truncated octahedron specs, and UI gauges.
- [**`gameplay.md`**](gameplay.md): Laws of physics, Kirchhoff graph solver ($L \cdot V = I$), Joule heating ($I^2 R$), gas reactivity, and survival rules.
- [**`development_plan.md`**](development_plan.md): Milestone progress checklist and current status.
- [**`audit.md`**](audit.md): Architectural Decision Records (ADRs 001–008) and context distillation log.
- [**`architecture.md`**](architecture.md): Technical subsystem breakdown, BCC lattice math, and local Ollama API integration.

---

## 🛠️ Automated Repository Rules
This repository enforces automated pre-push documentation updates via `.agents/rules/git_documentation_update.md`.
