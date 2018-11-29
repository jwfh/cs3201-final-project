#!/usr/bin/env python3

########################################################
#        Course: COMP-3201                             #
#    Assignment: Final Course Project                  #
# Group Members: Jacob House (201614260)               #
#                Nabil Miri (201547429)                #
#                Omar Mohamed (201501962)              #
#                Hassan El-Khatib (201504396)          #
########################################################

## System imports
import numpy as np

## Local imports
import crossover
import mutation
import fitness
import population
import selection
from timing import timing

DEBUG = 1

## Program entry point
@timing 
def main() -> None:

    #cities = population.initialization.init_file('../data/TSP_Canada_4663.txt')
    cities = population.initialization.init_file('../data/TSP_Uruguay_734.txt')
    # cities = population.initialization.init_file('../data/TSP_WesternSahara_29.txt')
    len_cities = cities.shape[0] # Get number of rows from shape

    # It is faster in Python to add something to itself than to multiply by 2
    CAND_POOL_SIZE = len_cities + len_cities
    MATING_POOL_SIZE = int(CAND_POOL_SIZE * 0.5)
    candidate_indices = population.candidates.pick_cands(len_cities, CAND_POOL_SIZE)

    distances = []
    for city_index in candidate_indices:
        # NumPy arrays allow passing array-like object to __getitem__
        distance = fitness.distance.adjacent_distance(cities[city_index])
        distances.append(distance)

    fitnesses = fitness.fitness.overall_fitness(distances)
    current_best_fitness = np.min(fitnesses)

    # So, guys, where do we go from here? Nabil comes and saves the day
    current_generation = 0
    GENERATION_LIMIT = 100
    improvement_threshold = 0.95
    # Spoof the previous min fitness so the loop starts
    previous_best_fitness = current_best_fitness + current_best_fitness
    while current_generation < GENERATION_LIMIT and \
            current_best_fitness < improvement_threshold*previous_best_fitness:
        previous_best_fitness = current_best_fitness

        parents_index = selection.mps.MPS(fitnesses, MATING_POOL_SIZE)

        np.random.shuffle(parents_index)
        xover_rate = 0.9
        mut_rate = 0.1
        offspring = np.array([])
        offspring_count = 0
        offspring_fitness = np.array([])
        i = 0
        #crossover
        while len(offspring) < MATING_POOL_SIZE:
            if random.random() < xover_rate:
                off1 = crossover.inver_over.inver_over(distances[parents_index[i]])
                off2 = crossover.inver_over.inver_over(distances[parents_index[i+1]])
            else:
                off1 = np.copy(distances[parents_index[i]])
                off2 = np.copy(distances[parents_index[i+1]])

            #mutation
            if random.random() < mut_rate:
                off1 = mutation.scramble.scramble_swap(off1)
            if random.random() < mut_rate:
                off2 = mutation.scramble.scramble_swap(off2)
            offspring = np.append(off1, axis=0)
            offspring_fitness = np.append(fitness.fitness.individual_fitness(off1))
            offspring = np.append(off2, axis=0)
            offspring_fitness = np.append(fitness.fitness.individual_fitness(off2))
            i = i + 2
            distances, fitnesses = selection.SurvivalSelection.mu_plus_lambda(distances, fitnesses, offspring, offspring_fitness)       

   
        """
        while offspring_count < MATING_POOL_SIZE:
            
            i += 1
        """

        current_generation += 1

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main()
