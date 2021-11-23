import pygame
from draw_all import Painter
import numpy as np
from buttons import LevelButton, StartButton

pygame.init()

LevelsCount = 6


class ScreenSaverController:
    def __init__(self, _surf, _fps, _window_width, _window_height, _active_screen, _labyrinth_file, _labyrinth=None,
                 _main_hero=None, _characters=None):
        """
        :param _labyrinth: лабиринт с комнатами
        :param _main_hero: главный герой
        :param _characters: другие герои
        :param _surf: Main Surface
        :param _fps: частота обновления кадров
        """
        self.active_screen = _active_screen
        self.fps = _fps
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.surf = _surf
        self.labyrinth_file = _labyrinth_file
        self.window_height = _window_height
        self.window_width = _window_width
        self.level_screen_saver = LevelScreenSaver(self.surf, self.fps, self.window_width, self.window_height,
                                                   self.active_screen, LevelsCount, self.labyrinth_file)
        self.start_screen_saver = StartScreenSaver(self.surf, self.fps, self.window_width, self.window_height,
                                                   _active_screen)
        self.main_screen_saver = MainScreenSaver(self.window_width, self.window_height, self.labyrinth, self.main_hero,
                                                 self.characters, self.surf, self.fps, self.active_screen)
        self.selected_level = None

    def update(self):
        """
        Вызывает функции обновления объекта отрисовки игровых объектов и интерфейса
        """
        self.surf.fill("WHITE")
        if self.active_screen == "start_screen":
            self.start_screen_saver.update()
        elif self.active_screen == "main_screen":
            self.main_screen_saver.update()
        elif self.active_screen == "level_screen":
            self.level_screen_saver.update()
        pygame.display.update()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.set_game_params_to_main_screen_saver()

    def set_game_params_to_main_screen_saver(self):
        self.main_screen_saver.set_game_params(self.labyrinth, self.main_hero, self.characters)


class GameScreenSaver:

    def __init__(self, _surf, _window_width, _window_height, _fps, _background_img):
        """
        Объект класса - заставка экрана игры
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        self.surf = _surf
        self.delta_time = 1 / _fps
        self.game_time = 0
        self.window_width = _window_width
        self.window_height = _window_height
        self.background_img = _background_img
        self.background_scale_k = self.calculate_background_scale_k()

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img)
        k = self.window_height / img_surf.get_height()
        return k

    def update_background(self):
        """
        Обновление картинки заднего плана
        """
        img_surf = pygame.image.load(self.background_img)
        img_surf = pygame.transform.scale(img_surf, (
            int(img_surf.get_width() * self.background_scale_k), int(img_surf.get_height() * self.background_scale_k)))
        img_rect = img_surf.get_rect()
        self.surf.blit(img_surf, img_rect)


class StartScreenSaver(GameScreenSaver):

    def __init__(self, _surf, _fps, _window_width, _window_height, _active_screen):
        """
        Объект класса
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        super().__init__(_surf, _window_width, _window_height, _fps, "assets/backgrounds/start_background.png")
        self.start_button = StartButton(_surf, _window_width, _window_height, _active_screen)
        self.window_height = _window_height
        self.window_width = _window_width
        self.background_img = "assets/backgrounds/start_background.png"
        self.background_scale_k = self.calculate_background_scale_k()

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img)
        k = self.window_height / img_surf.get_height()
        return k

    def update(self):
        """
        Функция обновления изображений кнопок на начальном экране игры и его заднего плана
        """
        self.update_background()
        self.start_button.update()


class MainScreenSaver(GameScreenSaver):

    def __init__(self, _window_width, _window_height, _labyrinth, _main_hero, _characters, _surf, _fps, _active_screen):
        """
        Главная заставка игры, где пользователь может управлять героем
        :param _surf: Main Surface of the game
        :param _labyrinth: объект, в котором храняться комнаты лабиринта
        :param _main_hero: главный герой игры
        :param _characters: другие герои игры
        """
        super().__init__(_surf, _window_width, _window_height, _fps, "assets/backgrounds/main_background.png")
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.window_height = _window_height
        self.window_width = _window_width
        self.painter = Painter(self.surf, self.window_width, self.window_height, self.labyrinth, self.main_hero,
                               self.characters)
        self.notifications = [Notification()]

    def draw_game_space(self):
        """
        функция отрисовки главного пространства игры
        """
        self.update_background()
        self.painter.update()

    def update(self):
        """
        будет обрабатывать действия с уведомлениями
        """
        self.main_hero.update()
        self.draw_game_space()
        for notification in self.notifications:
            notification.update()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.painter.set_game_params(self.labyrinth, self.main_hero, self.characters)


class LevelScreenSaver(GameScreenSaver):

    def __init__(self, _surf, _fps, _window_width, _window_height, _active_screen, _levels_count, _labyrinth_file):
        super().__init__(_surf, _window_width, _window_height, _fps, "assets/backgrounds/start_background.png")
        self.window_width = _window_width
        self.window_height = _window_height
        self.levels_count = _levels_count
        self.labyrinth_file = _labyrinth_file
        self.active_screen = _active_screen
        self.level_buttons = self.fill_level_buttons_array()

    def fill_level_buttons_array(self):
        buttons_array = np.zeros(self.levels_count, dtype=LevelButton)
        button_surf = pygame.image.load("assets/buttons/0_lvl_button.png")
        button_width = button_surf.get_width()
        indent = button_width // 4
        button_height = button_surf.get_height()
        if self.levels_count <= 5:
            zero_button_x = self.window_width // 2 - (
                    (self.levels_count / 2 - 1 / 2) * button_width + (self.levels_count - 1) / 2 * indent)
            for i in range(self.levels_count):
                button_x = zero_button_x + i * (indent + button_width)
                button_y = self.window_height // 2
                buttons_array[i] = LevelButton(self.surf, self.window_width, self.window_height, button_x, button_y,
                                               self.active_screen, i, self.labyrinth_file)
        elif self.levels_count <= 10:
            zero_button_x = self.window_width // 2 - (
                    ((self.levels_count + 1) // 2 / 2 - 1 / 2) * button_width + (self.levels_count - 1) / 2 * indent)
            zero_button_y = self.window_height // 2 - button_height // 2 - indent // 2
            for i in range((self.levels_count + 1) // 2):
                button_x = zero_button_x + i * (indent + button_width)
                button_y = zero_button_y
                buttons_array[i] = LevelButton(self.surf, self.window_width, self.window_height, button_x, button_y,
                                               self.active_screen, i, self.labyrinth_file)
            zero_button_x = self.window_width // 2 - (
                    ((self.levels_count - (self.levels_count + 1) // 2) / 2 - 1 / 2) * button_width + (
                        self.levels_count - 1) / 2 * indent)
            for i in range((self.levels_count + 1) // 2, self.levels_count):
                button_x = zero_button_x + (i - (self.levels_count + 1) // 2) * (button_width + indent)
                button_y = zero_button_y + indent + button_height
                buttons_array[i] = LevelButton(self.surf, self.window_width, self.window_height, button_x, button_y,
                                               self.active_screen, i, self.labyrinth_file)

        return buttons_array

    def update(self):
        self.update_background()
        for button in self.level_buttons:
            button.update()


class Notification:

    def __init__(self):
        """
        Уведомления
        """
        pass

    def update(self):
        pass
