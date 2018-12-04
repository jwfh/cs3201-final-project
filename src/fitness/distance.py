#!/usr/bin/env python3

from timing import timing
import numpy as np
from numba import jit
import multiprocessing.dummy as mpd

## Begin class fitness.distance.Distances
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
    def _add_edge(self, start_idx, end_idx) -> None:
        '''
        Adds an "edge" between two cities by populating the adjacency cell in the matrix created
        in the constructor with the [cheaply calculated] distance between the two cities. Uses 
        self._distance for the calculation.

        Adds the distance A -> B and B -> A.
        '''

        start_end_dist =  self._distance(self._cities[start_idx], self._cities[end_idx])
        self._weighted_adjacency[start_idx][end_idx] = start_end_dist
        self._weighted_adjacency[end_idx][start_idx] = start_end_dist
    ## Begin function fitness.distance.Distances._add_edge
    
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
    def gen_all(self) -> None:
        '''
        [Cheaply] Generates all distances between all pairs of cities.

        Uses multithreading.
        '''

        # Generate all non-symmetric pairs (i.e., not (1, 2) and (2, 1))
        city_pairs = ((start_idx, end_idx) for start_idx in range(self._cities.shape[0]) \
                                           for end_idx in range(start_idx + 1, self._cities.shape[0]))
        # Spread this across the computer's cores
        with mpd.Pool() as pool:
            pool.map(lambda city_pair: self._add_edge(*city_pair), city_pairs)
    ## End function fitness.distance.Distances.gen_all

    ## Begin function fitness.distance.Distances.get
    def get(self, start_idx: int, end_idx: int, true_distance: bool=False) -> float:
        '''
        Returns the distance between two cities. Accepts two city indices as input. Optional boolean
        parameter to return the true distance (by performing the square root) or cheap distance.

        If start_idx is equal to end_idx then just return zero.
        '''

        if start_idx == end_idx:
            return 0.0
        elif self._weighted_adjacency[start_idx][end_idx] == 0.0:
            self._add_edge(start_idx, end_idx)
        if true_distance:
            return np.sqrt(self._weighted_adjacency[start_idx][end_idx])
        else:
            return self._weighted_adjacency[start_idx][end_idx]
    ## End function fitness.distance.Distances.get

    ## Begin function fitness.distance.Distances.__len__
    def __len__(self) -> int:
        '''
        Returns the length of the object as the number of cities in self._cities.
        '''

        return self._cities.shape[0]
    ## End function fitness.distance.Distances.__len__
## End class fitness.distance.Distances

## Begin function fitness.distance.adjacent_distance
@timing
# @jit
def adjacent_distance(distances: Distances, city_idxs: list, true_distance :bool=False) -> np.ndarray:
    '''
    This function computes the distance between adjacent cities in a list `cities' passed to the function.

    We expect an entry in cities to be an integer denoting the index of the city in being traveled.

    In the last iteration, i+1 will, using modular arithmetic, wrap back around to the beginning of the array 
    to compute the Euclidean distance between the last city and the first in the list.

    @param cities An ordered list of city indices. That is, the candidate solution in the TSP problem.

    @return A list of distances between adjacent cities.
    '''

    # Number of cities in the passed-in list
    num_cities = len(city_idxs)

    # Helper function to map the calculation to
    def invoke_dist_calc(i: int) -> float:
        return distances.get(city_idxs[i], city_idxs[(i+1) % num_cities])

    # If there are less than 100 cities in the route just do it on 1 core. Otherwise thread it.
    if num_cities < 100:
        adjacent_distances = np.fromiter(map(invoke_dist_calc, range(num_cities)), dtype=np.float)
    else:
        with mpd.Pool() as pool:
            adjacent_distances = np.fromiter(pool.map(invoke_dist_calc, range(num_cities)), dtype=np.float)
    return adjacent_distances
## End function fitness.distance.adjacent_distance