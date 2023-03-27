from ursina import *

class Ankheg(Entity):
    def __init__(self,player, **kwargs):
        super().__init__(
            model = '../assets/monsters/ankheg.obj',
            scale = 0.3,
            texture = '../assets/monsters/ankheg',
            color = color.rgb(150,150,150),
            collider = 'box',
            double_sided = True,
            **kwargs
            )
        self.player = player
    
    def play_screamer(self):
        Audio('../assets/sounds/monsterscream.mp3', autoplay = True)
        self.player.mode = 2
        self.position = (0,-4.4,25)
        AmbientLight(color=(1, 1, 1, 1.0))
        self.animate_position((0,-10,0), duration = .2)
        camera.parent = scene
        camera.position = (0,-5,-4)
        camera.rotation = (5,2,0)
        camera.shake(duration = 1, magnitude = 1)
        


if __name__ == '__main__':
    app = Ursina()
    Ankheg()
    EditorCamera()
    app.run()