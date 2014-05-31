from sys import exit
from random import randint

class player(object):

	def __init__(self):
		self.ship_Board = shipBoard()
		self.firing_Board = firingBoard()
				
	def shot_Fired(self, shot, boat):
		self.firing_Board.shoot_Target(shot, boat)		
		
	def shot_Received(self, coordinates):
		#modify ship board
		boat_Hit = self.ship_Board.shot_incoming(coordinates)
	
	def is_Boat_Hit(self, coordinate):
		boat_Hit = self.ship_Board.is_A_Boat_At_Coordinates(coordinate)
		return boat_Hit
		
	def what_Boat_Hit(self, coordinate):
		boat = self.ship_Board.ship_At_Coordinates(coordinate)
		return boat
		
	def did_Shot_Sink_Boat(self, ship):
		ship_Sunk = self.ship_Board.is_Ship_Sunk(ship)
		return ship_Sunk
		
	def are_Ships_Remaining(self):
		#return true if any ships are remaining
		if self.ship_Board.ship_Positions_Remaining() != 0:
			return (True)
		elif self.ship_Board.ship_Positions_Remaining() == 0:
			return (False)
		else:
			print 'error in are_Ships_Remaining'

	def is_Target_Valid(self, target):
		valid = self.firing_Board.valid_Target(target)
		return valid
			
	def enemy_Ship_Coordinate(self, coordinate, ship):
		pass
	
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
			target = str(raw_input("[You]> ")).upper()
			valid = self.firing_Board.valid_Target(target)
			target_Picked = valid
			
		return target
		
		
class playerComputer(player):
	"""
	Difficulty Easy:
		Shoots every other square until a Target is hit. Fires around the entirety of the target.
		
	Difficulty Medium:
		Shoots every other square until a target is hit. Determines the ships vector and discontinues
		shooting when the ship has sunk.
		
	Difficulty Hard:
		Determines the probability of ship positions, and shoots at the most likely. When a target is 
		found, a vector will be determined and shooting will cease once the target is sunk.
		
	"""
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
		self.enemy_Ships_And_Their_coordinates = {}
		self.rand_Queue = []		
		self.firing_Queue = []		
		self.shot_Log = []
		self.column = self.firing_Board.column
		self.row = self.firing_Board.row
		self.ship_Lengths = self.firing_Board.ships
		
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
			target = self.computer_Logic()
			valid = self.firing_Board.valid_Target(target)
			target_Picked = valid
		
		print "[Computer]> " + target
		return target
		
	def enemy_Ship_Coordinate(self, coordinate, ship):
		if ship not in self.enemy_Ships_And_Their_coordinates:
			self.enemy_Ships_And_Their_coordinates[ship] = []
		self.enemy_Ships_And_Their_coordinates[ship].append(coordinate)

	def generate_Random_Queue_Targets(self):
		column = self.column
		row = self.row
		
		#fire only on every other square
		if self.rand_Queue == []:
			for i in column:
				if column.index(i) % 2 == 0:
					# If column is even, fire on odd row
					for n in row:
						if row.index(n) % 2 == 1:
							self.rand_Queue.append((i + n))
				if column.index(i) % 2 == 1:
					for n in row:
						if row.index(n) % 2 == 0:
							self.rand_Queue.append((i + n))

	def all_Adjacent_Coords(self, starting_Coord):
		column = self.column
		row = self.row

		starting_Coord_Column_Letter = starting_Coord[:1]
		starting_Coord_Row_Number = starting_Coord[1:]

		#confirmed hit column index
		starting_Coord_Column_Index = column.index(starting_Coord_Column_Letter)
		starting_Coord_Row_Index = row.index(starting_Coord_Row_Number)

		potential_Targets = []

		first_Column_Letter = (column[0])
		last_Column_Letter = (column[-1])
		first_Row_Number = (row[0])
		last_Row_Number = (row[-1])
		
		if starting_Coord_Column_Letter != last_Column_Letter:
			#add 1 to column
			#C3
			potential_Targets.append((column[(starting_Coord_Column_Index + 1)] + starting_Coord_Row_Number))
		if starting_Coord_Column_Letter != first_Column_Letter:
			#subtract 1 from column
			#A3
			potential_Targets.append((column[(starting_Coord_Column_Index - 1)] + starting_Coord_Row_Number))
		if starting_Coord_Row_Number != last_Row_Number:
			#add 1 to row
			#B4
			potential_Targets.append((starting_Coord_Column_Letter + row[(starting_Coord_Row_Index + 1)]))
		if starting_Coord_Row_Number != first_Row_Number:
			#subtract 1 from row
			#B2
			potential_Targets.append((starting_Coord_Column_Letter + row[(starting_Coord_Row_Index - 1)]))

		return (potential_Targets)


