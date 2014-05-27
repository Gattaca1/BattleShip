from sys import exit
from random import randint


class player(object):

	def __init__(self):
	
		self.ship_Board = gameBoard()
		self.ship_Board.initialize_Ships()
		self.firing_Board = gameBoard()
		self.shot_Log = []
		self.firing_Queue = []
		self.boat_Hit_Log = []
		self.rand_Queue = []
		
		
	def shots_Fired(self, shot):
	
		self.shot_Log.append(shot)
		self.firing_Board.board[shot][1] = ('hit')
		if shot in self.rand_Queue:
			self.rand_Queue.remove(shot)
		
		
	def hit_Boat(self, shot):
	
		self.boat_Hit_Log.append(shot)
		self.firing_Board.board[shot][0] = ('boat')
		
		
	def display_Boards(self):
	
		print "						Firing Board"
		print ""
		self.firing_Board.display_Board()
		print "						Ship Board"
		print ""
		self.ship_Board.display_Board()
		
		
	def game_Status(self):
		
		if self.ship_Board.ships_Left == []:
			return (True)
		return (False)
		
		
	def computer_Logic(self):
	
		#Add items to the firing queue
		self.future_Targets()
		
		if self.firing_Queue != []:
		
			target = randint(0, (len(self.firing_Queue) - 1))
			return (self.firing_Queue.pop(target))
			
		else:
			column = self.firing_Board.column
			row = self.firing_Board.row
			
			#fire only on every other square
			if self.rand_Queue == []:
				for i in column:
					if column.index(i) % 2 == 0:
						for n in row:
							if row.index(n) % 2 == 0:
								self.rand_Queue.append((i + n))
					elif column.index(i) % 2 != 0:
						for n in row:
							if row.index(n) % 2 != 0:
								self.rand_Queue.append((i + n))
			
			target = self.rand_Queue[(randint(0, (len(self.rand_Queue) - 1)))]
			return target
		
		
	def future_Targets(self):
		
		#Add area around confirmed hits to a firing queue
		for item in self.boat_Hit_Log:
			
			# Only add it if its not in the queue already
			# and if it hasn't been shot
			column_Letter = item[:1]
			row_Number = item[1:]			
			column_Pos = self.firing_Board.column.index(column_Letter)
			row_Pos = self.firing_Board.row.index(row_Number)			
			potential_Targets = []
			
			if column_Pos != (9):
				#add 1 to column
				potential_Targets.append((self.firing_Board.column[(column_Pos + 1)] + row_Number))
			if column_Pos != (0):
				#subtract 1 from column
				potential_Targets.append((self.firing_Board.column[(column_Pos - 1)] + row_Number))
			if row_Pos != (9):
				#add 1 to row
				potential_Targets.append((column_Letter + self.firing_Board.row[(row_Pos + 1)]))
			if row_Pos != (0):
				#subtract 1 from row
				potential_Targets.append((column_Letter + self.firing_Board.row[(row_Pos - 1)]))
			
			for target in potential_Targets:
				valid = self.firing_Board.valid_Target(target)
				if target not in self.shot_Log and valid == (True) and target not in self.firing_Queue:
					self.firing_Queue.append(target)
			
class playerComputer(player):
	pass
	
