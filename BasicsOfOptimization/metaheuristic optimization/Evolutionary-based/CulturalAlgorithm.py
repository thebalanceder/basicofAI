import numpy as np
import random

# Parameters for the Cultural Algorithm
POPULATION_SIZE = 50
GENOME_LENGTH = 2  # Optimizing for two variables (x1, x2)
GENERATIONS = 100
MUTATION_RATE = 0.2
MUTATION_SCALE = 0.1

# Sphere function to minimize
def sphere_function(solution):
    return np.sum(solution**2)

# Create a random individual (solution)
def create_individual():
    return np.random.uniform(-5.12, 5.12, GENOME_LENGTH)

# Create an initial population
def create_population(size):
    return [create_individual() for _ in range(size)]

# Mutation: Apply small changes to the solution
def mutate(individual):
    if np.random.rand() < MUTATION_RATE:
        mutation = np.random.normal(0, MUTATION_SCALE, size=GENOME_LENGTH)
        individual += mutation
    return np.clip(individual, -5.12, 5.12)

# Belief space with normative knowledge (range for genes) and situational knowledge (best solution)
class BeliefSpace:
    def __init__(self):
        # Initialize normative belief (ranges) and situational belief (best solution)
        self.normative_range = [(-5.12, 5.12)] * GENOME_LENGTH
        self.best_solution = None

    # Update the belief space with knowledge from the population
    def update_belief_space(self, population, fitnesses):
        # Update situational knowledge with the best solution
        best_idx = np.argmin(fitnesses)
        best_individual = population[best_idx]
        if self.best_solution is None or sphere_function(best_individual) < sphere_function(self.best_solution):
            self.best_solution = best_individual

        # Update normative knowledge (range of genes in the population)
        population_matrix = np.array(population)
        for i in range(GENOME_LENGTH):
            min_gene_value = np.min(population_matrix[:, i])
            max_gene_value = np.max(population_matrix[:, i])
            self.normative_range[i] = (min_gene_value, max_gene_value)

    # Influence the population based on the belief space
    def influence_population(self, individual):
        # Modify the genes to be within the normative range
        for i in range(GENOME_LENGTH):
            norm_min, norm_max = self.normative_range[i]
            individual[i] = np.clip(individual[i], norm_min, norm_max)
        return individual

# Selection: Choose the best individuals for the next generation
def select(population, fitnesses, retain_fraction=0.3):
    retain_length = int(len(population) * retain_fraction)
    sorted_indices = np.argsort(fitnesses)  # Sort by fitness (ascending)
    selected = [population[i] for i in sorted_indices[:retain_length]]
    return selected

# Crossover: Combine two parents to create a child (average genes)
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2

# Cultural Algorithm
def cultural_algorithm():
    # Initialize population and belief space
    population = create_population(POPULATION_SIZE)
    belief_space = BeliefSpace()

    for generation in range(GENERATIONS):
        fitnesses = np.array([sphere_function(individual) for individual in population])

        # Get the best fitness in the current generation
        best_fitness = np.min(fitnesses)
        print(f"Generation {generation}: Best fitness = {best_fitness}")

        # Update the belief space with knowledge from the current population
        belief_space.update_belief_space(population, fitnesses)

        # Select the top individuals for the next generation
        selected = select(population, fitnesses)

        # Create new population via crossover and mutation
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.choices(selected, k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            
            # Influence the child based on the belief space
            child = belief_space.influence_population(child)
            new_population.append(child)

        # Update the population
        population = new_population

    # Return the best solution found
    best_fitness = np.min([sphere_function(ind) for ind in population])
    best_solution = population[np.argmin([sphere_function(ind) for ind in population])]
    return best_solution, best_fitness

# Run the Cultural Algorithm
best_solution, best_fitness = cultural_algorithm()
print(f"Best solution: {best_solution}, Fitness: {best_fitness}")

