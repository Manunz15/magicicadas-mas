from utils.settings import *
from utils.math_utils import prob
from agents.agent import Agent

class Grass(Agent):
    def __init__(self, pos, time, groups, grass_growth_func):
        super().__init__(pos, time, groups)
        self.grass_growth_func = grass_growth_func
        self.growth_state = 0

    def grow(self, grow_rate):
        if self.growth_state < MAX_GRASS_GROWTH and prob(grow_rate):
            self.growth_state += 1

    def update(self):
        self.grow(self.grass_growth_func[self.time.current_day - 1])