#!/usr/bin/env python3
"""2D particle system with emitters, forces, and rendering."""
import sys, random, math

class Particle:
    def __init__(self, x, y, vx, vy, life=1.0, color=0):
        self.x,self.y,self.vx,self.vy = x,y,vx,vy
        self.life,self.max_life,self.color = life,life,color
    def alive(self): return self.life > 0

class ParticleSystem:
    def __init__(self, x, y, rate=10, spread=30, speed=3, life=2.0):
        self.x,self.y,self.rate = x,y,rate
        self.spread,self.speed,self.life = spread,speed,life
        self.particles = []; self.gravity = 2.0
    def emit(self, dt):
        n = int(self.rate * dt + random.random())
        for _ in range(n):
            angle = math.radians(-90 + random.uniform(-self.spread, self.spread))
            spd = self.speed * random.uniform(0.5, 1.5)
            self.particles.append(Particle(self.x, self.y, math.cos(angle)*spd, math.sin(angle)*spd, self.life))
    def update(self, dt):
        self.emit(dt)
        for p in self.particles:
            p.vy += self.gravity*dt; p.x += p.vx*dt; p.y += p.vy*dt; p.life -= dt
        self.particles = [p for p in self.particles if p.alive()]
    def render(self, w=40, h=20):
        grid = [['·']*w for _ in range(h)]
        chars = "█▓▒░"
        for p in self.particles:
            ix, iy = int(p.x), int(p.y)
            if 0<=ix<w and 0<=iy<h:
                age = 1 - p.life/p.max_life
                grid[iy][ix] = chars[min(int(age*4), 3)]
        for row in grid: print("".join(row))

def main():
    random.seed(42); ps = ParticleSystem(20, 2, rate=20, spread=40, speed=5, life=1.5)
    for _ in range(30): ps.update(0.05)
    print(f"Particles: {len(ps.particles)}")
    ps.render()

if __name__ == "__main__": main()
