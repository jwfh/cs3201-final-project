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
from numba import jit, njit
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

    GENERATION_LIMIT = 5000
    CAND_POOL_SIZE = 50
    MATING_POOL_SIZE = int(CAND_POOL_SIZE * 0.5)
    XOVER_RATE = {
        'low':   0.50,
        'normal': 0.90
    }
    MUT_TYPE_FAVOR = {
        'even':     0.50,
        'scramble': 0.80
    }
    MUT_RATE = {
        'high':   0.70,
        'normal': 0.10
    }
    MUT_FACTOR = {
        'high':   0.40,
        'normal': 0.10
    }
    PAR_TYPE_FAVOUR = {
        'replacement': 0.25,
        'mu_lambda': 0.75
    }

    cities = population.initialization.init_file(tiny_dataset)
    distances = fitness.distance.Distances(cities)
    len_cities = distances.length
    del cities

    candidates = population.candidates.pick_cands(len_cities, CAND_POOL_SIZE)

    with mpd.Pool() as pool:
        fitnesses = np.fromiter(pool.map(lambda candidate: fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(distances, candidate)), candidates), dtype=np.float, count=CAND_POOL_SIZE)

    current_best_fitness = np.min(fitnesses)

    # Initialization is done. Now do a few loops and call it a day.

    current_generation = 0
    last_change_gen = 0

    def new_offspring(offspring_count):
        if np.random.random() < xover_rate:
                offspring = crossover.inver_over.inver_over(
                    candidates[parents_idxs],
                    offspring_count,
                    distances,
                    fitnesses[parents_idxs][offspring_count]
                )
        else:
            offspring = np.copy(candidates[parents_idxs][offspring_count])

        #mutation
        if np.random.random() < mut_rate:
            if np.random.random() < mut_chooser:
                offspring = mutation.scramble.scramble_individual(offspring, mut_factor)
            else:
                offspring = mutation.swap.swap_individual(offspring, mut_factor)

        offspring_fitness = fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(distances, offspring))
        return offspring, offspring_fitness

    def append_offspring_helper(offspring, offspring_fitness):
        offsprings.append(offspring)
        offspring_fitnesses.append(offspring_fitness)


    while current_generation < GENERATION_LIMIT:

        parents_idxs = selection.parent.mps(fitnesses, MATING_POOL_SIZE)

        np.random.shuffle(parents_idxs)

        if current_generation < 0 and current_best_fitness == previous_best_fitness:
            # Let's throw some randomness into this 
            mut_chooser = MUT_TYPE_FAVOR['scramble']
            mut_rate = MUT_RATE['high']
            xover_rate = XOVER_RATE['low']
            mut_factor = MUT_FACTOR['high']
            par_chooser = PAR_TYPE_FAVOUR['replacement']
        elif False :
            pass 
        else:
            mut_chooser = MUT_TYPE_FAVOR['even']
            mut_rate = MUT_RATE['normal']
            xover_rate = XOVER_RATE['normal']
            mut_factor = MUT_FACTOR['normal']
            par_chooser = PAR_TYPE_FAVOUR['mu_lambda']

        previous_best_fitness = current_best_fitness

        offsprings = []
        offspring_count = 0
        offspring_fitnesses = []
        # while offspring_count < MATING_POOL_SIZE:
        #     #crossover
        #     if np.random.random() < xover_rate:
        #         offspring = crossover.inver_over.inver_over(
        #             candidates[parents_idxs],
        #             offspring_count,
        #             distances,
        #             fitnesses[parents_idxs][offspring_count]
        #         )
        #     else:
        #         offspring = np.copy(candidates[parents_idxs][offspring_count])

        #     #mutation
        #     if np.random.random() < mut_rate:
        #         if np.random.random() < mut_chooser:
        #             offspring = mutation.scramble.scramble_individual(offspring, mut_factor)
        #         else:
        #             offspring = mutation.swap.swap_individual(offspring, mut_factor)

        with mpd.Pool() as pool:
            map(lambda offspring_tuple: append_offspring_helper(*offspring_tuple), pool.map(new_offspring, range(MATING_POOL_SIZE)))

        # offsprings.append(offspring)
        # offspring_fitnesses.append(fitness.fitness.individual_fitness(fitness.distance.adjacent_distance(distances, offspring)))

            # offspring_count += 1
        
        # offsprings = np.asarray(offsprings)

        # Survivor selection
        if np.random.random() < par_chooser:
            # Use Mu+Lambda
            candidates, fitnesses = selection.survival.mu_plus_lambda(candidates, fitnesses, offsprings, offspring_fitnesses)       
        else:
            # Use replacement
            candidates, fitnesses = selection.survival.replacement(candidates, fitnesses, offsprings, offspring_fitnesses)

        current_best_fitness = np.min(fitnesses)
        if current_best_fitness < previous_best_fitness:
            print('\033[1;32;40m[BETTER FITNESS]\033[1;37;40m Generation %d (squared) fitness: %f' % (current_generation, current_best_fitness))
            last_change_gen = current_generation
        elif current_best_fitness == previous_best_fitness:
            print(' \033[1;33;40m[EQUAL FITNESS]\033[1;37;40m Generation %d (squared) fitness: %f' % (current_generation, current_best_fitness))
        else:
            print(' \033[1;31;40m[WORSE FITNESS]\033[1;37;40m Generation %d (squared) fitness: %f' % (current_generation, current_best_fitness))

        current_generation += 1

    tf = fitness.distance.adjacent_distance(distances, candidates[np.where(fitnesses == current_best_fitness)[0][0]], true_distance=True)
    print("\r\nLast geration with improvement:", last_change_gen)
    print("Best route:", candidates[np.where(fitnesses == current_best_fitness)[0][0]])
    print("Best fitness:", fitness.fitness.individual_fitness(tf))

    

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main()
