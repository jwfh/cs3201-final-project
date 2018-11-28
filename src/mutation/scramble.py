#!/usr/bin/env python3

## System imports 
import numpy as np

## Begin function mutation.scramble.scramble_swap
def scramble_swap(individual: np.ndarray, mutation_factor: float=0.25) -> np.ndarray:
    '''
    Selects start and end indices in (0, i) where i is the length of the individual and the 
    length of [start, end) is no less than the mutation factor multiplied by the length 
    of the individual. As this number is the greatest lower bound of the set of possible
    mutation lengths, it is probable for the mutation to effect more elements than this.

    For example, if mutation_factor := 0.4 and the individual is of length 100, then the 
    mutation should affect no \em LESS than 40 consecutive elements in the NumPy array, however
    it may affect more.

    This is to prevent near-negligible mutations when the mutation trigger is activated.
    Conversely, these sort of mutations could be allowed and the mutation trigger made much
    more sensitive.

    @param individual The NumPy array containing city indices for a particular individual 
                      we wish to mutate.
    @param mutation_factor A real number representing the proportion of the individual 
                           that must be mutated.

    @return The mutated individual.
    '''

    mutant = np.copy(individual)
    length = mutant.shape[0]
    mutation_thresold = mutation_factor * length
    
    start_idx = end_idx = 0
    while end_idx-start_idx < mutation_thresold:
        start_idx = random.randint(0, length // 2)
        end_idx = random.randint(start_idx + 2, length - 1)
    
    np.random.shuffle(mutant[start_idx:end_idx])

    return mutant
## End function mutation.scramble.scramble_swap

