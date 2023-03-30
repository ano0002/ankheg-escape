from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import unlit_shader


class Spider(Entity):
    def __init__(self,target, **kwargs):
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
    
    def run(self, position = None):
        self.enable()
        self.fade_in(duration=0.1)
        if not position:
            position = self.target
        self.animate_position(position, duration=2.3, curve=curve.linear)
        self.look_at(position)
        self.rotation = (0, self.rotation_y, 0)

    def reset(self):
        self.fade_out(duration=0.1)
        invoke(self.disable, delay=0.1)
        invoke(Func(setattr,self,"position",self.reset_position),delay = 0.2)

    

if __name__ == '__main__':
        
    app = Ursina(borderless=False)
    EditorCamera()
    camera.clip_plane_far = 1000
    camera.clip_plane_near = 0.001
    spiders = [Spider(position=(i, j, k)) for i in range(0, 2) for j in range(0, 2) for k in range(0, 2)]
    
    def update():
        random.choice(spiders).run(camera.position)
    app.run()
