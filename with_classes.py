from tkinter import *
from random import *

WIN_SIZE = 1000

model ={1:[[1,1],[1,1]], 2:[[1,1,1,1]], 3:[[1],[1],[1],[1]], 4:[[1, 1, 1], [0, 1, 0]], 5:[[0, 1], [1, 1], [0, 1]],
		6:[[0, 1, 0], [1, 1, 1]], 7:[[1, 0], [1, 1], [1, 0]], 8:[[0, 1, 1], [1, 1, 0]], 9:[[1, 0], [1, 1], [0, 1]],
		10:[[1, 1, 0], [0, 1, 1]], 11:[[0, 1], [1, 1], [1, 0]], 12:[[1, 1], [1, 0], [1, 0]], 13:[[1, 1, 1], [0, 0, 1]],
		14:[[0, 1], [0, 1], [1, 1]], 15:[[1, 0, 0], [1, 1, 1]], 16:[[1, 1], [0, 1], [0, 1]], 17:[[0, 0, 1], [1, 1, 1]],
		18:[[1, 0], [1, 0], [1, 1]], 0:[[1, 1, 1], [1, 0, 0]]}


class Board:

	def __init__(self):
		self.size = 2
		self.board = []

	def print_board(self):
		for row in self.board:
			for cell in row:
				print(chr(cell) if cell != 0 else 0, ' ', end='')
			print()

	def new_board(self, size):
		self.board = [[0] * size for y in range(size)]

	def feelit(self, pieces):
		self.new_board(self.size)
		while True:
			for c, p in enumerate(pieces):
				for off_y, row in enumerate(self.board):
					for off_x, col in enumerate(row):
						if self.check_collision(p, (off_x, off_y)):
							self.put_piece(p, (off_x, off_y), chr(ord('A') + c))
							break
					else:
						continue
					break
			if self.isfull(len(pieces)):
				break
			self.size += 1
			self.new_board(self.size)

	def isfull(self, char):
		i = 4 * char
		for row in self.board:
			for cell in row:
				if cell:
					i -= 1
		return True if i == 0 else False

	def put_piece(self, piece, offset, c):
		off_x, off_y = offset
		for cy, row in enumerate(piece):
			for cx, cell in enumerate(row):
				self.board[cy + off_y][cx + off_x] = ord(c) if self.board[cy + off_y][cx + off_x] == 1 or cell \
					else self.board[cy + off_y][cx + off_x]

	def check_collision(self, piece, offset):
		off_x, off_y = offset
		for cy, row in enumerate(piece):
			for cx, cell in enumerate(row):
				try:
					if cell and self.board[cy + off_y][cx + off_x]:
						return False
				except IndexError:
					return False
		return True

class Win(Board):

	def __init__(self):
		self.root = Tk()
		self.root.title("FEEEEEELIT")
		self.piiieces = []
		Board.__init__(self)

	####	Board Frame		####
		self.canvas = Canvas(self.root, height=WIN_SIZE, width=WIN_SIZE, background='black')
		self.canvas.pack(side=LEFT)

	####	Piece Frame		####
		self.frame = Frame(self.root, height=WIN_SIZE / 3, width=WIN_SIZE / 3)
		self.frame.pack(side=TOP)
		self.label = Label(self.frame, text="Put piece here").pack(side=TOP)
		self.textbox = Text(self.frame, relief=GROOVE, borderwidth=2)
		self.textbox.pack()
		self.button_piece = Button(self.frame, text='Commit piece', command=lambda: self.retrieve_input())
		self.button_piece.pack()

		self.button_lien = Button(self.frame, text='Commit link', command=lambda: self.retrieve_link())
		self.entry_lien = Entry(self.frame)
		self.entry_lien.pack()
		self.button_lien.pack()
		self.button_pop = Button(self.frame, text='POP', command=lambda: self.poplast())
		self.button_pop.pack()
		self.exit_button = Button(self.root, text="Exit", command=lambda: self.root.quit())
		self.exit_button.pack()
		self.mess = Message(self.root, text='fndsfhdkslbgsi;FHndjlsbgLJKFvbdjsvbJK>Gbfhjsabdks')
		self.mess.pack()


	####	Start	####
		self.main()
		self.root.mainloop()

	def main(self):
		self.feelit(self.piiieces)
		self.DrawInFrame(self.board, len(self.piiieces))
		self.message()
		self.print_board()

	def poplast(self):
		if self.piiieces:
			self.piiieces.pop()
			self.thin_piece()
			self.parsing()
		if not self.piiieces:
			self.board = []
		self.size = 2
		self.main()

	def message(self): #print board in the window
		m = ''
		for row in self.board:
			for cell in row:
				m += chr(cell) + ' ' if cell else '0 '
			m += '\n'
		self.mess.config(text=m)

	def retrieve_input(self):
		self.piiieces +=  [[[0 if i == '.' else 1 for i in l]for l in self.textbox.get("1.0",'end-1c').split('\n')]]
		self.thin_piece()
		self.parsing()
		self.main()

	def retrieve_link(self):
		link = self.entry_lien.get()
		try:
			if link:
				self.piiieces = self.piiieces + [\
					[[0 if i == '.' else 1 for i in l if l] for l in block.split('\n') if l]\
					for block in open(link).read().split('\n\n')]
				while not self.piiieces[-1]:
					self.piiieces.pop()
				self.thin_piece()
				self.parsing()
				self.main()
		except FileNotFoundError:
			print('Mauvais chemin fichier')

	def DrawInFrame(self, board, len_piece):
		offset_x = WIN_SIZE / len(board[0])
		offset_y = WIN_SIZE / len(board)
		for i in range(len_piece):
			color = '#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255))
			for off_y, row in enumerate(board):
				for off_x, cell in enumerate(row):
					if cell == ord('A') + i:
						rect = self.canvas.create_rectangle \
							(offset_x * off_x, offset_y * off_y, offset_x * (off_x + 1), offset_x * (off_y + 1)
							 , fil=color, outline='white')
					elif cell == 0:
						rect = self.canvas.create_rectangle \
							(offset_x * off_x, offset_y * off_y, offset_x * (off_x + 1), offset_x * (off_y + 1),
							 fil='black', outline='white')

	def thin_piece(self):
		for i, block in enumerate(self.piiieces):
			if not self.check_len_block(block):
				del self.piiieces[i:]
				break
			for p in range(len(block[0]) - 1, -1, -1):
				c1 = self.get_col(block, p)
				if c1 == [0] * len(block):
					self.del_col(block, p)
		for block in self.piiieces:
			c2 = [0] * len(block[0])
			while c2 in block:
				block.remove(c2)

	def check_len_block(self, block):  # check the len of each block's block
		i = len(block[0])
		for j in block:
			if len(j) != i:
				return False
		return True

	def get_col(self, block, i):
		return [row[i] for row in block]

	def del_col(self,block, i):
		for row in block:
			del row[i]

	def parsing(self):
		boo = False
		k = 0
		for i in range(0, len(self.piiieces)):
			for j in range(len(model)):
				if self.piiieces[i] == model[j]:
					boo = True
					break
			if boo and k < 26:
				k += 1
				boo = False
			else:
				del self.piiieces[i:]
				break


if __name__ == '__main__':
	win = Win()
	win.root.destroy()
	exit(0)
