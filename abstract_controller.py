# all classes that would like to control a blob family should implement this abstract class, the game logic expects an update
# function and  a constructor with manipulator as the first parameter

class AbstractController:
    def __init__(self, manipulator):
        self.manipulator = manipulator

    def update(self):
        raise NotImplementedError('subclasses must override update()!')