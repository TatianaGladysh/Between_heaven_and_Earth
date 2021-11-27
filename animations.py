import pygame
from labyrinth import Room
from heroes import Hero

QuestAnimationTime = 0.5


class Animator:

    def __init__(self, _painter):
        """
        управляет анимациями, связанными с захождениями в лифт и выхождениями из него
        :param _painter: ссылка на Painter
        """
        self.painter = _painter
        self.elevator_correction_x = _painter.elevator_correction_x
        self.elevator_correction_y = _painter.elevator_correction_y
        self.max_elevator_correction_y = 0
        self.max_elevator_correction_x = 0
        self.images_animations = []
        self.cords_animations = []
        self.later_on_funcs = []
        self.quests_animations = []
        self.dt = 1 / _painter.fps
        self.fps = _painter.fps
        self.processing = False

    def set_game_params(self):
        """
        устанавливает максимальные координаты коррекции для захождения в лифт и выхода из него при рассчете единичных
        длин в painter 'е
        """
        self.max_elevator_correction_y = - 0.09166 * self.painter.unit_height
        self.max_elevator_correction_x = - 0.0083 * self.painter.unit_width
        self.elevator_correction_x, self.elevator_correction_y = \
            self.painter.elevator_correction_x, self.painter.elevator_correction_y

    def add_animation(self, animation):
        """
        добавляет в листы анимаций координат и изображений новую
        :param animation: анимация, которую нужно добавить
        """
        if isinstance(animation, ImageAnimation):
            self.images_animations.append(animation)
        elif isinstance(animation, ElevatorCorrectionCordsAnimation):
            self.cords_animations.append(animation)
        elif isinstance(animation, QuestAnimation):
            self.quests_animations.append(animation)

    def add_later_on_funcs(self, func, delay, args=None):
        """
        добавляет в лист функций, которые нужно сделать через некоторый промежуток времени еще одну
        :param func: функция
        :param delay: задержка
        :param args: аргументы функции
        """
        if args is None:
            args = []
        self.later_on_funcs.append(LaterOnFunc(func, delay, self.painter.fps, args))

    def change_rendering_of_layers(self, value=None):
        """
        изменяет параметр, отвечающий за отрисовку героя в лифте/вне его на противоположный по умолчание или на value
        """
        if value is None:
            self.painter.draw_main_hero_in_the_elevator = not self.painter.draw_main_hero_in_the_elevator
        else:
            self.painter.draw_main_hero_in_the_elevator = value

    def emergency_finish_elevator_animations(self):
        """
        отвечает за вызов быстрого завершения всех анимаций и функций с задержкой лифта
        """
        for animation in self.images_animations:
            animation.emergency_finish()
        for func in self.later_on_funcs:
            func.emergency_finish()
        for animation in self.cords_animations:
            animation.emergency_finish()
        self.images_animations = self.cords_animations = self.later_on_funcs = []

    def elevator_entering(self):
        """
        отвечает за анимацию захождения главного героя в лифт
        завершает анимации с лифтом, которые были вызваны и активны до этого
        """
        self.emergency_finish_elevator_animations()
        self.add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.15))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=0.15, args=[True])
        self.add_animation(ElevatorCorrectionCordsAnimation(self.painter, (self.max_elevator_correction_x,
                                                                           self.max_elevator_correction_y),
                                                            _time_interval=0.15, _fps=self.painter.fps))
        self.add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.15, _delay=0.15))

    def elevator_exit(self):
        """
        отвечает за анимацию выхода главного героя из лифта
        завершает анимации с лифтом, которые были вызваны и активны до этого
        """
        self.emergency_finish_elevator_animations()
        self.add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.15))
        self.add_animation(
            ElevatorCorrectionCordsAnimation(self.painter, (0, 0), _time_interval=0.15, _fps=self.painter.fps,
                                             _delay=0.2))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=0.15, args=[False])
        self.add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.15,
                                     _delay=0.15))

    def update(self):
        """
        обновляет все анимации и функции с задержкой, из соответствующих списков, удаляет из них завершенные,
        если таковые имеются
        :return:
        """
        for animation in self.quests_animations:
            if animation.done:
                self.quests_animations.remove(animation)
            else:
                animation.update()
        for animation in self.images_animations:
            if animation.done:
                self.images_animations.remove(animation)
            else:
                animation.update()
        for animation in self.cords_animations:
            if animation.done:
                self.cords_animations.remove(animation)
            else:
                animation.update()
        for func in self.later_on_funcs:
            if func.done:
                self.later_on_funcs.remove(func)
            else:
                func.update()


