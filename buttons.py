import pygame


class Button:

    def __init__(self, _game):
        """
        Класс кнопок на разных экранах

        :param _game: объект класса Game
        """
        self.game = _game
        self.img_file_pressed = "assets/none.png"
        self.img_file_released = "assets/none.png"
        self.window_height = _game.screen_height
        self.window_width = _game.screen_width
        self.surf = _game.game_surf
        self.pressed = False
        self.img_file_released = "assets/none.png"
        self.img_file_pressed = "assets/none.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.x = 0
        self.y = 0
        self.unit_width = 0
        self.unit_height = 0

    def get_cords(self):
        """
        возвращает координаты верхнего левого угла кнопки
        :return: координаты
        """
        return self.x, self.y

    def get_width(self):
        """
        возвращает ширину кнопки
        :return: ширина
        """
        return self.unit_width

    def get_height(self):
        """
        возвращает высоту кнопки
        :return: высота
        """
        return self.unit_height

    def update_picture(self):
        """
        Обновляет изображение кнопки
        """
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.img_surf.set_alpha(255)
        img_rect = self.img_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.img_surf, img_rect)

    def check_button_click(self, mouse_position):
        """
        Проверяет нажатие мыши по кнопкам на экране

        :param mouse_position: координата мыши на экране
        """
        button_x, button_y = self.get_cords()
        button_width = self.get_width()
        button_height = self.get_height()
        mouse_x, mouse_y = mouse_position
        return button_x - button_width // 2 <= mouse_x <= button_x + button_width // 2 and \
               button_y - button_height // 2 <= mouse_y <= button_y + button_height // 2

    def update(self):
        """
        Обновляет изображение, которое должно быть у кнопки
        """
        if self.pressed:
            self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        else:
            self.img_surf = pygame.image.load(self.img_file_released).convert_alpha()
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.update_picture()

    def command(self):
        """
        Выполняет команду, привязанную к данной кнопке
        """
        pass


class StartButton(Button):

    def __init__(self, _game, _active_screen="start_screen"):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(_game)
        self.img_file_released = "assets/buttons/start_button.png"
        self.img_file_pressed = "assets/buttons/pressed_start_button.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.active_screen = _active_screen
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта

        :return: координаты, коэффициент размера, длину и высоту
        """
        # в расчетах используются специально подобранные параметры
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 4
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 2
        y = self.window_height // 2
        return x, y, k, unit_width, unit_height

    def command(self):
        """
        Переключает экран
        """
        self.pressed = False
        self.game.active_screen = "level_screen"


class ExitButton(Button):

    def __init__(self, _game):
        """
        Кнопка выхода из игры на начальном экране игры
        """
        super().__init__(_game)
        self.img_file_pressed = "assets/buttons/pressed_exit_button.png"
        self.img_file_released = "assets/buttons/exit_button.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта
        :return: координаты, коэффициент размера, длину и высоту
        """
        # в расчетах используются специально подобранные параметры
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 6
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 2
        y = self.window_height * 19 // 30
        return x, y, k, unit_width, unit_height

    def command(self):
        """
        Завершает игру
        """
        self.pressed = False
        self.game.event_processor.quit = True


