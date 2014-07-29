from random import randint
from shipPlacement import shipPlacement

class player(object):

	def __init__(self, column, row, ships):
		#         Things to track		
		# Ships and associated coordinates
		# Shots fired, shots connected, 
		# Shots received, shots received connected
		# Enemy ships & their coordinates
		self.column = column
		self.row = row
		self.ships_And_Lengths = ships
		self.all_Board_Coordinates = []
		self.all_Board_Coordinates = self.get_All_Board_Coordinates()
		self.list_Of_Ship_Names = []
		self.list_Of_Ship_Names = self.get_List_Of_Ship_Names()		
		self.generated_Ship_Coordinates = shipPlacement(self.column, self.row, self.ships_And_Lengths, self.all_Board_Coordinates)
		self.shots_Fired_Log = []
		self.shots_Fired_Hit_Log = []
		self.shots_Received_Log = []
		self.shots_Received_Hit_Log = []
		self.enemy_Ships_And_Their_Coordinates = {}		
		self.ships_And_Associated_Coordinates = {}
		self.ships_And_Associated_Coordinates = self.get_Ships_And_Associated_Coordinates()
		self.occupied_Coordinates = []
		self.occupied_Coordinates = self.get_List_Of_All_Occupied_Coordinates()

	################ PUBLIC ################
				
	def shot_Fired(self, coordinate):
		self.shots_Fired_Log.append(coordinate)

	def shot_Fired_Hit_Ship_At_Coordinate(self, coordinate, ship_Name):
		self.shots_Fired_Hit_Log.append(coordinate)
		if ship_Name not in self.enemy_Ships_And_Their_Coordinates:
			self.enemy_Ships_And_Their_Coordinates[ship_Name] = []
			self.enemy_Ships_And_Their_Coordinates[ship_Name].append(coordinate)
		else:
			self.enemy_Ships_And_Their_Coordinates[ship_Name].append(coordinate)
		
	def shot_Received(self, coordinate):
		self.shots_Received_Log.append(coordinate)

	def shot_Received_Is_Confirmed_Hit(self, coordinate):
		self.shots_Received_Hit_Log.append(coordinate)

	def is_A_Boat_At_Coordinate(self, coordinate):
		for ship_Name in self.ships_And_Associated_Coordinates:
			if coordinate in self.ships_And_Associated_Coordinates[ship_Name]:
				return (True)
		else:
			return (False)
		
	def which_Boat_At_Coordinate(self, coordinate):
		for ship_Name in self.ships_And_Associated_Coordinates:
			if coordinate in self.ships_And_Associated_Coordinates[ship_Name]:
				return ship_Name
		
	def is_Ship_Sunk(self, ship_Name):
		ship_Coordinates = self.ships_And_Associated_Coordinates[ship_Name]
		remaining_Coords = set(ship_Coordinates) - set(self.shots_Received_Log)
		if bool(remaining_Coords) == (False):
			return (True)
		else:
			return (False)
		
	def are_Ships_Remaining(self):
		tally = 0
		for ship_Name in self.ships_And_Lengths:
			tally += self.ships_And_Lengths[ship_Name]
		if tally > len(self.shots_Received_Hit_Log):
			return (True)
		elif tally == len(self.shots_Received_Hit_Log):
			return (False)
		else:
			print 'error in are_Ships_Remaining'

	def return_Board_Info(self):
		empty_List = []
		return empty_List

	def pick_Target(self):
		pass

	def get_Name(self):
		return self.name

	def get_Roll(self):
		return self.roll

	################ PRIVATE ################

	def get_List_Of_Ship_Names(self):
		names = []
		for ship_Name, ship_Length in self.ships_And_Lengths.iteritems():
			names.append(ship_Name)
		return names

	def get_All_Board_Coordinates(self):
		all_Coords = []
		for letter in self.column:
			for number in self.row:
				all_Coords.append(letter + number)
		return all_Coords

	def get_List_Of_All_Occupied_Coordinates(self):
		return self.generated_Ship_Coordinates.return_All_Occupied_Positions()

	def get_Ships_And_Associated_Coordinates(self):
		return self.generated_Ship_Coordinates.return_Ship_Names_And_Coordinates()

	def is_Target_Valid(self, coordinate):
		# coordinate must exist
		# coordinate must not yet be shot at
		if coordinate not in self.all_Board_Coordinates:
			return (False)

		if coordinate in self.shots_Fired_Log:
			return (False)
		return (True)