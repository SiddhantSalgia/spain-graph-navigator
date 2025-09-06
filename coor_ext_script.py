from geopy.geocoders import Nominatim
from meteostat import Point, Daily, Stations
import time
import asyncio
import pandas as pd

geolocator = Nominatim(user_agent="spain-graph-navigator")
upload_path = "UPLOAD_PATH"
country = "Spain"

def sync_geocode(city):
    result = geolocator.geocode(city+", "+country)
    if asyncio.iscoroutine(result):
        return asyncio.run(result)   # force coroutine to resolve
    return result

#20 Spanish cities are considered for builing a simple search agent
spain_city_list = [
    "Barcelona",
    "Pamplona",
    "Madrid",
    "Granada",
    "León",        
    "Seville",
    "Valencia",
    "Salamanca",
    "Toledo",
    "Cuenca",
    "Zaragoza",
    "Valladolid",
    "Bilbao",
    "Córdoba",     
    "Albacete",
    "Cáceres",     
    "Murcia",
    "Badajoz",
    "Burgos",      
    "Logroño"
]

def spain_cities_coord_gen(city_list):
    geolocator = Nominatim(user_agent="spain-graph-navigator")
    spain_city_coords = {}

    for city in city_list:
        if city not in spain_city_coords:
            try:
                location = sync_geocode(city)
                if location:

                    # Append latitude and longitude in the dictionary
                    spain_city_coords[city] =[location.latitude,location.longitude]
                else:
                    print(f"Couldn't find coordinates for {city}")
            except Exception as e:
                print(f"Error fetching crds for {city}: {e}")
            
            time.sleep(1)
    return spain_city_coords

spain_coord_dataset = pd.DataFrame.from_dict(
    spain_cities_coord_gen(spain_city_list),
    orient="index",
    columns=["Latitude","Longitude"]
).reset_index()

spain_coord_dataset.columns = ["CityName", "Latitude", "Longitude"]
file_name = "Spain_Cities_Coodinates.csv"
spain_coord_dataset.to_csv(upload_path+file_name,index=False)
