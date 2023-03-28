from ursina import *
from ursina.shaders import lit_with_shadows_shader as lit_with_shadows
import json
from entity.interior_ui import Custom_Button
from entity.exterior import Tree, Post
from entity.player import Player
from entity.ennemy import Ankheg
from shader.fur_shader import *
from entity.menu import UI

app = Ursina()

world = Entity(model = "./assets/world/world.obj", scale = (50, 5, 50),texture="./assets/world/world.png", position = (0, 0, 0), collider = 'mesh',shader=lit_with_shadows)
grass = Fur(entity=world, scale=500, layers=2, layerSize=0.005)

sound_manager = Audio("assets/sounds/atmosphere-dark.mp3", autoplay=False, loop=True, volume=0.5)

player = Player(position = (0,12.5, 0),rotation = (0,180,0), camera = camera, mode= 3)



#button = Custom_Button(scale = (1,1,1), position = (0, 2, 15), color=color.red)


tree_types = [
    "Tree Type0 01.dae",
    "Tree Type0 02.dae",
    "Tree Type0 03.dae",
    "Tree Type0 04.dae",
    "Tree Type0 05.dae",
    "Tree Type0 06.dae"
]

tree_type = random.randint(0, len(tree_types)-1)

trees = [Tree(".\\assets\\trees\\Models\\"+random.choice(tree_types), texture_path = '.\\assets\\trees\\Textures\\Colorsheet Tree Cold.png', position = (i[0]/2,i[1]/2,i[2]/2)) for i in json.load(open("trees.json", "r"))]



sun = DirectionalLight()
sun.look_at((-1, -0.9, 0))

AmbientLight(color=(0.1, 0.1, 0.1, 1.0))

ankheg = Ankheg(player = player,position = (15,-100,15), rotation = (0,180,0))

Sky(texture='assets/world/sky.jpg', scale=1000, double_sided=True)

screamer_box = Entity(model = "cube", scale = (80,5,80), position = (0,-5,0), color = color.black,double_sided = True)

post = Post(position = (-0.7,1,0),rotation= (0,180,0))

grillage = Entity(model = "cube", scale = (29.5,5,0.1), position = (6.75,3.5,5.05),rotation_z= -2.5,texture="./assets/world/grillage.png",texture_scale=(12.25,5,2.5))
camp = Entity(model = "./assets/world/camp.obj", scale = (5,5,5), position = (6.24644, 0.75, 23.2621),color = color.rgb(0,0.12*255,0.035*255),rotation_z= -1,texture_scale=(1,1))

"""
#Remove this to remove the fog
fog = []
for i in range(10):
    fog.append(Entity(parent=player,color = color.rgba(0,0,0,i*0.1), model='sky_dome', scale=4+i*7,texture='assets/world/sky.jpg'))
"""


def update():
    """
    if distance_xz(player.position, post.position) >5 and player.mode != 2:
        ankheg.play_screamer()
    """
    if player.mode == 3:
        pass
     
def input(key):
    if key == "f":
        ankheg.play_screamer()
        

def start():
    sound_manager.play()
    enter()

def leave():
    player.mode = 0
    player.position = (1,2.52, 0)
    door_leave.disable()
    door_leave.text.visible = False
    door_enter.enable()

def enter():
    player.mode =1
    player.position = (-0.05,1.51, 0)
    player.rotation = (0,180,0)
    camera.rotation = (0,0,0)
    door_leave.enable()
    door_enter.disable()
    door_enter.text.visible = False

door_leave = Custom_Button(scale = (0.01,1,0.5), position = (0.4,1.51,0.25), color=color.clear, text = "Leave", on_click = leave,animated=False, player=player)
door_enter = Custom_Button(scale = (0.01,1,0.5), position = (0.6,1.51,0.25), color=color.clear, text = "Enter", on_click = enter,animated=False, player=player)


menu = UI(start = start,player = player)


app.run()