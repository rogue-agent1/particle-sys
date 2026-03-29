#!/usr/bin/env python3
"""particle_sys - Particle system."""
import sys,argparse,json,random,math
class Particle:
    def __init__(self,x=0,y=0,vx=0,vy=0,life=1.0):self.x=x;self.y=y;self.vx=vx;self.vy=vy;self.life=life
    def update(self,dt,gravity=0.1):self.vy+=gravity*dt;self.x+=self.vx*dt;self.y+=self.vy*dt;self.life-=dt*0.5
    def alive(self):return self.life>0
class Emitter:
    def __init__(self,x=0,y=0,rate=10,spread=1.0,speed=2.0):
        self.x=x;self.y=y;self.rate=rate;self.spread=spread;self.speed=speed;self.particles=[]
    def emit(self):
        for _ in range(self.rate):
            angle=random.uniform(-self.spread,self.spread)-math.pi/2
            speed=random.uniform(self.speed*0.5,self.speed)
            self.particles.append(Particle(self.x,self.y,math.cos(angle)*speed,math.sin(angle)*speed))
    def step(self,dt=0.1):
        self.emit()
        for p in self.particles:p.update(dt)
        self.particles=[p for p in self.particles if p.alive()]
def main():
    p=argparse.ArgumentParser(description="Particle system")
    p.add_argument("--steps",type=int,default=50);p.add_argument("--rate",type=int,default=5)
    p.add_argument("--seed",type=int,default=42)
    args=p.parse_args()
    random.seed(args.seed)
    em=Emitter(rate=args.rate)
    stats=[]
    for i in range(args.steps):
        em.step()
        stats.append({"step":i,"active":len(em.particles),"avg_life":round(sum(p.life for p in em.particles)/max(1,len(em.particles)),3)})
    print(json.dumps({"steps":args.steps,"peak_particles":max(s["active"] for s in stats),"final_particles":stats[-1]["active"],"sample":stats[::max(1,args.steps//10)]},indent=2))
if __name__=="__main__":main()
