import numpy as np
import matplotlib.pyplot as plt

# Objective function: minimize f(x) = x^2
def objective_function(x):
    return x**2

# Tabu Search algorithm
def tabu_search(objective_function, initial_x, max_iter, tabu_size, neighborhood_size):
    # Initialize the best solution and the tabu list
    current_x = initial_x
    best_x = current_x
    tabu_list = []
    history = [current_x]
    
    for _ in range(max_iter):
        # Generate neighborhood solutions
        neighbors = [current_x + np.random.uniform(-1, 1) for _ in range(neighborhood_size)]
        
        # Filter neighbors that are in the tabu list
        neighbors = [x for x in neighbors if x not in tabu_list]
        
        # If no valid neighbors are found, skip to the next iteration
        if len(neighbors) == 0:
            continue
        
        # Find the best neighbor
        best_neighbor = min(neighbors, key=objective_function)
        
        # Update the current solution and the best solution
        current_x = best_neighbor
        if objective_function(current_x) < objective_function(best_x):
            best_x = current_x
        
        # Update the tabu list
        tabu_list.append(current_x)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)  # Remove the oldest solution from the tabu list
        
        # Record history
        history.append(current_x)
    
    return best_x, history

# Parameters
initial_x = 10  # Starting point
max_iter = 100  # Maximum number of iterations
tabu_size = 5  # Maximum size of the tabu list
neighborhood_size = 20  # Number of neighbors to consider at each step

# Run Tabu Search
best_solution, history = tabu_search(objective_function, initial_x, max_iter, tabu_size, neighborhood_size)

# Plotting the progress
x_vals = np.linspace(-10, 10, 1000)
y_vals = objective_function(x_vals)
plt.plot(x_vals, y_vals, label="Objective function $f(x) = x^2$")
plt.scatter(history, [objective_function(x) for x in history], color="red", label="Tabu Search Path", s=10)
plt.title(f"Tabu Search Optimization\nBest Solution: x = {best_solution:.4f}, f(x) = {objective_function(best_solution):.4f}")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()