class QuestAnimation:

    def __init__(self, _quest, _fps, _pos_in_order):
        self.indent = 20
        self.quest = _quest
        self.img_surf = pygame.image.load(self.quest.img_file)
        self.opacity = 255
        self.dt = 1 / _fps
        self.step_change = (0 - self.opacity) * (self.dt / QuestAnimationTime)
        self.time = 0
        self.done = False
        self.pos_in_order = _pos_in_order
        self.screen_x = 0
        self.screen_y = 0
        self.unit_width = 0
        self.unit_height = 0
        self.scale_k = 0
        self.calculate_params()

    def calculate_params(self):
        self.unit_width = self.quest.notification_screen.main_screen_saver.game.screen_width // 5
        img_width = self.img_surf.get_width()
        img_height = self.img_surf.get_height()
        self.scale_k = self.unit_width / img_width
        self.unit_height = img_height * self.scale_k
        self.screen_x = self.indent + self.unit_width // 2
        self.screen_y = self.indent + self.unit_height // 2 + self.pos_in_order * (self.indent + self.pos_in_order)

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == "quest":
            self.img_surf = pygame.image.load(self.quest.img_file)

    def update_pic(self):
        self.update_image(self.quest.notification_screen.main_screen_saver.game.game_surf, self.img_surf, self.screen_x,
                          self.screen_y, self.opacity, self.scale_k)

    def update(self):
        self.time += self.dt
        if self.time >= QuestAnimationTime:
            self.done = True
        else:
            self.opacity += self.step_change
            self.update_pic()

    @staticmethod
    def update_image(surf, obj_surf, x, y, opacity, scale_k=1):
        """
        Отрисовывает на экран картинку из файла
        :param y:
        :param x:
        :param obj_surf:
        :param surf: main Surface
        :param scale_k: размер относительно единичной длины
        :param opacity: непрозрачность картинки
        """
        img_width = obj_surf.get_width()
        img_height = obj_surf.get_height()
        img_surf = pygame.transform.scale(obj_surf, (int(scale_k * img_width), int(scale_k * img_height)))
        img_surf.set_alpha(opacity)
        img_rect = img_surf.get_rect(center=(x, y))
        surf.blit(img_surf, img_rect)


class ElevatorCorrectionCordsAnimation:
    def __init__(self, _painter, _end_values_cords, _time_interval, _fps, _delay=0.0):
        """
        анимация координат, отвечающая за линейные(пока есть только такие, но возможно только пока) перемещения
        главного героя в лифт и из него
        :param _painter: Painter
        :param _end_values_cords: конечные значения корректировочных координат на экране
        :param _time_interval: время выполнения анимации
        :param _fps: фпс
        :param _delay: задержка перед началом анимации
        """
        self.painter = _painter
        self.variable_x = _painter.elevator_correction_x
        self.variable_y = _painter.elevator_correction_y
        self.end_value_cords = _end_values_cords
        self.time_interval = _time_interval
        self.time = 0
        self.dt = 1 / _fps
        self.delay = _delay
        self.variable_step_x = (_end_values_cords[0] - self.variable_x) / (_time_interval / self.dt)
        self.variable_step_y = (_end_values_cords[1] - self.variable_y) / (_time_interval / self.dt)
        self.done = False

    def change_variables(self):
        """
        изменяет координаты на один шаг и возвращает их в painter
        """
        self.variable_x += self.variable_step_x
        self.variable_y += self.variable_step_y
        self.painter.update_elevator_correction_cords(self.variable_x, self.variable_y)

    def emergency_finish(self):
        """
        мгновенно завершает выполнение анимации
        """
        self.variable_x = self.end_value_cords[0]
        self.variable_y = self.end_value_cords[1]
        self.painter.update_elevator_correction_cords(self.variable_x, self.variable_y)
        self.done = True

    def update(self):
        """
        вызывает обновление координат
        :return:
        """
        self.time += self.dt
        if self.delay <= self.time <= self.delay + self.time_interval and not self.done:
            self.change_variables()
        if self.time > self.delay + self.time_interval:
            self.done = True


