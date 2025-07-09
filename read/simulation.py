import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class Simulation:
    def __init__(self, filename: str, grass: str, pred: str, seed: str) -> None:
        # initialization
        self.filename: str = filename
        self.grass: str = grass
        self.pred: str = pred
        self.seed: str = seed

        self.read()
        self.calc()

    def __str__(self) -> str:
        return self.sim.__str__()

    def read(self) -> None:
        self.sim: pd.DataFrame = pd.read_csv(os.path.join(self.filename, self.grass,self.pred, self.seed, 'run.csv'))
        self.sim.index += 1

    def calc(self) -> None:
        self.sim_average: pd.DataFrame = self.sim.groupby(np.arange(len(self.sim)) // 365).mean()
        self.sim_maximum: pd.DataFrame = self.sim.groupby(np.arange(len(self.sim)) // 365).max()
        self.sim_minimum: pd.DataFrame = self.sim.groupby(np.arange(len(self.sim)) // 365).min()

    def plot(self, type: str = 'complete') -> None:
        to_plot: pd.DataFrame = {'complete': {'df': self.sim,         'xscale': 365, 'ylabel': 'Population'},
                                 'average':  {'df': self.sim_average, 'xscale': 1, 'ylabel': 'Average population'},
                                 'maximum':  {'df': self.sim_maximum, 'xscale': 1, 'ylabel': 'Maximum population'},
                                 'minimum':  {'df': self.sim_minimum, 'xscale': 1, 'ylabel': 'Minimum population'}}[type]
        labels: list[str] = [f'Gene {col}' if col != 'predators' else 'Predators' for col in to_plot['df'].columns]
        
        # plot
        X = to_plot['df'].index / to_plot['xscale']
        plt.plot(X, to_plot['df'], label = labels)
        plt.xlabel('Years')
        plt.ylabel(to_plot['ylabel'])
        plt.legend()
        plt.show()