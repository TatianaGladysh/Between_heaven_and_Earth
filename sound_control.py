import pygame

MUSIC_INCREASE_TIME = 1.0
MUSIC_VOLUME = 0.7

pygame.init()
pygame.mixer.init()


class SoundController:
    """
    Модуль контроля звуков в игре.
    """
    def __init__(self, _game):
        """
        Инициализация музыки. Загрузка всех мелодий в словарь.
        :param _game: Объект класса Game
        """
        self.game = _game
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(999)
        pygame.mixer.music.set_volume(0)
        self.sounds = {
            "elevator_moving": pygame.mixer.Sound("assets/sounds/elevator_moving.mp3"),
            "elevator_closing": pygame.mixer.Sound("assets/sounds/elevator_moving.mp3"),
            "button_click": pygame.mixer.Sound("assets/sounds/button_click.mp3"),
            "door_open": pygame.mixer.Sound("assets/sounds/door_open.mp3"),
            "elevator_bell": pygame.mixer.Sound("assets/sounds/elevator_bell.mp3"),
            "elevator_doors": pygame.mixer.Sound("assets/sounds/elevator_open_close.mp3")

        }
        self.music_volume_changing = None
        self.sounds_on = False
        self.music_on = False
        self.music_on_off()

    def exit_elevator_sound_play(self):
        """
        Музыка при закрытии лифта.
        """
        if self.sounds_on:
            self.sounds["elevator_bell"].play()
            self.sounds["elevator_doors"].play()

    def enter_elevator_sound_play(self):
        """
        Музыка при открытии лифта.
        """
        if self.sounds_on:
            self.sounds["elevator_doors"].play()

    def play_sound(self, action):
        """
        Проигрывание музыки при действии
        :param action: Действие, а точнее ключ из словаря звуков.
        """
        if self.sounds_on:
            self.sounds[action].play()

    def sounds_on_off(self, value=None):
        """
        Выключение или включение звуков
        :param value: True else False
        """
        if value is None:
            self.sounds_on = not self.sounds_on
        else:
            self.sounds_on = value

    def music_on_off(self):
        """
        Выключение или выключение фоновой музыки и всех звуков.
        """
        if not self.music_on:
            self.music_volume_changing = SmoothMusicVolumeChanging(pygame.mixer.music.get_volume(), MUSIC_VOLUME,
                                                                   MUSIC_INCREASE_TIME, self.game.fps)
            self.music_on = True
        else:
            self.music_volume_changing = SmoothMusicVolumeChanging(pygame.mixer.music.get_volume(), 0,
                                                                   MUSIC_INCREASE_TIME / 2, self.game.fps)
            self.music_on = False
        self.sounds_on_off()

    def update(self):
        if self.music_volume_changing:
            self.music_volume_changing.update()
            if self.music_volume_changing.done:
                self.music_volume_changing = None


class SmoothMusicVolumeChanging:
    """
    Класс для плавного уменьшения/увеличения громкости при включении/выключении музыки.
    """
    def __init__(self, volume, _end_volume, _time_interval, _fps, _delay=0):
        """
        :param volume: Начальная громкость
        :param _end_volume: Конечная громкость
        :param _time_interval: Временной интервал
        :param _fps: FPS
        :param _delay: Время действия
        """
        self.volume = volume
        self.delay = _delay
        self.fps = _fps
        self.time = 0
        self.end_volume = _end_volume
        self.time_interval = _time_interval
        self.general_changing = self.end_volume - self.volume
        self.done = False

    def change_volume_on_step(self):
        """
        Изменение громкости за интервал времени. Обеспечивает плавность перехода.
        """
        self.volume += self.general_changing * (
                (1 / self.fps.value) / self.time_interval)
        pygame.mixer.music.set_volume(self.volume)

    def update(self):
        if self.delay <= self.time <= self.delay + self.time_interval:
            self.change_volume_on_step()
        elif self.time > self.delay + self.time_interval:
            self.done = True
        self.time += (1 / self.fps)
