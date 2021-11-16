# здесь отдельно от всего можно рисовать объекты

from game_field import Room
from heroes import MainHero, Character
from main import WIDTH
import pygame


class Painter:

    def __init__(self, _surf, _rooms, _main_hero, _characters):
        """
        Класс, объект которого может рассчитывать по игровым координатам координаты объектов на экране и отрисовывать их
        :param _surf: surface of the game
        :param _rooms: массив всех комнат игры
        :param _main_hero: объект класса MainHero - главный персонаж игры, которым управляет пользователь
        :param _characters: стальные персонажи игры
        """
        self.surf = _surf
        self.unit_width = WIDTH / 5
        self.unit_height = self.get_unit_height()
        self.unit_depth = self.unit_height * (1 / 3)
        self.zero_x, self.zero_y = _main_hero.get_cords()
        self.rooms = _rooms
        self.main_hero = _main_hero
        self.characters = _characters
        self.img_scale_k = 1

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

    @staticmethod
    def read_img_file(obj):
        """
        Определяет то, какое фото должно быть у объекта по его типу
        (будет дописываться)
        :param obj: объект
        """
        if isinstance(obj, Room):
            obj_type = obj.get_type()
            if obj_type == "elevator":
                return "assets/elevator/close_elevator.png"
            elif obj_type == "empty":
                return "assets/Default_room.png"
            elif obj_type == "door":
                pass
        if isinstance(obj, MainHero):
            pass
        if isinstance(obj, Character):
            pass

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

    def calculate_transparency(self, obj):
        """
        рассчитывает, какая непрозрачность объекта в связи с его расположением по отношению к главному персонажу
        :param obj: объект
        :return: непрозрачность, которую должно иметь изображение объекта
        """
        game_obj_x, game_obj_y, game_obj_z = obj.get_cords()
        game_hero_x, game_hero_y, game_hero_z = self.main_hero.get_cords()
        if game_obj_z == game_hero_z:
            opacity = 255
        elif game_obj_z > game_hero_z:
            opacity = 0
        elif game_obj_z < game_hero_z and game_obj_z <= game_hero_z:
            opacity = 64
        else:
            opacity = 0
        return opacity

    def update_pics(self):
        """
        Обновляет картинки комнат и героев на экране
        """
        self.update_background_pics()
        for room in self.rooms:
            opacity = self.calculate_transparency(room)
            if opacity > 0:
                screen_cords = self.transform_game_cords_in_screen_cords(room)
                x = screen_cords[0]
                y = screen_cords[1] + screen_cords[2]
                self.update_img(x, y, self.read_img_file(room), opacity)

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
        :return:
        """
        img_surf = pygame.image.load(file)
        img_surf = pygame.transform.scale(img_surf, size=self.img_scale_k)
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        self.surf.blit(img_surf, img_rect)
