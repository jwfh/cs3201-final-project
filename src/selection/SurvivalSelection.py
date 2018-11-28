import numpy as np

def sort_population(population, fitness): # sort a population based on fitness, from max to min
    pop_fit_pair = list(map(list,zip(population, fitness)))
    pop_fit_pair.sort(key=operator.itemgetter(1), reverse=True)
    sorted_pop = []
    sorted_fit = []
    for entry in pop_fit_pair:
        sorted_pop.append(entry[0])
        sorted_fit.append(entry[1])
    return sorted_pop, sorted_fit


def mu_plus_lambda(current_pop, current_fitness, offspring, offspring_fitness):   
    population = np.array ([])
    fitness = np.array ([])
    temp_pop = np.concatenate(np.copy(current_pop),np.copy(offspring))
    temp_fit = np.concatenate(np.copy(current_fitness),np.copy(offspring_fitness))
    sorted_pop, sorted_fit = sort_population(temp_pop, temp_fit)
    for i in range(0,current_pop.size):
        population = np.append(population, sorted_pop[i])
        fitness = np.append(fitness, sorted_fit[i])
    return population, fitness
