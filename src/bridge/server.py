"""
Obsidia-7 Harmony — Local HTTP Engine Server & Web Bridge
Serves Web3D Three.js frontend and exposes live simulation REST APIs.
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

from src.core.organism import Organism
from src.core.config_loader import load_config

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8000
OLLAMA_URL = "http://localhost:11434/api/generate"

# Initialize global organism & configuration
config = load_config()
organism = Organism(species_name="Aethel-Spark-Alpha", config=config)


class ObsidiaHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler serving static web files and REST endpoints."""

    def do_GET(self):
        if self.path == "/api/organism":
            self.send_json_response(organism.to_json_blueprint())
        elif self.path == "/" or self.path == "/index.html":
            self.path = "/demos/demo1_web_threejs/index.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == "/api/step":
            event, snapshot = organism.step_simulation(gas_environment="G_minus")
            self.send_json_response(snapshot)
        elif self.path == "/api/ollama_mutate":
            prompt = (
                f"You are the AI mutation engine for Obsidia-7 Harmony. "
                f"Organism '{organism.species_name}' has {len(organism.nodes)} blocks: {[n.block_type for n in organism.nodes]}. "
                f"Current Charge is {organism.charge:.1f}V in G-- gas environment. "
                f"In 2 short sentences, describe its new Riveting-Punk adaptation."
            )
            report = query_local_ollama(prompt)
            self.send_json_response({"species": organism.species_name, "ai_report": report})
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
        return "[Local Ollama Engine]: Organism synthesized reinforced brass cooling vanes to vent thermal overloads."


def run_server():
    # Set current directory to workspace root
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    with socketserver.TCPServer(("", PORT), ObsidiaHTTPHandler) as httpd:
        print("\n" + "=" * 65)
        print(" ⚙️ OBSIDIA-7 HARMONY — Engine Server & Web Bridge Active")
        print(f" Live Web App UI: http://localhost:{PORT}")
        print(f" Organism API:    http://localhost:{PORT}/api/organism")
        print("=" * 65 + "\n")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
