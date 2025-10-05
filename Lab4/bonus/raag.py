import random
from typing import List
from music21 import stream, note, midi

RAAG_ASC = ['C', 'C#', 'E', 'F', 'G', 'G#', 'B']
RAAG_DESC = ['C', 'B', 'G#', 'G', 'F', 'E', 'C#']

def random_melody(length: int) -> List[str]:
    melody = []
    for _ in range(length):
        scale = RAAG_ASC if random.random() > 0.5 else RAAG_DESC
        melody.append(random.choice(scale))
    return melody

def score_melody(melody: List[str]) -> int:
    score = 0
    la, ld = len(RAAG_ASC), len(RAAG_DESC)

    for i in range(len(melody) - ld + 1):
        if melody[i:i + ld] == RAAG_DESC:
            score += 10
        for j in range(2, ld):
            if melody[i:i + j] == RAAG_DESC[:j]:
                score += j

    for i in range(len(melody) - la + 1):
        if melody[i:i + la] == RAAG_ASC:
            score += 10
        for j in range(2, la):
            if melody[i:i + j] == RAAG_ASC[:j]:
                score += j

    return score

def crossover(parent1: List[str], parent2: List[str]) -> (List[str], List[str]):
    if len(parent1) < 2:
        return parent1[:], parent2[:]
    split = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2

def mutate(melody: List[str], mutation_rate: float) -> List[str]:
    for i in range(len(melody)):
        if random.random() < mutation_rate:
            melody[i] = random.choice(RAAG_ASC if random.random() > 0.5 else RAAG_DESC)
    return melody

def run_genetic_algorithm(
    generations: int = 1000,
    population_size: int = 100,
    mutation_rate: float = 0.1,
    melody_length: int = 64
) -> List[str]:
    population = [random_melody(melody_length) for _ in range(population_size)]

    for _ in range(generations):
        scored = [(m, score_melody(m)) for m in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        best_melody = scored[0][0]
        selected = [m for m, _ in scored[: population_size // 2]]

        next_gen = []
        while len(next_gen) < population_size:
            p1, p2 = random.sample(selected, 2)
            c1, c2 = crossover(p1, p2)
            next_gen.append(mutate(c1, mutation_rate))
            if len(next_gen) < population_size:
                next_gen.append(mutate(c2, mutation_rate))

        population = next_gen

    return best_melody

def melody_to_stream(melody: List[str]) -> stream.Stream:
    s = stream.Stream()
    for pitch in melody:
        s.append(note.Note(pitch))
    return s

if __name__ == "__main__":
    random.seed()  # remove or set an int for reproducible runs
    best = run_genetic_algorithm(
        generations=500,
        population_size=80,
        mutation_rate=0.12,
        melody_length=64
    )

    s = melody_to_stream(best)
    mf = midi.translate.music21ObjectToMidiFile(s)
    mf.open("Lab4/bonus/raag.mid", "wb")
    mf.write()
    mf.close()

    print("Generated melody saved to raag.mid")
