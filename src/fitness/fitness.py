#!/usr/bin/env python3

from timing import timing

## Begin function fit.fitness
@timing
def overall_fitness(cand_distances: list) -> list:
    '''
    Computes the fitness for each candidate. Currently this just means returning a list of sums.

    @param cand_distances A two-dimensional list of lists containing each inter-city distances
                          for each candidate solution for the TSP.

    @return A list of sums of inter-city distancs of length equal to the number of candidates.
    '''
    
    fitnesses = sum_dist(cand_distances)
    
    return fitnesses
## End function fit.fitness

## Begin function fit.sum_dist
def sum_dist(cand_distances: list) -> list:
    '''
    Computes the sum of distances for each sub-list representing each candidate solution.

    @param cand_distances A two-dimensional list of lists containing each inter-city distances
                          for each candidate solution for the TSP.

    @return A list of sums of inter-city distancs of length equal to the number of candidates.
    '''
    return list(map(sum, cand_distances))
## End function fit.sum_dist