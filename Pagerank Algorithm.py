rounds = 5
graph = {"b0": ["b1", "b2"], "b1": [], "b2": []}
delta = 0.75
scores = {x: 1 for x in graph}
for round in range(rounds):
    print()
    print()
    print("R before iter", round)
    print(scores)
    scores_new = {x: 1 - delta for x in graph}
    print("R' before iter", round)
    print(scores_new)
    for src in graph:
        for dst in graph[src]:
            print(
                "R'[{}] = {} + ({} * {}) / {}".format(
                    dst, scores_new[dst], delta, scores[src], len(graph[src])
                )
            )
            scores_new[dst] += delta * scores[src] / len(graph[src])
    S = len(scores)
    for i, v in scores_new.items():
        S -= v
    print("S = {} -".format(len(scores)), scores_new.values())
    for k in scores.keys():
        scores[k] = scores_new[k] + (S / len(scores))
    print("R' after iter", round)
    print(scores_new)
    print("R after iter", round)
    print(scores)
