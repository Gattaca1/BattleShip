from player import player
from playerHuman import playerHuman
from playerComputer import playerComputer
from playerComputerEasy import playerComputerEasy
from playerComputerHard import playerComputerHard
from playerComputerMedium import playerComputerMedium

class playerFactory(object):

	def __init__(self, column, row, ships):
		self.column = column
		self.row = row
		self.ships = ships

	def initialize_Player_Mode(self, player_Mode, roll):
		if player_Mode == 'HUMAN':
			return playerHuman(self.column, self.row, self.ships, roll)
		elif player_Mode == 'EASY':
			return playerComputerEasy(self.column, self.row, self.ships, roll)
		elif player_Mode == 'MEDIUM':
			return playerComputerMedium(self.column, self.row, self.ships, roll)
		elif player_Mode == 'HARD':
			return playerComputerHard(self.column, self.row, self.ships, roll)
	"""

	def shot_Fired(self, coordinate):
		return self.player.shot_Fired(coordinate)

	def shot_Fired_Hit_Ship_At_Coordinate(self, coordinate, ship_Name):
		return self.player.shot_Fired_Hit_Ship_At_Coordinate(coordinate, ship_Name)
		
	def shot_Received(self, coordinate):
		return self.player.shot_Received(coordinate)

	def shot_Received_Is_Confirmed_Hit(self, coordinate):
		return self.player.shot_Received_Is_Confirmed_Hit(coordinate)

	def is_A_Boat_At_Coordinate(self, coordinate):
		return self.player.is_A_Boat_At_Coordinate(coordinate)
		
	def which_Boat_At_Coordinate(self, coordinate):
		return self.player.which_Boat_At_Coordinate(coordinate)
		
	def is_Ship_Sunk(self, ship_Name):
		return self.player.is_Ship_Sunk(ship_Name)
		
	def are_Ships_Remaining(self):
		return self.player.are_Ships_Remaining()

	def return_Board_Info(self):
		return self.player.return_Board_Info()

	def pick_Target(self):
		return self.player.pick_Target()
	"""