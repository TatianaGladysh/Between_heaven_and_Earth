import pygame
from enum import Enum

FPS = 60
WIDTH = 800
HEIGHT = 600


import draw_all
import labyrinth
import heroes
import event_processing
import game_field







def main():
    pygame.init()
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        # draw_all()
        # движение всех героев, обновление картинки
        clock.tick(FPS)
        for event in pygame.event.get():
            # движение главного героя - обработка событий
            finished = event_processing.process_event(event)
    pygame.quit()


if __name__ == "__main__":
    main()
