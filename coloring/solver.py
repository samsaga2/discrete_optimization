#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import random

def random_resolve(node_colors):
    # sort by colors
    sorted_nodes = range(len(node_colors))
    sorted_nodes = sorted(sorted_nodes, key=lambda n: len(node_colors[n]))
    sorted_nodes = list(filter(lambda n: len(node_colors[n]) > 1, sorted_nodes))
    if not sorted_nodes:
        return node_colors, None
    
    # get one random color from the first node
    node = sorted_nodes[0]
    node_colors[node] = set([list(node_colors[node])[0]])
    # print("random", node, node_colors[node])
    return (node_colors, node)

def propagate(node_colors, edges, node):
    colors = node_colors[node]
    for edge in edges[node]:
        new_colors = node_colors[edge] - colors
        if node_colors[edge] != new_colors:
            # print("propagate", edge, node_colors[edge], "->", new_colors)
            node_colors[edge] = new_colors
            if node_colors[edge] == None:
                raise "Unresolved"
            if node_colors[edge] == 1:
                propagate(node_colors, edges, edge)

    return node_colors

def solver(node_count, edges, num_colors):
    # create a dict of nodes with their set of colors
    all_colors = set(range(num_colors))

    node_colors = []
    for node in range(node_count):
        node_colors.append(set(all_colors))

    # resolve
    # print(node_colors)
    while True:
        node_colors, node = random_resolve(node_colors)
        if node is None:
            break
        node_colors = propagate(node_colors, edges, node)
        # print("state", node_colors)

    if not is_solved(node_count, edges, node_colors):
        return None

    # read the solution
    solution = []
    for color in node_colors:
        solution.append(list(color)[0])
    return solution

def is_solved(node_count, edges, node_colors):
    for node in range(node_count):
        color = list(node_colors[node])
        if len(color) != 1:
            return False
        for edge in edges[node]:
            edge_colors = list(node_colors[edge])
            if len(edge_colors) != 1 or color[0] == edge_colors[0]:
                # print("failed", node, edge, color, edge_colors)
                return False
    return True

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = defaultdict(lambda: [])
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        node1 = int(parts[0])
        node2 = int(parts[1])
        edges[node1].append(node2)
        edges[node2].append(node1)
    solution = None
    while not solution:
        best_solution  = None
        max_best = None
        for i in range(50):
            solution = solver(node_count, edges, 1000)
            max_solution = max(solution)
            if not best_solution or max_best > max_solution or max_best == max_solution and sum(best_solution) < sum(solution):
                best_solution = solution
                max_best = max(best_solution)

    if solution is None:
        # print("Unresolved")
        solution = list(range(0, node_count))
        return None

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

