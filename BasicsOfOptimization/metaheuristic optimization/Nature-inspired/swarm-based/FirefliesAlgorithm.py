import numpy as np

# Objective function: Rosenbrock function
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2 + 1000*(x[1]**2-x[2]**3)**2

# Firefly Algorithm parameters
alpha = 0.2  # Randomization parameter
beta_0 = 1.0  # Attractiveness at r=0
gamma = 1.0  # Light absorption coefficient
num_fireflies = 15  # Number of fireflies
max_iter = 100  # Maximum number of iterations
dim = 3  # Dimensionality of the problem (2D in this case)

# Initialize fireflies at random positions
fireflies = np.random.rand(num_fireflies, dim) * 10 - 5  # Random values in the range [-5, 5]
fitness = np.zeros(num_fireflies)

# Function to calculate Euclidean distance
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2)**2))

# Main loop of the Firefly Algorithm
for t in range(max_iter):
    # Calculate the fitness of each firefly
    for i in range(num_fireflies):
        fitness[i] = rosenbrock(fireflies[i])

    # Move fireflies towards brighter ones
    for i in range(num_fireflies):
        for j in range(num_fireflies):
            if fitness[j] < fitness[i]:  # Move firefly i towards firefly j
                r = euclidean_distance(fireflies[i], fireflies[j])
                beta = beta_0 * np.exp(-gamma * r**2)
                fireflies[i] += beta * (fireflies[j] - fireflies[i]) + alpha * (np.random.rand(dim) - 0.5)
    
    # Output the best solution at each iteration
    best_firefly = np.argmin(fitness)
    print(f"Iteration {t+1}, Best solution: {fireflies[best_firefly]}, Best fitness: {fitness[best_firefly]}")

# Final best solution
best_firefly = np.argmin(fitness)
print(f"Final best solution: {fireflies[best_firefly]}")
print(f"Final best fitness: {fitness[best_firefly]}")

