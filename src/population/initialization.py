import numpy as np
import os.path

from timing import timing

## Begin function population.initialization.init_file
@timing
def init_file(populationFilePath: str) -> np.ndarray:
    '''
    Read city locations from a space-separated text file with format:
    city_index    latitude    longitude
    '''
    
    if not os.path.isfile(populationFilePath):
        raise FileNotFoundError

    # Skip city_index since it is implied through array indexing.
    return np.loadtxt(populationFilePath, delimiter=' ', usecols=(1, 2))
## End function population.initialization.init_file