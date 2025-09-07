import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

path = "/Dataset/"

def get_Path(file_name):
  return str(path+file_name)

def convert_degrees_to_km(cities):
    R = 6371 # Radius of Earth in km
    phi = math.radians(40.0) #Reference latitude for Spain
    city_names = list(cities.keys())
    coordinates_array = np.array(list(cities.values()))
    lon_rad, lat_rad = np.radians(coordinates_array[:,0]), np.radians(coordinates_array[:,1])
    X, Y = R*lon_rad*math.cos(phi), R*lat_rad

    xy_coord = {
        city_names[i]: [round(X[i].item(),2),round(Y[i].item(),2)]
        for i in range(len(city_names))
    }

    return xy_coord

def construct_graph(cities_of_spain,neighbours):
    spain_map = {}
    # Plot cities as scatter points and annotate with city names
    x_coords = [coords[0] for coords in cities_of_spain.values()]
    y_coords = [coords[1] for coords in cities_of_spain.values()]
    city_names = list(cities_of_spain.keys())
    plt.scatter(x_coords, y_coords, color='blue')
    for i, city in enumerate(city_names):
        plt.text(x_coords[i] + 0.05, y_coords[i] + 0.05, city, fontsize=6, color="black")

    # Plot connections and distances, and build the spain_map dictionary
    for city1, city2, dist in neighbours:

        spain_map.setdefault(city1, {})[city2] = {'distance': dist}
        spain_map.setdefault(city2, {})[city1] = {'distance': dist}

        x1, y1 = cities_of_spain[city1]
        x2, y2 = cities_of_spain[city2]
        plt.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=1)

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        offset = 0.15
        plt.text(mid_x, mid_y + offset, str(dist), fontsize=5.5, color="green", ha='left', va='baseline')

    plt.xlabel("X-coordinates")
    plt.ylabel("Y-coordinates")
    plt.title("Visualised Map of Spain in the form of a Graph with Neighbour connections and Distances",fontsize=10)

    # Display the graph
    plt.show()
    print("\n")
    return spain_map


city_data = pd.read_csv(get_Path("Spain_Cities_Coodinates.csv"))
dist_matrix = pd.read_csv(get_Path("Spain_Cities_Corelation_Matrix.csv"))

cities_of_spain = {
    row.CityName: [row.Longitude, row.Latitude]
    for row in city_data.itertuples(index=False)
}

cities_of_spain = convert_degrees_to_km(cities_of_spain)
city_data = pd.DataFrame(cities_of_spain).T
city_data.columns = ["X-Coordinate","Y-Coordinate"]
print(cities_of_spain)
print("\n")

neighbours = []

for i in range(dist_matrix.shape[0]):
    x = dist_matrix.iloc[i, :]
    relation_key = x.iloc[0]
    for j in range(1, dist_matrix.shape[1]):
        if j > i and x.iloc[j] != 0:
            temp_tuple = (relation_key, dist_matrix.columns[j], int(x.iloc[j]))
            neighbours.append(temp_tuple)
print(neighbours)

spain_map = construct_graph(cities_of_spain,neighbours)