import pygame

from model import Model
from view import View

def run():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    model = Model()
    view = View(screen, model)

    done = False

    while not done:
        if pygame.event.peek(pygame.QUIT):
            done = True

        view.render()

        pygame.event.clear()
        pygame.display.flip()


if __name__ == '__main__':
    run()