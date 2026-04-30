import random


def get_probabilities(player):
    pa = max(player["PA"], 1)

    return {
        "1B": player["1B"] / pa,
        "2B": player["2B"] / pa,
        "3B": player["3B"] / pa,
        "HR": player["HR"] / pa,
        "BB": player["BB"] / pa,
        "OUT": player["OUT"] / pa,
    }


def simulate_at_bat(player):
    probs = get_probabilities(player)
    r = random.random()
    cumulative = 0

    for outcome, p in probs.items():
        cumulative += p
        if r <= cumulative:
            return outcome

    return "OUT"


def advance_runners(bases, outcome):
    runs = 0

    if outcome == "OUT":
        return bases, runs

    if outcome == "BB" or outcome == "1B":
        if bases[2]:
            runs += 1
        bases = [True, bases[0], bases[1]]

    elif outcome == "2B":
        runs += bases[2] + bases[1]
        bases = [False, True, bases[0]]

    elif outcome == "3B":
        runs += sum(bases)
        bases = [False, False, True]

    elif outcome == "HR":
        runs += sum(bases) + 1
        bases = [False, False, False]

    return bases, runs


def simulate_inning(lineup, start_index):
    outs = 0
    bases = [False, False, False]
    runs = 0
    i = start_index

    while outs < 3:
        player = lineup[i % len(lineup)]
        outcome = simulate_at_bat(player)

        if outcome == "OUT":
            outs += 1
        else:
            bases, new_runs = advance_runners(bases, outcome)
            runs += new_runs

        i += 1

    return runs, i % len(lineup)


def simulate_game(lineup, innings=7):
    total_runs = 0
    batter_index = 0

    for _ in range(innings):
        runs, batter_index = simulate_inning(lineup, batter_index)
        total_runs += runs

    return total_runs


def simulate_many(lineup, sims=1000):
    results = []

    for _ in range(sims):
        runs = simulate_game(lineup)
        results.append(runs)

    results.sort()

    return {
        "avg_runs": sum(results) / len(results),
        "min_runs": results[0],
        "max_runs": results[-1],
        "median_runs": results[len(results)//2],
    }