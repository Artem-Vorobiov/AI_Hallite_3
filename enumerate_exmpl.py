my_list = ['apple', 'banana', 'grapes', 'pear']

for c, value in enumerate(my_list, 1):
	print(c, value)
print('\n\n')

# Итерирует через лист и присвает важдому значению листа порядковый номер!


halite_dict = {(0, -1): 708, (0, 1): 492, (1, 0): 727, (-1, 0): 472, (0, 0): 0}

# print(max(halite_dict, key=halite_dict.get))	#	727
# print(max(halite_dict))						#	727


#########################################################
def throw_max_value(old_array, max_value):
	new_array = {}
	for i in old_array:
		if i != max(old_array):
			new_array[i] = old_array[i]
		else:
			print('\n\t\t This element has been removed: {}'.format(i))
	return new_array
# print(halite_dict)
# halite_dict = throw_max_value(halite_dict, max(halite_dict))

# print(www)
# halite_dict = www
# print(halite_dict)
#########################################################




#########################################################
def throw_occupied_value(old_array, value):
	new_array = {}
	for i in old_array:
		if old_array[i] != value:
			new_array[i] = old_array[i]
		else:
			print('\n\t\t This element has been removed: {}'.format(i))
	return new_array
halite_dict = throw_occupied_value(halite_dict, 708)
print(halite_dict)
#########################################################


#	Поставить не If ,  а пройтись циклом For и избавиться от ненужных (is_occupied)
#	Таким образом создав массив


