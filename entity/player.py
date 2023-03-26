from ursina import *

class Player(Entity):
    def __init__(self,camera, **kwargs):
        super().__init__(
            **kwargs
        )
        camera.parent = self
        self.camera = camera
        self.rotation_speed = 100
        self.locked_camera = False
        self.gravity = 1
        self.velocity = Vec3(0, 0, 0)

    def update(self):
        ray = raycast(self.position, self.down, distance=self.velocity[1])
        if ray.hit:
        self.velocity += (0, -self.gravity, 0)
        if held_keys['w']:
            self.z += 0.1
        if held_keys['s']:
            self.z -= 0.1
        if held_keys['a']:
            self.x -= 0.1
        if held_keys['d']:
            self.x += 0.1
        if self.locked_camera:
            self.rotation_y -= mouse.velocity[1] * self.rotation_speed
            self.rotation_x += mouse.velocity[0] * self.rotation_speed
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity:
                mouse.hovered_entity.color = color.lime
                
                