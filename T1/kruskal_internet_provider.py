from queue import PriorityQueue  # https://docs.python.org/3/library/queue.html
from math import inf

# Basado en la implementación de kruskal:
# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/


class Connection:
    """Class for keeping track of Connections info."""

    def __init__(self, connections, cost):
        self.connections = connections
        self.cost = cost

    def __lt__(self, value):
        return self.cost < value.cost

    def __eq__(self, value):
        return self.connections == value.connections

    def __repr__(self):
        return f"{self.connections[0]} -{self.cost}-> {self.connections[1]}"


def find(parent, node):
    if parent[node] == node:
        return node
    new_parent = find(parent, parent[node])
    parent[node] = new_parent
    return new_parent


def union(parent, rank, x_tree_set, y_tree_set):
    x_tree_root = find(parent, x_tree_set)
    y_tree_root = find(parent, y_tree_set)

    if rank[x_tree_root] < rank[x_tree_root]:
        parent[x_tree_root] = y_tree_root
    elif rank[x_tree_root] > rank[y_tree_root]:
        parent[y_tree_root] = x_tree_root
    else:
        parent[y_tree_root] = x_tree_root
        rank[x_tree_root] += 1


def kruskal(edges, total_nodes, towns, provider_cost, banned=set(), offset=0):
    final_edges = []
    backup = PriorityQueue()
    final_sum = 0
    nodes = [node for node in range(total_nodes)]
    ranks = [0] * total_nodes

    edge_count = 0
    while edge_count < total_nodes - 1 - offset:

        cable = edges.get()
        backup.put(cable)
        x_i, x_j = cable.connections
        if x_j in banned or x_i in banned:
            continue
        spot_a = find(nodes, nodes[x_i])
        spot_b = find(nodes, nodes[x_j])
        if spot_a != spot_b:
            final_edges.append(cable)
            edge_count += 1
            final_sum += provider_cost if cable.cost == 0 else cable.cost
            union(nodes, ranks, spot_a, spot_b)

    while not (backup.empty()):
        cable = backup.get()
        edges.put(cable)
    return final_edges, edges, final_sum


def create_graph(town_quantity, provider_cost, cable_unit_cost, house_qty):
    connections = PriorityQueue()
    for provider_index in range(town_quantity):
        for town_index in range(town_quantity):
            estimated_cost = (
                abs((town_index + 1) - (provider_index + 1)) * cable_unit_cost
            )
            new_connection = Connection(
                connections=(town_index, provider_index + town_quantity),
                cost=estimated_cost * house_qty[town_index],
            )
            connections.put(new_connection)
        extra_connection = Connection(
            connections=(provider_index + town_quantity, 2 * town_quantity),
            cost=0,
        )
        connections.put(extra_connection)
    return connections


def calc_optimum_internet_provider(
    town_quantity, provider_cost, cable_unit_cost, house_qty
):
    optimum_internet_provider_cost = [inf] * (town_quantity)
    optimum_internet_provider_cost[-1] = town_quantity*provider_cost

    connections = create_graph(
        town_quantity, provider_cost, cable_unit_cost, house_qty
    )
    all_options = set([town_quantity + town for town in range(town_quantity)])

    solve(
        all_options,
        town_quantity,
        provider_cost,
        connections,
        optimum_internet_provider_cost,
    )

    return " ".join((str(i) for i in optimum_internet_provider_cost))


def solve(
    all_options,
    town_quantity,
    provider_cost,
    connections,
    optimum_internet_provider_cost,
    banned=set(),
    viewed=set(),
):
    if len(banned) == 1:
        return
    if frozenset(banned) in viewed:
        return
    if banned == set():
        banned = all_options

    banned_group = list()
    for option in banned:
        to_banned = banned - {option}
        if frozenset(to_banned) in viewed:
            continue
        mst, connections, final_sum = kruskal(
            connections,
            2 * town_quantity + 1,
            town_quantity,
            provider_cost,
            banned=to_banned,
            offset=len(to_banned),
        )
        viewed_towns = set()
        final_solution = list()
        for connection in mst:
            x_i, x_j = connection.connections
            if not (x_i in viewed_towns) and x_j != 2 * town_quantity:
                viewed_towns.add(x_i)
                final_solution.append(connection)
            else:
                final_sum -= (
                    provider_cost if connection.cost == 0 else connection.cost
                )
        test_index = town_quantity - len(to_banned) - 1
        if final_sum < optimum_internet_provider_cost[test_index]:
            optimum_internet_provider_cost[test_index] = final_sum
        else:
            continue
        print(final_solution, final_sum, to_banned)
        viewed.add(frozenset(banned))
        banned_group.append((final_sum, set() | to_banned))
    banned_group.sort()
    for final_sum, group in banned_group:
        solve(
            all_options,
            town_quantity,
            provider_cost,
            connections,
            optimum_internet_provider_cost,
            group,
        )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        town_quantity, provider_cost, cable_unit_cost = 5, 7, 1
        house_qty = 1, 5, 3, 2, 4
    else:
        town_quantity, provider_cost, cable_unit_cost = (
            input().strip("\n").split(" ")
        )
        house_qty = [int(town) for town in input().strip("\n").split(" ")]
    print(
        calc_optimum_internet_provider(
            int(town_quantity),
            int(provider_cost),
            int(cable_unit_cost),
            house_qty,
        )
    )
