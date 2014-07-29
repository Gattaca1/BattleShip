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