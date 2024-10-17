import numpy as np
import matplotlib.pyplot as plt

# Objective function: minimize f(x) = x^2
def objective_function(x):
    return x**2

# Simulated Annealing algorithm
def simulated_annealing(objective_function, initial_x, initial_temperature, alpha, stopping_temp, max_iter):
    # Initialize the current solution, temperature, and history tracking
    current_x = initial_x
    current_temp = initial_temperature
    history = [current_x]
    
    for i in range(max_iter):
        # Generate a new candidate solution (small random perturbation)
        new_x = current_x + np.random.uniform(-1, 1)
        
        # Compute the change in objective function
        delta_f = objective_function(new_x) - objective_function(current_x)
        
        # Acceptance criteria: accept if new solution is better or with probability exp(-delta_f / T)
        if delta_f < 0 or np.random.uniform(0, 1) < np.exp(-delta_f / current_temp):
            current_x = new_x  # Accept the new solution

        # Cool down the temperature
        current_temp *= alpha

        # Store the current solution in history
        history.append(current_x)

        # Check if stopping temperature is reached
        if current_temp <= stopping_temp:
            break

    return current_x, history

# Parameters
initial_x = 10  # Starting point
initial_temperature = 100  # Initial temperature
alpha = 0.9  # Cooling rate
stopping_temp = 1e-5  # Minimum temperature to stop
max_iter = 1000  # Maximum number of iterations

# Run simulated annealing
best_solution, history = simulated_annealing(objective_function, initial_x, initial_temperature, alpha, stopping_temp, max_iter)

# Plotting the progress
x_vals = np.linspace(-10, 10, 1000)
y_vals = objective_function(x_vals)
plt.plot(x_vals, y_vals, label="Objective function $f(x) = x^2$")
plt.scatter(history, [objective_function(x) for x in history], color="red", label="SA Path", s=10)
plt.title(f"Simulated Annealing Optimization\nBest Solution: x = {best_solution:.4f}, f(x) = {objective_function(best_solution):.4f}")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()

