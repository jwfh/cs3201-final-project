#!/usr/bin/env python3

########################################################
#        Course: COMP-3201                             #
#    Assignment: Final Course Project                  #
# Group Members: Jacob House (201614260)               #
#                Nabil Miri (201547429)                #
#                Omar Mohamed (201501962)              #
#                Hassan El-Khatib (201504396)          #
########################################################

import random

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
    POP_SIZE = len_cities * len_cities
    MATING_POOL_SIZE = int(POP_SIZE * 0.5)
    candidate_indices = population.candidates.pick_cands(len_cities, POP_SIZE)

    distances = []
    for city_index in candidate_indices:
        # NumPy arrays allow passing array-like object to __getitem__
        distance = fitness.distance.adjacent_distance(cities[city_index])
        distances.append(distance)

    fitnesses = fitness.fitness.overall_fitness(distances)

    # So, guys, where do we go from here? Nabil comes and saves the day
    current_generation = 0
    GENERATION_LIMIT = 100
    while current_generation < GENERATION_LIMIT:

        parents_index = selection.mps.MPS(fitnesses, MATING_POOL_SIZE)

        random.shuffle(parents_index)

        offspring = []
        offspring_fitness = []
        i = 0
        """
        while len(offspring) < MATING_POOL_SIZE:

            i += 1
        """

        current_generation += 1

if __name__ == '__main__':
    # If the module is the main program, not an import, then run main()
    main()
