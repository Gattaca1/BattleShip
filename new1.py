from sys import exit
from random import randint
"""
	Difficulty Hard:
		Determines the probability of ship positions, and shoots at the most likely. When a target is 
		found, a vector will be determined and shooting will cease once the target is sunk.
	Computer has 2 AI targeting systems. The first is for when there is no hits have been made,
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
#\"""
column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
row = ['1','2','3','4','5','6','7','8','9','10']



enemy_Ships_And_Their_coordinates = {}
ship_Lengths = {
		'Carrier':5,
		'Battleship':4,
		'Cruiser':3,
		'Submarine':3,
		'Destroyer':2
		}

def enemy_Ship_Coordinate(coordinate, ship):
		if ship not in enemy_Ships_And_Their_coordinates:
			enemy_Ships_And_Their_coordinates[ship] = []
		enemy_Ships_And_Their_coordinates[ship].append(coordinate)

enemy_Ship_Coordinate('A2', 'Destroyer')
enemy_Ship_Coordinate('A3', 'Battleship')
enemy_Ship_Coordinate('B3', 'Battleship')
enemy_Ship_Coordinate('F4', 'Cruiser')
firing_Queue = []
shot_Log = ['A2', 'A3', 'B3', 'F4']
print enemy_Ships_And_Their_coordinates

print len(enemy_Ships_And_Their_coordinates)


for ship in enemy_Ships_And_Their_coordinates:
	print ship
	print enemy_Ships_And_Their_coordinates[ship]

def generate_All_Coordinates():
	for letter in column:
		for number in row:
			all_Coordinates.append(letter + number)
all_Coordinates = []
generate_All_Coordinates()
print all_Coordinates