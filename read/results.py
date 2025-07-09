import numpy as np
import os

from read.plot import plot2D, plot3D

class Results:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.read()

    def read(self) -> None:
        # grass and feed
        self.grass_range: np.ndarray = np.load(os.path.join(self.filename, 'grass.npy'))
        self.pred_range:  np.ndarray = np.load(os.path.join(self.filename, 'pred.npy'))

        # read planes
        self.plane_average: dict[np.ndarray] = {file[:-4]: np.load(os.path.join(self.filename, 'average', file)) for file in os.listdir(os.path.join(self.filename, 'average'))}
        self.plane_maximum: dict[np.ndarray] = {file[:-4]: np.load(os.path.join(self.filename, 'max', file)) for file in os.listdir(os.path.join(self.filename, 'max'))}
        self.plane_minimum: dict[np.ndarray] = {file[:-4]: np.load(os.path.join(self.filename, 'min', file)) for file in os.listdir(os.path.join(self.filename, 'min'))}

    def prime_numbers(self) -> None:
        self.primes: np.ndarray = np.zeros([len(self.grass_range), len(self.pred_range)])
        genes: list[str] = list(self.plane_average.keys())[:-1]

        for i in range(self.primes.shape[0]):
            for j in range(self.primes.shape[1]):
                sim: list[float] = [self.plane_average[gene][i, j] for gene in genes]
                # if np.sum(sim) > 0:
                for index, gene in enumerate(genes):
                    if gene in ['11', '13', '17', '19']:
                        self.primes[i, j] += sim[index] / np.sum(sim)

        plot2D(self.primes, self.grass_range, self.pred_range, 'Prime numbers percentage in population')

    def plot2D(self, key: str, type: str = 'average') -> None:
        to_plot: dict = {'average': self.plane_average[key],
                         'maximum': self.plane_maximum[key],
                         'minimum': self.plane_minimum[key]}[type]
        
        # plot
        title: str = 'Predators population' if key == 'predators' else f'Cicadas population ({key} years life cycles)'
        plot2D(to_plot, self.grass_range, self.pred_range, title)

    def plot3D(self, key: str, type: str = 'average') -> None:
        to_plot: dict = {'average': self.plane_average[key],
                         'maximum': self.plane_maximum[key],
                         'minimum': self.plane_minimum[key]}[type]
        
        # plot
        plot3D(to_plot, self.grass_range, self.pred_range)