class playerComputerEasy(playerComputer):

	def __init__(self):
		playerComputer.__init__(self)
		self.generate_Random_Queue_Targets()	

	def find_Future_Targets(self):
		#Add area around confirmed hits to a firing queue
		for confirmed_Hit_Coordinate in self.confirmed_Hit_Log:
			potential_Targets = self.all_Adjacent_Coords(confirmed_Hit_Coordinate)

			# Only add it if its not in the queue already
			# and if it hasn't been shot
			
			for target in potential_Targets:
				valid = self.is_Target_Valid(target)
				if valid == (True) and target not in self.target_Queue:
					self.target_Queue.append(target)