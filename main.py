import pygame

from model import Model
from stupid_hungry_ai_controller import StupidHungryAIController
from view import View


def run():
    model = Model()
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())


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