class playerComputerEasy(playerComputer):

	def __init__(self):
		playerComputer.__init__(self)
		self.boat_Hit_Log = []
		self.generate_Random_Queue_Targets()		
		
	def shot_Fired(self, coordinate, is_Boat_Hit):
		self.firing_Board.shoot_Target(coordinate, is_Boat_Hit)
		self.shot_Log.append(coordinate)
		if coordinate in self.rand_Queue:
			self.rand_Queue.remove(coordinate)		
		if is_Boat_Hit == (True):
			self.boat_Hit_Log.append(coordinate)	

	def computer_Logic(self):	
		#Add items to the firing queue
		self.future_Targets()
		
		if self.firing_Queue != []:		
			target = randint(0, (len(self.firing_Queue) - 1))
			return (self.firing_Queue.pop(target))
			
		else:
			target = self.rand_Queue[(randint(0, (len(self.rand_Queue) - 1)))]
			return target

	def future_Targets(self):
		#Add area around confirmed hits to a firing queue
		for confirmed_Hit_Coordinate in self.boat_Hit_Log:
			potential_Targets = self.all_Adjacent_Coords(confirmed_Hit_Coordinate)

			# Only add it if its not in the queue already
			# and if it hasn't been shot
			
			for target in potential_Targets:
				valid = self.firing_Board.valid_Target(target)
				if valid == (True) and target not in self.firing_Queue:
					self.firing_Queue.append(target)

