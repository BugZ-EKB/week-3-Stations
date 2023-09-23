import csv
import re


number_bus_stations = 0
street_station_list = []
max_street_name = ''
max_street_count = 0

with open('bus_stops.csv', 'r', encoding='windows-1251') as bus_stops:
    reader = csv.DictReader(bus_stops, delimiter=';')
    pattern = r'», ([^()]+)'
    for row in reader:
        number_bus_stations += 1
        match_street = re.search(pattern, row['Name'])
        if match_street:
            street_name = match_street.group(1).strip()
            street_station_list.append(street_name)

street_location_station_sum = {}
for street in street_station_list:
    if street in street_location_station_sum:
        street_location_station_sum[street] += 1
    else:
        street_location_station_sum[street] = 1
    if street_location_station_sum[street] > max_street_count:
        max_street_name = street
        max_street_count = street_location_station_sum[street]

print(f'Количество остановок: {number_bus_stations}')
print(f'Больше всего остановок на улице "{max_street_name}" - {max_street_count} штук')
