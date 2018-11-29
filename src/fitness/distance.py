#!/usr/bin/env python3

from timing import timing
import numpy as np
import time

## Begin function fitness.distance.adjacent_distance
# @timing
def adjacent_distance(cities: list) -> list:
    '''
    This function computes the distance between adjacent cities in a list `cities' passed to the function.

    We expect an entry in cities to be two-dimensional list
        - cities[i][0] is the longitude as a float
        - cities[i][1] is the latitude as a float
    Then the computation is, $d_{i, i+1} = \sqrt{ (cities[i+1][0] - cities[i][0])^2 + (cities[i+1][1] - 
    cities[i][1])^2 }$. In the last iteration, i+1 will, using modular arithmetic, wrap back around 
    to the beginning of the array to compute the Euclidean distance between the last city and the first in the list.

    \em Note: The square root function is very computationally expensive. Instead, let's just not compute the root
    and instead deal with the square of the real distance; we'll just be comparing if sqrt(a) < sqrt(b) later on and 
    if a >= 1 and b >= 1 then a < b if, and only if, sqrt(a) < sqrt(b). The first condition should be satisfied for
    all cities. (To make certain of this, there is an assertion added in the loop.)

    @param cities An ordered list of cities. That is, the candidate solution in the TSP problem.

    @return A list of distances between adjacent cities.
    '''

    # List storing distance between adjacent cities
    distances = []

    # Number of cities in the passed-in list; len() is O(n) not constant... let's minimize computation
    num_cities = len(cities)

    # Experimentation revealed that accessing is much more costly than our little computation.
    # We're initializing x1,y1 outside the loop (i-1) and only getting x2,y2 at the beginning of each 
    # iteration (i). Then do stuff with these and reassign x1,y2 to the next thing (i+1), passing it 
    # to the next iteration where i := i+2.
    x1 = cities[0][0] 
    y1 = cities[0][1] 
    for i in range(1, num_cities, 2):

        x2 = cities[i % num_cities][0]
        y2 = cities[i % num_cities][1]

        # I don't like that these are floats. Any way to make them all integers and avoid float multiplication?
        delta_x = ((x2 - x1)**2)
        delta_y = ((y2 - y1)**2)
        square_city_distance_1_2 = delta_x + delta_y

        x1 = cities[(i+1) % num_cities][0]
        y1 = cities[(i+1) % num_cities][1]

        delta_x = ((x1 - x2)**2)
        delta_y = ((y1 - y2)**2)
        square_city_distance_2_3 = delta_x + delta_y

        assert square_city_distance_1_2 >= 1, "The distance between two cities should be more than 1."
        assert square_city_distance_2_3 >= 1, "The distance between two cities should be more than 1."
        
        distances.append(square_city_distance_1_2)
        distances.append(square_city_distance_2_3)

    if num_cities % 2:
        # We need ONE more computation to wrap around
        assert x1 == cities[-1][0] and y1 == cities[-1][1], "Value of x1 and y1 are wrong."
        x2 = cities[0][0] 
        y2 = cities[0][1]
        delta_x = ((x2 - x1)**2)
        delta_y = ((y2 - y1)**2)
        last_square_city_distance = delta_x + delta_y
        distances.append(last_square_city_distance)

    return distances
## End function fitness.distance.adjacent_distance