import sys

grid = """
|-------|-------|-------|
|   1   |   2   |   3   |
|-------|-------|-------|
|   4   |   5   |   6   |
|-------|-------|-------|
|   7   |   8   |   9   |
|-------|-------|-------|

"""
grid_list = [[0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0]]

def read(i):
	if i <= 3 and i >= 1:
		return(grid_list[0][i])
	elif i <= 4 and i >= 6:
		return(grid_list[1][i])
	elif i <= 7 and i >= 9:
		return(grid_list[2][i])

def write(i):
	pass


player_turn = 1
done = False
print(grid)
while not done:
	try:
		move = int(input("Move? "))
	except ValueError:
		print("You have to enter a number.")
		sys.exit(1)
	if move <= 9 and move >= 1:
		field = get(move)
		if field == 0:
