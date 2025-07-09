import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from read.simulation import Simulation
from utils.settings import CICADAS_AWAKING_DAY

class AverageSimulation:
    def __init__(self, filename: str, grass: str, pred: str) -> None:
            # initialization
            self.filename: str = filename
            self.grass: str = grass
            self.pred: str = pred

            self.read()
            self.calc()

    def __str__(self) -> str:
        return self.sim.__str__()
    
    def read(self) -> None:
        # read
        self.sim_list: list[Simulation] = []
        for seed in os.listdir(os.path.join(self.filename, self.grass,self.pred)):
             self.sim_list.append(Simulation(self.filename, self.grass, self.pred, seed))

    def calc(self) -> None:
        # complete
        concat: pd.DataFrame = pd.concat([sim.sim for sim in self.sim_list])
        self.sim: pd.DataFrame = concat.groupby(concat.index).mean()

        # average
        concat: pd.DataFrame = pd.concat([sim.sim_average for sim in self.sim_list])
        self.sim_average: pd.DataFrame = concat.groupby(concat.index).mean()

        # maximum
        concat: pd.DataFrame = pd.concat([sim.sim_maximum for sim in self.sim_list])
        self.sim_maximum: pd.DataFrame = concat.groupby(concat.index).mean()

        # minimum
        concat: pd.DataFrame = pd.concat([sim.sim_minimum for sim in self.sim_list])
        self.sim_minimum: pd.DataFrame = concat.groupby(concat.index).mean()

        # single valuse
        self.final_average: float = {col: self.sim_average[col].to_numpy()[-1] for col in self.sim_average.columns}
        self.final_maximum: float = {col: self.sim_maximum[col].to_numpy()[-1] for col in self.sim_maximum.columns}
        self.final_minimum: float = {col: self.sim_minimum[col].to_numpy()[-1] for col in self.sim_minimum.columns}

    def fit(self, gene: str = '1') -> None:
        # data to be fitted
        data: np.ndarray = self.sim[gene].to_numpy()
        to_fit: np.ndarray = np.zeros(365 - 1)
        for year in range(len(data) // 365 - 1):
             to_fit += data[year * 365 + CICADAS_AWAKING_DAY + 1:  (year + 1) * 365 + CICADAS_AWAKING_DAY]
        to_fit /= to_fit[0]

        # fit functions
        def growth(x: np.ndarray, a: float, b: float):
             return a * x ** b + 1
        def degrowth(x: np.ndarray, a: float, b: float, c: float, d: float): 
            x = x ** d
            return a * x * np.exp(- x / b) + c

        # fit
        X: np.ndarray = np.arange(364)
        max_: int = np.argmax(to_fit)
        gparams, _ = curve_fit(growth, np.arange(364)[:max_], to_fit[:max_])
        dparams, _ = curve_fit(degrowth, np.arange(364)[max_:], to_fit[max_:], p0 = [1, max_, 1, 1])

        print(f'Growth like x^{gparams[1]:.1f}')
        print(f'Degrowth like y*exp(-y/{dparams[1]:.1f}) with y = x^{dparams[3]:.1f}')

        # plot
        plt.plot(to_fit * 100, linewidth = 2, label = 'Average population trend', c = "#0040ff")
        plt.plot(X[:max_], growth(X[:max_], *gparams) * 100, '--', c = 'red', linewidth = 2, 
                 label = rf'Growth $\sim{gparams[0]:.2f}\cdot x^{{{gparams[1]:.1f}}}$')
        plt.plot(X[max_:], degrowth(X[max_:], *dparams) * 100, '--', c = "#ffa600", linewidth = 2, 
                 label = rf'Degrowth $\sim{dparams[0]:.3f}\cdot z\cdot e^{{-z /{dparams[1]:.0f}}}$; $z = x^{{{dparams[3]:.1f}}}$')
        plt.xlabel('Days from emersion', fontweight = 'bold')
        plt.ylabel('Population size [%]', fontweight = 'bold')
        plt.xlim(-5, 200)
        plt.legend(framealpha = 0)
        plt.show()

    def plot(self, type: str = 'average') -> None:
        to_plot: pd.DataFrame = {'complete': {'df': self.sim,         'xscale': 365, 'ylabel': 'Population'},
                                 'average':  {'df': self.sim_average, 'xscale': 1, 'ylabel': 'Average population'},
                                 'maximum':  {'df': self.sim_maximum, 'xscale': 1, 'ylabel': 'Maximum population'},
                                 'minimum':  {'df': self.sim_minimum, 'xscale': 1, 'ylabel': 'Minimum population'}}[type]
        labels: list[str] = [f'Gene {col}' if col != 'predators' else 'Predators' for col in reversed(to_plot['df'].columns)]
        colors: list[str] = ['red', "#0040ff", 'cyan', 'green', 'lime', 'orange', 'purple', 'violet', 'pink', 'gray', 'black', 'magenta']
        
        # plot
        X = to_plot['df'].index / to_plot['xscale']
        for i, (col, label) in enumerate(zip(reversed(to_plot['df'].columns), labels)):
            plt.plot(X, to_plot['df'][col], label = label, c = colors[i])
            
        plt.xlabel('Year', fontweight = 'bold')
        plt.ylabel(to_plot['ylabel'], fontweight = 'bold')
        plt.legend(framealpha = 0, reverse = True)
        plt.show()