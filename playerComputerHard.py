from random import randint
from playerComputer import playerComputer

class playerComputerHard(playerComputer):	

	def __init__(self, column, row, ships, roll):
		self.name = "ComputerHard"
		self.roll = roll
		playerComputer.__init__(self, column, row, ships)
		self.board_Probability = {}
		self.probability = 0
		self.weight = 1
		self.priority_Target_Queue = []
		self.probability_Of_Target_Queue_Coordinate = (0)
		self.ships_Remaining = []
		self.initialize_Ships_Remaining()

	def initialize_Ships_Remaining(self):
		for ship in self.list_Of_Ship_Names:
			self.ships_Remaining.append(ship)

	def which_Ships_Remaining(self):
		for ship in self.enemy_Ships_And_Their_Coordinates:
			if len(self.enemy_Ships_And_Their_Coordinates[ship]) == self.ships_And_Lengths[ship]:
				try:
					self.ships_Remaining.remove(ship)
				except:
					pass
	"""	
	Generate the probability of a ship being in each spot on the board and assign that to board_Probability
		- only check ships that havn't been sunk.
		- evaluate all of each ships horizontal positions, starting from the left and moving right.
			- start at A1. get coords that a ship would cover given its length
				- if the ship has confirmed coords, then this list needs to contain all of them
					- the coords in the list that arn't the confirmed hits need to have a weight added to them
				- if this list contains any discontinuous points, then toss it out
				- if all the coords are valid, add 1 probability point to each coord.
			- move to A2 and repeat previous steps

		- evaluate all of each ships vertical positions.

	Shoot at the coordinate with the highest weight and highest probability. If theres a 
		tie, take a random from the tie
		- for each coordinate in all board coordinates, get value
		- store initial key in firing queue
		- compare the next coordinates value with the value of coordinate in firing queue
			- if new coordinate has greater value, then empty the firing queue and add this coord.

	Every turn reevaluate.
		- purge the probability and weight of each coord.
	"""
	def determine_Each_Coordinate_Probability(self):
		self.purge_Then_Generate_Probability_Board()
		for ship in self.ships_Remaining:
			if ship in self.enemy_Ships_And_Their_Coordinates:
				ship_Length = self.ships_And_Lengths[ship]
				if len(self.enemy_Ships_And_Their_Coordinates[ship]) == ship_Length:
					continue
			self.horizontal_Positions(ship)
			self.vertical_Positions(ship)

	def purge_Then_Generate_Probability_Board(self):
		# If the dictionary already exists, purge all the values within and recreate
		# board_Probability = {A1:[probability, weight], A2:[probability, weight]}
		self.board_Probability = {}
		for letter in self.column:
			for num in self.row:
				self.board_Probability[letter + num] = [(0), (0)]	

	def horizontal_Positions(self, ship):
		# Generate every horizontal position a ship can have
		ship_Length = self.ships_And_Lengths[ship]
		for letter in self.column:
			for number in self.row:

				increment = (0)
				potential_Ship_Position = []
				while increment < ship_Length:
					if (self.row.index(number) + ship_Length) <= len(self.row):
						potential_Ship_Position.append((letter + self.row[(self.row.index(number) + increment)]))
					increment += (1)

				self.add_Coordinates_To_Appropriate_Queue(ship, potential_Ship_Position, ship_Length)

	def vertical_Positions(self, ship):
		# Generate every vertical position a ship can have
		ship_Length = self.ships_And_Lengths[ship]
		for number in self.row:
			for letter in self.column:

				increment = (0)
				potential_Ship_Position = []
				while increment < ship_Length:
					if (self.column.index(letter) + ship_Length) <= len(self.column):
						potential_Ship_Position.append((self.column[(self.column.index(letter) + increment)] + number))
					increment += (1)

				self.add_Coordinates_To_Appropriate_Queue(ship, potential_Ship_Position, ship_Length)

	def add_Coordinates_To_Appropriate_Queue(self, ship, potential_Ship_Position, ship_Length):
		if len(potential_Ship_Position) == ship_Length:
			# Check to see if all the points are valid
			invalid_Coordinates = self.invalid_Points(ship)
			if len((set(potential_Ship_Position) - set(invalid_Coordinates))) != len(potential_Ship_Position):
				return
			ship_Confirmed_Hits = self.ship_Coordinates(ship)
			if bool(ship_Confirmed_Hits) == (True):
				# If a ship has confirmed hits, make sure they are all containted in the potential_Ship_Position
				if len((set(potential_Ship_Position) & set(ship_Confirmed_Hits))) == len(ship_Confirmed_Hits):
					#set probability and weight
					for coordinate in ((set(potential_Ship_Position)) - (set(ship_Confirmed_Hits))):
						self.board_Probability[coordinate][self.probability] += (1)
						self.board_Probability[coordinate][self.weight] += (1)
				else:
					return
			else:
				for coordinate in potential_Ship_Position:
					self.board_Probability[coordinate][self.probability] += (1)
		else:
			return

	def ship_Coordinates(self, ship):
		confirmed_Hits = []
		if ship in self.enemy_Ships_And_Their_Coordinates:
			confirmed_Hits = self.enemy_Ships_And_Their_Coordinates[ship]
		return confirmed_Hits

	def invalid_Points(self, ship):
		invalids = []
		for coordinate in self.shots_Fired_Log:
			if ship in self.enemy_Ships_And_Their_Coordinates:
				if coordinate not in self.enemy_Ships_And_Their_Coordinates[ship]:
					invalids.append(coordinate)
			else:
				invalids.append(coordinate)
		return invalids

	def generate_Probable_Targets(self):
		# coordinates with a higher weight get priority listing in the firing queue
		probability = self.probability
		weight = self.weight
		# Find the ships with the highest probability number
		for coordinate in self.board_Probability:
			if self.board_Probability[coordinate][weight] > 0:
				self.priority_Target_Queue.append(coordinate)
			if bool(self.target_Queue) == (False):
				self.target_Queue.append(coordinate)
			elif self.board_Probability[coordinate][probability] == self.board_Probability[(self.target_Queue[0])][probability]:
				self.target_Queue.append(coordinate)
			elif self.board_Probability[coordinate][probability] > self.board_Probability[(self.target_Queue[0])][probability]:
				self.target_Queue = []
				self.target_Queue.append(coordinate)				
			else:
				pass

	def find_Future_Targets(self):
		# Clears the firing queue
		self.target_Queue = []
		self.priority_Target_Queue = []
		self.which_Ships_Remaining()
		# determines probability and weight of each coordinate and assigns it to the probability board
		self.determine_Each_Coordinate_Probability()
		# Adds to the firing queue, no return
		self.generate_Probable_Targets()

	def generate_Target(self):
		# If the firing queue is not empty, return a random coord from it
		# Else, error
		if bool(self.priority_Target_Queue) == (True):
			target = self.priority_Target_Queue.pop(randint(0, (len(self.priority_Target_Queue) - 1)))
			return target
		elif len(self.target_Queue) > (0):		
			target = self.target_Queue.pop(randint(0, (len(self.target_Queue) - 1)))
			return target			
		else:
			print 'Erro in generate_Target in playerComputerHard'