import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging

# Slightly improved reversed navigation

game = hlt.Game()  # game object
game.ready("New")


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

	# logging.info('\n\n \t\t {}'.format(me.get_ships()))
	for s in me.get_ships():
		ships_pos.append(s.position)
	# logging.info('\n\n \t\t {}'.format(ships_pos))


	for ship in me.get_ships():
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


		if ship.halite_amount >= 900:
			ship_status[ship.id] = "returning"
			ship_pos_returning   = ship.position		


		if ship.id not in ship_status:
			ship_status[ship.id] = "exploring"
			# logging.info('\n\n \t\t\t\t\t inside exploring')

			directional_choice = max(halite_dict, key=halite_dict.get)
			if position_dict[directional_choice] not in position_choices\
			and position_dict[directional_choice] not in ships_pos:
				position_choices.append(position_dict[directional_choice])
				command_queue.append(ship.move(directional_choice))


		elif ship_status[ship.id] == "returning":
			# logging.info('\n\n \t\t\t\t\t inside returning')

			if ship.position == me.shipyard.position:
				logging.info('\n\n \t\t\t\t\t ====> TURN RIGHT')
				position_choices.append(position_dict[Direction.East])
				command_queue.append(ship.move(Direction.East))
				ship_status[ship.id] = "exploring"

			else: 
				# logging.info('\n\n \t\t\t\t\t ELSE go to shipyard')
				move_home = game_map.naive_navigate(ship, me.shipyard.position)
				if position_dict[move_home] not in position_choices\
				and position_dict[move_home] not in ships_pos\
				and not move_near:
					position_choices.append(position_dict[move_home])
					command_queue.append(ship.move(move_home))
					continue
				else:
					move_near = game_map.naive_navigate(ship, www)
					position_choices.append(position_dict[move_near])
					command_queue.append(ship.move(move_near))


	if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied and len(me.get_ships()) <= 10:
		# logging.info('\n\n\t\t {}'.format(len(me.get_ships())))
		command_queue.append(me.shipyard.spawn())

	game.end_turn(command_queue)