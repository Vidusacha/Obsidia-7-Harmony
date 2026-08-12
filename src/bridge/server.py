"""
Obsidia-7 Harmony — Local HTTP Engine Server & Live Game Bridge
Serves Web3D Three.js Spectator interface and exposes God Overseer REST APIs.
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.request
from typing import Dict, Any

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.game.game_manager import GameManager

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8000
OLLAMA_URL = "http://localhost:11434/api/generate"

# Initialize global game manager
game = GameManager()


class ObsidiaGameHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler serving Web3D game assets and REST API endpoints."""

    def do_GET(self):
        if self.path == "/api/game_state" or self.path == "/api/organism":
            state = game.tick_game_loop()
            self.send_json_response(state)
        elif self.path == "/" or self.path == "/index.html":
            self.path = "/demos/demo1_web_threejs/index.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == "/api/game_tick" or self.path == "/api/step":
            state = game.tick_game_loop()
            self.send_json_response(state)

        elif self.path == "/api/god_setting":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body_bytes = self.rfile.read(content_length)
                try:
                    body = json.loads(body_bytes.decode('utf-8'))
                    num_species = body.get('num_species', 2)
                    speed = body.get('speed', 1.0)
                    gas_env = body.get('gas_env', 'G_minus')
                    mutation_mult = body.get('mutation_mult', 1.0)
                    game.set_god_options(num_species, speed, gas_env, mutation_mult)
                except Exception:
                    pass

            state = game.tick_game_loop()
            self.send_json_response(state)

        elif self.path == "/api/ollama_mutate":
            active_species = [e.organism.species_name for e in game.ecosystem.species_entities.values()]
            prompt = (
                f"You are the Lead Systems Architect AI for Obsidia-7 Harmony. "
                f"An autonomous ecosystem of {len(active_species)} species ({active_species}) is evolving in oil ocean. "
                f"Doom Clock: {game.doom_clock.remaining_years:,} years remaining until Helios-Omega supernova. "
                f"Describe their dynamic interaction and Riveting-Punk species adaptation in 2 short sentences."
            )
            report = query_local_ollama(prompt)
            self.send_json_response({"ai_report": report})
        else:
            self.send_error(404, "Endpoint not found")

    def send_json_response(self, data: Dict[str, Any]):
        body = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet logger for clean terminal output
        pass


def query_local_ollama(prompt: str, model_name: str = "qwen:latest") -> str:
    """Sends prompt to local Ollama API."""
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "max_tokens": 120}
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('response', '').strip()
    except Exception:
        return "[Local Ollama Engine]: Species Brass-Aurum developed twin reactive nozzles to evade Copper-Rubrum predation."


def run_server():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    with socketserver.TCPServer(("", PORT), ObsidiaGameHTTPHandler) as httpd:
        print("\n" + "=" * 65)
        print(" ⚙️ OBSIDIA-7 HARMONY — Spectator Ecosystem Server Active")
        print(f" Live Web3D Spectator UI: http://localhost:{PORT}")
        print("=" * 65 + "\n")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
