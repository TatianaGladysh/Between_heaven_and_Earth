class Hero:
    def __init__(self, start_position):
        self.labyrinth_position = start_position

    def draw(self):
        pass


class MainHero(Hero):
    def __init__(self):
        super().__init__()
        # self.task

    # в какой клетке нужно оказаться: номер или тип другого героя, координата конечной клетки
    # надо придумать, как кодировать текущее задание

    def check_task(self):
        # выполнил ли герой задание
        pass


class Character(Hero):
    def __init__(self):
        super().__init__()
