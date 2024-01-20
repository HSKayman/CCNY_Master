## DEPENDENCIES: deap, basemap, and basemap-data-hiresfrom deap
import random
from deap import creator, base, tools, algorithms
import gps
import pandas as pd
import tsp_functions as tf

# Beyonce's video blogger Charlene plans to travel throughout the Carribean.
# She wants to plan out the best way to visit each Caribbean county? 
# Beyonce hired you as an AI engineer to provide Charlene with the shortest route.
# Please help Charlene and make Beyonce happy so that you can get back-stage passes
# for her Carribean concert.
cities_file = 'Carribean_countries.csv'

## load city data into a dataframe df
df = pd.read_csv(cities_file)
## generate a weight matrix where the weights are the distances between cities
distance_matrix = gps.generate_distance_matrix(df)

## set chromosome length to the number of cities
CHROM_LENGTH = len(distance_matrix)

## create a variable called FitnessMin with the create() function.
## FitnessMin inherits from base.Fitness and it will store whether
## the fitness should be minimized or maximized:
##      if weights == -1.0, then minimize the fitness
##      if weights == 1.0, then maximize the fitness

creator.create("FitnessMin",base.Fitness,weights=(-1.0,))
## create a variable called Individual that will determine the 
## datastructure used for the chromosome.
## Individual inherits from list and it will store integers.
creator.create("Individual", list,typecode='i',fitness=creator.FitnessMin)
 
## initialize a new toolbox variable to configure GA parameters:
toolbox = base.Toolbox()
 

## configure the population of the GA so that each chromosome is initialized
## as a random permutation of the sequence from 0 to CHROM_LENGTH-1
## range(CHROM_LENGTH): creates a list from 0 to CHROM_LENGTH-1
## range: [0,1,...,9] indices is a random permutation of range
toolbox.register("indices",random.sample,range(CHROM_LENGTH), CHROM_LENGTH)

## assign contents of indices as genes in genome
toolbox.register("genome",tools.initIterate,creator.Individual,toolbox.indices)

## repeat chromosome assignment for each chromosome in the population
toolbox.register("population",tools.initRepeat,list,toolbox.genome)

## define the fitness function 
def TSP_fit_func(chromosome):
    ## sum up the total distance of the path stored in chromosome
    ## initialize distance from last element to the first element
    distance=distance_matrix[chromosome[-1]][chromosome[0]]
    ## sum all distances from i to i+1 for all i
    for i in range(len(chromosome)-1):
        distance+=distance_matrix[chromosome[i]][chromosome[i+1]]

    ## return the path's distance as the fitness 
    ## (at least one comma is needed in return in deap - stupid rule)
    return distance,

## configure the evaluate parameter by passing the fitness function
toolbox.register("evaluate",TSP_fit_func)

## implementation of crossover oeprator:
## set the reproduction function to partially matched crossover which
## produces children that are also permutations
toolbox.register("mate",tools.cxPartialyMatched)
## set a 5 percent of mutation, which causes genes in the chromosome to
## be randomly swapped and the result of the mutation is also a permutation
toolbox.register("mutate", tools.mutShuffleIndexes,indpb=0.05)
## set the selection function to tournment selection, which will pick three
## chromosomes at random and select the one with the best fitness
toolbox.register("select",tools.selTournament,tournsize=3)

## set population size to n=100 (n=20 or n=10 see the impact of n)
pop=toolbox.population(n=10)
## have variable best_genome store the chromosome with the best fitness
best_genome= tools.HallOfFame(1)

## run GA to get the solution
#algorithms.eaSimple(pop, toolbox, xo prob, mut prob, gens, store best)
algorithms.eaSimple(pop,toolbox,0.7,0.2,10,halloffame=best_genome)
## store the solution into best_path
best_path = best_genome[0]
## print best_path
print('\nBEST PATH:\n')
for i in range(len(best_path)):
    print(df['Country'][best_path[i]])
print(df['Country'][best_path[0]])
cost = 0
print('\nBEST PATH COST:\n')
for i in range(len(best_path)-1):
    tempo = distance_matrix[best_path[i]][best_path[i+1]]
    cost+= tempo
    print(df['Country'][best_path[i]], tempo)
print(df['Country'][best_path[0]],distance_matrix[len(best_path)-1][best_path[0]])
cost += distance_matrix[len(best_path)-1][best_path[0]]
print("TOTAL COST: ",cost)
