# represents all game entities that can be consumed
class AbstractItem:
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def get_position(self): return self.position

    def get_size(self): return self.size

    def collides(self, other):
        pass

    def get_proxy(self):
        raise NotImplementedError('subclasses must override get_proxy()!')