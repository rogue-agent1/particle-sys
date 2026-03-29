#!/usr/bin/env python3
"""particle_sys - Particle system with emitters, forces, and lifecycle."""
import sys, math, random

class Particle:
    def __init__(self, x, y, vx, vy, life=1.0, size=1.0, color=(255,255,255)):
        self.x = x; self.y = y; self.vx = vx; self.vy = vy
        self.life = life; self.max_life = life; self.size = size; self.color = color
        self.alive = True
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life <= 0:
            self.alive = False

class Emitter:
    def __init__(self, x, y, rate=10, spread=math.pi/4, speed=50, life=2.0, direction=math.pi/2):
        self.x = x; self.y = y; self.rate = rate; self.spread = spread
        self.speed = speed; self.life = life; self.direction = direction
        self.accumulator = 0
    def emit(self, dt, rng):
        self.accumulator += self.rate * dt
        particles = []
        while self.accumulator >= 1:
            angle = self.direction + rng.uniform(-self.spread/2, self.spread/2)
            speed = self.speed * rng.uniform(0.5, 1.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particles.append(Particle(self.x, self.y, vx, vy, self.life * rng.uniform(0.5, 1.5)))
            self.accumulator -= 1
        return particles

class ParticleSystem:
    def __init__(self, seed=None):
        self.particles = []
        self.emitters = []
        self.forces = []
        self.rng = random.Random(seed)
    def add_emitter(self, emitter):
        self.emitters.append(emitter)
    def add_force(self, fx, fy):
        self.forces.append((fx, fy))
    def update(self, dt):
        for e in self.emitters:
            self.particles.extend(e.emit(dt, self.rng))
        for p in self.particles:
            for fx, fy in self.forces:
                p.vx += fx * dt
                p.vy += fy * dt
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]
    @property
    def count(self):
        return len(self.particles)

def test():
    ps = ParticleSystem(seed=42)
    ps.add_emitter(Emitter(0, 0, rate=100, life=1.0))
    ps.add_force(0, -9.81)  # gravity
    for _ in range(100):
        ps.update(0.016)
    assert ps.count > 0
    assert ps.count < 200  # particles die
    # all alive particles should have life > 0
    assert all(p.alive and p.life > 0 for p in ps.particles)
    # particles should have moved
    assert any(p.y != 0 for p in ps.particles)
    # without emitter, all die
    ps2 = ParticleSystem(seed=42)
    ps2.particles = [Particle(0, 0, 0, 0, life=0.1)]
    for _ in range(20):
        ps2.update(0.016)
    assert ps2.count == 0
    print("OK: particle_sys")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: particle_sys.py test")
