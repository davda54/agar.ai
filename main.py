import argparse
import importlib
import itertools

import pygame
from pygame.locals import *

from controllers.mouse_controller import mouse_controller
from gameboard_view import GameboardView
from model import Model
from parameters import *
from player_view import PlayerView


#TODO: support play without graphics
def run(play, display, controllers):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    model = Model()

    if play:
        model.register_controller(mouse_controller(screen.get_size(), MOUSE_SENSITIVE_RADIUS, model))

    for controller in controllers:
        model.register_controller(controller())

    if play or display:
        view = PlayerView(screen, model, model.blob_families[0], MOUSE_SENSITIVE_RADIUS)
    else:
        view = GameboardView(screen, model)


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


def num_controller(arg):
    values = arg.split(',')
    if len(values) != 2: raise argparse.ArgumentError()

    number = int(values[0])
    class_name = values[1]

    if number < 1: raise argparse.ArgumentError()

    module = importlib.import_module("controllers." + class_name)
    class_ = getattr(module, class_name)

    return [class_ for _ in range(int(number))]

# CALL EXAMPLES

# 10,coward_hungry_ai_controller
# --display 3,coward_hungry_ai_controller 8,stupid_hungry_ai_controller 1,middle_ai_controller
# --play 3,coward_hungry_ai_controller 8,stupid_hungry_ai_controller 1,middle_ai_controller

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run agar.ai with custom AI')
    parser.add_argument('--display', action='store_true', help='display the first controller from the first person view')
    parser.add_argument('--play', action='store_true', help='play for one blob manually')
    parser.add_argument('controllers', metavar='N', type=num_controller, nargs='+', help='list of pairs "N,C" where C is controller class name and N is number of these controllers to instantiate')

    args = parser.parse_args()

    run(args.play, args.display, itertools.chain.from_iterable(args.controllers))

