import numpy as np

class Car(object):

    def __init__(self, loc):
        self.position = loc
        self.status = 'idle'
        self.destination = None

    def get_position(self):
        return self.position

    def set_destination(self, dest):
        self.destination = dest
        self.x_dir = np.sign(dest[0] - self.position[0])
        self.y_dir = np.sign(dest[1] - self.position[1])

    def set_status(self, new_status):
        self.status = new_status

    def get_status(self):
        return self.status

    def possible_moves(self):
        if self.x_dir == 0:
            return [np.array([0, self.y_dir])]
        elif self.y_dir == 0:
            return [np.array([self.x_dir, 0])]
        else:
            return [np.array([self.x_dir, 0]), np.array([0, self.y_dir])]

    def move(self, new_pos):
        self.position += new_pos
        if self.position[0] == self.destination[0]:
            self.x_dir = 0
        if self.position[1] == self.destination[1]:
            self.y_dir = 0
        if self.x_dir == 0 and self.y_dir == 0:
            return 1


