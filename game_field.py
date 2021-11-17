class Room:
    def __init__(self, coordinates, type_of_room):
        self.room_coordinates = coordinates
        self.type = type_of_room

    def get_cords(self):
        return tuple(self.room_coordinates)

    def get_type(self):
        return self.type






