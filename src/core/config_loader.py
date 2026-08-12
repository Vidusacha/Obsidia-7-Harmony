"""
Obsidia-7 Harmony — Config Loader Module
Loads external YAML/JSON configuration files for simulation parameters.
"""

import json
import os
from typing import Dict, Any


def load_config(config_path: str = "config/default_config.yaml") -> Dict[str, Any]:
    """Loads YAML or JSON configuration file. Provides default fallback if file missing."""
    if not os.path.exists(config_path):
        return get_default_config()

    try:
        # Try YAML parsing if available, or fallback to simple JSON parser
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                import yaml
                return yaml.safe_load(content)
            except ImportError:
                # Basic key-value parser for simple YAML if pyyaml not installed
                return parse_simple_yaml(content)
    except Exception:
        return get_default_config()


def parse_simple_yaml(yaml_text: str) -> Dict[str, Any]:
    """Fallback simple YAML parser for basic nested structures."""
    result: Dict[str, Any] = {}
    current_section = result

    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if not val:
                result[key] = {}
                current_section = result[key]
            else:
                try:
                    current_section[key] = float(val) if '.' in val else int(val)
                except ValueError:
                    current_section[key] = val

    return result if result else get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Hardcoded default configuration dictionary."""
    return {
        "simulation": {"time_step_sec": 0.1, "min_body_size": 5},
        "thermodynamics": {
            "mutation_chance": 0.10,
            "base_maintenance_cost": 1.0,
            "synthesis_charge_threshold": 30.0,
            "synthesis_materia_threshold": 10.0,
            "decay_charge_threshold": 5.0,
            "max_thermal_entropy_limit": 25.0
        },
        "gas_reactivity_scale": {
            "G_minus_minus": {"energy_output": 25.0, "thermal_hazard": 8.0},
            "G_minus": {"energy_output": 12.0, "thermal_hazard": 3.0},
            "G_zero": {"energy_output": 6.0, "thermal_hazard": 1.0}
        }
    }
