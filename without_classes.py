#from with_classes import *
from graphics import *
from random import *

WIN_X, WIN_Y = 1000, 1000

model ={1:[[1,1],[1,1]], 2:[[1,1,1,1]], 3:[[1],[1],[1],[1]], 4:[[1, 1, 1], [0, 1, 0]], 5:[[0, 1], [1, 1], [0, 1]],
		6:[[0, 1, 0], [1, 1, 1]], 7:[[1, 0], [1, 1], [1, 0]], 8:[[0, 1, 1], [1, 1, 0]], 9:[[1, 0], [1, 1], [0, 1]],
		10:[[1, 1, 0], [0, 1, 1]], 11:[[0, 1], [1, 1], [1, 0]], 12:[[1, 1], [1, 0], [1, 0]], 13:[[1, 1, 1], [0, 0, 1]],
		14:[[0, 1], [0, 1], [1, 1]], 15:[[1, 0, 0], [1, 1, 1]], 16:[[1, 1], [0, 1], [0, 1]], 17:[[0, 0, 1], [1, 1, 1]],
		18:[[1, 0], [1, 0], [1, 1]], 0:[[1, 1, 1], [1, 0, 0]]}


def get_col(ps, i):
	return [row[i] for row in ps]


def del_col(ps, i):
	for row in ps:
		del row[i]


def new_board(cols, rows):
	return [[0] * cols for y in range(rows)]


def check_len_block(block): #check the len of each block's block
	i = len(block[0])
	for j in block:
		if len(j) != i:
			return False
	return True


def alphapieces(p, alpha):
	return [[alpha if c == 1 else 0 for c in b]for b in p]


def thin_piece(ps):
	for i, block in enumerate(ps):
		if not check_len_block(block):
			del ps[i:]
			break
		for p in range(len(block[0]) - 1, -1, -1):
			c1 = get_col(block, p)
			if c1 == [0] * len(block):
				del_col(block, p)
	for block in ps:
		c2 = [0] * len(block[0])
		while c2 in block:
			block.remove(c2)


def parsing(ps):
	boo = False
	k = 0
	for i in range(0, len(ps)):
		for j in range(len(model)):
			if ps[i] == model[j]:
				boo = True
				print(ps[i])
				break
		if boo and k < 26:
			k += 1
			boo = False
		else:
			del ps[i:]
			break

def GetPieces():
	p = [[[0 if i == '.' else 1 for i in l if l] for l in block.split('\n') if l] \
		 for block in open('tetri.txt').read().split('\n\n')]
	while not p[-1]:
		p.pop()
	return p


def check_collision(board, piece, offset):
	off_x, off_y = offset
	for cy, row in enumerate(piece):
		for cx, cell in enumerate(row):
			try:
				if cell and board[cy + off_y][cx + off_x]:
					return False
			except IndexError:
				return False
	return True


def put_piece(board, piece, offset, c):
	off_x, off_y = offset
	for cy, row in enumerate(piece):
		for cx, cell in enumerate(row):
			board[cy + off_y][cx + off_x] = ord(c) if board[cy + off_y][cx + off_x] == 1 or cell else \
			board[cy + off_y][cx + off_x]


def print_board(board):
	for row in board:
		for cell in row:
			print(chr(cell) if cell != 0 else 0,' ', end='')
		print()


def popopo(board, long):
	offset_x = WIN_X / len(board[0])
	offset_y = WIN_Y / len(board)
	win = GraphWin("FEELIT", WIN_X, WIN_Y)
	for i in range(long):
		r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
		for off_y, row in enumerate(board):
			for off_x, cell in enumerate(row):
				pt = Point(offset_x * off_x, offset_y * off_y)
				pt2 = Point(offset_x * (off_x + 1), offset_y * (off_y + 1))
				rect = Rectangle(pt, pt2)
				if cell == ord('A') + i:
					rect.setFill(color_rgb(r, g, b))
				elif cell == 0:
					rect.setFill(color_rgb(0, 0, 0))
				rect.setOutline('white')
				rect.draw(win)
	win.getMouse()


def isfull(board, char):
	i = 4 * char
	for row in board:
		for cell in row:
			if cell:
				i -= 1
	return True if i == 0 else False


def feelit(pieces):
	x = 2
	while True:
		board = new_board(x, x)
		for c, p in enumerate(pieces):
			for off_y, row in enumerate(board):
				for off_x, col in enumerate(row):
					if check_collision(board, p, (off_x, off_y)):
						put_piece(board, p, (off_x, off_y), chr(ord('A') + c))
						break
				else:
					continue
				break
		if isfull(board, len(pieces)):
			break
		x += 1
	return board


if __name__ == '__main__':
	pieces = GetPieces()
	thin_piece(pieces)
	parsing(pieces)
	board = feelit(pieces)
	print_board(board)
	popopo(board, len(pieces))

