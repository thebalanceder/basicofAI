import numpy as np
import random

# Objective function (example: minimize sum of squares)
def objective_function(x):
    return sum(x_i ** 2 for x_i in x)

# Initialize population (molecules)
def initialize_population(pop_size, dim, lower_bound, upper_bound):
    return [np.random.uniform(lower_bound, upper_bound, dim).tolist() for _ in range(pop_size)]

# CRO Operations
def on_wall_ineffective_collision(molecule, lower_bound, upper_bound):
    # Apply small random change to the molecule's position
    perturbation = np.random.uniform(-1, 1, len(molecule))
    new_position = molecule + perturbation
    return np.clip(new_position, lower_bound, upper_bound)

def decomposition(molecule, lower_bound, upper_bound):
    # Decompose molecule into two new molecules
    random_vector = np.random.uniform(-1, 1, len(molecule))
    molecule1 = (molecule / 2) + random_vector
    molecule2 = (molecule / 2) - random_vector
    return [np.clip(molecule1, lower_bound, upper_bound), np.clip(molecule2, lower_bound, upper_bound)]

def intermolecular_ineffective_collision(molecule1, molecule2):
    # Exchange information between two molecules
    r1, r2 = random.random(), random.random()
    new_molecule1 = molecule1 + r1 * (molecule2 - molecule1)
    new_molecule2 = molecule2 + r2 * (molecule1 - molecule2)
    return new_molecule1, new_molecule2

def synthesis(molecule1, molecule2):
    # Combine two molecules into one
    return (molecule1 + molecule2) / 2

# CRO Algorithm
def chemical_reaction_optimization(pop_size=30, dim=5, lower_bound=-10, upper_bound=10, max_iter=100):
    # Initialize population of molecules
    population = initialize_population(pop_size, dim, lower_bound, upper_bound)
    
    # Track the best solution
    best_molecule = min(population, key=objective_function)
    best_fitness = objective_function(best_molecule)
    
    for t in range(max_iter):
        for i in range(len(population)):
            reaction_type = random.choice(["on_wall", "decomposition", "intermolecular", "synthesis"])
            
            if reaction_type == "on_wall":
                # Perform on-wall ineffective collision
                population[i] = on_wall_ineffective_collision(population[i], lower_bound, upper_bound)
            
            elif reaction_type == "decomposition":
                # Perform decomposition
                new_molecules = decomposition(np.array(population[i]), lower_bound, upper_bound)
                population.extend(new_molecules)
            
            elif reaction_type == "intermolecular":
                # Perform intermolecular ineffective collision with a random molecule
                j = random.randint(0, len(population) - 1)
                if i != j:
                    molecule1, molecule2 = intermolecular_ineffective_collision(np.array(population[i]), np.array(population[j]))
                    population[i] = molecule1
                    population[j] = molecule2
            
            elif reaction_type == "synthesis" and len(population) > 1:
                # Perform synthesis with a random molecule
                j = random.randint(0, len(population) - 1)
                if i != j:
                    population[i] = synthesis(np.array(population[i]), np.array(population[j]))

        # Update the best solution found
        current_best_molecule = min(population, key=objective_function)
        current_best_fitness = objective_function(current_best_molecule)
        
        if current_best_fitness < best_fitness:
            best_molecule = current_best_molecule
            best_fitness = current_best_fitness

        # Optionally: print progress
        print(f"Iteration {t+1}: Best Fitness = {best_fitness}")

    return best_molecule, best_fitness

# Run the CRO algorithm
best_solution, best_fitness = chemical_reaction_optimization()
print("Best Solution Found:", best_solution)
print("Best Fitness:", best_fitness)