class LaterOnFunc:
    def __init__(self, _func, _time_interval, _fps, _args=None):
        """
        объект класса содержит в себе функцию, которую выполнит через время _time_interval
        :param _func: функция
        :param _time_interval: время задержки
        :param _fps: фпс
        :param _args: аргументы функции, по умолчанию None
        """
        if _args is None:
            _args = []
        self.func = _func
        self.time_interval = _time_interval
        self.args = _args
        self.time = 0
        self.dt = 1 / _fps
        self.done = False

    def execute(self):
        """
        вызывает выполнение функции
        :return:
        """
        self.done = True
        self.func(*self.args)

    def emergency_finish(self):
        """
        вызывает быстрое выполнение функции, ранее чем прошло время задержки
        :return:
        """
        self.execute()

    def update(self):
        """
        обновляет время и вызывает выполнение функции по его прошествии
        :return:
        """
        self.time += self.dt
        if self.time_interval <= self.time:
            if not self.done:
                self.execute()


class ImageAnimation:
    id = 0

    def __init__(self, _obj, _frames_files, _time_interval, _fps, _delay, _nature_of_frames_change="linear"):
        """
        объект класса может описывать анимацию, связанную с изменением изображений с течением времени, пока только
        линейным
        :param _obj: объект, у которого следует изменять изображение
        :param _frames_files: файлы изображений в анимации
        :param _time_interval: общее время выполнения анимации
        :param _fps: фпс
        :param _delay: задержка перед началом выполнения функции
        :param _nature_of_frames_change: характер изменения изображений во времени, пока осуществим только линейный
        """
        self.obj = _obj
        self.frames_files = _frames_files
        self.frames_count = len(self.frames_files)
        self.frame_surfaces = self.fill_the_array_of_surfaces()
        self.active_surf_number = 0
        self.active_surf = self.frame_surfaces[0]
        self.time_interval = _time_interval
        self.dt = 1 / _fps
        self.converting_frame_interval = 0
        self.countdown = self.time_interval / len(self.frames_files)
        self.done = False
        self.nature_of_frames_change = _nature_of_frames_change
        self.id = ImageAnimation.id
        self.delay = _delay

    def get_time_of_action(self):
        """
        возвращает время выполнения анимации
        :return:
        """
        return self.time_interval

    def fill_the_array_of_surfaces(self):
        """
        заполняет массив surface 'ов исходя из поданных файлов изображений
        """
        frames_surfaces = []
        for i in range(len(self.frames_files)):
            frames_surfaces.append(pygame.image.load(self.frames_files[i]))
        return frames_surfaces

    def update_frame(self):
        """
        обновляет кадр анимации
        """
        self.active_surf_number += 1
        self.converting_frame_interval = 0
        if self.active_surf_number >= self.frames_count:
            self.finish()
            return
        self.active_surf = self.frame_surfaces[self.active_surf_number]
        if isinstance(self.obj, Room) or isinstance(self.obj, Hero):
            self.obj.set_surf(self.active_surf)
        if self.nature_of_frames_change == "linear":
            pass
        # при нелинейной анимации можно будет изменять время cool_count

    def emergency_finish(self):
        """
        вызывает быстрое завершение анимации
        """
        self.active_surf_number = self.frames_count
        self.active_surf = self.frame_surfaces[-1]
        self.finish()

    def finish(self):
        """
        устанавливает параметр done=True при вызове
        :return:
        """
        self.done = True

    def update(self):
        """
        вызывает обновление кадров анимации в нужное время
        """
        if self.delay > 0:
            self.delay -= self.dt
        else:
            self.converting_frame_interval += self.dt
            if self.converting_frame_interval >= self.countdown:
                self.update_frame()


