import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Harmony Search Parameters
HMS = 10       # Harmony memory size
HMCR = 0.9     # Harmony memory consideration rate
PAR = 0.3      # Pitch adjustment rate
BW = 0.05      # Bandwidth for pitch adjustment
GENOME_LENGTH = 2  # Number of variables (dimensionality of problem)
ITERATIONS = 1000  # Number of iterations
BOUNDS = [-5.12, 5.12]  # Search space bounds for Rastrigin function

# Initialize harmony memory with random solutions
def initialize_harmony_memory():
    return [np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH) for _ in range(HMS)]

# Pitch adjustment for an individual value
def pitch_adjustment(value):
    return value + BW * (np.random.rand() * 2 - 1)  # Adjust value by small random factor within [-BW, BW]

# Generate a new harmony (solution)
def generate_new_harmony(harmony_memory):
    new_harmony = np.zeros(GENOME_LENGTH)
    for i in range(GENOME_LENGTH):
        if np.random.rand() < HMCR:  # Memory consideration
            new_harmony[i] = harmony_memory[np.random.randint(HMS)][i]
            if np.random.rand() < PAR:  # Pitch adjustment
                new_harmony[i] = pitch_adjustment(new_harmony[i])
        else:
            # Random selection
            new_harmony[i] = np.random.uniform(BOUNDS[0], BOUNDS[1])
    
    # Ensure new harmony is within bounds
    return np.clip(new_harmony, BOUNDS[0], BOUNDS[1])

# Harmony Search Algorithm
def harmony_search():
    # Step 1: Initialize harmony memory with random solutions
    harmony_memory = initialize_harmony_memory()
    fitnesses = [rastrigin_function(harmony) for harmony in harmony_memory]
    
    best_solution = harmony_memory[np.argmin(fitnesses)]
    best_fitness = min(fitnesses)

    for iteration in range(ITERATIONS):
        # Step 2: Generate a new harmony
        new_harmony = generate_new_harmony(harmony_memory)
        new_fitness = rastrigin_function(new_harmony)

        # Step 3: If the new harmony is better than the worst harmony, replace the worst
        worst_index = np.argmax(fitnesses)
        if new_fitness < fitnesses[worst_index]:
            harmony_memory[worst_index] = new_harmony
            fitnesses[worst_index] = new_fitness

        # Update best solution if the new harmony is the best so far
        if new_fitness < best_fitness:
            best_fitness = new_fitness
            best_solution = new_harmony

        # Print the best fitness at each iteration
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the Harmony Search Algorithm
best_solution, best_fitness = harmony_search()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

