from abstract_controller import AbstractController

# controls a blob family according to a mouse movemnt
class MouseController(AbstractController):
    def __init__(self, manipulator):
        super().__init__(manipulator)

    def update(self):
        pass