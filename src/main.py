#!/usr/bin/env python3

########################################################
#        Course: COMP-3201                             #
#    Assignment: Final Course Project                  #
# Group Members: Jacob House (201614260)               # 
#                Nabil Miri (201547429)                #
#                Omar Mohamed (201501962)              #
#                Hassan El-Khatib (201504396)          #
########################################################


## System Imports
import random
import math

## Local imports
import crossover
import mutation
import fitness
import population
import selection

## Begin function main
def main():
    cities = population.initialization.init_file('../data/TSP_WesternSahara_29.txt')
    len_cities = len(cities)
    
    # It is faster in Python to add something to itself than to multiply by 2
    pop_size = len_cities + len_cities
    cand_size = pop_size
    candidates = population.candidates.pick_cands(cities, cand_size)

    distances = list()
    for i in range(cand_size):
        distance = fitness.distance.adjacent_distance(candidates[i])
        distances.append(distance)
    # distances is now a list (of lists of each adjacent distance for each canidate)

    fitnesses = fitness.fitness.overall_fitness(distances)

    # So, guys, where do we go from here?

## End function main

if __name__ == '__main__':
    # If the module is the main program, not an import then run main()
    main()
