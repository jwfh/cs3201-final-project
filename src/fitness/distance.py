#!/usr/bin/env python3

## Begin function fit.distance
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

    # Iterate i in {0, 1, 2, ..., (num_cities-1)}
    for i in range(num_cities):
        x1 = cities[i+1 % num_cities][0]
        x2 = cities[i % num_cities][0]
        y1 = cities[i+1 % num_cities][1]
        y2 = cities[i % num_cities][1]
        # I don't like that these are floats. Any way to make them all integers and avoid float multiplication?
        delta_x = ((x2 - x1)**2) 
        delta_y = ((y2 - y1)**2)
        square_city_distance = delta_x + delta_y

        assert(square_city_distance >= 1, "The distance between two cities should be more than 1.")

        distances.append(square_city_distance)

    return distances
## End function fit.distance