class playerComputerMedium(playerComputer):
	#If 2 coordinates are known of an enemy ship, you can be sure of its vector (vertical/horizontal).
	#if 1 coordinate is kown of an enemy ship, gonna have to shoot around to find its vector.
	#only add 1 thing to the firing queue at a time. that way you never have to derive the logic to decide
	#if something needs to be removed.

	def __init__(self):
		playerComputer.__init__(self)
		self.generate_Random_Queue_Targets()

	def shot_Fired(self, coordinate, is_Boat_Hit):
		self.firing_Board.shoot_Target(coordinate, is_Boat_Hit)
		self.shot_Log.append(coordinate)
		if coordinate in self.rand_Queue:
			self.rand_Queue.remove(coordinate)

	def computer_Logic(self):
		num_Of_Enemy_Ships_Hit = (len(self.enemy_Ships_And_Their_coordinates))

		if num_Of_Enemy_Ships_Hit >= 1:
			self.add_Potential_Target_To_Firing_Queue()

		if len(self.firing_Queue) >= 1:
			target = (self.firing_Queue.pop((len(self.firing_Queue) - 1)))
			print "firing_Queue >= 1 and target is: " + target
			return target
		else:
			target = self.rand_Queue[(randint(0, (len(self.rand_Queue) - 1)))]
			return target

	def add_Potential_Target_To_Firing_Queue(self):
		#have any ships been hit that are not yet sunk? better try and sink that ship
		#are two coordinates known, or just one?
		target_Added = (False)
		can_Target_Be_Added = (True)

		while target_Added == (False) and can_Target_Be_Added == (True):

			for ship in self.enemy_Ships_And_Their_coordinates:
				num_Of_Coordinates_Hit_On_Ship = len(self.enemy_Ships_And_Their_coordinates[ship])
				ship_Length = self.ship_Lengths[ship]
				
				#see if it has 1 coordinate, or 2+
				if num_Of_Coordinates_Hit_On_Ship == 1:
					target = self.rand_Coord_Adjacent_To_Confirmed_Hit(ship)
					valid = self.is_Target_Valid(target)

					if valid == (True):
						self.firing_Queue.append(target)
						target_Added = (True)

				elif num_Of_Coordinates_Hit_On_Ship >= 2 and num_Of_Coordinates_Hit_On_Ship < ship_Length:
					target = self.rand_Coord_Along_Vector_Of_Confirmed_Hits(ship)
					valid = self.is_Target_Valid(target)

					if valid == (True):
						self.firing_Queue.append(target)
						target_Added = (True)

			#Just incase, this breaks the loop
			can_Target_Be_Added = (False)

	def rand_Coord_Adjacent_To_Confirmed_Hit(self, ship):
		# confirmed_Hit = B3
		# Add to potential_Targets: B2, B4, A3, C3
		confirmed_Hit_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		potential_Targets = self.all_Adjacent_Coords(confirmed_Hit_Coordinate)
		print "rand_Coord_Adjacent_To_Confirmed_Hit potential_Targets: " + str(potential_Targets)
		for target in potential_Targets:
			valid = self.firing_Board.valid_Target(target)

			if valid == (False):
				potential_Targets.remove(target)
		print "potential_Targets after non valids removed: " + str(potential_Targets)
		random_Target = potential_Targets[randint(0, (len(potential_Targets) - 1))]
		return random_Target
		
	def rand_Coord_Along_Vector_Of_Confirmed_Hits(self, ship):
		"""Will never be executed if ship is already sunk."""
		#compare 2 confirmed ship coordinates and see if they are in the same column or row
		#just compare point 1 & 2 and then add and subtract 1 to each and see of those
		#are in the shot log, but not in the shipHit log
		#determine the endpoints, and fire at one beyond that.
		#check to see if the coordinate beyond that is valid (eg, hasn't been shot at yet)
		#also check to see if the coordinate is at a wall or not
		first_Confirmed_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		second_Confirmed_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][1]

		first_Coordinate_Column_Letter = first_Confirmed_Coordinate[:1]
		first_Coordinate_Row_Number = first_Confirmed_Coordinate[1:]
		second_Coordinate_Column_Letter = second_Confirmed_Coordinate[:1]
		second_Coordinate_Row_Number = second_Confirmed_Coordinate[1:]

		#is the matching vector horizontal or vertical?
		matching_Vector = ''
		if first_Coordinate_Column_Letter == second_Coordinate_Column_Letter:
			matching_Vector = 'horizontal'
		elif first_Coordinate_Row_Number == second_Coordinate_Row_Number:
			matching_Vector = 'vertical'

		column = self.column
		row = self.row

		first_Coordinate_Column_Index = column.index(first_Coordinate_Column_Letter)
		first_Coordinate_Row_Index = row.index(first_Coordinate_Row_Number)

		#find the furthest points shot on both ends of the ship
			#See if 1 past that is in the shot log
		potential_Targets = []
		target_Added = (False)
		increment = 1
		while target_Added == (False):
			previous_Increment = (increment - 1)

			if matching_Vector == 'horizontal':
				#try increase vector
				previous_Increased_Vector = (first_Coordinate_Column_Letter + row[(first_Coordinate_Row_Index + previous_Increment)])
				if previous_Increased_Vector in self.enemy_Ships_And_Their_coordinates[ship]:
					increased_Vector = (first_Coordinate_Column_Letter + row[(first_Coordinate_Row_Index + increment)])
					potential_Targets.append(increased_Vector)

				#try decrease vector
				decreased_Vector = (first_Coordinate_Column_Letter + row[(first_Coordinate_Row_Index - increment)])
				potential_Targets.append(decreased_Vector)

			elif matching_Vector == 'vertical':
				#try increase vector
				increased_Vector = (column[(first_Coordinate_Column_Index + increment)] + first_Coordinate_Row_Number)
				potential_Targets.append(increased_Vector)

				#try decrease vector
				decreased_Vector = (column[(first_Coordinate_Column_Index - increment)] + first_Coordinate_Row_Number)
				potential_Targets.append(decreased_Vector)

			for target in potential_Targets:
				if target in self.enemy_Ships_And_Their_coordinates[ship]:
					potential_Targets.remove(target)
				if target in self.shot_Log:
					pass
			"""
			Gotta stop it from doing this:
			turn1) _ _ [#] (X) (X) _ _ 
			turn2) _ _ [#] (X) (X) () _
			turn3) _ _ [#] (X) (X) ()()
			"""
			increment = increment + 1
			
		
