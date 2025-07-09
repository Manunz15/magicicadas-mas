from utils.settings import *
from utils.group import Group
from utils.time import Time

from agents.grass import Grass
from agents.cicada import Cicada, CicadaGroup
from agents.predators import Predator, PredatorGroup

from random import randint, seed
import pandas as pd
import numpy as np
from time import sleep
import os

class Environment:
    def __init__(self, genes, grass_growth_func, predators_feeding, folder, random_seed = 42):

        # initialization
        self.time = Time()
        self.genes = genes
        seed(random_seed)

        # groups
        self.grass_group = Group()
        self.cicadas_group = CicadaGroup(self.grass_group)
        self.adult_cicadas_group = CicadaGroup(self.grass_group)
        self.predators_group = PredatorGroup(predators_feeding)

        # agents
        self.initialize_grass(grass_growth_func)
        self.initialize_cicadas()
        self.initialize_predators()        

        # save file
        self.save_init(folder)

    def __str__(self):
        return f'Date: {self.time.current_day}, {self.time.current_year}. {len(self.cicadas_group)} cicadas. {len(self.predators_group)} predators.'

    def initialize_grass(self, grass_growth_func):
        for row in range(ROWS):
            for col in range(COLS):
                Grass((row, col), self.time, self.grass_group, grass_growth_func)

    def initialize_cicadas(self):
        for gene in self.genes:
            for _ in range(CICADAS_PER_GENE):
                pos = (randint(0, ROWS - 1), randint(0, COLS - 1))
                Cicada(pos, (gene, gene), self.time, self.cicadas_group)


    def initialize_predators(self):
        for _ in range(PREDATORS):
            pos = (randint(0, ROWS - 1), randint(0, COLS - 1))
            Predator(pos, self.time, self.predators_group)

    def save_init(self, folder):
        # create folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        # create files
        self.save_file = f'{folder}/run.csv'
        self.count_array = np.zeros([365, len(self.genes) + 1]).astype(int)
        pd.DataFrame(columns = list(map(str, self.genes)) + ['predators']).to_csv(self.save_file, index = None)

    def save(self):
        # count cicadas
        for cicada in self.cicadas_group:
            self.count_array[self.time.current_day - 1, self.genes.index(min(cicada.genes))] += 1

        # count predators
        self.count_array[self.time.current_day - 1, -1] = len(self.predators_group)

        # save each year
        if self.time.current_day == 365:
            # print(self)
            df = pd.DataFrame(self.count_array, columns = list(map(str, self.genes)) + ['predators'])
            df.to_csv(self.save_file, mode = 'a', header = False, index = None)
            self.count_array = np.zeros([365, len(self.genes) + 1]).astype(int)

    def update(self, pause): 
        # new day
        self.time.update()

        # update
        if len(self.cicadas_group):
            self.grass_group.update()
        self.predators_group.update(self.adult_cicadas_group)
        self.adult_cicadas_group.update()

        # awake cicadas
        if self.time.current_day == CICADAS_AWAKING_DAY:
            self.cicadas_group.awake(self.adult_cicadas_group)

        # save data
        self.save()

        # sleep
        sleep(pause * 0.001)

    def run(self, years = 1e4, max_cicadas = 1e5, pause = 0):
        while years >= self.time.current_year and len(self.cicadas_group) <= max_cicadas:
            self.update(pause)
