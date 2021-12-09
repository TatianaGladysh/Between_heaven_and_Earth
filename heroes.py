import pygame
import json

from math import copysign as sign
from random import randint


class Hero:
    """
    Класс героев.
    """

    def __init__(self, _start_position):
        """
        Инициализация героя. Имеет стартовую позицию в лабиринте.
        :param _start_position: Стартовая позиция героя, которая задается в json-файле лабиринта изначально.
        """
        self.x, self.y, self.z = _start_position[0], _start_position[1], _start_position[2]
        self.arrival_x, self.arrival_y, self.arrival_z = self.x, self.y, self.z
        self.img_surf = None

    def get_cords(self):
        """
        Возвращает координаты героя.
        """
        return self.x, self.y, self.z

    def set_surf(self, surf):
        """
        Присваивает поверхность отрисовки героя.
        :param surf: Поверхность,которая присваивается.
        """
        self.img_surf = surf


class MainHero(Hero):
    """
    Класс главного героя, т.е. самого игрока.
    """

    def __init__(self, _game):
        """
        Инициализация главного героя. Изначально изображение направлено вправо (self.walking_direction),
        скорость равна 0. Имеет начальные координаты.
        :param _game: Объект класса Game
        """
        self.game = _game
        self.walking_direction = "right"
        self.read_cords()
        super().__init__((self.x, self.y, self.z))
        self.img_file = "assets/main_hero/stay.png"
        self.img_surf = pygame.image.load(self.img_file).convert_alpha()
        self.max_speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.fps = self.game.fps
        self.epsilon = 0.1
        self.inside_elevator = False
        self.move_blocked = False

    def is_moves(self):
        """
        Проверка, движется ли герой, и возврат True в случае движения и False в обратном случае.
        """
        return self.speed_x ** 2 + self.speed_y ** 2 + self.speed_z ** 2 == 0

    def read_cords(self):
        """
        Сначала считывает координаты главного героя из json-файла, а затем присваивает их главному герою.
        """
        with open(self.game.labyrinth_file, "r") as file:
            main_hero_cords = json.load(file)["main_hero"]["start_cords"]
        self.x = main_hero_cords[0]
        self.y = main_hero_cords[1]
        self.z = main_hero_cords[2]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "inside_elevator":
            try:
                self.game.screen_controller.main_screen_saver.painter.animator.enter_exit_in_elevator()
            except AttributeError:
                print("Main hero is not announced")
            finally:
                self.quest_check()
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file).convert_alpha()

    def move_x_axis(self, move_by_length):
        """
        Движение главного героя по оси x.
        :param move_by_length: Расстояние, на которое перемещается герой. Певроначально либо на 1 вправо,
        либо на 1 влево. В зависимости от направления движения меняется направление героя.
        """
        if self.game.labyrinth.get_x_width() > self.arrival_x + move_by_length >= 0 and abs(
                self.arrival_x - self.x) < 1:
            self.arrival_x += move_by_length
            self.speed_x = sign(self.max_speed, move_by_length)
            if self.speed_x > 0:
                self.walking_direction = "right"
            elif self.speed_x < 0:
                self.walking_direction = "left"

    def move_y_axis(self, move_by_length):
        """
        Движение главного героя по оси y.
        :param move_by_length: Расстояние, на которое перемещается герой. Певроначально либо на 1 вверх,
        либо на 1 вниз.
        """
        self.arrival_y += move_by_length
        self.speed_y = sign(10 * self.max_speed, move_by_length)

    def move_z_axis(self, move_by_length):
        """
        Движение главного героя по оси z.
        :param move_by_length: Расстояние, на которое перемещается герой. Певроначально либо на 1 от нас,
        либо на 1 на нас.
        """
        self.arrival_z += move_by_length
        self.speed_z = sign(self.max_speed, move_by_length)

    def quest_check(self):
        """
        Обновление game_controller.
        """
        self.game.game_controller.update()

    def check_own_and_arrival_pos(self):
        """
        Проверка местоположения героя и возможность движениия по каждой оси.
        Если движение невозможно, скорость обнуляется и герой не двигается, упервшись в стену.
        """
        if abs(self.x - self.arrival_x) < self.epsilon:
            self.speed_x = 0
            self.x = round(self.x)
            self.game.screen_controller.main_screen_saver.painter.animator.end_walking_animations(self)
        if abs(self.y - self.arrival_y) < 3 * self.epsilon:
            self.speed_y = 0
            self.y = round(self.y)
        if abs(self.z - self.arrival_z) < self.epsilon:
            self.speed_z = 0
            self.z = round(self.z)

    def walking_animation_check(self):
        """
        Проверка того, нужна ли анимация движения, и воспроизведение анимации при необходимости.
        """
        if (self.game.screen_controller.main_screen_saver.painter.animator.main_hero_walking_animations == []) and \
                self.speed_x != 0:
            self.game.screen_controller.main_screen_saver.painter.animator.add_walking_animation(self)

    def update(self):
        """
        Обновление героя. Каждый раз определяет, в каком состоянии находится герой и выполняет необходимые команды -
        движение, анимация, отрисовка.
        :return:
        """
        if self.speed_x or self.speed_y or self.speed_z:
            self.check_own_and_arrival_pos()
            if not self.move_blocked:
                self.x += self.speed_x * (1 / self.fps)
                self.y += self.speed_y * (1 / self.fps)
                self.z += self.speed_z * (1 / self.fps)
            self.walking_animation_check()
            self.quest_check()


