#!/usr/bin/env python3

## Begin function fit.fit
def fit(distances: list) -> list:
    '''
    WIP; don't touch.

    Computes the average distance between [?]

    '''

    fit = []

    for i in range(len(distances)):
        avg = 0
        summer = 0
        for j in range(len(distances[i])):
            summer = summer + distances[i][j]
        avg = summer/len(distances[i])
        fit.append(avg)
    
    return fit
## End function fit.fitness