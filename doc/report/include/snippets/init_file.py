def init_file(populationFilePath):
    if not os.path.isfile(populationFilePath):
        raise FileNotFoundError
    return np.loadtxt(
        populationFilePath, 
        delimiter=' ', 
        usecols=(1, 2))