import math
import random
import time

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)

def td(tour):
    return sum(distance(tour[i], tour[(i+1) % len(tour)]) for i in range(len(tour)))

def grc(num_cities, max_coordinate):
    return [(random.randint(0, max_coordinate), random.randint(0, max_coordinate)) for _ in range(num_cities)]

def nearneighbour(cities):
    unvisited=cities[1:]
    tour=[cities[0]]
    while unvisited:
        nearest = min(unvisited, key=lambda city: distance(tour[-1], city))
        tour.append(nearest)
        unvisited.remove(nearest)
    return tour

def opt(tour):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1: continue
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                if td(new_tour) < td(tour):
                    tour = new_tour
                    improved = True
    return tour

def tsp(cities):
    start_time = time.time()
    
    initial_tour = nearneighbour(cities)
    optimized_tour = opt(initial_tour)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return optimized_tour, td(optimized_tour), execution_time

num_cities = 20
max_coordinate = 100
    
cities = grc(num_cities, max_coordinate)
    
tour,distance,time = tsp(cities)
    
print(f"Number of cities: {num_cities}")
print(f"Best tour distance: {distance:.2f}")
print(f"Execution time: {time:.4f} seconds")
print("Best tour:")
for city in tour:
    print(f"({city[0]}, {city[1]})")