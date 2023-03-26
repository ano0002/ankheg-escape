from ursina import *
from ursina.shaders import lit_with_shadows_shader as lit_with_shadows
import json
from entity.interior_ui import Button
from entity.exterior import Tree
from entity.player import Player
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()

world = Entity(model = Terrain("./assets/world.png",skip=5), scale = (100, 10, 100),color=color.rgb(10,75,10), position = (0, 0, 0), collider = 'mesh',shader=lit_with_shadows)

player = Player(position = (0,25, 0), camera = camera)



#button = Button(scale = 1, position = (0, 0, 15), color=color.red,)

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




app.run()