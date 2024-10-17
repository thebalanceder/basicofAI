import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Monkey Algorithm parameters
num_monkeys = 10
dimensions = 5
bounds = (-10, 10)
max_iterations = 100
climbing_step = 0.1
jumping_step = 0.5
sliding_step = 0.05

# Initialize monkeys (population)
def initialize_monkeys(num_monkeys, dimensions, bounds):
    return np.random.uniform(bounds[0], bounds[1], (num_monkeys, dimensions))

# Monkey Algorithm
def monkey_algorithm():
    # Step 1: Initialize the population of monkeys
    monkeys = initialize_monkeys(num_monkeys, dimensions, bounds)
    fitness = np.array([sphere_function(monkey) for monkey in monkeys])
    
    # Step 2: Start the optimization process
    for iteration in range(max_iterations):
        # Step 3: Perform climbing, jumping, and sliding for each monkey
        for i in range(num_monkeys):
            current_monkey = monkeys[i]
            current_fitness = fitness[i]
            
            # Climbing step (local search)
            new_monkey_climb = current_monkey + climbing_step * (np.random.rand(dimensions) - 0.5)
            new_monkey_climb = np.clip(new_monkey_climb, bounds[0], bounds[1])
            new_fitness_climb = sphere_function(new_monkey_climb)
            
            # If climbing improves fitness, update monkey's position
            if new_fitness_climb < current_fitness:
                monkeys[i] = new_monkey_climb
                fitness[i] = new_fitness_climb
                current_monkey = new_monkey_climb
                current_fitness = new_fitness_climb
            
            # Jumping step (exploration)
            new_monkey_jump = current_monkey + jumping_step * (np.random.rand(dimensions) - 0.5)
            new_monkey_jump = np.clip(new_monkey_jump, bounds[0], bounds[1])
            new_fitness_jump = sphere_function(new_monkey_jump)
            
            # If jumping improves fitness, update monkey's position
            if new_fitness_jump < current_fitness:
                monkeys[i] = new_monkey_jump
                fitness[i] = new_fitness_jump
                current_monkey = new_monkey_jump
                current_fitness = new_fitness_jump
            
            # Downward sliding step (escape local minima)
            new_monkey_slide = current_monkey + sliding_step * (np.random.rand(dimensions) - 0.5)
            new_monkey_slide = np.clip(new_monkey_slide, bounds[0], bounds[1])
            new_fitness_slide = sphere_function(new_monkey_slide)
            
            # If sliding improves fitness, update monkey's position
            if new_fitness_slide < current_fitness:
                monkeys[i] = new_monkey_slide
                fitness[i] = new_fitness_slide
        
        # Track the best solution found so far
        best_fitness_idx = np.argmin(fitness)
        best_solution = monkeys[best_fitness_idx]
        best_fitness = fitness[best_fitness_idx]
        
        print(f"Iteration {iteration + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run the Monkey Algorithm on the Sphere function
best_solution, best_fitness = monkey_algorithm()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

