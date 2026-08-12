"""
Obsidia-7 Harmony — Environment & World Simulation
Manages atmospheric gas clouds (G-- to G++), oil ocean currents, UV radiation, and Materia scrap nodes.
"""

import math
import random
from typing import List, Tuple, Dict, Any


class GasCloud:
    """A floating 3D volumetric cloud of atmospheric gas."""

    def __init__(self, cloud_id: int, pos: Tuple[float, float, float], radius: float, gas_type: str):
        self.cloud_id = cloud_id
        self.pos = pos  # (x, y, z)
        self.radius = radius
        self.gas_type = gas_type  # G_minus_minus, G_minus, G_zero, G_plus, G_plus_plus
        self.density: float = random.uniform(0.8, 1.5)

    def contains_point(self, point: Tuple[float, float, float]) -> bool:
        dx = point[0] - self.pos[0]
        dy = point[1] - self.pos[1]
        dz = point[2] - self.pos[2]
        return (dx*dx + dy*dy + dz*dz) <= (self.radius * self.radius)


class MateriaNode:
    """A floating scrap/mineral salt briquette in the world."""

    def __init__(self, node_id: int, pos: Tuple[float, float, float], amount: float = 15.0):
        self.node_id = node_id
        self.pos = pos
        self.amount = amount
        self.active = True


class Environment:
    """World environment tracking currents, gas clouds, UV flux, and scrap nodes."""

    def __init__(self, bounds_size: float = 50.0):
        self.bounds_size = bounds_size
        self.gas_clouds: List[GasCloud] = []
        self.materia_nodes: List[MateriaNode] = []
        self.uv_intensity: float = 1.0
        self.time_step: int = 0
        self.oil_current_velocity: Tuple[float, float, float] = (0.5, 0.0, 0.2)

        self._spawn_initial_world()

    def _spawn_initial_world(self):
        """Populates initial gas clouds and Materia scrap nodes."""
        gas_types = ["G_minus_minus", "G_minus", "G_zero", "G_plus", "G_plus_plus"]
        for i in range(8):
            pos = (
                random.uniform(-self.bounds_size*0.4, self.bounds_size*0.4),
                random.uniform(-10, 10),
                random.uniform(-self.bounds_size*0.4, self.bounds_size*0.4)
            )
            gtype = random.choice(gas_types)
            self.gas_clouds.append(GasCloud(i, pos, radius=8.0, gas_type=gtype))

        for j in range(12):
            pos = (
                random.uniform(-self.bounds_size*0.4, self.bounds_size*0.4),
                random.uniform(-5, 5),
                random.uniform(-self.bounds_size*0.4, self.bounds_size*0.4)
            )
            self.materia_nodes.append(MateriaNode(j, pos, amount=random.uniform(10.0, 25.0)))

    def update_environment(self):
        """Updates environment cycles, shifts gas clouds, and oscillates UV radiation."""
        self.time_step += 1
        
        # Slowly drift oil ocean currents
        angle = self.time_step * 0.05
        self.oil_current_velocity = (
            math.cos(angle) * 0.8,
            0.0,
            math.sin(angle) * 0.8
        )

        # UV cycle oscillation
        self.uv_intensity = 1.0 + 0.5 * math.sin(self.time_step * 0.02)

        # Drift gas clouds slowly
        for cloud in self.gas_clouds:
            cx, cy, cz = cloud.pos
            cloud.pos = (
                cx + self.oil_current_velocity[0] * 0.1,
                cy,
                cz + self.oil_current_velocity[2] * 0.1
            )

    def get_gas_at_position(self, pos: Tuple[float, float, float]) -> str:
        """Returns the dominant gas type at a given 3D position."""
        for cloud in self.gas_clouds:
            if cloud.contains_point(pos):
                return cloud.gas_type
        return "G_zero"  # Default ambient atmosphere

    def to_dict(self) -> Dict[str, Any]:
        """Serializes environment state for JSON API."""
        return {
            "time_step": self.time_step,
            "uv_intensity": round(self.uv_intensity, 2),
            "oil_current": [round(c, 2) for c in self.oil_current_velocity],
            "gas_clouds": [
                {
                    "id": c.cloud_id,
                    "pos": [round(p, 2) for p in c.pos],
                    "radius": c.radius,
                    "type": c.gas_type
                } for c in self.gas_clouds
            ],
            "materia_nodes": [
                {
                    "id": m.node_id,
                    "pos": [round(p, 2) for p in m.pos],
                    "amount": round(m.amount, 1),
                    "active": m.active
                } for m in self.materia_nodes if m.active
            ]
        }
