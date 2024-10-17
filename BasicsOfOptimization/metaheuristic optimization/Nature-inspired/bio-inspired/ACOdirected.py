import numpy as np

class AntColonyOptimization:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        # Allowing for non-square distance matrix
        self.distances = distances
        self.n_rows, self.n_cols = distances.shape  # Rows and columns of the matrix
        self.pheromone = np.ones((self.n_rows, self.n_cols)) / self.n_rows  # Pheromone matrix with the same shape
        self.all_row_indices = range(self.n_rows)
        self.all_col_indices = range(self.n_cols)
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
                # Spread pheromone across rows and columns based on non-square matrix
                self.pheromone[move[0], move[1]] += 1.0 / dist

    def generate_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.generate_path(0)
            all_paths.append((path, self.calculate_path_distance(path)))
        return all_paths

    def generate_path(self, start_row):
        path = []
        visited_cols = set()
        prev_row = start_row
        for i in range(min(self.n_rows, self.n_cols) - 1):
            move = self.pick_move(self.pheromone[prev_row], self.distances[prev_row], visited_cols)
            path.append((prev_row, move))
            prev_row = move
            visited_cols.add(move)
        return path

    def pick_move(self, pheromone_row, dist_row, visited_cols):
        pheromone_row = np.copy(pheromone_row)
        pheromone_row[list(visited_cols)] = 0

        # Avoid division by zero by replacing zero distances with a large value
        dist_row = np.where(dist_row == 0, np.inf, dist_row)

        row = pheromone_row ** self.alpha * ((1.0 / dist_row) ** self.beta)
        norm_row = row / row.sum()  # Normalize to get probabilities
        move = np.random.choice(self.all_col_indices, 1, p=norm_row)[0]
        return move

    def calculate_path_distance(self, path):
        total_distance = 0
        for row, col in path:
            total_distance += self.distances[row, col]
        return total_distance


# Example non-square distance matrix (e.g., 3 rows, 4 columns)
distances = np.array([[0, 2, 9, 10],
                      [1, 0, 6, 4],
                      [7, 4, 0, 8]])

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

