#!/usr/bin/python
# -*- coding: utf-8 -*-

import array
import os
import array
import sys
import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def total_length(solution, points):
    nodeCount = len(points)
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj


def find_nearest(node1, nodes, points):
    costs = [1.0/(1+length(points[nodes[node1]], points[nodes[i]]))
             for i in range(len(nodes))]
    costs[node1] = 0
    while True:
        n = random.choices(nodes, weights=costs)[0]
        #print(n)
        if node1 != n:
            break
    # n = min(range(len(points)), key=costs.__getitem__)
    # print(node1, n)
    return n


def solve1(nodes, points, title):
    nodeCount = len(points)
    cost = total_length(nodes, points)

    max_tries = 10 if nodeCount < 1000 else 1

    tries = 0
    while tries < max_tries:
        for node in range(len(nodes)):
            node1 = node
            node2 = find_nearest(node1, nodes, points)

            new_nodes = list(nodes)
            new_nodes[node1], new_nodes[node2] = new_nodes[node2], new_nodes[node1]

            new_cost = total_length(new_nodes, points)
            #print(node, len(nodes))

            # if node%10==0:
            #     print("{} tries={} node->{}/{} ({}%)\r".format(title, tries, node, nodeCount, 100*node//len(nodes)), end="", file=sys.stderr)

            if new_cost < cost:
                nodes = new_nodes
                cost = new_cost
                tries = 0
        tries += 1
        #os.system('title '+title+' cost='+str(cost)+' tries='+str(tries))

    return cost, nodes


def solve(points, title):
    nodeCount = len(points)
    nodes = list(range(0, len(points)))
    random.shuffle(nodes)
    best_cost, best_nodes = solve1(nodes, points, title)

    if len(points) < 1000:
        max_tries = 100
        for i in range(max_tries):
            # random.shuffle(nodes)
            cost, nodes = solve1(nodes, points, title +
                                ' best_cost=' + str(best_cost) + ' solver_iter='+str(i))
            if cost < best_cost:
                best_cost = cost
                best_nodes = nodes
                # print(cost)

            if i % 20 == 0:
                for k in range(10):
                    node1 = random.randrange(0, nodeCount)
                    node2 = random.randrange(node1, node1+nodeCount) % nodeCount
                    nodes[node1], nodes[node2] = nodes[node2], nodes[node1]

    return best_cost, best_nodes


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
    obj, solution = solve(points, 'start')

    if len(points) < 500:
        max_tries = 10
    elif len(points) < 1000:
        max_tries = 5
    else:
        max_tries = 1

    for i in range(max_tries):
        title = 'best_tries={} best_solution={}'.format(i, obj)
        obj1, solution1 = solve(points, title)
        if obj1 < obj:
            obj = obj1
            solution = solution1

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
