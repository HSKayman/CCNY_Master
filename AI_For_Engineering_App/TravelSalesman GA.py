import numpy as np
import random

def route_distance(cities):
    total_distance = 0
    for i in range(len(cities)):
        j = (i + 1) % len(cities)
        city_a, city_b = cities[i], cities[j]
        distance = np.sqrt((city_a[0] - city_b[0])**2 + (city_a[1] - city_b[1])**2)
        total_distance += distance
    return total_distance

def initial_population(cities, population_size):
    return [random.sample(cities, len(cities)) for _ in range(population_size)]

def selection(population, fitness, selection_size):
    selected_indices = np.argsort(fitness)[:selection_size]
    return [population[index] for index in selected_indices]

def crossover(parent1, parent2):
    cut_points = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[cut_points[0]:cut_points[1]] = parent1[cut_points[0]:cut_points[1]]
    child = [city for city in parent2 if city not in child] + child
    child = [city for city in child if city is not None]
    return child

def mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(cities, population_size=100, generations=500, selection_size=20, mutation_rate=0.01):
    population = initial_population(cities, population_size)
    
    for _ in range(generations):
        fitness = [1 / route_distance(route) for route in population]
        population = selection(population, fitness, selection_size)
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            offspring.append(child)
        population = offspring
    
    best_route = population[np.argmax([1 / route_distance(route) for route in population])]
    return best_route, route_distance(best_route)

cities = [(0, 0), (10, 0), (0, 10), (10, 10), (5, 5)]  # Example cities as (x, y) coordinates
best_route, distance = genetic_algorithm(cities)
print("Best route:", best_route)
print("Distance:", distance)
