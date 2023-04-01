from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import unlit_shader
import random

class Spider(Entity):
    def __init__(self,target,world, **kwargs) -> None:
        super().__init__(**kwargs)
        self.actor = Actor("./assets/monsters/animated_spider (1).glb")

        self.actor.reparentTo(self)
        self.actor.set_scale(0.3)
        self.actor.set_hpr(0,-90, 0)
        self.actor.loop("Armature|run")
        self.shader = unlit_shader
        self.reset_position = self.position
        self.disable()
        self.target = target
        self.world = world

    def run(self, position = None, duration = 2.3) -> None:
        self.enable()
        self.fade_in(duration=0.1)
        if not position:
            position = self.target
        self.animate_position(position, duration=duration, curve=curve.in_sine)
        self.look_at(position)
        self.rotation_y += 180
        self.rotation = (0, self.rotation_y, 0)

    def reset(self) -> None:
        self.fade_out(duration=0.1)
        invoke(self.disable, delay=0.1)
        invoke(Func(setattr,self,"position",self.reset_position),delay = 0.2)

    def update(self) -> None:
        if self.enabled :
            if self.world.player.light_cone.enabled :
                ray = raycast(self.position,(0,1,0))
                if ray.hit:
                    self.disable()

    def play_screamer(self) -> None:
        self.enable()
        self.world.spider_steps.play()
        self.world.player.mode = 2
        self.position = (0,-5.5,10)
        AmbientLight(color=(1, 1, 1, 1.0))
        self.animate_position((0,-5.5,-3), duration = 6,curve = curve.in_sine)
        for i in range(-10, 10):
            spider = Spider(position=(i/10, -5.5, 10),target = (i/10,-5.5,-3), world = self.world)
            invoke(Func(spider.run,duration=6), delay = random.random()*5)
            
        camera.parent = scene
        camera.position = (0,-5,-4)
        camera.rotation = (5,2,0)
        def scream(spider):
            spider.position = (0,-5.2,-3.5)
            spider.world.spider_hiss.position = (0,-5.2,-3)
            spider.world.spider_hiss.play()

            
        invoke(scream,self,delay = 6)


if __name__ == '__main__':

    app = Ursina(borderless=False)
    EditorCamera()
    camera.clip_plane_far = 1000
    camera.clip_plane_near = 0.001
    spiders = [Spider(position=(i, j, k)) for i in range(0, 2) for j in range(0, 2) for k in range(0, 2)]

    def update():
        random.choice(spiders).run(camera.position)
    app.run()
