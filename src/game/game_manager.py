"""
Obsidia-7 Harmony — Master Game Manager
Orchestrates environment, physics world, organism ecosystem, and Doom Clock meta-progression.
"""

from typing import List, Dict, Any
from ..core.organism import Organism
from ..core.config_loader import load_config
from .environment import Environment
from .physics_world import PhysicsWorld
from .doom_clock import DoomClockManager


class GameManager:
    """Master game orchestrator linking all simulation subsystems."""

    def __init__(self):
        self.config = load_config()
        self.environment = Environment(bounds_size=60.0)
        self.physics_world = PhysicsWorld()
        self.doom_clock = DoomClockManager(initial_years=3000000)

        # Create Player Organism
        self.player_organism = Organism("Aethel-Spark-Player", self.config)
        self.player_entity = self.physics_world.add_organism(0, self.player_organism, (0.0, 0.0, 0.0))

        # Create AI Wild Species
        self.ai_species: List[Organism] = []
        self._spawn_ai_species()

    def _spawn_ai_species(self):
        names = ["Vulcan-Chassis", "Zephyr-Filter", "Cobalt-Scraptron"]
        for idx, name in enumerate(names, start=1):
            ai_org = Organism(name, self.config)
            self.ai_species.append(ai_org)
            self.physics_world.add_organism(
                idx,
                ai_org,
                (idx * 8.0 - 12.0, 0.0, idx * 6.0 - 9.0)
            )

    def tick_game_loop(self, player_steering_yaw: float = 0.0) -> Dict[str, Any]:
        """Advances game loop by 1 tick."""
        # 1. Update Environment
        self.environment.update_environment()

        # 2. Steer player organism
        self.player_entity.yaw += player_steering_yaw

        # 3. Physics & Movement Integration
        self.physics_world.step(dt=0.1, oil_current=self.environment.oil_current_velocity)

        # 4. Check Materia collection collisions
        self.physics_world.check_materia_collisions(self.environment.materia_nodes)

        # 5. Step Thermodynamic engine for all organisms
        player_gas = self.environment.get_gas_at_position(tuple(self.player_entity.pos))
        event, player_snapshot = self.player_organism.step_simulation(player_gas)

        ai_snapshots = []
        for ai_org in self.ai_species:
            _, ai_snap = ai_org.step_simulation("G_minus")
            ai_snapshots.append(ai_snap)

        # 6. Tick Doom Clock
        all_sizes = [len(self.player_organism.nodes)] + [len(a.nodes) for a in self.ai_species]
        avg_size = sum(all_sizes) / len(all_sizes)
        self.doom_clock.tick_cycle(
            active_species_count=1 + len(self.ai_species),
            average_size=avg_size,
            gas_stability=0.8
        )

        # Full Game State Snapshot
        return {
            "environment": self.environment.to_dict(),
            "doom_clock": self.doom_clock.to_dict(),
            "player": {
                "entity_id": self.player_entity.entity_id,
                "pos": [round(p, 2) for p in self.player_entity.pos],
                "vel": [round(v, 2) for v in self.player_entity.vel],
                "yaw": round(self.player_entity.yaw, 2),
                "blueprint": self.player_organism.to_json_blueprint(),
                "snapshot": player_snapshot
            },
            "ai_organisms": [
                {
                    "entity_id": entity_id,
                    "pos": [round(p, 2) for p in entity.pos],
                    "species": entity.organism.species_name,
                    "size": len(entity.organism.nodes)
                } for entity_id, entity in self.physics_world.entities.items() if entity_id != 0
            ]
        }
