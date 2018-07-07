# represents all game entities that can be consumed
class AbstractItem:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def get_position(self): return self.position

    def get_radius(self): return self.radius

    def collides(self, other):
        pass

    def get_proxy(self):
        raise NotImplementedError('subclasses must override get_proxy()!')