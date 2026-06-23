import numpy as np

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def build_qubo(points):
    n = len(points)
    Q = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                Q[i][j] = distance(points[i], points[j])

    return Q

def compute_energy(path, Q):
    energy = 0

    for i in range(len(path)):
        current_point = path[i]
        next_point = path[(i + 1)%len(path)]

        energy += Q[current_point][next_point]

    return energy