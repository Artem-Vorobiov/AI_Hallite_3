import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging

import cv2
import numpy as np
import math
import time



game = hlt.Game()  # game object
game.ready("Bot2")
whole_picture = []


while True:
	ship_status = {}
	move_near = False
	game.update_frame()
	me = game.me
	game_map = game.game_map
###########################################################################################
	game_data = np.zeros((game_map.width, game_map.height, 3), np.uint8)
	grayed = cv2.cvtColor(game_data, cv2.COLOR_BGR2GRAY)
	# resized = cv2.resize(grayed, dsize=None, fx=10, fy=10)
	# cv2.waitKey(1)

	# if game.turn_number == 50:
		# logging.info('METADATA Map Width: \n\t\t {}\n'.format(type(game_map.width)))	# int
		# logging.info('METADATA Map Height: \n\t\t {}\n'.format(game_map.height))
		# logging.info('METADATA Map Height: \n\t\t {}\n'.format(game_data))

	for s in me.get_ships():
		pos = s.position
		logging.info('X: \n\t\t {}\n'.format(pos.x))
		logging.info('Y: \n\t\t {}\n'.format(pos.y))
		cv2.circle(grayed, (int(pos.x), int(pos.y)), 1, (255, 255, 255), -1)
		ships_pos.append(s.position)
		whole_picture.append(grayed)
		# cv2.imshow('Random Intel', grayed)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
###########################################################################################
	
	command_queue = []
	direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

	shipyard_position = me.shipyard.position
	new_shipyard_position = tuple((shipyard_position.x - 1, shipyard_position.y))
	www = Position(shipyard_position.x - 1, shipyard_position.y)


	position_choices = []
	ships_pos        = []





	count = 0 
	for ship in me.get_ships():
		count += 1

		position_options = ship.position.get_surrounding_cardinals() + [ship.position]
		position_dict = {}
		halite_dict = {}

		for n, direction in enumerate(direction_order):
			position_dict[direction] = position_options[n]

		for direction in position_dict:
			position = position_dict[direction]
			halite_amount = game_map[position].halite_amount
			if position_dict[direction] not in position_choices:
				if direction == Direction.Still:
					halite_amount *= 4
				halite_dict[direction] = halite_amount


#######################################################################################
		if len(me.get_dropoffs()) < 1:
			if game_map.calculate_distance(ship.position, me.shipyard.position) >= 10:
				if me.halite_amount >= 4000 and len(me.get_ships()) >= 5 and 0 < ship.halite_amount < 100:
					command_queue.append(ship.make_dropoff())
					position_choices.append(ship.position)
					ship_status[ship.id] = "dropped_off"
#######################################################################################


		if ship.position == me.shipyard.position and game.turn_number > 100:
			ship_status[ship.id] = "adjusting"

		if ship.id not in ship_status:
			ship_status[ship.id] = "exploring"

		if ship_status[ship.id] == "adjusting":
			# logging.info('\n\n \t\t\t\t\t ====> ADJUSTING')
			if ship.position == me.shipyard.position:
				if position_dict[Direction.East] not in position_choices\
				and position_dict[Direction.East] not in ships_pos:
					logging.info('\n\n \t\t\t\t\t ====> EAST')
					position_choices.append(position_dict[Direction.East])
					command_queue.append(ship.move(Direction.East))
				else:
					logging.info('\n\n \t\t\t\t\t ====> NORTH')
					position_choices.append(position_dict[Direction.North])
					command_queue.append(ship.move(Direction.North))
			else:
				ship_status[ship.id] = "exploring"
				# logging.info('\n\n \t\t\t\t\t ====> EXPLORING')


		if ship.halite_amount >= 900:
			ship_status[ship.id] = "returning"
			ship_pos_returning = ship.position	


		if ship_status[ship.id] == "exploring":
			directional_choice = max(halite_dict, key=halite_dict.get)
			if position_dict[directional_choice] not in position_choices\
			and position_dict[directional_choice] not in ships_pos:
				position_choices.append(position_dict[directional_choice])
				command_queue.append(ship.move(directional_choice))


		elif ship_status[ship.id] == "returning":
			if not me.get_dropoffs():
				move_home  = game_map.naive_navigate(ship, me.shipyard.position)
				if position_dict[move_home] not in position_choices\
				and position_dict[move_home] not in ships_pos\
				and not move_near:
					position_choices.append(position_dict[move_home])
					command_queue.append(ship.move(move_home))
					# logging.info('\n\n \t\t\t\t\t ====> MOVE -- HOME')
					continue
				else:
					move_near = game_map.naive_navigate(ship, www)
					position_choices.append(position_dict[move_near])
					command_queue.append(ship.move(move_near))
					# logging.info('\n\n \t\t\t\t\t ====> MOVE -- NEAR')
#######################################################################################
			else:
				for i in me.get_dropoffs():
					move_depot = game_map.calculate_distance(ship.position, i.position)
					move_shipyard  = game_map.calculate_distance(ship.position, me.shipyard.position)
					logging.info('\n\n \t\t\t\t\t ====> DROP OFF DISTANCE. {}'.format(move_depot))
					logging.info('\n\n \t\t\t\t\t ====> Shipyard DISTANCE. {}'.format(move_shipyard))
					if move_depot >= move_shipyard:
						move_home  = game_map.naive_navigate(ship, me.shipyard.position)
						if position_dict[move_home] not in position_choices\
						and position_dict[move_home] not in ships_pos:
							position_choices.append(position_dict[move_home])
							command_queue.append(ship.move(move_home))
							# logging.info('\n\n \t\t\t\t\t ====> MOVE -- HOME')
							continue
					else:
						move_dropoff  = game_map.naive_navigate(ship, i.position)
						if position_dict[move_dropoff] not in position_choices\
						and position_dict[move_dropoff] not in ships_pos:
							position_choices.append(position_dict[move_dropoff])
							command_queue.append(ship.move(move_dropoff))
							# logging.info('\n\n \t\t\t\t\t ====> MOVE -- HOME')
							continue

#######################################################################################


	if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied and len(me.get_ships()) <= 10:
		command_queue.append(me.shipyard.spawn())
	elif me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied\
	and len(me.get_ships()) <= 13 and game.turn_number > 100:
		command_queue.append(me.shipyard.spawn())

	game.end_turn(command_queue)
	 np.save("{}.npy".format(str(int(time.time()))), np.array(whole_picture))