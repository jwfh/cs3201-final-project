#!/usr/bin/env python3

## System imports
import random

def pick_cands(a,size):
    pop = []
    
    for i in range(size):
        pop.append(random.sample(a, len(a)))

    return pop