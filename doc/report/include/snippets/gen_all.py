def gen_all(self):
    city_pairs = (
        (start_idx, end_idx)
        for start_idx in range(self._cities.shape[0])
        for end_idx in range(
            start_idx + 1, 
            self._cities.shape[0]))
    with mp.Pool() as pool:
        [self._add_edge(*data_point) 
            for data_point in pool.starmap(
                self._add_edge_map_helper, 
                city_pairs)]