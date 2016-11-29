from Grid import Grid
import numpy as np
pm = np.genfromtxt('prob_matrix.csv', delimiter = ',')
g = Grid(pm, 2)
g.summon_passengers()
print [x.position for x in g.passengers]
print[x.get_position() for x in g.idle_car_list]

g.assign_cars()
print[x.get_position() for x in g.use_car_list]
print [x.position for x in g.passengers]