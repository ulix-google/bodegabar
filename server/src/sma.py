class SMA:
    def __init__(self, buffer_window_length: float, time_period: float) -> None:
        self.buffer = [0] * int(buffer_window_length / time_period)
        self.buffer_ready = False
        self.buffer_pointer = 0
        self.cum_sum = 0
        self.average = None

    def insert(self, value) -> None:
        self.cum_sum += value
        self.cum_sum -= self.buffer[self.buffer_pointer]
        self.buffer[self.buffer_pointer] = value
        self.buffer_pointer += 1
        if self.buffer_pointer >= len(self.buffer):
            self.buffer_pointer = 0
            if self.buffer_ready is False:
                self.buffer_ready = True
        self._compute_average()

    def _compute_average(self):
        if self.buffer_ready:
            self.average = self.cum_sum / len(self.buffer)
