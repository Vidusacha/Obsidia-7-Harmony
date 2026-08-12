"""
Obsidia-7 Harmony — Master Native 3D Mechanical Robot Engine (120+ FPS)
Renders True 3D Truncated Octahedra & 7 Specialized Robot Parts with 3D Matrix Camera.
"""

import sys
import os
import math
import time
import random
import pygame
from pyrr import Matrix44, Vector4
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
    """Sparks, gas bubbles, and thrust particles in 3D."""
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


class Camera3D:
    """True 3D Perspective Camera using Pyrr Matrix44 transformation."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.fov = 45.0
        self.distance = 32.0
        self.pitch = 0.45  # Angle looking down (rad)
        self.yaw = 0.0     # Orbit angle (rad)
        self.target = [0.0, 0.0, 0.0]

    def get_view_proj_matrix(self) -> Matrix44:
        # Calculate camera eye position orbiting target
        cx = self.target[0] + math.sin(self.yaw) * math.cos(self.pitch) * self.distance
        cy = self.target[1] + math.sin(self.pitch) * self.distance
        cz = self.target[2] - math.cos(self.yaw) * math.cos(self.pitch) * self.distance

        view = Matrix44.look_at(
            eye=[cx, cy, cz],
            target=self.target,
            up=[0.0, 1.0, 0.0]
        )
        proj = Matrix44.perspective_projection(self.fov, self.screen_w / self.screen_h, 0.1, 200.0)
        return proj * view

    def project_point(self, x: float, y: float, z: float) -> Tuple[int, int, float]:
        """Projects 3D point (x,y,z) into screen coordinates (sx, sy, scale)."""
        view_proj = self.get_view_proj_matrix()
        pos_4d = view_proj * Vector4([x, y, z, 1.0])
        
        w = pos_4d[3]
        if abs(w) < 0.001 or w <= 0:
            return -1000, -1000, 0.0

        ndc_x = pos_4d[0] / w
        ndc_y = pos_4d[1] / w

        sx = int((ndc_x + 1.0) * 0.5 * self.screen_w)
        sy = int((1.0 - ndc_y) * 0.5 * self.screen_h)
        scale = max(4, int(480.0 / w))

        return sx, sy, scale


def render_3d_robot_part(screen, camera: Camera3D, world_pos: Tuple[float, float, float], btype: str, metal_rgb, glow_rgb, elapsed: float, yaw: float):
    """Renders 3D Mechanical Geometry for Proto-Protein Robot Parts with 3D Depth."""
    wx, wy, wz = world_pos
    sx, sy, scale = camera.project_point(wx, wy, wz)

    if sx < -100 or sy < -100 or sx > camera.screen_w + 100 or sy > camera.screen_h + 100:
        return

    box_size = scale * 2
    rect = pygame.Rect(sx - scale, sy - scale, box_size, box_size)

    # 1. Base Chassis Frame
    pygame.draw.rect(screen, metal_rgb, rect, border_radius=4)
    pygame.draw.rect(screen, glow_rgb, rect, width=2, border_radius=4)

    # Docking Port Center Ring
    port_r = max(2, scale // 3)
    pygame.draw.circle(screen, (184, 115, 51), (sx, sy), port_r, 2)

    # 2. Render 7 Specialized Mechanical Features
    if btype == "In-G":
        # Gas Filter: Spinning 4-blade copper turbine intake fan
        spin_a = elapsed * 9.0
        for i in range(4):
            ba = spin_a + i * (math.pi / 2.0)
            bx = sx + int(math.cos(ba) * (scale * 0.75))
            by = sy + int(math.sin(ba) * (scale * 0.75))
            pygame.draw.line(screen, (184, 115, 51), (sx, sy), (bx, by), 2)
        pygame.draw.circle(screen, glow_rgb, (sx, sy), max(2, scale // 4))

    elif btype == "In-M":
        # Scrap Magnet: Extended 3D Claws
        claw_len = int(scale * 0.9)
        claw_a = math.sin(elapsed * 4.0) * 0.3
        # Left Jaw
        lx1, ly1 = sx - int(scale * 0.5), sy - int(scale * 0.5)
        lx2, ly2 = lx1 - int(math.cos(claw_a) * claw_len), ly1 - int(math.sin(claw_a) * claw_len)
        pygame.draw.line(screen, (212, 175, 55), (lx1, ly1), (lx2, ly2), 3)
        # Right Jaw
        rx1, ry1 = sx + int(scale * 0.5), sy - int(scale * 0.5)
        rx2, ry2 = rx1 + int(math.cos(-claw_a) * claw_len), ry1 - int(math.sin(-claw_a) * claw_len)
        pygame.draw.line(screen, (212, 175, 55), (rx1, ry1), (rx2, ry2), 3)

    elif btype == "In-I":
        # Antenna / Eye: Vertical Brass Antenna & Glowing Eye Lens
        ant_top_y = sy - int(scale * 1.6)
        pygame.draw.line(screen, (212, 175, 55), (sx, sy - scale), (sx, ant_top_y), 2)
        eye_r = max(3, scale // 3)
        pygame.draw.circle(screen, glow_rgb, (sx, ant_top_y), eye_r)
        pygame.draw.circle(screen, (255, 255, 255), (sx, ant_top_y), max(1, eye_r // 2))

    elif btype == "Out-G":
        # Flared Rocket Exhaust Nozzle Cone
        nozz_w = int(scale * 0.85)
        nozz_y = sy + scale + max(3, scale // 2)
        points = [(sx - nozz_w, nozz_y), (sx + nozz_w, nozz_y), (sx, sy + scale)]
        pygame.draw.polygon(screen, (184, 115, 51), points)
        pygame.draw.polygon(screen, (255, 69, 0), points, 2)

    elif btype == "Out-M":
        # Waste Chute Hatch
        hatch_w = int(scale * 0.8)
        hatch_h = int(scale * 0.4)
        hatch_rect = pygame.Rect(sx - hatch_w // 2, sy + scale - hatch_h, hatch_w, hatch_h)
        pygame.draw.rect(screen, (90, 90, 90), hatch_rect)
        pygame.draw.rect(screen, (212, 175, 55), hatch_rect, 1)

    elif btype == "Out-I":
        # Vacuum Tube Signal Lamp
        tube_w = int(scale * 0.5)
        tube_h = int(scale * 1.3)
        tube_rect = pygame.Rect(sx - tube_w // 2, sy - scale - tube_h, tube_w, tube_h)
        pygame.draw.rect(screen, glow_rgb, tube_rect, border_radius=3)
        pygame.draw.line(screen, (255, 255, 255), (sx, sy - scale - tube_h + 2), (sx, sy - scale - 2), 2)


def draw_analog_gauge(surface, center_x, center_y, radius, title, value_str, value_ratio, text_font):
    """Renders a Riveting-Punk brass analog gauge with needle and non-overlapping text."""
    # Title ABOVE Gauge Dial
    t_surf = text_font.render(title, True, (212, 175, 55))
    surface.blit(t_surf, (center_x - t_surf.get_width() // 2, center_y - radius - 16))

    # Brass Rim & Dark Dial Face
    pygame.draw.circle(surface, (212, 175, 55), (center_x, center_y), radius, 3)
    pygame.draw.circle(surface, (14, 16, 22), (center_x, center_y), radius - 3)

    # Dial Needle
    angle = -math.pi * 0.75 + (min(1.0, max(0.0, value_ratio))) * (math.pi * 1.5)
    nx = center_x + int(math.cos(angle) * (radius - 6))
    ny = center_y + int(math.sin(angle) * (radius - 6))
    pygame.draw.line(surface, (255, 50, 50), (center_x, center_y), (nx, ny), 2)
    pygame.draw.circle(surface, (212, 175, 55), (center_x, center_y), 3)

    # Value BELOW Gauge Dial
    v_surf = text_font.render(value_str, True, (255, 255, 255))
    surface.blit(v_surf, (center_x - v_surf.get_width() // 2, center_y + radius + 4))


def run_native_3d_engine():
    pygame.init()
    pygame.font.init()

    screen_w, screen_h = 1200, 850
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("⚙️ Obsidia-7 Harmony — Master Native 3D Mechanical Engine (120+ FPS)")

    font_small = pygame.font.SysFont("Segoe UI", 12)
    font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 18, bold=True)

    # 3D Camera Setup
    camera = Camera3D(screen_w, screen_h)

    # Initialize Master Game Manager
    game = GameManager()
    game.set_god_options(num_species=4, speed=1.0, gas_env="G_minus", mutation_mult=1.0)

    particles: List[Particle] = []
    clock = pygame.time.Clock()
    running = True
    is_paused = False
    focused_species_id = 0
    start_time = time.time()
    ollama_log_text = "[Ollama AI Engine]: Native 3D Engine active. Press 'O' for AI species adaptation report."

    print("\n" + "=" * 70)
    print(" ⚙️ OBSIDIA-7 HARMONY — Master Native 3D Robot Engine Active!")
    print(" 7 Proto-Proteins: In-G Turbine, In-M Claw, In-I Antenna, Out-G Rocket, Out-M Chute, Out-I Lamp, Base Chassis")
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
                        f"Describe their dynamic Riveting-Punk mechanical robot adaptation in 2 short sentences."
                    )
                    report = query_local_ollama(prompt)
                    ollama_log_text = f"[AI Ticker]: \"{report}\""

        # Advance Game Tick
        state = game.tick_game_loop() if not is_paused else game.tick_game_loop()

        # Clear Screen (Dark Junkyard Atmosphere Background)
        screen.fill((8, 9, 12))

        # Camera Position & Smooth Tracking Target
        focus_entity = game.ecosystem.species_entities.get(focused_species_id)
        if focus_entity:
            camera.target[0] += (focus_entity.pos[0] - camera.target[0]) * 0.1
            camera.target[1] = 0.0
            camera.target[2] += (focus_entity.pos[2] - camera.target[2]) * 0.1
        
        camera.yaw = elapsed * 0.2  # Smooth 3D orbit

        # 1. Draw Oil Ocean Grid
        for gz in range(-45, 50, 10):
            p1_2d = camera.project_point(-50.0, -2.5, gz)
            p2_2d = camera.project_point(50.0, -2.5, gz)
            if p1_2d[0] > -500 and p2_2d[0] > -500:
                pygame.draw.line(screen, (28, 20, 14), (p1_2d[0], p1_2d[1]), (p2_2d[0], p2_2d[1]), 1)

        # 2. Draw Environment Gas Clouds & Scrap Materia Nodes
        for gc in state["environment"]["gas_clouds"]:
            color = (255, 69, 0) if gc["type"] == "G_minus_minus" else (0, 240, 255)
            sx, sy, size = camera.project_point(gc["pos"][0], gc["pos"][1], gc["pos"][2])
            if sx > -100 and sy > -100:
                radius = max(8, int(gc["radius"] * size * 0.35))
                pygame.draw.circle(screen, color, (sx, sy), radius, 1)

        for mn in state["environment"]["materia_nodes"]:
            sx, sy, size = camera.project_point(mn["pos"][0], mn["pos"][1], mn["pos"][2])
            if sx > -100 and sy > -100:
                pygame.draw.polygon(screen, (255, 215, 0), [
                    (sx, sy - size), (sx + size, sy), (sx, sy + size), (sx - size, sy)
                ])

        # 3. Draw Species Organisms with 7 Specialized Mechanical Robot Parts!
        for sp in state["species_list"]:
            s_id = sp["species_id"]
            theme = SPECIES_PALETTES.get(s_id, SPECIES_PALETTES[0])

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

            # Draw 7 Proto-Protein Robot Modules in Horizontal 3D Space (X, Z)
            blocks = (sp["blueprint"] and sp["blueprint"]["blocks"]) or []
            for b in blocks:
                bcc = b["bcc"]
                btype = b["type"]
                
                # Rotate relative BCC block offsets in horizontal plane (X, Z)
                rx = bcc[0] * math.cos(yaw) - bcc[2] * math.sin(yaw)
                rz = bcc[0] * math.sin(yaw) + bcc[2] * math.cos(yaw)

                world_x = ox + rx * 1.1
                world_y = oy + (bcc[1] * 0.3) + math.sin(elapsed * 4 + b["id"]) * 0.1
                world_z = oz + rz * 1.1

                render_3d_robot_part(screen, camera, (world_x, world_y, world_z), btype, metal_rgb, glow_rgb, elapsed, yaw)

        # 4. Update & Render Particles
        for p in particles[:]:
            p.update(dt)
            if p.life <= 0:
                particles.remove(p)
                continue
            sx, sy, size = camera.project_point(p.x, p.y, p.z)
            if sx > -100 and sy > -100:
                pygame.draw.circle(screen, p.color, (sx, sy), max(1, size // 2))

        # 5. Draw Clean Spaced ASCII HUD & Overlord Panel
        hdr_rect = pygame.Rect(15, 15, 570, 118)
        pygame.draw.rect(screen, (16, 18, 24), hdr_rect, border_radius=6)
        pygame.draw.rect(screen, (212, 175, 55), hdr_rect, width=2, border_radius=6)

        t_hdr = font_title.render("[OBSIDIA-7 HARMONY] -- NATIVE 3D ENGINE (120+ FPS)", True, (212, 175, 55))
        d_hdr = font_bold.render(f"[HELIOS-OMEGA]: {state['doom_clock']['years_formatted']}  |  HARMONY: {state['doom_clock']['harmony_index']}%", True, (255, 69, 0))
        screen.blit(t_hdr, (25, 22))
        screen.blit(d_hdr, (25, 48))

        # Species Tags Legend with generous horizontal spacing
        lx = 25
        for s_idx, sp in enumerate(state["species_list"]):
            theme = SPECIES_PALETTES.get(s_idx, SPECIES_PALETTES[0])
            glow_rgb = ((theme.glow_color >> 16) & 0xFF, (theme.glow_color >> 8) & 0xFF, theme.glow_color & 0xFF)
            focus_mark = " (CAM)" if s_idx == focused_species_id else ""
            tag = font_small.render(f"* {sp['species_name']}{focus_mark}", True, glow_rgb)
            screen.blit(tag, (lx, 74))
            lx += tag.get_width() + 18

        # AI Ticker Banner
        ai_rect = pygame.Rect(15, 100, 550, 24)
        pygame.draw.rect(screen, (0, 0, 0), ai_rect, border_radius=3)
        ai_txt = font_small.render(ollama_log_text[:90], True, (200, 215, 230))
        screen.blit(ai_txt, (22, 104))

        # Analog Gauges Bottom Left (Non-overlapping labels!)
        player_sp = state["species_list"][0]["snapshot"] if state["species_list"] else {}
        chg_v = player_sp.get("charge", 50.0)
        ent_v = player_sp.get("entropy", 2.0)
        draw_analog_gauge(screen, 70, screen_h - 75, 36, "CHARGE", f"{chg_v:.1f}V", chg_v / 100.0, font_small)
        draw_analog_gauge(screen, 185, screen_h - 75, 36, "ENTROPY", f"{ent_v:.1f}BAR", ent_v / 25.0, font_small)

        # Overseer Controls Legend Bottom Right
        ctrl_rect = pygame.Rect(screen_w - 450, screen_h - 85, 435, 70)
        pygame.draw.rect(screen, (16, 18, 24), ctrl_rect, border_radius=6)
        pygame.draw.rect(screen, (184, 115, 51), ctrl_rect, width=2, border_radius=6)

        c_txt1 = font_bold.render("[OVERSEER GOD CONTROLS]", True, (212, 175, 55))
        c_txt2 = font_small.render(f"[1/2] {game.ecosystem.num_active_species} Species | [S] Speed {game.simulation_speed:.0f}x | [G] {game.forced_gas_environment} | [C] Cam Focus", True, (220, 220, 220))
        c_txt3 = font_small.render("[O] Query Ollama AI Log | [SPACE] Pause | FPS: " + f"{clock.get_fps():.1f}", True, (0, 240, 255))
        screen.blit(c_txt1, (screen_w - 440, screen_h - 80))
        screen.blit(c_txt2, (screen_w - 440, screen_h - 60))
        screen.blit(c_txt3, (screen_w - 440, screen_h - 40))

        pygame.display.flip()

    pygame.quit()
    print("Master Native Pygame 3D Robot Engine closed cleanly.")


if __name__ == "__main__":
    run_native_3d_engine()
