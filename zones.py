import csv
import numpy as np
from datetime import datetime
from sympy.solvers import solve
from sympy import Symbol




#assigns each pickup to the closest point. delta is the distance between points
#makes max_lat, max_long the largest index in the grid
def assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data):

	delta_lat = delta / 69
	delta_lon = delta / 52.49
	print("delta_lat ", delta_lat)
	print("delta_lon ", delta_lon)
	lat_r = np.arange(min_lat, max_lat, delta_lat)
	lon_r = np.arange(min_lon, max_lon, delta_lon)
	lat_range = np.append(lat_r, max_lat)
	lon_range = np.append(lon_r, max_lon)
	#prints the list of points
	print("lat range:", lat_range)
	print("lon range:", lon_range)


	#line[3] and line[4] are the coordinates of closest point
	#line[5] and line[6] are numbered coordinates of closest point aka (0,1), (1,0) etc
	lat_points = {}
	i=0
	for lat in lat_range:
		lat_points[lat]=i
		i += 1
	
	lon_points = {}
	j=0
	for lon in lon_range:
		lon_points[lon]=j
		j += 1

	for line in data:
		line.append(0)
		line.append(0)
		line.append(0)
		line.append(0)	
		for lat in lat_range:
			if line[1] <= lat + delta_lat/2:
				line[3] = lat
				line[5] = lat_points[lat]
				break
		for lon in reversed(lon_range):
			if line[2] <= lon + delta_lon/2:
				line[4] = lon
				line[6] = lon_points[lon]

	return [i,j]


#sample rectangle in Manhattan
max_lat = 40.750790
min_lat = 40.711246

max_lon = -73.977716
min_lon = -74.008615


data = []
with open('small_uber_dataset.csv', 'r') as f:
	count = 0
	for line in f:
		if count == 0:
			count += 1
			continue
		split_line = line.split(',')
		date_str, lat_str, lon_str, base_str = split_line
		new_line=[None]*3
		if float(lat_str) < max_lat and float(lat_str) > min_lat and float(lon_str) < max_lon and float(lon_str) > min_lon:
			new_line[0] = datetime.strptime(date_str, '%m/%d/%y %H:%M')
			new_line[1] = float(lat_str)
			new_line[2] = float(lon_str)
		if (not all(x is None for x in new_line)):
			data.append(new_line[0:3])

#print("data", data)
#print(max_lat, min_lat, max_lon, min_lon)

#delta in miles
delta = 0.2
print("delta", delta, " miles")
[max_x, max_y] = assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data)
np_data = np.array(data)

#max_x = max(max([np_data[:,6]]))
#[np_data[:,5]]

print("density matrix", max_x, "by ", max_y)


density = np.matrix(np.zeros(shape=(max_x, max_y)))
for line in data:
	density.itemset((line[5], line[6]), density.item(line[5], line[6])+1)
print(density)

np.savetxt("density.csv", density, delimiter=",", fmt="%05d")









