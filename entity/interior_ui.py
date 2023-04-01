from ursina import *

class Custom_Button(Entity):
    def __init__(self, text = 'button', scale = (1, 1, 1), on_click = None,animated = True,player = None, **kwargs) -> None:
        super().__init__(
            model = 'cube',
            scale = scale,
            collider = 'box',
            **kwargs
            )
        self.default_scale = scale
        self.on_click = on_click
        self.animated = animated
        self.player = player
        self.text = Text(text, parent = camera.ui,visible = False,font = 'assets/fonts/Zombie_Holocaust.ttf',scale = 2)
    def update(self) -> None:
        self.text.visible = False
        if self.player != None :
            if self.hovered and distance_xz(self.player.position, self.position) < 2:
                if self.animated:
                    self.scale_y = self.default_scale[1] * 0.7
                self.text.visible = True
            else:
                self.scale_y = self.default_scale[1]
            if self.player.mode in (0,2):
                self.text.position = Vec3(0, -0.05,0)
            else :
                self.text.position =  mouse.position + Vec3(0.05, -0.02,0)

    def input(self, key) -> None:
        if (
            self.player != None
            and self.hovered
            and distance_xz(self.player.position, self.position) < 2
            and key == 'left mouse down'
            and self.on_click
        ):
            self.on_click()


