import numpy as np


class Room:
    def __init__(self, coordinates, type_of_room):
        self.room_coordinates = coordinates
        self.type = type_of_room
        self.img_file = self.def_img_file()

    def get_cords(self):
        return tuple(self.room_coordinates)

    def get_type(self):
        return self.type

    def def_img_file(self):
        if self.type == "empty":
            return "assets/Default_room.png"
        if self.type == "elevator":
            return "assets/elevator/close_elevator.png"
        if self.type == "door":
            # нужно нарисовать картинку комнаты с дверью
            return "assets/door_room.png"
        if self.type == "block":
            # нужно нарисовать картинку закрытой комнаты(стены)
            return "assets/block_room.png"
        if self.type == "none":
            return "assets/none.png"

    def get_img(self):
        return self.img_file

    def set_img(self, filename):
        self.img_file = filename


# FIXME есть какая-то реальная причина делать массив так,
#  чтобы к его координатам приходилось обращаться в обратном порядке? Это очень неудобно


class Labyrinth:
    def __init__(self, _filename):
        """
        Инициализация трехмерного лабиринта. Он разбит на три этажа, чтобы было удобней воспринимать. Каждый этаж -
        двумерный массив, в котором массивы - строчки, параллельные оси Ox, в текстовом файле это прописано.
        """
        self.file = _filename
        self.template, self.width, self.height, self.depth = self.input_labyrinth()
        self.none_room = NoneRoom()

    def input_labyrinth(self):
        with open(self.file.get_value(), "r") as file:
            lines = file.readlines()  # читаем все строки
            all_layers = []
            layer = []
            for line in lines:
                if line[0] in "xed0":
                    layer.append(list(line.split()))  # записываем в срез этажи по очереди
                elif layer:
                    all_layers.append(layer)  # добывляем срез в массив со всеми срезами
                    layer = []
        # преобразуем буквы из файла в объекты Room
        x_len = len(all_layers[0][0])
        y_len = len(all_layers[0])
        z_len = len(all_layers)
        print(x_len, y_len, z_len)
        template = np.zeros((z_len, y_len, x_len), dtype=Room)
        for z_cor in range(z_len):
            for y_cor in range(y_len):
                for x_cor in range(x_len):
                    template[z_cor][y_cor][x_cor] = self.def_room(all_layers, x_cor, y_cor, z_cor)
        return template, x_len, y_len, z_len

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

# one = Labyrinth('3.txt')
# print(one.get_room(2, 1, 1))
