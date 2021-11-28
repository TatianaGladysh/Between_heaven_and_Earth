# здесь отдельно от всего можно рисовать объекты
import pygame
import labyrinth
import heroes
from animations import Animator

indent = 40


class Painter:

    def __init__(self, _game, _width, _height):
        """
        Класс, объект которого может рассчитывать по игровым координатам координаты объектов на экране и отрисовывать их
        """
        self.game = _game
        self.grid_unit_surf = pygame.image.load("assets/grid_unit.png").convert_alpha()
        self.fps = self.game.fps
        self.surf = self.game.game_surf
        self.window_width = self.game.screen_width
        self.window_height = self.game.screen_height
        self.unit_height, self.unit_width, self.unit_depth = 0, 0, 0
        self.zero_screen_cord_x = 0
        self.zero_screen_cord_y = 0
        self.img_scale_k = 0
        self.labyrinth = self.game.labyrinth
        self.main_hero = self.game.main_hero
        self.characters = self.game.characters
        self.elevator_correction_x = 0
        self.elevator_correction_y = 0
        self.draw_main_hero_in_the_elevator = False
        self.animator = Animator(self)
        self.elevator_inside = ElevatorInside()
        self.grid_cells_cords_and_opacity = []

    def draw_grid_cell(self, x, y, opacity):
        """
        Вызывает отрисовку единицы сетки экрана
        :param x: координаты на экране центра клетки,
        :param y: которую обрамляет рамка
        :param opacity: прозрачность
        """
        self.update_image(self.surf, self.grid_unit_surf, x, y, opacity, self.img_scale_k)

    def update_elevator_correction_cords(self, x, y):
        """
        обновляет значения корректировочных координат персонажа при заходе/выходе из лифта
        :param x: значения корректировочных координат
        :param y: на экране
        """
        self.elevator_correction_x = x
        self.elevator_correction_y = y

    def calculate_unit_lengths(self):
        """
        рассчитывает единичные размеры комнат(по сути, размеры комнат на экране)
        """
        img_surf = pygame.image.load("assets/Default_room.png").convert_alpha()
        img_width = img_surf.get_width()
        img_height = img_surf.get_height()
        k = img_width / img_height
        labyrinth_x_len = self.labyrinth.get_x_width()
        labyrinth_y_len = self.labyrinth.get_y_width()
        self.unit_width = int(min((self.window_width - 2 * indent) / labyrinth_x_len,
                                  k * (self.window_height - 2 * indent) / labyrinth_y_len))
        self.unit_height = int(self.unit_width / k)
        self.unit_depth = int(self.unit_height * 0.18333333333)

    def set_game_params(self, _labyrinth: labyrinth.Labyrinth, _main_hero: heroes.MainHero, _characters):
        """
        при запуске основной части игры устанавливает параметры:
        :param _labyrinth: лабиринт
        :param _main_hero: главный герой
        :param _characters: другие персонажи
        """
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.calculate_unit_lengths()
        self.calculate_scale_k()
        self.calculate_zero_screen_cords()
        self.animator.set_game_params()

    def calculate_zero_screen_cords(self):
        """
        рассчитывает координаты левой верхней клетки на экране
        """
        self.zero_screen_cord_x = int(
            self.window_width / 2 - self.unit_width * self.labyrinth.get_x_width() / 2 + self.unit_width / 2)
        self.zero_screen_cord_y = int(self.window_height / 2 - self.unit_height *
                                      self.labyrinth.get_y_width() / 2 + self.unit_height / 2)

    def calculate_scale_k(self):
        """
        Рассчитыват коэффициент размера изображений
        """
        img_surf = pygame.image.load("assets/Default_room.png").convert_alpha()
        img_height = img_surf.get_height()
        self.img_scale_k = self.unit_height / img_height

    def transform_game_cords_in_screen_cords(self, obj):
        """
        Пересчитывает координыты из игровых в экранные
        :param obj: объект класса Room, MainHero или Character
        :return: координаты объекта на экране
        """
        game_hero_x, game_hero_y, game_hero_z = self.main_hero.get_cords()
        game_obj_x, game_obj_y, game_obj_z = obj.get_cords()
        screen_x = self.zero_screen_cord_x + game_obj_x * self.unit_width
        screen_y = self.zero_screen_cord_y + game_obj_y * self.unit_height
        screen_z = self.unit_depth * (game_obj_z - game_hero_z)
        screen_y -= screen_z
        return screen_x, screen_y

    def update_room_pic(self, room: labyrinth.Room, opacity: int):
        """
        Вызывает функцию отрисовки картинки, подавая в нее соответствующий комнате файл и прозрачность
        :param opacity: непрозрачность
        :param room: объект класса Room
        """
        x, y = self.transform_game_cords_in_screen_cords(room)
        self.update_image(self.surf, room.img_surf, x, y, opacity, self.img_scale_k)
        self.grid_cells_cords_and_opacity.append((x, y, opacity))

    def update_rooms_pics(self):
        """
        Выявляет, какие комнаты нужно отрисовать и вызывает функцию отрисовки
        """

        x0, y0, z0 = self.main_hero.get_cords()
        for i in range(0, self.labyrinth.get_x_width()):
            for j in range(0, self.labyrinth.get_y_width()):
                opacity = 255
                room = self.labyrinth.get_room(i, j, z0)
                if isinstance(room, labyrinth.Room):
                    self.update_room_pic(room, opacity)

        for i in range(-1, 2):
            opacity = 64
            x0, y0, z0 = self.main_hero.get_cords()
            check_room = self.labyrinth.get_room(x0 + i, y0, z0 - 1)
            if check_room.type == "door":
                self.update_room_pic(check_room, opacity)

    def update_grid_img(self):
        """
        вызывает функции обновления клеток сетки
        """
        for params in self.grid_cells_cords_and_opacity:
            self.draw_grid_cell(*params)
        self.grid_cells_cords_and_opacity = []

    def update_all_pics(self):
        """
        Обновляет картинки комнат и героев на экране
        """
        if self.draw_main_hero_in_the_elevator:
            self.update_elevator_inside()
            self.update_main_hero_pic()
            self.update_rooms_pics()
            self.update_grid_img()
        else:
            self.update_elevator_inside()
            self.update_rooms_pics()
            self.update_main_hero_pic()
            self.update_grid_img()

    def update_elevator_inside(self):
        """
        обновляет картинку внутренности лифта
        """
        self.elevator_inside.x, self.elevator_inside.y = self.transform_game_cords_in_screen_cords(self.main_hero)
        self.update_image(self.surf, self.elevator_inside.img_surf, self.elevator_inside.x, self.elevator_inside.y, 255,
                          self.img_scale_k)

    def update_main_hero_pic(self):
        """
        вызывает функцию обновления изображения главного героя
        """
        main_hero_screen_x = self.zero_screen_cord_x + self.main_hero.x * self.unit_width + self.elevator_correction_x
        main_hero_screen_y = self.zero_screen_cord_y + self.main_hero.y * self.unit_height + self.elevator_correction_y
        self.update_image(self.surf, self.main_hero.img_surf, main_hero_screen_x, main_hero_screen_y, 255,
                          self.img_scale_k)

    def update_characters(self):
        pass

    @staticmethod
    def update_image(surf, obj_surf, x, y, opacity, scale_k=1):
        """
        Отрисовывает на экран картинку из файла
        :param y:
        :param x:
        :param obj_surf:
        :param surf: main Surface
        :param scale_k: размер относительно единичной длины
        :param opacity: непрозрачность картинки
        """
        img_width = obj_surf.get_width()
        img_height = obj_surf.get_height()
        img_surf = pygame.transform.scale(obj_surf,
                                          (int(scale_k * img_width), int(scale_k * img_height))).convert_alpha()
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        surf.blit(img_surf, img_rect)

    def update(self):
        """
        вызывает функции обновления рисунков комнат, героев и обновление анимаций
        """
        self.update_all_pics()
        self.animator.update()


class ElevatorInside:

    def __init__(self):
        """
        отвечает за отрисовку лифта изнутри
        """
        self.img_file = "assets/elevator/elevator_inside.png"
        self.img_surf = pygame.image.load(self.img_file).convert_alpha()
        self.screen_x, self.screen_y = -10, -10

    def set_screen_cords(self, x, y):
        self.screen_x = x
        self.screen_y = y

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file).convert_alpha()
