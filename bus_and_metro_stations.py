import re
import csv
import json
from geopy.distance import geodesic

def convert_bus_stop(bus_stop):
    return {
        'ID': bus_stop['ID'],
        'Longitude': float(bus_stop['Longitude_WGS84']),
        'Latitude': float(bus_stop['Latitude_WGS84']),
    }


with open('bus_stops.csv', 'r', encoding='windows-1251') as bus_stops:
    reader = csv.DictReader(bus_stops, delimiter=';')
    filtered_bus_stops = [convert_bus_stop(row) for row in reader]


with open('data-397-2023-09-17.json', 'r') as metro_stations:
    metro_stations_list = json.load(metro_stations)
pattern = r'(.*), в'
coordinates_station_dict = {}
for station in metro_stations_list:
    match_station = re.search(pattern, station['Name'])
    station_name = match_station.group(1)
    if station_name not in coordinates_station_dict:
        coordinates_station_dict[station_name] = [(float(station['Latitude_WGS84']), float(station['Longitude_WGS84']))]
    else:
        coordinates_station_dict[station_name] += [(float(station['Latitude_WGS84']), float(station['Longitude_WGS84']))]


bus_stops_near_station = {}
max_station_name = ''
max_station_count = 0
for bus in filtered_bus_stops:
    bus_coord = [bus['Latitude'], bus['Longitude']]
    for station in coordinates_station_dict:
        for station_coord in coordinates_station_dict[station]:
            if geodesic(station_coord, bus_coord) <= 0.5:
                if station in bus_stops_near_station:
                    bus_stops_near_station[station] += 1
                else:
                    bus_stops_near_station[station] = 1
                if bus_stops_near_station[station] > max_station_count:
                    max_station_name = station
                    max_station_count = bus_stops_near_station[station]
                break

print(f'Больше всего остановок рядом со станцией "{max_station_name}" - {max_station_count} штук')
