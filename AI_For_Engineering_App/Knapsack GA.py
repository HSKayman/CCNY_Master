import numpy as np
import random

items = [(10, 5), (6, 4), (7, 3), (8, 2)]

max_weight = 10

population_size = 50
mutation_rate = 0.1
generations = 100

def initial_population(size):
    return [np.random.randint(2, size=len(items)) for _ in range(size)]

def fitness(solution):
    total_value = np.dot(solution, [item[0] for item in items])
    total_weight = np.dot(solution, [item[1] for item in items])
    if total_weight > max_weight:
        return 0  
    return total_value

def select(population, fitnesses, num_parents):
    parents = np.random.choice(population, size=num_parents, replace=False, p=fitnesses/np.sum(fitnesses))
    return parents

def crossover(parent1, parent2):
    crossover_point = np.random.randint(len(parent1))
    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    return child

def mutate(solution):
    if np.random.rand() < mutation_rate:
        mutation_point = np.random.randint(len(solution))
        solution[mutation_point] = 1 - solution[mutation_point]
    return solution

def genetic_algorithm():
    population = initial_population(population_size)
    
    for generation in range(generations):
        fitnesses = np.array([fitness(solution) for solution in population])
        
        selected_parents = select(population, fitnesses, population_size // 2)
        
        next_generation = []
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(list(selected_parents), 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)
        
        population = next_generation
    
    best_solution_index = np.argmax([fitness(solution) for solution in population])
    best_solution = population[best_solution_index]
    return best_solution, fitness(best_solution)

best_solution, best_solution_fitness = genetic_algorithm()
print("Best Solution:", best_solution)
print("Best Solution Fitness (Total Value):", best_solution_fitness)
