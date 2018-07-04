from abstract_controller import AbstractController

class IOController(AbstractController):
    def __init__(self, manipulator):
        super().__init__(manipulator)

    def update(self):
        pass