import pygame
from draw_all import Painter
from enum import Enum

pygame.init()


class Button:

    def __init__(self, _command, _surf):
        """Кнопка на начальном экране игры"""
        self.command = _command
        self.surf = _surf

    def on_click(self):
        self.command()

    def update_pic(self):
        pass


class StartButton(Button):

    def __init__(self, _surf):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(self.start, _surf)

    def start(self):
        pass


class GameScreenSavers:

    def __init__(self, _surf, _fps):
        """
        Объект класса - заставка экрана игры
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        self.surf = _surf
        self.delta_time = 1 / _fps

        self.game_time = 0

    def update(self):
        """
        Не окончата(можно сказать, даже не начата)
        :return:
        """
        self.surf.fill("WHITE")
        pygame.display.update()


class StartScreenSaver(GameScreenSavers):

    def __init__(self, _surf, _fps):
        """
        Объект класса
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        super().__init__(_surf, _fps)
        self.start_button = StartButton(_surf)
        self.active = True

    def update_buttons(self):
        """
        Функция обновления изображений кнопок на начальном экране игры
        :return:
        """
        self.start_button.update_pic()


class MainScreenSaver(GameScreenSavers):

    def __init__(self, _surf, _fps, _rooms, _main_hero, _characters):
        """
        Главная заставка игры, где пользователь может управлять героем
        :param _surf: Main Surface of the game
        :param _rooms: Массив комнат игры
        :param _main_hero: главный герой игры
        :param _characters: другие герои игры
        """
        super().__init__(_surf, _fps)
        self.rooms = _rooms
        self.main_hero = _main_hero
        self.characters = _characters
        self.painter = Painter(self.surf, self.rooms, self.main_hero, self.characters)
        self.active = False

    def draw_game_space(self):
        """функция отрисовки главного пространства игры"""
        self.painter.update_pics()
