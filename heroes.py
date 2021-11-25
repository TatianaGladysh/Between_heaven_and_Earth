from math import copysign as sign

import pygame.image


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
    def __init__(self, _start_position, _fps, _game):
        super().__init__(_start_position)
        self.img_file = "assets/main_hero.png"
        self.img_surf = pygame.image.load(self.img_file)
        self.dt = 1 / _fps
        self.max_speed = 7
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.epsilon = 0.1
        self.game = _game
        self.inside_elevator = False
        self.move_blocked = False

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "inside_elevator":
            try:
                self.game.screen_controller.main_screen_saver.painter.animator.enter_exit_in_elevator()
            except AttributeError:
                # print("Main hero is not announced")
                pass
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file)

    def check_task(self):
        pass

    def move_x_axis(self, move_by_length):
        self.arrival_x = round(self.x + move_by_length)
        self.speed_x = sign(self.max_speed, move_by_length)

    def move_y_axis(self, move_by_length):
        self.arrival_y = round(self.y + move_by_length)
        self.speed_y = sign(self.max_speed, move_by_length)

    def move_z_axis(self, move_by_length):
        self.arrival_z = round(self.z + move_by_length)
        self.speed_z = sign(self.max_speed, move_by_length)

    def check_own_and_arrival_pos(self):
        if abs(self.x - self.arrival_x) < self.epsilon:
            self.speed_x = 0
            self.x = round(self.x)
        if abs(self.y - self.arrival_y) < self.epsilon:
            self.speed_y = 0
            self.y = round(self.y)
        if abs(self.z - self.arrival_z) < self.epsilon:
            self.speed_z = 0
            self.z = round(self.z)

    def update(self):
        self.check_own_and_arrival_pos()
        if not self.move_blocked:
            self.x += self.speed_x * self.dt
            self.y += self.speed_y * self.dt
            self.z += self.speed_z * self.dt


class Character(Hero):

    def __init__(self, _start_position):
        super().__init__(_start_position)
        self.img_file = "assets/main_hero.png"
