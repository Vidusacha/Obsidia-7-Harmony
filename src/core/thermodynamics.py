"""
Obsidia-7 Harmony — Thermodynamic Engine
Calculates n=m synthesis vs decay kinetics, maintenance costs, and thermal entropy.
"""

from typing import List, Dict, Tuple


class ThermodynamicsEngine:
    """Computes thermodynamic resource dynamics, entropy dissipation, and growth/decay rates."""

    def __init__(self, config: Dict):
        self.config = config.get("thermodynamics", {})
        self.gas_scale = config.get("gas_reactivity_scale", {})

    def evaluate_step(
        self,
        node_types: List[str],
        current_charge: float,
        current_materia: float,
        current_entropy: float,
        gas_environment: str = "G_minus"
    ) -> Tuple[float, float, float, str]:
        """
        Calculates 1 step of thermodynamic flux.
        Returns: (new_charge, new_materia, new_entropy, state_event)
        """
        num_blocks = len(node_types)
        base_cost = self.config.get("base_maintenance_cost", 1.0)
        maintenance_cost = num_blocks * base_cost

        # Gas Intake Reaction Output
        gas_info = self.gas_scale.get(gas_environment, {"energy_output": 6.0, "thermal_hazard": 1.0})
        in_g_count = node_types.count("In-G")
        out_g_count = node_types.count("Out-G")

        energy_yield = in_g_count * gas_info["energy_output"]
        thermal_hazard = in_g_count * gas_info["thermal_hazard"]

        # Calculate new resources
        new_charge = max(0.0, current_charge + energy_yield - maintenance_cost)
        
        # Entropy builds up with intake and dissipates with exhaust nodes (Out-G / Out-M)
        entropy_dissipation = (out_g_count * 2.5) + (node_types.count("Out-M") * 1.5)
        new_entropy = max(0.0, current_entropy + thermal_hazard - entropy_dissipation)

        # Check synthesis (n) vs decay (m) thresholds
        synth_charge_thresh = self.config.get("synthesis_charge_threshold", 30.0)
        synth_materia_thresh = self.config.get("synthesis_materia_threshold", 10.0)
        decay_charge_thresh = self.config.get("decay_charge_threshold", 5.0)
        max_entropy_limit = self.config.get("max_thermal_entropy_limit", 25.0)

        synthesis_rate_n = 1 if (new_charge >= synth_charge_thresh and current_materia >= synth_materia_thresh) else 0
        decay_rate_m = 1 if (new_charge <= decay_charge_thresh or new_entropy >= max_entropy_limit) else 0

        if synthesis_rate_n > decay_rate_m:
            event = "SYNTHESIS"
            new_materia = current_materia - synth_materia_thresh
        elif decay_rate_m > synthesis_rate_n:
            event = "DECAY"
            new_materia = current_materia + 5.0  # Dissolved block returns scrap
        else:
            event = "HARMONY"
            new_materia = current_materia

        return new_charge, new_materia, new_entropy, event
