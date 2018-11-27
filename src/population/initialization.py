import numpy as np
import os.path

from timing import timing

# Read city locations from a space-separated text file with format:
# city_index    latitude    longitudee
@timing
def init_file(populationFilePath: str) -> np.ndarray:
    
    if not os.path.isfile(populationFilePath):
        raise FileNotFoundError

    # Skip city_index since it is implied through array indexing.
    return np.loadtxt(populationFilePath, delimiter=' ', usecols=(1, 2))
   
