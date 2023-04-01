from ursina import *
from ursina.shaders import lit_with_shadows_shader

class Tree(Entity):
    def __init__(self, tree, texture_path,**kwargs) -> None:
        super().__init__(
            model =tree,
            texture = texture_path,
            **kwargs
            )

class Post(Entity):
    def __init__(self,**kwargs) -> None:
        super().__init__(
            model ="../assets/post/security post.obj",
            texture = "../assets/post/texture.png",
            **kwargs,
            scale = (0.02,0.02,0.02),
            double_sided = True,
            shader = lit_with_shadows_shader,
            collider = 'box'
            )

if __name__ == "__main__":
    app = Ursina()
    post = Post(position = (0,0,0))
    sun = DirectionalLight()
    sun.look_at((-1, -0.9, 0))

    AmbientLight(color=(0.1, 0.1, 0.1, 1.0))

    EditorCamera()
    app.run()