from ursina import *


class Tree(Entity):
    def __init__(self, tree_path, texture_path, position = (0, 0, 0), scale = (1, 1, 1), color = color.white):
        super().__init__(
            model = tree_path,
            texture = texture_path,
            position = position,
            scale = scale,
            collider = 'box'
            )