from ursina import *

class Audio3d(Audio):
    def __init__(self,sound_file_name,player,max_distance=10 , **kwargs):
        super().__init__(sound_file_name, **kwargs)
        self.player = player
        self.max_distance = max_distance
        
    def update(self):
        self.balance = math.sin((self.world_position.xz-self.player.world_position.xz).normalized().signedAngleRad(self.player.forward.xz)/2)
        self.volume = 1 - min(distance(self.world_position, self.player.world_position)/self.max_distance,1)
