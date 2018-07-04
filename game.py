from model import Model
from view import View

class Game:
    def __init__(self):
        self.model = Model()
        self.view = View(self.model)
        self.render = True

    def run(self):
        pass