import random
import numpy as np
from numba import njit, prange
GRID_SIZE=100
@njit(parallel=True)
def collision_step(state, map, w,tau):
    size = state.shape[0]
    for x in prange(size):
        for y in range(size):
            if not np.array_equal(map[y, x], [0, 0, 0]):
                C = np.sum(state[y, x])
                for i in range(4):
                    feq = C * w[i]
                    state[y, x, i] += (feq - state[y, x, i])/tau
    return state

@njit(parallel=True)
def streaming_step(state, next_state, map, Dirs):
    size = state.shape[0]
    next_state.fill(0)
    for x in prange(size):
        for y in range(size):
            if not np.array_equal(map[y, x], [0, 0, 0]):
                for i in range(4):
                    dx, dy = Dirs[i]
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        if np.array_equal(map[ny, nx], [0, 0, 0]):  # Odbicie
                            next_state[y, x, (i + 2) % 4] += state[y, x, i]
                        else:
                            next_state[ny, nx, i] += state[y, x, i]
    return next_state
class LBM:
    def __init__(self,tau,size=GRID_SIZE, num_dirs=4):
        self.size=size      #zakładmay kwadratową przestrzeń
        self.tau=tau        #współczynnik tau wykorzystywany w obliczaniu kroku kolizji
        self.state=np.zeros((size,size,num_dirs))     #macierz f - stanów
        self.next_state=np.copy(self.state)    #macierz fout - pomocnicza w obliczeniach
        self.map=self.make_map()               #mapa przechwoująca obraz przestrzeni - używana do rysowania
        self.initialize_state(num_dirs)
        self.num_dirs=num_dirs#wywołanie funkcji inicjalizującej stan

    def initialize_state(self,num_dirs):
        limit = self.size // 4
        step = self.size // 80
        if type(self)==LBM:
            for x in range(limit - step):
                for y in range(self.size):
                    for i in range(num_dirs):
                        rest=1-np.sum(self.state[y,x])
                        self.state[y,x,i]=random.uniform(0.0,rest)
        else:
            for x in range(self.size):
                for y in range(self.size):
                    if x<limit-step:
                        self.state[y,x,:] = 1.0/num_dirs
                    elif x>limit+step:
                        self.state[y,x,:]=0.5/num_dirs
    def step(self):
        w = np.array([0.25] * 4)
        Dirs = np.array([[0, -1], [1, 0], [0, 1], [-1, 0]])
        self.state = collision_step(self.state, self.map, w,self.tau)
        self.next_state = streaming_step(self.state, self.next_state, self.map, Dirs)
        self.state = np.copy(self.next_state)
        self.count_intensity()

    def make_map(self):
        map = np.zeros((self.size, self.size,3))
        limit = self.size // 4
        step = self.size // 80
        for x in range(1,self.size-1):
            for y in range(1,self.size-1):
                if x<limit+step and x>limit-step:
                    if y > 45 * self.size // 100 and y < 55 * self.size // 100:
                    #if y==50*self.size//100:
                        map[y][x] = [255, 255, 255]
                else:
                    map[y][x]=[255,255,255]
        return map

    def count_intensity(self):
        limit = self.size // 4
        step = self.size // 80
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                if not np.array_equal(self.map[y][x],[0,0,0]):
                    ret = abs(np.sum((self.state[y][x])))
                    if ret == 0:  # Brak intensywności, kolor biały
                        self.map[y][x] = [255, 255, 255]
                    else:
                        # Normalizacja ret do zakresu [0, 1]
                        ret_normalized = min(ret, 1.0)
                        r = int(255 * (1 - ret_normalized))
                        g = 255# Zielony stały
                        b = int(255 * (1 - ret_normalized))
                        self.map[y][x] = [r, g, b]

    def reset(self):
        self.state[:,:].fill(0)
        self.initialize_state(self.num_dirs)
        self.map= self.make_map()