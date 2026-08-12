"""
Obsidia-7 Harmony — BCC Grid Spatial Lattice
Manages 3D positioning and 14-face docking ports for truncated octahedra.
"""

from typing import List, Tuple, Dict, Optional
import math


class BCCPort:
    """Represents one of the 14 docking ports on a truncated octahedron face."""
    
    # 6 Square faces + 8 Hexagonal faces
    FACE_NORMALS: Dict[str, Tuple[int, int, int]] = {
        # 6 Square faces
        "SQ_PX": (1, 0, 0),
        "SQ_NX": (-1, 0, 0),
        "SQ_PY": (0, 1, 0),
        "SQ_NY": (0, -1, 0),
        "SQ_PZ": (0, 0, 1),
        "SQ_NZ": (0, 0, -1),
        # 8 Hexagonal faces
        "HX_PPP": (1, 1, 1),
        "HX_PPM": (1, 1, -1),
        "HX_PMP": (1, -1, 1),
        "HX_PMM": (1, -1, -1),
        "HX_NPP": (-1, 1, 1),
        "HX_NPM": (-1, 1, -1),
        "HX_NMP": (-1, -1, 1),
        "HX_NMM": (-1, -1, -1)
    }

    def __init__(self, port_id: str, face_normal: Tuple[int, int, int]):
        self.port_id = port_id
        self.face_normal = face_normal
        self.connected_to: Optional[Tuple[int, str]] = None  # (target_node_id, target_port_id)


class BCCBlockNode:
    """Represents a single modular truncated octahedron block in 3D BCC space."""

    def __init__(self, node_id: int, bcc_coords: Tuple[int, int, int], block_type: str = "Base"):
        self.node_id = node_id
        self.bcc_coords = bcc_coords  # (x, y, z) in BCC integer lattice
        self.block_type = block_type
        self.ports: Dict[str, BCCPort] = {
            pid: BCCPort(pid, normal) for pid, normal in BCCPort.FACE_NORMALS.items()
        }

    def get_cartesian_position(self, unit_scale: float = 1.0) -> Tuple[float, float, float]:
        """Converts BCC lattice coordinates to 3D Cartesian coordinates."""
        x, y, z = self.bcc_coords
        return (x * unit_scale, y * unit_scale, z * unit_scale)

    def is_port_available(self, port_id: str) -> bool:
        return port_id in self.ports and self.ports[port_id].connected_to is None


class BCCGrid:
    """Spatial container enforcing discrete BCC lattice alignment."""

    def __init__(self, unit_scale: float = 1.0):
        self.unit_scale = unit_scale
        self.occupied_positions: Dict[Tuple[int, int, int], BCCBlockNode] = {}

    def can_place_block(self, bcc_coords: Tuple[int, int, int]) -> bool:
        return bcc_coords not in self.occupied_positions

    def place_block(self, node_id: int, bcc_coords: Tuple[int, int, int], block_type: str) -> BCCBlockNode:
        if not self.can_place_block(bcc_coords):
            raise ValueError(f"BCC position {bcc_coords} is already occupied!")
        node = BCCBlockNode(node_id, bcc_coords, block_type)
        self.occupied_positions[bcc_coords] = node
        return node

    def connect_blocks(self, node_a: BCCBlockNode, port_a_id: str, node_b: BCCBlockNode, port_b_id: str):
        """Establishes a bi-directional docking connection between two ports."""
        if not node_a.is_port_available(port_a_id) or not node_b.is_port_available(port_b_id):
            raise ValueError("One or both docking ports are unavailable!")

        node_a.ports[port_a_id].connected_to = (node_b.node_id, port_b_id)
        node_b.ports[port_b_id].connected_to = (node_a.node_id, port_a_id)
