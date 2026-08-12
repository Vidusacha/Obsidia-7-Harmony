"""
Obsidia-7 Harmony — Master Game Manager & God Overseer Engine
Orchestrates autonomous multi-species evolution, God Sliders, tracking camera, and Ollama AI.
"""

from typing import List, Dict, Any
from ..core.config_loader import load_config
from .environment import Environment
from .physics_world import PhysicsWorld
from .doom_clock import DoomClockManager
from .ecosystem import EcosystemManager


class GameManager:
    """Master game orchestrator linking all simulation subsystems."""

    def __init__(self):
        self.config = load_config()
        self.environment = Environment(bounds_size=70.0)
        self.physics_world = PhysicsWorld()
        self.doom_clock = DoomClockManager(initial_years=3000000)
        self.ecosystem = EcosystemManager(self.config, self.environment, self.physics_world)

        # God Overseer Controls
        self.simulation_speed: float = 1.0
        self.mutation_rate_mult: float = 1.0
        self.forced_gas_environment: str = "G_minus"
        self.tracking_camera_species_id: int = 0

    def set_god_options(self, num_species: int = 2, speed: float = 1.0, gas_env: str = "G_minus", mutation_mult: float = 1.0):
        """Updates God Overseer controls dynamically."""
        self.simulation_speed = max(0.5, min(5.0, speed))
        self.mutation_rate_mult = max(0.1, min(5.0, mutation_mult))
        self.forced_gas_environment = gas_env

        if num_species != self.ecosystem.num_active_species:
            self.ecosystem.spawn_initial_ecosystem(num_species)

    def tick_game_loop(self) -> Dict[str, Any]:
        """Advances autonomous game loop by 1 tick."""
        # 1. Update Environment
        self.environment.update_environment()

        # 2. Physics & Movement Integration
        self.physics_world.step(dt=0.1 * self.simulation_speed, oil_current=self.environment.oil_current_velocity)

        # 3. Check Materia collection collisions
        self.physics_world.check_materia_collisions(self.environment.materia_nodes)

        # 4. Autonomous Ecosystem Step for All Species (2 or 4)
        species_snapshots = self.ecosystem.update_autonomous_ecosystem(
            simulation_speed=self.simulation_speed,
            mutation_rate_mult=self.mutation_rate_mult
        )

        # 5. Tick Doom Clock
        all_sizes = [len(entity.organism.nodes) for entity in self.ecosystem.species_entities.values()]
        avg_size = sum(all_sizes) / len(all_sizes) if all_sizes else 5.0
        self.doom_clock.tick_cycle(
            active_species_count=len(self.ecosystem.species_entities),
            average_size=avg_size,
            gas_stability=0.85
        )

        # Full Game State Snapshot for Web3D Spectator HUD
        return {
            "god_controls": {
                "simulation_speed": self.simulation_speed,
                "mutation_rate_mult": self.mutation_rate_mult,
                "forced_gas_env": self.forced_gas_environment,
                "num_species": self.ecosystem.num_active_species,
                "tracking_camera_id": self.tracking_camera_species_id
            },
            "environment": self.environment.to_dict(),
            "doom_clock": self.doom_clock.to_dict(),
            "species_list": [
                {
                    "species_id": s_id,
                    "species_name": entity.organism.species_name,
                    "pos": [round(p, 2) for p in entity.pos],
                    "yaw": round(entity.yaw, 2),
                    "blueprint": entity.organism.to_json_blueprint(),
                    "snapshot": snapshot
                } for (s_id, entity), snapshot in zip(self.ecosystem.species_entities.items(), species_snapshots)
            ]
        }
