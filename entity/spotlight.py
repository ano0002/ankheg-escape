from ursina import *
from ursina.shaders import unlit_shader

class Spotlight(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model="../assets/post/spotlight.obj",
            color=color.black,
            double_sided=True,
            scale = 0.1,
            **kwargs
        )
        self.light_cone = Entity(parent=self, model='../assets/flashlight/lightcone.obj', color=color.white50,\
                                 position=(0,1,0),rotation = Vec3(-100,-90,0),scale=100,shader = unlit_shader,
                                 double_sided=True,collider= "mesh")
    
    
    def toggle(self):
        self.light_cone.enabled = not self.light_cone.enabled
    
    

if __name__ == '__main__':
    app = Ursina()
    spotlight = Spotlight()
    EditorCamera()
    app.run()