import pygame


class EventProcessor:

    def __init__(self, _active_screen, _start_button, _main_hero=None, _labyrinth=None, _characters=None):
        self.start_button = _start_button
        self.quit = False
        self.active_screen = _active_screen
        self.main_hero = _main_hero
        self.labyrinth = _labyrinth
        self.characters = _characters

    def global_event_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                continue
            # обработка событий с клавиатуры
            if event.type == pygame.KEYDOWN:
                # движение по главной плоскости xOy вдоль x

                if self.active_screen == "main_screen":

                    if event.key == pygame.K_a and self.main_hero.x != 0:
                        self.main_hero.x -= 1
                    elif event.key == pygame.K_d and self.main_hero.x != self.labyrinth.width-1:
                        self.main_hero.x += 1
                    # лифт
                    elif event.key == pygame.K_f:
                        if self.main_hero.inside_elevator:
                            # механизм запускающий отрисовку выхождения из лифта
                            # (например отдельный параметр True or False)
                            self.main_hero.inside_elevator = False
                        elif self.have_an_elevator("here"):
                            # в условии проверяет есть ли лифт в том месте где находится персонаж
                            # механизм запускающий отрисовку вхождения в лифт
                            # (например отдельный параметр True or False,
                            # который передается в раздел отрисовки)
                            self.main_hero.inside_elevator = True
                    # опускается на один этаж, меняется координата по y
                    elif event.key == pygame.K_DOWN and self.main_hero.y != self.labyrinth.height-1:
                        if self.main_hero.inside_elevator and self.have_an_elevator("below"):
                            self.main_hero.y += 1
                    # поднимается на один этаж, меняется координата по y
                    elif event.key == pygame.K_UP and self.main_hero.y != 0:
                        if self.main_hero.inside_elevator and self.have_an_elevator("overhead"):
                            self.main_hero.y -= 1
                    # механизм входа в комнату
                    # FIXME может, дать возможность делать проходные комнаты и
                    # дать возможность выбирать игроку напраление движения как в лифте?
                    elif event.key == pygame.K_e:
                        if self.main_hero.z != self.labyrinth.depth-1 and self.have_a_door("behind"):
                            self.main_hero.z += 1
                        elif self.main_hero.z != 0 and self.have_a_door("front"):
                            self.main_hero.z -= 1

                # мышь

            if self.active_screen == "start_screen":

                # start_button events

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.check_button_click(self.start_button) and self.start_button.pressed:
                        self.set_active_screen("main_screen")
                        self.start_button.pressed = False

                if event.type == pygame.MOUSEMOTION:
                    if not self.check_button_click(self.start_button):
                        self.start_button.pressed = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_button_click(self.start_button):
                        self.start_button.pressed = True

    def have_a_door(self, direction):
        """
        функция проверяет наличие двери в ячейке нахождения персонажа
        """
        if direction == "behind":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z + 1).type == "door"
        elif direction == "front":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z - 1).type == "door"

    def have_an_elevator(self, direction):
        """
        функция проверяет наличие лифта в ячейке нахождения персонажа (вдруг клавиша будет нажата случайно)
        """
        if direction == "below":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y + 1, self.main_hero).type == "elevator"
        elif direction == "overhead":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y - 1, self.main_hero.z).type == "elevator"
        elif direction == "here":
            return self.labyrinth.get_room(self.main_hero.x, self.main_hero.y, self.main_hero.z).type == "elevator"

    @staticmethod
    def check_button_click(button):
        """
        Проверяет нажатие мыши по кнопкам на экране
        """
        button_x, button_y = button.get_cords()
        button_width = button.get_width()
        button_height = button.get_height()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    def set_active_screen(self, screen_name: str):
        self.active_screen.set_value(screen_name)

    def update_events_statuses_and_objects_cords(self):
        # FIXME мб сразу давать ссылку на следующую функцию?
        self.global_event_process()

    def set_game_params(self, _labyrinth, _main_hero, _characters):
        self.labyrinth = _labyrinth
        self.main_hero = _main_hero
        self.characters = _characters
