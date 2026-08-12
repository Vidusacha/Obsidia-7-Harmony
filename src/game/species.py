"""
Obsidia-7 Harmony — Species Generator & Visual Identity Palette
Manages distinct visual themes, color shaders, and procedural Primal Spark organism blueprints.
"""

import random
from typing import List, Tuple, Dict, Any


class SpeciesTheme:
    """Visual theme and material properties for a species."""

    def __init__(self, species_id: int, name: str, metal_color: int, glow_color: int, roughness: float, metalness: float):
        self.species_id = species_id
        self.name = name
        self.metal_color = metal_color  # Hex integer
        self.glow_color = glow_color    # Hex integer
        self.roughness = roughness
        self.metalness = metalness


# 4 Distinct Riveting-Punk Species Palettes
SPECIES_PALETTES: Dict[int, SpeciesTheme] = {
    0: SpeciesTheme(0, "Brass-Aurum (Alpha)", 0xd4af37, 0x00f0ff, 0.25, 0.85),   # Golden Brass + Cyan Glow
    1: SpeciesTheme(1, "Copper-Rubrum (Beta)", 0xb87333, 0xff3344, 0.45, 0.90),   # Weathered Copper + Crimson Glow
    2: SpeciesTheme(2, "Steel-Azure (Gamma)", 0x8a9ea7, 0x00ffaa, 0.30, 0.80),    # Steel Zinc + Emerald Glow
    3: SpeciesTheme(3, "Bronze-Purpura (Delta)", 0xcd7f32, 0xaa00ff, 0.50, 0.85)  # Vintage Bronze + Violet Glow
}


def generate_random_primal_spark(species_id: int, config: Dict[str, Any]) -> Tuple[str, List[Tuple[Tuple[int, int, int], str]]]:
    """
    Generates a procedural random Primal Spark organism.
    Returns: (species_name, [(bcc_coords, block_type), ...])
    """
    theme = SPECIES_PALETTES.get(species_id, SPECIES_PALETTES[0])
    
    # Random block composition (5 to 7 blocks)
    num_blocks = random.randint(5, 7)
    available_types = ["In-G", "Out-G", "In-M", "Out-M", "In-I", "Out-I", "Base"]
    
    blocks: List[Tuple[Tuple[int, int, int], str]] = []
    # Always include at least 1 In-G (intake) and 1 Out-G (thrust)
    blocks.append(((0, 0, 0), "In-G"))
    blocks.append(((1, 1, 1), "Base"))
    blocks.append(((2, 0, 2), "In-M"))
    blocks.append(((3, 1, 3), "Base"))
    blocks.append(((4, 2, 4), "Out-G"))

    # Add extra random blocks if num_blocks > 5
    for i in range(5, num_blocks):
        coords = (i, i // 2, i)
        btype = random.choice(available_types)
        blocks.append((coords, btype))

    return theme.name, blocks
