import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# GSO Parameters
num_individuals = 20
dimensions = 5
bounds = (-10, 10)
max_iterations = 100
step_size = 0.1
scrounger_factor = 0.5
ranger_factor = 0.5

# Initialize the individuals (group)
def initialize_group(num_individuals, dimensions, bounds):
    return np.random.uniform(bounds[0], bounds[1], (num_individuals, dimensions))

# Producer behavior: Search in random directions
def producer_behavior(position, step_size, dimensions):
    random_direction = np.random.randn(dimensions)
    new_position = position + step_size * random_direction
    return new_position

# Scrounger behavior: Move towards the best solution
def scrounger_behavior(best_position, dimensions, scrounger_factor):
    random_factor = np.random.rand(dimensions) - 0.5
    new_position = best_position + scrounger_factor * random_factor
    return new_position

# Ranger behavior: Explore new random regions
def ranger_behavior(position, dimensions, ranger_factor):
    random_factor = np.random.rand(dimensions) - 0.5
    new_position = position + ranger_factor * random_factor
    return new_position

# Group Search Optimization Algorithm
def group_search_optimization():
    # Step 1: Initialize group and fitness
    group = initialize_group(num_individuals, dimensions, bounds)
    fitness = np.array([sphere_function(individual) for individual in group])
    best_solution = group[np.argmin(fitness)]
    best_fitness = np.min(fitness)
    
    # Step 2: Start the optimization process
    for iteration in range(max_iterations):
        for i in range(num_individuals):
            current_individual = group[i]
            current_fitness = fitness[i]
            
            # Producer behavior: Search in random directions
            if np.random.rand() < 0.5:  # 50% chance for producer behavior
                new_position = producer_behavior(current_individual, step_size, dimensions)
                new_position = np.clip(new_position, bounds[0], bounds[1])
                new_fitness = sphere_function(new_position)
                
                # If the new position is better, update the individual's position
                if new_fitness < current_fitness:
                    group[i] = new_position
                    fitness[i] = new_fitness
            
            # Scrounger behavior: Move towards the best solution
            elif np.random.rand() < 0.3:  # 30% chance for scrounger behavior
                new_position = scrounger_behavior(best_solution, dimensions, scrounger_factor)
                new_position = np.clip(new_position, bounds[0], bounds[1])
                new_fitness = sphere_function(new_position)
                
                if new_fitness < current_fitness:
                    group[i] = new_position
                    fitness[i] = new_fitness
            
            # Ranger behavior: Random exploration
            else:  # 20% chance for ranger behavior
                new_position = ranger_behavior(current_individual, dimensions, ranger_factor)
                new_position = np.clip(new_position, bounds[0], bounds[1])
                new_fitness = sphere_function(new_position)
                
                if new_fitness < current_fitness:
                    group[i] = new_position
                    fitness[i] = new_fitness
        
        # Update the best solution
        best_solution_idx = np.argmin(fitness)
        if fitness[best_solution_idx] < best_fitness:
            best_fitness = fitness[best_solution_idx]
            best_solution = group[best_solution_idx]
        
        print(f"Iteration {iteration + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run GSO on the Sphere function
best_solution, best_fitness = group_search_optimization()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

