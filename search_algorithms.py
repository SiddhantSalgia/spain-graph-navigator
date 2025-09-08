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

def bredth_first_search_path(graph, start, destination):
    print(f"Evaluating the path from {start} to {destination} using BFS!!")
    frontier = deque()
    frontier.append((start,[start],0))
    visited ={start}
    index = 0

    while frontier:
        print("\n")
        index+=1
        print(f"Iteration: {index}")
        if frontier:
            print(f"Frontier: {frontier[0]}")
        else:
            print("Frontier is empty")
        (vertex,path,distance) = frontier.popleft()
        print(f"Exploring node: {vertex} with cost: {distance}")

        if vertex == destination:
            return path, distance, index
        
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                new_distance = distance + graph[vertex][neighbour]['distance']
                next_path = [*path,neighbour]
                frontier.append((neighbour,next_path,new_distance))
                print(f"Adding neighbour: {neighbour} with cost: {new_distance}")
    return None

def depth_first_search_path(graph, start, destination):
    print(f"Evaluating the path from {start} to {destination} using DFS!!")
    frontier = [(start,[start],0)]
    visited = {start}

    index = 0

    while frontier:
        print("\n")
        index += 1 
        print(f"Iteration: {index}")
        if frontier:
            print(f"Frontier top: {frontier[-1]}")
        else:
            print(f"Frontier is empty!!")
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        if vertex == destination:
            return path, distance, index
        
        for neighbour in graph[vertex]:
            new_distance = distance + graph[vertex][neighbour]['distance']
            next_path = [*path,neighbour]
            frontier.append((neighbour,next_path,new_distance))
            print(f"Adding neighbour: {neighbour} with cost: {new_distance}")
    return None


def uniform_cost_search_path(graph, start, destination):
    print(f"Evaluating the path from {start} to {destination} Using UCS!!\n")
    frontier = PriorityQueue()
    frontier.push((start,[start],0),0)
    visited_distance = {start: 0}
    index = 0

    while not frontier.is_empty():
        print("\n")
        index += 1
        print(f"Iteration: {index}")
        if not frontier.is_empty():
            print(f"Frontier : {frontier.peek()}")
        else:
            print("Frontier is empty!!")
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        if distance > visited_distance.get(vertex, float('inf')):
            print(f"Skipping {vertex} as a cheaper path was already found.")
            continue

        if vertex == destination:
            return path,distance,index

        for neighbour in graph[vertex]:
            new_distance = visited_distance[vertex] + graph[vertex][neighbour]['distance']

            if neighbour not in visited_distance or new_distance < visited_distance[neighbour]:
                visited_distance[neighbour] = new_distance
                next_path = [*path, neighbour]
                frontier.push((neighbour, next_path,new_distance), new_distance)
                print(f"Adding/Updating neighbour: {neighbour} with new cost: {new_distance}")
                print(f"Highest priority in frontier: {frontier.peek()}")
    return None

def greedy_best_first_search(graph, start, destination, cities):
    print(f"Evaluating the path from {start} to {destination} Using GBFS!!\n")
    frontier = PriorityQueue()
    frontier.push((start,[start],0),heuristic(cities[start],cities[destination]))

    visited_distance = {start:0}

    index = 0

    while not frontier.is_empty():
        index+=1
        print(f"Iteration: {index}")
        if not frontier.is_empty():
            print(f"Frontier: {frontier.peek()}")
        else:
            print("Frontier is empty!!")
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        if vertex == destination:
            return path, distance, index
        
        for neighbour in graph[vertex]:
            new_distance = visited_distance[vertex] + graph[vertex][neighbour]['distance']
            if neighbour not in visited_distance or new_distance < visited_distance[neighbour]:
                visited_distance[neighbour] = new_distance
                next_path = [*path, neighbour]
                h_cost = heuristic(cities[neighbour],cities[destination])
                frontier.push((neighbour,next_path,new_distance), h_cost)
                print(f"Adding/Updating neighbour: {neighbour} with neqw cost: {new_distance}, h_cost: {round(h_cost,2)}")
                print(f"Highest priority in frontier: {frontier.peek()}")
    return None 

def astar_search_path(graph, start, destination, cities):
    print(f"Evaluating the path from {start} to {destination} Using A*!!\n")
    frontier = PriorityQueue()
    frontier.push((start, [start], 0), 0 + heuristic(cities[start], cities[destination]))
    visited_distance = {start: 0}
    index = 0

    while not frontier.is_empty():
        print("\n")
        index += 1

        print(f"Iteration: {index}")
        if not frontier.is_empty():
            print(f"Frontier : {frontier.peek()}")
        else:
            print("Frontier is empty!!")
        (vertex, path, distance) = frontier.pop()
        print(f"Exploring node: {vertex} with cost: {distance}")

        if distance > visited_distance.get(vertex, float('inf')):
             print(f"Skipping {vertex} as a cheaper path (based on g-cost) was already found.")
             continue

        if vertex == destination:
                return path, distance, index

        for neighbor in graph[vertex]:
            new_distance = visited_distance[vertex] + graph[vertex][neighbor]['distance']

            if neighbor not in visited_distance or new_distance < visited_distance[neighbor]:
                visited_distance[neighbor] = new_distance
                next_path = [*path, neighbor]
                # The priority for A* is g + h
                f_cost = new_distance + heuristic(cities[neighbor], cities[destination])
                frontier.push((neighbor, next_path, new_distance), f_cost)
                print(f"Adding/Updating neighbor: {neighbor} with new cost (g): {new_distance}, f-cost: {round(f_cost,2)}")
                print(f"Highest priority in frontier: {frontier.peek()}")
    return None