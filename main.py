import json
import time

import pygame

from event_processing import EventProcessor
from heroes import MainHero, Character
from labyrinth import Labyrinth
from screensavers_control import ScreenSaverController
import animations

pygame.init()

FPS = 200
WIDTH = 1000
HEIGHT = 600


class Game:

    def __init__(self):
        """
        Вся игра со совим лабиринтом, героями
        """
        self.begin = False
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.game_surf = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = Fps(self.clock)
        self.labyrinth = None
        self.labyrinth_file = ""
        self.main_hero = None
        self.characters = None
        self.screen_controller = ScreenSaverController(self)
        self.event_processor = EventProcessor(self)
        self.screen_controller.add_begin_screen_animation()
        self.active_screen = "start_screen"
        self.later_on_func = None

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "active_screen":
            if self.active_screen == "main_screen":
                self.later_on_func = animations.LaterOnFunc(self.start_main_part, animations.BeginScreenAnimationTime,
                                                            self.fps, [self.labyrinth_file])
            else:
                self.later_on_func = animations.LaterOnFunc(self.set_active_screen_in_screen_controller,
                                                            animations.BeginScreenAnimationTime,
                                                            self.fps, [self.active_screen])

            if self.begin:
                self.screen_controller.add_switch_screen_animation()
            else:
                self.screen_controller.add_begin_screen_animation()
                self.begin = True

    def set_active_screen_in_screen_controller(self, screen_name):
        self.screen_controller.set_active_screen(screen_name)

    def create_main_hero(self):
        self.main_hero = MainHero(self)

    def create_characters(self):
        with open(self.labyrinth_file) as file:
            characters_dict = json.load(file)["characters"]
        self.characters = []
        for character_description_dict in characters_dict:
            cords = character_description_dict["start_cords"]
            appearance_stage = character_description_dict["appearance_stage"]
            name = character_description_dict["name"]
            task = character_description_dict["task"]
            self.characters.append(Character(self, cords, name, task, appearance_stage))

    def start_main_part(self, level_file_name):
        """
        потом можно будет сделать выбор карты
        """
        self.labyrinth = Labyrinth(level_file_name)
        self.create_main_hero()
        self.create_characters()
        # потом нужно будет сделать задаваемые координаты из файла с
        self.screen_controller.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.event_processor.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.screen_controller.set_active_screen("main_screen")

    def set_active_screen(self, screen_name):
        self.active_screen = screen_name

    def main_process(self):
        self.event_processor.update_events_statuses_and_objects_cords()
        self.screen_controller.update()
        if self.later_on_func:
            self.later_on_func.update()

    def update(self):
        """
        Основной цикл игры
        """
        while not self.event_processor.quit:
            self.fps.begin_of_cycle()
            self.main_process()
            self.fps.end_of_cycle()


class Fps:
    def __init__(self, _clock):
        self.value = FPS
        self.start_time = 0
        self.end_time = 0
        self.clock = _clock
        self.display_delay = 0.5
        self.display_countdown = 0

    def __rtruediv__(self, other):
        return other / self.value

    def begin_of_cycle(self):
        self.start_time = time.time()

    def end_of_cycle(self):
        self.end_time = time.time()
        self.value = 1 / (self.end_time - self.start_time)
        self.display_countdown += (1 / self.value)
        if self.display_countdown >= self.display_delay:
            self.display_countdown = 0
            pygame.display.set_caption("FPS = {:.2f}".format(self.value))


if __name__ == "__main__":
    game = Game()
    game.update()
