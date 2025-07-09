from utils.settings import *
from utils.group import Group
from utils.math_utils import counter
from agents.agent import Animal

from random import choice

class Predator(Animal):
    def __init__(self, pos, time, groups):
        super().__init__(pos, None, time, groups, 
                         max_satiety = PREDATORS_MAX_SATIETY, 
                         hunger_rate = PREDATORS_HUNGER_RATE, 
                         longevity = PREDATORS_LONGEVITY,
                         mate_probability = PREDATORS_MATE_PROBABILITY)

        # initialization
        self.age = 0

    def __str__(self):
        return f'Predators, {self.gender}, in pos {self.pos}, satiety = {self.satiety}'
    
    def eat(self, cicadas):
        # eat cicada
        if len(cicadas):
            self.satiety += 1
            choice(cicadas).death()
        else:
            self.move()

    def feed(self):
        if self.satiety < self.max_satiety:
            self.satiety += 1

    def update(self, cicadas, other_predators):
        eat_func = lambda : self.eat(cicadas)
        super().update(other_predators, eat_func)


class PredatorGroup(Group):
    def __init__(self, feeding):
        super().__init__()
        self.feeding = feeding
        self.predator_counter = counter()

    def add(self, predator):
        super().add(predator)
        predator.name = f'predator_{next(self.predator_counter)}'

    def update(self, adult_cicadas_group):
        # random supplies
        if len(self):
            for _ in range(self.feeding):
                choice(self).feed()

        # update predators
        for predator in self:
            predators_in_tile = []
            cicadas_in_tile = []
            for other_predator in self:
                if predator.pos == other_predator.pos and predator.gender != other_predator.gender:
                    predators_in_tile.append(other_predator)

            for cicada in adult_cicadas_group:
                if predator.pos == cicada.pos:
                    cicadas_in_tile.append(cicada)

            predator.update(cicadas_in_tile, predators_in_tile)