class LevelButton(Button):

    def __init__(self, _x, _y, _id, _game):
        """
        Создает кнопку уровня

        :param _x: координата центра кнопки по оси OX
        :param _y: координата центра по оси OY
        :param _id: номер кнопки
        :param _game: объект класса Game
        """
        self.id: int = _id
        super(LevelButton, self).__init__(_game)
        self.x = _x
        self.y = _y
        self.block = self.adopted_from_file()
        if not self.block:
            self.img_file_released = "assets/buttons/" + str(self.id) + "_lvl_button.png"
            self.img_file_pressed = "assets/buttons/pressed_" + str(self.id) + "_lvl_button.png"
        else:
            self.img_file_released = "assets/buttons/lock_level_button.png"
            self.img_file_pressed = "assets/buttons/lock_level_button.png"
        self.pressed = False
        self.width = pygame.image.load("assets/buttons/0_lvl_button.png").convert_alpha().get_width()
        self.height = pygame.image.load("assets/buttons/0_lvl_button.png").convert_alpha().get_height()
        self.unit_width, self.unit_height = self.width, self.height
        self.selected_level = 0

    def __setattr__(self, key, value):
        """
        при изменении параметра block для кнопки уровня меняет свои surface' ы и записывает обновленные данные
        о заблокированных уровнях в файл
        :param key:
        :param value:
        :return:
        """
        self.__dict__[key] = value
        if key == "block":
            if self.block:
                self.img_file_released = "assets/buttons/lock_level_button.png"
                self.img_file_pressed = "assets/buttons/lock_level_button.png"
            else:
                self.img_file_released = "assets/buttons/" + str(self.id) + "_lvl_button.png"
                self.img_file_pressed = "assets/buttons/pressed_" + str(self.id) + "_lvl_button.png"

            if hasattr(self.game, "event_processor"):
                print(self.game.event_processor.levels_cheat_active, self.block)
                if self.game.event_processor.levels_cheat_active:
                    with open("levels/button_lock_data.txt", 'r') as file:
                        string_with_data = file.readline()
                        codes_array = list(string_with_data.split())
                        codes_array[self.id] = "T" if self.block else "F"
                        result_string = " ".join(codes_array)
                    with open("levels/button_lock_data.txt", 'w') as file:
                        file.write(result_string)

    def read_img_file(self):
        """
        Считывает подходищую по номеру уровня картинку для кнопки
        """
        img_file = "assets/buttons/" + str(self.id) + "_lvl_button.png"
        return img_file

    def adopted_from_file(self):
        """
        Считывает, открыл или закрыт сейчас данный уровень
        :return: закрыт ли уровень, True/False
        """
        with open("levels/button_lock_data.txt", 'r') as file:
            string_with_data = file.readline()
            code = string_with_data.split()[self.id]
            block = False
            if code == "F":
                block = False
            elif code == "T":
                block = True
            return block

    def command(self):
        """
        Если уровень доступен, открывает его
        """
        if not self.block:
            self.game.labyrinth_file = "levels/" + str(self.id) + ".json"
            self.game.active_screen = "main_screen"
            self.game.screen_controller.level_screen_saver.selected_level = self.id


class BackButton(Button):
    def __init__(self, _game):
        """
        Кнопка возвращения на экран с уровнями на экране игры

        :param _game: объект класса Game
        """
        super().__init__(_game)
        self.img_file_released = "assets/buttons/exit_button.png"
        self.img_file_pressed = "assets/buttons/pressed_exit_button.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки возвращения
        :return: координаты, коэффициент размера, длину и высоту
        """
        # в расчетах используются специально подобранные параметры
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 10
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 10 * 9
        y = self.window_height // 10
        return x, y, k, unit_width, unit_height

    def command(self):
        """
        Переключает на предыдущий экран
        """
        self.pressed = False
        if self.game.active_screen == "level_screen":
            self.game.active_screen = "start_screen"
        elif self.game.active_screen == "main_screen":
            self.game.active_screen = "level_screen"
            self.game.exit_level()


class TaskButton(Button):
    def __init__(self, _game):
        """
        Кнопка открывает список заданий на экране игры

        :param _game: объект класса Game
        """
        super().__init__(_game)
        self.img_file_released = "assets/buttons/tasks_button.png"
        self.img_file_pressed = "assets/buttons/tasks_button_pressed.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки возвращения
        :return: координаты, коэффициент размера, длину и высоту
        """
        # в расчетах используются специально подобранные параметры
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 10
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 10 * 9
        y = self.window_height // 5
        return x, y, k, unit_width, unit_height

    def command(self):
        """
        Открывает окно заданий и временно блокирует движение главного героя
        Или же закрывает окно заданий и позволяет главному герою двигаться
        """
        self.pressed = False
        self.game.main_hero.move_blocked = not self.game.main_hero.move_blocked
        self.game.screen_controller.main_screen_saver.notification_screen.active = \
            not self.game.screen_controller.main_screen_saver.notification_screen.active


class SoundButton(Button):
    def __init__(self, _game):
        """
        Кнопка возвращения на экран с уровнями на экране игры

        :param _game: объект класса Game
        """
        super().__init__(_game)
        self.img_file_released = "assets/buttons/sound_on.png"
        self.img_file_pressed = "assets/buttons/sound_off.png"
        self.img_surf = pygame.image.load(self.img_file_pressed).convert_alpha()
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки возвращения
        :return: координаты, коэффициент размера, длину и высоту
        """
        # в расчетах используются специально подобранные параметры
        img_rect = pygame.image.load("assets/buttons/sound_on.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 15
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 20
        y = self.window_height // 10 * 9
        return x, y, k, unit_width, unit_height

    def command(self):
        """
        Переключает звук
        """
        self.game.sounds_controller.music_on_off()
        self.game.sounds_controller.update()
