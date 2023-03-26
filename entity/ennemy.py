from ursina import *

class Ankheg(Entity):
    def __init__(self):
        super().__init__(
            model = 'ankheg',
            scale = 0.3,
            texture = 'ankheg',
            color = color.rgb(150,150,150),
            collider = 'box',
            )


if __name__ == '__main__':
    app = Ursina()
    Ankheg()
    EditorCamera()
    app.run()