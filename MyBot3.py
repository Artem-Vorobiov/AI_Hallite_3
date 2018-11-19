import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging

# Slightly improved reversed navigation

game = hlt.Game()  # game object
game.ready("Bot3")


while True:
	ship_status = {}
	move_near = False
	game.update_frame()
	me = game.me
	game_map = game.game_map
	command_queue = []
	direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

	shipyard_position = me.shipyard.position
	new_shipyard_position = tuple((shipyard_position.x - 1, shipyard_position.y))
	www = Position(shipyard_position.x - 1, shipyard_position.y)


	position_choices = []
	ships_pos        = []
	dropp_off_dist   = []
	dropp_off_list   = []
	dropp_off_dict   = {}

	# logging.info('\n\n \t\t {}'.format(me.get_ships()))
	for s in me.get_ships():
		ships_pos.append(s.position)
	# logging.info('\n\n \t\t {}'.format(ships_pos))

	count = 0 
	for ship in me.get_ships():
		count += 1

		# logging.info('\n\n \t\t\t\t\t Start'.format(position_choices))
		# logging.info('\n\n \t\t\t\t\t Ship status: {} ID: {}'.format(ship_status, ship.id))

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

#######################################################################################
#######################################################################################
		if game.turn_number > 360:
			if ship.position != me.shipyard.position:
				ship_status[ship.id] = "back_to_base"
				move_home  = game_map.naive_navigate(ship, me.shipyard.position)
				# position_choices.append(position_dict[move_home])
				command_queue.append(ship.move(move_home))
				continue
			else: 
				ship_status[ship.id] = "run"
				for i in me.get_dropoffs():
					move_depot = game_map.calculate_distance(ship.position, i.position)
					dropp_off_dist.append(move_depot)
					dropp_off_dict[move_depot] = i
				minn = min(dropp_off_dist)
				one = dropp_off_dict[minn]
				move_off  = game_map.naive_navigate(ship, one.position)
				command_queue.append(ship.move(move_off))
				continue
#######################################################################################
#######################################################################################


		if len(me.get_dropoffs()) < 1:
			if game_map.calculate_distance(ship.position, me.shipyard.position) >= 13:
				if me.halite_amount >= 4000 and len(me.get_ships()) >= 5 and 0 < ship.halite_amount < 200:
					command_queue.append(ship.make_dropoff())
					position_choices.append(ship.position)
					ship_status[ship.id] = "dropped_off"

		elif len(me.get_dropoffs()) == 1:
			for i in me.get_dropoffs():
				if game_map.calculate_distance(ship.position, i.position) >= 13\
				and game_map.calculate_distance(ship.position, me.shipyard.position) >= 10:
					if me.halite_amount >= 4000 and len(me.get_ships()) >= 5 and 0 < ship.halite_amount < 200:
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
					dropp_off_dist.append(move_depot)
					dropp_off_dict[move_depot] = i

				move_to_dropoff = min(dropp_off_dist)
				move_shipyard   = game_map.calculate_distance(ship.position, me.shipyard.position)

				logging.info('\n\n \t\t\t\t\t ====> DROP OFF DISTANCE. {}'.format(move_depot))
				logging.info('\n\n \t\t\t\t\t ====> Shipyard DISTANCE. {}'.format(move_shipyard))
				if move_to_dropoff >= move_shipyard:
					move_home  = game_map.naive_navigate(ship, me.shipyard.position)
					if position_dict[move_home] not in position_choices\
					and position_dict[move_home] not in ships_pos:
						position_choices.append(position_dict[move_home])
						command_queue.append(ship.move(move_home))
						# logging.info('\n\n \t\t\t\t\t ====> MOVE -- HOME')
						continue
#######################################################################################
#######################################################################################
				else:
					move_dropoff  = game_map.naive_navigate(ship, dropp_off_dict[move_to_dropoff].position)
					if position_dict[move_dropoff] not in position_choices\
					and position_dict[move_dropoff] not in ships_pos:
						position_choices.append(position_dict[move_dropoff])
						command_queue.append(ship.move(move_dropoff))
						# logging.info('\n\n \t\t\t\t\t ====> MOVE -- HOME')
						continue
#######################################################################################
#######################################################################################


#######################################################################################


	if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied and len(me.get_ships()) <= 10\
	and game.turn_number < 330:
		command_queue.append(me.shipyard.spawn())
	elif me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied\
	and len(me.get_ships()) <= 13 and game.turn_number > 165 and game.turn_number < 330:
		command_queue.append(me.shipyard.spawn())

	game.end_turn(command_queue)