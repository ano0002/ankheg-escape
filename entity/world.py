from ursina import *
from ursina.shaders import lit_with_shadows_shader
from shader.fur_shader import *
from entity.ennemy import Ankheg
from entity.menu import UI
from entity.interior_ui import Custom_Button
from entity.exterior import Tree, Post
import json



class World(Entity):
    def __init__(self,player):
        super().__init__()
        self.player = player
        self.ui = None
        self.load_world()
        self.load_sound()
        self.load_ui()
        
    def load_world(self):
        self.load_lights()
        self.load_ground()
        self.load_trees()
        self.load_camp()
        self.load_post()
        self.sky = Sky(texture='assets/world/sky.jpg', scale=1000, double_sided=True)

    def load_camp(self):
        self.grillage = Entity(model = "cube", scale = (29.5,5,0.1), position = (6.75,3.5,5.05),rotation_z= -2.5,texture="./assets/world/grillage.png",texture_scale=(12.25,5,2.5))
        self.camp = Entity(model = "./assets/world/camp.obj", scale = (5,5,5), position = (6.24644, 0.75, 23.2621),color = color.rgb(0,0.12*255,0.035*255),rotation_z= -1,texture_scale=(1,1))

    
    def load_ground(self):
        self.ground = Entity(model = "./assets/world/world.obj", scale = (50, 5, 50),texture="./assets/world/world.png", position = (0, 0, 0), collider = 'mesh',shader=lit_with_shadows_shader)
        self.grass = Fur(entity=self.ground, scale=500, layers=2, layerSize=0.005)
        
    def load_trees(self):
        tree_types = [
            "Tree Type0 01.dae",
            "Tree Type0 02.dae",
            "Tree Type0 03.dae",
            "Tree Type0 04.dae",
            "Tree Type0 05.dae",
            "Tree Type0 06.dae"
        ]

        tree_type = random.randint(0, len(tree_types)-1)

        self.trees = [Tree("..\\assets\\trees\\Models\\"+random.choice(tree_types), texture_path = '.\\assets\\trees\\Textures\\Colorsheet Tree Cold.png', position = (i[0]/2,i[1]/2,i[2]/2)) for i in json.load(open("trees.json", "r"))]

    def load_lights(self):       
        self.sun = DirectionalLight()
        self.sun.look_at((-1, -0.9, 0))

        AmbientLight(color=(0.1, 0.1, 0.1, 1.0))


    def load_sound(self): 
        self.background_sound = Audio("assets/sounds/atmosphere-dark.mp3", autoplay=False, loop=True, volume=0.5)

    def load_screamer(self):

        self.ankheg = Ankheg(player = self.player,position = (15,-100,15), rotation = (0,180,0))

        self.screamer_box = Entity(model = "cube", scale = (80,5,80), position = (0,-5,0), color = color.black,double_sided = True)

    def load_post(self):
        self.post = Post(position = (-0.7,1,0),rotation= (0,180,0))
        self.load_panes()
        self.load_door()

    def load_panes(self):
        self.left_pane = Entity(model = "cube", scale = (0.01,0,0.75), position = Vec3(0.525, 2.01, -0.325), color = color.white,texture_scale=(0.5,1,0.5))

    def load_door(self):
        self.door_leave = Custom_Button(scale = (0.01,1,0.5), position = (0.4,1.51,0.25), color=color.clear, text = "Leave", on_click = self.leave_post,animated=False, player=self.player)
        self.door_enter = Custom_Button(scale = (0.01,0,0.75), position = (0.6,1.51,0.25), color=color.clear, text = "Enter", on_click = self.enter_post,animated=False, player=self.player)

    def load_ui(self):
        self.ui = UI(start = self.start,player = self.player)

    def start(self):
        self.background_sound.play()
        self.enter_post()

    def leave_post(self):
        self.player.mode = 0
        self.player.position = (1,2.52, 0)
        self.door_leave.disable()
        self.door_leave.text.visible = False
        self.door_enter.enable()

    def enter_post(self):
        self.player.mode = 1
        self.player.position = (-0.05,1.51, 0)
        self.door_leave.enable()
        self.door_enter.disable()
        self.door_enter.text.visible = False

    def toggle_left_pane(self):
        print(self.left_pane.scale_y)
        if self.left_pane.scale_y <0.3:
            self.close_left_pane()
        else:
            self.open_left_pane()

    def close_left_pane(self):
        self.left_pane.animate_position((0.525, 1.71, -0.325), duration=0.2, curve=curve.linear)
        self.left_pane.animate_scale((0.01,0.6,0.75), duration=0.2, curve=curve.linear)
        
    def open_left_pane(self):
        self.left_pane.animate_position((0.525, 2.01, -0.325), duration=0.2, curve=curve.linear)
        self.left_pane.animate_scale((0.01,0,0.75), duration=0.2, curve=curve.linear)
    
