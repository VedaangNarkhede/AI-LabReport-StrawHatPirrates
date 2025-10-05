import string
import random
from itertools import combinations

def ask_int(prompt):
    return int(input(prompt))

def make_formulas(num_clauses, lits_per_clause, total_vars, max_attempts=100):
    letters = list(string.ascii_lowercase[:total_vars])
    letters_up = [c.upper() for c in letters]
    symbols = letters + letters_up
    all_combs = list(combinations(symbols, lits_per_clause))
    if not all_combs:
        return []
    take = min(num_clauses, len(all_combs))
    sampled = random.sample(all_combs, take)
    return [list(c) for c in sampled]

def make_assignment(symbols):
    vals = random.choices([0, 1], k=len(symbols))
    return dict(zip(symbols, vals))

def eval_clause(clause, assignment):
    return 1 if any(assignment.get(lit, 0) for lit in clause) else 0

def evlfml(formula, assignment):
    return sum(eval_clause(clause, assignment) for clause in formula)

def hill_climb(formula, start_assignment, max_iters=1000):
    current = start_assignment.copy()
    current_score = evlfml(formula, current)
    steps = 0
    while steps < max_iters:
        steps += 1
        improved = False
        best_neighbor = None
        best_score = current_score
        for var in list(current.keys()):
            neighbor = current.copy()
            neighbor[var] = 1 - neighbor[var]
            score = evlfml(formula, neighbor)
            if score > best_score:
                best_score = score
                best_neighbor = neighbor
        if best_neighbor is None:
            break
        current = best_neighbor
        current_score = best_score
        if current_score == len(formula):
            break
    return current, current_score, steps

def beam_search(formula, start_assignment, beam_width=3, max_iters=1000):
    start_score = evlfml(formula, start_assignment)
    beam = [(start_assignment.copy(), start_score)]
    steps = 0
    if start_score == len(formula):
        return start_assignment.copy(), steps
    while steps < max_iters:
        steps += 1
        candidates = []
        for asn, sc in beam:
            for var in asn.keys():
                na = asn.copy()
                na[var] = 1 - na[var]
                s = evlfml(formula, na)
                candidates.append((na, s))
                if s == len(formula):
                    return na, steps
        candidates.sort(key=lambda x: x[1], reverse=True)
        beam = candidates[:beam_width]
        if not beam:
            break
    return beam[0][0] if beam else start_assignment.copy(), steps

def variable_neighborhood_descent(formula, start_assignment, max_k=4, max_iters=1000):
    current = start_assignment.copy()
    current_score = evlfml(formula, current)
    steps = 0
    symbols = list(current.keys())
    k = 1
    while steps < max_iters and k <= max_k:
        improved = False
        combos = list(combinations(symbols, k))
        if len(combos) > 200:
            combos = random.sample(combos, 200)
        for subset in combos:
            steps += 1
            neighbor = current.copy()
            for s in subset:
                neighbor[s] = 1 - neighbor[s]
            sscore = evlfml(formula, neighbor)
            if sscore > current_score:
                current = neighbor
                current_score = sscore
                improved = True
                break
            if steps >= max_iters:
                break
        if improved:
            k = 1
            if current_score == len(formula):
                break
        else:
            k += 1
    return current, current_score, steps

def run():
    num_clauses = int(input("Formula (number of clauses): "))
    lits_per_clause = int(input("Variable per formula: "))
    total_vars = int(input("Total var: "))
    formulas = make_formulas(num_clauses, lits_per_clause, total_vars)
    symbols = list(string.ascii_lowercase[:total_vars]) + [c.upper() for c in string.ascii_lowercase[:total_vars]]
    for i, formula in enumerate(formulas, 1):
        print(f"\n{i}: {formula}")
        init_asn = make_assignment(symbols)
        init_score = evlfml(formula, init_asn)
        hc_asn, hc_score, hc_steps = hill_climb(formula, init_asn, max_iters=1000)
        bs_asn, bs_steps = beam_search(formula, init_asn, beam_width=3, max_iters=1000)
        vnd_asn, vnd_score, vnd_steps = variable_neighborhood_descent(formula, init_asn, max_k=4, max_iters=1000)
        print(f"Init: S={init_score}")
        print(f"HC: S={hc_score}, Steps={hc_steps}")
        print(f"BS: S={evlfml(formula, bs_asn)}, Steps={bs_steps}")
        print(f"VND: S={vnd_score}, Steps={vnd_steps}")

if __name__ == "__main__":
    run()
