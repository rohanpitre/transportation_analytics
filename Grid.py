import numpy as np
from Car import Car
from Passenger import Passenger
import random

class Grid(object):

    '''
    initializes the grid with a probability matrix
    the the entry (i,j) of the matrix is the probability
    of arriving of a passenger arriving at (i,j) in a time step
    -1 means the point is not on the grid

    num_cars is the number of cars and they are randomly placed
    in the beginning ofthe simulation
    '''
    def __init__(self, prob_matrix, num_cars):
        self.grid = prob_matrix
        self.dim_x, self.dim_y = prob_matrix.shape

        self.idle_car_list = []
        self.use_car_list = []
        for i in range(num_cars):
            self.idle_car_list.append(Car(self.choose_rand_point()))

        self.passengers = []


    #chooses valid random point in the grid
    def choose_rand_point(self):
        valid = -1
        while valid == -1:
            x = random.randint(0, self.dim_x-1)
            y = random.randint(0, self.dim_y-1)
            valid = self.grid[x, y]
        return (x,y)

    #arrival of passengers
    def summon_passengers(self):
        for i in range(self.dim_x):
            for j in range(self.dim_y):
                if self.grid[i,j] == -1:
                    continue
                else:
                    roll = random.random()
                    if roll < self.grid[i,j]:
                        self.passengers.append(Passenger((i,j)))
                        self.passengers[-1].set_destination(self.choose_rand_point())

    #assign cars to passengers
    #if there are not enough cars
    def assign_cars(self):
        for i in range(len(self.passengers)):
            if len(self.idle_car_list) == 0:
                break
            asignee = self.passengers.pop(0)
            assigned_car = self.idle_car_list.pop(0)
            assigned_car.set_destination(asignee.position)
            self.use_car_list.append(assigned_car)
            assigned_car.set_status('pickup')

    #moves all the cars in use and changes status if necessary
    def move_cars(self):
        use_car_list_copy = []
        for car in self.use_car_list:
            candidates = car.possible_moves()
            delta = None
            if len(candidates) == 1:
                delta = candidates[0]
            else:
                car_pos = car.get_position()
                up_down = car_pos + candidates[1]
                left_right = car_pos + candidates[0]
                if self.grid[up_down[0], up_down[1]] > self.grid[left_right[0], left_right[1]]:
                    delta = candidates[0]
                else:
                    delta = candidates[1]
            reached = car.move(delta)
            if reached == 1:
                if car.get_status() == 'pickup':
                    car.set_status('dropoff')
                    car.set_destination(self.choose_rand_point())
                    use_car_list_copy.append(car)
                elif car.get_status() == 'dropoff':
                    car.set_status('idle')
                    self.idle_car_list.append(car)
            else:
                use_car_list_copy.append(car)
        self.use_car_list = use_car_list_copy[:]



