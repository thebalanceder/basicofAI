import numpy as np

# Objective function: Rosenbrock function
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Local search: Simple greedy local search
def local_search(x, step_size):
    current = np.copy(x)
    f_current = rosenbrock(current)
    improved = True
    
    while improved:
        improved = False
        # Explore neighborhood
        for i in range(len(x)):
            # Try step in positive and negative direction
            for delta in [-step_size, step_size]:
                neighbor = np.copy(current)
                neighbor[i] += delta
                f_neighbor = rosenbrock(neighbor)
                if f_neighbor < f_current:
                    current = neighbor
                    f_current = f_neighbor
                    improved = True
                    break  # Move to the better neighbor
    
    return current, f_current

# Shaking: Perturbation in the k-th neighborhood
def shaking(x, k, max_step_size):
    perturbed = np.copy(x)
    for i in range(len(x)):
        perturbation = np.random.uniform(-k * max_step_size, k * max_step_size)
        perturbed[i] += perturbation
    return perturbed

# Variable Neighborhood Search Algorithm
def variable_neighborhood_search(x0, max_iter=1000, k_max=3, max_step_size=0.5, step_size=0.01):
    x_current = np.copy(x0)
    f_current = rosenbrock(x_current)
    
    for iteration in range(max_iter):
        k = 1
        while k <= k_max:
            # Step 1: Shaking
            x_shaken = shaking(x_current, k, max_step_size)
            
            # Step 2: Local Search
            x_local, f_local = local_search(x_shaken, step_size)
            
            # Step 3: Move or Increase Neighborhood
            if f_local < f_current:
                x_current = x_local
                f_current = f_local
                k = 1  # Reset to the first neighborhood
            else:
                k += 1  # Move to the next neighborhood
            
        print(f"Iteration {iteration+1}, Best solution: {x_current}, Best fitness: {f_current}")
    
    return x_current, f_current

# Initial solution
x0 = np.random.rand(2) * 4 - 2  # Random initial solution in range [-2, 2]

# Perform Variable Neighborhood Search
best_solution, best_fitness = variable_neighborhood_search(x0)

# Output the final result
print(f"Final best solution: {best_solution}")
print(f"Final best fitness: {best_fitness}")

