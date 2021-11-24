class LinearFunction:
    def __init__(self, _start_value, _end_value, _delay, _time_interval, _fps):
        self.delay = _delay
        self.start_value = _start_value
        self.end_value = _end_value
        self.time_interval = _time_interval
        self.past_time = 0
        self.delta_time = 1 / _fps
        self.ratio = (self.end_value - self.start_value) / self.time_interval

    def update(self):
        if self.past_time < self.delay:
            self.past_time += self.delta_time
            return self.start_value
        elif self.past_time < self.delay + self.time_interval:
            return self.start_value + self.delta_time * self.ratio




