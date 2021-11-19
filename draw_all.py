# здесь отдельно от всего можно рисовать объекты
import pygame
import labyrinth
import heroes

rooms_in_line = 5
rooms_in_column = 3


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
        self.unit_height = self.window_height / rooms_in_line / 2
        # нужно будет убрать масштабирование FIXME
        self.img_scale_k = self.calculate_scale_k()
        self.unit_width = self.get_unit_width()
        self.unit_depth = self.unit_height * (1 / 3)
        # self.zero_x, self.zero_y, self.zero_z = tuple(_main_hero.get_cords())
        self.main_hero_screen_x = self.window_width // 2
        self.main_hero_screen_y = self.window_height // 2
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.animator = Animator()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters

    def get_unit_width(self):
        """
        рассчитывает единичную ширину (которую должна иметь картинка на экране)
        :return: единичная ширина
        """
        img_surf = pygame.image.load("assets/Default_room.png")
        img_width = img_surf.get_width()
        return img_width * self.img_scale_k

    def calculate_scale_k(self):
        """
        Рассчитыват коэффициент размера изображений
        """
        img_surf = pygame.image.load("assets/Default_room.png")
        img_height = img_surf.get_width()
        return self.unit_height / img_height

    def transform_game_cords_in_screen_cords(self, obj):
        """
        Пересчитывает координыты из игровых в экранные

        :param obj: объект
        :return: координаты объекта на экране(screen_z - проекция его координаты в глубину на плоскость экрана)
        """
        game_obj_x, game_obj_y, game_obj_z = obj.get_cords()
        game_hero_x, game_hero_y, game_hero_z = self.main_hero.get_cords()
        screen_x = self.main_hero_screen_x + self.unit_width * (game_obj_x - game_hero_x)
        screen_y = self.main_hero_screen_y + self.unit_height * (game_obj_y - game_hero_y)
        screen_z = self.unit_depth * (game_obj_z - game_hero_z)
        print(screen_x, screen_y)
        screen_y += screen_z
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
        for i in range(-2, 3):
            for j in range(-1, 2):
                opacity = 255
                if x0 + i >= 0 and y0 + j >= 0 and z0 >= 0:
                    # нужно добавить проверку на максимальный размер
                    room = self.labyrinth.get_room(x0 + i, y0 + j, z0)
                    self.update_room_pic(room, opacity)

        for i in range(-1, 2):
            opacity = 64
            x0, y0, z0 = self.main_hero.get_cords()
            check_room = self.labyrinth.get_room(x0 + i, y0, z0 - 1)
            if check_room.type == "door":
                middle_room = check_room
                left_room = self.labyrinth.get_room(x0 + i - 1, y0, z0 - 1)
                right_room = self.labyrinth.get_room(x0 + i + 1, y0, z0 - 1)
                for room in (left_room, middle_room, right_room):
                    self.update_room_pic(room, opacity)

    def update_all_pics(self):
        """
        Обновляет картинки комнат и героев на экране
        """
        self.update_background_pics()
        self.update_rooms_pics()
        self.update_heroes()

    def update_heroes(self):
        self.update_image_from_file(self.surf, self.main_hero_screen_x, self.main_hero_screen_y,
                                    self.main_hero.img_file, 255, self.img_scale_k)

    def update_background_pics(self):
        """
        Будет отрисовывать задний фон на экране
        """

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
        # добавить анматора


class Animator:
    pass
