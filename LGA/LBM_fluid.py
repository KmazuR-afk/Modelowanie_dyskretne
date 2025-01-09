import random
import numpy as np
from numba import njit, prange

from LBM import LBM

GRID_SIZE=100
@njit(parallel=True)
def collision_step(state, map, w, tau, Dirs):
    size=state.shape[0]
    next_state=np.zeros_like(state)
    for x in range(size):
        for y in range(size):
            if not np.array_equal(map[y, x], [0, 0, 0]):
                ro=np.sum(state[y, x])
                if ro<=0:
                    continue
                else:
                    u=np.dot(state[y, x], Dirs)/ro
                    u_norm_squared = np.dot(u, u)  # |u|^2
                    ci_dot_u = np.dot(Dirs, u)
                    feq = w * ro * (1 + 3 * ci_dot_u + 4.5 * ci_dot_u ** 2 - 1.5 * u_norm_squared)
                    #if x == 10 and y == 10:
                    #    print(feq)
                    for i in range(9):
                        next_state[y, x, i]=state[y,x,i]+(feq[i] - state[y, x, i]) / tau
    return next_state

@njit(parallel=True)
def streaming_step(state, next_state, map, Dirs):
    bounce_back=np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])
    size = state.shape[0]
    state.fill(0)
    for x in prange(size):
        for y in range(size):
            if not np.array_equal(map[y, x], [0, 0, 0]):
                for i in range(9):
                    dx, dy = Dirs[i]
                    nx, ny = int(x + dx), int(y + dy)
                    if 0 <= nx < size and 0 <= ny < size:
                        if np.array_equal(map[ny, nx], [0, 0, 0]):  # Odbicie
                            state[y, x, bounce_back[i]] += next_state[y, x, i]
                        else:
                           state[ny, nx, i] += next_state[y, x, i]
    return state
class LBM_fluid(LBM):
    def __init__(self,tau,g_size=None,num_dirs=9):
        super().__init__(tau,g_size,num_dirs)
    def step(self):
        w = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
        Dirs = np.array([[0, 0], [0, -1], [1, 0], [0, 1], [-1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]],dtype=np.float64)
        self.next_state = collision_step(self.state, self.map, w,self.tau, Dirs)
        self.state = streaming_step(self.state, self.next_state, self.map, Dirs)
        #super().count_intensity()
        self.count_intensity()
        #self.count_intensity_speed(Dirs)
    def count_intensity(self):
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                if not np.array_equal(self.map[y][x], [0, 0, 0]):
                    rho = np.abs(np.sum(self.state[y, x]))  # Magnitude of velocity
                    if rho == 0:
                        self.map[y][x] = [255, 255, 255]  # White for no intensity
                    else:
                        normalized = min(rho, 1.0)  # Normalize to [0, 1]
                        red = int(255 * normalized)
                        blue = int(255 * (1 - normalized))
                        self.map[y][x] = [red, 100, blue]

    def count_intensity_speed(self,Dirs):
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                if not np.array_equal(self.map[y][x], [0, 0, 0]):
                    rho = np.sum(self.state[y, x, :])
                    u_x = np.dot(self.state[y, x, :], Dirs[:, 0]) / rho
                    u_y = np.dot(self.state[y, x, :], Dirs[:, 1]) / rho
                    self.map[y][x] = map_velocity_to_color(u_x,u_y)

def map_velocity_to_color(ux, uy):
    u_magnitude = np.sqrt(ux ** 2 + uy ** 2)
    normalized = np.clip(u_magnitude / np.max(u_magnitude), 0.5, 1)  # Normalizacja do [0, 1]

    if ux > 0:
        red = int(255 * normalized)
        green = int(255 * (1 - normalized))
        blue = 0
    elif ux < 0:
        red = 0
        green = int(255 * (1 - normalized))
        blue = int(255 * normalized)
    else:  # Neutralne prędkości
        red, green, blue = 255, 255, 255  # Biały dla zerowej prędkości

    return (red, green, blue)