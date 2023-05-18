class SMA:
    """Implements Simple Moving Average.

    Implements the Simple Moving Average, see:
    https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average
    Computing a given average is O(1) in time complexity, and the entire class
    is O(N) in space complexity.

    Attributes:
        buffer_window_length: A number representing the length of the circular
          buffer in seconds.
        spreadsheet_id: A number representing the time period of the main loop.
    """

    def __init__(self, buffer_window_length: float, time_period: float) -> None:
        """Initializes the instance with the provided metadata.

        Args:
          sheet_tab_name: The length of the circular buffer in seconds.
          spreadsheet_id: The time period of the main loop.
        """
        self.buffer = [0] * int(buffer_window_length / time_period)
        self.buffer_ready = False
        self.buffer_pointer = 0
        self.cum_sum = 0
        self.average = None

    def insert(self, value: float) -> None:
        """Inserts the next value in a stream of data to be averaged out.

        Inserts the next value of a given stream of data to a circular buffer,
        and computes the average iff the buffer is full.

        Args:
            value: A number (float) to be inserted.

        Returns:
            TBD
        """
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
