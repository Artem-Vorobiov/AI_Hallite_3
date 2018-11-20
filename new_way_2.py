import hlt
from hlt import constants
from hlt.positionals import Direction, Position
# from hlt.game_map 	 import MapCell, GameMap
from hlt import entity 
import random
import logging
from collections import defaultdict

game     = hlt.Game()
game.ready("new_way")
go_home = defaultdict(lambda: False)


while True:
	game.update_frame()
	me 			  = game.me 	
	game_map 	  = game.game_map
	direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
	command_queue = []
	ship_status = {}

	# for ship in me.get_ships():

	if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied and len(me.get_ships()) <= 10:
		command_queue.append(me.shipyard.spawn())

	game.end_turn(command_queue)
