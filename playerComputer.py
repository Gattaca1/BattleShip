from random import randint
from player import player

class playerComputer(player):

	def __init__(self, column, row, ships):
		player.__init__(self, column, row, ships)	
		self.random_Target_Queue = []		
		self.target_Queue = []
				
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
			target = self.computer_Logic()
			valid = self.is_Target_Valid(target)
			target_Picked = valid
		
		print "[Opponent]> " + target
		return target

	def computer_Logic(self):
		self.find_Future_Targets()
		target = self.generate_Target()
		return target

	def generate_Target(self):			
		if bool(self.target_Queue) == (True):		
			target = self.target_Queue.pop(randint(0, (len(self.target_Queue) - 1)))
			return target			
		else:
			target = self.random_Target_Queue.pop(randint(0, (len(self.random_Target_Queue) - 1)))
			return target
		
	def confirmed_Coordinate_Of_This_Ship(self, coordinate, ship):
		"""Create a link between an enemy ship and a coordinate"""
		self.shots_Fired_Hit_Log.append(coordinate)
		if ship not in self.enemy_Ships_And_Their_Coordinates:
			self.enemy_Ships_And_Their_Coordinates[ship] = []
			self.enemy_Ships_And_Their_Coordinates[ship].append(coordinate)
		else:
			self.enemy_Ships_And_Their_Coordinates[ship].append(coordinate)

	def generate_Random_Queue_Targets(self):
		column = self.column
		row = self.row
		
		#fire only on every other square
		if self.random_Target_Queue == []:
			for i in column:
				if column.index(i) % 2 == 0:
					# If column is even, fire on odd row
					for n in row:
						if row.index(n) % 2 == 1:
							self.random_Target_Queue.append((i + n))
				if column.index(i) % 2 == 1:
					for n in row:
						if row.index(n) % 2 == 0:
							self.random_Target_Queue.append((i + n))

	def all_Adjacent_Coords(self, starting_Coord):
		column = self.column
		row = self.row

		starting_Coord_Column_Letter = starting_Coord[:1]
		starting_Coord_Row_Number = starting_Coord[1:]

		#confirmed hit column index
		starting_Coord_Column_Index = column.index(starting_Coord_Column_Letter)
		starting_Coord_Row_Index = row.index(starting_Coord_Row_Number)

		adjacent_Coords = []

		first_Column_Letter = (column[0])
		last_Column_Letter = (column[-1])
		first_Row_Number = (row[0])
		last_Row_Number = (row[-1])
		
		if starting_Coord_Column_Letter != last_Column_Letter:
			#add 1 to column
			#C3
			adjacent_Coords.append((column[(starting_Coord_Column_Index + 1)] + starting_Coord_Row_Number))
		if starting_Coord_Column_Letter != first_Column_Letter:
			#subtract 1 from column
			#A3
			adjacent_Coords.append((column[(starting_Coord_Column_Index - 1)] + starting_Coord_Row_Number))
		if starting_Coord_Row_Number != last_Row_Number:
			#add 1 to row
			#B4
			adjacent_Coords.append((starting_Coord_Column_Letter + row[(starting_Coord_Row_Index + 1)]))
		if starting_Coord_Row_Number != first_Row_Number:
			#subtract 1 from row
			#B2
			adjacent_Coords.append((starting_Coord_Column_Letter + row[(starting_Coord_Row_Index - 1)]))

		return (adjacent_Coords)