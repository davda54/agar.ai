class AbstractController:
    def __init__(self, manipulator):
        self.manipulator = manipulator

    def update(self):
        raise NotImplementedError('subclasses must override update()!')