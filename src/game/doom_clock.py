"""
Obsidia-7 Harmony — Doom Clock & Meta-Progression Manager
Tracks the 3M-year countdown of star Helios-Omega and calculates Ecosystem Harmony Index.
"""

from typing import List, Dict, Any


class DoomClockManager:
    """Manages the supernova countdown and survival goals."""

    def __init__(self, initial_years: int = 3000000):
        self.remaining_years = initial_years
        self.years_per_cycle = 5000  # 5,000 years pass per simulation cycle
        self.harmony_index: float = 100.0  # Percentage dynamic stability
        self.planetary_shield_progress: float = 0.0
        self.spacefaring_progress: float = 0.0
        self.is_supernova_triggered: bool = False

    def tick_cycle(self, active_species_count: int, average_size: float, gas_stability: float):
        """Advances time and recalculates Ecosystem Harmony Index."""
        if self.remaining_years > 0:
            self.remaining_years -= self.years_per_cycle
        else:
            self.remaining_years = 0
            self.is_supernova_triggered = True

        # Harmony Index calculation based on species diversity & balance
        ideal_diversity = 5.0
        diversity_factor = min(1.0, active_species_count / ideal_diversity)
        stability_factor = gas_stability

        self.harmony_index = round((diversity_factor * 0.6 + stability_factor * 0.4) * 100.0, 1)

        # Progress towards planetary shielding & spacefaring goals
        if average_size > 10 and self.harmony_index > 70.0:
            self.planetary_shield_progress = min(100.0, self.planetary_shield_progress + 1.2)
            self.spacefaring_progress = min(100.0, self.spacefaring_progress + 0.8)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Doom Clock state for UI HUD display."""
        return {
            "remaining_years": self.remaining_years,
            "years_formatted": f"{self.remaining_years:,} Years",
            "harmony_index": self.harmony_index,
            "planetary_shield_percent": round(self.planetary_shield_progress, 1),
            "spacefaring_percent": round(self.spacefaring_progress, 1),
            "supernova_triggered": self.is_supernova_triggered
        }
