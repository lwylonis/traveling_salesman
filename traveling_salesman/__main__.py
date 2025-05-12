import numpy as np
import math
import argparse
from traveling_salesman.utils import *


# Argument settings
parser = argparse.ArgumentParser()
parser.add_argument('--coordinates_path', type=str, required=True, help='Path to list of coordinates')
parser.add_argument('--permutation_output_path', type=str, required=True, help='Path to output folder for permutation')
parser.add_argument('--image_output_path', type=str, required=True, help='Path to output folder for image')
parser.add_argument('--init', type=str, required=True, help='Initialization: original, random, nn')
parser.add_argument('--cooling', type=str, required=True, help='Cooling schedule: inverse_log, geometric')
parser.add_argument('--num_steps', type=str, required=True, help='Number of steps')
args = parser.parse_args()

# Global variables
NODE_COORDINATES = read_input(args.coordinates_path)
NUM_NODES = len(NODE_COORDINATES)
NUM_STEPS = int(args.num_steps)

# Initialization
if args.init == 'original':
    perm = list(range(NUM_NODES))
elif args.init == 'random':
    perm = np.random.default_rng().permutation(NUM_NODES).tolist()
elif args.init == 'nn':
    perm = nearest_neighbor_start(NODE_COORDINATES)
else:
    raise ValueError(f'Unknown intialization: {args.init}')

# Estimate initial temperature
T0 = estimate_T0(perm, NODE_COORDINATES)
Tf = 1e-4 #always finishes at 1e-4, otherwise will be stuck in place
alpha = (Tf / T0) ** (1 / NUM_STEPS) # Geometric cooling parameter
T = T0

# Log initial values
print(f'INITIAL PARAMETERS')
print(f'    Initial distance: {round(total_distance(perm, NODE_COORDINATES), 5)}')
print(f'    Initial temperature: {round(T0, 4)}')
print(f'    Number of nodes: {NUM_NODES}')
print(f'    Number of steps: {NUM_STEPS}')
print(f'    Initialization: {args.init}')
print(f'    Cooling: {args.cooling}\n')

# Parameters to keep track of through simulation
best_perm = perm.copy()
best_dist = total_distance(perm, NODE_COORDINATES)
best_step = 0

# Simulation loop
for k in range(1, NUM_STEPS):

    # Cooling schedule
    if args.cooling == 'geometric':
        T *= alpha
    elif args.cooling == 'inverse_log':
        T = T0/math.log(k + 2)
    else:
        raise ValueError(f'Unknown cooling schedule: {args.cooling}')

    # Updates permutation
    accepted = update(perm, NODE_COORDINATES, T)
    if accepted:
        d = total_distance(perm, NODE_COORDINATES)
        if d < best_dist:
            best_dist = d
            best_step = k
            best_perm = perm.copy()


# Log results
print(f"RESULTS")
print(f"    Best distance: {round(best_dist, 5)}")
print(f"    Best step: {best_step}")
print(f"    Final temperature: {round(T, 4)}\n")

# Save best permutation
permf_name = args.permutation_output_path
with open(permf_name, "w", encoding="utf-8") as fout:
    fout.write(",".join(map(str, best_perm)))
    fout.write("\n")
print(f"Saved permutation to {args.permutation_output_path}")

# Plot final image and save
plot_edges(best_perm, NODE_COORDINATES, args.image_output_path)