# здесь отдельно от всего можно рисовать объекты
import pygame
import labyrinth
import heroes

indent = 40


class Painter:

    def __init__(self, _surf: pygame.Surface, _window_width: int, _window_height: int, _labyrinth: labyrinth.Labyrinth,
                 _characters, _main_hero: heroes.MainHero):
        # FIXME неработающая типизация, поэтому пока ее убрала
        # def __init__(self, _surf: pygame.Surface, _window_width: int, _window_height: int,
        #              _labyrinth: labyrinth.Labyrinth,
        #              _characters: list[heroes.Character()], _main_hero: heroes.MainHero):
        """
        Класс, объект которого может рассчитывать по игровым координатам координаты объектов на экране и отрисовывать их
        :param _surf: surface of the game
        :param _labyrinth: массив всех комнат игры
        :param _main_hero: объект класса MainHero - главный персонаж игры, которым управляет пользователь
        :param _characters: остальные персонажи игры
        """
        self.surf = _surf

        self.window_width = _window_width
        self.window_height = _window_height
        self.unit_height, self.unit_width, self.unit_depth = 0, 0, 0
        self.zero_screen_cord_x = 0
        self.zero_screen_cord_y = 0
        self.img_scale_k = 0
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.animator = Animator(self.labyrinth, self.main_hero)
        self.elevator_correction_x = 0
        self.elevator_correction_y = 0
        self.elevator_inside = ElevatorInside()

    def calculate_unit_lengths(self):
        img_surf = pygame.image.load("assets/Default_room.png")
        img_width = img_surf.get_width()
        img_height = img_surf.get_height()
        k = img_width / img_height
        labyrinth_x_len = self.labyrinth.get_x_width()
        labyrinth_y_len = self.labyrinth.get_y_width()
        self.unit_width = int(min((self.window_width - 2 * indent) / labyrinth_x_len,
                                  k * (self.window_height - 2 * indent) / labyrinth_y_len))
        self.unit_height = int(self.unit_width / k)
        self.unit_depth = int(self.unit_height * 0.18333333333)

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.calculate_unit_lengths()
        self.calculate_scale_k()
        self.calculate_zero_screen_cords()
        self.calculate_elevator_correction_cords()
        self.animator.__setattr__("labyrinth", self.labyrinth)
        self.animator.__setattr__("main_hero", self.main_hero)
        self.animator.__setattr__("characters", self.characters)

    def calculate_elevator_correction_cords(self):
        self.elevator_correction_y = - 0.09166 * self.unit_height
        self.elevator_correction_x = - 0.0083 * self.unit_width

    def calculate_zero_screen_cords(self):
        self.zero_screen_cord_x = int(
            self.window_width / 2 - self.unit_width * self.labyrinth.get_x_width() / 2 + self.unit_width / 2)
        self.zero_screen_cord_y = int(self.window_height / 2 - self.unit_height *
                                      self.labyrinth.get_y_width() / 2 + self.unit_height / 2)

    def calculate_scale_k(self):
        """
        Рассчитыват коэффициент размера изображений
        """
        img_surf = pygame.image.load("assets/Default_room.png")
        img_height = img_surf.get_height()
        self.img_scale_k = self.unit_height / img_height

    def transform_game_cords_in_screen_cords(self, obj):
        """
        Пересчитывает координыты из игровых в экранные
        :param obj: объект
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
        img_file = room.get_img()
        self.update_image_from_file(self.surf, x, y, img_file, opacity, self.img_scale_k)

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

    def update_all_pics(self):
        """
        Обновляет картинки комнат и героев на экране
        """
        if self.main_hero.inside_elevator:
            self.update_elevator_inside()
            self.update_main_hero_pic()
            self.update_rooms_pics()
        else:
            self.update_rooms_pics()
            self.update_main_hero_pic()

    def update_elevator_inside(self):
        self.elevator_inside.x, self.elevator_inside.y = self.transform_game_cords_in_screen_cords(self.main_hero)
        self.update_image_from_file(self.surf, self.elevator_inside.x, self.elevator_inside.y,
                                    self.elevator_inside.img_file, 255, self.img_scale_k)

    def update_main_hero_pic(self):
        if not self.main_hero.inside_elevator:
            main_hero_screen_x = self.zero_screen_cord_x + self.main_hero.x * self.unit_width
            main_hero_screen_y = self.zero_screen_cord_y + self.main_hero.y * self.unit_height
            self.update_image_from_file(self.surf, main_hero_screen_x, main_hero_screen_y,
                                        self.main_hero.img_file, 255, self.img_scale_k)
        else:
            main_hero_screen_x = self.zero_screen_cord_x + self.main_hero.x * self.unit_width + \
                self.elevator_correction_x
            main_hero_screen_y = self.zero_screen_cord_y + self.main_hero.y * self.unit_height + \
                self.elevator_correction_y
            self.update_image_from_file(self.surf, main_hero_screen_x, main_hero_screen_y,
                                        self.main_hero.img_file, 255, self.img_scale_k)

    def update_characters(self):
        pass

    def update_img(self, x, y, file, opacity):
        """
        Отрисовывает на экран картинку из файла
        :param x: расположение по горизонтвли центра картинки на экране
        :param y: расположение по вертикали центра картинки на экране
        :param file: файл картинки
        :param opacity: непрозрачность картинки
        """
        img_surf = pygame.image.load(file)
        img_surf = pygame.transform.scale(img_surf, size=self.img_scale_k)
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        self.surf.blit(img_surf, img_rect)

    @staticmethod
    def update_image_from_file(surf, x, y, file, opacity, scale_k):
        """
        Отрисовывает на экран картинку из файла
        :param surf: main Surface
        :param scale_k: размер относительно единичной длины
        :param x: расположение по горизонтвли центра картинки на экране
        :param y: расположение по вертикали центра картинки на экране
        :param file: файл картинки
        :param opacity: непрозрачность картинки
        """
        img_surf = pygame.image.load(file)
        img_width = img_surf.get_width()
        img_height = img_surf.get_height()
        img_surf = pygame.transform.scale(img_surf, (int(scale_k * img_width), int(scale_k * img_height)))
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        surf.blit(img_surf, img_rect)

    def update(self):
        self.update_all_pics()
        self.animator.update()


class Animator:

    def __init__(self, _labyrinth, _main_hero):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero

    def elevator_opening(self):
        elevator_room = self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z)
        elevator_room.set_img("assets/elevator/open_elevator.png")

    def elevator_closing(self):
        elevator_room = self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z)
        elevator_room.set_img("assets/elevator/close_elevator.png")
        # потом сделать чтобы он сначала открывался, потом закрывался

    def enter_exit_in_elevator(self):
        if self.main_hero.inside_elevator:
            self.elevator_opening()
        else:
            self.elevator_closing()

    def update(self):
        pass


class ElevatorInside:
    def __init__(self):
        self.img_file = "assets/elevator/elevator_inside.png"
        self.screen_x, self.screen_y = -10, -10

    def set_screen_cords(self, x, y):
        self.screen_x = x
        self.screen_y = y

# class ExecuteLaterFunc:
#
#     def __init__(self, _fps, _func, _time_interval, _func_args: tuple = tuple()):
#         self.func = _func
#         self.args = _func_args
#         self.time_interval = _time_interval
#         self.dt = 1 / _fps
#
#     def execute(self):
#         self.func(self.args)
#
#     def update(self):
#         self.time_interval -= self.dt
#         if self.time_interval <= 0:
#             self.execute()
