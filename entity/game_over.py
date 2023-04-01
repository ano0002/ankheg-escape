from ursina import *

class GameOver(Entity):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.overlay = Entity(parent=camera.ui, model='quad', color=color.black, scale=(2,1), z=-1)
        self.text = Text("""GAME OVER""",
            scale=11, x=-.8, y=.4,z=-2,resolution = 1000,size = 0.8,color= color.red)
if __name__ == '__main__':
    app = Ursina()

    GameOver()

    app.run()
    