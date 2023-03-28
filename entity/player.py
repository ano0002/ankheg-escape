from ursina import *
from ursina.shaders import unlit_shader

class Player(Entity):
    def __init__(self, **kwargs):
        self.rotation_speed = 100
        self.speed = 2
        self.gravity = 0.5
        self.velocity = Vec3(0, 0, 0)
        self.flashlight = Entity(parent=camera, model='../assets/flashlight/flashlight.obj', texture='../assets/flashlight/texture.jpg',\
                                 double_sided = True ,scale= 0.0003,rotation = Vec3(2,-5,-60), position=(0.5, -0.2, 0.8), always_on_top = True)
        self.light_cone = Entity(parent=camera, model='../assets/flashlight/lightcone.obj', color=color.white50,\
                                 position=(0.5, -0.2, 0.8),rotation = Vec3(-85,0,0),scale=100,double_sided = True,shader = unlit_shader)
        self.battery = 100
        self.mode = 0
        super().__init__(
            **kwargs
        )
        camera.parent = self
        camera.position = (0, 0.2, 0)
        camera.fov = 90
        self.frame = 0
        self.time = 0
        self.last_battery_drop = 0
        
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value == 0: #free cam
            mouse.locked = True
            mouse.visible = False
            self.flashlight.enabled = True
            self.light_cone.enabled = True
        elif value == 1:#in post
            mouse.locked = False
            mouse.visible = False
            self.flashlight.enabled = False
            self.light_cone.enabled = False
        elif value == 2:#screamer
            mouse.locked = False
            mouse.visible = False
            self.flashlight.enabled = False
            self.light_cone.enabled = False
        elif value == 3:#in menu
            mouse.locked = False
            mouse.visible = False
            self.flashlight.enabled = False
            self.light_cone.enabled = False
        else:
            raise ValueError("Mode must be 0, 1, 2 or 3")
        self._mode = value
    
    def update(self):
        self.frame += 1
        self.time += time.dt
        if self.frame == 60:
            self.frame = 0
        
        if self.time > 300:
            self.time = 0
        
        if self.time-self.last_battery_drop > 0.2 :
            self.last_battery_drop = self.time
            if self.battery > 0:
                if self.light_cone.enabled:
                    self.battery -= 1
                    self.light_cone.color = color.rgba(255,255,255,self.battery/100*.50*255)
        
        
        if self.mode == 0:#free cam
            ray = raycast(self.position, (0,-1,0),distance=abs(self.velocity[1])+0.6)
            if not ray.hit:#if the player is not on the ground, apply gravity, else set the player to the ground and set the velocity to 0
                self.y += self.velocity[1]
                self.velocity[1] -= self.gravity*time.dt
            elif ray.hit:
                self.y = ray.world_point[1]+0.5
                self.velocity[1] = 0
                
            w_movement= Vec3(self.forward[0],0,self.forward[2]) * held_keys['w']
            s_movement= Vec3(self.back[0],0,self.back[2]) * held_keys['s']
            a_movement= Vec3(self.left[0],0,self.left[2]) * held_keys['a']
            d_movement= Vec3(self.right[0],0,self.right[2]) * held_keys['d']
            
            total_movement = (w_movement + s_movement + a_movement + d_movement).normalized()*self.speed*time.dt
            
            self.rotation_y += mouse.velocity[0] * self.rotation_speed
            camera.rotation_x -= mouse.velocity[1] * self.rotation_speed
            ray = raycast(self.position, total_movement.normalized(),distance=abs(sum(total_movement))+0.1)
            if not ray.hit:
                self.position += total_movement
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
            
    def input(self,key):
        if self.mode == 0:
            if key == "left mouse down":
                """
                self.toggling_light = True
                self.light_cone.animate_scale(0, duration = 0.1,curve=curve.in_out_sine)
                func =Func(Sequence(self.light_cone.,Func(setattr,self,"toggling_light",False)).start)
                func.delay = 0.1
                func()
                """
                if self.light_cone.enabled:
                    self.light_cone.fade_out(duration = .3)
                    function =Func(setattr,self.light_cone,"enabled",False)
                    invoke(function, delay = .3)
                else:
                    self.light_cone.enabled = True
                    self.light_cone.color = color.rgba(255,255,255,self.battery/100*.50*255)
        elif self.mode == 1 :
            if key == "a":
                self.animate_rotation((0, round(self.rotation_y/90)*90-90,0), duration = 0.2,curve=curve.in_out_sine)
            elif key == "d":
                self.animate_rotation((0, round(self.rotation_y/90)*90+90,0), duration = 0.2,curve=curve.in_out_sine)
                