class Hero:
    def __init__(self, _start_position):
        self.labyrinth_position = _start_position
        self.x, self.y, self.z = self.get_cords()

    def get_cords(self):
        return tuple(self.labyrinth_position)


class MainHero(Hero):
    def __init__(self, _start_position):
        super().__init__(_start_position)
        self.inside_elevator = False
        self.img_file = "assets/will_be_made_later.png"

    def check_task(self):
        pass


class Character(Hero):

    def __init__(self, _start_position):
        super().__init__(_start_position)
        self.img_file = "assets/will_be_made_later.png"
