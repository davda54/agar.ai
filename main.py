import pygame

from basic_ai_controller import BasicAIController
from model import Model
from view import View


def run():
    model = Model()
    model.register_controller(BasicAIController())
    model.register_controller(BasicAIController())
    model.register_controller(BasicAIController())
    model.register_controller(BasicAIController())

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    view = View(screen, model)

    done = False

    while not done:
        if pygame.event.peek(pygame.QUIT):
            done = True

        model.update()
        view.render()

        pygame.event.clear()
        pygame.display.flip()


if __name__ == '__main__':
    run()