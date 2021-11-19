from game_field import Room


class Labyrinth:
    def __init__(self, _filename):
        """
        Инициализация трехмерного лабиринта. Он разбит на три этажа, чтобы было удобней воспринимать. Каждый этаж -
        двумерный массив, в котором массивы - строчки, параллельные оси Ox, в текстовом файле это прописано.
        """
        self.file = _filename
        self.template, self.width, self.height, self.depth = self.input_labyrinth()

    def input_labyrinth(self):
        with open(self.file, "r") as file:
            lines = file.readlines()  # читаем все строки
            all_layers = []
            layer = []
            for line in lines:
                if line[0] in "xed0":
                    layer.append(list(line[:-1].split()))  # записываем в срез этажи по очереди
                elif layer:
                    all_layers.append(layer)  # добывляем срез в массив со всеми срезами
                    layer = []
        # преобразуем буквы из файла в объекты Room
        x_len = len(all_layers[0][0])
        y_len = len(all_layers[0])
        z_len = len(all_layers)
        template = [[[None] * x_len] * y_len] * z_len
        for i in range(x_len):
            for j in range(y_len):
                for k in range(z_len):
                    template[k][j][i] = self.def_room(all_layers, i, j, k)
        return template, x_len, y_len, z_len

    @staticmethod
    def def_room(letter_cods, x, y, z):
        code = letter_cods[z][y][x]
        room_type = ""
        if code == "0":
            room_type = "empty"
        elif code == "e":
            room_type = "elevator"
        elif code == "d":
            room_type = "door"
        elif code == "x":
            room_type = "block"
        return Room((x, y, z), room_type)

    def get_room(self, x, y, z):
        """
        Возвращает комнату по данным координатам
        """
        return self.template[x][y][z]

    def get_x_width(self):
        return len(self.template[0][0])
