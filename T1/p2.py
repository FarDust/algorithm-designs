from queue import PriorityQueue  # https://docs.python.org/3/library/queue.html
from copy import copy

# Basado en la implementación de kruskal:
# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/


class Connection:
    """Class for keeping track of Connections info."""

    def __init__(self, connections, cost, real_cost):
        self.connections = connections
        self.cost = cost
        self.real_cost = real_cost

    def __lt__(self, value):
        return self.cost < value.cost

    def __eq__(self, value):
        return self.connections == value.connections

    def __repr__(self):
        return f"{self.connections[0]} -> {self.connections[1]}"


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


def kruskal(edges, total_nodes, banned=set(), offset=0):
    final_edges = []
    final_sum = 0
    backup = list()
    banned_vertexes = set()
    banned_vertexes = banned_vertexes | banned
    nodes = [node for node in range(total_nodes)]
    ranks = [0] * total_nodes

    edge_count = 0
    while edge_count < total_nodes - 1 - offset:

        cable = edges.get()
        backup.append(cable)
        x_i, x_j = cable.connections
        if x_j in banned_vertexes or x_i in banned_vertexes:
            continue
        spot_a = find(nodes, nodes[x_i])
        spot_b = find(nodes, nodes[x_j])
        if (
            spot_a != spot_b
            and not (x_i in banned_vertexes)
        ):
            edge_count += 1
            final_sum += cable.real_cost
            final_edges.append(cable)
            union(nodes, ranks, spot_a, spot_b)
            if x_j != total_nodes - 1:
                banned_vertexes.add(x_i)
            
    for cable in backup:
        edges.put(cable)
    return final_edges, edges, final_sum


def create_graph(town_quantity, provider_cost, cable_unit_cost, house_qty):
    connections = PriorityQueue()
    extra_connections = list()
    for provider_index in range(town_quantity):
        for town_index in range(town_quantity):
            estimated_cost = (
                abs((town_index + 1) - (provider_index + 1)) * cable_unit_cost
            )
            new_connection = Connection(
                connections=(town_index, provider_index + town_quantity),
                cost=estimated_cost / int(house_qty[town_index]),
                real_cost=estimated_cost
            )
            connections.put(new_connection)
        extra_connection = Connection(
            connections=(provider_index + town_quantity, 2 * town_quantity),
            cost=provider_cost / int(house_qty[provider_index]),
            real_cost=provider_cost
        )
        connections.put(extra_connection)
        extra_connections.append(extra_connection)
    return connections, extra_connections


def calc_optimum_internet_provider(
    town_quantity, provider_cost, cable_unit_cost, house_qty
):
    optimum_internet_provider_cost = [0] * (town_quantity + 1)

    connections, extra_connections = create_graph(
        town_quantity, provider_cost, cable_unit_cost, house_qty
    )
    banned = set()
    for i in range(town_quantity - 1):
        banned.add(extra_connections[i].connections[0])
        mst, connections, final_sum = kruskal(
            copy(connections),
            2 * town_quantity + 1,
            banned=banned,
            offset=len(banned)
        )
        print(mst, final_sum)

    return "".join(optimum_internet_provider_cost)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        town_quantity, provider_cost, cable_unit_cost = 6, 9, 1
        house_qty = 9, 11, 3, 2, 7, 6
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