"""	
class playerComputerHard(playerComputer):

	def __init__(self):
		playerComputer.__init__(self)
"""	
	
class gameBoard(object):

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
		self.not_Hit_Boat_Occupied_Coordinates = []
			#old name = self.ships_Left
		self.ship_Positions = {}
		self.initialize_Ships()		
		
	def shot_incoming(self, coordinate):
		#modify the ship board
		#remove coordinate from ships_Left
		self.board[coordinate][1] = ('hit')
		if self.is_A_Boat_At_Coordinates(coordinate) == (True):
			self.not_Hit_Boat_Occupied_Coordinates.remove(coordinate)		
	
	def is_A_Boat_At_Coordinates(self, coordinate):
		#old name = was_Boat_Hit
		if coordinate in self.not_Hit_Boat_Occupied_Coordinates:
			return (True)
		else:
			return (False)		
		
	def ship_At_Coordinates(self, coordinate):
		#old name = ship_Hit
		for ship in self.ship_Positions:
			if coordinate in self.ship_Positions[ship]:
				return ship				
				
	def is_Ship_Sunk(self, ship):
		coordinates_Left = []
		for coordinate in self.ship_Positions[ship]:
			if coordinate in self.not_Hit_Boat_Occupied_Coordinates:
				coordinates_Left.append(coordinate)
		if coordinates_Left == []:
			return (True)
		else:
			return (False)		
		
	def ship_Positions_Remaining(self):
		#old name = ships_Remaining
		return (len(self.not_Hit_Boat_Occupied_Coordinates))		
		
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
			self.not_Hit_Boat_Occupied_Coordinates.append(coordinate)
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
			
	def shoot_Target(self, coordinate, is_Boat_Hit):
		self.board[coordinate][1] = 'hit'
		if is_Boat_Hit == (True):
			self.board[coordinate][0] = 'boat'
		
		
class gameEngine(object):

	def __init__(self):
		self.player_Computer = self.select_Difficulty()
		self.player_Human = playerHuman()
		self.player_Order = self.player_Turn_Order()
		
	def select_Difficulty(self):
	
		difficulty_Set = (False)
		
		while difficulty_Set == (False):
			print "Select difficulty: Easy, Medium, Hard"
			difficulty = raw_input("> ").upper()
			
			if difficulty == ('EASY'):
				return playerComputerEasy()
				difficulty_Set = (True)
				
			if difficulty == ('MEDIUM'):
				return playerComputerMedium()
				difficulty_Set = (True)
				
			if difficulty == ('HARD'):
				return playerComputerEasy()
				difficulty_Set = (True)

				
	def shoot(self, friendly, tango, destination):
		#was a boat hit?
		is_Boat_Hit = tango.is_Boat_Hit(destination)
		
		#shoot
		tango.shot_Received(destination)
		
		is_Ship_Sunk = (False)
		#what boat was hit
		if is_Boat_Hit == (True):
			boat_Hit = tango.what_Boat_Hit(destination)
			print boat_Hit + " Hit"
			
			#pass the boat name to the friendly player to keep track of boats they've hit
			friendly.enemy_Ship_Coordinate(destination, boat_Hit)
			
			#did the shot sink the ship
			is_Ship_Sunk = tango.did_Shot_Sink_Boat(boat_Hit)
			if is_Ship_Sunk == (True):
				print boat_Hit + " Sunk"
				
		#modify firing board
		friendly.shot_Fired(destination, is_Boat_Hit)
				
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
