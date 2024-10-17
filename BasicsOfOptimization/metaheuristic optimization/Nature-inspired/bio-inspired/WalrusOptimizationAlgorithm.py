import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Walrus Optimization parameters
num_walruses = 30
dimensions = 5
bounds = (-10, 10)
max_iterations = 100
alpha = 0.5  # Exploration step size factor
beta = 0.8  # Exploitation attraction factor
gamma = 0.1  # Randomness factor

# Initialize the walruses (solutions)
def initialize_walruses(num_walruses, dimensions, bounds):
    return np.random.uniform(bounds[0], bounds[1], (num_walruses, dimensions))

# Exploration phase: Random exploration
def exploration_phase(position, alpha, dimensions):
    random_factor = np.random.rand(dimensions) - 0.5
    new_position = position + alpha * random_factor
    return new_position

# Exploitation phase: Move towards the best solution
def exploitation_phase(position, best_position, beta, gamma, dimensions):
    random_factor = np.random.rand(dimensions) - 0.5
    new_position = position + beta * (best_position - position) + gamma * random_factor
    return new_position

# Walrus Optimization Algorithm
def walrus_optimization():
    # Step 1: Initialize walruses and fitness
    walruses = initialize_walruses(num_walruses, dimensions, bounds)
    fitness = np.array([sphere_function(walrus) for walrus in walruses])
    best_solution = walruses[np.argmin(fitness)]
    best_fitness = np.min(fitness)
    
    # Step 2: Start the optimization process
    for iteration in range(max_iterations):
        for i in range(num_walruses):
            current_walrus = walruses[i]
            current_fitness = fitness[i]
            
            # Exploration phase
            if np.random.rand() < 0.5:  # 50% chance for exploration
                new_position = exploration_phase(current_walrus, alpha, dimensions)
                new_position = np.clip(new_position, bounds[0], bounds[1])
                new_fitness = sphere_function(new_position)
                
                if new_fitness < current_fitness:
                    walruses[i] = new_position
                    fitness[i] = new_fitness
            
            # Exploitation phase
            else:  # 50% chance for exploitation
                new_position = exploitation_phase(current_walrus, best_solution, beta, gamma, dimensions)
                new_position = np.clip(new_position, bounds[0], bounds[1])
                new_fitness = sphere_function(new_position)
                
                if new_fitness < current_fitness:
                    walruses[i] = new_position
                    fitness[i] = new_fitness
        
        # Update the best solution
        best_solution_idx = np.argmin(fitness)
        if fitness[best_solution_idx] < best_fitness:
            best_fitness = fitness[best_solution_idx]
            best_solution = walruses[best_solution_idx]
        
        print(f"Iteration {iteration + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run WOA on the Sphere function
best_solution, best_fitness = walrus_optimization()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

