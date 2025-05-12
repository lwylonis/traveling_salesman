import os
import random
import math
import matplotlib.pyplot as plt


def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.hypot(x2 - x1, y2 - y1)

def total_distance(perm, coords):
    dist = 0.0
    length = len(perm)
    for i in range(length):
        curr = perm[i]
        next = perm[(i+1)%length]
        dist += distance(coords[curr], coords[next])
    return dist

def change_perm(perm, i, j):
    while i < j:
        perm[i], perm[j] = perm[j], perm[i]
        i += 1
        j -= 1

def update(perm, coords, T):

    N = len(perm)
    i, j = random.sample(range(N), 2)
    i, j = min(i, j), max(i, j)

    diff = distance(coords[perm[(i-1)%N]], coords[perm[i]]) - distance(coords[perm[(i-1)%N]], coords[perm[j]]) + distance(coords[perm[j]], coords[perm[(j+1)%N]]) - distance(coords[perm[i]], coords[perm[(j+1)%N]])

    if diff > 0:
        change_perm(perm, i, j)
        return True
    else:
        u = random.random()
        if u < math.exp(diff/T):
            change_perm(perm, i, j)
            return True
        return False
    
def read_input(path):
    coords = []
    with open(path, 'r') as f:
        for line in f:
            x, y = line.strip().split(',')
            coords.append((float(x), float(y)))
    return coords

def plot_edges(perm, coords, path=None):

    x = [coords[i][0] for i in perm] + [coords[perm[0]][0]]
    y = [coords[i][1] for i in perm] + [coords[perm[0]][1]]
    
    fig, ax = plt.subplots()
    ax.plot(x, y, '-o') 
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Tour Plot")

    if path:
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved tour plot to {path}")
    else:
        plt.show()
        plt.close(fig)

def nearest_neighbor_start(coords, start=0):
    N = len(coords)
    unvisited = set(range(N))
    tour = [start]
    unvisited.remove(start)
    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda j: distance(coords[last], coords[j]))
        tour.append(next_city)
        unvisited.remove(next_city)
    return tour

def estimate_T0(perm, coords, n_samples=100):
    bad_diffs = []
    N = len(coords)
    for _ in range(n_samples):
        i, j = sorted(random.sample(range(len(perm)), 2))
        diff = distance(coords[perm[(i-1)%N]], coords[perm[i]]) - distance(coords[perm[(i-1)%N]], coords[perm[j]]) + distance(coords[perm[j]], coords[perm[(j+1)%N]]) - distance(coords[perm[i]], coords[perm[(j+1)%N]])
        if diff < 0:
            bad_diffs.append(-diff)
    avg_bad = sum(bad_diffs) / len(bad_diffs)
    return -avg_bad / math.log(0.8)
