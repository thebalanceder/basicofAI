import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Initialize habitats (population)
def initialize_habitats(pop_size, dimensions, bounds):
    population = np.random.uniform(bounds[0], bounds[1], (pop_size, dimensions))
    return population

# Biogeography-Based Optimization (BBO)
def biogeography_based_optimization(pop_size=50, dimensions=5, bounds=(-5, 5), generations=100, I_max=1.0, E_max=1.0, mutation_rate=0.05):
    # Step 1: Initialize population (habitats)
    population = initialize_habitats(pop_size, dimensions, bounds)
    fitness = np.array([sphere_function(ind) for ind in population])
    
    # Step 2: Start the BBO evolutionary process
    for generation in range(generations):
        # Step 3: Calculate HSI (fitness) for each habitat
        HSI = fitness
        max_HSI = np.max(HSI)
        min_HSI = np.min(HSI)
        
        # Normalize HSI to calculate immigration and emigration rates
        normalized_HSI = (HSI - min_HSI) / (max_HSI - min_HSI + 1e-8)
        emigration_rate = E_max * normalized_HSI
        immigration_rate = I_max * (1 - normalized_HSI)
        
        # Step 4: Migration: share information between habitats
        new_population = np.copy(population)
        for i in range(pop_size):
            for j in range(dimensions):
                if np.random.rand() < immigration_rate[i]:
                    # Select a random emigrating habitat
                    selected_habitat = np.random.choice(range(pop_size), p=emigration_rate/np.sum(emigration_rate))
                    new_population[i, j] = population[selected_habitat, j]
        
        # Step 5: Mutation: randomly modify some habitats
        for i in range(pop_size):
            if np.random.rand() < mutation_rate:
                new_population[i] = np.random.uniform(bounds[0], bounds[1], dimensions)
        
        # Step 6: Update population and fitness
        population = new_population
        fitness = np.array([sphere_function(ind) for ind in population])
        
        # Track the best solution found so far
        best_fitness_idx = np.argmin(fitness)
        best_solution = population[best_fitness_idx]
        best_fitness = fitness[best_fitness_idx]
        
        print(f"Generation {generation + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run the BBO on the Sphere function
best_solution, best_fitness = biogeography_based_optimization()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

