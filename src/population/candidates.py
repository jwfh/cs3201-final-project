#!/usr/bin/env python3

## System imports
import numpy as np

# Randomly select num_cities_to_pick cities from [0, num_cities).
# Resulting values represent indices into original cities array.
def pick_cands(num_cities: int, num_cities_to_pick: int) -> np.ndarray:
	
	return np.random.randint(0, high=num_cities, size=num_cities_to_pick)
