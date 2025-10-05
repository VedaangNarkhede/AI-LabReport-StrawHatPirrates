import string
import random
from itertools import combinations

def get_input(prompt):
    return int(input(prompt))

def generate_random_clauses(num_clauses, vars_per_clause, total_vars):
    lvars = list(string.ascii_lowercase[:total_vars])
    uvars = [v.upper() for v in lvars]
    symbols = lvars + uvars

    all_combs = list(combinations(symbols, vars_per_clause))
    unique_clauses = set()
    tries = 0
    max_tries = 18

    while len(unique_clauses) < num_clauses and tries < max_tries:
        clause = tuple(sorted(random.choice(all_combs)))
        unique_clauses.add(clause)
        tries += 1

    return [list(c) for c in unique_clauses]

def main():
    print("Random Clause Generator")
    num_clauses = get_input("Enter the number of clauses: ")
    vars_per_clause = get_input("Enter the number of variables in a clause: ")
    total_vars = get_input("Enter the total number of variables: ")

    for i, clause in enumerate(generate_random_clauses(num_clauses, vars_per_clause, total_vars), 1):
        print(f"{i}: {clause}")

if __name__ == "__main__":
    main()
