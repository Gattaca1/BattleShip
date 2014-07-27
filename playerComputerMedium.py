class playerComputerMedium(playerComputer):
	#If 2 coordinates are known of an enemy ship, you can be sure of its vector (vertical/horizontal).
	#if 1 coordinate is kown of an enemy ship, gonna have to shoot around to find its vector.
	#only add 1 thing to the firing queue at a time. that way you never have to derive the logic to decide
	#if something needs to be removed.

	def __init__(self):
		playerComputer.__init__(self)
		self.generate_Random_Queue_Targets()

	def find_Future_Targets(self):
		#grab a target from the firing log. If its empty then default to a random shot.

		num_Of_Enemy_Ships_Hit = (len(self.enemy_Ships_And_Their_coordinates))

		if num_Of_Enemy_Ships_Hit > (0):
			self.add_Potential_Target_To_Firing_Queue()

	def add_Potential_Target_To_Firing_Queue(self):
		#have any ships been hit that are not yet sunk? better try and sink that ship
		#are two coordinates known, or just one?

		for ship in self.enemy_Ships_And_Their_coordinates:
			num_Of_Coordinates_Hit_On_Ship = len(self.enemy_Ships_And_Their_coordinates[ship])
			ship_Length = self.ship_Lengths[ship]

			if num_Of_Coordinates_Hit_On_Ship != ship_Length:			
				#see if it has 1 coordinate, or 2+
				if num_Of_Coordinates_Hit_On_Ship == 1:
					target = self.rand_Coord_Adjacent_To_Confirmed_Hit(ship)

				elif num_Of_Coordinates_Hit_On_Ship < ship_Length:
					target = self.rand_Coord_Along_Vector_Of_Confirmed_Hits(ship)
				else:
					print "error in add_Potential_Target_To_Firing_Queue"
				valid = self.is_Target_Valid(target)
				if valid == (True):
					self.target_Queue.append(target)
			else:
				pass

	def rand_Coord_Adjacent_To_Confirmed_Hit(self, ship):
		# confirmed_Hit = B3
		# Add to potential_Targets: B2, B4, A3, C3
		confirmed_Hit_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		potential_Targets = self.all_Adjacent_Coords(confirmed_Hit_Coordinate)
		for target in potential_Targets:
			valid = self.is_Target_Valid(target)

			if valid == (False):
				potential_Targets.remove(target)
		random_Target = potential_Targets[randint(0, (len(potential_Targets) - 1))]
		return random_Target
		
	def rand_Coord_Along_Vector_Of_Confirmed_Hits(self, ship):
		"""Will never be executed if ship is already sunk."""

		matching_Vector = self.determine_Vector(ship)
		if matching_Vector == 'horizontal':
			target = self.closest_Coordinate_Along_Horizontal_Vector(ship)
		elif matching_Vector == 'vertical':
			target = self.closest_Coordinate_Along_Vertical_Vector(ship)

		target_Valid = self.is_Target_Valid(target)
		if target_Valid == (True):
			return target

	def determine_Vector(self, ship):
		first_Confirmed_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		second_Confirmed_Coordinate = self.enemy_Ships_And_Their_coordinates[ship][1]

		first_Coordinate_Column_Letter = first_Confirmed_Coordinate[:1]
		first_Coordinate_Row_Number = first_Confirmed_Coordinate[1:]

		second_Coordinate_Column_Letter = second_Confirmed_Coordinate[:1]
		second_Coordinate_Row_Number = second_Confirmed_Coordinate[1:]

		if first_Coordinate_Column_Letter == second_Coordinate_Column_Letter:
			matching_Vector = 'horizontal'
		elif first_Coordinate_Row_Number == second_Coordinate_Row_Number:
			matching_Vector = 'vertical'

		return matching_Vector

	def closest_Coordinate_Along_Horizontal_Vector(self, ship):
		"""Return the closest valid horizontal coordinate"""

		column = self.column
		row = self.row

		coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		coordinate_Column_Letter = coordinate[:1]
		coordinate_Row_Number = coordinate[1:]
		coordinate_Row_Index = row.index(coordinate_Row_Number)

		num_Of_Coordinates_Hit_On_Ship = len(self.enemy_Ships_And_Their_coordinates[ship])
		ship_Length = self.ship_Lengths[ship]
		
		#fire right until it misses
		#then fire left until it misses.
		#ship should be sunk.

		# increase vector
		increment = 0
		while increment < ship_Length:
			increment = (increment + 1)

			# Make sure its not against the right edge
			previous_Increased_Vector = ''
			previous_Increment = (increment - 1)
			if (coordinate_Row_Index + increment) <= (len(row) - 1):			
				previous_Increased_Vector = (coordinate_Column_Letter + row[(coordinate_Row_Index + previous_Increment)])
			else:
				continue

			# If previous vector was a confirmed hit, move right 1
			increased_Vector = ''	
			if previous_Increased_Vector in self.enemy_Ships_And_Their_coordinates[ship]:
				increased_Vector = (coordinate_Column_Letter + row[(coordinate_Row_Index + increment)])
			else:
				continue

			# Check that the target hasn't already been shot at	
			valid = (False)
			if increased_Vector not in self.shots_Fired_Log:
				valid = self.is_Target_Valid(increased_Vector)
			else:
				continue

			if valid == (True):
				return increased_Vector

		# decrease vector
		increment = 0
		while increment < ship_Length:
			increment = (increment + 1)

			# Make sure its not against the left edge
			previous_Decreased_Vector = ''
			previous_Increment = (increment - 1)
			if (coordinate_Row_Index - increment) >= (0):
				previous_Decreased_Vector = (coordinate_Column_Letter + row[(coordinate_Row_Index - previous_Increment)])
			else:
				continue

			# If the previous vector was a confirmed hit, move left 1
			decreased_Vector = ''	
			if previous_Decreased_Vector in self.enemy_Ships_And_Their_coordinates[ship]:
				decreased_Vector = (coordinate_Column_Letter + row[(coordinate_Row_Index - increment)])
			else:
				continue

			# Check that the target hasn't already been shot at
			valid = (False)
			if decreased_Vector not in self.shots_Fired_Log:
				valid = self.is_Target_Valid(decreased_Vector)
			else:
				continue
			
			if valid == (True):
				return decreased_Vector


	def closest_Coordinate_Along_Vertical_Vector(self, ship):
		"""Return the closest valid vertial coordinate"""

		column = self.column
		row = self.row

		coordinate = self.enemy_Ships_And_Their_coordinates[ship][0]
		coordinate_Column_Letter = coordinate[:1]
		coordinate_Row_Number = coordinate[1:]
		coordinate_Column_Index = column.index(coordinate_Column_Letter)		

		num_Of_Coordinates_Hit_On_Ship = len(self.enemy_Ships_And_Their_coordinates[ship])
		ship_Length = self.ship_Lengths[ship]

		#fire down until it misses
		#then fire up until it misses.
		#ship should be sunk.

		increment = 0
		while increment < ship_Length:
			increment = (increment + 1)

			# Make sure its not against the bottom edge
			previous_Increased_Vector = ''
			previous_Increment = (increment - 1)
			if (coordinate_Column_Index + increment) <= (len(column) - 1):
				previous_Increased_Vector = (column[(coordinate_Column_Index + previous_Increment)] + coordinate_Row_Number)
			else:
				continue

			# If the previous vector was a confirmed hit, move down 1
			increased_Vector = ''
			if previous_Increased_Vector in self.enemy_Ships_And_Their_coordinates[ship]:
				increased_Vector = (column[(coordinate_Column_Index + increment)] + coordinate_Row_Number)
			else:
				continue

			# Check that the target hasn't already been shot at	
			valid = (False)
			if increased_Vector not in self.shots_Fired_Log:
				valid = self.is_Target_Valid(increased_Vector)
			else:
				continue

			if valid == (True):
				return increased_Vector

		increment = 0
		while increment < ship_Length:
			increment = (increment + 1)

			# Make sure its not against the top edge
			previous_Decreased_Vector = ''			
			previous_Increment = (increment - 1)		
			if (coordinate_Column_Index - increment) >= (0):
				previous_Decreased_Vector = (column[(coordinate_Column_Index - previous_Increment)] + coordinate_Row_Number)
			else:
				continue

			#If the previous vector was a confirmed hit, move up 1
			decreased_Vector = ''
			if previous_Decreased_Vector in self.enemy_Ships_And_Their_coordinates[ship]:
				decreased_Vector = (column[(coordinate_Column_Index - increment)] + coordinate_Row_Number)
			else:
				continue

			# Check that the target hasn't already been shot at
			valid = (False)
			if decreased_Vector not in self.shots_Fired_Log:
				valid = self.is_Target_Valid(decreased_Vector)
			else:
				continue

			if valid == (True):
				return decreased_Vector