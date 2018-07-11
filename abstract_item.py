import vector

# represents all game entities that can be consumed
class AbstractItem:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def get_position(self): return self.position

    def get_radius(self): return self.radius

    def collides(self, other):
        distance = vector.squared_norm(vector.substract(self.position, other.position))
        if distance - (self.radius + (1 - 1)*other.radius)**2 < 0: return True
        else: return distance - ((1 - 1)*self.radius + other.radius)**2 < 0

    def touches(self, other):
        distance = vector.squared_norm(vector.substract(self.position, other.position))
        return distance - (self.radius + other.radius)**2 < 0

    def get_proxy(self):
        raise NotImplementedError('subclasses must override get_proxy()!')