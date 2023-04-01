from ursina import *
from entity.player import Player
from entity.world import World

app = Ursina()




player = Player(position = (0,12.5, 0),rotation = (0,180,0), camera = camera, mode= 3)
world = World(player = player)
player.world = world



#Remove this to remove the fog
fog = []
for i in range(10):
    fog.append(Entity(parent=player,color = color.rgba(0,0,0,i*0.1), model='sky_dome', scale=1+i*2,texture='assets/world/sky.jpg'))


def update() -> None:
    distance = distance_xz(player.position, world.post.position)
    for i in range(10):
        fog[i].scale = 1-distance*0.1+i*(2-distance*0.1)
    if distance > 15 and player.mode == 0:
        world.ankheg.play_screamer()
    
def input(key) -> None:
    if key == "f":
        world.ankheg.play_screamer()
    if key == "g":
        world.spiders[0].play_screamer()

app.run()