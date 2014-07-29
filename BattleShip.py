from sys import exit
from random import randint
from gameEngine import gameEngine
	
def play_Again():
	
	restart = ''
	while restart != 'Y' and restart != 'N':
		print "Play again? answer with y or n"
		restart = raw_input("> ").upper()
		
	if restart == 'Y':
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