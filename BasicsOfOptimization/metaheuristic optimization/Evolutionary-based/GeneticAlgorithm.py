import random

# Parameters for GA
POPULATION_SIZE = 20
GENES = (0, 1)  # Binary chromosome
GENE_LENGTH = 5  # Chromosome length
MUTATION_RATE = 0.01
GENERATIONS = 100

# Target function to minimize: f(x) = x^2
def fitness(chromosome):
    # Convert binary chromosome to integer
    value = int(''.join(map(str, chromosome)), 2)
    return (value+1)**3+3

# Create a random chromosome
def create_chromosome():
    return [random.choice(GENES) for _ in range(GENE_LENGTH)]

# Selection: Tournament selection
def select(population, fitnesses):
    tournament = random.sample(list(zip(population, fitnesses)), 3)
    return min(tournament, key=lambda x: x[1])[0]

# Crossover: Single-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, GENE_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation: Flip a random gene
def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        point = random.randint(0, GENE_LENGTH - 1)
        chromosome[point] = 1 - chromosome[point]  # Flip the bit

# Initialize population
population = [create_chromosome() for _ in range(POPULATION_SIZE)]

# Main GA loop
for generation in range(GENERATIONS):
    fitnesses = [fitness(chromosome) for chromosome in population]
    
    # Print best chromosome of the generation
    best = min(fitnesses)
    print(f'Generation {generation + 1}: Best fitness = {best}')
    
    new_population = []
    
    # Create new generation
    while len(new_population) < POPULATION_SIZE:
        # Selection
        parent1 = select(population, fitnesses)
        parent2 = select(population, fitnesses)
        
        # Crossover
        child1, child2 = crossover(parent1, parent2)
        
        # Mutation
        mutate(child1)
        mutate(child2)
        
        new_population.extend([child1, child2])
    
    # Update population for next generation
    population = new_population[:POPULATION_SIZE]

