
def input_labyrinth(input_filename, numbers_floor):
    floor = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            name = line.split()[0]
            if name == 'size':
                size = int(line.split()[2])
            if name == numbers_floor:
                axe_x = []
                list_symbol = line.split()
                for i in range(1, len(list_symbol)):
                    if list_symbol[i] == '0':
                        axe_x.append('empty')
                    if list_symbol[i] == 'd':
                        axe_x.append('door')
                    if list_symbol[i] == 'e':
                        axe_x.append('elevator')
                    if list_symbol[i] == 'x':
                        axe_x.append('block')
                floor.append(axe_x)
    return floor


def labyrinth_transform(floor, number):
    for i in range(len(floor)):
        for j in range(len(floor[i])):
            if floor[i][j] == 'empty':
                floor[i][j] = Room([j, number, i], 'empty')
            if floor[i][j] == 'block':
                floor[i][j] = Room([j, number, i], 'block')
            if floor[i][j] == 'elevator':
                floor[i][j] = Room([j, number, i], 'elevator')
            if floor[i][j] == 'door':
                floor[i][j] = Room([j, number, i], 'door')
    return floor


class Labyrinth:
    def __init__(self, filename):
        """
        Инициализация трехмерного лабиринта. Он разбит на три этажа, чтобы было удобней воспринимать. Каждый этаж -
        двумерный массив, в котором массивы - строчки, параллельные оси Ox, в текстовом файле это прописано.
        """
        self.first_floor = input_labyrinth(filename, '1')
        self.second_floor = input_labyrinth(filename, '2')
        self.third_floor = input_labyrinth(filename, '3')
        self.first_floor = labyrinth_transform(self.first_floor, 1)
        self.second_floor = labyrinth_transform(self.second_floor, 2)
        self.third_floor = labyrinth_transform(self.third_floor, 3)

    def get_floor(self, number):
        if number == '1':
            return self.first_floor
        if number == '2':
            return self.second_floor
        if number == '3':
            return self.third_floor

    def get_room(self, x, y, z):
        """
        Возвращает комнату по данным координатам
        """
        if y == 1:
            return self.first_floor[z][x]
        if y == 2:
            return self.second_floor[z][x].get_type
        if y == 3:
            return self.third_floor[z][x].get_type


class Room:
    def __init__(self, coordinates, type_of_room):
        self.room_coordinates = coordinates
        self.type = type_of_room

    def get_cords(self):
        return tuple(self.room_coordinates)

    def get_type(self):
        return self.type


# one = Labyrinth('3')
# print(one)
# h = one.get_room(0, 1, 0)
# print(h.get_type())
# input_labyrinth('3', '1')
# print(one.get_floor('1'))
# labyrinth_transform(one.get_floor('1'), 1)
