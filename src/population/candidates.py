#!/usr/bin/env python3

## System imports
import numpy as np

from timing import timing

## Begin function population.candidates.pick_cands
@timing
def pick_cands(num_cities: int, num_candidates: int) -> list:
    '''
    Randomly select num_candidates permutations from [0, num_cities).

    @return Resulting values represent indices into original cities array.
    '''
	
    return np.asarray([np.random.permutation(num_cities) for x in range(num_candidates)])
## End function population.candidates.pick_cands