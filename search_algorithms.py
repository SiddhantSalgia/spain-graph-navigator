from collections import deque
import numpy as np
import heapq
class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self._heap)[1]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self._heap[0][1]

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

def heuristic(u, v):
  # Heuristic is taken as a Euclidean distance
  # u -> x1,y1     v -> x2,y2
  return np.sqrt(sum((p - q)**2 for p, q in zip(u, v)))

def uniform_cost_search_path(graph, start, destination):
    print(f"Evaluating the path from {start} to {destination} Using UCS!!\n")
    frontier = PriorityQueue()

    # Store tuple of (vertex,path,distance) in the priority queue where the priority is the cost to reach the vertex.
    frontier.push((start,[start],0),0)

    #Dictionary to store the minimum distance found so far to reach each node
    visited_distance = {start: 0}

    #Counter for iteration
    index = 0

    while not frontier.is_empty():
        print("\n")
        index += 1
        #Information about the node being explored.
        print(f"Iteration: {index}")
        if not frontier.is_empty():
            print(f"Frontier : {frontier.peek()}")
        else:
            print("Frontier is empty!!")
        # Get the element with the lowest cost from the priority queue.
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        # if the cost of the current path is greater than the minimum cost already found for this vertex,
        # skip this path (it is not optimal)
        if distance > visited_distance.get(vertex, float('inf')):
            print(f"Skipping {vertex} as a cheaper path was already found.")
            continue

        # if the currt path is the goal, return the path
        if vertex == destination:
            return path,distance,index

        # Explore the neighbours of the current vertex.
        for neighbour in graph[vertex]:
            new_distance = visited_distance[vertex] + graph[vertex][neighbour]['distance']

            # if neighbour has not been visited before or the new cost is lower thathe previously recorded cost,
            # update the cost and add/update the neighbour in the priority queue.
            if neighbour not in visited_distance or new_distance < visited_distance[neighbour]:
                visited_distance[neighbour] = new_distance
                next_path = [*path, neighbour]
                frontier.push((neighbour, next_path,new_distance), new_distance)
                print(f"Adding/Updating neighbour: {neighbour} with new cost: {new_distance}")
                print(f"Highest priority in frontier: {frontier.peek()}")
    return None

def astar_search_path(graph, start, destination, cities):
    print(f"Evaluating the path from {start} to {destination} Using A*!!\n")
    frontier = PriorityQueue()
    # Store tuples of (vertex, path, cost) in the priority queue. The priority is the cost to reach the vertex (g) + the heuristic estimate (h).
    frontier.push((start, [start], 0), 0 + heuristic(cities[start], cities[destination]))

    # Dictionary to store the minimum cost found so far to reach each node.
    visited_distance = {start: 0}

    # Counter for iterations to show progress.
    index = 0

    while not frontier.is_empty():
        print("\n")
        index += 1
        # Get the element with the lowest f-cost (cost + heuristic) from the priority queue.

        # Print information about the node being explored.
        print(f"Iteration: {index}")
        if not frontier.is_empty():
            print(f"Frontier : {frontier.peek()}")
        else:
            print("Frontier is empty!!")
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        # If the cost of the current path (g) > the minimum cost already found for this vertex, skip this path (not optimal based on g-cost).
        if distance > visited_distance.get(vertex, float('inf')):
             print(f"Skipping {vertex} as a cheaper path (based on g-cost) was already found.")
             continue

        # If the current vertex is the goal, return the path.
        if vertex == destination:
                return path, distance, index

        # Explore the neighbors of the current vertex.
        for neighbor in graph[vertex]:
            # Calculate the cost to reach the neighbor through the current vertex (new g-cost).
            new_distance = visited_distance[vertex] + graph[vertex][neighbor]['distance']

            # If neighbor has not been visited before or the new cost < previously recorded cost (g-cost),
            # update the cost and add/update the neighbor in the priority queue.
            if neighbor not in visited_distance or new_distance < visited_distance[neighbor]:
                visited_distance[neighbor] = new_distance
                next_path = [*path, neighbor]
                # The priority for A* is g + h
                f_cost = new_distance + heuristic(cities[neighbor], cities[destination])
                frontier.push((neighbor, next_path, new_distance), f_cost)
                print(f"Adding/Updating neighbor: {neighbor} with new cost (g): {new_distance}, f-cost: {round(f_cost,2)}")
                print(f"Highest priority in frontier: {frontier.peek()}")
    return None