import numpy as np
import random
fitnesses = np.array ([0,1,2,3,4,5])
PoolSize = int(pop_size/2)
def MPS(fitnesses, PoolSize):
    mates = np.array([])
    cumul_prop = np.array([])
    fit_sum = np.sum(fitnesses)
    cumul_prop = np.append(cumul_prop, fitnesses[0]/fit_sum)
    for i in range (1, fitnesses.size):
        cumul_prop = np.append(cumul_prop, cumul_prop[i-1] + fitness[i]/fit_sum)
    rv = random.uniform(0,1/PoolSize)
    i=0
    while len(mates) < PoolSize:
        while rv <= cumul_prop[i]:
            mates = np.append(mates,i)
            rv = rv +1/mating_pool_size
        i = i+1
    return mates
print(mates)