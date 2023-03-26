from ursina import *

class Button(Entity):
    def __init__(self, text = 'button', scale = (1, 1, 1), position = (0, 0, 0), color = color.white, on_click = None):
        super().__init__(
            model = 'cube',
            scale = scale,
            position = position,
            color = color,
            collider = 'box'
            )

        self.on_click = on_click

    def input(self, key):
        print(self.hovered, self.on_click)
        if self.hovered:
            if key == 'left mouse down':
                if self.on_click:
                    self.on_click()
                    

