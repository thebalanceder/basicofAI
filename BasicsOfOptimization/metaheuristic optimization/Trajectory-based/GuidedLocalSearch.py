import numpy as np
import random

# Objective function: Traveling Salesman Problem (TSP) distance calculation
def tsp_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i+1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]  # Return to starting city
    return total_distance

# Local search: 2-opt swap for TSP
def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

# Guided Local Search (GLS) Algorithm
def guided_local_search(distance_matrix, max_iter=100, penalty_weight=0.1):
    num_cities = len(distance_matrix)
    
    # Step 1: Initialization
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)  # Start with a random tour
    penalties = np.zeros((num_cities, num_cities))  # Initialize penalties to zero
    best_tour = current_tour
    best_distance = tsp_distance(current_tour, distance_matrix)
    
    # Step 2: GLS iterations
    for iteration in range(max_iter):
        # Step 3: Perform local search (2-opt for TSP)
        improved = True
        while improved:
            improved = False
            for i in range(1, num_cities - 1):
                for j in range(i+ 1, num_cities):
                    new_tour = two_opt_swap(current_tour, i, j)
                    new_distance = tsp_distance(new_tour, distance_matrix) + penalty_weight * np.sum(penalties[new_tour[:-1], new_tour[1:]])
                    
                    if new_distance < best_distance:
                        current_tour = new_tour
                        best_tour = new_tour
                        best_distance = new_distance
                        improved = True

        # Step 4: Update penalties when stuck in a local optimum
        if not improved:
            # Identify features (edges) that contribute the most to the current solution
            for i in range(num_cities):
                a, b = current_tour[i], current_tour[(i+1) % num_cities]
                penalties[a][b] += 1
                penalties[b][a] += 1  # Symmetric for undirected graph

        # Print current best solution
        print(f"Iteration {iteration + 1}, Best tour: {best_tour}, Best distance: {best_distance}")

    return best_tour, best_distance

# Example distance matrix for TSP
distance_matrix = np.array([
    [0, 29, 20, 21],
    [29, 0, 15, 17],
    [20, 15, 0, 28],
    [21, 17, 28, 0]
])

# Run Guided Local Search on the TSP problem
best_tour, best_distance = guided_local_search(distance_matrix)

# Output final best solution
print(f"Final best tour: {best_tour}")
print(f"Final best distance: {best_distance}")

