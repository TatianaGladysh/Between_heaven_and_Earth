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
    # отдельная камната на экране
    def __init__(self, coordinates):
        self.coordinates_in_labyrinth = coordinates

