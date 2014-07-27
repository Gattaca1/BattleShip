from player import player

class playerHuman(player):

	def __init__(self, column, row, ships):
		self.column = column
		self.row = row
		self.ships = ships
		player.__init__(self, self.column, self.row, self.ships)
		
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
	
			print "Shoot with the format A4"
			target = str(raw_input("[You]> ")).upper()
			valid = self.is_Target_Valid(target)
			target_Picked = valid
			
		return target