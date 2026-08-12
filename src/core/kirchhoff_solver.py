"""
Obsidia-7 Harmony — Kirchhoff Circuit & Conductive Physics Solver
Solves Laplacian equation L * V = I for electrical potentials and Joule heating.
"""

from typing import List, Tuple, Dict
import math


def solve_gaussian_elimination(A: List[List[float]], b: List[float]) -> List[float]:
    """Solves A * x = b using Gaussian elimination with partial pivoting in pure Python."""
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


class KirchhoffSolver:
    """Computes electrical node potentials and Joule heating power dissipation across a body graph."""

    def __init__(self, base_intake_current: float = 12.0):
        self.base_intake_current = base_intake_current

    def solve(self, num_nodes: int, node_types: List[str], edges: List[Tuple[int, int, float]]) -> Tuple[List[float], Dict[Tuple[int, int], float]]:
        """
        Solves circuit potentials V and returns (voltages, joule_heating_dict).
        - num_nodes: Total number of modules in body graph
        - node_types: List of block types ("In-G", "Out-G", "Base", etc.)
        - edges: List of tuples (u_idx, v_idx, conductance_g)
        """
        if num_nodes == 0:
            return [], {}

        L = [[0.0] * num_nodes for _ in range(num_nodes)]
        I_inj = [0.0] * num_nodes

        # Inject currents at intake/exhaust nodes
        for idx, btype in enumerate(node_types):
            if btype == "In-G":
                I_inj[idx] += self.base_intake_current
            elif btype == "Out-G":
                I_inj[idx] -= self.base_intake_current

        # Build Conductance Matrix L
        for u, v, g in edges:
            L[u][v] -= g
            L[v][u] -= g
            L[u][u] += g
            L[v][v] += g

        # Ground node 0 to fix gauge invariance
        L_mod = [row[:] for row in L]
        L_mod[0] = [0.0] * num_nodes
        L_mod[0][0] = 1.0
        I_mod = I_inj[:]
        I_mod[0] = 0.0

        voltages = solve_gaussian_elimination(L_mod, I_mod)

        # Compute Joule Heating P = (V_u - V_v)^2 * g
        joule_heat: Dict[Tuple[int, int], float] = {}
        for u, v, g in edges:
            v_diff = voltages[u] - voltages[v]
            power = (v_diff ** 2) * g
            joule_heat[(u, v)] = power

        return voltages, joule_heat
