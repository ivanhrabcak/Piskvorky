import sys, math, random

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

class AI: # haha
	def __init__(self, grid_max, seed = "random"):
		if not seed == "random" and type(seed) == int:
			random.seed(seed)
		self.max = grid_max
		
	def move(self):
		return(random.randint(1, self.max))

class Grid:
	def __init__(self, l = [], shape = (3, 3)):
		self.shape = shape
		if l == []:
			l = self.grid()

		self.max = shape[0] * shape[1]
		self.grid = l

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

	def read(self, i): # dá sa to urobiť aj lepšie?
		i -= 1 # counting from zero
		l = []
		for item in self.grid:
			for n in item:
				l.append(n)
		return(l[i])

	def write(self, move, new): # dá sa to urobiť aj lepšie?
		move -= 1 # counting from zero
		copy = []
		for item in self.grid:
			for n in item:
				copy.append(n)
		copy[move] = new # overwrite old value
		max_value = self.shape[0] * self.shape[1]
		max_obj = self.shape[0]
		g = []
		index_multiplier = 0
		for n in range(0, max_value):
			objs = []
			for index in range(0, max_obj):
				index += index_multiplier
				try:
					objs.append(copy[index])
				except Exception:
					self.grid = g
					return(True)
			g.append(objs)
			index_multiplier += max_obj

	def transform(self):
		g = []
		for item in self.grid:
			for n in item:
				g.append(n)
		return(g)

	def draw(self):
		def draw_line():
			g = self.transform()
			grid_outer_1 = "|-------|"
			grid_outer_2 = "|   n   |"
			grid_outer_3 = "|-------|"
			grid_inner_1 = "-------|"
			grid_inner_2 = "   n   |"
			grid_inner_3 = "-------|"
			print(grid_outer_1 + grid_inner_1 * (self.shape[1] - 1))
			for n in range(0, self.shape[1]):
				line = self.grid[n]
				for i in range(0, len(line)):
					if i == 0:
						print(grid_outer_2.replace("n", str(line[0])), end = "")
					else:
						print(grid_inner_2.replace("n", str(line[i])), end = "")
				print("\n" + grid_outer_3 + grid_inner_3 * (self.shape[1] - 1))
		draw_line()
player_turn = 1

grid_shape = (3, 3)
grid_list = []
grid_max = grid_shape[0] * grid_shape[1] # tazka matika
grid = Grid(l = [[0,0,0], [0,0,0], [0,0,0]], shape = grid_shape)

ai_enabled = True

if ai_enabled:
	ai = AI(grid_max, seed = 1)

grid.draw()

while True: # nic nerobi
	move = input("\nMove? ")
	if not is_numerical(move):
		print("You must enter a number.")

	elif not in_range(int(move), [1, grid_max]):
		print("This is not a valid field.")
	
	elif not grid.read(int(move)) == 0:
		print("This field is already claimed.")

	else:

		move = int(move)
		grid.write(move, player_turn)
		if not ai_enabled:
			if player_turn == 2:
				player_turn = 1
			else:
				player_turn = 2
			print("It's player %s's turn!" % (str(player_turn)))
		else:
			move = ai.move()
			if not grid.read(int(move)) == 0:
				while True:
					move = ai.move()
					if grid.read(int(move)) == 0:
						break
			else:
				grid.write(move, 2)
		grid.draw()