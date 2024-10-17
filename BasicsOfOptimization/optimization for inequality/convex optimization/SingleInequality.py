import numpy as np
from scipy.optimize import minimize

# Define the objective function
# f(x1, x2) = 0.5 * (x1^2 + x2^2) + x1 + 2*x2
def objective(x):
    x1, x2 = x
    return 0.5 * (x1**2 + x2**2) + x1 + 2*x2+5

# Define the constraint: x1 + x2 <= 1
def constraint1(x):
    return 1 - (x[0] + x[1])  # This ensures that x1 + x2 <= 1

# Define bounds: x1 >= 0, x2 >= 0
bounds = [(0, None), (0, None)]  # (lower bound, upper bound) for x1 and x2

# Define the constraints in a format for scipy.optimize
constraints = {'type': 'ineq', 'fun': constraint1}

# Initial guess for x1 and x2
x0 = [0.5, 0.5]

# Solving the optimization problem
solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# Print the solution
print(f"Optimal solution: x1 = {solution.x[0]}, x2 = {solution.x[1]}")
print(f"Optimal objective value: {solution.fun}")

