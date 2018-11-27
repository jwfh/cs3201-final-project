#!/usr/bin/env python3

## System imports
import numpy as np

from timing import timing

# Randomly select num_candidates permutations from [0, num_cities).
# Resulting values represent indices into original cities array.
@timing
def pick_cands(num_cities: int, num_candidates: int) -> list:
	
	return [np.random.permutation(num_cities) for x in range(num_candidates)]
