

def initialization(location):
    
    f = open(location, "r")
    
    file_str = f.readlines()
       
    a = []
 
    for line in file_str:
        a.append(line.strip(None).split()[1:])

    f.close()
    
    return a


    

def candidates(a,size):
    pop = []
    
    for i in range(size):
        pop.append(random.sample(a, len(a)))

    return pop