import numpy as np

# Distance matrix for TSP (example: 4 cities)
dist_matrix = np.array([[0, 2, 9, 10],
                        [1, 0, 6, 4],
                        [15, 7, 0, 8],
                        [6, 3, 12, 0]])

# Parameters for IWD
num_cities = dist_matrix.shape[0]
num_water_drops = 10
max_iterations = 100
C_v = 100
C_s = 0.01
initial_soil = 1000

# Initialize soil matrix
soil_matrix = np.ones((num_cities, num_cities)) * initial_soil

# IWD algorithm
def iwd_tsp():
    # Initialize best tour and best distance
    best_tour = None
    best_distance = np.inf

    for iteration in range(max_iterations):
        tours = []
        tour_distances = []
        
        for wd in range(num_water_drops):
            # Initialize water drop's tour
            tour = [np.random.randint(num_cities)]  # Start from a random city
            visited = set(tour)
            current_city = tour[-1]
            
            # Travel to each city
            for step in range(num_cities - 1):
                # Compute probabilities of going to unvisited cities
                unvisited = [city for city in range(num_cities) if city not in visited]
                probabilities = []
                for city in unvisited:
                    soil = soil_matrix[current_city, city]
                    probabilities.append(1 / (soil + C_s))
                
                probabilities = np.array(probabilities) / np.sum(probabilities)
                
                # Select next city based on probability
                next_city = np.random.choice(unvisited, p=probabilities)
                tour.append(next_city)
                visited.add(next_city)
                
                # Update velocity and soil
                soil = soil_matrix[current_city, next_city]
                velocity = C_v / (C_s + soil)
                soil_matrix[current_city, next_city] -= velocity  # Soil removal
                
                current_city = next_city
            
            # Return to the starting city
            tour.append(tour[0])
            tour_distance = sum(dist_matrix[tour[i], tour[i+1]] for i in range(len(tour) - 1))
            
            tours.append(tour)
            tour_distances.append(tour_distance)
        
        # Update best solution if a better tour is found
        min_distance_idx = np.argmin(tour_distances)
        if tour_distances[min_distance_idx] < best_distance:
            best_distance = tour_distances[min_distance_idx]
            best_tour = tours[min_distance_idx]
        
        print(f"Iteration {iteration + 1}, Best Distance: {best_distance}")
    
    return best_tour, best_distance

# Run IWD for TSP
best_tour, best_distance = iwd_tsp()

# Output the best solution
print(f"Best tour found: {best_tour}")
print(f"Best distance: {best_distance}")

