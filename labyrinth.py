import numpy as np
import pygame.image
import json


class Room:
    def __init__(self, coordinates, type_of_room):
        self.room_coordinates = coordinates
        self.type = type_of_room
        self.img_file, self.img_surf = self.def_img_file()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file)

    def get_cords(self):
        return tuple(self.room_coordinates)

    def get_type(self):
        return self.type

    def def_img_file(self):
        if self.type == "empty":
            img_file = "assets/Default_room.png"
            return img_file, pygame.image.load(img_file)
        if self.type == "elevator":
            img_file = "assets/elevator/close_elevator.png"
            return img_file, pygame.image.load(img_file)
        if self.type == "door":
            # нужно нарисовать картинку комнаты с дверью
            img_file = "assets/door_room.png"
            return img_file, pygame.image.load(img_file)
        if self.type == "block":
            # нужно нарисовать картинку закрытой комнаты(стены)
            img_file = "assets/block_room.png"
            return img_file, pygame.image.load(img_file)
        if self.type == "none":
            img_file = "assets/none.png"
            return img_file, pygame.image.load(img_file)

    def get_img(self):
        return self.img_file

    def set_img(self, filename):
        self.img_file = filename
        self.img_surf = pygame.image.load(self.img_file)

    def set_surf(self, surf):
        self.img_surf = surf


# FIXME есть какая-то реальная причина делать массив так,
#  чтобы к его координатам приходилось обращаться в обратном порядке? Это очень неудобно


class Labyrinth:
    def __init__(self, _filename):
        """
        Инициализация трехмерного лабиринта. Он разбит на три этажа, чтобы было удобней воспринимать. Каждый этаж -
        двумерный массив, в котором массивы - строчки, параллельные оси Ox, в текстовом файле это прописано.
        """
        self.file = _filename
        self.none_room = NoneRoom()
        self.width, self.height, self.depth = 0, 0, 0
        self.template = None
        self.input_labyrinth()

    def input_labyrinth(self):
        with open(self.file, "r") as file:
            file_dict = json.load(file)
            labyrinth_layers_dict = file_dict["layers"]
            self.input_rooms(labyrinth_layers_dict)

    def input_rooms(self, labyrinth_layers_dict):
        """
        читает из словаря комнаты и добавляет из в template
        :param labyrinth_layers_dict: часть словаря из json файла, содержащая типы комнат
        """
        all_layers = []
        for layer_name in labyrinth_layers_dict:
            layer = list(
                labyrinth_layers_dict[layer_name][i].split() for i in range(len(labyrinth_layers_dict[layer_name])))
            all_layers.append(layer)
        x_len = len(all_layers[0][0])
        y_len = len(all_layers[0])
        z_len = len(all_layers)
        self.template = np.zeros((z_len, y_len, x_len), dtype=Room)
        for z_cor in range(z_len):
            for y_cor in range(y_len):
                for x_cor in range(x_len):
                    self.template[z_cor][y_cor][x_cor] = self.def_room(all_layers, x_cor, y_cor, z_cor)
        self.width, self.height, self.depth = x_len, y_len, z_len

    @staticmethod
    def def_room(letter_cods, x_cor, y_cor, z_cor):
        code = letter_cods[z_cor][y_cor][x_cor]
        room_type = ""
        if code == "0":
            room_type = "empty"
        elif code == "e":
            room_type = "elevator"
        elif code == "d":
            room_type = "door"
        elif code == "x":
            room_type = "block"
        return Room((x_cor, y_cor, z_cor), room_type)

    def get_room(self, x, y, z):
        """
        Возвращает комнату по данным координатам
        """
        # FIXME надо разобраться с порядком переменных в массиве и сделать здесь проверку
        if x >= 0 and y >= 0 and z >= 0:
            try:
                return self.template[int(z)][int(y)][int(x)]
            except IndexError:
                # print("Room in (" + str(x) + ", " + str(y) + ", " + str(z) + ") does not exist")
                return self.none_room
        else:
            # print("Requested room with negative coordinates")
            return self.none_room

    # FIXME я написала эти функции до перестанови координат лабиринта, потом от них будет лучше избавиться
    # у нас есть отличные свойства лабиринта self.width, .height и .depth
    def get_x_width(self):
        return len(self.template[0][0])

    def get_y_width(self):
        return len(self.template[0])

    def get_z_width(self):
        return len(self.template)


class NoneRoom(Room):
    def __init__(self):
        super(NoneRoom, self).__init__((-10, -10, -10), "none")
