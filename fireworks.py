import pygame
import random
import os
from moviepy.editor import ImageSequenceClip

BLACK = (0, 0, 0)

pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

done = False
clock = pygame.time.Clock()

fireworks = []
particles = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

class Firework:
    def __init__(self):
        self.x = random.uniform(0, size[0])
        self.y = size[1]
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-15, -5)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.trail = []

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail, 2)

frame_rate = 60
frame_duration = 1.0 / frame_rate
frames = []

frame_count = 0
os.makedirs("frames", exist_ok=True)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if random.random() < 0.1:
        fireworks.append(Firework())

    for f in fireworks[:]:
        f.update()
        if f.vy > 0:
            fireworks.remove(f)
            for _ in range(50):
                particles.append(Particle(f.x, f.y, f.color))

    for p in particles[:]:
        p.update()
        if p.y > size[1]:
            particles.remove(p)

    screen.fill(BLACK)

    for f in fireworks:
        f.draw(screen)

    for p in particles:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(frame_rate)

    frame_path = f"frames/frame_{frame_count}.jpg"
    pygame.image.save(screen, frame_path)
    frames.append(frame_path)
    frame_count += 1

pygame.quit()

clip = ImageSequenceClip(frames, fps=frame_rate)
clip.write_videofile("fireworks.mp4")

for frame in frames:
    os.remove(frame)
