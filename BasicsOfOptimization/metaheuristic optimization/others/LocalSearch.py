import numpy as np

# Objective function: Rosenbrock function
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Local Search parameters
max_iter = 1000  # Maximum number of iterations
step_size = 0.01  # Step size for exploring neighbors
tol = 1e-6  # Tolerance for stopping

# Neighborhood exploration
def explore_neighborhood(x, step_size):
    # Generate small perturbations around the current solution
    neighbors = []
    for i in range(len(x)):
        neighbor_up = np.copy(x)
        neighbor_down = np.copy(x)
        neighbor_up[i] += step_size
        neighbor_down[i] -= step_size
        neighbors.append(neighbor_up)
        neighbors.append(neighbor_down)
    return neighbors

# Local Search Algorithm
def local_search(x0):
    x_current = x0
    f_current = rosenbrock(x_current)
    
    for iteration in range(max_iter):
        # Explore the neighborhood
        neighbors = explore_neighborhood(x_current, step_size)
        
        # Evaluate the objective function for all neighbors
        f_best = f_current
        x_best = x_current
        for neighbor in neighbors:
            f_neighbor = rosenbrock(neighbor)
            if f_neighbor < f_best:
                f_best = f_neighbor
                x_best = neighbor
        
        # If the best neighbor improves the solution, move to it
        if f_best < f_current:
            x_current = x_best
            f_current = f_best
        else:
            # If no improvement, stop the search
            print(f"Terminating after {iteration + 1} iterations")
            break

        # Check for convergence
        if abs(f_best - f_current) < tol:
            print(f"Converged after {iteration + 1} iterations")
            break

    return x_current, f_current

# Initial solution
x0 = np.random.rand(2) * 4 - 2  # Random initial solution in range [-2, 2]

# Perform Local Search
best_solution, best_fitness = local_search(x0)

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness value: {best_fitness}")

