#!/usr/bin/env python3

## System imports
import numpy as np
import fitness

## Local imports
from timing import timing

## Begin function crossover.inver_over.inver_over
def inver_over1(parent: list, selected_city: int) -> list:
	selected_city_idx = np.where(parent == selected_city)
	print(parent, selected_city, selected_city_idx)

	c_prime = None
	while True:
		# Select a random city to the right of selected_city
		c_prime = np.random.choice(parent[selected_city_idx:-1], size=1)
		if c_prime != selected_city:
			break
	
	c_prime_idx = np.where(parent == c_prime)

	# Reverse values in between above indices
	parent[selected_city_idx:c_prime_idx] = parent[selected_city_idx:c_prime_idx][::-1]

	return parent
## End function crossover.inver_over.inver_over
#@timing
def inver_over(parent_pool: list, initial_parent_idx: int, distances: np.ndarray, initial_parent_fitness: int) -> list:
	child = parent_pool[initial_parent_idx]
	not_used_cities = np.arange(0, child.shape[0])

	# c is the selected city
	c_idx = np.random.choice(not_used_cities)
	c = child[c_idx]
	not_used_cities = np.delete(not_used_cities, c_idx)

	p = 0.5
	while not_used_cities.shape[0] > 0:
		if np.random.random() < p:
			c_prime_idx = np.random.choice(not_used_cities)
			c_prime = child[c_prime_idx % child.shape[0]]
		else:
			new_parent = parent_pool[np.random.randint(parent_pool.shape[0])]
			new_parent_c_idx = np.where(new_parent == c)[0][0]
			c_prime_idx = new_parent_c_idx + 1
			c_prime = child[c_prime_idx % child.shape[0]]
		not_used_cities = np.delete(not_used_cities, np.where(not_used_cities == c_prime_idx))
		if child[(c_idx + 1) % child.shape[0]] == c_prime or child[(c_idx - 1) % child.shape[0]] == c_prime:
			break
		# invert child[c_idx+1:c_prime_idx]
		child[c_idx+1:c_prime_idx] = child[c_idx+1:c_prime_idx][::-1]
		c_idx = c_prime_idx
		c = c_prime
	child_fitness = fitness.fitness.individual_fitness(fitness.distance.single_cand_adjacent_distance(distances, child))
	if child_fitness >= initial_parent_fitness:
		return child
	else:
		return parent_pool[initial_parent_idx]
