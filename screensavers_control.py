import pygame
from draw_all import Painter
import numpy as np

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
        print(self.window_height, img_surf.get_height())
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


class Button:

    def __init__(self, _command, _surf, _window_width, _window_height):
        """
        Кнопка на начальном экране игры
        """
        self.window_height = _window_height
        self.window_width = _window_width
        self.command = _command
        self.surf = _surf
        self.pressed = False
        self.x = 0
        self.y = 0
        self.unit_width = 0
        self.unit_height = 0

    def click(self):
        """
        Вызывает функцию, привязанную к кнопке
        """
        self.command()

    def get_cords(self):
        """
        возвращает координаты верхнего левого угла кнопки
        """
        return self.x, self.y

    def get_width(self):
        """
        возвращает ширину кнопки
        """
        return self.unit_width

    def get_height(self):
        """
        возвращает высоту кнопки
        """
        return self.unit_height


class StartButton(Button):

    def __init__(self, _surf, _window_width, _window_height, _active_screen):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(self.start, _surf, _window_width, _window_height)
        self.img_file = "assets/buttons/start_button.png"
        self.img_surf = pygame.image.load(self.img_file)
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.active_screen = _active_screen
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта
        :return: координаты, коэффициент размера, длину и высоту
        """
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 4
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 2
        y = self.window_height // 2
        return x, y, k, unit_width, unit_height

    def update(self):
        """
        обновляет изображение, которое должно быть у кнопки
        """
        if self.pressed:
            self.img_file = "assets/buttons/pressed_start_button.png"
        else:
            self.img_file = "assets/buttons/start_button.png"

        self.img_surf = pygame.image.load(self.img_file)
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.update_pic()

    def update_pic(self):
        """
        обновляет картинку кнопки
        """
        self.update_image(255)

    def update_image(self, opacity):
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.img_surf.set_alpha(opacity)
        img_rect = self.img_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.img_surf, img_rect)

    def start(self):
        self.pressed = False
        self.active_screen.set_value("level_screen")


class LevelButton(Button):

    def __init__(self, _surf, _window_width, _window_height, _x, _y, _active_screen, _id, _labyrinth_file):
        super(LevelButton, self).__init__(self.launch_lvl, _surf, _window_width, _window_height)
        self.active_screen = _active_screen
        self.id = _id
        self.x = _x
        self.y = _y
        self.block = self.adopted_from_file()
        self.img_file = self.read_img_file()
        self.pressed = False
        self.labyrinth_file = _labyrinth_file
        self.width, self.height = self.calculate_dimensions()
        self.unit_width, self.unit_height = self.width, self.height

    @staticmethod
    def calculate_dimensions():
        img_surf = pygame.image.load("assets/buttons/0_lvl_button.png")
        return img_surf.get_width(), img_surf.get_height()

    def read_img_file(self):
        img_file = "assets/buttons/" + str(self.id) + "_lvl_button.png"
        return img_file

    def adopted_from_file(self):
        with open("levels/button_lock_data.txt", 'r') as file:
            string_with_data = file.readline()
            code = string_with_data.split()[self.id]
            block = False
            if code == "F":
                block = False
            elif code == "T":
                block = True
            return block

    def launch_lvl(self):
        self.labyrinth_file.set_value("levels/" + str(self.id) + ".txt")
        self.active_screen.set_value("main_screen")

    def update_pic(self, opacity=255):
        img_surf = pygame.image.load(self.img_file)
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(img_surf, img_rect)

    def update(self):
        if self.pressed:
            # self.img_file = "pressed_" + str(self.id) + "_lvl_button.png"
            self.img_file = "assets/buttons/pressed_" + str(self.id) + "_lvl_button.png"
        else:
            self.img_file = "assets/buttons/" + str(self.id) + "_lvl_button.png"
        self.update_pic()

    def get_width(self):
        """
        возвращает ширину кнопки
        """
        return self.unit_width

    def get_height(self):
        """
        возвращает высоту кнопки
        """
        return self.unit_height


class Notification:

    def __init__(self):
        """
        Уведомления
        """
        pass

    def update(self):
        pass
