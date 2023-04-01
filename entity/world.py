from ursina import *
from ursina.shaders import lit_with_shadows_shader, unlit_shader
from shader.fur_shader import *
from entity.ennemy import Ankheg
from entity.menu import UI
from entity.interior_ui import Custom_Button
from entity.exterior import Tree, Post
from entity.spider import Spider
from entity.audio3d import Audio3d
from entity.intro import Intro
from entity.spotlight import Spotlight
import random
import json



class World(Entity):
    def __init__(self,player) -> None:
        super().__init__()
        self.player = player
        self.ui = None
        self.load_world()
        self.load_sound()
        self.load_ui()
        self.time = 0
        self.next_hiss = random.randint(5,10)

    def load_world(self) -> None:
        self.load_lights()
        self.load_ground()
        self.load_trees()
        self.load_camp()
        self.load_post()
        self.load_screamer()
        self.load_spiders()
        self.load_grass()
        self.load_buttons()
        self.load_intro()
        #self.sky = Sky(texture='assets/world/sky.jpg', scale=1000, double_sided=True)

    def load_camp(self)-> None:
        self.grillage = Entity(model = "cube", scale = (29.5,5,0.1), position = (6.75,3.5,5.05),rotation_z= -2.5,texture="./assets/world/grillage.png",texture_scale=(12.25,5,2.5))
        self.camp = Entity(model = "./assets/world/camp.obj", scale = (5,5,5), position = (6.24644, 0.75, 23.2621),color = color.rgb(0,0.12*255,0.035*255),rotation_z= -1,texture_scale=(1,1))

    def load_ground(self) -> None:
        self.ground = Entity(model = "./assets/world/world.obj", scale = (50, 5, 50),texture="./assets/world/world.png", position = (0, 0, 0), collider = 'mesh',shader=lit_with_shadows_shader)
        #self.grass = Fur(entity=self.ground, scale=500, layers=1, layerSize=0.005)
        
    def load_grass(self)-> None:
        return
        grass_types = [
            "Grass_001.fbx",
            "Grass_002.fbx",
            "Grass_003.fbx",
            "Grass_004.fbx",
            "Grass_005.fbx",
            "Grass_006.fbx",
            "Grass_007.fbx"
        ]          
        self.grass = []
        for x in range(-10,10):
            for z in range(-10,10) :
                x_offset = x / 5 + random.random() / 20
                z_offset = z / 5 + random.random() / 20
                ray = raycast(origin=(x_offset,0,z_offset), direction=(0,1,0))
                if ray.hit :
                    grass_type = random.choice(grass_types)
                    scale = 0.005

                    self.grass.append(
                        Entity(
                            model=grass_type,
                            scale=scale,
                            position=(x_offset, ray.world_point.y, z_offset),
                            rotation=(0, 0, 0),
                            texture_scale=(1, 1),
                            shader=lit_with_shadows_shader,
                        )
                    )
    
            
    def load_trees(self) -> None:
        tree_types = [
            "Tree Type0 01.dae",
            "Tree Type0 02.dae",
            "Tree Type0 03.dae",
            "Tree Type0 04.dae",
            "Tree Type0 05.dae",
            "Tree Type0 06.dae"
        ]

        self.trees = [
            Tree(
                f"./assets/trees/Models/{random.choice(tree_types)}",
                texture_path = './assets/trees/Textures/Colorsheet Tree Cold.png',
                position = i,
                rotation = (0, random.randint(0, 360), 0),
            )
            for i in json.load(open("./trees.json"))
        ]



    def load_lights(self) -> None:
        self.sun = DirectionalLight(intensity=0.5,shadow_map_resolution=(4000,4000))
        self.sun.look_at((-1, -0.9, 0))

        AmbientLight(color=(0.1, 0.1, 0.1, 1.0))

    def load_screamer(self) -> None:
        self.ankheg = Ankheg(player = self.player,world=self, rotation = (0,180,0))
        self.screamer_box = Entity(model = "cube", scale = (80,5,80), position = (0,-5,0), color = color.black,double_sided = True)

    def load_post(self) -> None:
        self.post = Post(position = (-0.7,1,0),rotation= (0,180,0))
        self.shades = Shades(self)
        self.load_door()
        self.spotlight = Spotlight(position = (0,2.13,-0.55),rotation = (0,90,0),world = self)

    def load_door(self) -> None:
        self.door_leave = Custom_Button(scale = (0.01,1,0.5), position = (0.4,1.51,0.25), color=color.clear, text = "Leave", on_click = self.leave_post,animated=False, player=self.player)
        self.door_enter = Custom_Button(scale = (0.01,1,0.75), position = (0.6,1.51,0.25), color=color.clear, text = "Enter", on_click = self.enter_post,animated=False, player=self.player)

    def load_spiders(self) -> None:
        self.spiders = [Spider(position = i,target = j) for i,j in json.load(open("spiders.json", "r"))]


    def load_sound(self) -> None:
        self.background_sound = Audio("assets/sounds/atmosphere-dark.mp3", autoplay=False, loop=True, volume=0.5)
        self.spider_hiss = Audio3d("assets/sounds/spider_hiss.wav", volume=0.5,player = self.player,position = (0,0,0))
        self.monster_scream = Audio("assets/sounds/monster_scream.mp3", autoplay=False, loop=False, volume=1)
        
    def load_buttons(self)-> None:
        self.button1 = Custom_Button( scale = 0.1, position = Vec3(-0.2, 1.4, -0.6),on_click= self.spotlight.toggle)
        self.button2 = Custom_Button( scale = 0.1, position = Vec3(0, 1.4, -0.6))
        self.button3 = Custom_Button(scale = 0.1, position = Vec3(0.2, 1.4, -0.6))
        self.button4 = Custom_Button(scale= 0.07,position= Vec3(-0.6,1.4,-0.45),on_click=self.shades.toggle_right_pane)
        self.button5 = Custom_Button(scale=0.07, position=Vec3(0.45,1.4,-0.45),on_click=self.shades.toggle_left_pane)


    def load_ui(self) -> None:
        self.ui = UI(start = self.start,player = self.player)

    def load_intro(self) -> None:
        self.intro = Intro(on_end=lambda: setattr(self, "intro", None))


    def update(self) -> None:
        self.time += time.dt
        if self.time > self.next_hiss:
            self.spider = random.choice(self.spiders)
            self.spider_hiss.play()
            self.spider_hiss.parent = self.spider
            self.spider_hiss.position = (0,0,0)
            self.spider.run()
            invoke(self.spider.reset, delay=2.2)
            self.next_hiss = self.time + random.randint(5,10)

    def start(self):
        self.background_sound.play()
        self.enter_post()

    def leave_post(self)-> None:
        self.player.mode = 0
        self.player.position = (1,2.52, 0)
        self.door_leave.disable()
        self.door_leave.text.visible = False
        self.door_enter.enable()

    def enter_post(self) -> None:
        self.player.mode = 1
        self.player.position = (-0.05,1.51, 0)
        self.player.rotation = (0,180,0)
        camera.rotation = (0,0,0)
        self.door_leave.enable()
        self.door_enter.disable()
        self.door_enter.text.visible = False



