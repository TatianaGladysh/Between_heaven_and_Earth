class GameMainProcessController:

    def __init__(self, _game):
        """
        объект класса обрабатывает массивы героев, обновляет их в связи с выполненными заданиями
        :param _game: объект класса Game
        """
        self.game = _game
        self.characters = self.game.characters
        self.active_characters = []
        self.passed_characters = []
        self.upcoming_characters = self.characters.copy()
        self.main_hero = self.game.main_hero
        self.max_stage = 0
        self.active_stage = 0
        self.level_complete = False

    def clear_params(self):
        """
        очищает параметры при выходе с уровня
        """
        self.active_stage = 0
        self.max_stage = 0
        self.level_complete = False
        self.active_characters.clear()
        self.passed_characters.clear()
        self.upcoming_characters.clear()

    def __define_max_stage(self):
        """
        определяет максимальный этап появления героев
        """
        _max_stage = 0
        for character in self.characters:
            if character.appearance_stage > _max_stage:
                _max_stage = character.appearance_stage
        self.max_stage = _max_stage

    def __setattr__(self, key, value):
        """
        при обновлении стадии игры вызывает обновление массива героев
        :param key: атрибут
        :param value: новое значение
        """
        self.__dict__[key] = value
        if key == "active_stage":
            self.__update_active_characters_array()
            try:
                self.game.screen_controller.main_screen_saver.notification_screen.active_stage = self.active_stage
            except AttributeError:
                print("screen_controller is not announced yet")

    def set_game_params(self, _main_hero, _characters):
        """
        устанавливает параметры героев в себя
        :param _main_hero: герой
        :param _characters: персонажи
        """
        self.main_hero = _main_hero
        self.characters = _characters
        self.upcoming_characters = self.characters.copy()
        self.__update_active_characters_array()
        self.__define_max_stage()
        self.game.screen_controller.main_screen_saver.notification_screen.draw_spawn_animations()
        self.game.screen_controller.main_screen_saver.notification_screen.coming_characters = self.upcoming_characters
        self.game.screen_controller.main_screen_saver.notification_screen.recalculate_order_of_quests()

    def __update_active_characters_array(self):
        """
        обновляет список активных героев
        """
        for character in self.upcoming_characters:
            if character.appearance_stage == self.active_stage:
                self.upcoming_characters.remove(character)
                self.active_characters.append(character)

    def __quest_complete_check(self):
        """
        проверяет выполнение заданий
        """
        for active_character in self.active_characters:
            if active_character.check_task_completion():
                self.active_characters.remove(active_character)
                self.passed_characters.append(active_character)
                self.game.screen_controller.main_screen_saver.notification_screen.recalculate_order_of_quests()
                if len(self.active_characters) == 0:
                    self.active_stage += 1
                    self.game.screen_controller.main_screen_saver.notification_screen.draw_spawn_animations()

    def update(self):
        """
        обновляет себя при вызове (вызывается при изменении координаты главного персонажа
        и его позиции(в лифте или нет))
        """
        self.__quest_complete_check()
        if self.active_stage > self.max_stage and not self.level_complete:
            self.level_complete = True
            self.game.complete_level()
        else:
            self.__update_active_characters_array()
