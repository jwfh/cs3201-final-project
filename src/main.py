#!/usr/bin/env python3

########################################################
#        Course: COMP-3201                             #
#    Assignment: Final Course Project                  #
# Group Members: Jacob House (201614260)               # 
#                Nabil Miri (201547429)                #
#                Omar Mohamed (201501962)              #
#                Hassan El-Khatib (201504396)          #
########################################################

import crossover
import mutation
import fitness
import population
import selection

## Program entry point
def main() -> None:

    cities = population.initialization.init_file('../data/TSP_WesternSahara_29.txt')
    len_cities = cities.shape[0] # Get number of rows from shape
    
    # It is faster in Python to add something to itself than to multiply by 2
    pop_size = len_cities + len_cities
    cand_size = pop_size
    candidate_indices = population.candidates.pick_cands(len_cities, cand_size)

    distances = list()
    for city_index in candidate_indices:
        distance = fitness.distance.adjacent_distance(cities[city_index])
        distances.append(distance)
    # distances is now a list (of lists of each adjacent distance for each canidate)

    fitnesses = fitness.fitness.overall_fitness(distances)

    # So, guys, where do we go from here?

if __name__ == '__main__':
    # If the module is the main program, not an import then run main()
    main()
