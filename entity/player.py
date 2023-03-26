from ursina import *

class Player(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.random_color(),
            position=(0, 0, 0),
            collider = 'box',
            scale = (1, 1, 1)
        )

    def update(self):
        if held_keys['w']:
            self.z += 0.1
        if held_keys['s']:
            self.z -= 0.1
        if held_keys['a']:
            self.x -= 0.1
        if held_keys['d']:
            self.x += 0.1


    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity:
                mouse.hovered_entity.color = color.lime
                
                