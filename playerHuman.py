from player import player

class playerHuman(player):

	def __init__(self, column, row, ships, roll):
		self.name = "You"
		self.roll = roll
		player.__init__(self, column, row, ships)
		
	def pick_Target(self):
		# returns the target in format 'A4'
		
		target_Picked = (False)
		while target_Picked == (False):
	
			print "Shoot with the format A4"
			target = str(raw_input("[You]> ")).upper()
			valid = self.is_Target_Valid(target)
			target_Picked = valid
			
		return target

	def return_Board_Info(self):
		""" Returns a list of 4 items, each item being a list. They are as follows:
		1) all occupied Coordinates
		2) all shots received
		3) all shots fired
		4) all shots hit
		"""
		#my occupied coordinates
		#shots received
		#shots fired
		#shots hit
		board_Info = []
		board_Info.append(self.occupied_Coordinates)
		board_Info.append(self.shots_Received_Log)
		board_Info.append(self.shots_Fired_Log)
		board_Info.append(self.shots_Fired_Hit_Log)
		return board_Info