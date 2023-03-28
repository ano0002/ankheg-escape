from ursina import *
from entity.player import Player
from entity.world import World

app = Ursina()




player = Player(position = (0,12.5, 0),rotation = (0,180,0), camera = camera, mode= 3)
world = World(player = player)
player.world = world

#button = Custom_Button(scale = (1,1,1), position = (0, 2, 15), color=color.red)




#Remove this to remove the fog
fog = []
for i in range(10):
    fog.append(Entity(parent=player,color = color.rgba(0,0,0,i*0.1), model='sky_dome', scale=4+i*7,texture='assets/world/sky.jpg'))



def update():
    """
    if distance_xz(player.position, post.position) >5 and player.mode != 2:
        ankheg.play_screamer()
    """
    """
    left_pane.position += Vec3(
        (held_keys['d']-held_keys['a']) * time.dt * 0.5,
        (held_keys['space']-held_keys['shift']) * time.dt * 0.5,
        (held_keys['w']-held_keys['s']) * time.dt * 0.5
    )
    """
    
def input(key):
    if key == "f":
        world.ankheg.play_screamer()
    if key == "escape":
        world.toggle_left_pane()
        pass




app.run()