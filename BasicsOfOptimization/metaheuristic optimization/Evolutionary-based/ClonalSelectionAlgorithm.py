import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Initialize population (colonies)
def initialize_population(pop_size, dimensions, bounds):
    population = np.random.uniform(bounds[0], bounds[1], (pop_size, dimensions))
    return population

# Fitness evaluation
def evaluate_population(population):
    fitness = np.array([sphere_function(individual) for individual in population])
    return fitness

# Selection: Tournament selection
def tournament_selection(population, fitness, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = np.random.choice(len(population), tournament_size, replace=False)
        winner = tournament[np.argmin(fitness[tournament])]
        selected.append(population[winner])
    return np.array(selected)

# Crossover: Blend crossover
def blend_crossover(parent1, parent2, alpha=0.5):
    return alpha * parent1 + (1 - alpha) * parent2

# Mutation: Add random noise
def mutate(individual, mutation_rate=0.01, bounds=(-5, 5)):
    mutation_vector = np.random.normal(0, mutation_rate, size=individual.shape)
    mutated_individual = individual + mutation_vector
    mutated_individual = np.clip(mutated_individual, bounds[0], bounds[1])  # Ensure bounds are respected
    return mutated_individual

# Colony Selection Algorithm (CSA)
def colony_selection_algorithm(pop_size=50, dimensions=5, bounds=(-5, 5), generations=100, mutation_rate=0.01):
    # Step 1: Initialize population
    population = initialize_population(pop_size, dimensions, bounds)
    best_solution = None
    best_fitness = float('inf')
    
    # Step 2: Evolve colonies over generations
    for generation in range(generations):
        # Step 3: Evaluate fitness of population
        fitness = evaluate_population(population)
        
        # Step 4: Keep track of the best solution
        min_fitness = np.min(fitness)
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_solution = population[np.argmin(fitness)]
        
        # Step 5: Selection (using tournament selection)
        selected_population = tournament_selection(population, fitness)
        
        # Step 6: Crossover (blend crossover)
        new_population = []
        for i in range(0, pop_size, 2):
            parent1, parent2 = selected_population[i], selected_population[i + 1]
            offspring1 = blend_crossover(parent1, parent2)
            offspring2 = blend_crossover(parent2, parent1)
            new_population.append(offspring1)
            new_population.append(offspring2)
        
        # Step 7: Mutation
        new_population = [mutate(individual, mutation_rate, bounds) for individual in new_population]
        population = np.array(new_population)
        
        print(f"Generation {generation + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run the CSA on the Sphere function
best_solution, best_fitness = colony_selection_algorithm()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

