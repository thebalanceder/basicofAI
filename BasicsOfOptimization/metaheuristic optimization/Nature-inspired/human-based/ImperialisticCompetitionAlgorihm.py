import numpy as np

# Objective function: Sphere function
def sphere_function(x):
    return np.sum(x ** 2)

# Initialize nations (population)
def initialize_nations(pop_size, dimensions, bounds):
    population = np.random.uniform(bounds[0], bounds[1], (pop_size, dimensions))
    return population

# Imperialistic Competitive Algorithm (ICA)
def ica(pop_size=50, num_imperialists=5, dimensions=5, bounds=(-5, 5), generations=100, beta=2, zeta=0.1, revolution_rate=0.1):
    # Step 1: Initialize population (nations)
    population = initialize_nations(pop_size, dimensions, bounds)
    fitness = np.array([sphere_function(ind) for ind in population])
    
    # Step 2: Sort the population and divide it into imperialists and colonies
    sorted_indices = np.argsort(fitness)
    imperialists = population[sorted_indices[:num_imperialists]]
    colonies = population[sorted_indices[num_imperialists:]]
    
    # Assign colonies to imperialists
    num_colonies_per_empire = len(colonies) // num_imperialists
    empires = [colonies[i*num_colonies_per_empire: (i+1)*num_colonies_per_empire] for i in range(num_imperialists)]
    
    # Step 3: Start the evolutionary process
    for generation in range(generations):
        # Step 4: Assimilation: move colonies towards the imperialist
        for i in range(num_imperialists):
            imperialist = imperialists[i]
            empire = empires[i]
            for j in range(len(empire)):
                # Move colony towards imperialist
                empire[j] += beta * np.random.rand(dimensions) * (imperialist - empire[j])
                # Ensure bounds
                empire[j] = np.clip(empire[j], bounds[0], bounds[1])
        
        # Step 5: Revolution: some colonies undergo random changes
        for i in range(len(colonies)):
            if np.random.rand() < revolution_rate:
                colonies[i] = np.random.uniform(bounds[0], bounds[1], dimensions)
        
        # Step 6: Imperialistic competition
        total_powers = []
        for i in range(num_imperialists):
            imperialist_fitness = sphere_function(imperialists[i])
            colonies_fitness = np.mean([sphere_function(col) for col in empires[i]])
            total_power = imperialist_fitness + zeta * colonies_fitness
            total_powers.append(total_power)
        
        # Find the weakest empire and give its colonies to the strongest one
        weakest_empire_idx = np.argmax(total_powers)
        strongest_empire_idx = np.argmin(total_powers)
        if empires[weakest_empire_idx].size > 0:
            weakest_colony = empires[weakest_empire_idx][-1]
            empires[strongest_empire_idx] = np.vstack((empires[strongest_empire_idx], weakest_colony))
            empires[weakest_empire_idx] = empires[weakest_empire_idx][:-1]
        
        # Step 7: Check if there is only one empire left (termination)
        if len([emp for emp in empires if emp.size > 0]) == 1:
            break
        
        # Step 8: Update the best solution
        fitness = np.array([sphere_function(ind) for ind in population])
        min_fitness_idx = np.argmin(fitness)
        best_solution = population[min_fitness_idx]
        best_fitness = fitness[min_fitness_idx]
        
        print(f"Generation {generation + 1}, Best fitness: {best_fitness}")
    
    return best_solution, best_fitness

# Run the ICA on the Sphere function
best_solution, best_fitness = ica()

# Output the final result
print(f"Best solution found: {best_solution}")
print(f"Best fitness: {best_fitness}")

