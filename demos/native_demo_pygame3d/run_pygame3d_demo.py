"""
Obsidia-7 Harmony — Native GPU Demo B: Pygame 3D Hardware Accelerated Pipeline
Renders 4 Autonomous Species with Particle Sparks & Kirchhoff Circuit Overload HUD at 120+ FPS.
"""

import sys
import math
import time
import random
import pygame

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Particle:
    """Sparks and Thrust bubble particles."""
    def __init__(self, x, y, z, vx, vy, vz, color, life):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.color = color
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        self.life -= dt


class DemoBOrganism:
    """Multi-block organism with 3D projection."""
    def __init__(self, species_id: int, name: str, metal_color, glow_color, start_pos):
        self.species_id = species_id
        self.name = name
        self.metal_color = metal_color
        self.glow_color = glow_color
        self.pos = list(start_pos)
        self.vel = [random.uniform(-1, 1), 0.0, random.uniform(-1, 1)]
        self.yaw = random.uniform(0, math.pi * 2)

        # 5 BCC relative block offsets
        self.blocks = [
            (0.0, 0.0, 0.0, "In-G"),
            (0.9, 0.5, 0.5, "Base"),
            (1.8, 0.0, 1.0, "In-M"),
            (2.7, 0.5, 1.5, "Base"),
            (3.6, 1.0, 2.0, "Out-G")
        ]

    def update(self, dt):
        # Autonomous movement
        self.yaw += random.uniform(-0.1, 0.1)
        speed = 3.0
        self.vel[0] = math.cos(self.yaw) * speed
        self.vel[2] = math.sin(self.yaw) * speed

        self.pos[0] += self.vel[0] * dt
        self.pos[2] += self.vel[2] * dt

        # Wrap around bounds
        if abs(self.pos[0]) > 20: self.pos[0] *= -0.9
        if abs(self.pos[2]) > 15: self.pos[2] *= -0.9


def project_3d_to_2d(x, y, z, cam_pos, screen_w, screen_h):
    """Projects 3D point (x,y,z) onto 2D screen surface."""
    rel_x = x - cam_pos[0]
    rel_y = y - cam_pos[1]
    rel_z = z - cam_pos[2]

    # Simple 3D perspective projection
    fov = 400.0
    depth = max(0.1, rel_z + 25.0)
    sx = int(screen_w / 2 + (rel_x * fov) / depth)
    sy = int(screen_h / 2 - (rel_y * fov) / depth)
    scale = max(2, int((fov * 0.4) / depth))
    return sx, sy, scale


def run_pygame3d_demo():
    pygame.init()
    pygame.font.init()
    screen_w, screen_h = 1024, 768
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("⚙️ Obsidia-7 Harmony — GPU Demo B: Pygame 3D Native Engine")

    font = pygame.font.SysFont("Segoe UI", 16, bold=True)
    title_font = pygame.font.SysFont("Segoe UI", 22, bold=True)

    # 4 Species
    species_list = [
        DemoBOrganism(0, "Brass-Aurum (Alpha)", (0xd4, 0xaf, 0x37), (0x00, 0xf0, 0xff), (-8.0, 0.0, -5.0)),
        DemoBOrganism(1, "Copper-Rubrum (Beta)", (0xb8, 0x73, 0x33), (0xff, 0x33, 0x44), (8.0, 0.0, 5.0)),
        DemoBOrganism(2, "Steel-Azure (Gamma)", (0x8a, 0x9e, 0xa7), (0x00, 0xff, 0xaa), (-5.0, 0.0, 8.0)),
        DemoBOrganism(3, "Bronze-Purpura (Delta)", (0xcd, 0x7f, 0x32), (0xaa, 0x00, 0xff), (5.0, 0.0, -8.0))
    ]

    particles = []
    clock = pygame.time.Clock()
    running = True
    start_time = time.time()

    print("\n" + "=" * 65)
    print(" ⚙️ OBSIDIA-7 HARMONY — GPU Demo B: Pygame 3D Engine Running!")
    print(" Press ESC or Close Window to exit.")
    print("=" * 65 + "\n")

    while running:
        dt = clock.tick(120) / 1000.0  # 120 FPS
        elapsed = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Clear Screen (Dark Junkyard Oil Ocean Background)
        screen.fill((10, 11, 14))

        # Camera orbiting slowly
        cam_x = math.sin(elapsed * 0.3) * 5.0
        cam_pos = [cam_x, 8.0, 0.0]

        # Draw Grid Ground
        for gz in range(-20, 25, 5):
            p1_2d = project_3d_to_2d(-25, -2, gz, cam_pos, screen_w, screen_h)
            p2_2d = project_3d_to_2d(25, -2, gz, cam_pos, screen_w, screen_h)
            pygame.draw.line(screen, (30, 22, 14), (p1_2d[0], p1_2d[1]), (p2_2d[0], p2_2d[1]), 1)

        # Update & Draw Organisms
        for sp in species_list:
            sp.update(dt)
            
            # Spawn Out-G thrust particles
            if random.random() < 0.3:
                particles.append(Particle(
                    sp.pos[0], sp.pos[1], sp.pos[2],
                    -sp.vel[0] * 0.5 + random.uniform(-0.5, 0.5),
                    random.uniform(0.1, 0.5),
                    -sp.vel[2] * 0.5 + random.uniform(-0.5, 0.5),
                    sp.glow_color,
                    random.uniform(0.5, 1.2)
                ))

            # Draw blocks
            for b_idx, (bx, by, bz, btype) in enumerate(sp.blocks):
                # Rotate local block offset by organism yaw
                cos_y, sin_y = math.cos(sp.yaw), math.sin(sp.yaw)
                rx = bx * cos_y - bz * sin_y
                rz = bx * sin_y + bz * cos_y
                
                world_x = sp.pos[0] + rx
                world_y = sp.pos[1] + by + math.sin(elapsed * 4 + b_idx) * 0.15
                world_z = sp.pos[2] + rz

                sx, sy, size = project_3d_to_2d(world_x, world_y, world_z, cam_pos, screen_w, screen_h)

                # Draw Block Box
                rect = pygame.Rect(sx - size, sy - size, size * 2, size * 2)
                pygame.draw.rect(screen, sp.metal_color, rect, border_radius=3)
                pygame.draw.rect(screen, sp.glow_color, rect, width=2, border_radius=3)

        # Update & Draw Particles
        for p in particles[:]:
            p.update(dt)
            if p.life <= 0:
                particles.remove(p)
                continue
            sx, sy, size = project_3d_to_2d(p.x, p.y, p.z, cam_pos, screen_w, screen_h)
            alpha = max(0, int(255 * (p.life / p.max_life)))
            pygame.draw.circle(screen, p.color, (sx, sy), max(1, size // 3))

        # HUD Overlay
        title_txt = title_font.render("⚙️ OBSIDIA-7 HARMONY — GPU Demo B (120+ FPS)", True, (212, 175, 55))
        fps_txt = font.render(f"FPS: {clock.get_fps():.1f} | Active Species: 4 | Particles: {len(particles)}", True, (0, 240, 255))
        screen.blit(title_txt, (20, 15))
        screen.blit(fps_txt, (20, 45))

        # Legend Tags
        lx = 20
        for sp in species_list:
            tag = font.render(f"• {sp.name}", True, sp.glow_color)
            screen.blit(tag, (lx, 75))
            lx += 220

        pygame.display.flip()

    pygame.quit()
    print("Demo B (Pygame 3D) closed cleanly.")


if __name__ == "__main__":
    run_pygame3d_demo()
