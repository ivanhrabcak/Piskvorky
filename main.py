import sys, math, random, socket, time, json

"""
## Grid numbering help

|-------|-------|-------|
|   1   |   2   |   3   |
|-------|-------|-------|
|   4   |   5   |   6   |
|-------|-------|-------|
|   7   |   8   |   9   |
|-------|-------|-------|

|-------|
|   0   | - not claimed
|-------|

|-------|
|   1   | - Player 1
|-------|

|-------|
|   2   | - Player 2
|-------|
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

class Client:
	def __init__(self, host, port):
		self.port = port
		self.host = host
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send(self, m):
		s = self.s

		if type(m) == bytes:
			message = m
		else:
			message = bytes(str(m), "utf8")

		s.sendall(message)


	def recv(self):
		s = self.s
		return(s.recv(1024).decode("utf8"))

	def connect(self):
		HOST = self.host
		PORT = self.port
		s = self.s

		s.connect((HOST, PORT))

class Server:
	def __init__(self, port, shape = (3, 3)):
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.shape = shape

	def send(self, conn, m):
		if type(m) == bytes:
			message = m
		else:
			message = bytes(str(m), "utf8")

		conn.sendall(message)

	def recv(self, conn):
		return(conn.recv(1024).decode("utf8"))

	def listen(self):
		PORT = self.port
		HOST = "127.0.0.1"

		self.s.bind((HOST, PORT))
		self.s.listen()
		conn, addr = self.s.accept()
		self.handle(conn, addr)

	def handle(self, conn, addr):
		print("%s has connected!" % (str(addr)))
		self.g_list = []
		self.g = Grid(grid_storage = self.g_list, shape = self.shape)
		self.send(conn, json.dumps(self.g.grid))
		self.player_turn = 1
		while True:
			move = self.recv(conn)
			self.g.write(self.player_turn, move)
		
			move = input("\nMove? ")
			if not is_numerical(move):
				print("You must enter a number.")
	
			elif not in_range(int(move), [1, grid_max]):
				print("This is not a valid field.")
		
			elif not grid.read(int(move)) == 0:
				print("This field is already claimed.")
	
			else:
				move = int(move)
				self.g.write(move, player_turn)
				self.g.check_win(player_turn)
			grid.draw()
			self.send(conn, json.dumps(self.g.grid))



class AI: # haha
	def __init__(self, grid_max, seed = "random"): # grid_max = Grid.shape[0] * Grid.shape[1]
		if seed != "random" and type(seed) == int:
			random.seed(seed)
		self.max = grid_max
		
	def move(self): # Return a random number
		return random.randint(1, self.max)

class Grid:
	def __init__(self, grid_storage = [], shape = (3, 3)): # l - grid storage
		self.shape = shape
		if grid_storage == []:
			grid_storage = self.gen()

		self.max = shape[0] * shape[1]
		self.grid = grid_storage

	def gen(self): # Generate 2d array with zeros
		l = [[]] * self.shape[1]
		for i in range(0, self.shape[1]):
			l[i] = [0] * self.shape[0]
		return l

	def read(self, i): # read the field i (README grid numbering help)
		i -= 1
		return self.grid[self.get_index(i)][self.get_position(i)]

	def write(self, move, new): # write to the field move (README grid numbering help)
		self.grid[self.get_index(move)][self.get_position(move)] = new

	def check_win(self, player_turn):
		# Diagonals
		for x in range(0, self.shape[1]):
			if x + 2 < self.shape[1]: # Case 1
				for y in range(0, self.shape[0]):
					if y + 2 >=  self.shape[0]:
						continue
					i = self.grid[x][y]
					if i == self.grid[x + 1][y + 1] and i == self.grid[x + 2][y +2] and i != 0:
						print("Player %s has won!" % (player_turn))
						return "Case 1"
			
			if x + 2 < self.shape[1]: # Case 2
				for y in range(0, self.shape[1]):
					if y - 2 < 0:
						continue
					i = self.grid[x][y]
					if i == self.grid[x + 1][y - 1] and i == self.grid[x + 2][y - 2] and i != 0:
						print("Player %s has won!" % (player_turn))
						return "Case 2"
		# |
		for x in range(0, self.shape[1]):
			if x + 2 < self.shape[1]:
				for y in range(0, self.shape[0]):
					i = self.grid[x][y]
					if i == self.grid[x + 1][y] and i == self.grid[x + 2][y] and i != 0:
						print("Player %s has won!" % (player_turn))
						return "Case 3"
		
		# ---
		for x in range(0, self.shape[1]):
			for y in range(0, self.shape[0]):
				if y + 2 >= self.shape[1]:
					continue
				i = self.grid[x][y]
				if i == self.grid[x][y + 1] and i == self.grid[x][y + 2] and i != 0:
					print("Player %s has won!" % (player_turn))
					return "Case 4"
		return False

	def draw(self): # print the grid nicely
		def draw_line():
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

	def get_index(self, i):
		return math.floor(i / self.shape[0])

	def get_position(self, i):
		return math.floor(i % self.shape[0])

player_turn = 1

grid_shape = (3, 3)
grid_list = []
grid_max = grid_shape[0] * grid_shape[1]
grid = Grid(grid_storage = grid_list, shape = grid_shape)

ai_enabled = False

if ai_enabled:
	ai = AI(grid_max, seed = 1)

grid.draw()

while True:
	move = input("\nMove? ")
	if not is_numerical(move):
		print("You must enter a number.")
		continue

	elif not in_range(int(move), [1, grid_max]):
		print("This is not a valid field.")
		continue
	
	elif not grid.read(int(move)) == 0:
		print("This field is already claimed.")
		continue
	
	move = int(move) - 1
	grid.write(move, player_turn)
	win = grid.check_win(player_turn)
	if win != False:
			print(win)
			break	
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
					grid.write(move, 2)
					break
		else:
			grid.write(move, 2)
	grid.draw()

