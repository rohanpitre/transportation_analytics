import csv
import numpy as np
from datetime import datetime
import time
from sympy.solvers import solve
from sympy import Symbol
import matplotlib.pyplot as plt

#assigns each pickup to the closest point. delta is the distance between points in miles
#returns max index of lat and lon points
def assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data):

	#latitude and longitude degrees are translated into miles differently
	#calculate specific deltas
	delta_lat = delta / 69
	delta_lon = delta / 52.49
	print("delta_lat ", delta_lat)
	print("delta_lon ", delta_lon)

	#create two arrays that list the coordinates of points that pickups will be assigned to
	#from minimum to maximum with step delta
	lat_r = np.arange(min_lat, max_lat, delta_lat)
	lon_r = np.arange(min_lon, max_lon, delta_lon)
	#add the max values that arrange omits to get the full list of points.
	#notice that distance between the last two points will be smaller than delta
	lat_range = np.append(lat_r, max_lat)
	lon_range = np.append(lon_r, max_lon)
	print("lat range:", lat_range)
	print("lon range:", lon_range)

	#for each tuple line[3] and line[4] are the coordinates of closest point
	#line[5] and line[6] are numbered coordinates of closest point aka (0,1), (1,0) etc
	
	#dictionaries that will help translate coordinates into indeces
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

	#for each tuple fill in line[3], [4], [5], [6] with correct values
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
	#returns max index of lat and lon points
	return [i,j]



#sample rectangle in Manhattan
max_lat = 40.750790
min_lat = 40.711246

max_lon = -73.977716
min_lon = -74.008615

#delta in miles
delta = 0.2
print("delta", delta, " miles")

#convert csv file into a 2D array: datetime, latitude, longtitude
csv_file = 'apr14-uber-dataset.csv'
#csv_file = 'small_uber_dataset.csv'
data = []
with open(csv_file, 'r') as f:
	count = 0
	for line in f:
		if count == 0:
			count += 1
			continue
		split_line = line.split(',')
		date_str, lat_str, lon_str, base_str = split_line
		new_line=[None]*3
		d=datetime.strptime(date_str, '%m/%d/%y %H:%M')
		if d.isoweekday()<=5 and d.hour > 16 and d.hour < 18 and float(lat_str) < max_lat and float(lat_str) > min_lat and float(lon_str) < max_lon and float(lon_str) > min_lon:
			new_line[0] = d
			new_line[1] = float(lat_str)
			new_line[2] = float(lon_str)
		if (not all(x is None for x in new_line)):
			data.append(new_line[0:3])

#assign zones will alter the data array and return max indeces for lat and lon
[max_x, max_y] = assign_zones(max_lat, min_lat, max_lon, min_lon, delta, data)

#create a matrix where value at i,j is the number of pickups at (i,j) point
print("density matrix", max_x, "by ", max_y)
density = np.matrix(np.zeros(shape=(max_x, max_y)))

for line in data:
	density.itemset((line[5], line[6]), density.item(line[5], line[6])+1)
density=density/22.0
print(density)

np.savetxt("density.csv", density, delimiter=",", fmt="%05f")

#plotting original points on a map
#plotting the nodes w/ size of node proportional to #requests assigned to it
np_data = np.array(data)
freq = {}
print((np_data[:,4]).size)
for i in range(0, (np_data[:,4]).size):
	key = (np_data[i,4], np_data[i,3])
	print(key)
	if key in freq:
		freq[key] += 1
	else:
		freq[key] = 1

freq2 = []
for key, f in freq.items():
	freq2.append((key[0], key[1], f))

for key, value in freq.items():
	print(key)
	print(freq[key])

fig1 = plt.figure(1)                                                          
ax = fig1.add_subplot(1,1,1)

lat_ticks = np.arange(min_lat, max_lat, float("{0:.3f}".format(delta/69)))                                              
lon_ticks = np.arange(min_lon, max_lon, float("{0:.3f}".format(delta/52.49)))                                              

ax.set_xticks(lon_ticks)                                                                                                 
ax.set_yticks(lat_ticks)                                                       
plt.xlabel('Longitude')
plt.ylabel('Latitude')

im = plt.imread('ny.png')
implot = plt.imshow(im, extent = [min_lon, max_lon, min_lat, max_lat])
plt.axis("scaled")
plt.axis([min_lon, max_lon, min_lat, max_lat])

plt.title('Scatterplot of Requests')

plt.plot(np_data[:,2], np_data[:,1], 'ro', markersize=2)
plt.show()

plt.xlabel('Longitude')
plt.ylabel('Latitude')


fig2 = plt.figure(2)
ax = fig2.add_subplot(1,1,1)

lat_ticks = np.arange(min_lat, max_lat, float("{0:.3f}".format(delta/69)))                                              
lon_ticks = np.arange(min_lon, max_lon, float("{0:.3f}".format(delta/52.49)))
ax.set_xticks(lon_ticks)                                                                                                 
ax.set_yticks(lat_ticks)                                                       

im = plt.imread('ny.png')
implot = plt.imshow(im, extent = [min_lon, max_lon, min_lat, max_lat])
plt.axis("scaled")
plt.axis([min_lon, max_lon, min_lat, max_lat])
np_freq = np.array(freq2)
plt.title('Demand at Each Node')

plt.scatter(np_freq[:,0], np_freq[:,1], s = np_freq[:,2])
plt.show()












