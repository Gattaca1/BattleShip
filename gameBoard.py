class gameBoard(object):

	def __init__(self, column, row):	
		self.column = column 
		# ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

		self.row = row 
		# ['1','2','3','4','5','6','7','8','9','10']
		
		self.board = {}	
		self.create_Board()

	def create_Board(self):	
		for letter in self.column:
			for num in self.row:
				if board == ('firing'):
					self.board[letter + num] = ['noBoat', 'noHit']
	
	def format_Coordinates(self, key):	
		if self.board[key][0] == 'noBoat' and self.board[key][1] == 'noHit':
			return ""
		elif self.board[key][0] == 'boat' and self.board[key][1] == 'noHit':
			return "[#]"
		elif self.board[key][0] == 'noBoat' and self.board[key][1] == 'hit':
			return "( )"
		elif self.board[key][0] == 'boat' and self.board[key][1] == 'hit':
			return "(X)"		
		
	def display_Coordinates(self):		
		row_Header = ''
		for num in self.row:
			row_Header = row_Header + ('\t' + (num))
		print row_Header
		print ""
		
		for letter in self.column:
			row_Body = '' + letter
			for num in self.row:
				row_Body = row_Body + ('\t' + (self.format_Coordinates(letter + num)))
			print row_Body
			print ""

	def display_Board(self, board_Name):
		print "						" + board_Name
		print ""
		display_Coordinates()

	def update_Board(self, boat_Coordinates, firing_Coordinates):
		for coordinate in boat_Coordinates:
			self.board[coordinate][0] == 'boat'
		for coordinate in firing_Coordinates:
			self.board[coordinate][1] == 'hit'		