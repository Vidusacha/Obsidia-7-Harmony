"""
Obsidia-7 Harmony — Master Native Pygame 3D Ecosystem Simulator (120+ FPS)
High-performance native GPU-accelerated desktop application for autonomous multi-species evolution.
"""

import sys
import os
import math
import time
import random
import pygame
from typing import List, Tuple, Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.game.game_manager import GameManager
from src.game.species import SPECIES_PALETTES
from src.bridge.server import query_local_ollama

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Particle:
    """Sparks and Out-G thrust bubble particles."""
    def __init__(self, x, y, z, vx, vy, vz, color, life, size=3):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        self.life -= dt


def project_3d_to_2d(x: float, y: float, z: float, cam_pos: List[float], screen_w: int, screen_h: int) -> Tuple[int, int, int]:
    """Projects 3D point (x, y, z) onto 2D Pygame surface with perspective."""
    rel_x = x - cam_pos[0]
    rel_y = y - cam_pos[1]
    rel_z = z - cam_pos[2]

    fov = 420.0
    depth = max(0.1, rel_z + 28.0)
    sx = int(screen_w / 2 + (rel_x * fov) / depth)
    sy = int(screen_h / 2 - (rel_y * fov) / depth)
    scale = max(2, int((fov * 0.38) / depth))
    return sx, sy, scale


