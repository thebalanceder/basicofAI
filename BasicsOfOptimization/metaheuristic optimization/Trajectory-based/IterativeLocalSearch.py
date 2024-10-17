import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Local Search: Simple Hill Climbing
def local_search(x, step_size=0.05, max_iters=100):
    for _ in range(max_iters):
        new_x = x + np.random.uniform(-step_size, step_size, len(x))  # Small random step
        new_x = np.clip(new_x, BOUNDS[0], BOUNDS[1])  # Keep within bounds
        
        if rastrigin_function(new_x) < rastrigin_function(x):  # Only accept improvement
            x = new_x
    return x

# Perturbation: Slightly alter the current solution
def perturbation(x, perturb_factor=0.5):
    return x + np.random.uniform(-perturb_factor, perturb_factor, len(x))

# Iterative Local Search
def iterative_local_search(max_iters=1000):
    # Step 1: Generate an initial random solution
    x_current = np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)
    x_current = local_search(x_current)  # Apply local search
    
    best_solution = x_current
    best_fitness = rastrigin_function(x_current)
    
    for iteration in range(max_iters):
        # Step 2: Perturb the solution
        x_perturb = perturbation(x_current)
        x_perturb = local_search(x_perturb)  # Apply local search again to the perturbed solution
        
        # Step 3: Acceptance criteria (accept if the new solution is better)
        if rastrigin_function(x_perturb) < best_fitness:
            best_solution = x_perturb
            best_fitness = rastrigin_function(x_perturb)
        
        # Optionally: Add a diversification step (random restart) if stuck in local minima
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")
    
    return best_solution, best_fitness

# Constants for the optimization problem
GENOME_LENGTH = 2  # Dimensionality of the problem
BOUNDS = [-5.12, 5.12]  # Search space bounds
MAX_ITERS = 1000

# Run the Iterative Local Search
best_solution, best_fitness = iterative_local_search(MAX_ITERS)
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

