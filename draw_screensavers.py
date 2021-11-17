import pygame
from main import WIDTH, HEIGHT
from draw_all import Painter

pygame.init()

update_image_from_file = getattr(Painter, "update_image_from_file")


class ScreenSaverController:
    def __init__(self, _labyrinth, _main_hero, _characters, _surf, _fps):
        """

        :param _labyrinth: лабиринт с комнатами
        :param _main_hero: главный герой
        :param _characters: другие герои
        :param _surf: Main Surface
        :param _fps: частота обновления кадров
        """
        self.fps = _fps
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.surf = _surf
        self.start_screen_saver = StartScreenSaver(self.surf, self.fps, _active=True)
        self.main_screen_saver = MainScreenSaver(self.labyrinth, self.main_hero, self.characters, self.surf, self.fps,
                                                 _active=False)

    def update(self):
        """
        Вызывает функции обновления объекта отрисовки игровых объектов и интерфейса
        """
        self.surf.fill("WHITE")
        if self.start_screen_saver.active:
            self.start_screen_saver.update()
        elif self.main_screen_saver.active:
            self.main_screen_saver.update()


class MouseController:

    def __init__(self, _start_button):
        """
        Объект класса наблюдает за нажатостью кнопки и за клики по кнопкам на экране
        :param _start_button: кнопка старта
        """
        self.mouse = pygame.mouse
        self.pressed = False
        self.start_button = _start_button
        self.active_screen = "start"

    def check_button_click(self, button):
        """
        Проверяет нажатие мыши по кнопкам на экране
        :param button: кнопка
        """
        if isinstance(button, Button):
            button_x, button_y = button.get_cords()
            button_width = button.get_width()
            button_height = button.get_height()
            mouse_x, mouse_y = self.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                return True
        else:
            return False

    def event_check(self):
        """
        Обрабатывает события мыши
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if self.check_button_click(self.start_button) and self.start_button.pressed:
                    self.active_screen = self.start_button.click()
                    self.start_button.pressed = False

            if event.type == pygame.MOUSEMOTION:
                if not self.check_button_click(self.start_button):
                    self.start_button.pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_button_click(self.start_button):
                    self.start_button.pressed = True

    def update(self):
        """
        Функция обновления проверки событий, связанных с мышью
        """
        self.event_check()


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

    def __init__(self, _surf, _fps, _active=True):
        """
        Объект класса
        :param _surf: Main Surface of the game
        :param _fps: частота обновления кадров игры
        """
        super().__init__(_surf, _fps)
        self.start_button = StartButton(_surf)
        self.active = _active
        self.background_img = "assets/backgrounds/start_background.png"
        self.background_scale_k = self.calculate_background_scale_k()
        self.mouse_controller = MouseController(self.start_button)

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img)
        k = img_surf.get_height() / HEIGHT
        return k

    def background_update(self):
        """
        Обновление картинки заднего плана
        """
        img_surf = pygame.image.load(self.background_img)
        img_surf = pygame.transform.scale(img_surf, size=self.background_scale_k)
        img_rect = img_surf.get_rect()
        self.surf.blit(img_surf, img_rect)

    def update(self):
        """
        Функция обновления изображений кнопок на начальном экране игры и его заднего плана
        """
        self.background_update()
        self.mouse_controller.update()
        self.start_button.update()


class MainScreenSaver(GameScreenSaver):

    def __init__(self, _labyrinth, _main_hero, _characters, _surf, _fps, _active=False):
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
        self.active = _active
        self.painter = Painter(self.surf, self.labyrinth, self.main_hero, self.characters)
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
        for notification in self.notifications:
            notification.update()


class Button:

    def __init__(self, _command, _surf):
        """
        Кнопка на начальном экране игры
        """
        self.command = _command
        self.surf = _surf
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()
        self.pressed = False

    def click(self):
        """
        Вызывает функцию, привязанную к кнопке
        """
        self.command()

    @staticmethod
    def calculate_cords():
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта
        :return: координаты, коэффициент размера, длину и высоту
        """
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = WIDTH // 5
        k = unit_width / img_width
        unit_height = k * img_height
        x = WIDTH // 2 - unit_width // 2
        y = HEIGHT // 2 - unit_height // 2
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

    def __init__(self, _surf):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(self.start, _surf)
        self.img_file = "assets/buttons/start_button.png"
        self.img = pygame.image.load(self.img_file)

    def update(self):
        """
        обновляет изображение, которое должно быть у кнопки
        """
        if self.pressed:
            self.img_file = "assets/buttons/pressed_start_button.png"
        else:
            self.img_file = "assets/buttons/start_button.png"

        self.img = pygame.image.load(self.img_file)
        self.update_pic()

    def update_pic(self):
        """
        обновляет картинку кнопки
        """
        update_image_from_file(self.surf, self.x, self.y, self.img_file, 255, self.scale_k)

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
