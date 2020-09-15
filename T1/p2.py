from queue import PriorityQueue  # https://docs.python.org/3/library/queue.html

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
        return frozenset(self.connections) == frozenset(value.connections)


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


def kruskal(edges, total_nodes):
    final_count = 0
    edges_map = set()
    nodes = [node for node in range(total_nodes)]
    ranks = [0] * total_nodes

    edge_count = 0
    while edge_count < total_nodes - 1:

        cable = edges.get()
        if cable.connections in edges_map:
            continue
        else:
            edges_map.add(cable.connections)
        x_i, x_j = cable.connections
        spot_a = find(nodes, nodes[x_i])
        spot_b = find(nodes, nodes[x_j])
        if spot_a != spot_b:
            edge_count += 1
            final_count += cable.cost
            union(nodes, ranks, spot_a, spot_b)
    return final_count


def create_graph(town_quantity, provider_cost, cable_unit_cost, house_qty):
    connections = PriorityQueue()

    for provider_index in range(town_quantity - 1):
        for town_index in range(town_quantity - 1):
            new_connection = Connection(
                connections=frozenset({provider_index, town_index}),
                cost=(
                    ((town_index + 1) - (provider_index + 1)) * cable_unit_cost
                )
                / int(house_qty[town_index]),
            )
            connections.put(new_connection)
        extra_connection = Connection(
            connections=frozenset({provider_index, town_quantity}),
            cost=provider_cost / int(house_qty[provider_index]),
        )
        connections.put(extra_connection)
    return connections


def calc_optimum_internet_provider(
    town_quantity, provider_cost, cable_unit_cost, house_qty
):
    optimum_internet_provider_cost = [0 for i in range(town_quantity + 1)]

    connections = create_graph(
        town_quantity, provider_cost, cable_unit_cost, house_qty
    )

    kruskal(connections, town_quantity + 1)

    return "".join(optimum_internet_provider_cost)


if __name__ == "__main__":
    town_quantity, provider_cost, cable_unit_cost = input().split(" ")
    house_qty = input().split(" ")
    print(
        calc_optimum_internet_provider(
            town_quantity, provider_cost, cable_unit_cost, house_qty
        )
    )
