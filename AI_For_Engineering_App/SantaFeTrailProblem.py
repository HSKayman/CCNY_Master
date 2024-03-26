import numpy as np
import matplotlib.pyplot as plt
grid_size = (32, 32)
trail = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
    (3, 4), (2, 4), (2, 3), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
    (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
    (16, 2), (16, 3), (16, 4), (16, 5), (15, 5), (14, 5), (13, 5), (12, 5),
    (11, 5), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5),
    (2, 5), (1, 5), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9),
    (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9),
    (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9),
    (20, 9), (20, 10), (20, 11), (20, 12), (20, 13), (20, 14), (20, 15),
    (20, 16), (20, 17), (20, 18), (20, 19), (20, 20), (20, 21), (20, 22),
    (20, 23), (20, 24), (20, 25), (20, 26), (20, 27), (20, 28), (20, 29),
    (20, 30), (20, 31)
]

grid = np.zeros(grid_size, dtype=int)
for pos in trail:
    grid[pos] = 1

class Ant:
    def __init__(self, position=(0, 0), direction=0):
        self.position = position
        self.direction = direction  # 0: right, 1: down, 2: left, 3: up
        self.collected_food = 0

    def move_forward(self):
        if self.direction == 0:  # Right
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 1:  # Down
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == 2:  # Left
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 3:  # Up
            self.position = (self.position[0] - 1, self.position[1])

        if grid[self.position] == 1:
            self.collected_food += 1
            grid[self.position] = 0  # Remove the food

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction - 1) % 4

    def simulate(self):
        for _ in range(100): 
            next_position = self.position
            if self.direction == 0:
                next_position = (self.position[0], self.position[1] + 1)
            elif self.direction == 1:
                next_position = (self.position[0] + 1, self.position[1])
            elif self.direction == 2:
                next_position = (self.position[0], self.position[1] - 1)
            elif self.direction == 3:
                next_position = (self.position[0] - 1, self.position[1])

            if 0 <= next_position[0] < grid_size[0] and 0 <= next_position[1] < grid_size[1] and grid[next_position] == 1:
                self.move_forward()
            else:
                self.turn_right()

ant = Ant()
ant.simulate()

print("Collected food:", ant.collected_food)



for pos in trail:
    grid[pos] = 1

plt.figure(figsize=(10, 10))
plt.imshow(grid.T, cmap='Greys', origin='upper')
plt.scatter(*ant.position, color='red')  
plt.title("Santa Fe Trail with Ant's Final Position")
plt.show()

