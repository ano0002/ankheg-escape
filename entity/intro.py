from ursina import *

class Intro(Entity):
    def __init__(self,on_end, **kwargs):
        super().__init__(**kwargs)
        self.overlay = Entity(parent=camera.ui, model='quad', color=color.black, scale=(2,1), z=-1)
        
        self.text = Text("""You are the new security guard on the night shift, stationed at the abandoned research facility. It's your first night on the job, and you're feeling a little uneasy. The facility has been closed for years, and the rumors about what happened here have always been unsettling.

You settle into your chair at the entrance security desk, and you begin to monitor the security cameras. The facility looks quiet, but something doesn't feel right. The shadows seem to be moving, and strange whispers echo through the speakers.

Suddenly, the lights flicker, and you hear a loud rumble coming from the entrance gate. The security cameras show something massive, breaking through the fence and heading straight for you.

Your heart races as you try to call for backup, but the line is dead. You're on your own. You see it coming closer, its mandibles clicking hungrily. You try to run, but it's too fast, too strong.

You feel its acid spray burning your skin, and you scream in agony. Just when you think it's all over, you wake up, still at the entrance security desk.

It was all just a nightmare, but the fear lingers. You realize that the rumors about the facility might be true, and the ankheg might still be out there, waiting for its next victim.

The abandoned research facility is a place of horror, and you must survive the night shift if you want to uncover the truth about what really happened here. The ankheg is still out there, waiting to hunt you down. Will you be able to make it to morning, or will you become the next victim of the ankheg's endless hunger?  """,
            scale=1, x=-.8, y=.4,z=-2, line_height=1.2, max_width=1.5,resolution = 50,size = 0.04,wordwrap = 80	)
        self.text.appear(speed=0.05)
        self.skip = Text("Press space to skip",scale=1, x=-.8, y=-.4,z=-2, line_height=1.2, max_width=1.5,resolution = 50,size = 0.04,wordwrap = 80	)
        self.on_end = on_end
        invoke(self.slide_in, delay=0.05*500)
        
    def _on_end(self):
        destroy(self.overlay)
        destroy(self.text)
        destroy(self.skip)
        destroy(self)
        self.on_end()
    
    def slide_in(self):
        try :
            self.text.animate_position(Vec2(-.8,1.4),duration=54,curve= curve.linear)
        except:
            pass
    
    def input(self,key):
        if key == "space":
            if not self.text.appear_sequence.finished:
                self.text.appear(speed=0)
                self.text.position = Vec2(-.8,1.4)
            else:
                self._on_end()
            
if __name__ == '__main__':
    app = Ursina()
    
    on_end = lambda: print("end")
    Intro(on_end = on_end)
    
    app.run()
    