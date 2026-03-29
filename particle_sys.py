#!/usr/bin/env python3
"""Particle System - Emit, update, and render particles with physics."""
import sys, random, math

class Particle:
    def __init__(self, x, y, vx, vy, life=1.0, color="*"):
        self.x=x;self.y=y;self.vx=vx;self.vy=vy;self.life=life;self.age=0;self.color=color
    def update(self, dt, gravity=9.8):
        self.vy += gravity * dt; self.x += self.vx * dt; self.y += self.vy * dt; self.age += dt
    @property
    def alive(self): return self.age < self.life

class Emitter:
    def __init__(self, x, y, rate=10, spread=1.0, speed=5.0, life=2.0):
        self.x=x;self.y=y;self.rate=rate;self.spread=spread;self.speed=speed;self.life=life;self.accum=0
    def emit(self, dt):
        self.accum += self.rate * dt; particles = []
        while self.accum >= 1:
            angle = random.uniform(-self.spread, self.spread) + math.pi/2
            spd = self.speed * random.uniform(0.5, 1.5)
            particles.append(Particle(self.x, self.y, math.cos(angle)*spd, -math.sin(angle)*spd, self.life))
            self.accum -= 1
        return particles

def simulate(emitter, steps=30, dt=0.1, width=60, height=20):
    particles = []; frames = []
    for step in range(steps):
        particles.extend(emitter.emit(dt))
        for p in particles: p.update(dt)
        particles = [p for p in particles if p.alive and 0<=p.x<width and 0<=p.y<height]
        grid = [["."]*width for _ in range(height)]
        for p in particles:
            r, c = int(p.y), int(p.x)
            if 0<=r<height and 0<=c<width:
                frac = 1 - p.age/p.life
                grid[r][c] = "*" if frac > 0.6 else "+" if frac > 0.3 else "."
        frames.append((step, len(particles), ["".join(r) for r in grid]))
    return frames

def main():
    random.seed(42)
    em = Emitter(30, 18, rate=20, spread=0.8, speed=15, life=1.5)
    frames = simulate(em, steps=15)
    print("=== Particle System ===\n")
    for step, count, grid in frames[::3]:
        print(f"Step {step} ({count} particles):")
        for row in grid: print(f"  {row}")
        print()

if __name__ == "__main__":
    main()
