"""
Obsidia-7 Harmony — Demo 3: Headless Core + Local Ollama Integration Showcase
Runs thermodynamic growth cycles (n=m) and queries local Ollama (http://localhost:11434) for AI mutations & lore.
"""

import json
import random
import sys
import time
import urllib.request
import urllib.error

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen:latest"  # Fallback: qwen3.5-abliterated:27b or qwen:latest


class HeadlessOrganism:
    def __init__(self, species_name: str):
        self.species_name = species_name
        self.blocks = ["In-G", "Base", "Base", "Out-G", "Base"]  # Initial 5-block organism
        self.charge = 50.0
        self.materia = 20.0
        self.entropy = 5.0
        self.age_cycles = 0

    def calculate_thermodynamic_step(self, gas_environment: str = "G-"):
        """Calculates 1 cycle of synthesis (n) vs decay (m)"""
        self.age_cycles += 1
        num_blocks = len(self.blocks)

        # Maintenance Cost = sum(block_costs) * stress
        base_maintenance = num_blocks * 1.5
        
        # Gas intake reaction
        in_g_count = self.blocks.count("In-G")
        gas_energy_yield = in_g_count * (15.0 if gas_environment == "G--" else 8.0)

        # Update Charge & Entropy
        self.charge = max(0.0, self.charge + gas_energy_yield - base_maintenance)
        self.entropy += (in_g_count * 2.0) - (self.blocks.count("Out-G") * 2.5)
        self.entropy = max(0.0, self.entropy)

        # Rate of synthesis (n) vs Rate of decay (m)
        synthesis_rate_n = 1 if (self.charge > 30.0 and self.materia > 10.0) else 0
        decay_rate_m = 1 if (self.charge < 5.0 or self.entropy > 25.0) else 0

        # Apply growth or decay
        if synthesis_rate_n > decay_rate_m:
            new_block = random.choice(["In-M", "Out-G", "In-I", "Out-M", "Base"])
            self.blocks.append(new_block)
            self.materia -= 8.0
            return f"SYNTHESIS (+1 Block: {new_block})"
        elif decay_rate_m > synthesis_rate_n and len(self.blocks) > 5:
            removed_block = self.blocks.pop()
            return f"DECAY (-1 Block: {removed_block})"
        else:
            return "DYNAMIC HARMONY (n = m)"


def query_local_ollama(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """Queries local Ollama instance at http://localhost:11434"""
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 150
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', '').strip()
    except Exception as e:
        # Fallback offline simulation output if Ollama is busy or initializing
        return (f"[Offline Local Fallback Engine]: Specimen '{DEFAULT_MODEL}' evolved new 'Turbo-Exhaust' "
                f"nozzle adapting to G-- atmospheric turbulence. Structural integrity stable.")


def run_ollama_headless_demo():
    print("\n" + "=" * 70)
    print(" [OBSIDIA-7 HARMONY] -- Demo 3: Headless Core + Local Ollama Showcase")
    print(" Running Thermodynamic n=m cycles & Local LLM Procedural Blueprinting")
    print("=" * 70)

    creature = HeadlessOrganism("Aethel-Spark-V1")
    print(f" Initial Organism: '{creature.species_name}' | Size: {len(creature.blocks)} Blocks")
    print(f" Initial Blocks: {creature.blocks}")
    print("-" * 70)

    # Simulate 5 Cycles
    for cycle in range(1, 6):
        gas_env = "G--" if cycle == 3 else "G-"
        event = creature.calculate_thermodynamic_step(gas_env)
        print(f" Cycle {cycle:2d} | Gas: {gas_env:3s} | Charge: {creature.charge:5.1f}V | "
              f"Entropy: {creature.entropy:4.1f} | Size: {len(creature.blocks)} | Status: {event}")
        time.sleep(0.3)

    print("-" * 70)
    print(" Requesting Local Ollama AI species adaptation report...")
    prompt = (
        f"You are the AI mutation engine for Obsidia-7 Harmony. "
        f"A creature '{creature.species_name}' has grown to {len(creature.blocks)} blocks: {creature.blocks}. "
        f"Current Charge is {creature.charge:.1f}V in a reactive G-- gas environment. "
        f"In 2 concise sentences in English, describe its emergent mutation and Riveting-Punk aesthetic adaptation."
    )

    print(f" Prompting Model [{DEFAULT_MODEL}] at http://localhost:11434 ...")
    ai_report = query_local_ollama(prompt)

    print("\n" + ">>> LOCAL OLLAMA GENERATIVE REPORT <<<")
    print(f'"{ai_report}"')
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_ollama_headless_demo()
