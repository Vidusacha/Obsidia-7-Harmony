# Obsidia-7 Harmony — Game & Visual Design

## Visual Style: "Riveting-Punk" (Atom-Punk / Retro-Futurism)
Informed by *Robots (2005)* and *Meet the Robinsons*, the visual language avoids sleek modern plastic or synthetic organics. Everything is metallic, heavy, industrial, and tactile.

### Material Palette & PBR Properties
- **Polished Brass**: High metallic value (0.9), low roughness (0.2), warm golden specular highlights. Used for primary module casings and structural framing.
- **Weathered Copper**: Metallic (0.85), roughness (0.4–0.6) with green/cyan patina in crevices. Used for joint couplings and high-wear surfaces.
- **Rivets & Clockwork**: Heavy copper and steel rivets, visible internal meshing clockwork gears through glass or mesh cutouts.
- **Vacuum Tubes & Filaments**: Glowing neon-blue filaments for electrical Charge conduction; glowing orange-red for thermal overloads ($I^2 R$ Joule heating).
- **Oily Atmosphere & Water**: High-reflectivity oil oceans, volumetric gas clouds (G-- to G++), dark metallic junkyard backgrounds with soft bokeh highlights.

## Module Geometry: Truncated Octahedron (Kelvin Cell)
Each modular block (Proto-Protein) is shaped as a **Truncated Octahedron** (14 faces: 8 regular hexagons, 6 squares).
- **Spatial Alignment**: Modules map to a **Body-Centered Cubic (BCC)** spatial lattice.
- **Docking Ports**: 14 mechanical circular docking ports with glowing central filaments.
- **Discrete Rotations**: 14 docking face normals:
  - 6 Square faces: $(\pm 1, 0, 0), (0, \pm 1, 0), (0, 0, \pm 1)$
  - 8 Hexagon faces: $(\pm 1/\sqrt{3}, \pm 1/\sqrt{3}, \pm 1/\sqrt{3})$

## The 7 Proto-Protein Modules
1. **In-G (Gas Filter)**: Turbine intake drawing atmospheric/aquatic gases.
2. **In-M (Scrap Magnet)**: Mechanical claw collecting mineral salts & Materia.
3. **In-I (Antenna/Eye)**: Sensor array detecting resource gradients and external signals.
4. **Out-G (Exhaust)**: Rocket nozzle providing reactive thrust from gas reactions.
5. **Out-M (Waste Chute)**: Secretes armor plates, heat dissipation fins, or Materia briquettes.
6. **Out-I (Signal Lamp)**: Broadcasts vector signals and blueprint vectors to nearby organisms.
7. **Base Block (Chassis)**: Structural skeleton with minimal maintenance power draw.

## UI & HUD Aesthetics
- **Analog Gauges**: Brass rims, glass covers, trembling needles indicating `Charge` (Volts) and `Pressure` (Bar).
- **Diagnostic Blueprint Overlay**: Schematic grid overlay displaying electrical node potentials ($V_i$) and thermal entropy heat spots.
