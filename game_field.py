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
            return "assets/Default_room.png"
        if self.type == "block":
            # нужно нарисовать картинку закрытой комнаты(стены)
            return "assets/Default_room.png"

    def get_img(self):
        return self.img_file

    def set_img(self, filename):
        self.img_file = filename