class ElevatorOpeningAnimation(ImageAnimation):

    def __init__(self, _obj, _fps, _main_hero, _time_interval, _delay=0):
        """
        описывает анимацию открывания дверей лифта
        :param _obj: комната с лифтом
        :param _fps: фпс
        :param _main_hero: главный герой
        :param _time_interval: время анимации
        :param _delay: задержка
        """
        self.main_hero = _main_hero
        self.frames_files = ["assets/elevator/close_elevator.png", "assets/elevator/closing_elevator_18.png",
                             "assets/elevator/closing_elevator_17.png", "assets/elevator/closing_elevator_16.png",
                             "assets/elevator/closing_elevator_15.png", "assets/elevator/closing_elevator_14.png",
                             "assets/elevator/closing_elevator_13.png", "assets/elevator/closing_elevator_12.png",
                             "assets/elevator/closing_elevator_11.png", "assets/elevator/closing_elevator_10.png",
                             "assets/elevator/closing_elevator_9.png", "assets/elevator/closing_elevator_8.png",
                             "assets/elevator/closing_elevator_7.png", "assets/elevator/closing_elevator_6.png",
                             "assets/elevator/closing_elevator_5.png", "assets/elevator/closing_elevator_4.png",
                             "assets/elevator/closing_elevator_3.png", "assets/elevator/closing_elevator_2.png",
                             "assets/elevator/closing_elevator_1.png", "assets/elevator/open_elevator.png"]
        self.main_hero = _main_hero
        super().__init__(_obj, self.frames_files, _time_interval, _fps, _delay)

    def update(self):
        """
        обновляет параметры анимации и параметр героя, отвечающий за блокировку его движений при выполнении анимации
        """
        super(ElevatorOpeningAnimation, self).update()
        if not self.done:
            self.main_hero.move_blocked = True
        else:
            self.main_hero.move_blocked = False


class ElevatorClosingAnimation(ImageAnimation):

    def __init__(self, _obj, _fps, _main_hero, _time_interval, _delay=0.0):
        """
        описывает анимацию закрытия дверей лифта
        :param _obj: комната с лифтом
        :param _fps: фпс
        :param _main_hero: главный герой
        :param _time_interval: время анимации
        :param _delay: задержка
        """
        self.frames_files = ["assets/elevator/open_elevator.png", "assets/elevator/closing_elevator_1.png",
                             "assets/elevator/closing_elevator_2.png", "assets/elevator/closing_elevator_3.png",
                             "assets/elevator/closing_elevator_4.png", "assets/elevator/closing_elevator_5.png",
                             "assets/elevator/closing_elevator_6.png", "assets/elevator/closing_elevator_7.png",
                             "assets/elevator/closing_elevator_8.png", "assets/elevator/closing_elevator_9.png",
                             "assets/elevator/closing_elevator_10.png", "assets/elevator/closing_elevator_11.png",
                             "assets/elevator/closing_elevator_12.png", "assets/elevator/closing_elevator_13.png",
                             "assets/elevator/closing_elevator_14.png", "assets/elevator/closing_elevator_15.png",
                             "assets/elevator/closing_elevator_16.png", "assets/elevator/closing_elevator_17.png",
                             "assets/elevator/closing_elevator_18.png", "assets/elevator/close_elevator.png"]
        self.main_hero = _main_hero
        super().__init__(_obj, self.frames_files, _time_interval, _fps, _delay)

    def update(self):
        """
        обновляет параметры анимации и параметр героя, отвечающий за блокировку его движений при выполнении анимации
        """
        super(ElevatorClosingAnimation, self).update()
        if not self.done:
            self.main_hero.move_blocked = True
        else:
            self.main_hero.move_blocked = False
