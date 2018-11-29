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
    # cities = population.initialization.init_file('../data/TSP_Uruguay_734.txt')
    cities = population.initialization.init_file('../data/TSP_WesternSahara_29.txt')
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
    improvement_threshold = 1
    # Spoof the previous min fitness so the loop starts
    previous_best_fitness = current_best_fitness + current_best_fitness
    while current_generation < GENERATION_LIMIT:
        # if current_generation > 0.5*GENERATION_LIMIT and \
        #         current_best_fitness < improvement_threshold*previous_best_fitness:
        #     print("FITNESS broke")
        #     break
        previous_best_fitness = current_best_fitness
        # print("Previous FITNESS", previous_best_fitness)

        parents_index = selection.mps.MPS(fitnesses, MATING_POOL_SIZE)

        np.random.shuffle(parents_index)
        xover_rate = 0.9
        mut_rate = 0.05
        offspring = []
        offspring_count = 0
        offspring_fitness = []
        while offspring_count < MATING_POOL_SIZE:
            #crossover
            if np.random.random() < xover_rate:
                a = candidate_indices[parents_index]
                b = offspring_count
                c = np.array(fitnesses[parents_index])
                d = c[offspring_count]
                off1 = crossover.inver_over.inver_over(
                    candidate_indices[parents_index],
                    offspring_count,
                    cities,
                    fitnesses[parents_index][offspring_count]
                )
            else:
                off1 = np.copy(candidate_indices[parents_index][offspring_count])

            #mutation
            if np.random.random() < mut_rate:
                off1 = mutation.scramble.scramble_swap(off1)
            offspring.append(off1)
            offspring_fitness.append(fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(cities[off1])))
            offspring_count += 1
        candidate_indices, fitnesses = selection.survival.mu_plus_lambda(candidate_indices, fitnesses, offspring, offspring_fitness)       
        current_best_fitness = np.min(fitnesses)
        print("Current FITNESS", current_best_fitness)
        current_generation += 1
    print("Best fitness:", fitnesses[np.where(fitnesses == current_best_fitness)[0][0]])
    print("Best route:", candidate_indices[np.where(fitnesses == current_best_fitness)[0][0]])
    

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main()
