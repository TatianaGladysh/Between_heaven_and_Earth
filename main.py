import pygame
from heroes import MainHero, Character
from event_processing import EventProcessor
from screensavers_control import ScreenSaverController
from labyrinth import Labyrinth
import json

pygame.init()

FPS = 180
WIDTH = 1000
HEIGHT = 600


class Game:

    def __init__(self):
        """
        Вся игра со совим лабиринтом, героями
        """
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.game_surf = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.labyrinth = None
        self.labyrinth_file = ""
        self.main_hero = None
        self.characters = None
        self.active_screen = "start_screen"
        self.fps = FPS
        self.screen_controller = ScreenSaverController(self)
        self.event_processor = EventProcessor(self)
        self.previous_screen = "start_screen"

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

    def set_active_screen(self, screen_name):
        self.active_screen = screen_name

    def update(self):
        """
        Основной цикл игры
        """
        while not self.event_processor.quit:
            self.clock.tick(FPS)
            self.event_processor.update_events_statuses_and_objects_cords()
            if self.active_screen != self.previous_screen:
                self.previous_screen = self.active_screen
                if self.active_screen == "main_screen":
                    self.start_main_part(self.labyrinth_file)
            self.screen_controller.update()


if __name__ == "__main__":
    game = Game()
    game.update()
