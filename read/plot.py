import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot2D(to_plot: np.ndarray, grass_range: list[float], pred_range: list[float], title: str = None) -> None:
    # plot
    plt.imshow(to_plot.T, cmap = 'YlOrRd')
    plt.xlabel('Grass growth rate', fontweight = 'bold')
    plt.ylabel('Predators feed', fontweight = 'bold')
    plt.title(title)
    plt.ylim(plt.ylim()[1], plt.ylim()[0])
    new_xticks: np.ndarray = np.linspace(0, to_plot.shape[0] - 1, len(grass_range[::2]))
    new_yticks: np.ndarray = np.linspace(0, to_plot.shape[1] - 1, len(pred_range))
    plt.xticks(ticks = new_xticks, labels = grass_range[::2])
    plt.yticks(ticks = new_yticks, labels = pred_range)
    plt.colorbar()
    plt.show()

def plot3D(to_plot: np.ndarray, grass_range: list[float], pred_range: list[float]) -> None:
    # plot
    X, Y = np.meshgrid(pred_range, grass_range)
    fig, ax = plt.subplots(subplot_kw = {"projection": "3d"})
    surf = ax.plot_surface(X, Y, to_plot, cmap = cm.coolwarm, linewidth = 0, antialiased = False)
    ax.set_xlabel('Predators feed')
    ax.set_ylabel('Grass')
    plt.show()