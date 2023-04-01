from ursina import *
from ursina.shaders import unlit_shader

class Spotlight(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model="../assets/post/spotlight.obj",
            color=color.black,
            rotation= Vec3(0,90,0),
            double_sided=True,
            **kwargs
        )
        self.light_cone = Entity(parent=self, model='../assets/flashlight/lightcone.obj', color=color.white50,\
                                 position=(0,1,0),rotation = Vec3(80,-90,0),scale=100,shader = unlit_shader)
        

if __name__ == '__main__':
    app = Ursina()
    spotlight = Spotlight()
    EditorCamera()
    app.run()