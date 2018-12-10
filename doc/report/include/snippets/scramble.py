def scramble_individual(individual, mutation_factor=0.25):
    mutant = individual
    n = mutant.shape[0]
    mutation_thresold = mutation_factor * n

    start_idx = end_idx = 0
    while end_idx-start_idx < mutation_thresold:
        start_idx = np.random.randint(0, n - 3)
        end_idx = np.random.randint(start_idx+2, n-1)
    np.random.shuffle(mutant[start_idx:end_idx])
    return mutant