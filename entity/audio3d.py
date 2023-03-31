from ursina import *

class Audio3d(Audio):
    def __init__(self,sound_file_name,player,max_distance=10 , **kwargs):
        super().__init__(sound_file_name,autoplay=False, **kwargs)
        self.player = player
        self.max_distance = max_distance
        
    def update(self):
        self.balance = math.sin((self.world_position.xz-self.player.world_position.xz).normalized().signedAngleRad(self.player.forward.xz)/2)
        self.volume = 1 - min(distance(self.world_position, self.player.world_position)/self.max_distance,1)


if __name__ == "__main__":
    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    
    ground = Entity(model= Terrain('heightmap_1'),scale = (50,2,50),texture = 'heightmap_1',collider = 'mesh')
    
    player = FirstPersonController()
    
    audio = Audio3d('./spider_hiss.wav',player)
    
    def update():
        print("balance :",audio.balance)
    
    def input(key):
        if key == "space":
            audio.play()

    app.run()
    
    