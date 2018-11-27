import numpy as np
import random
#individual = [0,1,2,3,4,5,6]
def ScrambleMutation(individual):
        #please replace individual with the same parameters passed into
        print(individual)
        #print("-------------------------------")
        mutant = np.copy(individual)
        length = mutant.size
        ind1 = random.randint(0,length//2)
        ind2 = random.randint(length//2, length-1)

        while(ind1 == ind2):
                ind2 = random.randint(length//2, length-1)
        holder = mutant[ind1:ind2+1]
        np.random.shuffle(holder)
        mutant[ind1:ind2+1] = holder

        print(mutant)
#ScrambleMutation(individual)

