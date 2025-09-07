import data_extraction as de
import search_algo_implem as s
import time
import pandas as pd

def main():
    graph = de.spain_map
    
    source = input("Enter the Start City: ")
    destination = input("Enter Destination: ")

    start_time_1 = time.perf_counter()
    ucs_path,total_distance_1,iterations_1 = s.uniform_cost_search_path(graph, source, destination) # type: ignore
    end_time_1 = time.perf_counter()
    elapsed_time_1 = end_time_1 - start_time_1
    print(f"\nPath determined by UCS from {source} to {destination} is {ucs_path} in {iterations_1} iterations and the total distance is {total_distance_1}")

    start_time_2 = time.perf_counter()
    as_path, total_distance_2, iterations_2 = s.astar_search_path(graph, source, destination) # type: ignore
    end_time_2 = time.perf_counter()
    elapsed_time_2 = end_time_2 - start_time_2
    print(f"\nPath determined by A* from {source} to {destination} is {as_path} in {iterations_2} iterations and the total distance is {total_distance_2}")

    performance_metrics = pd.DataFrame({
        "Algorithm":["UCS","A*"],
        "Path Distance (in km)":[total_distance_1,total_distance_2],
        "Nodes Expanded":[iterations_1,iterations_2],
        "Runtime (in ms)":[elapsed_time_1,elapsed_time_2]
    })
    print(performance_metrics)

main()