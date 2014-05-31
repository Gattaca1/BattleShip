"""
class myEggs(object):
	def __init__(self):
		self.cock = '-1'
		
	def shit_Stain(self):
		print 'Open My Eggs'
		
	def pregnant(self):
		print "i've got bad news 4 u"
		
		
class subHub(myEggs):
	def __init__(self):
		self.vaselineslug = 'lets slide around on the floor'
		myEggs.__init__(self)
		
	def shit_Stain(self):
		print 'Sub the shit Stain Hub'
		
	def print_Cock(self):
		print self.cock
		
	def print_Vaseline_Slug(self):
		print self.vaselineslug
		
		
ballsack = subHub()
ballsack.shit_Stain() #sub the shit stain hub
ballsack.pregnant() #i've got bad news 4 u
ballsack.print_Cock() #-1
ballsack.print_Vaseline_Slug() #lets slide around on the floor

nutsack = myEggs()
nutsack.shit_Stain() #open my eggs
"""

column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
row = ['1','2','3','4','5','6','7','8','9','10']
"""
tempStr = ''
for num in row:
	tempStr = tempStr + ('\t' + (num))
print tempStr
print ''
for letter in column:
	strToPrint = '' + letter
	for num in row:
		strToPrint = strToPrint + ('\t' + (letter + num))
	print strToPrint
	print ''
"""
"""

enemy_Ships_And_Their_coordinates = {}
ship_Lengths = {
		'Battleship':3,
		'Submarine':3,
		'Carrier':5,
		'Tug':2
		}

def enemy_Ship_Coordinate(coordinate, ship):
		if ship not in enemy_Ships_And_Their_coordinates:
			enemy_Ships_And_Their_coordinates[ship] = []
		enemy_Ships_And_Their_coordinates[ship].append(coordinate)

enemy_Ship_Coordinate('A1', 'Tug')
enemy_Ship_Coordinate('A2', 'Tug')
enemy_Ship_Coordinate('A3', 'Battleship')
enemy_Ship_Coordinate('B3', 'Battleship')
enemy_Ship_Coordinate('C3', 'Battleship')
print enemy_Ships_And_Their_coordinates

print len(enemy_Ships_And_Their_coordinates)
"""

def rand_Coord_Adjacent_To_Confirmed_Hit():
	# confirmed_Hit = B3
	# Add to potential_Targets: B2, B4, A3, C3
	confirmed_Hit_Coordinate = 'B3'

	#column = self.column
	#row = self.row

	confirmed_Hit_Column_Letter = confirmed_Hit_Coordinate[:1]
	confirmed_Hit_Row_Number = confirmed_Hit_Coordinate[1:]

	#confirmed hit column index
	confirmed_Hit_Column_Index = column.index(confirmed_Hit_Column_Letter)
	confirmed_Hit_Row_Index = row.index(confirmed_Hit_Row_Number)

	potential_Targets = []

	first_Column_Letter = (column[0])
	last_Column_Letter = (column[-1])
	first_Row_Number = (row[0])
	last_Row_Number = (row[-1])
	
	if confirmed_Hit_Column_Letter != last_Column_Letter:
		#add 1 to column
		#C3
		potential_Targets.append((column[(confirmed_Hit_Column_Index + 1)] + confirmed_Hit_Row_Number))
	if confirmed_Hit_Column_Letter != first_Column_Letter:
		#subtract 1 from column
		#A3
		potential_Targets.append((column[(confirmed_Hit_Column_Index - 1)] + confirmed_Hit_Row_Number))
	if confirmed_Hit_Row_Number != last_Row_Number:
		#add 1 to row
		#B4
		potential_Targets.append((confirmed_Hit_Column_Letter + row[(confirmed_Hit_Row_Index + 1)]))
	if confirmed_Hit_Row_Number != first_Row_Number:
		#subtract 1 from row
		#B2
		potential_Targets.append((confirmed_Hit_Column_Letter + row[(confirmed_Hit_Row_Index - 1)]))

	print potential_Targets


target_Added = (False)
while target_Added == (False):
	for (i = 0, i < 10, i++):
		#increase vector loop
		#decrease vector loop
		print 'Incriment = ' + str(i)
