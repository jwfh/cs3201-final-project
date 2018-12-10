class Distances:
    def __init__(self, cities):
        self._cities = cities
        self._weights = np.zeros(
            (self._cities.shape[0], 
            self._cities.shape[0]))

    def _add_edge(self, start_idx, end_idx, start_end_dist=None):
        if start_end_dist == None:
            start_end_dist =  self._distance(
                self._cities[start_idx], 
                self._cities[end_idx])
        self._weights[start_idx][end_idx] = start_end_dist
        self._weights[end_idx][start_idx] = start_end_dist

    def _add_edge_map_helper(self, start_idx, end_idx):
        return start_idx, end_idx, self._distance(
            self._cities[start_idx], 
            self._cities[end_idx])

    def _distance(self, start_city, end_city):
        x1, y1 = start_city[0], start_city[1]
        x2, y2 = end_city[0], end_city[1]
        square_city_distance = (x2-x1)**2 + (y2-y1)**2
        assert square_city_distance >= 1, "The distance between two cities should be more than 1."
        return square_city_distance
    
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

   