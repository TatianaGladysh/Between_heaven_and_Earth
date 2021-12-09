class GameMainProcessController:

    def __init__(self, _game):
        self.game = _game
        self.characters = self.game.characters
        self.active_characters = []
        self.passed_characters = []
        self.upcoming_characters = self.characters.copy()
        self.main_hero = self.game.main_hero
        self.max_stage = 0
        self.active_stage = 0
        self.level_complete = False

    def __define_max_stage(self):
        _max_stage = 0
        for character in self.characters:
            if character.appearance_stage > _max_stage:
                _max_stage = character.appearance_stage
        self.max_stage = _max_stage

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "active_stage":
            self.__update_active_characters_array()
            try:
                self.game.screen_controller.main_screen_saver.notification_screen.active_stage = self.active_stage
            except AttributeError:
                print("screen_controller is not announced yet")

    def set_game_params(self, _main_hero, _characters):
        self.main_hero = _main_hero
        self.characters = _characters
        self.upcoming_characters = self.characters.copy()
        self.__update_active_characters_array()
        self.__define_max_stage()
        self.game.screen_controller.main_screen_saver.notification_screen.draw_spawn_animations()
        self.game.screen_controller.main_screen_saver.notification_screen.coming_characters = self.upcoming_characters
        self.game.screen_controller.main_screen_saver.notification_screen.recalculate_order_of_quests()

    def __update_active_characters_array(self):
        for character in self.upcoming_characters:
            if character.appearance_stage == self.active_stage:
                self.upcoming_characters.remove(character)
                self.active_characters.append(character)

    def __quest_complete_check(self):
        for active_character in self.active_characters:
            if active_character.check_task_completion():
                self.active_characters.remove(active_character)
                self.passed_characters.append(active_character)
                self.game.screen_controller.main_screen_saver.notification_screen.recalculate_order_of_quests()
                if len(self.active_characters) == 0:
                    self.active_stage += 1
                    self.game.screen_controller.main_screen_saver.notification_screen.draw_spawn_animations()

    def update(self):
        self.__quest_complete_check()
        if self.active_stage > self.max_stage and not self.level_complete:
            self.level_complete = True
            self.game.complete_level()
        else:
            self.__update_active_characters_array()
