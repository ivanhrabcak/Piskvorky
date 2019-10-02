import sys
import numpy as np

grid_help = """
|-------|-------|-------|
|   1   |   2   |   3   |
|-------|-------|-------|
|   4   |   5   |   6   |
|-------|-------|-------|
|   7   |   8   |   9   |
|-------|-------|-------|


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
		if n >= r[0] and n <= r[0]:
			return(True)
		else:
			return(False)

class AI:
	def __init__(self, grid, shape):
		self.grid = grid
		self.shape = shape

class Grid:
	def __init__(self, l = [], shape = (3, 3)):
		self.shape = shape
		if l == []:
			grid = self.grid()

		self.grid = grid

	def grid(self):
		shape = self.shape

		l = []
		for i in range(0, shape[0]):
			line = []
			for i in range(0, shape[1]):
				line.append(0)
			l.append(line)
		return(l)

	def get(self):
		return(self.grid)

	def read(self, i):
		i = i - 1
		if i <= 3 and i >= 1:
			return(grid_list[0][i])
		elif i >= 4 and i <= 6:
			i = i - 3
			return(grid_list[1][i])
		elif i >= 7 and i <= 9:
			i = i - 6
			return(grid_list[2][i])
		else:
			raise IndexError()

	def write(self, i):
		if i <= 3 and i >= 1:
			return(grid_list[0][i])
		elif i <= 4 and i >= 6:
			return(grid_list[1][i])
		elif i <= 7 and i >= 9:
			return(grid_list[2][i])
		else:
			raise IndexError()

player_turn = 1
ai = False
done = False

grid_shape = (3, 3)
grid_list = []
grid = Grid(l = grid_list, shape = grid_shape)

print(grid_help)

while not done:
	move = input("Move? ")
	if not is_numerical(move):
		while True:
			print("You must enter a number.")
			move = input("Move? ")
			if is_numerical(move):
				break
	if in_range(move, grid_shape[0]):
		print(move)
		break
	else:
		sys.exit(print(":("))