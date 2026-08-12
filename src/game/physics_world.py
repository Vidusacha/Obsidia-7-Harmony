"""
Obsidia-7 Harmony — Physics World & 3D Locomotion Solver
Solves organism kinematic movement, Out-G thrust vectors, oil current drag, and collision dynamics.
"""

import math
from typing import List, Tuple, Dict, Any
from ..core.organism import Organism


class PhysicsEntity:
    """A physical 3D organism entity in the simulation world."""

    def __init__(self, entity_id: int, organism: Organism, pos: Tuple[float, float, float]):
        self.entity_id = entity_id
        self.organism = organism
        self.pos = list(pos)        # [x, y, z]
        self.vel = [0.0, 0.0, 0.0]  # [vx, vy, vz]
        self.acc = [0.0, 0.0, 0.0]  # [ax, ay, az]
        self.yaw = 0.0              # Heading angle in radians
        self.mass = len(organism.nodes) * 2.0  # Mass proportional to block count

    def apply_force(self, fx: float, fy: float, fz: float):
        self.acc[0] += fx / self.mass
        self.acc[1] += fy / self.mass
        self.acc[2] += fz / self.mass

    def update_physics(self, dt: float, oil_current: Tuple[float, float, float]):
        """Integrates kinematics with Euler integration and oil current drag."""
        # 1. Out-G Exhaust Reactive Thrust
        out_g_count = [n.block_type for n in self.organism.nodes].count("Out-G")
        thrust_magnitude = out_g_count * 8.0

        if thrust_magnitude > 0:
            tx = math.cos(self.yaw) * thrust_magnitude
            tz = math.sin(self.yaw) * thrust_magnitude
            self.apply_force(tx, 0.0, tz)

        # 2. Hydrodynamic Drag in Oil Ocean
        rel_vx = self.vel[0] - oil_current[0]
        rel_vz = self.vel[2] - oil_current[2]
        rel_speed = math.sqrt(rel_vx*rel_vx + rel_vz*rel_vz)
        
        drag_coeff = 0.15
        drag_fx = -drag_coeff * rel_vx * rel_speed
        drag_fz = -drag_coeff * rel_vz * rel_speed
        self.apply_force(drag_fx, 0.0, drag_fz)

        # 3. Integrate Velocity & Position
        self.vel[0] += self.acc[0] * dt
        self.vel[1] += self.acc[1] * dt
        self.vel[2] += self.acc[2] * dt

        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

        # Reset acceleration
        self.acc = [0.0, 0.0, 0.0]


class PhysicsWorld:
    """Container managing entity movement and collision interactions."""

    def __init__(self):
        self.entities: Dict[int, PhysicsEntity] = {}

    def add_organism(self, entity_id: int, organism: Organism, pos: Tuple[float, float, float]) -> PhysicsEntity:
        entity = PhysicsEntity(entity_id, organism, pos)
        self.entities[entity_id] = entity
        return entity

    def step(self, dt: float, oil_current: Tuple[float, float, float]):
        """Updates physics integration for all organisms."""
        for entity in self.entities.values():
            entity.update_physics(dt, oil_current)

    def check_materia_collisions(self, materia_nodes: List[Any]):
        """Checks if In-M scrap claws are close enough to collect Materia nodes."""
        for entity in self.entities.values():
            in_m_count = [n.block_type for n in entity.organism.nodes].count("In-M")
            if in_m_count == 0:
                continue

            collect_radius = 2.5 + in_m_count * 0.5
            ex, ey, ez = entity.pos

            for node in materia_nodes:
                if not node.active:
                    continue
                nx, ny, nz = node.pos
                dist_sq = (ex-nx)**2 + (ey-ny)**2 + (ez-nz)**2
                if dist_sq <= collect_radius * collect_radius:
                    # Harvest Materia!
                    entity.organism.materia += node.amount
                    node.active = False
