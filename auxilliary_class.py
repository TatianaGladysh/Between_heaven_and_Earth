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
        """
        self.done = True
        self.func(*self.args)

    def emergency_finish(self):
        """
        вызывает быстрое выполнение функции, ранее чем прошло время задержки
        """
        self.execute()

    def update(self):
        """
        обновляет время и вызывает выполнение функции по его прошествии
        """
        self.time += (1 / max(self.fps.value, MIN_ALLOWABLE_FPS))
        if self.time_interval <= self.time:
            if not self.done:
                self.execute()