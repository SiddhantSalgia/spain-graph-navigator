# spain-graph-navigator
An end-to-end implementation of path finding on a map of Spain - represented in the form of a graph - using UCS and A* algorithms. 

The objective is to compare both Uniform Cost Search and A* Search algorithms in terms of accuracy, efficiency, and computational performance. 
UCS, also known as Dijkstra’s algorithm, guarantees an optimal solution by expanding nodes based solely on the lowest path cost. A* Search builds on this principle by including a heuristic function to guide the search, potentially reducing the number of nodes expanded.
Implementation has been done in a Jupiter Notebook environment using a self-constructed dataset of Spanish cities and distances. 
Both algorithms generated the same optimal path and cost, confirming their correctness. However, A* demonstrated better efficiency, solving with fewer node expansions and reduced computational effort as compared to UCS.

This comparison shows how different AI search strategies can affect problem-solving effectiveness, shedding light on the practical selection of algorithms for real-world optimisation problems.
