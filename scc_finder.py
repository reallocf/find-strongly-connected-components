#!/usr/bin/env python
from sys import argv

def parse(inputText):
    nodes = set()
    with open(inputText, "r") as f:
        graph = {}
        for row in f.read().split('\n'):
            if row:
                row = row.split(' ')
                if row[0] not in graph:
                    graph[row[0]] = set([row[1]])
                    nodes.add(row[0])
                else:
                    graph[row[0]].add(row[1])
    return nodes, graph

def printGraph(graph):
    for key, val in graph.items():
        print(key + ": " + str(val))

def reverse(graph):
    revGraph = {}
    for key, values in graph.items():
        for val in values:
            if val not in revGraph:
                revGraph[val] = set([key])
            else:
                revGraph[val].add(key)
    return revGraph

def first_dfs(graph, unvisitedNodes):
    order = []
    orderSet = set()
    while unvisitedNodes:
        stack = [unvisitedNodes.pop()]
        unvisitedNodes.add(stack[0])
        while stack:
            node = stack[-1]
            if node in graph and node in unvisitedNodes:
                unvisitedNodes.remove(node)
                unvisitedNeighbors = set([elem for elem in graph[node] if elem in unvisitedNodes])
                stack.extend(unvisitedNeighbors)
                if not unvisitedNeighbors:
                    if node not in orderSet:
                        order.append(stack.pop())
                        orderSet.add(node)
                    else:
                        stack.pop()
            else:
                try:
                    unvisitedNodes.remove(node)
                except:
                    pass
                if node not in orderSet:
                    order.append(stack.pop())
                    orderSet.add(node)
                else:
                    stack.pop()
    return order

def second_dfs(graph, order, unvisitedNodes):
    sccSizes = []
    while unvisitedNodes:
        stack = [order.pop()]
        count = 0
        while stack:
            node = stack[-1]
            if node in graph and node in unvisitedNodes:
                count += 1
                unvisitedNodes.remove(node)
                unvisitedNeighbors = set([elem for elem in graph[node] if elem in unvisitedNodes])
                stack.extend(unvisitedNeighbors)
                if not unvisitedNeighbors:
                    stack.pop()
            else:
                try:
                    unvisitedNodes.remove(node)
                except:
                    pass
                stack.pop()
        if count != 0:
            sccSizes.append(count)
    return sccSizes

if __name__ == "__main__":
    if len(argv) != 2:
        print("usage ./scc_finder.py graph.txt")
        exit()
    nodes, graph = parse(argv[1])
    print("Done parsing")
    revGraph = reverse(graph)
    print("Done building reverse graph")
    order = first_dfs(revGraph, set(nodes))
    print("Done with first dfs")
    sccSizes = second_dfs(graph, order, nodes)
    print("Done with second dfs")
    print("Largest SCC Sizes: " + str(sorted(sccSizes, reverse=True)[:10]))
