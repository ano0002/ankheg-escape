from ursina import *

class UI_Button(Entity):
    def __init__(self,main_ui, texture, scale = (1,1,1), on_click = None, **kwargs):
        super().__init__(
            model = 'quad',
            texture = texture,
            scale = scale,
            collider = 'box',
            parent = main_ui,
            **kwargs
            )
        self.on_click = on_click
        self.default_scale = scale
    
    def update(self):
        if self.hovered:
            self.scale = self.default_scale * 1.1
        else:
            self.scale = self.default_scale
    
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if self.on_click:
                    self.on_click()
            

class UI(Entity):
    def __init__(self,player,start=None, **kwargs):
        super().__init__(parent = camera.ui,**kwargs)
        self.start = start
        self.play_button = UI_Button(main_ui=self,texture="./assets/ui/play_button.png", scale = Vec2(0.2,0.1), position = (0,0), on_click = self._start)
        self.main_menu = [self.play_button]
        self.cursor = Entity(parent = camera.ui, model = 'quad', scale = (0.04,0.04), origin = (-0.5,0), texture = './assets/ui/cursor.png')
        self.player = player
    
    def update(self):
        if self.player.mode not in (0,2):
            self.cursor.position = mouse.position
        else:
            self.cursor.position = (-1,-1)
    
    def _start(self):
        for child in self.main_menu:
            child.disable()
        self.start()