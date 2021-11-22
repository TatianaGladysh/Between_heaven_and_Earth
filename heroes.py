class Hero:
    def __init__(self, _start_position):
        self.x, self.y, self.z = _start_position[0], _start_position[1], _start_position[2]
        self.x, self.y, self.z = self.get_cords()

    def get_cords(self):
        return self.x, self.y, self.z


class MainHero(Hero):
    def __init__(self, _start_position):
        super().__init__(_start_position)
        self.inside_elevator = False
        self.img_file = "assets/main_hero.png"

    def check_task(self):
        pass


class Character(Hero):

    def __init__(self, _start_position):
        super().__init__(_start_position)
        self.img_file = "assets/main_hero.png"
