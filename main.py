from environment import Environment

from presets import test, preliminary, complete

def main(filename, YEARS, GENES, SEEDS, GRASS_RATES, FEEDS):
    for grass_rate in GRASS_RATES:
        GRASS_GROWTH_FUNCTION = [0] * 60 + [grass_rate] * 90 + [0] * 215
        for feed in FEEDS:
            for seed in SEEDS:
                print(f'Grass {grass_rate}, feed {feed}, seed {seed}')
                folder = f'simulations/{filename}/grass{grass_rate}/pred{feed}/seed{seed}'

                env = Environment(folder = folder,
                                  random_seed = seed,
                                  genes = GENES, 
                                  grass_growth_func = GRASS_GROWTH_FUNCTION, 
                                  predators_feeding = feed)
                env.run(YEARS)

if __name__ == '__main__':
    # simulation = preliminary
    # main(*simulation())

    simulation = complete
    main(*simulation())