# здесь отдельно от всего можно рисовать объекты

from main import WIDTH
import pygame


class Painter:

    def __init__(self, _surf, _labyrinth, _main_hero, _characters):
        """
        Класс, объект которого может рассчитывать по игровым координатам координаты объектов на экране и отрисовывать их
        :param _surf: surface of the game
        :param _labyrinth: массив всех комнат игры
        :param _main_hero: объект класса MainHero - главный персонаж игры, которым управляет пользователь
        :param _characters: стальные персонажи игры
        """
        self.surf = _surf
        self.unit_width = WIDTH / 5
        self.unit_height = self.get_unit_height()
        self.unit_depth = self.unit_height * (1 / 3)
        self.zero_x, self.zero_y = _main_hero.get_cords()
        self.main_hero_screen_x = self.zero_x
        self.main_hero_screen_y = self.zero_y
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.img_scale_k = self.calculate_scale_k()
        self.animator = Animator()

    def get_unit_height(self):
        """
        рассчитывает единичную высоту (которую должна иметь картинка на экране)
        :return: единичная высота
        """
        img_surf = pygame.image.load("assets/Default_room.png")
        img_rect = img_surf.get_rect()
        k = img_rect.height / img_rect.width
        return k * self.unit_width

    def calculate_scale_k(self):
        """
        Рассчитыват коэффициент размера изображений
        """
        img_surf = pygame.image.load("assets/Default_room.png")
        img_width = img_surf.get_width()
        return self.unit_width / img_width

    def transform_game_cords_in_screen_cords(self, obj):
        """
        Пересчитывает координыты из игровых в экранные
        :param obj: объект
        :return: координаты объекта на экране(screen_z - проекция его координаты в глубину на плоскость экрана)
        """
        game_obj_x, game_obj_y, game_obj_z = obj.get_cords()
        game_hero_x, game_hero_y, game_hero_z = self.main_hero.get_cords()
        screen_x = self.zero_x * self.unit_width * (game_obj_x - game_hero_x)
        screen_y = self.zero_y * self.unit_height * (game_obj_y - game_hero_y)
        screen_z = self.unit_depth * (game_obj_z - game_hero_z)
        return screen_x, screen_y, screen_z

    def update_room_pic(self, room, opacity):
        """
        Вызывает функцию отрисовки картинки, подавая в нее соответствующий комнате файл и прозрачность
        :param opacity: непрозрачность
        :param room: объект класса Room
        """
        screen_cords = self.transform_game_cords_in_screen_cords(room)
        x = screen_cords[0]
        y = screen_cords[1] + screen_cords[2]
        img_file = room.get_img()
        self.update_image_from_file(self.surf, x, y, img_file, opacity, self.img_scale_k)

    def update_rooms_pics(self):
        """
        Выявляет, какие комнаты нужно отрисовать и вызывает функцию отрисовки
        """
        for i in range(-2, 3):
            for j in range(-1, 2):
                opacity = 255
                x0, y0, z0 = self.main_hero.get_cords()
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
        img_surf = pygame.transform.scale(img_surf, scale_k)
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        surf.blit(img_surf, img_rect)

    def update(self):
        self.update_all_pics()


class Animator:
    pass
