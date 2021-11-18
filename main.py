import pygame
from enum import Enum
from event_processing import process_event
import draw_screensavers

pygame.init()

FPS = 60
WIDTH = 1000
HEIGHT = 600


class Game:
    def __init__(self):
        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.hero_coordinates = [0, 0, 0]
        self.finished = False
        self.fps = FPS
        self.controller = draw_screensavers.ScreenSaverController(self.game_screen, self.fps)

    def start(self):
        self.finished = False
        self.update()

    def update(self):
        while not self.finished:
            self.clock.tick(FPS)
            self.controller.update()
            for event in pygame.event.get():
                self.finished, self.hero_coordinates = process_event(event, self.hero_coordinates)


if __name__ == "__main__":
    game = Game()
    game.start()
