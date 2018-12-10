def single_cand_adjacent_distance(distances, city_idx, true_distance=False):
    dist = []
    if true_distance:
        for i in range(city_idx.shape[0]):
            start_idx = city_idx[i]
            end_idx = city_idx[(i+1) % city_idx.shape[0]]
            d = distances[start_idx][end_idx] ** 0.5
            dist.append(d)
    else:
        for i in range(city_idx.shape[0]):
            start_idx = city_idx[i]
            end_idx = city_idx[(i+1) % city_idx.shape[0]]
            d = distances[start_idx][end_idx]
            dist.append(d)
    return np.array(dist)