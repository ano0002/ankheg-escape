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

world = Entity(model = "./assets/world/world.obj", scale = (100, 10, 100),texture="./assets/world/world.png", position = (0, 0, 0), collider = 'mesh',shader=lit_with_shadows)
grass = Fur(entity=world, scale=1000, layers=2, layerSize=0.005)

sound_manager = Audio("assets/sounds/atmosphere-dark.mp3", autoplay=False, loop=True, volume=0.5)

player = Player(position = (0,25, 0),rotation = (0,180,0), camera = camera, mode= 3)



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

trees = [Tree(".\\assets\\trees\\Models\\"+random.choice(tree_types), texture_path = '.\\assets\\trees\\Textures\\Colorsheet Tree Cold.png', position = (i[0],i[1],i[2])) for i in json.load(open("trees.json", "r"))]


sun = DirectionalLight()
sun.look_at((-1, -0.9, 0))

AmbientLight(color=(0.1, 0.1, 0.1, 1.0))

ankheg = Ankheg(player = player,position = (15,-100,15), rotation = (0,180,0))

Sky(texture='assets/world/sky.jpg', scale=1000, double_sided=True)

screamer_box = Entity(model = "cube", scale = (80,5,80), position = (0,-5,0), collider = 'box', color = color.black,double_sided = True)

post = Post(position = (-0.7,2,0),rotation= (0,180,0))

grillage = Entity(model = "cube", scale = (59,5,0.1), position = (13.5,3.5,10.1),rotation_z= -5,texture="./assets/world/grillage.png",texture_scale=(24.5,2.5))
camp = Entity(model = "./assets/world/camp.obj", scale = (5,5,5), position = (-3.41799, 1.5, 27.8483),color = color.rgb(0,0.12*255,0.035*255),rotation_z= -1,texture_scale=(1,1))
camp2 = Entity(model = "./assets/world/camp.obj", scale = (5,5,5), position = (28.9974, 3.5, 27.8483),color = color.rgb(0,0.12*255,0.035*255),rotation_z= -5,texture_scale=(1,1))

fog = []
for i in range(10):
    fog.append(Entity(parent=player,color = color.rgba(0,0,0,i*0.1), model='sky_dome', scale=4+i*7,texture='assets/world/sky.jpg'))

def update():	
    """
    if distance_xz(player.position, post.position) >5 and player.mode != 2:
        ankheg.play_screamer()
    """
    if player.mode == 3:
        pass
     
def input(key):
    if key == "escape":
        ankheg.play_screamer()

def start():
    sound_manager.play()
    player.mode = 0
    player.position = (0,5, 0)

menu = UI(start = start,player = player)

app.run()