import numpy as np

# Objective function: Rastrigin function (minimization)
def objective_function(x):
    return 10 * len(x) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])
    #return 2*x**2

# ABC Parameters
num_bees = 30          # Number of bees (population)
max_iterations = 1000  # Maximum number of iterations
limit = 50             # Limit for abandoning a food source
dim = 2                # Problem dimension (e.g., Rastrigin function in 2D)
lower_bound = -5.12    # Lower bound of the search space
upper_bound = 5.12     # Upper bound of the search space

# Initialize the bee colony
solutions = np.random.uniform(lower_bound, upper_bound, (num_bees, dim))
fitness = np.array([objective_function(sol) for sol in solutions])
trials = np.zeros(num_bees)  # Counter for abandonment
a=trials

# ABC Algorithm
for iteration in range(max_iterations):
    # Employed bees phase
    for i in range(num_bees):
        k = np.random.randint(0, num_bees)
        while k == i:
            k = np.random.randint(0, num_bees)
        phi = np.random.uniform(-1, 1, dim)
        new_solution = solutions[i] + phi * (solutions[i] - solutions[k])
        new_solution = np.clip(new_solution, lower_bound, upper_bound)
        new_fitness = objective_function(new_solution)
        
        # Greedy selection
        if new_fitness < fitness[i]:
            solutions[i] = new_solution
            fitness[i] = new_fitness
            trials[i] = 0
        else:
            trials[i] += 1

    # Onlooker bees phase
    fitness_sum = np.sum(1.0 / (1.0 + fitness))
    for i in range(num_bees):
        if np.random.uniform() < (1.0 / (1.0 + fitness[i])) / fitness_sum:
            k = np.random.randint(0, num_bees)
            while k == i:
                k = np.random.randint(0, num_bees)
            phi = np.random.uniform(-1, 1, dim)
            new_solution = solutions[i] + phi * (solutions[i] - solutions[k])
            new_solution = np.clip(new_solution, lower_bound, upper_bound)
            new_fitness = objective_function(new_solution)
            
            # Greedy selection
            if new_fitness < fitness[i]:
                solutions[i] = new_solution
                fitness[i] = new_fitness
                trials[i] = 0
            else:
                trials[i] += 1

    # Scout bees phase
    for i in range(num_bees):
        if trials[i] > limit:
            solutions[i] = np.random.uniform(lower_bound, upper_bound, dim)
            fitness[i] = objective_function(solutions[i])
            trials[i] = 0
    
    # Best solution found
    best_index = np.argmin(fitness)
    best_solution = solutions[best_index]
    print(f"Iteration {iteration}: Best Solution = {best_solution}, Best Fitness = {fitness[best_index]}")

# Final solution
print(f"Optimal solution: {best_solution} with fitness {fitness[best_index]}")
print(a)

