"""
Obsidia-7 Harmony — Demo 2: Python Native Stack (Dependency-Free Pure Python)
BCC Spatial Lattice & Pure Python Kirchhoff Matrix Solver (L * V = I)
"""

import math
import sys
import json

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# --- Pure Python Gaussian Elimination for L * V = I ---
def solve_linear_system(A, b):
    """Solves A * x = b using Gaussian elimination with partial pivoting"""
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[max_row][i]) < 1e-12:
            continue
        M[i], M[max_row] = M[max_row], M[i]

        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot

        for r in range(n):
            if r != i:
                factor = M[r][i]
                for j in range(i, n + 1):
                    M[r][j] -= factor * M[i][j]

    return [M[i][n] for i in range(n)]


# --- 1. BCC Spatial Lattice Grid for Truncated Octahedra ---
class BCCNode:
    def __init__(self, node_id: int, bcc_coords: tuple, block_type: str):
        self.node_id = node_id
        self.bcc_coords = bcc_coords  # (x, y, z) in BCC integer space
        self.block_type = block_type
        self.pos = (bcc_coords[0] * 1.0, bcc_coords[1] * 1.0, bcc_coords[2] * 1.0)
        self.voltage = 0.0
        self.injected_current = 0.0


class KirchhoffBodyGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []  # List of tuples (u_idx, v_idx, conductance g)

    def add_node(self, bcc_coords: tuple, block_type: str) -> int:
        idx = len(self.nodes)
        node = BCCNode(idx, bcc_coords, block_type)
        self.nodes.append(node)
        return idx

    def add_edge(self, u: int, v: int, conductance: float = 1.0):
        self.edges.append((u, v, conductance))

    def solve_kirchhoff_circuit(self):
        """Solves Laplacian equation: L * V = I_inj"""
        n = len(self.nodes)
        if n == 0:
            return

        L = [[0.0] * n for _ in range(n)]
        I_inj = [0.0] * n

        # Set injected currents
        for idx, node in enumerate(self.nodes):
            if node.block_type == "In-G":
                I_inj[idx] = 12.0  # Intake current (12 Amps)
            elif node.block_type == "Out-G":
                I_inj[idx] = -12.0  # Exhaust drain (-12 Amps)

        # Build Conductance Matrix L
        for u, v, g in self.edges:
            L[u][v] -= g
            L[v][u] -= g
            L[u][u] += g
            L[v][v] += g

        # Ground node 0 to fix gauge invariance
        L_mod = [row[:] for row in L]
        L_mod[0] = [0.0] * n
        L_mod[0][0] = 1.0
        I_mod = I_inj[:]
        I_mod[0] = 0.0

        V = solve_linear_system(L_mod, I_mod)

        for idx, node in enumerate(self.nodes):
            node.voltage = V[idx]
            node.injected_current = I_inj[idx]

    def compute_joule_heating(self):
        """Computes power dissipation P = (V_u - V_v)^2 * g for each edge"""
        heat_dict = {}
        for u, v, g in self.edges:
            v_diff = self.nodes[u].voltage - self.nodes[v].voltage
            power = (v_diff ** 2) * g
            heat_dict[(u, v)] = power
        return heat_dict


# --- 2. Construct Sample Organism (6-Block BCC Spine) ---
def create_sample_organism() -> KirchhoffBodyGraph:
    graph = KirchhoffBodyGraph()
    n0 = graph.add_node((0, 0, 0), "In-G")      # Tail Intake
    n1 = graph.add_node((1, 1, 1), "Base")      # Linker 1
    n2 = graph.add_node((2, 0, 2), "In-M")      # Scrap Claw
    n3 = graph.add_node((3, 1, 3), "Base")      # Linker 2
    n4 = graph.add_node((4, 2, 4), "In-I")      # Antenna
    n5 = graph.add_node((5, 3, 5), "Out-G")     # Head Thrust Exhaust

    graph.add_edge(n0, n1, 1.2)
    graph.add_edge(n1, n2, 1.0)
    graph.add_edge(n2, n3, 0.8)
    graph.add_edge(n3, n4, 1.0)
    graph.add_edge(n4, n5, 1.5)
    graph.add_edge(n1, n3, 0.5)

    return graph


# --- 3. ASCII & Terminal Visualization ---
def run_python_native_demo():
    graph = create_sample_organism()
    graph.solve_kirchhoff_circuit()
    joule_heat = graph.compute_joule_heating()

    print("\n" + "=" * 65)
    print(" [OBSIDIA-7 HARMONY] -- Demo 2: Python Native Stack")
    print(" Kirchhoff Body-Graph Solver (L * V = I) & Joule Heating")
    print("=" * 65)
    print(" Node ID | Block  | BCC Coordinates | Voltage (V) | Current Injected")
    print("-" * 65)
    for node in graph.nodes:
        print(f"   [{node.node_id}]   | {node.block_type:6s} | {str(node.bcc_coords):15s} |  {node.voltage:6.2f} V  |  {node.injected_current:+5.1f} A")
    print("-" * 65)
    print(" Edge (Joint)  | Conductance g | Voltage Delta | Joule Heat P (I^2*R)")
    print("-" * 65)
    # Find conductance lookup table
    cond_map = {(u, v): g for u, v, g in graph.edges}

    for (u, v), power in joule_heat.items():
        g = cond_map[(u, v)]
        v_u = graph.nodes[u].voltage
        v_v = graph.nodes[v].voltage
        v_diff = abs(v_u - v_v)
        heat_indicator = "OVERLOAD HEAT" if power > 50.0 else "NOMINAL"
        print(f"  ({u} <---> {v})  |     {g:.1f} S     |    {v_diff:5.2f} V   |   {power:6.2f} W [{heat_indicator}]")
    print("=" * 65 + "\n")

    print("--- ASCII CIRCUIT CONDUCTIVITY DIAGRAM ---")
    print(" [In-G #0] ---1.2---> [Base #1] ---1.0---> [In-M #2]")
    print("   (0.0V)             (-10.0V)            (-15.6V)")
    print("                         |                   |")
    print("                        0.5                 0.8")
    print("                         v                   v")
    print("                       [Base #3] ---1.0---> [In-I #4] ---1.5---> [Out-G #5]")
    print("                        (-22.7V)            (-34.7V)            (-42.7V)")
    print("-------------------------------------------\n")


if __name__ == "__main__":
    run_python_native_demo()
