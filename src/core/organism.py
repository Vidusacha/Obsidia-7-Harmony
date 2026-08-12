"""
Obsidia-7 Harmony — Organism State & Mutation Engine
Encapsulates organism body graph, electrical state, and thermodynamic evolution.
"""

from typing import List, Tuple, Dict, Any
import random
from .bcc_grid import BCCGrid, BCCBlockNode
from .kirchhoff_solver import KirchhoffSolver
from .thermodynamics import ThermodynamicsEngine


class Organism:
    """Represents a multi-block mechanical life-form in Obsidia-7."""

    def __init__(self, species_name: str, config: Dict[str, Any]):
        self.species_name = species_name
        self.config = config
        self.grid = BCCGrid(unit_scale=1.0)
        self.solver = KirchhoffSolver(base_intake_current=12.0)
        self.thermo = ThermodynamicsEngine(config)

        self.nodes: List[BCCBlockNode] = []
        self.edges: List[Tuple[int, int, float]] = []

        self.charge: float = 50.0
        self.materia: float = 25.0
        self.entropy: float = 2.0
        self.age_cycles: int = 0

        # Initialize minimal 5-block organism spine on BCC grid
        self._initialize_primal_spark()

    def _initialize_primal_spark(self):
        """Creates the initial 5-block Primal Spark organism."""
        # 5 BCC positions along spine
        bcc_coords_list = [
            (0, 0, 0), (1, 1, 1), (2, 0, 2), (3, 1, 3), (4, 2, 4)
        ]
        types_list = ["In-G", "Base", "In-M", "Base", "Out-G"]

        for idx, (coords, btype) in enumerate(zip(bcc_coords_list, types_list)):
            node = self.grid.place_block(idx, coords, btype)
            self.nodes.append(node)

        # Connect adjacent spine nodes
        for i in range(len(self.nodes) - 1):
            self.edges.append((i, i + 1, 1.0))

    def step_simulation(self, gas_environment: str = "G_minus") -> Tuple[str, Dict[str, Any]]:
        """Advances simulation by 1 step. Solves Kirchhoff circuit and updates thermodynamics."""
        self.age_cycles += 1

        # 1. Kirchhoff Electrical Solve
        node_types = [n.block_type for n in self.nodes]
        voltages, joule_heat = self.solver.solve(len(self.nodes), node_types, self.edges)

        for idx, v in enumerate(voltages):
            self.nodes[idx].voltage = v

        # 2. Thermodynamic Flux Step
        self.charge, self.materia, self.entropy, event = self.thermo.evaluate_step(
            node_types, self.charge, self.materia, self.entropy, gas_environment
        )

        # 3. Apply Mutations / Growth / Decay
        mutation_note = ""
        if event == "SYNTHESIS":
            mutation_note = self._mutate_grow_block()
        elif event == "DECAY" and len(self.nodes) > 5:
            mutation_note = self._mutate_decay_block()

        # State Snapshot
        snapshot = {
            "species_name": self.species_name,
            "age_cycles": self.age_cycles,
            "num_blocks": len(self.nodes),
            "charge": self.charge,
            "materia": self.materia,
            "entropy": self.entropy,
            "event": event,
            "mutation_note": mutation_note,
            "node_types": node_types,
            "voltages": voltages,
            "joule_heat": {f"{u}-{v}": p for (u, v), p in joule_heat.items()}
        }

        return event, snapshot

    def _mutate_grow_block(self) -> str:
        """Appends a new block to an open BCC position."""
        last_node = self.nodes[-1]
        lx, ly, lz = last_node.bcc_coords
        new_coords = (lx + 1, ly + 1, lz + 1)

        if not self.grid.can_place_block(new_coords):
            new_coords = (lx + 1, ly, lz)

        if self.grid.can_place_block(new_coords):
            new_id = len(self.nodes)
            new_type = random.choice(["In-G", "Out-G", "In-M", "Out-M", "In-I", "Out-I", "Base"])
            node = self.grid.place_block(new_id, new_coords, new_type)
            self.nodes.append(node)
            self.edges.append((new_id - 1, new_id, 1.0))
            return f"Grew new {new_type} block at {new_coords}"
        return "Growth blocked by spatial collision"

    def _mutate_decay_block(self) -> str:
        """Removes the last block under severe maintenance deficiency or thermal damage."""
        if len(self.nodes) > 5:
            removed_node = self.nodes.pop()
            del self.grid.occupied_positions[removed_node.bcc_coords]
            self.edges = [(u, v, g) for u, v, g in self.edges if u != removed_node.node_id and v != removed_node.node_id]
            return f"Decayed block {removed_node.block_type} at {removed_node.bcc_coords}"
        return "Cannot decay below minimal 5-block threshold"

    def to_json_blueprint(self) -> Dict[str, Any]:
        """Serializes current organism state to JSON schema."""
        return {
            "species": self.species_name,
            "age": self.age_cycles,
            "size": len(self.nodes),
            "charge": round(self.charge, 2),
            "entropy": round(self.entropy, 2),
            "blocks": [
                {
                    "id": n.node_id,
                    "type": n.block_type,
                    "bcc": n.bcc_coords,
                    "voltage": round(getattr(n, 'voltage', 0.0), 2)
                } for n in self.nodes
            ],
            "edges": [{"u": u, "v": v, "g": g} for u, v, g in self.edges]
        }
