from displayBoard import displayBoard
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
		self.player_Human = self.select_Game_Mode()
		self.player_Computer = self.initialize_Opponent()
		self.player_Order = self.player_Turn_Order()		

	def select_Game_Mode(self):
		print "Play vs Computer, or watch Computer vs Computer"
		print "1 or 2"
		game_Mode = raw_input("> ")
		if game_Mode == "1":
			return playerHuman(self.column, self.row, self.ships)
		elif game_Mode == "2":
			print "Select player 1 difficulty: Easy, Medium, Hard"
			return self.select_Difficulty()
		else:
			self.select_Game_Mode()

	def initialize_Opponent(self):
		print "Select opponent difficulty: Easy, Medium, Hard"
		return self.select_Difficulty()
		
	def select_Difficulty(self):	
		difficulty_Set = (False)
		
		while difficulty_Set == (False):
			difficulty = raw_input("> ").upper()
			
			if difficulty == ('EASY'):
				return playerComputerEasy(self.column, self.row, self.ships)
				difficulty_Set = (True)
				
			if difficulty == ('MEDIUM'):
				return playerComputerMedium(self.column, self.row, self.ships)
				difficulty_Set = (True)
				
			if difficulty == ('HARD'):
				return playerComputerHard(self.column, self.row, self.ships)
				difficulty_Set = (True)
				
	def shoot(self, friendly, tango, coordinate):
		friendly.shot_Fired(coordinate)
		tango.shot_Received(coordinate)

		# Is a boat at target position?
		is_Coordinate_Occupied = tango.is_A_Boat_At_Coordinate(coordinate)
		if is_Coordinate_Occupied == (True):
			ship_Name = tango.which_Boat_At_Coordinate(coordinate)
			friendly.shot_Fired_Hit_Ship_At_Coordinate(coordinate, ship_Name)
			print "[Console]> " + ship_Name + " Hit"
			ship_Sunk = tango.is_Ship_Sunk(ship_Name)
			if ship_Sunk == (True):
				print "[Console]> " + ship_Name + " Sunk"
			print ""
		else:
			print "[Console]> Miss"
			print ""		
				
	def whose_Turn(self, turn_Count):
		if turn_Count % 2 == 0:
			return self.player_Order[0]
		return self.player_Order[1]
	
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
		shoots_First = [self.player_Human]
		shoots_First.insert((randint(0,1)), self.player_Computer)
		return shoots_First
		
	def play_Game(self):
		game_Won = (False)
		turn_Count = 0		
		
		while game_Won == (False):
			players_Turn = self.whose_Turn(turn_Count)
			
			if players_Turn == self.player_Human:
				board_Info = self.player_Human.return_Board_Info()
				view = displayBoard(self.column, self.row)
				view.display_Boards(board_Info)
				self.turn_Actions(self.player_Human, self.player_Computer)
				game_Won = self.is_Game_Over(self.player_Computer)
				if game_Won == (True):
					print "You win!"
				
			if players_Turn == self.player_Computer:
				self.turn_Actions(self.player_Computer, self.player_Human)	
				game_Won = self.is_Game_Over(self.player_Human)
				if game_Won == (True):
					print "Computer wins!"
							
			turn_Count += 1	