from random import randint

class shipPlacement(object):

	def __init__(self, column, row, ships, all_Board_Coords):
		self.column = column
		self.row = row
		self.ships = ships
		self.all_Board_Coords = all_Board_Coords
		self.ship_Names_And_Coordinates = {}
		self.occupied_Positions = []
		self.initialize_Ships()

		################ PUBLIC ################
		
	def initialize_Ships(self):	
		for ship in self.ships:		
			valid = (False)
			while valid == (False):				
				length = self.ships[ship]
				starting_Coord = self.random_Coord()				
				vector_Options = self.potential_Vectors(starting_Coord, length)	
				vector = self.random_Vector(vector_Options)				
				ship_Coordinates = self.generate_Ship_Coordinates(starting_Coord, length, vector)				
				valid = self.validate_Ship_Coordinates(ship_Coordinates)
				if valid == (True):
					self.assign_Ship_Coordinates(ship_Coordinates, ship)

	def return_Ship_Names_And_Coordinates(self):
		return self.ship_Names_And_Coordinates

	def return_All_Occupied_Positions(self):
		return self.occupied_Positions

		################ PRIVATE ################
					
	def random_Coord(self):	
		#return a random board coordinate
		rand_Row = self.row[randint(0, (len(self.row) - 1))]
		rand_Col = self.column[randint(0, (len(self.column) - 1))]
		return (rand_Col + rand_Row)		
		
	def potential_Vectors(self, initial_Coordinate, ship_Length):		
		#return potential vectors based on given coordinate and ship size
		vector_Options = ['down', 'up', 'right', 'left']
		lower_Bound = (ship_Length - 1)
		upper_Bound = (len(self.row) - ship_Length)
		row_Pos = self.row.index((initial_Coordinate[1:]))
		col_Pos = self.column.index((initial_Coordinate[:1]))
		
		#if a number is within a lower bound range than it can't go a certain direction
		#take coord A5, a ship could be placed in any direction except up
		if col_Pos < lower_Bound:
			#can't go up
			vector_Options.remove('up')
		if col_Pos > upper_Bound:
			#can't go down
			vector_Options.remove('down')
		if row_Pos < lower_Bound:
			#can't go left
			vector_Options.remove('left')
		if row_Pos > upper_Bound:
			#can't go right
			vector_Options.remove('right')
		return (vector_Options)		
		
	def random_Vector(self, potential_Vectors):		
		#return a random vector chosen from list of potential vectors
		vector = potential_Vectors[(randint(0,(len(potential_Vectors) - 1)))]
		return (vector)		
		
	def generate_Ship_Coordinates(self, initial_Coordinate, ship_Length, vector):	
		#return a set of coordinates that a ship will occupy given its initial starting point, vector, and ship size
		row_Pos = self.row.index((initial_Coordinate[1:]))
		col_Pos = self.column.index((initial_Coordinate[:1]))
		row_Val = (initial_Coordinate[1:])
		col_Val = (initial_Coordinate[:1])
		ship_Coordinates = []

		i = 0
		while i < ship_Length:
			if vector == 'up':
				#subtract from column
				ship_Coordinates.append((self.column[(col_Pos - i)] + row_Val))
			elif vector == 'down':
				#add to column
				ship_Coordinates.append((self.column[(col_Pos + i)] + row_Val))
			elif vector == 'left':
				#subtract from row
				ship_Coordinates.append((col_Val + (self.row[(row_Pos - i)])))
			elif vector == 'right':
				#add to row
				ship_Coordinates.append((col_Val + (self.row[(row_Pos + i)])))
			i += 1
		return (ship_Coordinates)		
		
	def validate_Ship_Coordinates(self, set_Coordinates):
		#a valid set of coordinates is one in which no coordinate in the set is occupied by a ship
		#>>> a & b                              # letters in both a and b
		potential_Coords = set(set_Coordinates)
		occupied_Coords = set(self.occupied_Positions)
		common_Coords = potential_Coords & occupied_Coords
		if len(common_Coords) == (0):
			return (True)
		else:
			return (False)
		
	def assign_Ship_Coordinates(self, ship_Coordinates, ship_Name):	
		#given a set of coordinates, set each coordinate to occupied by boat
		self.ship_Names_And_Coordinates[ship_Name] = ship_Coordinates
		for coordinate in ship_Coordinates:
			self.occupied_Positions.append(coordinate)			