import random

import numpy as np


class Particle:
    def __init__(self, x, y, velocities):
        self.x = x
        self.y = y
        self.velocity = list(velocities[np.random.randint(len(velocities))])
        self.velocities = velocities

    def move(self, grid, grid_size):
        new_x = self.x + self.velocity[0]
        new_y = self.y + self.velocity[1]

        if new_x < 0 or new_x >= grid_size-1 or new_y < 0 or new_y >= grid_size-1:
            if((new_x < 0 and new_y==0 or new_y==grid_size-1 ) or
                    (new_y<0 or new_y>grid_size-1 and new_x==0)):
                self.velocity=[1,0]
            if (new_x > grid_size-1 and new_y == 0 or new_y == grid_size - 1) or (
                        new_y < 0 or new_y > grid_size - 1 and new_x == grid_size-1):
                    self.velocity = [-1, 0]
            self._bounce()

        elif grid[new_y][new_x] == 255:
            self._bounce()
            new_x, new_y = self.x, self.y
        else:
            self.x, self.y = new_x, new_y

    def _bounce(self):
        if self.velocity == [1, 0] or self.velocity == [-1, 0]:
            rand=random.choice([1,2])
            self.velocity = list(self.velocities[2+rand])
        elif self.velocity == [0, 1] or self.velocity == [0, -1]:
            rand = random.choice([1, 2])
            self.velocity = list(self.velocities[rand])
