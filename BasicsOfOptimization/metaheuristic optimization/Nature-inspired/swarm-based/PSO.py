import numpy as np

# Objective function: Sphere function
def objective_function(position):
    x,y,z=position
    return np.sum(x ** 2+y**3+z**4)

# PSO Algorithm
class Particle:
    def __init__(self, num_dimensions):
        # Randomly initialize position and velocity
        self.position = np.random.uniform(-10, 10, num_dimensions)
        self.a=self.position
        self.velocity = np.random.uniform(-1, 1, num_dimensions)
        self.best_position = np.copy(self.position)
        self.best_value = objective_function(self.position)
        
    def update_velocity(self, global_best_position, w, c1, c2):
        r1, r2 = np.random.rand(), np.random.rand()
        cognitive_component = c1 * r1 * (self.best_position - self.position)
        social_component = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive_component + social_component
        
    def update_position(self):
        self.position += self.velocity
        # You can add boundary constraints if necessary
    
    def evaluate(self):
        current_value = objective_function(self.position)
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_position = np.copy(self.position)

def pso(num_particles, num_dimensions, num_iterations, w=0.5, c1=1.5, c2=1.5):
    # Initialize particles
    swarm = [Particle(num_dimensions) for _ in range(num_particles)]
    global_best_position = np.copy(swarm[0].best_position)
    global_best_value = swarm[0].best_value
    a=swarm[0].a
    # Main loop
    for _ in range(num_iterations):
        for particle in swarm:
            # Evaluate particle and update personal best
            particle.evaluate()
            # Update global best
            if particle.best_value < global_best_value:
                global_best_value = particle.best_value
                global_best_position = np.copy(particle.best_position)
        
        for particle in swarm:
            # Update velocity and position of the particle
            particle.update_velocity(global_best_position, w, c1, c2)
            particle.update_position()
    
    return global_best_position, global_best_value, a

# Parameters
num_particles = 30
num_dimensions = 3
num_iterations = 100

# Run PSO
best_position, best_value,a = pso(num_particles, num_dimensions, num_iterations)

print("fist initiated position:",a)
print("Best position found by PSO:", best_position)
print("Best objective value:", best_value)

