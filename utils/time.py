from utils.settings import *

class Time:
    def __init__(self):
        self.current_day = 0
        self.current_year = 0

    def __str__(self):
        return f'{self.current_day}, {self.current_year}'

    def get_time(self):
        return {'year': self.current_year, 'day': self.current_day}

    def update(self):
        # update day
        self.current_day += 1

        # update year
        if self.current_day > 365:
            self.current_day = 1
            self.current_year += 1
