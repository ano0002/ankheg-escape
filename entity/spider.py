from ursina import *
from direct.actor.Actor import Actor


class Spider(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.actor = Actor("./assets/monsters/animated_spider (1).glb")

        self.actor.reparentTo(self)
        self.actor.set_scale(0.3)
        self.actor.set_hpr(0,-90, 0)
        self.actor.loop("Armature|run")
        self.reset_position = self.position
        self.disable()
    
    def run(self,position):
        self.enable()
        self.fade_in(duration=0.1)
        self.animate_position(position, duration=2.3, curve=curve.linear)
        self.look_at(position)
    
    def reset(self):
        self.fade_out(duration=0.1)
        invoke(self.disable, delay=0.1)
        self.position = self.reset_position
    

if __name__ == '__main__':
        
    app = Ursina(borderless=False)
    EditorCamera()
    camera.clip_plane_far = 1000
    camera.clip_plane_near = 0.001
    spiders = [Spider(position=(i, j, k)) for i in range(0, 2) for j in range(0, 2) for k in range(0, 2)]
    
    def update():
        random.choice(spiders).run(camera.position)
    app.run()
