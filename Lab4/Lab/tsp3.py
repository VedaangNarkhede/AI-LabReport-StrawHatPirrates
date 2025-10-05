import math, random, time, os

def euclidean(a, b):
    """2-D Euclidean distance between two (x, y) points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def route_length(path):
    """Total length of a closed TSP path."""
    return sum(euclidean(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

def sa_tsp(nodes, T0=10_000, alpha=0.995, Tmin=1e-8, max_iters=1_000_000):
    """
    Simulated-annealing TSP solver.
    Neighbourhood: 2-opt (reverse a random sub-segment).
    """
    current = nodes[:]
    best    = current[:]
    n       = len(nodes)

    T, it = T0, 0
    while T > Tmin and it < max_iters:
        it += 1

        # 2-opt move
        i, j = sorted(random.sample(range(n), 2))
        neighbour = current[:]
        neighbour[i:j+1] = reversed(neighbour[i:j+1])

        old_len = route_length(current)
        new_len = route_length(neighbour)

        if new_len < old_len or random.random() < math.exp((old_len - new_len) / T):
            current = neighbour
            if new_len < route_length(best):
                best = neighbour[:]

        T *= alpha

    return best, route_length(best)

# ------------------------------------------------------------------
# TSPLIB parser (NODE_COORD_SECTION only)
# ------------------------------------------------------------------
def load_tsplib(path):
    coords = []
    with open(path) as f:
        active = False
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                active = True
                continue
            if line == "EOF":
                break
            if active:
                parts = line.split()
                if len(parts) >= 3 and parts[0].isdigit():
                    coords.append((float(parts[1]), float(parts[2])))
    return coords

# ------------------------------------------------------------------
# Benchmark runner
# ------------------------------------------------------------------
benchmarks = [
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/xqf131.tsp",
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/xqg237.tsp",
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pbk411.tsp",
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pbn423.tsp",
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pka379.tsp",
    r"C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pma343.tsp",
]

summary = {}
for file in benchmarks:
    if not os.path.isfile(file):
        print("Skipped (not found):", file)
        continue

    cities = load_tsplib(file)
    if not cities:
        print("No coordinates in", file)
        continue

    tag = os.path.splitext(os.path.basename(file))[0]
    t0 = time.perf_counter()
    _, dist = sa_tsp(cities)
    t1 = time.perf_counter()

    print(f"Instance : {tag}")
    print(f"Cities   : {len(cities)}")
    print(f"Distance : {dist:.2f}")
    print(f"Time     : {t1-t0:.2f}s")
    print("-" * 25)
    summary[tag] = (dist, t1 - t0)

print("\nSummary")
for tag, (d, t) in summary.items():
    print(f"{tag:12s}  {d:10.2f}  {t:8.2f}s")