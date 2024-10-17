import numpy as np

# Rastrigin function to minimize
def rastrigin_function(x):
    return 10 * len(x) + sum([xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x])

# Initialize parameters
NUM_GLOWWORMS = 50
GENOME_LENGTH = 2  # Dimensionality of the problem
MAX_ITERS = 1000
RANGE_MAX = 1.0
STEP_SIZE = 0.03
LUCIFERIN_DECAY = 0.4
LUCIFERIN_ENHANCEMENT = 0.6
NEIGHBOR_COUNT = 5

# Search space bounds
BOUNDS = [-5.12, 5.12]

# Glowworm class to represent each agent
class Glowworm:
    def __init__(self):
        self.position = np.random.uniform(BOUNDS[0], BOUNDS[1], GENOME_LENGTH)
        self.luciferin = 0.0
        self.range = RANGE_MAX

    def update_luciferin(self, fitness):
        self.luciferin = (1 - LUCIFERIN_DECAY) * self.luciferin + LUCIFERIN_ENHANCEMENT * fitness

    def move_towards(self, neighbor):
        direction = neighbor.position - self.position
        if np.linalg.norm(direction) > 0:  # Avoid division by zero
            self.position += STEP_SIZE * direction / np.linalg.norm(direction)
        # Ensure position is within bounds
        self.position = np.clip(self.position, BOUNDS[0], BOUNDS[1])

    def update_range(self, neighbor_count):
        self.range = min(RANGE_MAX, max(0, self.range + 0.1 * (NEIGHBOR_COUNT - neighbor_count)))

# Main GSO algorithm
def glowworm_swarm_optimization():
    # Step 1: Initialize the glowworms
    glowworms = [Glowworm() for _ in range(NUM_GLOWWORMS)]
    
    best_solution = None
    best_fitness = float('inf')

    # Step 2: Iterative optimization process
    for iteration in range(MAX_ITERS):
        fitnesses = [rastrigin_function(gw.position) for gw in glowworms]
        
        # Update best solution found
        for i, fitness in enumerate(fitnesses):
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = glowworms[i].position

        # Step 3: Update luciferin values for all glowworms
        for i, gw in enumerate(glowworms):
            gw.update_luciferin(1 / (1 + fitnesses[i]))  # Use 1/(1+fitness) for minimization

        # Step 4: Movement of glowworms towards neighbors with higher luciferin
        for i, gw in enumerate(glowworms):
            # Find neighbors within range
            neighbors = [glowworms[j] for j in range(NUM_GLOWWORMS) if i != j and np.linalg.norm(gw.position - glowworms[j].position) < gw.range]
            
            # Move towards the brightest neighbor
            brighter_neighbors = [n for n in neighbors if n.luciferin > gw.luciferin]
            if brighter_neighbors:
                brightest_neighbor = max(brighter_neighbors, key=lambda n: n.luciferin)
                gw.move_towards(brightest_neighbor)

            # Step 5: Update range based on neighbor count
            gw.update_range(len(neighbors))

        # Print progress
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the GSO algorithm
best_solution, best_fitness = glowworm_swarm_optimization()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

