from ursina import *

class Ankheg(Entity):
    def __init__(self):
        super().__init__(
            model = '../assets/monsters/ankheg.obj',
            scale = 0.3,
            texture = '../assets/monsters/ankheg',
            color = color.rgb(150,150,150),
            collider = 'box',
            double_sided = True
            )


if __name__ == '__main__':
    app = Ursina()
    Ankheg()
    EditorCamera()
    app.run()