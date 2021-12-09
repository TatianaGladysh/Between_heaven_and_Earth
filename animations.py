import pygame
from labyrinth import Room
from heroes import MainHero
import animations_preset

QUEST_ANIMATION_TIME = 3
ELEVATOR_OPENING_CLOSING_ANIMATION = 0.5
BEGIN_SCREEN_ANIMATION_TIME = 0.35
END_OF_SCREEN_ANIMATION_TIME = 0.35
MIN_ALLOWABLE_FPS = 25
WALKING_ANIMATION_TIME_INTERVAL = 1
LEVEL_COMPLETE_ANIMATION_TIME = 1.5


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
        self.switch_screen_animations = []
        self.main_hero_walking_animations = []
        self.complete_level_animations = []
        self.fps = _painter.fps
        self.processing = False

    def add_complete_level_animation(self):
        """
        добавляет в список анимаций анимацию после прохождения уровня
        """
        self.__add_animation(LevelCompleteAnimation(self.painter.game, "begin"))

    def set_game_params(self):
        """
        устанавливает максимальные координаты коррекции для захождения в лифт и выхода из него при рассчете единичных
        длин в painter 'е
        """
        self.max_elevator_correction_y = - 0.09166 * self.painter.unit_height
        self.max_elevator_correction_x = - 0.015 * self.painter.unit_width
        self.elevator_correction_x, self.elevator_correction_y = \
            self.painter.elevator_correction_x, self.painter.elevator_correction_y

    def add_quest_animation(self, quest, number):
        self.__add_animation(QuestAnimation(quest, self.fps, number))

    def __add_animation(self, animation):
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
        elif isinstance(animation, AnimationSwitchScreen):
            self.switch_screen_animations.append(animation)
        elif isinstance(animation, WalkingAnimation):
            self.main_hero_walking_animations.append(animation)
        elif isinstance(animation, LevelCompleteAnimation):
            self.complete_level_animations.append(animation)

    def add_walking_animation(self, obj):
        if isinstance(obj, MainHero):
            self.main_hero_walking_animations.append(WalkingAnimation(obj, self.fps, WALKING_ANIMATION_TIME_INTERVAL))

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

    def end_walking_animations(self, hero):
        if isinstance(hero, MainHero):
            for animation in self.main_hero_walking_animations:
                animation.emergency_finish()
                self.main_hero_walking_animations = []

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
        self.__add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero,
                                     _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=ELEVATOR_OPENING_CLOSING_ANIMATION, args=[True])
        self.__add_animation(ElevatorCorrectionCordsAnimation(self.painter, (self.max_elevator_correction_x,
                                                                             self.max_elevator_correction_y),
                                                              _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION,
                                                              _fps=self.painter.fps))
        self.__add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero,
                                     _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION,
                                     _delay=ELEVATOR_OPENING_CLOSING_ANIMATION))

    def elevator_exit(self):
        """
        отвечает за анимацию выхода главного героя из лифта
        завершает анимации с лифтом, которые были вызваны и активны до этого
        """
        self.emergency_finish_elevator_animations()
        self.__add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero,
                                     _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION))
        self.__add_animation(
            ElevatorCorrectionCordsAnimation(self.painter, (0, 0), _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION,
                                             _fps=self.painter.fps, _delay=ELEVATOR_OPENING_CLOSING_ANIMATION))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=0.15, args=[False])
        self.__add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero,
                                     _time_interval=ELEVATOR_OPENING_CLOSING_ANIMATION,
                                     _delay=ELEVATOR_OPENING_CLOSING_ANIMATION))

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
        for animation in self.main_hero_walking_animations:
            if animation.done:
                self.main_hero_walking_animations.remove(animation)
            else:
                animation.update()
        for animation in self.complete_level_animations:
            if animation.done:
                self.complete_level_animations.remove(animation)
            else:
                animation.update()
        for func in self.later_on_funcs:
            if func.done:
                self.later_on_funcs.remove(func)
            else:
                func.update()


class AnimationSwitchScreen:

    def __init__(self, _game, _start_opacity, _end_opacity, _delay, _switch_time):
        """
        анимация смены экрана
        :param _game: игра
        :param _start_opacity: начальная непрозрачность
        :param _end_opacity: конечная непрозрачность
        :param _delay: задержка до старта работы функции
        :param _switch_time: время анимации
        """
        self.game = _game
        self.self_surf = pygame.Surface((self.game.screen_width, self.game.screen_height))
        self.self_surf.set_alpha(_start_opacity)
        self.opacity = _start_opacity
        self.end_opacity = _end_opacity
        self.time_interval = _switch_time
        self.time = 0
        self.delay = _delay
        self.general_delta = _end_opacity - _start_opacity
        self.done = False

    def set_new_alpha(self):
        """
        устанавливает новый коэффициент прозрачности в свой surface
        """
        self.opacity += self.general_delta * ((1 / max(self.game.fps.value, MIN_ALLOWABLE_FPS)) / self.time_interval)
        if self.opacity > 255:
            self.opacity = 255
        if self.opacity < 0:
            self.opacity = 0
        self.self_surf.set_alpha(self.opacity)

    def update(self):
        """
        вызывает обновление коэффициента прозрачности и отрисовывает свой surface на экране
        """
        if self.delay <= self.time <= self.delay + self.time_interval:
            self.set_new_alpha()
            self.game.game_surf.blit(self.self_surf, (0, 0))
        elif self.time > self.delay + self.time_interval:
            self.done = True
        self.time += (1 / max(self.game.fps.value, MIN_ALLOWABLE_FPS))


