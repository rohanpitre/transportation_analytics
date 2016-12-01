import csv
import numpy as np
from datetime import datetime


data = []
with open('small_uber_dataset.csv', 'r') as f:
	count = 0
	for line in f:
		if count == 0:
			count += 1
			continue
		split_line = line.split(',')
		date_str, lat_str, lon_str, base_str = split_line
		split_line[0] = datetime.strptime(date_str, '%m/%d/%y %H:%M')
		split_line[1] = float(lat_str)
		split_line[2] = float(lon_str)
		data.append(split_line[0:3])

np_data = np.array(data)

#find max & min latitude & longtitude
max_lat = max(max([np_data[:,1]]))
min_lat = min(min([np_data[:,1]]))

max_lon = max(max([np_data[:,2]]))
min_lon = min(min([np_data[:,2]]))

#print(max_lat, min_lat, max_lon, min_lon)

#assigns each pickup to the closest point. delta is the distance between points
def assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data):
	lat_range=np.arange(min_lat, max_lat, delta)
	lon_range=np.arange(min_lon, max_lon, delta)

	#prints the list of points
	print(lat_range)
	print(lon_range)

	#line[3] and line[4] are the coordinates of closest point
	for line in data:
		line.append(0)
		line.append(0)	
		for lat in lat_range:
			if line[1] <= lat + delta/2:
				line[3] = lat
				break
		for lon in lon_range:
			if line[2] <= lon + delta/2:
				line[4] = lon
				break	
	return

delta=0.01
assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data)

freq = dict()
for line in data:
	if (line[3], line[4]) in freq:
		freq[(line[3], line[4])] += 1
	else:
		freq[(line[3], line[4])] = 1

for key in sorted(freq):
    print(key)
    print(freq[key])







