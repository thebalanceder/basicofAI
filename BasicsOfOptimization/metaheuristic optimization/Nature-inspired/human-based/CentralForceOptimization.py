import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Parameters for CFO
NUM_PROBES = 30          # Number of probes (agents)
MAX_ITERATIONS = 1000    # Maximum number of iterations
ALPHA = 0.1              # Attraction constant
BOUNDS = [-5.12, 5.12]   # Search space bounds
GENOME_LENGTH = 2        # Dimensionality of the problem

# Initialize a probe (random position and velocity)
def create_probe():
    position = np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)
    velocity = np.zeros(GENOME_LENGTH)
    return {'position': position, 'velocity': velocity}

# Evaluate fitness for each probe (using the Rastrigin function)
def evaluate_fitness(probes):
    return [rastrigin_function(probe['position']) for probe in probes]

# Update the velocity of each probe
def update_velocity(probes, best_position, best_fitness, alpha):
    for probe in probes:
        current_position = probe['position']
        current_fitness = rastrigin_function(current_position)
        distance = np.linalg.norm(best_position - current_position) + 1e-6  # To avoid division by zero
        
        # Update velocity using gravitational-like attraction
        probe['velocity'] += alpha * (best_fitness - current_fitness) / distance**2 * (best_position - current_position)

# Update the position of each probe based on its velocity
def update_position(probes):
    for probe in probes:
        probe['position'] += probe['velocity']
        # Ensure the position stays within the bounds
        probe['position'] = np.clip(probe['position'], BOUNDS[0], BOUNDS[1])

# Main CFO algorithm
def central_force_optimization():
    # Step 1: Initialize population of probes
    probes = [create_probe() for _ in range(NUM_PROBES)]
    best_solution = None
    best_fitness = float('inf')

    # Step 2: Iterative optimization process
    for iteration in range(MAX_ITERATIONS):
        # Evaluate fitness of probes
        fitnesses = evaluate_fitness(probes)
        
        # Update the best solution found so far
        for i, fitness in enumerate(fitnesses):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = probes[i]['position']
        
        # Step 3: Update velocities of the probes
        update_velocity(probes, best_solution, best_fitness, ALPHA)
        
        # Step 4: Update positions of the probes
        update_position(probes)
        
        # Print progress
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")
    
    return best_solution, best_fitness

# Run the CFO algorithm
best_solution, best_fitness = central_force_optimization()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

