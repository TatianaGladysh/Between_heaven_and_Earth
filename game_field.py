class GameField:
    # поле c клеточками - комнатами
    def __init__(self, program_width, program_height, rooms_in_line=5, rooms_in_column=3):
        self.number_of_cells_in_line = 5
        self.width = 0.8 * program_width
        self.height = 0.7 * program_width
        self.display_rooms = [[Room] * rooms_in_line for _ in range(3)]
        self.room_width = self.width / rooms_in_line
        self.room_heigth = self.heigth / rooms_in_column
        # кажется, так можно задать двумерный массив


class Room:
    # каждая ячейка представлет собой комнату, задаем единообразность
    # coordinates - массив координат определенной комнаты [x, y, z]
    # Есть два типа комнат: 1) спрятанные за дверью(zOy) и 2) находящиеся на главном срезе (xOz), в соответсвии с этим
    # сделано разбиение на два подкласса
    def __init__(self, coordinates):
        """
        Общий класс комнат
        :param coordinates: массив координат комнаты
        """
        self.room_coordinates = coordinates

    def get_cords(self):
        """
        :return: возвращает координаты комнаты
        """
        return tuple(self.room_coordinates)


class BackRoom(Room):
    # Спрятанные за дверьми комнаты, в отличие от других имеют ненулевую координату по y
    def __init__(self, coordinates, number, front_room_number):
        """
        Команты спрятанные за дверьми
        :param coordinates: массив из координат
        :param number: собственныцй номер комнаты
        :param front_room_number: номер комнаты из передней плоскости (xOz) за дверью котрой находится данная
        """
        super().__init__(coordinates)
        self.number = number
        self.front_room_number = front_room_number


class FrontRoom(Room):
    def __init__(self, coordinates, number, type_of_element, number_of_back_room):
        """
        Команты не спрятанные, то есть находящиеся на главной плоскости (xOz)
        :param coordinates: массив координат комнаты
        :param number: собсвтенный номер
        :param type_of_element: тип содержания комнаты ("door" - дверь, "elevator" - лифт, "empty" - пустая)
        :param number_of_back_room: номер комнаты класса BackRoom за дверью (есди есть - число отличное от нуля,
        иначе 0)
        """
        super().__init__(coordinates)
        self.number = number
        self.back_room_number = number_of_back_room
        self.type = type_of_element

    def get_type(self):
        """
        :return: возвращает тип содержания комнаты
        """
        return self.type


def file_reading(file_name):
    """
    Читает файлы
    :param file_name: имя входного файла
    :return: возвращает массив комнат определенного типа
    """
    rooms_massive = []
    with open(file_name) as file:
        # в первой строке записано количество комнат этого типа
        count_of_rooms = int(file.readline(1))
        for i in range(2, count_of_rooms + 1):
            line = file.readline(i)
            line_data = line.split()
            # массив с координатами комнаты
            massive_of_coordinates = [int(line_data[0]), int(line_data[1]), int(line_data[2])]
            room_number = int(line_data[3])
            # Если координата по y комнат = 0, то она принадлежит классу FrontRoom
            if massive_of_coordinates[1] == 0:
                type_of_element = line_data[4]
                number_of_back_room = int(line_data[5])
                rooms_massive.append(
                    FrontRoom(massive_of_coordinates, room_number, type_of_element, number_of_back_room))
            # Иначе это BackRoom
            else:
                front_room_number = int(line_data[4])
                rooms_massive.append(BackRoom(massive_of_coordinates, room_number, front_room_number))
    return rooms_massive
