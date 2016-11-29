class Passenger(object):

	def __init__(self, loc):
		self.position = loc

	def set_destination(self, destination):
		self.destination = destination

	def get_destination(self):
		return self.destination