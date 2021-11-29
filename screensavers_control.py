import pygame
from draw_all import Painter
import numpy as np
from buttons import LevelButton, StartButton, BackToLevelsButton, TaskButton
from animations import QuestAnimation

pygame.init()

LevelsCount = 6


class ScreenSaverController:
    def __init__(self, _game):
        self.game = _game
        self.fps = self.game.fps
        self.labyrinth = self.game.labyrinth
        self.main_hero = self.game.main_hero
        self.characters = self.game.characters
        self.surf = self.game.game_surf
        self.window_height = self.game.screen_height
        self.window_width = self.game.screen_width
        self.level_screen_saver = LevelScreenSaver(self.game)
        self.start_screen_saver = StartScreenSaver(self.game)
        self.main_screen_saver = MainScreenSaver(self.game)
        self.selected_level = None

    def update(self):
        """
        Вызывает функции обновления объекта отрисовки игровых объектов и интерфейса
        """
        self.surf.fill("WHITE")
        if self.game.active_screen == "start_screen":
            self.start_screen_saver.update()
        elif self.game.active_screen == "main_screen":
            self.main_screen_saver.update()
        elif self.game.active_screen == "level_screen":
            self.level_screen_saver.update()
        pygame.display.update()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.set_game_params_to_main_screen_saver()

    def set_game_params_to_main_screen_saver(self):
        self.main_screen_saver.set_game_params(self.labyrinth, self.main_hero, self.characters)


class GameScreenSaver:

    def __init__(self, _game, _background_img):
        self.game = _game
        self.surf = self.game.game_surf
        self.game_time = 0
        self.window_width = self.game.screen_width
        self.window_height = self.game.screen_height
        self.background_img = _background_img
        self.background_surf = pygame.image.load(self.background_img).convert_alpha()
        self.background_scale_k = self.calculate_background_scale_k()

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img).convert_alpha()
        k = self.window_height / img_surf.get_height()
        return k

    def update_background(self):
        """
        Обновление картинки заднего плана
        """
        img_surf = pygame.transform.scale(self.background_surf, (
            int(self.background_surf.get_width() * self.background_scale_k),
            int(self.background_surf.get_height() * self.background_scale_k)))
        img_rect = img_surf.get_rect()
        self.surf.blit(img_surf, img_rect)


class StartScreenSaver(GameScreenSaver):

    def __init__(self, _game):
        self.game = _game
        super(StartScreenSaver, self).__init__(self.game, "assets/backgrounds/start_background.png")
        self.start_button = StartButton(self.game)
        self.window_height = self.game.screen_height
        self.window_width = self.game.screen_width
        self.background_img = "assets/backgrounds/start_background.png"
        self.background_scale_k = self.calculate_background_scale_k()

    def calculate_background_scale_k(self):
        """
        Рассчет коэффициента размера картинки заднего фона
        """
        img_surf = pygame.image.load(self.background_img).convert_alpha()
        k = self.window_height / img_surf.get_height()
        return k

    def update(self):
        """
        Функция обновления изображений кнопок на начальном экране игры и его заднего плана
        """
        self.update_background()
        self.start_button.update()


class MainScreenSaver(GameScreenSaver):

    def __init__(self, _game):
        """
        Главная заставка игры, где пользователь может управлять героем
        :param _game: объект класса Game
        """
        self.game = _game
        self.fps = self.game.fps
        super().__init__(self.game, "assets/backgrounds/main_background.png")
        self.labyrinth = self.game.labyrinth
        self.main_hero = self.game.main_hero
        self.characters = self.game.characters
        self.painter = Painter(self.game, self.game.screen_width, self.game.screen_height)
        self.notifications = []
        self.back_to_levels_button = BackToLevelsButton(self.game)
        self.task_button = TaskButton(self.game)
        self.notification_screen = NotificationsScreen(self)

    def draw_game_space(self):
        """
        функция отрисовки главного пространства игры
        """
        self.update_background()
        self.painter.update()

    def update(self):
        """
        будет обрабатывать действия с уведомлениями
        """
        self.main_hero.update()
        self.draw_game_space()
        self.back_to_levels_button.update()
        self.task_button.update()
        self.notification_screen.update()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
        self.painter.set_game_params(self.labyrinth, self.main_hero, self.characters)
        self.notification_screen.set_quests()


