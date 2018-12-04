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
import numba
import multiprocessing.dummy as mpd

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

    tiny_dataset = '../data/TSP_WesternSahara_29.txt'
    small_dataset = '../data/TSP_Qatar_194.txt'
    medium_dataset = '../data/TSP_Uruguay_734.txt'
    large_dataset = '../data/TSP_Canada_4663.txt'
    extra_large_dataset = '../data/TSP_Italy_16862.txt'
    huge_dataset = '../data/TSP_China_71009.txt'

    GENERATION_LIMIT = 1000
    CAND_POOL_SIZE = 50
    MATING_POOL_SIZE = int(CAND_POOL_SIZE * 0.5)

    cities = population.initialization.init_file(tiny_dataset)
    distances = fitness.distance.Distances(cities)
    len_cities = len(distances)
    del cities

    candidates = population.candidates.pick_cands(len_cities, CAND_POOL_SIZE)

    with mpd.Pool() as pool:
        fitnesses = np.fromiter(pool.map(lambda candidate: fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(distances, candidate)), candidates), dtype=np.float, count=CAND_POOL_SIZE)

    current_best_fitness = np.min(fitnesses)

    # Initialization is done. Now do a few loops and call it a day.

    current_generation = 0
    while current_generation < GENERATION_LIMIT:

        parents_idxs = selection.mps.MPS(fitnesses, MATING_POOL_SIZE)

        np.random.shuffle(parents_idxs)
        xover_rate = 0.9
        mut_rate = 0.05
        offspring = []
        offspring_count = 0
        offspring_fitness = []
        while offspring_count < MATING_POOL_SIZE:
            #crossover
            if np.random.random() < xover_rate:
                off1 = crossover.inver_over.inver_over(
                    candidates[parents_idxs],
                    offspring_count,
                    distances,
                    fitnesses[parents_idxs][offspring_count]
                )
            else:
                off1 = np.copy(candidates[parents_idxs][offspring_count])

            #mutation
            if np.random.random() < mut_rate:
                off1 = mutation.scramble.scramble_swap(off1)
            offspring.append(off1)
            offspring_fitness.append(fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(distances, off1)))
            offspring_count += 1
        candidates, fitnesses = selection.survival.mu_plus_lambda(candidates, fitnesses, offspring, offspring_fitness)       
        current_best_fitness = np.min(fitnesses)
        print("Current FITNESS", current_best_fitness)
        current_generation += 1
    print("Best fitness:", fitnesses[np.where(fitnesses == current_best_fitness)[0][0]])
    print("Best route:", candidates[np.where(fitnesses == current_best_fitness)[0][0]])
    tf = fitness.distance.adjacent_distance(distances, candidates[np.where(fitnesses == current_best_fitness)[0][0]], true_distance=True)
    print("True best fitness:", fitness.fitness.individual_fitness(tf))
    

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main()
