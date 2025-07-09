import numpy as np

def test():
    filename = 'test'
    YEARS = 25
    GENES = [1]
    SEEDS = [0]
    GRASS_RATES = [50]
    PREDATORS_FEEDING = [5]

    return filename, YEARS, GENES, SEEDS, GRASS_RATES, PREDATORS_FEEDING

def preliminary():
    filename = 'preliminary'
    YEARS = 100
    GENES = [1]
    SEEDS = range(5)
    GRASS_RATES = np.arange(20 + 1) * 2.5
    PREDATORS_FEEDING = range(10 + 1)

    return filename, YEARS, GENES, SEEDS, GRASS_RATES, PREDATORS_FEEDING

def complete():
    filename = 'complete'
    YEARS = 1000
    GENES = list(range(10, 21))
    SEEDS = range(3, 5)
    GRASS_RATES = np.arange(10, 10 + 1) * 5
    # GRASS_RATES = np.arange(10, 10 + 1) * 5
    PREDATORS_FEEDING = range(4, 8 + 1)

    return filename, YEARS, GENES, SEEDS, GRASS_RATES, PREDATORS_FEEDING