class Shades(Entity):
    def __init__(self,world:World) -> None:
        super().__init__(self)
        self.left_pane = Shade(self,position = Vec3(0.535, 2.01, -0.355))
        self.right_pane = Shade(self,position = Vec3(-0.65, 2.01, -0.325))
        self.world = world
        

    def toggle_left_pane(self) -> None:
        self.left_pane.toggle()


    def toggle_right_pane(self)-> None:
        self.right_pane.toggle()

    def status(self) -> dict[dict[int,bool],dict[int,bool]]:
        return {
            "left_pane": {
                "durability": self.left_pane.durability,
                "is_open": self.left_pane.is_open
            },
            "right_pane": {
                "durability": self.right_pane.durability,
                "is_open": self.right_pane.is_open
            }
        }
    
    def update(self) -> None:
        if not self.status()["left_pane"]["is_open"]:
            pass

class Shade(Entity):
    def __init__(self,manager, **kwargs):
        super().__init__(model = "cube", scale = (0.01,0,0.67),texture = "./assets/world/roller-shutter.jpg",shader = unlit_shader,**kwargs)
        self.durability = 100
        self.is_open = True
        self.indicator = Structural_Integrity_Display(self)
        self.manager = manager
            
    @property
    def durability(self) -> int:
        return self._durability
    
    @durability.setter
    def durability(self, value: int) -> None:
        if value <= 0:
            self._durability = 0
        elif value > 100:
            self._durability = 100
        else:
            self._durability = value
    
    def toggle(self) -> None:
        if self.durability:
            if self.is_open:
                self.close()
            else:
                self.open()
            self.is_open = not self.is_open
    
    def close(self)-> None:
        self.animate_position((self.x, self.y-0.3, self.z), duration=0.2, curve=curve.linear)
        self.animate_scale((self.scale_x,0.6,self.scale_z), duration=0.2, curve=curve.linear)
    
    def open(self)-> None:
        self.animate_position((self.x, self.y+0.3, self.z), duration=0.2, curve=curve.linear)
        self.animate_scale((self.scale_x,0,self.scale_z), duration=0.2, curve=curve.linear)
        
class Structural_Integrity_Display(Entity):
    def __init__(self,shade, **kwargs):
        super().__init__(model = "quad",position=shade.position+Vec3(0,-0.3,0),double_sided=True,
                         scale = (0.2,0.2),texture = "../assets/ui/cle a molette.png",
                         texture_scale=(0.25,1),shader = unlit_shader,rotation=Vec3(0,90,0),
                         always_on_top=True,**kwargs)
        self.shade = shade
        
        
    def update(self) -> None:
        if self.shade.manager.world.player.mode == 0:
            self.visible = False
        else:
            self.visible = True
            
        if self.shade.durability <= 0:
            self.texture_offset = (.75,0)
        elif self.shade.durability > 66:
            self.texture_offset = (0,0)
        elif self.shade.durability > 33:
            self.texture_offset = (.25,0)
        elif self.shade.durability > 0:
            self.texture_offset = (.5,0)
    