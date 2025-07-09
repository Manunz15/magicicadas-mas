import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from tqdm import tqdm

from read.average import AverageSimulation
from read.plot import plot2D, plot3D

class SurvivalPlane:
    def __init__(self, filename: str, save_filename: str) -> None:
        self.filename: str = filename
        self.save_filename: str = save_filename

        self.read()
        self.calc()
        self.save()

    def read(self) -> None:
        # read
        self.sim_list: list[list[AverageSimulation]] = []
        self.grass_range: list[float] = []
        self.pred_range: list[float] = []

        for i, grass in tqdm(enumerate(os.listdir(self.filename))):
            self.grass_range.append(float(grass[5:]))
            row_list: list[AverageSimulation] = []
            for pred in os.listdir(os.path.join(self.filename, grass)):
                row_list.append(AverageSimulation(self.filename, grass, pred))
                if not i:
                    self.pred_range.append(float(pred[4:]))

            self.sim_list.append(row_list)

    def calc(self) -> None:
        # sort
        sorted_sim_list: list[list[AverageSimulation]] = []
        for row in self.sim_list:
            sorted_sim_list.append([sim for _, sim in sorted(zip(self.pred_range, row))])
        self.sim_list: list[list[AverageSimulation]] = [row for _, row in sorted(zip(self.grass_range, sorted_sim_list))]

        self.grass_range.sort()
        self.pred_range.sort()

        # single values
        arr_shape: list[int] = [len(self.sim_list), len(self.sim_list[0])]
        self.plane_average: np.ndarray = {key: np.zeros(arr_shape) for key in self.sim_list[0][0].final_average.keys()}
        self.plane_maximum: np.ndarray = {key: np.zeros(arr_shape) for key in self.sim_list[0][0].final_average.keys()}
        self.plane_minimum: np.ndarray = {key: np.zeros(arr_shape) for key in self.sim_list[0][0].final_average.keys()}
        
        for i, row in enumerate(self.sim_list):
            for j, sim in enumerate(row):
                for key in sim.final_average.keys():
                    self.plane_average[key][i, j] = sim.final_average[key]
                    self.plane_maximum[key][i, j] = sim.final_maximum[key]
                    self.plane_minimum[key][i, j] = sim.final_minimum[key]

    def save(self) -> None:
        if not os.path.exists(self.save_filename):
            os.mkdir(self.save_filename)

        # save grass and feed
        np.save(os.path.join(self.save_filename, 'grass'), np.array(self.grass_range))
        np.save(os.path.join(self.save_filename, 'pred'), np.array(self.pred_range))
        
        # save data
        for name, dict in zip(['average', 'max', 'min'], [self.plane_average, self.plane_maximum, self.plane_minimum]):
            path: str = os.path.join(self.save_filename, name)
            if not os.path.exists(path):
                os.mkdir(path)

            for key in dict.keys():
                np.save(os.path.join(path, key), dict[key])


    def plot2D(self, key: str, type: str = 'average') -> None:
        to_plot: dict = {'average': self.plane_average[key],
                         'maximum': self.plane_maximum[key],
                         'minimum': self.plane_minimum[key]}[type]
        plot2D(to_plot)

    def plot3D(self, key: str, type: str = 'average') -> None:
        to_plot: dict = {'average': self.plane_average[key],
                         'maximum': self.plane_maximum[key],
                         'minimum': self.plane_minimum[key]}[type]
        plot3D(to_plot, self.grass_range, self.pred_range)