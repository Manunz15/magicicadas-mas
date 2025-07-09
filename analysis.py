from read import AverageSimulation, Results

# test
sim = AverageSimulation('simulations/preliminary_final',
                        grass = 'grass25.0',
                        pred = 'pred6',
                        )
sim.fit()
sim.plot('complete')

res: Results = Results('results/preliminary_final')
res.plot2D('1')
res.plot2D('predators')

# final simulation
sim = AverageSimulation('simulations/complete',
                        grass = 'grass30',
                        pred = 'pred6')
sim.plot()

res: Results = Results('results/complete')
res.prime_numbers()
res.plot2D('predators')
for i in range(10, 20 + 1):
    print(i)
    res.plot2D(str(i))
