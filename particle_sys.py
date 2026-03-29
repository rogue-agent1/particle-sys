#!/usr/bin/env python3
"""2D particle system with emitters, forces, and rendering."""
import sys,math,random,time

class Particle:
    def __init__(self,x,y,vx=0,vy=0,life=2.0,size=1,color=None):
        self.x=x;self.y=y;self.vx=vx;self.vy=vy;self.life=life;self.max_life=life
        self.size=size;self.color=color or(255,200,50);self.alive=True

class Emitter:
    def __init__(self,x,y,rate=10,spread=0.5,speed=3,life=2.0):
        self.x=x;self.y=y;self.rate=rate;self.spread=spread
        self.speed=speed;self.life=life;self.angle=math.pi/2;self.accum=0
    def emit(self,dt):
        self.accum+=self.rate*dt;particles=[]
        while self.accum>=1:
            self.accum-=1;a=self.angle+random.uniform(-self.spread,self.spread)
            s=self.speed*random.uniform(0.5,1.5)
            particles.append(Particle(self.x,self.y,math.cos(a)*s,-math.sin(a)*s,
                self.life*random.uniform(0.5,1.5)))
        return particles

class ParticleSystem:
    def __init__(self):
        self.particles=[];self.emitters=[];self.gravity=(0,2);self.wind=(0,0)
    def add_emitter(self,e):self.emitters.append(e)
    def update(self,dt):
        for e in self.emitters:self.particles.extend(e.emit(dt))
        for p in self.particles:
            p.vx+=self.gravity[0]*dt+self.wind[0]*dt
            p.vy+=self.gravity[1]*dt+self.wind[1]*dt
            p.x+=p.vx*dt;p.y+=p.vy*dt;p.life-=dt
            if p.life<=0:p.alive=False
        self.particles=[p for p in self.particles if p.alive]
    def render_ascii(self,w=60,h=25):
        grid=[[" "]*w for _ in range(h)]
        chars="·∘○●"
        for p in self.particles:
            px,py=int(p.x),int(p.y)
            if 0<=px<w and 0<=py<h:
                age=1-p.life/p.max_life
                ci=min(int(age*len(chars)),len(chars)-1)
                grid[py][px]=chars[ci]
        return "\n".join("".join(r) for r in grid)

def main():
    print("=== Particle System ===\n")
    ps=ParticleSystem();ps.gravity=(0,5)
    ps.add_emitter(Emitter(30,20,rate=50,spread=0.8,speed=8,life=1.5))
    ps.add_emitter(Emitter(15,22,rate=30,spread=0.3,speed=6,life=1.0))
    for step in range(20):
        ps.update(0.1)
        if step%5==0:
            print(f"Step {step}: {len(ps.particles)} particles")
            print(ps.render_ascii());print()
    print(f"Final: {len(ps.particles)} active particles")

if __name__=="__main__":main()