class gameBoard(object):

	def __init__(self):
	
		self.column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
		self.row = ['1','2','3','4','5','6','7','8','9','10']	
		self.ships_Left = []
		self.ships = {
		'battleship':3,
		'submarine':3,
		'carrier':5,
		'tug':2
		}
		
		self.board = {}
		self.create_Board()
		
				
	def create_Board(self):
	
		for letter in self.column:
			for num in self.row:
				self.board[letter + num] = ['noBoat', 'noHit']
				
	####################################################### BOARD DISPLAY ##########################################################################			
	def format_Board(self, key):
	
		if self.board[key][0] == 'noBoat' and self.board[key][1] == 'noHit':
			return ""
		elif self.board[key][0] == 'boat' and self.board[key][1] == 'noHit':
			return "[#]"
		elif self.board[key][0] == 'noBoat' and self.board[key][1] == 'hit':
			return "( )"
		elif self.board[key][0] == 'boat' and self.board[key][1] == 'hit':
			return "(X)"
		
		
	def display_Board(self):
		
		print "		%s	%s	%s	%s	%s	%s	%s	%s	%s	%s" % (
		self.row[0], self.row[1], self.row[2], self.row[3], self.row[4],
		self.row[5], self.row[6], self.row[7], self.row[8], self.row[9],
		)
		print ""
		
		for letter in self.column:
			print "	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s" % (letter,
			self.format_Board(letter + self.row[0]), self.format_Board(letter + self.row[1]), 
			self.format_Board(letter + self.row[2]), self.format_Board(letter + self.row[3]), 
			self.format_Board(letter + self.row[4]), self.format_Board(letter + self.row[5]), 
			self.format_Board(letter + self.row[6]), self.format_Board(letter + self.row[7]), 
			self.format_Board(letter + self.row[8]), self.format_Board(letter + self.row[9])
			)
			print ""
		
	####################################################### BOARD SHOOTING ##########################################################################	
	def shot_Received(self, coordinate):
	
		#modify the ship board
		#remove from shipsLeft
		self.board[coordinate][1] = ('hit')
		if coordinate in self.ships_Left:
			self.ships_Left.remove(coordinate)
			return (True)
		return (False)
		
	def valid_Target(self, target):
		#Not valid if target does not exist or if target has already been hit
		if target not in self.board:
			return (False)
		elif self.board[target][1] == 'hit':
			return (False)
		else:
			return (True)
			
	####################################################### SHIPS ##################################################################################	
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
					self.assign_Ship_Coordinates(ship_Coordinates)
		#print "Ship list: %s" % (self.ships_Left)
									
					
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
				i += 1
			if vector == 'down':
				#add to column
				ship_Coordinates.append((self.column[(col_Pos + i)] + row_Val))
				i += 1
			if vector == 'left':
				#subtract from row
				ship_Coordinates.append((col_Val + (self.row[(row_Pos - i)])))
				i += 1
			if vector == 'right':
				#add to row
				ship_Coordinates.append((col_Val + (self.row[(row_Pos + i)])))
				i += 1
		return (ship_Coordinates)
		
		
	def validate_Ship_Coordinates(self, set_Coordinates):
		
		#return True if valid, False if not valid
		#a valid set of coordinates is one in which no coordinate in the set is occupied by a ship
		for coordinate in set_Coordinates:
			if self.board[coordinate][0] == ('boat'):
				return (False)		
		return (True)
		
		
	def assign_Ship_Coordinates(self, set_Coordinates):
	
		#given a set of coordinates, set each coordinate to occupied by boat
		for coordinate in set_Coordinates:
			self.board[coordinate][0] = ('boat')
			self.ships_Left.append(coordinate)
												

class gameEngine(object):

	def __init__(self):
		self.player_Computer = player()
		self.player_Human = player()
		
	def shoot(friendly, tango, destination):	
	
		#modify friendly firing board
		#write shot to friendly firing log
		friendly.shots_Fired(destination)
	
		#modify tango ship board
		#if it hits a boat, remove it from tango boats left list
		boat_Hit = tango.ship_Board.shot_Received(destination)
	
		if boat_Hit == (True):
	
			#if it hits a boat write to friendly boat hit log
			friendly.hit_Boat(destination)
			print "%s hit a boat!" % (destination)		
			
	
	def whose_Turn(player_List, turn_Count):

		if turn_Count % 2 == 0:
			return player_List[0]
		return player_List[1]
	
	def turn_Actions():
		#pick target
		#validate target
		#call shoot
		pass
	
	def game_Status():
		pass
	
	def turn_Order():
		pass
		
	def play_Game():

		game_Won = (False)
		turn_Count = 0
		
		players = [player_Human, player_Computer]
		# If a human is playing, set as player 1 (index 0)
	
		player1 = players[0]
		player2 = players[1]
		while game_Won == (False):
	
			turn = whose_Turn(players, turn_Count)
		
			if turn == player_Human:
				"""Turn order: 1) display board, 2) pick target, 3) check target(maybe refire), 4)launch missle"""
			
				player1.display_Boards()
				destination = pick_Target_Human(player1)
				shoot(player1, player_Computer, destination)
				game_Won = player_Computer.game_Status()
				if game_Won == (True):
					print "You win!"
				
			if turn == player_Computer:
						
				destination = pick_Target_Computer(player2)
				print "[Computer]> %s" % (destination)
				shoot(player2, player1, destination)
				game_Won = player1.game_Status()
				if game_Won == (True):
					print "Computer wins!"
							
			turn_Count += 1	
	
	
def pick_Target_Human(player):

	# returns the target in format 'A4'
	target_Picked = (False)
	while target_Picked == (False):
	
		print "Shoot with the format A4"
		target = str(raw_input("[You]> "))
		if target == ('exit'):
			exit()
		validity = player.firing_Board.valid_Target(target)
		target_Picked = validity
			
	return target	
		
		
def pick_Target_Computer(player):

	# returns the target in format 'A4'
	target_Picked = (False)
	while target_Picked == (False):
		target = player.computer_Logic()
		validity = player.firing_Board.valid_Target(target)
		target_Picked = validity
			
	return target
	
	
def play_Again():
	
	restart = ''
	while restart != 'y' and restart != 'n':
		print "Play again? answer with y or n"
		restart = raw_input("> ")
		
	if restart == 'y':
		return (True)
		
	else:
		exit()
		
		
def initiate_Game():

	new_Game = (True)
	while new_Game == (True):
		play_Game()
		new_Game = play_Again()
	
	
initiate_Game()