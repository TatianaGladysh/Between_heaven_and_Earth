import pygame
from draw_all import Painter
import numpy as np
from buttons import LevelButton, StartButton, BackButton, TaskButton, ExitButton, SoundButton
import animations

pygame.init()

TimeScreenSwitchAnimationCorrection = 0.07

LevelsCount = 6
NotificationsIndent = 0


class ScreenSaverController:
    def __init__(self, _game):
        self.game = _game
        self.fps = self.game.fps
        self.labyrinth = self.game.labyrinth
        self.main_hero = self.game.main_hero
        self.active_characters = self.game.game_controller.active_characters
        self.surf = self.game.game_surf
        self.window_height = self.game.screen_height
        self.window_width = self.game.screen_width
        self.level_screen_saver = LevelScreenSaver(self.game)
        self.start_screen_saver = StartScreenSaver(self.game)
        self.main_screen_saver = MainScreenSaver(self.game)
        self.screen_animations = []
        self.active_screen = "start_screen"
        self.loading = False
        self.later_on_funcs = []
        self.sound_button = SoundButton(self.game)

    def start_loading(self):
        self.loading = True

    def end_loading(self):
        self.loading = False

    def add_lightening_screen_animation(self):
        self.later_on_funcs.append(
            animations.LaterOnFunc(self.end_loading, TimeScreenSwitchAnimationCorrection, self.fps))
        self.screen_animations.append(
            animations.AnimationSwitchScreen(self.game, 255, 0, 0, animations.END_OF_SCREEN_ANIMATION_TIME))

    def add_blackout_screen_animation(self):
        self.screen_animations.append(
            animations.AnimationSwitchScreen(self.game, 0, 255, 0, animations.BEGIN_SCREEN_ANIMATION_TIME))
        self.later_on_funcs.append(
            animations.LaterOnFunc(self.start_loading, animations.BEGIN_SCREEN_ANIMATION_TIME,
                                   self.fps))

    def update_screen_animations(self):
        for animation in self.screen_animations:
            if animation.done:
                self.screen_animations.remove(animation)
            else:
                animation.update()

    def set_active_screen(self, _active_screen):
        self.active_screen = _active_screen

    def update_loading_screen(self):
        if self.loading:
            self.surf.fill("BLACK")

    def update_later_on_funcs(self):
        for func in self.later_on_funcs:
            if func.done:
                self.later_on_funcs.remove(func)
            else:
                func.update()

    def update(self):
        """
        Вызывает функции обновления объекта отрисовки игровых объектов и интерфейса
        """
        if self.active_screen == "start_screen":
            self.start_screen_saver.update()
        elif self.active_screen == "main_screen":
            self.main_screen_saver.update()
        elif self.active_screen == "level_screen":
            self.level_screen_saver.update()
        self.update_screen_animations()
        self.update_later_on_funcs()
        self.update_loading_screen()
        self.sound_button.update()
        pygame.display.update()

    def set_game_params(self, _labyrinth, _main_hero, _active_characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.active_characters = _active_characters
        self.set_game_params_to_main_screen_saver()

    def set_game_params_to_main_screen_saver(self):
        self.main_screen_saver.set_game_params(self.labyrinth, self.main_hero, self.active_characters)


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
        self.img_surf = pygame.transform.scale(self.background_surf, (
            int(self.background_surf.get_width() * self.background_scale_k),
            int(self.background_surf.get_height() * self.background_scale_k)))

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
        self.surf.blit(self.img_surf, (0, 0))


class StartScreenSaver(GameScreenSaver):

    def __init__(self, _game):
        self.game = _game
        super(StartScreenSaver, self).__init__(self.game, "assets/backgrounds/start_background.png")
        self.start_button = StartButton(self.game)
        self.exit_button = ExitButton(self.game)
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
        self.exit_button.update()


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
        self.painter = Painter(self.game)
        self.back_button = BackButton(self.game)
        self.task_button = TaskButton(self.game)
        self.notification_screen = NotificationsScreen(self)

    def draw_game_space(self):
        """
        функция отрисовки главного пространства игры
        """
        self.update_background()
        self.painter.update()

    def set_game_params(self, _labyrinth, _main_hero, _active_characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.painter.set_game_params(self.labyrinth, self.main_hero)

    def update(self):
        """
        будет обрабатывать действия с уведомлениями
        """
        try:
            self.main_hero.update()
        except AttributeError:
            print("main_hero is not announced already or yet")
        for character in self.game.game_controller.active_characters:
            character.update()
        self.draw_game_space()
        if self.notification_screen.active:
            self.notification_screen.update()
        self.back_button.update()
        self.task_button.update()


class NotificationsScreen:

    def __init__(self, _main_screen_saver):
        self.main_screen_saver = _main_screen_saver
        self.active = False
        self.background_opacity = 128
        self.background_surf = pygame.Surface(
            (self.main_screen_saver.game.screen_width, self.main_screen_saver.game.screen_height)).convert_alpha()
        self.background_surf.set_alpha(self.background_opacity)
        self.background_surf.fill("BLACK")
        self.active_characters = self.main_screen_saver.game.game_controller.active_characters
        self.coming_characters = self.main_screen_saver.game.game_controller.upcoming_characters
        self.passed_characters = self.main_screen_saver.game.game_controller.passed_characters
        self.active_stage = self.main_screen_saver.game.game_controller.active_stage

    def clear_params(self):
        self.active_stage = 0
        self.active = False

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "active_stage":
            self.recalculate_order_of_quests()

    def draw_spawn_animations(self):
        i = 0
        for character in self.active_characters:
            character.quest.draw_spawn_animation(i)
            i += 1

    def recalculate_order_of_quests(self):
        i = 0
        for character in self.active_characters:
            character.quest.set_pos_in_order(i)
            i += 1
        for character in self.coming_characters:
            character.quest.set_pos_in_order(i)
            i += 1
        for character in self.passed_characters:
            character.quest.set_pos_in_order(i)
            i += 1

    def update_background(self):
        self.main_screen_saver.game.game_surf.blit(self.background_surf, (0, 0))

    def update(self):
        if self.active:
            self.update_background()
            for character in self.active_characters + self.passed_characters + self.coming_characters:
                character.quest.update()


class LevelScreenSaver(GameScreenSaver):

    def __init__(self, _game, _active_screen="start_screen"):
        self.game = _game
        super().__init__(self.game, "assets/backgrounds/start_background.png")
        self.window_width = self.game.screen_width
        self.window_height = self.game.screen_height
        self.levels_count = LevelsCount
        self.labyrinth_file = self.game.labyrinth_file
        self.active_screen = _active_screen
        self.level_buttons = self.fill_level_buttons_array()
        self.back_button = BackButton(self.game)

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
        self.back_button.update()
