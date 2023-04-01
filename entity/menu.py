from ursina import *

class UI_Button(Entity):
    def __init__(self,main_ui, texture, scale = (1,1,1), on_click = None, **kwargs) -> None:
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

    def update(self) -> None:
        self.scale = self.default_scale * 1.1 if self.hovered else self.default_scale

    def input(self, key) -> None:
        if self.hovered and key == 'left mouse down' and self.on_click:
            self.on_click()

class UI(Entity):
    def __init__(self,player,start=None, **kwargs) -> None:
        super().__init__(parent = camera.ui,**kwargs)
        self.start = start
        self.play_button = UI_Button(main_ui=self,texture="./assets/ui/play_button.png", scale = Vec2(0.2,0.1), position = (-0.5,0), on_click = self._start)
        self.setting_button = UI_Button(main_ui=self,texture="./assets/ui/setting_button.png", scale = Vec2(0.2,0.1), position = (-0.5,-0.2), on_click = self.open_setting)
        self.main_menu = [self.play_button,self.setting_button]
        self.setting_menu = []
        self.setting_menu.append(UI_Button(main_ui=self,texture="./assets/ui/close_button.png", scale = Vec2(0.1,0.1), position = (-0.5,0.2), on_click = self.close_setting))
        self.cursor = Entity(parent = camera.ui, model = 'quad', scale = (0.04,0.04), origin = (-0.5,0), texture = './assets/ui/cursor.png')
        self.player = player
        for child in self.setting_menu:
            child.disable()

    def update(self) -> None:
        if self.player.mode not in (0,2):
            self.cursor.position = mouse.position
        else:
            self.cursor.position = (-1,-1)

    def _start(self) -> None:
        for child in self.main_menu:
            child.disable()
        self.start()

    def open_setting(self) -> None:
        for child in self.main_menu:
            child.disable()
        for child in self.setting_menu:
            child.enable()

    def close_setting(self) -> None:
        for child in self.setting_menu:
            child.disable()
        for child in self.main_menu:
            child.enable()