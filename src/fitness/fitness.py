#!/usr/bin/env python3

from timing import timing
import numpy as np
from numba import jit, njit
import multiprocessing as mp

## Begin function fitness.fitness.overall_fitness
#@timing
@njit
def bulk_fitness(cand_distances: np.ndarray) -> np.ndarray:
    '''
    Computes the fitness for each candidate. Currently this just means returning a list of sums.

    @param cand_distances A two-dimensional np.ndarray of np.ndarrays containing each inter-city distances
                          for each candidate solution for the TSP.

    @return A list of sums of inter-city distancs of length equal to the number of candidates.
    '''

    with mp.Pool(processes=mp.cpu_count()) as pool:
        fitnesses = np.fromiter(pool.starmap(individual_fitness, cand_distances), dtype=np.float64, count=cand_distances.shape[0])
    
    return fitnesses
## End function fitness.fitness.overall_fitness

## Begin function fitness.fitness.individual_fitness
#@timing
def individual_fitness(candidate_distance: np.ndarray) -> np.float64:
    '''
    Computes fitness for a single individual.
    '''

    return _sum_dist(candidate_distance)
## End function fitness.fitness.individual_fitness

## Begin function fitness.fitness.sum_dist
@jit
def _sum_dist(candidate_distance: np.ndarray) -> int:
    '''
    Computes the sum of distances for a list representing a candidate solution.

    @param candidate_distance A list containing each inter-city distance for a candidate solution for the TSP.

    @return A list of sums of inter-city distancs of length equal to the number of candidates.
    '''
    return np.sum(candidate_distance)
## End function fitness.fitness.sum_dist

