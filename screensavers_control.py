import pygame
from draw_all import Painter

pygame.init()


class ScreenSaverController:
    def __init__(self, _surf, _fps, _window_width, _window_height, _active_screen, _labyrinth=None, _main_hero=None,
                 _characters=None):
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
        self.window_height = _window_height
        self.window_width = _window_width
        self.start_screen_saver = StartScreenSaver(self.surf, self.fps, self.window_width, self.window_height,
                                                   _active=True)
        self.main_screen_saver = MainScreenSaver(self.window_width, self.window_height, self.labyrinth, self.main_hero,
                                                 self.characters, self.surf, self.fps)

    def update(self):
        """
        Вызывает функции обновления объекта отрисовки игровых объектов и интерфейса
        """
        self.surf.fill("WHITE")
        if self.active_screen == "start_screen":
            self.start_screen_saver.update()
        elif self.active_screen == "main_screen":
            self.main_screen_saver.update()
        pygame.display.update()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.set_game_params_to_main_screen_saver()

    def set_game_params_to_main_screen_saver(self):
        self.main_screen_saver.set_game_params(self.labyrinth, self.main_hero, self.characters)


class GameScreenSaver:

    def __init__(self, _surf, _fps):
        """
        Объект класса - заставка экрана игры
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        self.surf = _surf
        self.delta_time = 1 / _fps
        self.game_time = 0


class StartScreenSaver(GameScreenSaver):

    def __init__(self, _surf, _fps, _window_width, _window_height, _active=True):
        """
        Объект класса
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        super().__init__(_surf, _fps)
        self.start_button = StartButton(_surf, _window_width, _window_height)
        self.window_height = _window_height
        self.window_width = _window_width
        self.active = _active
        self.background_img = "assets/backgrounds/start_background.png"
        self.background_scale_k = self.calculate_background_scale_k()

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img)
        k = self.window_height / img_surf.get_height()
        return k

    def background_update(self):
        """
        Обновление картинки заднего плана
        """
        img_surf = pygame.image.load(self.background_img)
        img_surf = pygame.transform.scale(img_surf, (
            int(self.window_width * self.background_scale_k), int(self.window_height * self.background_scale_k)))
        img_rect = img_surf.get_rect()
        self.surf.blit(img_surf, img_rect)

    def update(self):
        """
        Функция обновления изображений кнопок на начальном экране игры и его заднего плана
        """
        self.background_update()
        self.start_button.update()


class MainScreenSaver(GameScreenSaver):

    def __init__(self, _window_width, _window_height, _labyrinth, _main_hero, _characters, _surf, _fps):
        """
        Главная заставка игры, где пользователь может управлять героем
        :param _surf: Main Surface of the game
        :param _labyrinth: объект, в котором храняться комнаты лабиринта
        :param _main_hero: главный герой игры
        :param _characters: другие герои игры
        """
        super().__init__(_surf, _fps)
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


class Button:

    def __init__(self, _command, _surf, _window_width, _window_height):
        """
        Кнопка на начальном экране игры
        """
        self.window_height = _window_height
        self.window_width = _window_width
        self.command = _command
        self.surf = _surf
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()
        self.pressed = False

    def click(self):
        """
        Вызывает функцию, привязанную к кнопке
        """
        self.command()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта
        :return: координаты, коэффициент размера, длину и высоту
        """
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 5
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 2 - unit_width // 2
        y = self.window_height // 2 - unit_height // 2
        return x, y, k, unit_width, unit_height

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

    def __init__(self, _surf, _window_width, _window_height):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(self.start, _surf, _window_width, _window_height)
        self.img_file = "assets/buttons/start_button.png"
        self.img_surf = pygame.image.load(self.img_file)
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()

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
        img_rect = self.img_surf.get_rect(center=(self.x + self.unit_width // 2, self.y + self.unit_height // 2))
        self.surf.blit(self.img_surf, img_rect)

    def start(self):
        pass


class Notification:

    def __init__(self):
        """
        Уведомления
        """
        pass

    def update(self):
        pass
