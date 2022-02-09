rounds = 3
graph = {"A": ["C", "D", "E"], "B": ["D", "E"], "C": [], "D": [], "E": []}
hub = {x: 1 for x in graph}
auth = {x: 0 for x in graph}
for round in range(rounds):
    print()
    print()
    print("Round {} Starting hub scores".format(round))
    print(hub)
    print("Round {} Starting auth scores".format(round))
    print(auth)
    for node, dests in graph.items():
        for dest in dests:
            auth[dest] += hub[node]
    print("Round {} UnNorm auth scores".format(round))
    print(auth)
    total_auth = sum(auth.values())
    for node in auth.keys():
        auth[node] /= total_auth
    for node, dests in graph.items():
        hub[node] = 0
        for dest in dests:
            hub[node] += auth[dest]
    print("Round {} UnNorm hub scores".format(round))
    print(hub)
    total_hub = sum(hub.values())
    for node in hub.keys():
        hub[node] /= total_hub
    print("Round {} Ending hub scores".format(round))
    print(hub)
    print("Round {} Ending auth scores".format(round))
    print(auth)
