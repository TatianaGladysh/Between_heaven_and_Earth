import pygame
from enum import Enum

pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 600


import draw_all
import labyrinth
import heroes
import event_processing
import game_field



class Game:
    def __init__(self):
        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def update(self):
        self.clock.tick(FPS)




def main():
    game = Game()

    finished = False

    while not finished:
        # draw_all()
        # движение всех героев, обновление картинки
        game.update()
        for event in pygame.event.get():
            # движение главного героя - обработка событий
            finished = event_processing.process_event(event)
    pygame.quit()


if __name__ == "__main__":
    main()
