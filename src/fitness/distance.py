#!/usr/bin/env python3

from timing import timing
import numpy as np
import numba
from numba import jit, njit, jitclass, int32, float64
import multiprocessing as mp
from parallel import parallel_map
import pathos.multiprocessing as pmp

distance_spec = [
    ('_cities', float64[:,:]),
    ('_weighted_adjacency', float64[:,:])
]

## Begin class fitness.distance.Distances
#@jitclass(distance_spec)
class Distances:
    '''
    Singleton class used to perform distance calculations either
        (i) all up front when the input file is loaded using mulithreading; or
       (ii) as the calculations are required.
    All calculated values are stored in a NumPy array and precomputed values are retrieved
    from the array if they are needed again throughout the program.
    '''

    ## Begin function fitness.distance.Distances.__init__
    def __init__(self, cities: np.ndarray):
        '''
        Store the cities as a NumPy array and allocate an N by N NumPy array to store distance
        information in.
        '''

        self._cities = cities
        self._weighted_adjacency = np.zeros((self._cities.shape[0], self._cities.shape[0]))
    ## End function fitness.distance.Distances.__init__

    ## Begin function fitness.distance.Distances._add_edge
    def _add_edge(self, start_idx, end_idx, start_end_dist=None) -> None:
        '''
        Adds an "edge" between two cities by populating the adjacency cell in the matrix created
        in the constructor with the [cheaply calculated] distance between the two cities. Uses 
        self._distance for the calculation.

        Adds the distance A -> B and B -> A.
        '''

        if start_end_dist == None:
            start_end_dist =  self._distance(self._cities[start_idx], self._cities[end_idx])
        self._weighted_adjacency[start_idx][end_idx] = start_end_dist
        self._weighted_adjacency[end_idx][start_idx] = start_end_dist
    ## Begin function fitness.distance.Distances._add_edge

    def _add_edge_mapper_helper(self, start_idx, end_idx, ) -> None:

        return start_idx, end_idx, self._distance(self._cities[start_idx], self._cities[end_idx])
    
    ## Begin function fitness.distance.Distances._distance
    def _distance(self, start_city: np.ndarray, end_city: np.ndarray) -> float:
        '''
        Private [cheap] distance calculator function.

        \em Note: The square root function is very computationally expensive. Instead, let's just not compute the root
        and instead deal with the square of the real distance; we'll just be comparing if sqrt(a) < sqrt(b) later on and 
        if a >= 1 and b >= 1 then a < b if, and only if, sqrt(a) < sqrt(b). The first condition should be satisfied for
        all cities. (To make certain of this, there is an assertion added.)
        '''

        x1, y1 = start_city[0], start_city[1]
        x2, y2 = end_city[0], end_city[1]
        square_city_distance = (x2-x1)**2 + (y2-y1)**2

        assert square_city_distance >= 1, "The distance between two cities should be more than 1."

        return square_city_distance
    ## End function fitness.distance.Distances._distance

    ## Begin function fitness.distance.Distances.gen_all
    @timing
    def gen_all(self) -> None:
        '''
        [Cheaply] Generates all distances between all pairs of cities.

        Uses multithreading.
        '''

        # Generate all non-symmetric pairs (i.e., not (1, 2) and (2, 1))
        city_pairs = ((start_idx, end_idx) for start_idx in range(self._cities.shape[0]) \
                                           for end_idx in range(start_idx + 1, self._cities.shape[0]))
        # Spread this across the computer's cores
        with mp.Pool(processes=mp.cpu_count()) as pool:
            [self._add_edge(*data_point) for data_point in pool.starmap(self._add_edge_mapper_helper, city_pairs)]

    ## End function fitness.distance.Distances.gen_all

    ## Begin function fitness.distance.Distances.get
    #def get(self, start_idx: int, end_idx: int, true_distance: bool=False) -> float:
    #    '''
    #    Returns the distance between two cities. Accepts two city indices as input. Optional boolean
    #    parameter to return the true distance (by performing the square root) or cheap distance.

    #    If start_idx is equal to end_idx then just return zero.
    #    '''

    #    if start_idx == end_idx:
    #        return 0.0
    #    elif self._weighted_adjacency[start_idx][end_idx] == 0.0:
    #        self._add_edge(start_idx, end_idx)
    #    if true_distance:
    #        return np.sqrt(self._weighted_adjacency[start_idx][end_idx])
    #    else:
    #        return self._weighted_adjacency[start_idx][end_idx]
    ## End function fitness.distance.Distances.get

    ## Begin property fitness.distance.Distances.length
    #@property
    #def length(self) -> int:
    #    '''
    #    Returns the length of the object as the number of cities in self._cities.
    #    '''

    #    return self._cities.shape[0]
    ## End property fitness.distance.Distances.length
## End class fitness.distance.Distances

## Begin function fitness.distance.adjacent_distance
#@timing
@jit
def adjacent_distance(distances: np.ndarray, city_idxs: np.ndarray, num_cities: int, true_distance :bool=False) -> np.ndarray:
    '''
    This function computes the distance between adjacent cities in a list `cities' passed to the function.

    We expect an entry in cities to be an integer denoting the index of the city in being traveled.

    In the last iteration, i+1 will, using modular arithmetic, wrap back around to the beginning of the array 
    to compute the Euclidean distance between the last city and the first in the list.

    @param cities An ordered list of city indices. That is, the candidate solution in the TSP problem.

    @return A list of distances between adjacent cities.
    '''
    adjacent_distances = []
    for j in range(num_cities):
        city_idx = city_idxs[j]
        distance = single_cand_adjacent_distance(distances, city_idx, true_distance)
        adjacent_distances.append(distance)

    #return [[distances[city_idx[i]][city_idx[(i+1) % city_idx.shape[0]]] for i in range(city_idx.shape[0])] for city_idx in city_idxs]
    return adjacent_distances
## End function fitness.distance.adjacent_distance

@njit
def single_cand_adjacent_distance(distances: np.ndarray, city_idx: np.ndarray, true_distance: bool=False) -> np.ndarray:
    dist = []
    if true_distance:
        for i in range(city_idx.shape[0]):
            start_idx = city_idx[i]
            end_idx = city_idx[(i+1) % city_idx.shape[0]]
            d = distances[start_idx][end_idx] ** 0.5
            dist.append(d)
    else:
        for i in range(city_idx.shape[0]):
            start_idx = city_idx[i]
            end_idx = city_idx[(i+1) % city_idx.shape[0]]
            d = distances[start_idx][end_idx]
            dist.append(d)
    return np.array(dist)