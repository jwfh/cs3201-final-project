#by Ting Hu for COMP3201 A2

import random

# mutate a permutation
def permutation_swap(ind: list) -> list: #ind is the individual as a 2d Array
	val = random.randint(0, len(ind)) #random mutation swap location

	mutant = ind.copy()
	mutation_points = random.sample(range(len(ind)), 2)
	mutant[mutation_points[val]] = ind[mutation_points[val+1]]
	mutant[mutation_points[val+1]] = ind[mutation_points[val]]

	return mutant
