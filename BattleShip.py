from sys import exit
from random import randint

class player(object):

	def __init__(self):
		self.ship_Board = shipBoard()
		self.firing_Board = firingBoard()
		
		
	def shot_Fired(self, shot, boat):
		self.firing_Board.shoot_Target(shot, boat)
		
		
	def shot_Received(self, shot):
		#modify ship board
		boat_Hit = self.ship_Board.shot_incoming(shot)
		return boat_Hit
		
		
	def are_Ships_Remaining(self):
		#return true if any ships are remaining
		if self.ship_Board.ships_Remaining() != 0:
			return (True)
		if self.ship_Board.ships_Remaining() == 0:
			return (False)
		else:
			print 'error in are_Ships_Remaining'
	
	
class playerHuman(player):

	def __init__(self):
		player.__init__(self)
		
		
	def display_Boards(self):
	
		print "						Firing Board"
		print ""
		self.firing_Board.display_Board()
		print "						Ship Board"
		print ""
		self.ship_Board.display_Board()
			
			
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
	
			print "Shoot with the format A4"
			target = str(raw_input("[You]> "))
			valid = self.firing_Board.valid_Target(target)
			target_Picked = valid
			
		return target
		
		
class playerComputer(player):
	"""Computer has 2 AI targeting systems. The first is for when there is no hits have been made,
		and the second is to sink a ship once one has been found. 
		
		The way the first targeting system works is by seeing every way each ship can be arranged on the board, 
		and assigning the number of positions to each cell. The cell with the highest number of positions 
		will be the most likely to contain a ship. This will also only fire on every second cell. 
		
		The way the second targeting system works is it takes an initial coordinate which is a confirmed 
		hit. it then determines the 4 points surrounding the hit, and assigns them to be the next targets
		to shoot at. when one of those 4 points also confirms a hit, and the hit is on the same ship as the
		original, then the vector has been confirmed. once the vector is confirmed, it will drop the remaining
		targets from the queue, and make 2 new target coordinates on either endpoint. 
		"""
	def __init__(self):
		player.__init__(self)
		self.firing_Queue = []
		self.rand_Queue = []
		self.boat_Hit_Log = []
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
			target = self.computer_Logic()
			valid = self.firing_Board.valid_Target(target)
			target_Picked = valid
		
		print "[Computer]> " + target
		return target
		
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
					

class gameBoard(object):

	def __init__(self):
	
		self.column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
		self.row = ['1','2','3','4','5','6','7','8','9','10']	
		
		self.board = {}
		self.create_Board()
		
				
	def create_Board(self):
	
		for letter in self.column:
			for num in self.row:
				self.board[letter + num] = ['noBoat', 'noHit']
				
	
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
		
		row_Header = ''
		for num in self.row:
			row_Header = row_Header + ('\t' + (num))
		print row_Header
		print ""
		
		for letter in self.column:
			row_Body = '' + letter
			for num in self.row:
				row_Body = row_Body + ('\t' + (self.format_Board(letter + num)))
			print row_Body
			print ""
		

class shipBoard(gameBoard):

	def __init__(self):
		gameBoard.__init__(self)
		self.ships_Left = []
		self.ships = {
		'Battleship':3,
		'Submarine':3,
		'Carrier':5,
		'Tug':2
		}
		self.ship_Positions = {}
		self.initialize_Ships()
		
		
	def shot_incoming(self, coordinate):
		#check if a boat was hit
		#Announce what boat was hit
		#remove coordinate from ships_Left
		#modify the ship board
		self.board[coordinate][1] = ('hit')
		if coordinate in self.ships_Left:
			self.announce_Ship_Hit(coordinate)
			self.announce_Ship_Sunk(coordinate)
			self.ships_Left.remove(coordinate)
			return (True)
		else:
			return (False)
		
	
	def was_Boat_Hit(self, coordinate):
		if coordinate in self.ships_Left:
			return (True)
		else:
			return (False)
		
		
	def announce_Ship_Hit(self, coordinate):
		for ship in self.ship_Positions:
			if coordinate in self.ship_Positions[ship]:
				print ship + " Hit"
				
	def announce_Ship_Sunk(self, coordinate):
		pass
		
	def ships_Remaining(self):
		return (len(self.ships_Left))
		
		
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
		
		
	def assign_Ship_Coordinates(self, set_Coordinates, ship):
	
		#given a set of coordinates, set each coordinate to occupied by boat
		self.ship_Positions[ship] = []
		for coordinate in set_Coordinates:
			self.board[coordinate][0] = ('boat')
			self.ships_Left.append(coordinate)
			self.ship_Positions[ship].append(coordinate)
			
		
class firingBoard(gameBoard):

	def __init__(self):
		gameBoard.__init__(self)
		
	def valid_Target(self, target):
		#Not valid if target does not exist or if target has already been hit
		if target not in self.board:
			return (False)
		elif self.board[target][1] == 'hit':
			return (False)
		else:
			return (True)
			
	def shoot_Target(self, target, boat):
		self.board[target][1] = 'hit'
		if boat == (True):
			self.board[target][0] = 'boat'
		
		
class gameEngine(object):

	def __init__(self):
		self.player_Computer = playerComputer()
		self.player_Human = playerHuman()
		self.player_Order = self.player_Turn_Order()
		
	def shoot(self, friendly, tango, destination):
		#was a boat hit?
		boat = tango.shot_Received(destination)
		#modify firing board
		friendly.shot_Fired(destination, boat)
				
	def whose_Turn(self, turn_Count):
		if turn_Count % 2 == 0:
			return self.player_Order[0]
		return self.player_Order[1]
	
	def turn_Actions(self, offense, defense):
		"""return the destination"""
		#pick target and confirm valid
		destination = offense.pick_Target()
		self.shoot(offense, defense, destination)
		
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
				self.player_Human.display_Boards()
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
	
	
def play_Again():
	
	restart = ''
	while restart != 'y' and restart != 'n':
		print "Play again? answer with y or n"
		restart = raw_input("> ")
		
	if restart == 'y':
		return (True)
		
	else:
		return (False)
		
		
def initiate_Game():

	start_New_Game = (True)
	while start_New_Game == (True):
		game_Instance = gameEngine()
		game_Instance.play_Game()
		start_New_Game = play_Again()
	exit()
	
	
initiate_Game()