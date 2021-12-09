import json
import time

import pygame

import screensavers_control
from event_processing import EventProcessor
from screensavers_control import ScreenSaverController
from sound_control import SoundController
import animations
from heroes import MainHero, Character, MapMarker
from labyrinth import Labyrinth
from game_main_process_control import GameMainProcessController

pygame.init()

FPS = 200

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h


class Game:

    def __init__(self):
        """
        Вся игра со совим лабиринтом, героями
        """
        self.later_on_funcs = []
        self.begin = False
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.game_surf = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = Fps(self.clock)
        self.labyrinth = None
        self.labyrinth_file = ""
        self.main_hero = None
        self.characters = []
        self.game_controller = GameMainProcessController(self)
        self.screen_controller = ScreenSaverController(self)
        self.event_processor = EventProcessor(self)
        self.sounds_controller = SoundController(self)
        self.active_screen = "start_screen"

    def complete_level(self):
        """
        Поздравить с завершением уровня и открыть следующий
        """
        self.screen_controller.main_screen_saver.painter.animator.add_complete_level_animation()
        self.open_new_level()

    def open_new_level(self):
        """
        Разблокирует кнопку нового уровня
        """
        if self.screen_controller.level_screen_saver.selected_level < screensavers_control.LevelsCount - 1:
            self.screen_controller.level_screen_saver.level_buttons[
                self.screen_controller.level_screen_saver.selected_level + 1].block = False

    def exit_level(self):
        """
        Сбрасывает все данные уровня как будто его еще не открывали
        """
        self.later_on_funcs.append(animations.LaterOnFunc(self.clear_game_params, animations.BeginScreenAnimationTime,
                                                          self.fps))

    def clear_game_params(self):
        """
        Делает параметры игры идентичными исходным
        """
        self.labyrinth = None
        self.main_hero = None
        self.characters.clear()
        self.game_controller.clear_params()
        self.screen_controller.main_screen_saver.notification_screen.clear_params()
        self.set_game_params_to_game_modules()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "active_screen":
            if self.active_screen == "main_screen":
                self.run_switch_to_main_screen_animation()
            else:
                if self.begin:
                    self.run_switch_screen_animation()
                else:
                    self.screen_controller.add_lightening_screen_animation()
                    self.begin = True

    def run_switch_to_main_screen_animation(self):
        """

        """
        self.screen_controller.add_blackout_screen_animation()
        self.later_on_funcs.append(
            animations.LaterOnFunc(self.start_main_part, animations.BeginScreenAnimationTime,
                                   self.fps, [self.labyrinth_file]))
        self.later_on_funcs.append(
            animations.LaterOnFunc(self.screen_controller.set_active_screen,
                                   animations.BeginScreenAnimationTime,
                                   self.fps, ["main_screen"]))

    def run_switch_screen_animation(self):
        self.screen_controller.add_blackout_screen_animation()
        self.later_on_funcs.append(animations.LaterOnFunc(
            self.set_active_screen_in_screen_controller,
            animations.BeginScreenAnimationTime,
            self.fps, [self.active_screen]))
        self.later_on_funcs.append(
            animations.LaterOnFunc(self.screen_controller.add_lightening_screen_animation,
                                   animations.BeginScreenAnimationTime, self.fps))

    def set_active_screen_in_screen_controller(self, screen_name):
        """
        Сменить экран игры

        :param screen_name: иня нового экрана
        """
        self.screen_controller.set_active_screen(screen_name)

    def create_main_hero(self):
        """
        Создать главного героя
        """
        self.main_hero = MainHero(self)

    def create_characters(self):
        """
        Создать второстепенных персонажей
        """
        with open(self.labyrinth_file) as file:
            characters_dict = json.load(file)["characters"]
        self.characters = []
        for character_description_dict in characters_dict:
            if character_description_dict["type"] == "MapMarker":
                cords = character_description_dict["start_cords"]
                appearance_stage = character_description_dict["appearance_stage"]
                name = character_description_dict["name"]
                elevator_condition = character_description_dict["inside_elevator"]
                self.characters.append(MapMarker(self, cords, name, elevator_condition, appearance_stage))
            else:
                cords = character_description_dict["start_cords"]
                appearance_stage = character_description_dict["appearance_stage"]
                name = character_description_dict["name"]
                self.characters.append(Character(self, cords, name, appearance_stage))

    def start_main_part(self, level_file_name):
        """
        Запуск уровня
        """
        self.labyrinth = Labyrinth(level_file_name)
        self.create_main_hero()
        self.create_characters()
        self.set_game_params_to_game_modules()
        self.screen_controller.add_lightening_screen_animation()

    def set_game_params_to_game_modules(self):
        """
        Задание параметров текущего уровня всем обработчикам
        """
        self.screen_controller.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.event_processor.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.game_controller.set_game_params(self.main_hero, self.characters)

    def set_active_screen(self, screen_name):
        self.active_screen = screen_name

    def update_later_on_funcs(self):
        for func in self.later_on_funcs:
            func.update()

    def main_process(self):
        self.sounds_controller.update()
        self.event_processor.update()
        self.screen_controller.update()
        self.update_later_on_funcs()

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
