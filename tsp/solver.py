#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import functools
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

@functools.cache
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def calc_length(solution, points):
    nodeCount = len(points)
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def random_swap(nodes, points):
    i = random.randrange(0, len(nodes) - 1)
    # while True:
    #     j = random.randrange(0, len(nodes))
    #     if j != i:
    #         break

    # i = random.randrange(0, len(best_nodes))
    j = random.randrange(i+1, len(nodes))

    # choices = range(i+1, len(nodes))
    # weights = [length(points[nodes[i]], points[nodes[j]]) for j in choices]
    # j = random.choices(choices, weights=weights)[0]

    new_nodes = list(nodes)
    new_nodes[i], new_nodes[j] = nodes[j], nodes[i]

    return new_nodes

def solve(points):
    nodeCount = len(points)
    best_nodes = list(range(0, nodeCount))
    best_cost = calc_length(best_nodes, points)

    max_depth = 5000

    n = 0
    while True:
        new_nodes = list(best_nodes)
        for k in range(0,10):
            i = random.randrange(0, len(new_nodes))
            j = random.randrange(0, len(new_nodes))
            new_nodes[i], new_nodes[j] = new_nodes[j], new_nodes[i]

            new_cost = calc_length(new_nodes, points)
            if new_cost < best_cost:
                best_cost = new_cost
                best_nodes = new_nodes
                # print(best_cost)
                n=0
                break
        new_nodes = list(best_nodes)
        n+=1
        if n==int(max_depth//3) or n==int(max_depth//3)*2:
            # print("split")
            l = len(new_nodes)//3
            i = random.randrange(0, len(new_nodes)-l)
            j = random.randrange(0, l)
            split=new_nodes[i:i+j]
            del new_nodes[i:i+j]
            split=split+new_nodes
            new_nodes=split
            new_cost = calc_length(new_nodes, points)
            if new_cost < best_cost:
                best_cost = new_cost
                best_nodes = new_nodes
                # print(best_cost)
                n=0
        if n>max_depth:
            break

    return best_cost, best_nodes


def solve_multiple(points):
    best_best_cost, best_best_nodes = solve(points)
    for tries in range(0, 5):
        best_cost, best_nodes = solve(points)
        if best_cost < best_best_cost:
            best_best_cost = best_cost
            best_best_nodes = best_nodes
            # print(best_best_cost)
    return best_best_cost, best_best_nodes

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    obj, solution = solve_multiple(points)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

