import pygame

from hungry_ai_controller import HungryAIController
from middle_ai_controller import MiddleAIController
from model import Model
from view import View


def run():
    model = Model()
    model.register_controller(MiddleAIController())
    model.register_controller(HungryAIController())
    model.register_controller(HungryAIController())
    model.register_controller(HungryAIController())
    model.register_controller(HungryAIController())


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