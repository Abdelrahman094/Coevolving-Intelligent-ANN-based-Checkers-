import numpy as np

def crossover(first, second, prob=0.25):
    return np.array([second[i] if np.random.rand() < prob else w for i, w in enumerate(first)])

def mutate(master, prob=0.25, delta=0.5):
    return np.array([w + np.random.rand() * delta - (delta / 2) if np.random.rand() < prob else w for w in master])

def create_new(size, delta=4):
    return np.array([np.random.rand() * delta - (delta / 2) for _ in range(size)])

def create_empty(size):
    return np.empty(size, dtype=np.float32)
