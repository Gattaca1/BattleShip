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
"""
column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
row = ['1','2','3','4','5','6','7','8','9','10']

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

enemy_Ships_And_Their_coordinates = {}

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

