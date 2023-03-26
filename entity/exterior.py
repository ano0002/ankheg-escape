from ursina import *


class Tree(Entity):
    def __init__(self, tree, texture_path,**kwargs):
        super().__init__(
            model =tree,
            texture = texture_path,
            **kwargs
            )