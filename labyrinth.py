from enum import Enum # как в лекции 11 числа по программированию
import numpy as np
import game_field


class Labyrinth(Enum):
    def __init__(self, size_x = 5, size_y = 5, size_z = 3):
        # Инициализация трехмерного лабиринта
        # первая координата - ось x, вторая - y, третья - z


        # можно записать лабиринт в кодировке в файл и затем как в проекте Солнечная система считать лабиринт из файла

        self.template = np.zeros(size_x, size_y, size_z)
        self.template =[[[game_field.Room()]*size_x for i in range(size_y)] for i in range(size_z)]

    def get_room(self, x, y, z):
        """
        возвращает объект Room с заданными координатами

        :param x:
        :param y:
        :param z:
        :return:
        """
        return self.template[x][y][z]

# class Cells:
#     def __init__(self):
#         # 0 - пустая клетка
#         # 1 - препятствие
#         # 21 - лестница только вверх
#         # 22 - лестница только вниз
#         # 20 лестница вверх и вниз
#         EMPTY = 0
#         BARRIER = 1
#         ELEVATOR = 2


