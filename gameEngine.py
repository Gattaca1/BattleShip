from random import randint
from displayBoard import displayBoard
from playerFactory import playerFactory

from player import player
from playerHuman import playerHuman
from playerComputer import playerComputer
from playerComputerEasy import playerComputerEasy
from playerComputerHard import playerComputerHard
from playerComputerMedium import playerComputerMedium

class gameEngine(object):

	def __init__(self):
		self.column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
		self.row = ['1','2','3','4','5','6','7','8','9','10']
		self.ships = {
		'Carrier':5,
		'Battleship':4,
		'Cruiser':3,
		'Submarine':3,
		'Destroyer':2
		}
		self.player_One_Mode = self.select_Game_Mode()
		self.player_Two_Mode = self.initialize_Opponent()
		player_Factory = playerFactory(self.column, self.row, self.ships)
		self.player_One = player_Factory.initialize_Player_Mode(self.player_One_Mode, "Player One")
		self.player_Two = player_Factory.initialize_Player_Mode(self.player_Two_Mode, "Player Two")

		#self.player_Human = self.select_Game_Mode()
		#self.player_Computer = self.initialize_Opponent()
		self.player_Order = self.player_Turn_Order()		

	def select_Game_Mode(self):
		print "Select Game Mode"
		print "1) You vs Computer"
		print "2) Computer vs Computer"
		print "Type 1 or 2"
		game_Mode = raw_input("> ")
		if game_Mode == "1":
			return "HUMAN"
		elif game_Mode == "2":
			print "Select player 1 difficulty: Easy, Medium, Hard"
			return self.select_Difficulty()
		else:
			self.select_Game_Mode()

	def initialize_Opponent(self):
		print "Select plaer 2 difficulty: Easy, Medium, Hard"
		return self.select_Difficulty()
		
	def select_Difficulty(self):		
		difficulty = raw_input("> ").upper()
		if difficulty == ('EASY') or difficulty == ('MEDIUM') or difficulty == ('HARD'):
			return difficulty
		else:
			self.select_Difficulty()
				
	def shoot(self, friendly, tango, coordinate):
		friendly.shot_Fired(coordinate)
		tango.shot_Received(coordinate)

		# Is a boat at target position?
		is_Coordinate_Occupied = tango.is_A_Boat_At_Coordinate(coordinate)
		if is_Coordinate_Occupied == (True):
			ship_Name = tango.which_Boat_At_Coordinate(coordinate)
			friendly.shot_Fired_Hit_Ship_At_Coordinate(coordinate, ship_Name)
			tango.shot_Received_Is_Confirmed_Hit(coordinate)
			print "[Console]> " + ship_Name + " Hit"
			ship_Sunk = tango.is_Ship_Sunk(ship_Name)
			if ship_Sunk == (True):
				print "[Console]> " + ship_Name + " Sunk"
			print ""
		else:
			print "[Console]> Miss"
			print ""		
				
	def whose_Turn(self, turn_Count):
		offense_Defense = []
		if turn_Count % 2 == 0:
			offense_Defense.append(self.player_Order[0])
			offense_Defense.append(self.player_Order[1])
			return offense_Defense
		else:
			offense_Defense.append(self.player_Order[1])
			offense_Defense.append(self.player_Order[0])			
			return offense_Defense

	def turn_Actions(self, offense, defense):
		"""return the destination"""
		#pick target and confirm valid
		target_Coordinate = offense.pick_Target()
		self.shoot(offense, defense, target_Coordinate)
		
	def is_Game_Over(self, player):
		if player.are_Ships_Remaining() == (True):
			return (False)
		if player.are_Ships_Remaining() == (False):
			return (True)
		else:
			print "ERROR in is_Game_Over"
	
	def player_Turn_Order(self):
		#randomly assign the turn order (human or computer shoots first)
		shoots_First = [self.player_One]
		shoots_First.insert((randint(0,1)), self.player_Two)
		return shoots_First

	def get_Player_Name_And_Roll(self, the_Player):
		name_Roll = []
		name_Roll.append(the_Player.get_Name())
		name_Roll.append(the_Player.get_Roll())
		return name_Roll
		
	def play_Game(self):
		game_Won = (False)
		turn_Count = 0		
		
		while game_Won == (False):
			offense, defense = self.whose_Turn(turn_Count)
			
			board_Info = offense.return_Board_Info()
			view = displayBoard(self.column, self.row)
			view.display_Boards(board_Info)
			self.turn_Actions(offense, defense)
			game_Won = self.is_Game_Over(defense)
			if game_Won == (True):
				player_Name, player_Roll = self.get_Player_Name_And_Roll(offense)
				rounded_Turn_Count = int(turn_Count / 2)
				print player_Roll + " (" + player_Name + ") wins after " + str(rounded_Turn_Count) + " Turns"
							
			turn_Count += 1	