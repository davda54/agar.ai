import pygame

from coward_hungry_ai_controller import CowardHungryAIController
from gameboard_view import GameboardView
from model import Model
from stupid_hungry_ai_controller import StupidHungryAIController


def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    model = Model()
    #model.register_controller(MouseController(screen.get_size(), 48))
    model.register_controller(CowardHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())

    view = GameboardView(screen, model)
    #view = PlayerView(screen, model, model.blob_families[0], 48)

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