class NotificationsScreen:

    def __init__(self, _main_screen_saver):
        self.quests = []
        self.main_screen_saver = _main_screen_saver
        self.finish = False
        self.active = False
        self.background_surf = pygame.Surface(
            (self.main_screen_saver.game.screen_width, self.main_screen_saver.game.screen_height))
        self.background_surf.set_colorkey("BLACK")
        self.background_opacity = 128
        self.active_stage = 0

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "active_stage":
            self.recalculate_order_of_quests()
            pos_in_anim_order = 0
            for quest in self.find_quests_by_stage(self.active_stage):
                quest.draw_spawn_animation(pos_in_anim_order)
                pos_in_anim_order += 1

    def recalculate_order_of_quests(self):
        correct_quests_queue = [*self.find_quests_by_stage(self.active_stage)]
        for i in range(self.find_max_stage_of_quest() - self.active_stage):
            for quest in self.find_quests_by_stage(i):
                correct_quests_queue.append(quest)
        for i in range(self.active_stage):
            for quest in self.find_quests_by_stage(i):
                correct_quests_queue.append(quest)
        self.quests = correct_quests_queue
        for i in range(len(self.quests)):
            self.quests[i].set_pos_in_order(i)

    def find_quests_by_stage(self, _stage):
        found_quests = []
        for quest in self.quests:
            if quest.stage == _stage:
                found_quests.append(quest)
        return found_quests

    def find_max_stage_of_quest(self):
        max_stage = 0
        for quest in self.quests:
            if quest.stage >= max_stage:
                max_stage = quest.stage
        return max_stage

    def set_quests(self):
        for character in self.main_screen_saver.characters:
            self.add_quest(character)
        self.active_stage = 0

    def add_quest(self, character):
        self.quests.append(Quest(character, self))

    @staticmethod
    def finish_quest(quest):
        quest.finish = True

    def update_background(self):
        Painter.update_image(self.main_screen_saver.game.game_surf, self.background_surf,
                             self.main_screen_saver.game.screen_width // 2,
                             self.main_screen_saver.game.screen_height // 2, self.background_opacity)

    def update(self):
        if self.active:
            self.update_background()
            for quest in self.quests:
                quest.update()


class Quest:

    def __init__(self, _character, _notifications_screen):
        self.notification_screen = _notifications_screen
        self.indent = 20
        self.screen_x = self.notification_screen.main_screen_saver.game.screen_width // 2
        self.screen_y = 0
        self.img_file = "assets/none.png"
        self.unit_width = 0
        self.unit_height = 0
        self.scale_k = 0
        self.opacity = 255
        self.pos_in_quests_order = 0
        self.calculate_screen_params()
        self.character = _character
        self.attached_character = _character
        self.finish = False
        self.stage = self.attached_character.appearance_stage
        self.screen_position = 0

    def calculate_screen_params(self):
        img_surf = pygame.image.load(self.img_file).convert_alpha()
        img_width = img_surf.get_width()
        img_height = img_surf.get_height()
        self.unit_width = self.notification_screen.main_screen_saver.game.screen_width // (3 / 4)
        self.scale_k = self.unit_width / img_width
        self.unit_height = img_height * self.scale_k
        self.screen_x = self.notification_screen.main_screen_saver.game.screen_width // 2
        self.screen_y = (self.indent + self.unit_height) * self.pos_in_quests_order + \
                        self.indent + self.unit_height // 2

    def set_pos_in_order(self, number):
        self.pos_in_quests_order = number
        self.calculate_screen_params()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "notifications_screen":
            if self.notification_screen.active_stage <= self.stage:
                self.img_file = "assets/none.png"
                self.opacity = 200
            elif self.notification_screen.active_stage >= self.stage:
                self.img_file = "assets/none.png"
                self.opacity = 200
            elif self.notification_screen.active_stage == self.stage:
                self.img_file = "assets/none.png"
                self.opacity = 255
        elif key == "img_file":
            self.img_surf = pygame.image.load(self.img_file).convert_alpha()

    def draw_spawn_animation(self, pos_in_animations_order):
        self.notification_screen.main_screen_saver.painter.animator.add_animation(
            QuestAnimation(self, self.notification_screen.main_screen_saver.fps, pos_in_animations_order))

    def update(self):
        self.draw_itself()

    def draw_itself(self):
        Painter.update_image(self.notification_screen.main_screen_saver.game.game_surf, self.img_surf, self.screen_x,
                             self.screen_y, 255, self.scale_k)


class LevelScreenSaver(GameScreenSaver):

    def __init__(self, _game):
        self.game = _game
        super().__init__(self.game, "assets/backgrounds/start_background.png")
        self.window_width = self.game.screen_width
        self.window_height = self.game.screen_height
        self.levels_count = LevelsCount
        self.labyrinth_file = self.game.labyrinth_file
        self.active_screen = self.game.active_screen
        self.level_buttons = self.fill_level_buttons_array()

    def fill_level_buttons_array(self):
        buttons_array = np.zeros(self.levels_count, dtype=LevelButton)
        button_surf = pygame.image.load("assets/buttons/0_lvl_button.png").convert_alpha()
        button_width = button_surf.get_width()
        indent = button_width // 4
        button_height = button_surf.get_height()
        if self.levels_count <= 5:
            zero_button_x = self.window_width // 2 - (
                    (self.levels_count / 2 - 1 / 2) * button_width + (self.levels_count - 1) / 2 * indent)
            for i in range(self.levels_count):
                button_x = zero_button_x + i * (indent + button_width)
                button_y = self.window_height // 2
                buttons_array[i] = LevelButton(button_x, button_y, i, self.game)
        elif self.levels_count <= 10:
            zero_button_x = self.window_width // 2 - (
                    ((self.levels_count + 1) // 2 / 2 - 1 / 2) * button_width + (self.levels_count - 1) / 2 * indent)
            zero_button_y = self.window_height // 2 - button_height // 2 - indent // 2
            for i in range((self.levels_count + 1) // 2):
                button_x = zero_button_x + i * (indent + button_width)
                button_y = zero_button_y
                buttons_array[i] = LevelButton(button_x, button_y, i, self.game)
            zero_button_x = self.window_width // 2 - (
                    ((self.levels_count - (self.levels_count + 1) // 2) / 2 - 1 / 2) * button_width + (
                    self.levels_count - 1) / 2 * indent)
            for i in range((self.levels_count + 1) // 2, self.levels_count):
                button_x = zero_button_x + (i - (self.levels_count + 1) // 2) * (button_width + indent)
                button_y = zero_button_y + indent + button_height
                buttons_array[i] = LevelButton(button_x, button_y, i, self.game)

        return buttons_array

    def update(self):
        self.update_background()
        for button in self.level_buttons:
            button.update()


class Notification:

    def __init__(self):
        """
        Уведомления
        """
        pass

    def update(self):
        pass
