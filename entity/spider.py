from ursina import *
from direct.actor.Actor import Actor
app = Ursina(borderless=False)


class Spider(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.actor = Actor("../assets/monsters/animated_spider (1).glb")

        self.actor.reparentTo(self)
        self.actor.set_scale(0.3)
        self.actor.set_hpr(0,-90, 0)
        self.actor.loop("Armature|run")

if __name__ == '__main__':
        
    EditorCamera()
    camera.clip_plane_far = 1000
    camera.clip_plane_near = 0.001
    for i in range(2):
        for j in range(2):
            for k in range(2):
                Spider(position=(i, j, k))
    app.run()
