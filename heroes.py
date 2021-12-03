from math import copysign as sign
from random import randint
import pygame
import json


class Hero:
    def __init__(self, _start_position):
        self.x, self.y, self.z = _start_position[0], _start_position[1], _start_position[2]
        self.arrival_x, self.arrival_y, self.arrival_z = self.x, self.y, self.z
        self.img_surf = None

    def get_cords(self):
        return self.x, self.y, self.z

    def set_surf(self, surf):
        self.img_surf = surf


class MainHero(Hero):

    def __init__(self, _game):
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

    def read_cords(self):
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
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file).convert_alpha()

    def check_task(self):
        pass

    def move_x_axis(self, move_by_length):
        self.arrival_x = round(self.x + move_by_length)
        self.speed_x = sign(self.max_speed, move_by_length)
        if self.speed_x > 0:
            self.walking_direction = "right"
        elif self.speed_x < 0:
            self.walking_direction = "left"

    def move_y_axis(self, move_by_length):
        self.arrival_y = round(self.y + move_by_length)
        self.speed_y = sign(20 * self.max_speed, move_by_length)

    def move_z_axis(self, move_by_length):
        self.arrival_z = round(self.z + move_by_length)
        self.speed_z = sign(self.max_speed, move_by_length)

    def check_own_and_arrival_pos(self):
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
        if (self.game.screen_controller.main_screen_saver.painter.animator.main_hero_walking_animations == []) and \
                self.speed_x != 0:
            self.game.screen_controller.main_screen_saver.painter.animator.add_walking_animation(self)

    def update(self):
        self.check_own_and_arrival_pos()
        self.walking_animation_check()
        if not self.move_blocked:
            self.x += self.speed_x * (1 / self.fps)
            self.y += self.speed_y * (1 / self.fps)
            self.z += self.speed_z * (1 / self.fps)


class Character(Hero):

    def __init__(self, _game, _start_position, _name, _task, _appearance_stage):
        self.game = _game
        self.task = _task
        self.name = _name
        self.appearance_stage = _appearance_stage
        super().__init__(_start_position)
        self.speed_x = 0
        self.max_speed = 100  # потом
        self.epsilon = 0.1
        self.fps = self.game.fps
        self.image_file = "assets/none.png"
        self.def_img_and_surf()
        self.quest_is_done = False

    def def_img_and_surf(self):
        if self.name == "Roma":
            self.image_file = "assets/none.png"
        elif self.name == "Leonid":
            self.image_file = "assets/none.png"
        elif self.name == "Hiryanov":
            self.image_file = "assets/none.png"
        elif self.name == "Kozheva":
            self.image_file = "assets/none.png"
        elif self.name == "Klemeshov":
            self.image_file = "assets/none.png"
        elif self.name == "Kiselev":
            self.image_file = "assets/none.png"
        self.img_surf = pygame.image.load(self.image_file).convert_alpha()

    def move_x_axis(self):
        if self.arrival_x == self.x:
            move_by_length = (-1) * randint(2, 3)
            if self.block_check(move_by_length):
                self.arrival_x = self.x + move_by_length
                self.speed_x = sign(self.max_speed, move_by_length)

    def block_check(self, move_by_length):
        return not self.game.labyrinth.get_room(self.x + move_by_length, self.y, self.z).type == "block"

    def update(self):
        self.move_check()
        self.x += self.speed_x * (1 / self.fps)

    def move_check(self):
        if abs(self.x - self.arrival_x) < self.epsilon:
            self.speed_x = 0
            self.x = self.arrival_x

    def image_change(self):
        pass
