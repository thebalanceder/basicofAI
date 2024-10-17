import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Levy flight calculation
def levy_flight(Lambda):
    # Generate step size using Levy distribution
    sigma = (np.math.gamma(1 + Lambda) * np.sin(np.pi * Lambda / 2) / 
            (np.math.gamma((1 + Lambda) / 2) * Lambda * 2**((Lambda - 1) / 2))) ** (1 / Lambda)
    
    u = np.random.normal(0, sigma, size=1)
    v = np.random.normal(0, 1, size=1)
    step = u / abs(v) ** (1 / Lambda)
    return step

# Cuckoo Search parameters
num_nests = 25
dimensions = 5
bounds = (-10, 10)
max_iterations = 100
pa = 0.25  # Discovery rate of alien eggs (abandonment probability)
alpha = 0.01  # Step size scaling factor
Lambda = 1.5  # Levy flight parameter

# Initialize the nests (solutions)
def initialize_nests(num_nests, dimensions, bounds):
    return np.random.uniform(bounds[0], bounds[1], (num_nests, dimensions))

# Get a new solution using Levy flight
def get_new_solution(current_solution, alpha, Lambda):
    step_size = levy_flight(Lambda)
    return current_solution + alpha * step_size * np.random.randn(len(current_solution))

# Replace some nests (worst solutions) with new solutions
def replace_nests(nests, pa, bounds):
    num_replaced = int(pa * len(nests))
    for i in range(num_replaced):
        nests[i] = np.random.uniform(bounds[0], bounds[1], len(nests[i]))
    return nests

# Cuckoo Search Algorithm
def cuckoo_search():
    # Step 1: Initialize nests and fitness
    nests = initialize_nests(num_nests, dimensions, bounds)
    fitness = np.array([sphere_function(nest) for nest in nests])
    
    # Step 2: Start the optimization process
    for iteration in range(max_iterations):
        # Step 3: Generate new cuckoo solutions via Levy flight
        for i in range(num_nests):
            new_solution = get_new_solution(nests[i], alpha, Lambda)
            new_solution = np.clip(new_solution, bounds[0], bounds[1])
            new_fitness = sphere_function(new_solution)
            
            # If new solution is better, replace the current nest
            if new_fitness < fitness[i]:
                nests[i] = new_solution
                fitness[i] = new_fitness
        
        # Step 4: Perform host nest discovery and abandonment
        nests = replace_nests(nests, pa, bounds)
        fitness = np.array([sphere_function(nest) for nest in nests])
        
        # Step 5: Track the best solution found so far
        best_fitness_idx = np.argmin(fitness)
        best_solution = nests[best_fitness_idx]
        best_fitness = fitness[best_fitness_idx]
        
        print(f"Iteration {iteration + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run Cuckoo Search on the Sphere function
best_solution, best_fitness = cuckoo_search()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