class QuestAnimation:

    def __init__(self, _quest, _fps, _pos_in_order, _begin_opacity=255):
        """
        анимации появления заданий на экране игры
        :param _quest: привязанное задание
        :param _fps: фпс
        :param _pos_in_order: позиция задания в очереди
        :param _begin_opacity: начальная прозрачность квеста
        """
        self.indent = 10
        self.quest = _quest
        self.img_surf = self.quest.active_surf
        self.begin_opacity = _begin_opacity
        self.opacity = 255
        self.fps = _fps
        self.step_change = (0 - self.opacity) * ((1 / max(self.fps.value, MIN_ALLOWABLE_FPS)) / QUEST_ANIMATION_TIME)
        self.time = 0
        self.done = False
        self.pos_in_order = _pos_in_order
        self.screen_x = 0
        self.screen_y = 0
        self.unit_width = 0
        self.unit_height = 0
        self.scale_k = 0
        self.img_rect = None
        self.calculate_params()

    def calculate_params(self):
        """
        вычисляет параметры уведомления на экране
        """
        self.unit_width = self.quest.character.game.screen_width // 4
        img_width = self.img_surf.get_width()
        img_height = self.img_surf.get_height()
        self.scale_k = self.unit_width / img_width
        self.unit_height = img_height * self.scale_k
        self.screen_x = self.indent + self.unit_width // 2
        self.screen_y = self.indent + self.unit_height // 2 + self.pos_in_order * (self.indent + self.unit_height)
        self.img_surf = pygame.transform.scale(self.img_surf, (int(self.unit_width), int(self.unit_height)))
        self.img_rect = self.img_surf.get_rect(center=(self.screen_x, self.screen_y))

    def update_pic(self):
        """
        обновляет картинку квеста
        """
        self.img_surf.set_alpha(self.opacity)
        self.quest.character.game.game_surf.blit(self.img_surf, self.img_rect)

    def update(self):
        """
        обновляет прозрачность квеста и следит за окончанием анимации
        """
        self.time += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
        if self.time >= QUEST_ANIMATION_TIME:
            self.done = True
        else:
            self.step_change = (0 - self.begin_opacity) * (
                    (1 / max(self.fps.value, MIN_ALLOWABLE_FPS)) / QUEST_ANIMATION_TIME)
            self.opacity += self.step_change
            self.update_pic()


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
        self.fps = _fps
        self.delay = _delay
        self.variable_step_x = (_end_values_cords[0] - self.variable_x) / (
                _time_interval / (1 / max(self.fps.value, MIN_ALLOWABLE_FPS)))
        self.variable_step_y = (_end_values_cords[1] - self.variable_y) / (
                _time_interval / (1 / max(self.fps.value, MIN_ALLOWABLE_FPS)))
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
        self.time += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
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
        self.fps = _fps
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
        self.time += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
        if self.time_interval <= self.time:
            if not self.done:
                self.execute()