class Character(Hero):
    """
    Герои, которые не двигаются и привязаны к лабиринту. Первоначально лекторы.
    """

    def __init__(self, _game, _start_position, _name, _appearance_stage):
        """
        Инициализация героя.
        :param _game:
        :param _start_position: Стартовая позиция.
        :param _name: Имя героя(лектора).
        :param _appearance_stage: Порядок, в котором они появляются. Если пройти одного, может появиться другой,
        и так до тех пор, пока не пройти всех.
        """
        self.game = _game
        self.name = _name
        self.appearance_stage = _appearance_stage
        self.inside_elevator = False
        super().__init__(_start_position)
        self.speed_x = 0
        self.max_speed = 100
        self.epsilon = 0.1
        self.fps = self.game.fps
        self.image_file = "assets/none.png"
        self.def_img_and_surf()
        self.quest_is_done = False
        self.quest = Quest(self)

    def def_img_and_surf(self):
        """
        Список возможных персонажей и их статичные изображения. Присваивает изображение и поверхность герою.
        """
        if self.name == "Roma":
            self.image_file = "assets/Heroes/Karas/stay.png"
        elif self.name == "Leonid":
            self.image_file = "assets/Heroes/Leonid/Leonid.png"
        elif self.name == "Khiryanov":
            self.image_file = "assets/Heroes/Khiryanov/stay.png"
        elif self.name == "Kozheva":
            self.image_file = "assets/Heroes/Kozhevnikov/stay.png"
        elif self.name == "Klemeshov":
            self.image_file = "assets/Heroes/Klemeshov/stay.png"
        elif self.name == "Kiselev":
            self.image_file = "assets/Heroes/Kisel/stay.png"
        elif self.name == "Artemiy":
            self.image_file = "assets/Heroes/Artemiy/stay.png"
        self.img_surf = pygame.image.load(self.image_file).convert_alpha()

    def move_x_axis(self):
        """
        Движение героя по оси x.
        """
        if self.arrival_x == self.x:
            move_by_length = (-1) * randint(2, 3)
            if self.block_check(move_by_length):
                self.arrival_x = self.x + move_by_length
                self.speed_x = sign(self.max_speed, move_by_length)

    def block_check(self, move_by_length):
        """
        Возвращает  True или False в зависимости от того, заблокирован проход или нет.
        :param move_by_length: На сколько перемещается.
        """
        return not self.game.labyrinth.get_room(self.x + move_by_length, self.y, self.z).type == "block"

    def update(self):
        """
        Обновление координаты героя.
        """
        self.move_check()
        self.x += self.speed_x * (1 / self.fps)

    def move_check(self):
        """
        Проверка движения героя.
        """
        if abs(self.x - self.arrival_x) < self.epsilon:
            self.speed_x = 0
            self.x = self.arrival_x

    def check_task_completion(self):
        """
        Проверка, выполнил ли игрок задание.
        :return: True else False
        """
        if self.game.main_hero.get_cords() == self.get_cords():
            if self.game.main_hero.inside_elevator == self.inside_elevator:
                self.quest_is_done = True
        return self.quest_is_done


