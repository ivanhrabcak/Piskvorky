import sys, math

grid_help = """
|-------|-------|-------|
|   1   |   2   |   3   |
|-------|-------|-------|
|   4   |   5   |   6   |
|-------|-------|-------|
|   7   |   8   |   9   |
|-------|-------|-------|

"""
"""
grid_list = [[0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0]]
"""

def is_numerical(string):
	try:
		int(string)
	except ValueError:
		return(False)
	else:
		return(True)

def in_range(n, r): # r = [min, max]
	if not type(r) == list:
		if n >= 0 and n <= r:
			return(True)
		else:
			return(False)
	else:
		if n >= r[0] and n <= r[1]:
			return(True)
		else:
			return(False)

class Grid:
	def __init__(self, l = [], shape = (3, 3)):
		self.shape = shape
		if l == []:
			grid = self.grid()

		self.grid = grid

	def grid(self):
		shape = self.shape

		l = []
		for i in range(0, shape[1]):
			line = []
			for i in range(0, shape[0]):
				line.append(0)
			l.append(line)
		return(l)

	def get(self):
		return(self.grid)

	def read(self, i): # zatial funguje iba ak shape = (3, 3) 
		if i <= 3 and i >= 1:
			i -= 1
			return(self.grid[0][i])
		elif i >= 4 and i <= 6:
			i = i - 4
			return(self.grid[1][i])
		elif i >= 7 and i <= 9:
			i = i - 5
			return(self.grid[2][i])
		else:
			raise IndexError()

	def write(self, i, new): # zatial (trosku) funguje iba ak shape = (3, 3)
		if i <= 3 and i >= 1:
			i -= 1
			self.grid[0][i] = new
		elif i <= 4 and i >= 6: # preco to nefunguje?
			i -= 4
			self.grid[1][i] = new
		elif i <= 7 and i >= 9:
			i -= 5
			self.grid[2][i] = new
		else:
			raise IndexError()

	def get_index(self, i): # AKO TOTO MOZE FUNGOVAT
		list_number = math.floor(i / self.shape[1])
		return(list_number)

	def get_position(self, i): # ????
		return(math.floor(self.shape[0] / i))

player_turn = 1

grid_shape = (3, 3)
grid_list = []
grid_max = grid_shape[0] * grid_shape[1] # tazka matika
grid = Grid(l = grid_list, shape = grid_shape)

print(grid_help)

while True: # nic nerobi
	move = input("Move? ")
	if not is_numerical(move):
		print("You must enter a number.")

	elif not in_range(int(move), [1, grid_max]):
		print("This is not a valid field.")
	
	elif not grid.read(int(move)) == 0:
		print("This field is already claimed.")

	move = int(move)
	grid.write(move, player_turn)

	if player_turn == 2:
		player_turn = 1
	else:
		player_turn = 2
	print("It's player %s's turn!" % (str(player_turn)))
	print(grid.get())
