# from collections import deque, namedtuple
from data import edges as edges, hideouts as hideouts
from dijkstra import Graph as Graph


def calculate_paths(hideouts, edges):
    graph = Graph(edges)
    paths = {}
    for i in range(len(hideouts)):
        paths[i] = graph.dijkstra(
            "0-0", str(hideouts[i][0]) + "-" + str(hideouts[i][1])
        )
    return paths


paths = calculate_paths(hideouts, edges)

print(edges)

def calculate_distances(edges, paths):
    distances = []
    for path in paths:
        current_distance = 0
        house_counter = 1
        while house_counter < len(paths[path]) - 1:
            edge_counter = 0
            until = 0
            for edge in edges:
                if (
                    paths[path][len(paths[path]) - 2] == edge[0]
                    and paths[path][len(paths[path]) - 1] == edge[1]
                ):
                    until = edges.index(edge) + 1
            while edge_counter < until:
                if (
                    edges[edge_counter][0] == paths[path][house_counter]
                    and edges[edge_counter][1] == paths[path][house_counter + 1]
                ):
                    current_distance += edges[edge_counter][2]
                edge_counter += 1
            house_counter += 1
        current_distance += edges[until][2]
        distances.append(current_distance)
    return distances


distances = calculate_distances(edges, paths)


def find_shortest_path(distances, paths):
    shortest = distances[0]
    for i in distances:
        if i < shortest:
            shortest = i
    index_of_shortest = distances.index(shortest)
    return shortest, paths[index_of_shortest]


shortest_path = find_shortest_path(distances, paths)


def print_shortest_path(shortest_path):
    print(
        f"A legrövidebb út hossza: {shortest_path[0]}\n"
        f"Az útvonal: {[coordinate for coordinate in shortest_path[1]]}"
    )


def print_hideouts(hideouts):
    print(f"A rejtekhelyek koordinátái:\n" f"{hideouts}")


print_hideouts(hideouts)
print_shortest_path(shortest_path)
