from ursina import *

class Custom_Button(Entity):
    def __init__(self, text = 'button', scale = (1, 1, 1), on_click = None,animated = True, **kwargs):
        super().__init__(
            model = 'cube',
            scale = scale,
            collider = 'box',
            **kwargs
            )
        self.default_scale = scale
        self.on_click = on_click
        self.animated = animated
    def update(self):
        if self.animated:
            if self.hovered:
                self.scale_y = self.default_scale[1] * 0.7
            else:
                self.scale_y = self.default_scale[1]

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if self.on_click:
                    self.on_click()
                    

