import numpy as np
import random

class AntColonyOptimization:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_indices = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.generate_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone *= self.decay
        return all_time_shortest_path

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def generate_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.generate_path(0)
            all_paths.append((path, self.calculate_path_distance(path)))
        return all_paths

    def generate_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # returning to the starting city
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        # Avoid division by zero by replacing zero distances with a small value
        dist = np.where(dist == 0, np.inf, dist)

        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        norm_row = row / row.sum()  # Normalize to get probabilities
        move = np.random.choice(self.all_indices, 1, p=norm_row)[0]
        return move

    def calculate_path_distance(self, path):
        total_distance = 0
        for ele in path:
            total_distance += self.distances[ele]
        return total_distance

# Distance matrix representing cities
distances = np.array([[0, 2, 2, 5, 7],
                      [2, 0, 5, 8, 2],
                      [2, 5, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])

# Parameters for ACO
n_ants = 10
n_best = 3
n_iterations = 100
decay = 0.95
alpha = 1
beta = 2

aco = AntColonyOptimization(distances, n_ants, n_best, n_iterations, decay, alpha, beta)
shortest_path = aco.run()

print("The shortest path found is:", shortest_path[0])
print("The total distance is:", shortest_path[1])

