from typing import Tuple
from ursina import *
from ursina.shaders import lit_with_shadows_shader, unlit_shader
from shader.fur_shader import *
from entity.ennemy import Ankheg
from entity.menu import UI
from entity.interior_ui import Custom_Button
from entity.exterior import Tree, Post
from entity.spider import Spider
from entity.audio3d import Audio3d
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
        self.sky = Sky(texture='assets/world/sky.jpg', scale=1000, double_sided=True)

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
        ]]            
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
        self.load_panes()
        self.load_door()

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
        self.button1 = Custom_Button( scale = 0.1, position = Vec3(-0.2, 1.4, -0.6))
        self.button2 = Custom_Button( scale = 0.1, position = Vec3(0, 1.4, -0.6))
        self.button3 = Custom_Button(scale = 0.1, position = Vec3(0.2, 1.4, -0.6))
        self.button4 = Custom_Button(scale= 0.07,position= Vec3(-0.6,1.4,-0.45))
        self.button5 = Custom_Button(scale=0.07, position=Vec3(0.45,1.4,-0.45))
        self.button1.on_click = self.spotlight

    def spotlight(self):
        print("spotted")

    def load_ui(self) -> None:
        self.ui = UI(start = self.start,player = self.player)


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



class Shades:
    def __init__(self) -> None:
        self.left_pane = Entity(model = "cube", scale = (0.01,0,0.67), position = Vec3(0.535, 2.01, -0.355), \
            texture = "./assets/world/roller-shutter.jpg",shader = unlit_shader)
        self.right_pane = Entity(model = "cube", scale = (0.01,0,0.67), position = Vec3(-0.65, 2.01, -0.325), \
            texture = "./assets/world/roller-shutter.jpg",shader = unlit_shader)


    def toggle_left_pane(self) -> None:
        if self.left_pane.scale_y <0.3:
            self.close_left_pane()
        else:
            self.open_left_pane()

    def close_left_pane(self)-> None:
        self.left_pane.animate_position((0.535, 1.71, -0.355), duration=0.2, curve=curve.linear)
        self.left_pane.animate_scale((0.01,0.6,0.67), duration=0.2, curve=curve.linear)

    def open_left_pane(self)-> None:
        self.left_pane.animate_position((0.535, 2.01, -0.355), duration=0.2, curve=curve.linear)
        self.left_pane.animate_scale((0.01,0,0.67), duration=0.2, curve=curve.linear)


    def toggle_right_pane(self)-> None:
        if self.right_pane.scale_y <0.3:
            self.close_right_pane()
        else:
            self.open_right_pane()

    def close_right_pane(self)-> None:
        self.right_pane.animate_position((-0.65, 1.71, -0.325), duration=0.2, curve=curve.linear)
        self.right_pane.animate_scale((0.01,0.6,0.67), duration=0.2, curve=curve.linear)

    def open_right_pane(self) -> None:
        self.right_pane.animate_position(Vec3(-0.65, 2.01, -0.325), duration=0.2, curve=curve.linear)
        self.right_pane.animate_scale((0.01,0,0.67), duration=0.2, curve=curve.linear)

    def status(self) -> Tuple[bool,bool]:
        return (self.left_pane.scale_y >= 0.3, self.right_pane.scale_y >= 0.3)

