import vector
from abstract_item import AbstractItem


class AbstractMovingItem(AbstractItem):
    def __init__(self, model, position, radius, speed, force):
        super().__init__(position, radius)

        self.model = model
        self.force = force
        self.speed = speed

    def update(self, dt, global_velocity=(0,0)):
        velocity = vector.add(global_velocity, vector.multiply(self.force, dt))
        self.force = vector.multiply(self.force, 0.95)
        self.position = vector.add(self.position, vector.multiply(velocity, dt * self.speed))

        self.bounce_from_boundaries()

    def bounce_from_boundaries(self):
        board_size = self.model.get_board_size()

        if self.position[0] < self.radius: x = self.radius - self.position[0] + 10
        elif self.position[0] > board_size[0] - self.radius: x = board_size[0] - self.radius - self.position[0] - 10
        else: x = 0

        if self.position[1] < self.radius: y =  self.radius - self.position[1] + 10
        elif self.position[1] > board_size[1] - self.radius: y = board_size[1] - self.radius - self.position[1] - 10
        else: y = 0

        self.force = vector.add(self.force, (x, y))