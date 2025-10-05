import math, random, time

def euclid(a, b):
    """2-D Euclidean distance between two (x, y) tuples."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def tour_length(route):
    """Total length of a closed TSP route."""
    return sum(euclid(route[i], route[(i + 1) % len(route)]) for i in range(len(route)))

def sa_tsp(locations, T0=1e4, alpha=0.995, Tmin=1e-8, max_iter=1_000_000):
    """
    Simulated-annealing solver for the symmetric TSP.
    2-opt move (reverse a sub-segment) is used as the neighbourhood operator.
    """
    current = locations[:]          # working solution
    best    = current[:]            # best solution seen so far
    n       = len(locations)

    T, step = T0, 0
    while T > Tmin and step < max_iter:
        step += 1

        # create neighbour by 2-opt swap
        i, j = sorted(random.sample(range(n), 2))
        neighbour = current[:]
        neighbour[i:j+1] = reversed(neighbour[i:j+1])

        old_len = tour_length(current)
        new_len = tour_length(neighbour)

        # accept or reject
        if new_len < old_len or random.random() < math.exp((old_len - new_len) / T):
            current = neighbour
            if new_len < tour_length(best):
                best = neighbour[:]

        T *= alpha

    return best, tour_length(best)

# ------------------------------------------------------------------
# 21 tourist spots in Rajasthan
# ------------------------------------------------------------------
rajasthan = [
    (26.9124, 75.7873),   # Jaipur
    (24.5854, 73.6684),   # Udaipur
    (26.2389, 73.1220),   # Jodhpur
    (26.4499, 74.6399),   # Ajmer
    (28.0229, 73.3120),   # Bikaner
    (26.4851, 74.6100),   # Pushkar
    (24.8796, 74.6293),   # Chittorgarh
    (26.9157, 70.9160),   # Jaisalmer
    (24.5921, 72.7014),   # Mount Abu
    (27.6106, 75.1393),   # Sikar
    (27.9852, 76.4577),   # Neemrana
    (25.1638, 75.8644),   # Kota
    (26.0899, 75.7889),   # Tonk
    (25.7410, 71.4280),   # Barmer
    (25.4472, 75.6306),   # Bundi
    (26.1865, 75.0499),   # Bikaner (duplicate name corrected)
    (26.0252, 76.3397),   # Sawai Madhopur
    (27.0977, 77.6616),   # Fatehpur Sikri
    (26.5290, 74.6100),   # Bhilwara
    (27.1500, 75.2520),   # Mandawa
    (23.5867, 76.1632),   # Jhalawar
]

t0 = time.perf_counter()
opt_route, opt_len = sa_tsp(rajasthan)
t1 = time.perf_counter()

print(f"Cities: {len(rajasthan)}")
print(f"Shortest distance found: {opt_len:.2f}")
print(f"Running time: {t1 - t0:.2f} s")