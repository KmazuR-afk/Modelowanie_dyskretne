
import numpy as np
from Particles import Particle

class Automaton:
    def __init__(self, grid_size, particle_prob):
        self.grid_size = grid_size
        self.particle_prob = particle_prob
        self.velocity_vectors = np.array([
            (0, 0),  # Stacjonarny
            (1, 0),  # Prawo
            (-1, 0),  # Lewo
            (0, 1),  # Dół
            (0, -1)  # Góra
        ])
        self.num_directions = len(self.velocity_vectors)
        self.state, self.buf = self.make_map(particle_prob)
        self.particles = [
            Particle(x, y, self.velocity_vectors)
            for x in range(grid_size)
            for y in range(grid_size)
            if self.state[y, x] == 1
        ]
        print("NPARTICLES: ",len(self.particles))

    def propagate(self):
        for particle in self.particles:
            particle.move(self.state, self.grid_size)

    def collide(self):

        self.propagate()

        self.state = np.copy(self.buf)
        collisions = {}

        for particle in self.particles:
            col = (particle.x, particle.y)
            if col not in collisions:
                collisions[col] = []
            collisions[col].append(particle)

        for col in collisions:
            if len(collisions[col]) > 1:
                self.solve_collision(collisions[col])

        for particle in self.particles:
            self.state[particle.y, particle.x] += 1

    def solve_collision(self, particles_in_collision):
        for particle in particles_in_collision:
            particle._bounce()

    def make_map(self, particle_prob):
        map = np.zeros((self.grid_size, self.grid_size))
        clean_map = np.zeros((self.grid_size, self. grid_size))
        limit = self.grid_size // 4
        step = self.grid_size // 80
        map[:, :limit - step] = np.random.choice([0, 1], size=(self.grid_size, limit - step),
                                                 p=[1 - particle_prob, particle_prob])
        for x in range(self.grid_size):
            map[0][x] = 255
            for y in range(self.grid_size):
                if x == 0 or x == self.grid_size - 1:
                    map[0][x] = 255
                map[y, limit - step:limit + step] = 255 if (
                        y < 45 * self.grid_size // 100 or y > 55 * self.grid_size // 100) else map[y,
                                                                                     limit - step:limit + step]
        for x in range(self.grid_size):
            clean_map[0][x] = 255
            for y in range(self.grid_size):
                if x == 0 or x == self.grid_size - 1:
                    clean_map[0][x] = 255
                clean_map[y, limit - step:limit + step] = 255 if (
                        y < 45 * self.grid_size // 100 or y > 55 * self.grid_size // 100) else clean_map[y,limit - step:limit + step]

        return map, clean_map

    def reset(self):
        self.state, self.buf = self.make_map(self.particle_prob)
        del self.particles
        self.particles = [
            Particle(x, y, self.velocity_vectors)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if self.state[y, x] == 1
        ]
        print("NPARTICLES: ", len(self.particles))
        return True