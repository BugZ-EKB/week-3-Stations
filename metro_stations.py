import json
from datetime import datetime
import re

with open('data-397-2023-09-17.json', 'r') as metro_stations:
    metro_stations_list = json.load(metro_stations)
    print(metro_stations_list[3])

station_repair_escalators = []
for station in metro_stations_list:
    if len(station['RepairOfEscalators']) != 0:
        station_repair_escalators.append(station)

dt_now = datetime.now()
pattern = r'(.*), в'
repairing_station_list = set()
for station in station_repair_escalators:
    if station['Name'] not in repairing_station_list:
        for repair_period in station['RepairOfEscalators']:
            start_date_str, end_date_str = repair_period['RepairOfEscalators'].split('-')
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
            if dt_now > start_date and dt_now < end_date:
                match_station = re.search(pattern, station['Name'])
                station_name = match_station.group(1)
                repairing_station_list.add(station_name)
                break

for station in repairing_station_list:
    print(station)