class ImageAnimation:
    id = 0

    def __init__(self, _obj, _frames_surfs, _time_interval, _fps, _delay, _nature_of_frames_change="linear"):
        """
        объект класса может описывать анимацию, связанную с изменением изображений с течением времени, пока только
        линейным
        :param _obj: объект, у которого следует изменять изображение
        :param _time_interval: общее время выполнения анимации
        :param _fps: фпс
        :param _delay: задержка перед началом выполнения функции
        :param _nature_of_frames_change: характер изменения изображений во времени, пока осуществим только линейный
        """
        self.obj = _obj
        self.frames_surfs = _frames_surfs
        self.frames_count = len(self.frames_surfs)
        self.active_surf_number = 0
        self.active_surf = self.frames_surfs[0]
        self.time_interval = _time_interval
        self.fps = _fps
        self.converting_frame_interval = 0
        self.countdown = self.time_interval / len(self.frames_surfs)
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

    def update_frame(self):
        """
        обновляет кадр анимации
        """
        self.active_surf_number += 1
        self.converting_frame_interval = 0
        if self.active_surf_number >= self.frames_count:
            self.finish()
            return
        self.active_surf = self.frames_surfs[self.active_surf_number]
        if isinstance(self.obj, Room):
            self.obj.set_surf(self.active_surf)
        if isinstance(self.obj, MainHero):
            if self.obj.walking_direction == "left":
                self.obj.set_surf(pygame.transform.flip(self.active_surf, True, False))
            else:
                self.obj.set_surf(self.active_surf)
        if self.nature_of_frames_change == "linear":
            pass
        # при нелинейной анимации можно будет изменять время cool_count

    def emergency_finish(self):
        """
        вызывает быстрое завершение анимации
        """
        self.active_surf_number = self.frames_count
        self.active_surf = self.frames_surfs[-1]
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
            self.delay -= (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
        else:
            self.converting_frame_interval += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
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
        self.frames_surfs = animations_preset.ElevatorOpeningSurfs
        super().__init__(_obj, self.frames_surfs, _time_interval, _fps, _delay)

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
        self.frames_surfs = animations_preset.ElevatorClosingSurfs
        self.main_hero = _main_hero
        super().__init__(_obj, self.frames_surfs, _time_interval, _fps, _delay)

    def update(self):
        """
        обновляет параметры анимации и параметр героя, отвечающий за блокировку его движений при выполнении анимации
        """
        super(ElevatorClosingAnimation, self).update()
        if not self.done:
            self.main_hero.move_blocked = True
        else:
            self.main_hero.move_blocked = False


class WalkingAnimation(ImageAnimation):
    def __init__(self, _hero, _fps, _time_interval, _delay=0):
        """
        описывает ходьбу человека
        :param _fps: фпс
        :param _time_interval: время анимации
        :param _delay: задержка
        """
        self.hero = _hero
        self.frames_surfaces = animations_preset.WalkingAnimationsSurfs
        super().__init__(_hero, self.frames_surfaces, _time_interval, _fps, _delay)

    def update_frame(self):
        """
        обновляет кадр
        """
        super().update_frame()

    def emergency_finish(self):
        """
        быстро заканчивает работу анимации, а именно
        устанавливает конечные значения параметров
        """
        super().emergency_finish()
        self.hero.img_surf = animations_preset.StayMainPersonSurf
        if self.hero.walking_direction == "left":
            self.hero.img_surf = pygame.transform.flip(self.hero.img_surf, True, False)

    def update(self):
        """
        обновляет параметры анимации и параметр героя, отвечающий за блокировку его движений при выполнении анимации
        """
        super(WalkingAnimation, self).update()


class LevelCompleteAnimation:

    def __init__(self, _game, _process_type="begin", _delay=0.0, _time_interval=LEVEL_COMPLETE_ANIMATION_TIME):
        """
        Анимация после прохождения уровня уровня
        :param _game: игра
        :param _process_type: тип процесса, то есть начало или конец анимации
        :param _delay: задержка перед началом
        :param _time_interval: время анимации
        """
        self.game = _game
        self.fps = self.game.fps
        self.time_interval = _time_interval
        if _process_type == "begin":
            self.opacity = 0.0
            self.end_opacity = 255.0
            self.frames_surfs = animations_preset.LevelCompleteSurfsBeginAnimation
            self.opacity_time_interval = self.time_interval / 2
        else:
            self.opacity = 255.0
            self.end_opacity = 0.0
            self.frames_surfs = animations_preset.LevelCompleteSurfsEndAnimation
            self.opacity_time_interval = self.time_interval
        self.frame_countdown = self.time_interval / len(self.frames_surfs)

        self.begin_opacity = self.opacity
        self.active_surf = self.frames_surfs[0]
        self.active_surf_num = 0
        self.converting_frame_interval = 0
        self.rect = self.active_surf.get_rect()
        self.opacity_step_change = (self.end_opacity - self.opacity) * (
                (1 / max(self.fps.value, MIN_ALLOWABLE_FPS)) / self.opacity_time_interval)
        self.time = 0
        self.done = False
        self.delay = _delay
        self.__update_pic()

    def __update_opacity(self):
        """
        обновляет значение непрозрачности
        """
        if 0 <= self.opacity <= 255:
            self.step_change = (self.end_opacity - self.begin_opacity) * (
                    (1 / max(self.fps.value, MIN_ALLOWABLE_FPS)) / self.opacity_time_interval)
            self.opacity += self.step_change
            self.active_surf.set_alpha(self.opacity)

    def __update_frame(self):
        """
        обновляет картинку
        """
        self.converting_frame_interval = 0
        if self.active_surf_num > len(self.frames_surfs) - 1:
            self.finish()
        else:
            self.active_surf = self.frames_surfs[self.active_surf_num]
        self.active_surf.set_alpha(self.opacity)
        self.active_surf_num += 1

    def finish(self):
        """
        устанавливает параметр сделано
        """
        self.done = True

    def __update_pic(self):
        """
        обновляет картинку на экране
        """
        self.game.game_surf.blit(self.active_surf, self.rect)

    def update(self):
        """
        обновляет свое время, картинку, если это надо и непрозрачность, а также завершает себя если это нужно
        если закончилось начало анимации, вызывает свой инит, только уже для конца анимации
        """
        self.time += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
        if self.delay <= self.time <= self.delay + self.time_interval:
            self.converting_frame_interval += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
            self.__update_opacity()
            if self.converting_frame_interval >= self.frame_countdown:
                self.__update_frame()
            self.__update_pic()
        elif self.delay + self.time_interval < self.time:
            if self.opacity <= 10:
                self.finish()
            else:
                self.__init__(self.game, "end", 0.0, self.time_interval / 1.3)
