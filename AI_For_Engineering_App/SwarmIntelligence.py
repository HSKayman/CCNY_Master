#PA
import numpy as np
def objective_function(x):
    return np.sum(x**2)

n_particles = 30
n_dimensions = 2
x_min, x_max = -10, 10  
v_max = (x_max - x_min) * 0.1  
iterations = 100
w = 0.5  
c1, c2 = 2.05, 2.05  

positions = np.random.uniform(x_min, x_max, (n_particles, n_dimensions))
velocities = np.zeros((n_particles, n_dimensions))
pbest_positions = positions.copy()
pbest_scores = np.array([objective_function(x) for x in positions])
gbest_position = pbest_positions[np.argmin(pbest_scores)]
gbest_score = np.min(pbest_scores)

for it in range(iterations):
    for i in range(n_particles):
        velocities[i] = (w * velocities[i] + 
                         c1 * np.random.rand() * (pbest_positions[i] - positions[i]) + 
                         c2 * np.random.rand() * (gbest_position - positions[i]))
        velocities[i] = np.clip(velocities[i], -v_max, v_max)
        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], x_min, x_max)
        score = objective_function(positions[i])
        if score < pbest_scores[i]:
            pbest_scores[i] = score
            pbest_positions[i] = positions[i].copy()
    gbest_candidate = np.argmin(pbest_scores)
    gbest_candidate_score = pbest_scores[gbest_candidate]
    if gbest_candidate_score < gbest_score:
        gbest_score = gbest_candidate_score
        gbest_position = pbest_positions[gbest_candidate].copy()
    
    print(f"Iteration {it+1}/{iterations}, Best Solution {gbest_score}")
print(f"Best position: {gbest_position}, Best score: {gbest_score}")
