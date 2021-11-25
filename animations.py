import pygame
from labyrinth import Room
from heroes import Hero


class ElevatorAnimator:

    def __init__(self, _painter):
        self.painter = _painter
        self.elevator_correction_x = _painter.elevator_correction_x
        self.elevator_correction_y = _painter.elevator_correction_y
        self.max_elevator_correction_y = 0
        self.max_elevator_correction_x = 0
        self.images_animations = []
        self.cords_animations = []
        self.later_on_funcs = []
        self.dt = 1 / _painter.fps
        self.fps = _painter.fps
        self.processing = False

    def set_game_params(self):
        self.max_elevator_correction_y = - 0.09166 * self.painter.unit_height
        self.max_elevator_correction_x = - 0.0083 * self.painter.unit_width
        self.elevator_correction_x, self.elevator_correction_y = \
            self.painter.elevator_correction_x, self.painter.elevator_correction_y

    def add_animation(self, animation):
        if isinstance(animation, ImageAnimation):
            self.images_animations.append(animation)
        elif isinstance(animation, ElevatorCorrectionCordsAnimation):
            self.cords_animations.append(animation)

    def add_later_on_funcs(self, func, delay, args=None):
        if args is None:
            args = []
        self.later_on_funcs.append(LaterOnFunc(func, delay, self.painter.fps, args))

    def change_rendering_of_layers(self, value=None):
        if value is None:
            self.painter.draw_main_hero_in_the_elevator = not self.painter.draw_main_hero_in_the_elevator
        else:
            self.painter.draw_main_hero_in_the_elevator = value

    def emergency_finish_all_animations(self):
        for animation in self.images_animations:
            animation.emergency_finish()
        for func in self.later_on_funcs:
            func.emergency_finish()
        for animation in self.cords_animations:
            animation.emergency_finish()
        self.images_animations = self.cords_animations = self.later_on_funcs = []

    def elevator_entering(self):
        self.emergency_finish_all_animations()
        self.add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.2))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=0.2, args=[True])
        self.add_animation(ElevatorCorrectionCordsAnimation(self.painter, (self.max_elevator_correction_x,
                                                                           self.max_elevator_correction_y),
                                                            _time_interval=0.2, _fps=self.painter.fps))
        self.add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.2, _delay=0.2))

    def elevator_exit(self):
        self.emergency_finish_all_animations()
        self.add_animation(
            ElevatorOpeningAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.2))
        self.add_animation(
            ElevatorCorrectionCordsAnimation(self.painter, (0, 0), _time_interval=0.2, _fps=self.painter.fps,
                                             _delay=0.2))
        self.add_later_on_funcs(self.change_rendering_of_layers, delay=0.2, args=[False])
        self.add_animation(
            ElevatorClosingAnimation(self.painter.labyrinth.get_room(*self.painter.main_hero.get_cords()),
                                     self.painter.fps, self.painter.main_hero, _time_interval=0.2,
                                     _delay=0.2))

    def update(self):
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


class ElevatorCorrectionCordsAnimation:
    def __init__(self, _painter, _end_values_cords, _time_interval, _fps, _delay=0.0):
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
        self.variable_x += self.variable_step_x
        self.variable_y += self.variable_step_y
        self.painter.update_elevator_correction_cords(self.variable_x, self.variable_y)

    def emergency_finish(self):
        self.variable_x = self.end_value_cords[0]
        self.variable_y = self.end_value_cords[1]
        self.painter.update_elevator_correction_cords(self.variable_x, self.variable_y)
        self.done = True

    def update(self):
        self.time += self.dt
        if self.delay <= self.time <= self.delay + self.time_interval and not self.done:
            self.change_variables()
        if self.time > self.delay + self.time_interval:
            self.done = True


class LaterOnFunc:
    def __init__(self, _func, _time_interval, _fps, _args=None):
        if _args is None:
            _args = []
        self.func = _func
        self.time_interval = _time_interval
        self.args = _args
        self.time = 0
        self.dt = 1 / _fps
        self.done = False

    def execute(self):
        self.done = True
        self.func(*self.args)

    def emergency_finish(self):
        self.execute()

    def update(self):
        self.time += self.dt
        if self.time_interval <= self.time:
            if not self.done:
                self.execute()


class ImageAnimation:
    id = 0

    def __init__(self, _obj, _frames_files, _time_interval, _fps, _delay, _nature_of_frames_change="linear"):
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
        return self.time_interval

    def fill_the_array_of_surfaces(self):
        frames_surfaces = []
        for i in range(len(self.frames_files)):
            frames_surfaces.append(pygame.image.load(self.frames_files[i]))
        return frames_surfaces

    def update_frame(self):
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
        self.active_surf_number = self.frames_count
        self.active_surf = self.frame_surfaces[-1]
        self.finish()

    def finish(self):
        self.done = True

    def update(self):
        if self.delay > 0:
            self.delay -= self.dt
        else:
            self.converting_frame_interval += self.dt
            if self.converting_frame_interval >= self.countdown:
                self.update_frame()


class ElevatorOpeningAnimation(ImageAnimation):

    def __init__(self, _obj, _fps, _main_hero, _time_interval, _delay=0):
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
        super(ElevatorOpeningAnimation, self).update()
        if not self.done:
            self.main_hero.move_blocked = True
        else:
            self.main_hero.move_blocked = False


class ElevatorClosingAnimation(ImageAnimation):

    def __init__(self, _obj, _fps, _main_hero, _time_interval, _delay=0.0):
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
        super(ElevatorClosingAnimation, self).update()
        if not self.done:
            self.main_hero.move_blocked = True
        else:
            self.main_hero.move_blocked = False
