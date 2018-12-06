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
import multiprocessing as mp
import time

## Local imports
import crossover
import mutation
import fitness
import population
import ga_helper
import selection
from functools import partial
from timing import timing

DEBUG = 1

## Program entry point
def main_helper() -> None:
    '''
    Helper function to precompute distances and pass to main so we can run the algo 
    multiple times without precomputing over and over.
    '''
    trials = 10
    tiny_dataset = '../data/TSP_WesternSahara_29.txt'
    small_dataset = '../data/TSP_Qatar_194.txt'
    medium_dataset = '../data/TSP_Uruguay_734.txt'
    large_dataset = '../data/TSP_Canada_4663.txt'
    extra_large_dataset = '../data/TSP_Italy_16862.txt'
    huge_dataset = '../data/TSP_China_71009.txt'

    selected_dataset = medium_dataset
    
    print("Computing", trials, "trials for", selected_dataset)
    
    cities = population.initialization.init_file(selected_dataset)
    distance_obj = fitness.distance.Distances(cities)
    distance_obj.gen_all()


    for trial in range(trials):
        main(distance_obj._weighted_adjacency)

@timing
def main(distances: np.ndarray) -> None:
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

    len_cities = distances.shape[0]

    candidates = population.candidates.pick_cands(len_cities, CAND_POOL_SIZE)
    candidate_distances = fitness.distance.adjacent_distance(distances, candidates, CAND_POOL_SIZE)
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        fitnesses = np.fromiter(pool.map(fitness.fitness.individual_fitness, candidate_distances), dtype=np.float, count=CAND_POOL_SIZE)
        
    # Initialization is done. Now do a few loops and call it a day.
    current_best_fitness = np.min(fitnesses)
    current_generation = 0
    last_change_gen = 0

    while current_generation < GENERATION_LIMIT:

        start_time = time.time()

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

        offspring_candidates, offspring_fitnesses = [], []
        
        with mp.Pool(processes=mp.cpu_count()) as pool:
            offspring = pool.map(partial(ga_helper.offspring.new, 
                                         candidates=candidates, 
                                         parents_idxs=parents_idxs, 
                                         distances=distances, 
                                         fitnesses=fitnesses, 
                                         xover_rate=xover_rate, 
                                         mut_rate=mut_rate, 
                                         mut_factor=mut_factor, 
                                         mut_chooser=mut_chooser
                                        ), 
                                 range(MATING_POOL_SIZE))

        for off in offspring:
            offspring_candidates.append(off[0])
            offspring_fitnesses.append(off[1])

        offspring_candidates = np.asarray(offspring_candidates)
        offspring_fitnesses = np.asarray(offspring_fitnesses)

        # Survivor selection
        if np.random.random() < par_chooser:
            # Use Mu+Lambda
            candidates, fitnesses = selection.survival.mu_plus_lambda(candidates, fitnesses, offspring_candidates, offspring_fitnesses)       
        else:
            # Use replacement
            candidates, fitnesses = selection.survival.replacement(candidates, fitnesses, offspring_candidates, offspring_fitnesses)

        current_best_fitness = np.min(fitnesses)
        elapsed_time = (time.time()-start_time)*1000.0

        if current_best_fitness < previous_best_fitness:
            print('\033[1;32;40m[BETTER FITNESS] \033[1;34;40m[%dms]\033[1;37;40m Generation %d (squared) fitness: %f' % (elapsed_time, current_generation, current_best_fitness))
            last_change_gen = current_generation
        elif current_best_fitness == previous_best_fitness:
            print(' \033[1;33;40m[EQUAL FITNESS] \033[1;34;40m[%dms]\033[1;37;40m Generation %d (squared) fitness: %f' % (elapsed_time, current_generation, current_best_fitness))
        else:
            print(' \033[1;31;40m[WORSE FITNESS] \033[1;34;40m[%dms]\033[1;37;40m Generation %d (squared) fitness: %f' % (elapsed_time, current_generation, current_best_fitness))

        current_generation += 1

    tf = fitness.distance.adjacent_distance(distances, candidates[np.where(fitnesses == current_best_fitness)[0][0]], true_distance=True)
    print("\r\nLast geration with improvement:", last_change_gen)
    print("Best route:", candidates[np.where(fitnesses == current_best_fitness)[0][0]])
    print("Best fitness:", fitness.fitness.individual_fitness(tf))

    

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main_helper()
