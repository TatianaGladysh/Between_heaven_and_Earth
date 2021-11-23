import pygame
from heroes import MainHero, Character
from event_processing import EventProcessor
from screensavers_control import ScreenSaverController
from labyrinth import Labyrinth

pygame.init()

FPS = 200
WIDTH = 1000
HEIGHT = 600


class Game:

    def __init__(self):
        """
        Вся игра со совим лабиринтом, героями
        """
        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.labyrinth = None
        self.labyrinth_file = LabyrinthFile()
        self.main_hero = None
        self.characters = None
        self.active_screen = Activity()
        self.fps = FPS
        self.screen_controller = ScreenSaverController(self.game_screen, self.fps, WIDTH, HEIGHT, self.active_screen,
                                                       self.labyrinth_file)
        self.event_processor = EventProcessor(self, self.active_screen,
                                              self.screen_controller.start_screen_saver.start_button,
                                              self.screen_controller.level_screen_saver.level_buttons)
        self.previous_screen = "start_screen"

    def start_main_part(self, level_file_name):
        """
        потом можно будет сделать выбор карты
        """
        self.labyrinth = Labyrinth(level_file_name)
        self.main_hero = MainHero((0, 0, 0), self.fps, self)
        # потом нужно будет сделать задаваемые координаты из файла с
        self.screen_controller.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.event_processor.set_game_params(self.labyrinth, self.main_hero, self.characters)

    def set_active_screen(self, screen_name):
        self.active_screen.set_value(screen_name)

    def update(self):
        """
        Основной цикл игры
        """
        while not self.event_processor.quit:
            self.clock.tick(FPS)
            self.event_processor.update_events_statuses_and_objects_cords()
            if self.event_processor.active_screen != self.previous_screen:
                self.previous_screen = self.active_screen.value
                if self.active_screen == "main_screen":
                    self.start_main_part(self.labyrinth_file)
            self.screen_controller.update()


class Activity:

    def __init__(self):
        """
        инициализиция окна игры
        """
        self.value = "start_screen"

    def set_value(self, name):
        """
        смена экрана игры
        :param name: имя нового экрана
        """
        self.value = name

    def __eq__(self, other):
        """
        Равен ли наш объект данному
        :param other: данный объект
        :return: True или False: равен или нет
        """
        return self.value == other


class LabyrinthFile:

    def __init__(self):
        self.value = ""

    def set_value(self, file_name):
        self.value = file_name

    def get_value(self):
        return self.value


if __name__ == "__main__":
    game = Game()
    game.update()
