from ursina import *

class UI(Entity):
    def __init__(self, add_to_scene_entities=True,start=None, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.start = start
        self.play_button = Button(parent = camera.ui, text = 'Play', scale = (0.2,0.1), position = (-0.8,0.4), on_click = self.start)
        