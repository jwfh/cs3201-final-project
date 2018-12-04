import numpy as np
import operator
from timing import timing

@timing 
def sort_population(population, fitness):
        pop_fit_pair = list(map(list,zip(population, fitness)))
        pop_fit_pair.sort(key=operator.itemgetter(1), reverse=True)
        sorted_pop = []
        sorted_fit = []
        for entry in pop_fit_pair:
                sorted_pop.append(entry[0])
                sorted_fit.append(entry[1])
        return np.asarray(sorted_pop), np.asarray(sorted_fit)

@timing
def mu_plus_lambda(current_pop, current_fitnesses, offspring, offspring_fitnesses):
        population = []
        fitness = []
        temp_pop = np.concatenate((np.copy(current_pop), np.copy(offspring)))
        temp_fit = np.concatenate((np.copy(current_fitnesses), np.copy(offspring_fitnesses)))
        sorted_pop, sorted_fit = sort_population(temp_pop, temp_fit)
        # print("Min FITNESS", np.min(temp_fit), np.where(sorted_fit == np.min(temp_fit)))
        # print("FITNESS size", current_pop.shape[0], sorted_pop.shape[0])
        for i in range(0, current_pop.shape[0]):
                population.append(sorted_pop[sorted_pop.shape[0]-i-1])
                fitness.append(sorted_fit[sorted_pop.shape[0]-i-1])
        return np.asarray(population), np.asarray(fitness)