class MapMarker(Character):
    """
    Класс, хранящий в себе метки для обучающего, т.е. 0 уровня. Может использоваться и для других уровней.
    Задания привязываются к конкретной координате, которые хранит этот класс.
    """

    def __init__(self, _game, _start_position, _appearance_object_name: str, _inside_elevator, _appearance_stage):
        """
        :param _game: Объект класса game
        :param _start_position: Координата задания.
        :param _appearance_object_name: Название задания
        :param _inside_elevator: Внутри лифта или нет.
        :param _appearance_stage: Порядок выполнения
        """
        self.name = _appearance_object_name
        super().__init__(_game, _start_position, self.name, _appearance_stage)
        self.inside_elevator = _inside_elevator


class Quest:
    """
    Класс заданий.
    """

    def __init__(self, _character):
        """
        У каждого героя есть задание, которое должен сделать игрок. Они трех типов - неактивное, активное, завершенное.
        :param _character: Герой, которому присваивают задания.
        """
        self.character = _character
        self.indent = 9
        self.screen_x = self.character.game.screen_width // 2
        self.screen_y = 0
        self.unit_height = 0
        self.img_files = self.define_img_file()
        self.active_surf = pygame.image.load(self.img_files[1])
        self.active_surf.set_alpha(255)
        self.done_surf = pygame.image.load(self.img_files[0])
        self.done_surf.set_alpha(128)
        self.coming_surf = pygame.image.load(self.img_files[2])
        self.coming_surf.set_alpha(255)
        self.transform_self_surfs()
        self.working_surface = self.coming_surf
        self.stage = self.character.appearance_stage
        self.surf_rect = self.coming_surf.get_rect(center=(0, 0))
        self.pos_in_order = 0

    def set_pos_in_order(self, number):
        """
        Присваивает  заданию номер его вывода на экран,начиная сверху.
        :param number: Номер задания
        """
        self.pos_in_order = number

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "working_surface":
            self.surf_rect = self.working_surface.get_rect(center=(self.screen_x, self.screen_y))
        if key == "screen_y":
            try:
                self.surf_rect = self.working_surface.get_rect(center=(self.screen_x, self.screen_y))
            except AttributeError:
                print(str(self) + " has no attribute working_surface ")
        if key == "pos_in_order":
            self.new_pos_in_order()

    def transform_self_surfs(self):
        """
        Изменение размеров поверхности задания для правильной отрисовки.
        """
        img_width = self.active_surf.get_width()
        img_height = self.active_surf.get_height()
        unit_width = (9 / 20) * self.character.game.screen_width
        k = unit_width / img_width
        self.unit_height = img_height * k
        self.active_surf = pygame.transform.scale(self.active_surf, (int(img_width * k), int(img_height * k)))
        self.done_surf = pygame.transform.scale(self.done_surf, (int(img_width * k), int(img_height * k)))
        self.coming_surf = pygame.transform.scale(self.coming_surf, (int(img_width * k), int(img_height * k)))

    def define_img_file(self):
        """
        По имени героя ему присваивается задание в трех состояниях. Возвращает список с изображениями.
        """
        if self.character.name == "Leonid":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Roma":
            img_files = ["assets/tasks/1-done.png", "assets/tasks/1-active.png",
                         "assets/tasks/1-coming.png"]
        elif self.character.name == "Khiryanov":
            img_files = ["assets/tasks/2-done.png", "assets/tasks/2-active.png",
                         "assets/tasks/2-coming.png"]
        elif self.character.name == "Kozheva":
            img_files = ["assets/tasks/3-done.png", "assets/tasks/3-active.png",
                         "assets/tasks/3-coming.png"]
        elif self.character.name == "Klemeshov":
            img_files = ["assets/tasks/4-done.png", "assets/tasks/4-active.png",
                         "assets/tasks/4-coming.png"]
        elif self.character.name == "Kiselev":
            img_files = ["assets/tasks/5-done.png", "assets/tasks/5-active.png",
                         "assets/tasks/5-coming.png"]
        elif self.character.name == "Artemiy":
            img_files = ["assets/tasks/6-done.png", "assets/tasks/6-active.png",
                         "assets/tasks/6-coming.png"]
        elif self.character.name == "F_button":
            if self.character.inside_elevator:
                img_files = ["assets/tasks/Education/5-done.png", "assets/tasks/Education/5-active.png",
                             "assets/tasks/Education/5-coming.png"]
            else:
                img_files = ["assets/tasks/Education/7-done.png", "assets/tasks/Education/7-active.png",
                             "assets/tasks/Education/7-coming.png"]
        elif self.character.name == "D_button":
            img_files = ["assets/tasks/Education/1-done.png", "assets/tasks/Education/1-active.png",
                         "assets/tasks/Education/1-coming.png"]
        elif self.character.name == "A_button":
            img_files = ["assets/tasks/Education/2-done.png", "assets/tasks/Education/2-active.png",
                         "assets/tasks/Education/2-coming.png"]
        elif self.character.name == "W_button":
            img_files = ["assets/tasks/Education/3-done.png", "assets/tasks/Education/3-active.png",
                         "assets/tasks/Education/3-coming.png"]
        elif self.character.name == "S_button":
            img_files = ["assets/tasks/Education/4-done.png", "assets/tasks/Education/4-active.png",
                         "assets/tasks/Education/4-coming.png"]
        elif self.character.name == "UP_button":
            img_files = ["assets/tasks/Education/8-done.png", "assets/tasks/Education/8-active.png",
                         "assets/tasks/Education/8-coming.png"]
        elif self.character.name == "DOWN_button":
            img_files = ["assets/tasks/Education/6-done.png", "assets/tasks/Education/6-active.png",
                         "assets/tasks/Education/6-coming.png"]
        else:
            img_files = ["assets/none.png", "assets/none.png", "assets/none.png"]
        return img_files

    def update_working_surface(self):
        """
        Изменение изображения задания в зависимости от прогресса его выполнения.
        """
        if self.stage < self.character.game.game_controller.active_stage or self.character.quest_is_done:
            self.working_surface = self.done_surf
        elif self.stage > self.character.game.game_controller.active_stage:
            self.working_surface = self.coming_surf
        else:
            self.working_surface = self.active_surf

    def new_pos_in_order(self):
        """
        Вычисление координат расположения изображения задания.
        """
        self.screen_y = self.indent + (self.indent + self.unit_height) * self.pos_in_order + self.unit_height // 2
        self.update_working_surface()
        if self.stage == self.character.game.game_controller.active_stage:
            self.surf_rect = self.active_surf.get_rect(center=(self.screen_x, self.screen_y))

    def draw_spawn_animation(self, pos_in_animations_order):
        """
        Вызывает анимацию отрисовки уведомлений в левомверхнем углу.
        :param pos_in_animations_order:
        """
        self.character.game.screen_controller.main_screen_saver.painter.animator.add_quest_animation(
            self, pos_in_animations_order)

    def update(self):
        """
        Совершение draw_itself()
        """
        self.draw_itself()

    def draw_itself(self):
        """
        Отрисовка поверхности задания на экране.
        :return:
        """
        self.character.game.game_surf.blit(self.working_surface, self.surf_rect)
