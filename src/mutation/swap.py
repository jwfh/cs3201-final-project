#!/usr/bin/env python3

## System imports 
import numpy as np

## Local imports
from timing import timing

## Begin function mutation.swap.swap_individual
@timing
def swap_individual(individual: np.ndarray, mutation_factor: float=0.25) -> np.ndarray:
    mutant = individual
    length = mutant.shape[0]
    mutation_thresold = mutation_factor * length
    
    start_idx = end_idx = 0
    while end_idx-start_idx < mutation_thresold:
        start_idx = np.random.randint(0, length - 3)
        end_idx = np.random.randint(start_idx + 2, length - 1)

    mutant[start_idx], mutant[end_idx] = mutant[end_idx], mutant[start_idx]

    return mutant
## End function mutation.swap.swap_individual