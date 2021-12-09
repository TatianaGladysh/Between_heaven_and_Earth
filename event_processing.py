import pygame


class EventProcessor:
    """
    Класс обработчика событий
    """

    def __init__(self, _game):
        """
        Конструктор класса обработки событий
        :param _game: объект класса Game
        """
        self.game = _game
        self.start_button = self.game.screen_controller.start_screen_saver.start_button
        self.exit_button = self.game.screen_controller.start_screen_saver.exit_button
        self.back_to_levels_button = self.game.screen_controller.main_screen_saver.back_button
        self.task_button = self.game.screen_controller.main_screen_saver.task_button
        self.level_buttons = self.game.screen_controller.level_screen_saver.level_buttons
        self.back_button = self.game.screen_controller.level_screen_saver.back_button
        self.sound_button = self.game.screen_controller.sound_button
        self.quit = False
        self.main_hero = self.game.main_hero
        self.labyrinth = self.game.labyrinth
        self.characters = self.game.characters

    def __global_event_process(self):
        """
        Обработка событий мыши и клавиатуры
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                continue
            self.__sound_button_check_click(event, self.sound_button)
            if self.game.active_screen == "main_screen":
                try:
                    if event.type == pygame.KEYDOWN and not self.game.main_hero.move_blocked:
                        self.__move_main_hero(event)
                    else:
                        self.__screen_buttons_check(event, self.back_to_levels_button)
                        self.__screen_buttons_check(event, self.task_button)
                except AttributeError:
                    print("main_hero is not announced yet")
            elif self.game.active_screen == "level_screen":
                for button in self.level_buttons:
                    self.__screen_buttons_check(event, button)
                self.__screen_buttons_check(event, self.back_button)
            elif self.game.active_screen == "start_screen":
                self.__screen_buttons_check(event, self.start_button)
                self.__screen_buttons_check(event, self.exit_button)

    def __move_main_hero(self, event):
        """
        Перемещение героя в зависимости от действия с клавиатуры
        :param event: нажатие на клавиатуру
        """
        if not self.main_hero.inside_elevator and self.main_hero.speed_z == 0:

            if event.key == pygame.K_a and \
                    self.labyrinth.get_room(self.main_hero.arrival_x - 1, self.main_hero.y,
                                            self.main_hero.z).type != "block":
                self.main_hero.move_x_axis(-1)

            elif event.key == pygame.K_d and \
                    self.labyrinth.get_room(self.main_hero.arrival_x + 1, self.main_hero.y,
                                            self.main_hero.z).type != "block":
                self.main_hero.move_x_axis(1)
        # лифт
        if event.key == pygame.K_f and self.main_hero.is_moves():
            if self.main_hero.inside_elevator:
                # механизм запускающий отрисовку выхождения из лифта
                # (например отдельный параметр True or False)
                self.game.sounds_controller.exit_elevator_sound_play()
                self.game.screen_controller.main_screen_saver.painter.animator.elevator_exit()
                self.main_hero.inside_elevator = False
            elif self.have_an_elevator("here"):
                # в условии проверяет есть ли лифт в том месте где находится персонаж
                # механизм запускающий отрисовку вхождения в лифт
                # (например отдельный параметр True or False,
                # который передается в раздел отрисовки)
                self.game.sounds_controller.enter_elevator_sound_play()
                self.game.screen_controller.main_screen_saver.painter.animator.elevator_entering()
                self.main_hero.inside_elevator = True
        # опускается на один этаж, меняется координата по y
        elif event.key == pygame.K_DOWN and self.main_hero.arrival_y != self.labyrinth.height - 1:
            if self.main_hero.inside_elevator and self.have_an_elevator("below"):
                self.main_hero.move_y_axis(1)
                self.game.sounds_controller.play_sound("elevator_moving")
        # поднимается на один этаж, меняется координата по y
        elif event.key == pygame.K_UP and self.main_hero.arrival_y != 0:
            if self.main_hero.inside_elevator and self.have_an_elevator("overhead"):
                self.main_hero.move_y_axis(-1)
                self.game.sounds_controller.play_sound("elevator_moving")
        # механизм входа в комнату
        elif event.key == pygame.K_w and self.main_hero.is_moves() and \
                self.main_hero.z != self.labyrinth.depth - 1 and \
                self.have_a_door("behind") and not self.main_hero.inside_elevator:
            self.main_hero.move_z_axis(1)
            self.game.sounds_controller.play_sound("door_open")
        elif event.key == pygame.K_s and self.main_hero.is_moves():
            if self.main_hero.z != 0 and self.have_a_door("front") and not self.main_hero.inside_elevator:
                self.main_hero.move_z_axis(-1)
                self.game.sounds_controller.play_sound("door_open")

    @staticmethod
    def __screen_buttons_check(event, button):
        """
        Обработка события мыши
        :param event: событие мыши
        :param button: кнопка
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if button.pressed and button.check_button_click(pygame.mouse.get_pos()):
                button.command()
                button.pressed = False

        if event.type == pygame.MOUSEMOTION:
            if not button.check_button_click(pygame.mouse.get_pos()):
                button.pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.check_button_click(pygame.mouse.get_pos()):
                button.pressed = True

    @staticmethod
    def __sound_button_check_click(event, button):
        """
        Проверка нажатия на кнопку
        :param event: событие мыши
        :param button: кнопка
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.check_button_click(pygame.mouse.get_pos()):
                button.pressed = not button.pressed
                button.command()

    def have_a_door(self, direction):
        """
        функция проверяет наличие двери в ячейке нахождения персонажа
        :param direction: положение двери относительно персонажа
        :return: True/False
        """
        if direction == "behind":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z).type == "door"
        elif direction == "front":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z - 1).type == "door"

    def have_an_elevator(self, direction):
        """
        функция проверяет наличие лифта в ячейке нахождения персонажа (вдруг клавиша будет нажата случайно)
        :param direction: положение лифта относительно персонажа
        :return: True/False
        """
        if direction == "below":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.arrival_y + 1,
                                           self.main_hero.z).type == "elevator"
        elif direction == "overhead":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.arrival_y - 1,
                                           self.main_hero.z).type == "elevator"
        elif direction == "here":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.arrival_y,
                                           self.main_hero.z).type == "elevator"

    def set_active_screen(self, screen_name: str):
        """
        меняет тип экрана игры
        """
        self.game.active_screen = screen_name

    def update(self):
        """
        обновляет игру, запуская обработку всех событий
        """
        self.__global_event_process()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        """
        устанавливает заданные лабиринт, главного героя и персонажей
        :param _labyrinth: лабиринт
        :param _main_hero: главный герой
        :param _characters: персонажи
        """
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
