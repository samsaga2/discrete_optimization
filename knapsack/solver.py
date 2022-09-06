#!/usr/bin/pypy3
# -*- coding: utf-8 -*-

from collections import namedtuple
import time

TIMEOUT_SECONDS = 60*60

Item = namedtuple("Item", ['index', 'value', 'weight'])
Node = namedtuple("Node", ['depth', 'taken', 'room', 'value'])

best_found_node = None
best_found_value = None
start_time = None

def calc_estimation_value(items, capacity):
    "Calculate the value of all the items"
    value = 0
    weight = 0
    for item in reversed(items):
        if weight+item.weight <= capacity:
            value += item.value
            weight += item.weight
        else:
            remaining = capacity - weight
            value += (item.value / item.weight) * remaining
            break
    return value

def traverse_graph(node, items):
    """Traverse the whole graph executing the indicated function at every node.
If the eval function returns False it will not evaluate the child nodes."""
    global best_found_node
    global best_found_value
    global start_time

    if time.time() - start_time > TIMEOUT_SECONDS:
        raise Exception('Timeout')

    # traverse childs
    if node.depth < len(items):
        node_item = items[node.depth]

        # left child
        left_room = node.room-node_item.weight
        if left_room >= 0:
            left_node = Node(node.depth+1, node.taken+[1], left_room, node.value+node_item.value)
            if best_found_value == None or calc_estimation_value(items[node.depth:], left_node.room) + left_node.value > best_found_value:
                traverse_graph(left_node, items)

        # right child
        right_node = Node(node.depth+1, node.taken+[0], node.room, node.value)
        if best_found_value == None or calc_estimation_value(items[node.depth:], right_node.room) + right_node.value > best_found_value:
            traverse_graph(right_node, items)
    elif best_found_value == None or best_found_value < node.value:
        # final node, check for best value
        best_found_node = node
        best_found_value = node.value

def solve_algorithm(items, capacity):
    "Solve using evaluation of the whole graph but pruning nodes"
    global best_found_node
    global best_found_value
    global start_time
    
    best_found_node = None
    best_found_value = None
    start_time = time.time()

    # sort by density to optimize
    sorted_indices = sorted(range(0, len(items)), key=lambda i: items[i].value/items[i].weight)
    sorted_items = [items[i] for i in sorted_indices]

    # resolve
    root_node = Node(0, [], capacity, 0)
    try:
        traverse_graph(root_node, sorted_items)
    except:
        # timeout
        pass
    
    # solution
    taken = [0]*len(items)
    for i in range(len(items)):
        if best_found_node.taken[i]:
            taken[sorted_items[i].index] = 1
    return best_found_value, taken

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # try to solve the knapsack problem
    value, taken = solve_algorithm(items, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

