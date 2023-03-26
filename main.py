from ursina import *

from entity.interior_ui import Button
from entity.exterior import Tree
app = Ursina()

tree = Tree('assets\\trees\\Models\\Tree Type0 01.dae', position = (0, 0, 0), scale = (1, 1, 1), color = color.white, texture_path = 'assets\\trees\\Textures\\Colorsheet Tree Cold.png')


button = Button(scale = 1, position = (0, 0, 15), color=color.red,)

def update():
    pass
    







app.run()