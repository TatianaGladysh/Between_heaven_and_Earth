import pygame


class Button:

    def __init__(self, _command, _surf, _window_width, _window_height):
        """
        Кнопка на начальном экране игры
        """
        self.window_height = _window_height
        self.window_width = _window_width
        self.command = _command
        self.surf = _surf
        self.pressed = False
        self.x = 0
        self.y = 0
        self.unit_width = 0
        self.unit_height = 0

    def click(self):
        """
        Вызывает функцию, привязанную к кнопке
        """
        self.command()

    def get_cords(self):
        """
        возвращает координаты верхнего левого угла кнопки
        """
        return self.x, self.y

    def get_width(self):
        """
        возвращает ширину кнопки
        """
        return self.unit_width

    def get_height(self):
        """
        возвращает высоту кнопки
        """
        return self.unit_height


class StartButton(Button):

    def __init__(self, _surf, _window_width, _window_height, _active_screen):
        """
        Кнопка старта на начальном экране игры
        """
        super().__init__(self.start, _surf, _window_width, _window_height)
        self.img_file = "assets/buttons/start_button.png"
        self.img_surf = pygame.image.load(self.img_file)
        self.img_height = self.img_surf.get_height()
        self.img_width = self.img_surf.get_width()
        self.active_screen = _active_screen
        self.x, self.y, self.scale_k, self.unit_width, self.unit_height = self.calculate_cords()

    def calculate_cords(self):
        """
        Рассчитывает координаты, коэффициент размера, длину и высоту картинки кнопки старта
        :return: координаты, коэффициент размера, длину и высоту
        """
        img_rect = pygame.image.load("assets/backgrounds/start_background.png").get_rect()
        img_width = img_rect.width
        img_height = img_rect.height
        unit_width = self.window_width // 4
        k = unit_width / img_width
        unit_height = k * img_height
        x = self.window_width // 2
        y = self.window_height // 2
        return x, y, k, unit_width, unit_height

    def update(self):
        """
        обновляет изображение, которое должно быть у кнопки
        """
        if self.pressed:
            self.img_file = "assets/buttons/pressed_start_button.png"
        else:
            self.img_file = "assets/buttons/start_button.png"

        self.img_surf = pygame.image.load(self.img_file)
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.update_pic()

    def update_pic(self):
        """
        обновляет картинку кнопки
        """
        self.update_image(255)

    def update_image(self, opacity):
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.img_surf.set_alpha(opacity)
        img_rect = self.img_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(self.img_surf, img_rect)

    def start(self):
        self.pressed = False
        self.active_screen.set_value("level_screen")


class LevelButton(Button):

    def __init__(self, _surf, _window_width, _window_height, _x, _y, _active_screen, _id, _labyrinth_file):
        self.id = _id
        super(LevelButton, self).__init__(self.launch_lvl, _surf, _window_width, _window_height)
        self.active_screen = _active_screen
        self.x = _x
        self.y = _y
        self.block = self.adopted_from_file()
        self.img_file = self.read_img_file()
        self.pressed = False
        self.labyrinth_file = _labyrinth_file
        self.width, self.height = self.calculate_dimensions()
        self.unit_width, self.unit_height = self.width, self.height

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "img_file":
            self.img_surf = pygame.image.load(self.img_file)
        elif key == "pressed":
            if self.pressed:
                self.img_file = "assets/buttons/pressed_" + str(self.id) + "_lvl_button.png"
            else:
                self.img_file = "assets/buttons/" + str(self.id) + "_lvl_button.png"

    @staticmethod
    def calculate_dimensions():
        img_surf = pygame.image.load("assets/buttons/0_lvl_button.png")
        return img_surf.get_width(), img_surf.get_height()

    def read_img_file(self):
        img_file = "assets/buttons/" + str(self.id) + "_lvl_button.png"
        return img_file

    def adopted_from_file(self):
        with open("levels/button_lock_data.txt", 'r') as file:
            string_with_data = file.readline()
            code = string_with_data.split()[self.id]
            block = False
            if code == "F":
                block = False
            elif code == "T":
                block = True
            return block

    def launch_lvl(self):
        self.labyrinth_file.set_value("levels/" + str(self.id) + ".txt")
        self.active_screen.set_value("main_screen")

    def update_pic(self, opacity=255):
        img_surf = self.img_surf
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(self.x, self.y))
        self.surf.blit(img_surf, img_rect)

    def update(self):
        self.update_pic()

    def get_width(self):
        """
        возвращает ширину кнопки
        """
        return self.unit_width

    def get_height(self):
        """
        возвращает высоту кнопки
        """
        return self.unit_height