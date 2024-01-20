import numpy as np
import random

def swap_mutate(chromosome,mutate_percent):
    ## flip coin to see if chromosome gets mutated
    if random.uniform(0,1) < mutate_percent:
        ## select 2 random genes of the chromosome
        gene1 = random.randint(0, len(chromosome)-1)
        gene2 = random.randint(0, len(chromosome)-1)
        while gene2 == gene1:
            gene2 == random.randint(0, len(chromosome)-1)
        ## swap the selected genes
        chromosome[gene1],chromosome[gene2]=chromosome[gene2],chromosome[gene1]

    return chromosome

def ordered_crossover(parent1,parent2):
	## ordered_crossover() takes in two parent chromosomes as input
	## and returns a child chromosome
	##
	## ordered_crossover() takes a random subarray from the first parent and
	## copies that subarray over to the child (note: the subarray can
	## wrap across the ends of the array)
	## the remaining genes of the child are filled in the order that
	## they appear in the second parent

	## set n to the chromosome length
	n = len(parent1)
	## initialize child with an array of zeros
	child = np.zeros(n, dtype=int)

	## select a random subarray of parent1 by first randomly selecting 
	## the start and end points of the subarray
	start_point = random.randint(0,n-1)
	## restrict the length of the subarray to between 1 and n - 2
	end_point = (start_point + random.randint(0,n-1 - 2)) % n

	print("start_point = ",start_point)
	print("end_point = ",end_point)

	## copy the subarray from parent1 into the child
	if start_point <= end_point:
	    child[start_point:end_point+1] = parent1[start_point:end_point+1]
	else:
	    ## if start_point is greater than end_point, the subarray 
	    ## wraps around the ends of the array
	    child[start_point:] = parent1[start_point:]
	    child[:end_point+1] = parent1[:end_point+1]
	## fill the remaining genes of the child in the order they appear
	## in parent2
	pointer = 0
	for i in range(n):
	    if parent2[i] not in child:
	        while child[pointer] != 0:
	            pointer += 1
	        child[pointer] = parent2[i]
	return child
def generate_permutation(n):
    ## create a random permutation of the sequence from 1 to n

    ## initialize the permutation with an array of zeros
    permutation = np.zeros(n, dtype=int)
    for i in range(n):
    	## randomly select an integer between 1 and n
        choice = random.randint(1,n)
        ## check if the chosen integer has already been 
        ## added to the permutation.
        ## if it has, keep choosing numbers until a new one
        ## is chosen
        while choice in permutation:
            choice = random.randint(1,n)
        ## add the new number to the permutation
        permutation[i] = choice    
    return permutation

if __name__ == "__main__":
    A = generate_permutation(6)
    B = generate_permutation(6)   
    print("A = ",A)
    print("B = ",B)

    child = ordered_crossover(A, B)
    print("child = ",child)
    
    swap_mutate(child, 1)
    print("mutated = ",child)