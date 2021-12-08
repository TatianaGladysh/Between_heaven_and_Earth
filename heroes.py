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

    def is_moves(self):
        return self.speed_x ** 2 + self.speed_y ** 2 + self.speed_z ** 2 == 0

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

    def move_x_axis(self, move_by_length):
        if self.game.labyrinth.get_x_width() > self.arrival_x + move_by_length >= 0 and abs(
                self.arrival_x - self.x) < 1:
            self.arrival_x += move_by_length
            self.speed_x = sign(self.max_speed, move_by_length)
            if self.speed_x > 0:
                self.walking_direction = "right"
            elif self.speed_x < 0:
                self.walking_direction = "left"

    def move_y_axis(self, move_by_length):
        self.arrival_y += move_by_length
        self.speed_y = sign(10 * self.max_speed, move_by_length)

    def move_z_axis(self, move_by_length):
        self.arrival_z += move_by_length
        self.speed_z = sign(self.max_speed, move_by_length)

    def quest_check(self):
        self.game.game_controller.quest_complete_check()

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
        if self.speed_x or self.speed_y or self.speed_z:
            self.check_own_and_arrival_pos()
            if not self.move_blocked:
                self.x += self.speed_x * (1 / self.fps)
                self.y += self.speed_y * (1 / self.fps)
                self.z += self.speed_z * (1 / self.fps)
            self.walking_animation_check()
            self.quest_check()


class Character(Hero):

    def __init__(self, _game, _start_position, _name, _task, _appearance_stage):
        self.game = _game
        self.task = _task
        self.name = _name
        self.appearance_stage = _appearance_stage
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
        if self.name == "Roma":
            self.image_file = "assets/Heroes/Karas/stay.png"
        elif self.name == "Leonid":
            self.image_file = "assets/Heroes/Leonid/Leonid.png"
        elif self.name == "Hiryanov":
            self.image_file = "assets/Heroes/Khiryanov/stay.png"
        elif self.name == "Kozheva":
            self.image_file = "assets/Heroes/Kozhevnikov/stay.png"
        elif self.name == "Klemeshov":
            self.image_file = "assets/Heroes/Klemeshov/stay.png"
        elif self.name == "Kiselev":
            self.image_file = "assets/Heroes/Kisel/stay.png"
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


class Quest:

    def __init__(self, _character):
        self.character = _character
        self.indent = 20
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
        img_width = self.active_surf.get_width()
        img_height = self.active_surf.get_height()
        unit_width = (3 / 5) * self.character.game.screen_width
        k = unit_width / img_width
        self.unit_height = img_height * k
        self.active_surf = pygame.transform.scale(self.active_surf, (int(img_width * k), int(img_height * k)))
        self.done_surf = pygame.transform.scale(self.done_surf, (int(img_width * k), int(img_height * k)))
        self.coming_surf = pygame.transform.scale(self.coming_surf, (int(img_width * k), int(img_height * k)))

    def define_img_file(self):
        if self.character.name == "Leonid":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Hiryanov":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Roma":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Kozheva":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Klemeshov":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        elif self.character.name == "Kiselev":
            img_files = ["assets/tasks/0-done.png", "assets/tasks/0-active.png",
                         "assets/tasks/0-coming.png"]
        else:
            img_files = ["assets/none.png", "assets/none.png", "assets/none.png"]
        return img_files

    def update_working_surface(self):
        if self.stage < self.character.game.game_controller.active_stage or self.character.quest_is_done:
            self.working_surface = self.done_surf
        elif self.stage > self.character.game.game_controller.active_stage:
            self.working_surface = self.coming_surf
        else:
            self.working_surface = self.active_surf

    def new_pos_in_order(self):
        self.screen_y = self.indent + (self.indent + self.unit_height) * self.pos_in_order + self.unit_height // 2
        self.update_working_surface()
        if self.stage == self.character.game.game_controller.active_stage:
            self.surf_rect = self.active_surf.get_rect(center=(self.screen_x, self.screen_y))

    def draw_spawn_animation(self, pos_in_animations_order):
        self.character.game.screen_controller. \
            main_screen_saver.painter.animator.add_quest_animation(self, pos_in_animations_order)

    def update(self):
        self.draw_itself()

    def draw_itself(self):
        self.character.game.game_surf.blit(self.working_surface, self.surf_rect)
