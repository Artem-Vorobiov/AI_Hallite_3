import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging

game = hlt.Game()  # game object
game.ready("ArtemVorobiov_V2")


while True:
	ship_status = {}
	dropoff_list = []
	game.update_frame()
	me = game.me
	game_map = game.game_map
	command_queue = []
	direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

	position_choices = []

	for ship in me.get_ships():

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

		if len(me.get_dropoffs()) < 1:
			if game_map.calculate_distance(ship.position, me.shipyard.position) >= 10:
				if me.halite_amount >= 4000 and len(me.get_ships()) >= 5 and 100 < ship.halite_amount < 400:
					command_queue.append(ship.make_dropoff())
					position_choices.append(ship.position)
					ship_status[ship.id] = "dropped_off"
					# me.halite_amount = me.halite_amount - 4000
		# elif len(me.get_dropoffs()) >= 1:
			# if game_map.calculate_distance(ship.position, me.shipyard.position) >= 9:

		# if len(me.get_dropoffs()) == 1:
		# 	if game_map.calculate_distance(ship.position, me.shipyard.position) >= 10:
		# 		if game_map.calculate_distance(ship.position, me.get_dropoffs()[0].position) >= 10:
		# 			if me.halite_amount >= 4000 and 50 < ship.halite_amount < 200:
		# 				command_queue.append(ship.make_dropoff())
		# 				position_choices.append(ship.position)
		# 				ship_status[ship.id] = "dropped_off"
		# 				# dropoff_list.append(me.get_dropoffs())
		# 				logging.info('\n\n\t\t FIRST Doff {}'.format(me.get_dropoffs()[0].position))

				


		if ship.id not in ship_status:
			ship_status[ship.id] = "exploring"

			directional_choice = max(halite_dict, key=halite_dict.get)
			position_choices.append(position_dict[directional_choice])
			command_queue.append(ship.move(directional_choice))			
		elif ship_status[ship.id] == "returning":
			if ship.position == me.shipyard.position:
				ship_status[ship.id] = "exploring"
			else: 


				dist_list = {}
				# logging.info('\n\n\t\t GET DROP OFF {}'.format(me.get_dropoffs()))		#	[Entity(id=2, Position(29, 19)), Entity(id=4, Position(26, 10))]
				# logging.info('\n\n\t\t TYOE {}'.format(type(me.get_dropoffs())))		#	<class 'list'>

				for i in me.get_dropoffs():
					# logging.info('\n\n\t\t one drop_off {}'.format(i))					#	Entity(id=2, Position(29, 19))
					# logging.info('\n\n\t\t one type {}'.format(type(i)))				#	<class 'hlt.entity.Entity'>

					# logging.info('\n\n\t\t drop off position {}'.format(i.position))	#	Position(29, 19)
					# logging.info('\n\n\t\t drop off type position {}'.format(type(i.position)))	#	<class 'hlt.positionals.Position'>

					a = game_map.calculate_distance(ship.position, i.position)
					b = i.position
					dist_list[a] = b
				dist_list[game_map.calculate_distance(ship.position, me.shipyard.position)] = me.shipyard.position

				# dist_list.append(game_map.calculate_distance(ship.position, me.shipyard.position))
				logging.info('\n\n\t\t Dictionery {}'.format(dist_list))				#	{18: Position(19, 20), 17: Position(28, 18), 10: Position(23, 16)}
				logging.info('\n\n\t\t Dictionery {}'.format(min(dist_list)))

				min_dist_to_dropoff = min(dist_list)
				logging.info('\n\n\t\t Dictionery {}'.format(dist_list[min_dist_to_dropoff]))

				move = game_map.naive_navigate(ship, dist_list[min_dist_to_dropoff])
				position_choices.append(position_dict[move])
				command_queue.append(ship.move(move))
				continue

	if game.turn_number < 340:
		if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied \
		and len(me.get_ships()) <= 6 and game.turn_number < 100:
			# logging.info('\n\n\t\t {}'.format(len(me.get_ships())))
			command_queue.append(me.shipyard.spawn())
		elif me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied \
		and len(me.get_ships()) <= 9 and game.turn_number > 150:
			command_queue.append(me.shipyard.spawn())

	game.end_turn(command_queue)