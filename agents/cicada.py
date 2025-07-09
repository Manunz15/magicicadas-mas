from utils.settings import *
from utils.group import Group
from utils.math_utils import counter
from agents.agent import Animal

class Cicada(Animal):
    def __init__(self, pos, genes, time, cicada_group):
        super().__init__(pos, genes, time, cicada_group, 
                         max_satiety = CICADAS_MAX_SATIETY, 
                         hunger_rate = CICADAS_HUNGER_RATE, 
                         longevity = CICADAS_LONGEVITY,
                         mate_probability = CICADAS_MATE_PROBABILITY)

        # initialization
        self.birth_year = time.current_year   

    def __str__(self):
        return f'Magicicada {self.genes}: {self.life_stage}, {self.gender}, in pos {self.pos}, satiety = {self.satiety}'
    
    def eat(self, grass):
        # try to eat or move away
        if grass.growth_state:
            self.satiety += 1
            grass.growth_state -= 1
        else:
            self.move()

    def awake(self, adult_group):
        if min(self.genes) == (self.time.current_year - self.birth_year):
            self.adult_group = adult_group
            self.adult_group.add(self)

    def death(self):
        try:
            self.adult_group.remove(self)
        except:
            pass
        super().death()

    def update(self, grass, other_cicadas):
        eat_func = lambda : self.eat(grass)
        super().update(other_cicadas, eat_func)


class CicadaGroup(Group):
    def __init__(self, grass_group):
        super().__init__()
        self.cicada_counter = counter()
        self.grass = grass_group

    def add(self, cicada):
        super().add(cicada)
        cicada.name = f'cicada_{next(self.cicada_counter)}'

    def awake(self, adult_group):
        for cicada in self:
            cicada.awake(adult_group)

    def update(self):
        # update cicadas
        for cicada in self:
            cicadas_in_tile = []
            for other_cicada in self:
                if cicada.pos == other_cicada.pos and cicada.gender != other_cicada.gender:
                    cicadas_in_tile.append(other_cicada)

            cicada.update(self.grass[cicada.pos[0] * COLS + cicada.pos[1]], cicadas_in_tile)