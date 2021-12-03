import pygame


class EventProcessor:

    def __init__(self, _game):
        self.game = _game
        self.start_button = self.game.screen_controller.start_screen_saver.start_button
        self.exit_button = self.game.screen_controller.start_screen_saver.exit_button
        self.back_to_levels_button = self.game.screen_controller.main_screen_saver.back_to_levels_button
        self.task_button = self.game.screen_controller.main_screen_saver.task_button
        self.level_buttons = self.game.screen_controller.level_screen_saver.level_buttons
        self.quit = False
        self.main_hero = self.game.main_hero
        self.labyrinth = self.game.labyrinth
        self.characters = self.game.characters

    def global_event_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                continue
            if self.game.active_screen == "main_screen":
                if event.type == pygame.KEYDOWN and not self.game.main_hero.move_blocked:
                    self.move_main_hero(event)
                else:
                    self.screen_buttons_check(event, self.back_to_levels_button)
                    self.screen_buttons_check(event, self.task_button)
            elif self.game.active_screen == "level_screen":
                for button in self.level_buttons:
                    self.screen_buttons_check(event, button)
            elif self.game.active_screen == "start_screen":
                self.screen_buttons_check(event, self.start_button)
                self.screen_buttons_check(event, self.exit_button)

    def move_main_hero(self, event):
        if event.key == pygame.K_a and self.main_hero.arrival_x != 0 and not self.main_hero.inside_elevator:
            if not self.labyrinth.get_room(self.main_hero.x - 1, self.main_hero.y, self.main_hero.z).type == "block":
                self.main_hero.move_x_axis(-1)
        elif event.key == pygame.K_d and self.main_hero.arrival_x != self.labyrinth.width - 1 and \
                not self.main_hero.inside_elevator:
            if not self.labyrinth.get_room(self.main_hero.x + 1, self.main_hero.y, self.main_hero.z).type == "block":
                self.main_hero.move_x_axis(1)
        # лифт
        elif event.key == pygame.K_f:
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
        elif event.key == pygame.K_w:
            if self.main_hero.z != self.labyrinth.depth - 1 and self.have_a_door(
                    "behind") and not self.main_hero.inside_elevator:
                self.main_hero.move_z_axis(1)
                self.game.sounds_controller.play_sound("door_open")
        elif event.key == pygame.K_s:
            if self.main_hero.z != 0 and self.have_a_door("front") and not self.main_hero.inside_elevator:
                self.main_hero.move_z_axis(-1)
                self.game.sounds_controller.play_sound("door_open")

    def screen_buttons_check(self, event, button):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.check_button_click(button) and button.pressed:
                button.click()
                button.pressed = False
                self.game.sounds_controller.play_sound("button_click")

        if event.type == pygame.MOUSEMOTION:
            if not self.check_button_click(button):
                button.pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_button_click(button):
                button.pressed = True

    def have_a_door(self, direction):
        """
        функция проверяет наличие двери в ячейке нахождения персонажа
        """
        if direction == "behind":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z).type == "door"
        elif direction == "front":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z - 1).type == "door"

    def have_an_elevator(self, direction):
        """
        функция проверяет наличие лифта в ячейке нахождения персонажа (вдруг клавиша будет нажата случайно)
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

    @staticmethod
    def check_button_click(button):
        """
        Проверяет нажатие мыши по кнопкам на экране
        """
        button_x, button_y = button.get_cords()
        button_width = button.get_width()
        button_height = button.get_height()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return button_x - button_width // 2 <= mouse_x <= button_x + button_width // 2 and \
            button_y - button_height // 2 <= mouse_y <= button_y + button_height // 2

    def set_active_screen(self, screen_name: str):
        self.game.active_screen = screen_name

    def update_events_statuses_and_objects_cords(self):
        # FIXME мб сразу давать ссылку на следующую функцию?
        self.global_event_process()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
