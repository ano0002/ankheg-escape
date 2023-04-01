from ursina import *

class Ankheg(Entity):
    def __init__(self,player,world, **kwargs) -> None:
        super().__init__(
            model = '../assets/monsters/ankheg.obj',
            scale = 0.3,
            texture = '../assets/monsters/ankheg',
            color = color.rgb(150,150,150),
            collider = 'box',
            double_sided = True,
            enabled = False,
            **kwargs
            )
        self.world=world
        self.player = player
        self.eyes = Entity(model="quad",scale = (0.5,0.5),texture = "../assets/monsters/eyes.jpg",position = (0,0,0),billboard = True)

    def play_screamer(self) -> None:
        self.enable()
        self.world.monster_scream.play()
        self.player.mode = 2
        self.position = (0,-4.4,25)
        AmbientLight(color=(1, 1, 1, 1.0))
        self.animate_position((0,-10,1.5), duration = .2)
        camera.parent = scene
        camera.position = (0,-5,-4)
        camera.rotation = (5,2,0)
        camera.shake(duration = 1, magnitude = 1)

    def walk(self) -> None:
        self.eyes.animate_position((0,0,0), duration = 1)
        invoke(self.world.ankheg_growl.play,delay = 1)
        invoke(self.walk,delay = 1.5)

    def reset(self) -> None:
        self.eyes.disable()
        invoke(self.disable, delay=0.1)
        invoke(Func(setattr,self,"position", (0,-4.4,25)),delay = 0.2)

if __name__ == '__main__':
    app = Ursina()
    Ankheg()
    EditorCamera()
    app.run()