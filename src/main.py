import random
import math

#3201 project
#Main function
#Initialization functions: initialization(location), candidates(a,size)
#Fitness functions: distance(a), fitness(a)

def main():
    data = initialization("West.txt")
    pop_size = len(data) * 2
    candidates_list = candidates(data, pop_size)
    distances = []
    for i in range(len(candidates_list)):
        dis = distance(candidates_list[i])
        distances.append(dis)

    fitnesses = fitness(distances)
    

def candidates(a,size):
    pop = []
    
    for i in range(size):
        pop.append(random.sample(a, len(a)))

    return pop

def distance(a):

    dist = []

    for i in range(len(a)-1):
        x1 = float(a[i+1][0])
        x2 = float(a[i][0]) 
        y1 = float(a[i+1][1])
        y2 = float(a[i][1])
        b = ((x2 - x1)**2)
        c = ((y2 - y1)**2)
        dist.append(math.sqrt(b + c))
    
    x = (float(a[len(a)-1][0]) - float(a[0][0]))**2
    y = (float(a[len(a)-1][1]) - float(a[0][1]))**2
    dist.append(math.sqrt(x + y))

    return dist

def fitness(a):

    fit = []

    for i in range(len(a)):
        avg = 0
        summer = 0
        for j in range(len(a[i])):
            summer = summer + a[i][j]
        avg = summer/len(a[i])
        fit.append(avg)
    
    return fit


def initialization(location):
    
    f = open(location, "r")
    g = open("Refined_Location.txt", "w")
    f1 = f.readlines()
    i = 1
    a = []
    for x in f1:
        if x.strip():
            g.write("\t".join(x.split()[1:]) + "\n")
    f.close()
    g.close()
    g = open("Refined_Location.txt", "r")
    
    g1 = g.readlines()
    for y in g1:
        y.strip("'")
        y.strip(",")
        a.append(y.split(None))
    g.close()
    
    return a

main()
