from datetime import datetime


class TimeDelta:

    def __init__(self):
        self.start_time = datetime.now()
        self.map = {"hour": self.hour_elapsed,
                    "minute": self.minute_elapsed,
                    "day": self.day_elapsed,
                    "on_press": lambda: True}

    def time_delta(self, upper_limit_seconds: int) -> bool:
        if (datetime.now() - self.start_time).seconds >= upper_limit_seconds:
            self.start_time = datetime.now()
            return True
        return False

    def hour_elapsed(self) -> bool:
        return self.time_delta(60 ** 2)

    def minute_elapsed(self) -> bool:
        return self.time_delta(60)

    def day_elapsed(self) -> bool:
        return self.time_delta((60 ** 2) * 24)
