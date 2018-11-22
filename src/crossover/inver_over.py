import numpy as np

def inver_over(parent: list, selected_city: int) -> list:
	selected_city_idx = np.where(parent == selected_city)

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