def draw_analog_gauge(surface, center_x, center_y, radius, title, value_str, value_ratio, text_font):
    """Renders a Riveting-Punk brass analog gauge with needle."""
    # Outer Brass Rim
    pygame.draw.circle(surface, (212, 175, 55), (center_x, center_y), radius, 3)
    pygame.draw.circle(surface, (16, 18, 24), (center_x, center_y), radius - 3)

    # Needle
    angle = -math.pi * 0.7 + (min(1.0, max(0.0, value_ratio))) * (math.pi * 1.4)
    nx = center_x + int(math.cos(angle) * (radius - 8))
    ny = center_y + int(math.sin(angle) * (radius - 8))
    pygame.draw.line(surface, (255, 60, 60), (center_x, center_y), (nx, ny), 2)
    pygame.draw.circle(surface, (212, 175, 55), (center_x, center_y), 4)

    # Text Labels
    t_surf = text_font.render(title, True, (212, 175, 55))
    v_surf = text_font.render(value_str, True, (255, 255, 255))
    surface.blit(t_surf, (center_x - t_surf.get_width() // 2, center_y + 6))
    surface.blit(v_surf, (center_x - v_surf.get_width() // 2, center_y + 18))


def run_native_3d_engine():
    pygame.init()
    pygame.font.init()

    screen_w, screen_h = 1150, 820
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("⚙️ Obsidia-7 Harmony — Native Pygame 3D Ecosystem Engine (120+ FPS)")

    font_small = pygame.font.SysFont("Segoe UI", 13)
    font_bold = pygame.font.SysFont("Segoe UI", 15, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 20, bold=True)

    # Initialize Master Game Manager
    game = GameManager()
    game.set_god_options(num_species=4, speed=1.0, gas_env="G_minus", mutation_mult=1.0)

    particles: List[Particle] = []
    clock = pygame.time.Clock()
    running = True
    is_paused = False
    focused_species_id = 0
    start_time = time.time()
    ollama_log_text = "[Ollama AI]: Native 3D Engine active. Press 'O' for AI species adaptation report."

    print("\n" + "=" * 70)
    print(" ⚙️ OBSIDIA-7 HARMONY — Master Native Pygame 3D Engine Running!")
    print(" Controls:")
    print("   [1 / 2] : Toggle 2 vs 4 Species")
    print("   [S]     : Toggle Speed (1x / 2x / 4x)")
    print("   [G]     : Toggle Gas Storm (G- Normal vs G-- Storm)")
    print("   [C]     : Cycle Camera Tracking Focus")
    print("   [O]     : Query Local Ollama AI Log")
    print("   [SPACE] : Pause / Resume Simulation")
    print("   [ESC]   : Exit")
    print("=" * 70 + "\n")

    while running:
        dt = clock.tick(120) / 1000.0  # 120 FPS Target
        elapsed = time.time() - start_time

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_1:
                    game.set_god_options(num_species=2, speed=game.simulation_speed, gas_env=game.forced_gas_environment)
                    ollama_log_text = "[Overseer]: Active ecosystem population set to 2 species."
                elif event.key == pygame.K_2:
                    game.set_god_options(num_species=4, speed=game.simulation_speed, gas_env=game.forced_gas_environment)
                    ollama_log_text = "[Overseer]: Active ecosystem population expanded to 4 species!"
                elif event.key == pygame.K_s:
                    new_speed = 2.0 if game.simulation_speed == 1.0 else (4.0 if game.simulation_speed == 2.0 else 1.0)
                    game.set_god_options(num_species=game.ecosystem.num_active_species, speed=new_speed, gas_env=game.forced_gas_environment)
                    ollama_log_text = f"[Overseer]: Simulation speed accelerated to {new_speed:.0f}x."
                elif event.key == pygame.K_g:
                    new_gas = "G_minus_minus" if game.forced_gas_environment == "G_minus" else "G_minus"
                    game.set_god_options(num_species=game.ecosystem.num_active_species, speed=game.simulation_speed, gas_env=new_gas)
                    ollama_log_text = f"[Overseer]: Atmosphere shifted to {new_gas}!"
                elif event.key == pygame.K_c:
                    focused_species_id = (focused_species_id + 1) % game.ecosystem.num_active_species
                    ollama_log_text = f"[Camera]: Focused tracking camera on Species #{focused_species_id}."
                elif event.key == pygame.K_o:
                    ollama_log_text = "[Ollama AI]: Querying local model at http://localhost:11434..."
                    active_species = [e.organism.species_name for e in game.ecosystem.species_entities.values()]
                    prompt = (
                        f"You are the Lead Systems Architect AI for Obsidia-7 Harmony. "
                        f"An autonomous ecosystem of {len(active_species)} species ({active_species}) is evolving in oil ocean. "
                        f"Doom Clock: {game.doom_clock.remaining_years:,} years remaining until Helios-Omega supernova. "
                        f"Describe their dynamic interaction and Riveting-Punk species adaptation in 2 short sentences."
                    )
                    report = query_local_ollama(prompt)
                    ollama_log_text = f"[AI Ticker]: \"{report}\""

        # Advance Game Tick if not paused
        state = game.tick_game_loop() if not is_paused else game.tick_game_loop()

        # Clear Screen (Dark Junkyard Atmosphere Background)
        screen.fill((7, 8, 11))

        # Camera Position (Orbiting or Tracking focused species)
        focus_entity = game.ecosystem.species_entities.get(focused_species_id)
        target_x = focus_entity.pos[0] if focus_entity else 0.0
        target_z = focus_entity.pos[2] if focus_entity else 0.0

        cam_x = target_x + math.sin(elapsed * 0.2) * 8.0
        cam_y = 12.0
        cam_z = target_z - 20.0
        cam_pos = [cam_x, cam_y, cam_z]

        # 1. Draw Oil Ocean Grid
        for gz in range(-40, 45, 8):
            p1_2d = project_3d_to_2d(-45, -2.5, gz, cam_pos, screen_w, screen_h)
            p2_2d = project_3d_to_2d(45, -2.5, gz, cam_pos, screen_w, screen_h)
            pygame.draw.line(screen, (28, 20, 14), (p1_2d[0], p1_2d[1]), (p2_2d[0], p2_2d[1]), 1)

        # 2. Draw Environment Gas Clouds & Scrap Materia Nodes
        for gc in state["environment"]["gas_clouds"]:
            color = (255, 69, 0) if gc["type"] == "G_minus_minus" else (0, 240, 255)
            sx, sy, size = project_3d_to_2d(gc["pos"][0], gc["pos"][1], gc["pos"][2], cam_pos, screen_w, screen_h)
            radius = max(8, int(gc["radius"] * size * 0.4))
            pygame.draw.circle(screen, color, (sx, sy), radius, 1)

        for mn in state["environment"]["materia_nodes"]:
            sx, sy, size = project_3d_to_2d(mn["pos"][0], mn["pos"][1], mn["pos"][2], cam_pos, screen_w, screen_h)
            pygame.draw.polygon(screen, (255, 215, 0), [
                (sx, sy - size), (sx + size, sy), (sx, sy + size), (sx - size, sy)
            ])

        # 3. Draw Species Organisms on BCC Lattice
        for sp in state["species_list"]:
            s_id = sp["species_id"]
            theme = SPECIES_PALETTES.get(s_id, SPECIES_PALETTES[0])

            # Convert RGB hex to tuples
            metal_rgb = (
                (theme.metal_color >> 16) & 0xFF,
                (theme.metal_color >> 8) & 0xFF,
                theme.metal_color & 0xFF
            )
            glow_rgb = (
                (theme.glow_color >> 16) & 0xFF,
                (theme.glow_color >> 8) & 0xFF,
                theme.glow_color & 0xFF
            )

            # Organism center position & rotation
            ox, oy, oz = sp["pos"]
            yaw = sp["yaw"]

            # Spawn Out-G Thrust Particles
            if not is_paused and random.random() < 0.4:
                particles.append(Particle(
                    ox - math.cos(yaw) * 1.5, oy, oz - math.sin(yaw) * 1.5,
                    -math.cos(yaw) * 2.0 + random.uniform(-0.5, 0.5),
                    random.uniform(0.1, 0.5),
                    -math.sin(yaw) * 2.0 + random.uniform(-0.5, 0.5),
                    glow_rgb,
                    random.uniform(0.4, 0.9)
                ))

            # Draw blocks & edges
            blocks = (sp["blueprint"] and sp["blueprint"]["blocks"]) or []
            for b in blocks:
                bcc = b["bcc"]
                # Rotate relative BCC block offsets by yaw
                rx = bcc[0] * math.cos(yaw) - bcc[2] * math.sin(yaw)
                rz = bcc[0] * math.sin(yaw) + bcc[2] * math.cos(yaw)

                world_x = ox + rx * 0.95
                world_y = oy + bcc[1] * 0.95 + math.sin(elapsed * 4 + b["id"]) * 0.1
                world_z = oz + rz * 0.95

                sx, sy, size = project_3d_to_2d(world_x, world_y, world_z, cam_pos, screen_w, screen_h)
                rect = pygame.Rect(sx - size, sy - size, size * 2, size * 2)

                # Draw Block Box & Wireframe Glow
                pygame.draw.rect(screen, metal_rgb, rect, border_radius=3)
                pygame.draw.rect(screen, glow_rgb, rect, width=2, border_radius=3)

                # Label Block Type
                if size > 6:
                    label_t = font_small.render(b["type"][:4], True, (255, 255, 255))
                    screen.blit(label_t, (sx - label_t.get_width() // 2, sy - 5))

        # 4. Update & Render Particles
        for p in particles[:]:
            p.update(dt)
            if p.life <= 0:
                particles.remove(p)
                continue
            sx, sy, size = project_3d_to_2d(p.x, p.y, p.z, cam_pos, screen_w, screen_h)
            pygame.draw.circle(screen, p.color, (sx, sy), max(1, size // 2))

        # 5. Draw Riveting-Punk HUD & Overlord Panel
        # Header Box
        hdr_rect = pygame.Rect(15, 15, 520, 115)
        pygame.draw.rect(screen, (16, 18, 24), hdr_rect, border_radius=6)
        pygame.draw.rect(screen, (212, 175, 55), hdr_rect, width=2, border_radius=6)

        t_hdr = font_title.render("⚙️ OBSIDIA-7 HARMONY — NATIVE ENGINE (120+ FPS)", True, (212, 175, 55))
        d_hdr = font_bold.render(f"💥 HELIOS-OMEGA: {state['doom_clock']['years_formatted']}  |  HARMONY: {state['doom_clock']['harmony_index']}%", True, (255, 69, 0))
        screen.blit(t_hdr, (25, 22))
        screen.blit(d_hdr, (25, 50))

        # Species Tags Legend
        lx = 25
        for s_idx, sp in enumerate(state["species_list"]):
            theme = SPECIES_PALETTES.get(s_idx, SPECIES_PALETTES[0])
            glow_rgb = ((theme.glow_color >> 16) & 0xFF, (theme.glow_color >> 8) & 0xFF, theme.glow_color & 0xFF)
            focus_mark = " (CAMERA)" if s_idx == focused_species_id else ""
            tag = font_small.render(f"• {sp['species_name']}{focus_mark}", True, glow_rgb)
            screen.blit(tag, (lx, 78))
            lx += 230

        # AI Ticker Banner
        ai_rect = pygame.Rect(15, 96, 520, 26)
        pygame.draw.rect(screen, (0, 0, 0), ai_rect, border_radius=3)
        ai_txt = font_small.render(ollama_log_text[:85], True, (200, 215, 230))
        screen.blit(ai_txt, (20, 101))

        # Analog Gauges Bottom Left
        player_sp = state["species_list"][0]["snapshot"] if state["species_list"] else {}
        chg_v = player_sp.get("charge", 50.0)
        ent_v = player_sp.get("entropy", 2.0)
        draw_analog_gauge(screen, 65, screen_h - 65, 45, "CHARGE", f"{chg_v:.1f}V", chg_v / 100.0, font_small)
        draw_analog_gauge(screen, 170, screen_h - 65, 45, "ENTROPY", f"{ent_v:.1f}BAR", ent_v / 25.0, font_small)

        # Overseer Controls Legend Bottom Right
        ctrl_rect = pygame.Rect(screen_w - 430, screen_h - 85, 415, 70)
        pygame.draw.rect(screen, (16, 18, 24), ctrl_rect, border_radius=6)
        pygame.draw.rect(screen, (184, 115, 51), ctrl_rect, width=2, border_radius=6)

        c_txt1 = font_bold.render("👑 OVERSEER CONTROLS:", True, (212, 175, 55))
        c_txt2 = font_small.render(f"[1/2] {game.ecosystem.num_active_species} Species | [S] Speed {game.simulation_speed:.0f}x | [G] {game.forced_gas_environment} | [C] Cam Focus", True, (220, 220, 220))
        c_txt3 = font_small.render("[O] Query Ollama AI Log | [SPACE] Pause | FPS: " + f"{clock.get_fps():.1f}", True, (0, 240, 255))
        screen.blit(c_txt1, (screen_w - 420, screen_h - 80))
        screen.blit(c_txt2, (screen_w - 420, screen_h - 60))
        screen.blit(c_txt3, (screen_w - 420, screen_h - 40))

        pygame.display.flip()

    pygame.quit()
    print("Master Native Pygame 3D Engine closed cleanly.")


if __name__ == "__main__":
    run_native_3d_engine()
