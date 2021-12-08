import numpy as np
import pygame.image
import json


class Room:
    """
    Класс комнат. Каждая комната имеет расположение в лабиринте, а также ее тип.
    """
    def __init__(self, coordinates, type_of_room):
        """
        Инициализация комнаты. В соответствии с типом комнаты инициализируется изображение комнаты.
        :param coordinates: Задаются координаты комнаты в лабиринте. Оси направлены так: ось z вглубь (от нас),
        ось x - вправо, ось y - вниз.
        :param type_of_room: Тип комнаты. Всего 4 типа - лифт, пустая комната, комната с дверью (можно идти по оси z
        вглубь), препятствие (стена, блок).
        """
        self.room_coordinates = coordinates
        self.type = type_of_room
        self.img_file, self.img_surf = self.def_img_file()

    def __setattr__(self, key, value):
        """
        Подгружает картинку при задании self.img_surf
        :return: Возвращает загруженное изображение с прозрачным фоном.
        """
        self.__dict__[key] = value
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file).convert_alpha()

    def get_cords(self):
        """
        Возвращает кортеж из координат комнаты.
        """
        return tuple(self.room_coordinates)

    def get_type(self):
        """
        Возвращает тип комнаты.
        """
        return self.type

    def def_img_file(self):
        """
        Возвращает тип комнаты. Основных типов комнаты - 4, для каждого из которых сразу определяется изображение.
        Тип комнаты "none" - тип для класса NoneRoom. Она не отрисовывается.
        """
        if self.type == "empty":
            img_file = "assets/Default_room.png"
            return img_file, pygame.image.load(img_file).convert_alpha()
        if self.type == "elevator":
            img_file = "assets/elevator/close_elevator.png"
            return img_file, pygame.image.load(img_file).convert_alpha()
        if self.type == "door":
            img_file = "assets/door_room.png"
            return img_file, pygame.image.load(img_file).convert_alpha()
        if self.type == "block":
            img_file = "assets/block_room.png"
            return img_file, pygame.image.load(img_file).convert_alpha()
        if self.type == "none":
            img_file = "assets/none.png"
            return img_file, pygame.image.load(img_file).convert_alpha()

    def get_img(self):
        """
        Возвращает изображение комнаты.
        """
        return self.img_file

    def set_img(self, filename):
        """
        Присваивает комнате изображение.
        :param filename: Название файла изображения.
        """
        self.img_file = filename
        self.img_surf = pygame.image.load(self.img_file).convert_alpha()

    def set_surf(self, surf):
        """
        Присваивает комнате поверхность.
        :param surf: Название поверхности.
        """
        self.img_surf = surf


class Labyrinth:
    """
    Класс лабиринта. Игроку виден каждый раз срез параллельно плоскости x0y. Лабиринт состоит из комнат.
    """
    def __init__(self, _filename):
        """
        Инициализация трехмерного лабиринта. Размер может быть в теории любым, но рекомендуется по оси y не более
        4-5 комнат, по оси x - 7-8. По оси z нет ограничений, глубина по этой оси чаще всего и определяет сложность.
        :param _filename: Лабиринт в формате json-файла. Есть модуль конвертера txt_convert_to_json.py,
        чтобы можно было создать в txt формате, а потом переделывать в json-файл.
        """
        self.file = _filename
        self.none_room = NoneRoom()
        self.width, self.height, self.depth = 0, 0, 0
        self.template = None
        self.input_labyrinth()

    def input_labyrinth(self):
        """
        Считывает лабиринт из json-файла и преобразует его в трехмерный массив.
        Считывает в словарь labyrinth_layers_dict срезы по оси z.
        """
        with open(self.file, "r") as file:
            file_dict = json.load(file)
            labyrinth_layers_dict = file_dict["layers"]
            self.input_rooms(labyrinth_layers_dict)

    def input_rooms(self, labyrinth_layers_dict):
        """
        Читает из словаря срезы по оси z и затем каждый текстовый элемент (комнату) преобразует в объект класса Room
        и добавляет в изначально пустой трехмерный массив template.
        :param labyrinth_layers_dict: Словарь, содержащий типы комнат, закодированные символами "x0ed".
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
        """
        Каждый текстовый символ преобразует в объект класса Room.
        :param letter_cods: Один из символов "x0ed"
        :param x_cor: Координата x комнаты
        :param y_cor: Координата y комнаты
        :param z_cor: Координата z комнаты
        """
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
        Возвращает комнату по данным координатам.
        """
        if x >= 0 and y >= 0 and z >= 0:
            try:
                return self.template[int(z)][int(y)][int(x)]
            except IndexError:
                return self.none_room
        else:
            return self.none_room

    def get_x_width(self):
        """
        Возвращает размер лабаринта по оси x.
        """
        return len(self.template[0][0])

    def get_y_width(self):
        """
        Возвращает размер лабаринта по оси y.
        """
        return len(self.template[0])

    def get_z_width(self):
        """
        Возвращает размер лабаринта по оси z.
        """
        return len(self.template)


class NoneRoom(Room):
    """
    Класс комнаты, которая не отрислвывается.
    """
    def __init__(self):
        super(NoneRoom, self).__init__((-10, -10, -10), "none")

