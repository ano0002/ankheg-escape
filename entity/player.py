from ursina import *

class Player(Entity):
    def __init__(self, **kwargs):
        self.rotation_speed = 100
        self.speed = 2
        self.gravity = 9.81
        self.velocity = Vec3(0, 0, 0)
        self.mode = 0
        super().__init__(
            model='cube',
            **kwargs
        )
        camera.parent = self
        camera.position = (0, 0.2, 0)
        self.frame = 0
        camera.fov = 90
        
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value == 0:
            mouse.locked = True
            mouse.visible = False
        elif value == 1:
            mouse.locked = False
            mouse.visible = True
        elif value == 2:
            mouse.locked = False
            mouse.visible = False
        else:
            raise ValueError("Mode must be 0, 1 or 2")
        self._mode = value

    def update(self):
        self.frame += 1
        if self.frame == 60:
            self.frame = 0
        
        
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

        

        if self.mode == 0:#free cam
            self.rotation_y += mouse.velocity[0] * self.rotation_speed
            camera.rotation_x -= mouse.velocity[1] * self.rotation_speed
            self.position += total_movement
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity:
                mouse.hovered_entity.color = color.lime
                
                