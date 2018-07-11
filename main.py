import pygame
from pygame.locals import *

from coward_hungry_ai_controller import CowardHungryAIController
from model import Model
from mouse_controller import MouseController
from parameters import *
from player_view import PlayerView
from stupid_hungry_ai_controller import StupidHungryAIController


def run():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    model = Model()
    model.register_controller(MouseController(screen.get_size(), MOUSE_SENSITIVE_RADIUS, model))
    model.register_controller(CowardHungryAIController())
    model.register_controller(CowardHungryAIController())

    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())
    model.register_controller(StupidHungryAIController())

    #view = GameboardView(screen, model)
    view = PlayerView(screen, model, model.blob_families[0], MOUSE_SENSITIVE_RADIUS)

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(60)

        model.events = pygame.event.get()
        for event in model.events:
            if event.type == QUIT:
                pygame.quit()
                return

        model.update()
        view.render()

        pygame.display.flip()


if __name__ == '__main__':
    run()