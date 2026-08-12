"""
Obsidia-7 Harmony — Ecosystem & Multi-Species Simulation Engine
Manages autonomous species interaction, predation, parasitic docking, and population evolution.
"""

import math
import random
from typing import List, Dict, Tuple, Any
from ..core.organism import Organism
from .species import SPECIES_PALETTES, generate_random_primal_spark
from .physics_world import PhysicsWorld, PhysicsEntity
from .environment import Environment


class EcosystemManager:
    """Manages autonomous multi-species evolution and interactions."""

    def __init__(self, config: Dict[str, Any], environment: Environment, physics_world: PhysicsWorld):
        self.config = config
        self.environment = environment
        self.physics_world = physics_world
        self.species_entities: Dict[int, PhysicsEntity] = {}
        self.num_active_species = 2  # Default: 2 species (can toggle to 4)

        self.spawn_initial_ecosystem(num_species=2)

    def spawn_initial_ecosystem(self, num_species: int = 2):
        """Spawns 2 or 4 distinct autonomous species in the world."""
        self.num_active_species = num_species
        self.physics_world.entities.clear()
        self.species_entities.clear()

        spawn_offsets = [
            (-12.0, 0.0, -10.0),
            (12.0, 0.0, 10.0),
            (-10.0, 0.0, 12.0),
            (10.0, 0.0, -12.0)
        ]

        for s_id in range(num_species):
            name, block_specs = generate_random_primal_spark(s_id, self.config)
            org = Organism(name, self.config)
            org.species_id = s_id
            
            entity = self.physics_world.add_organism(s_id, org, spawn_offsets[s_id])
            entity.species_id = s_id
            self.species_entities[s_id] = entity

    def update_autonomous_ecosystem(self, simulation_speed: float = 1.0, mutation_rate_mult: float = 1.0) -> List[Dict[str, Any]]:
        """Updates autonomous steering, predation, and thermodynamic steps for all active species."""
        snapshots = []

        # 1. Autonomous Navigation Towards Gas & Materia
        for s_id, entity in list(self.species_entities.items()):
            ex, ey, ez = entity.pos
            
            # Find nearest active Materia scrap node or gas cloud
            target_pos = self._find_nearest_resource_target((ex, ey, ez))
            if target_pos:
                dx = target_pos[0] - ex
                dz = target_pos[2] - ez
                desired_yaw = math.atan2(dz, dx)
                
                # Smoothly steer yaw towards target
                yaw_diff = (desired_yaw - entity.yaw + math.pi) % (2 * math.pi) - math.pi
                entity.yaw += max(-0.2, min(0.2, yaw_diff)) * simulation_speed

            # 2. Step Thermodynamics for Organism
            current_gas = self.environment.get_gas_at_position((ex, ey, ez))
            event, snapshot = entity.organism.step_simulation(current_gas)
            
            snapshot["species_id"] = s_id
            snapshot["species_name"] = entity.organism.species_name
            snapshot["pos"] = [round(p, 2) for p in entity.pos]
            snapshot["yaw"] = round(entity.yaw, 2)
            snapshot["theme"] = {
                "metal_color": SPECIES_PALETTES[s_id].metal_color,
                "glow_color": SPECIES_PALETTES[s_id].glow_color,
                "roughness": SPECIES_PALETTES[s_id].roughness,
                "metalness": SPECIES_PALETTES[s_id].metalness
            }
            snapshots.append(snapshot)

        # 3. Predation & Collision Dynamics
        self._resolve_predation_collisions()

        return snapshots

    def _find_nearest_resource_target(self, pos: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Finds nearest active Materia scrap node or Gas cloud."""
        ex, ey, ez = pos
        min_dist_sq = float('inf')
        best_target = None

        for node in self.environment.materia_nodes:
            if not node.active:
                continue
            nx, ny, nz = node.pos
            dist_sq = (ex-nx)**2 + (ey-ny)**2 + (ez-nz)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                best_target = node.pos

        return best_target if best_target else (0.0, 0.0, 0.0)

    def _resolve_predation_collisions(self):
        """Resolves organism collisions where larger organisms steal Charge/Materia from smaller ones."""
        entities = list(self.species_entities.values())
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                e1, e2 = entities[i], entities[j]
                dx = e1.pos[0] - e2.pos[0]
                dz = e1.pos[2] - e2.pos[2]
                dist = math.sqrt(dx*dx + dz*dz)

                if dist < 3.5:  # Collision contact!
                    # Predation: larger organism drains 5.0 Charge from smaller
                    size1 = len(e1.organism.nodes)
                    size2 = len(e2.organism.nodes)

                    if size1 > size2:
                        e1.organism.charge += 5.0
                        e2.organism.charge = max(0.0, e2.organism.charge - 5.0)
                    elif size2 > size1:
                        e2.organism.charge += 5.0
                        e1.organism.charge = max(0.0, e1.organism.charge - 5.0)
