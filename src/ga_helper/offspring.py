#!/usr/bin/env python3

## System imports
import numpy as np

## Local imports
import fitness
import crossover 
import mutation

def new(offspring_count, candidates, parents_idxs, distances, fitnesses, xover_rate, mut_rate, mut_factor, mut_chooser):
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

    offspring_fitness = fitness.fitness.individual_fitness(fitness.distance.single_cand_adjacent_distance(distances, offspring))
    return offspring, offspring_fitness


def append_offspring_helper(offspring_tuple, offsprings, offspring_fitnesses):
    offsprings.append(offspring_tuple[0])
    offspring_fitnesses.append(offspring_tuple[1])