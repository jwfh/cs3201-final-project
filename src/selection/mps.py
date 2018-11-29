#!/usr/bin/env python3

import numpy as np
import random

def MPS(fitnesses: list, mating_pool_size: int) -> np.ndarray:
    
    selected_to_mate = []
    cumul_prop = []
    fit_sum = sum(fitnesses)
    cumul_prop.append(fitnesses[0] / fit_sum)

    # Compute division only once instead of repeating the same crap
    inverse_mating_pool_size = 1 / mating_pool_size
    
    for i in range(1, len(fitnesses)):
        cumul_prop.append(cumul_prop[i-1] + fitnesses[i] / fit_sum)

    rv = random.uniform(0, inverse_mating_pool_size)
    
    i = 0
    while len(selected_to_mate) < mating_pool_size:
        while rv <= cumul_prop[i]:
            selected_to_mate.append(i)
            rv += inverse_mating_pool_size
        
        i += 1
    
    return np.asarray(selected_to_mate)