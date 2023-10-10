import pygame
from constants import *
from piece import *

class Board:
	def __init__(self, size, blackColor, whiteColor, validMovesBlackColor, validMovesWhiteColor):
		self.blackColor = blackColor
		self.whiteColor = whiteColor

		self.validMovesWhiteColor = whiteColor
		self.validMovesBlackColor = blackColor

		self.isSelectedPiece = False

		self.width = self.height = size
		self.tileSize = size / 8

		self.color = 'W'

		self.blackRectPos = []
		self.whiteRectPos = []

		self.validMoves = []

		self.winner = None

		self.board = [
		['rB', 'nB', 'bB', 'qB', 'kB', 'bB2', 'nB2', 'rB2'],
		['pB', 'pB1', 'pB2', 'pB3', 'pB4', 'pB5', 'pB6', 'pB7'],
		['--', '--', '--', '--', '--', '--', '--', '--'],
		['--', '--', '--', '--', '--', '--', '--', '--'],
		['--', '--', '--', '--', '--', '--', '--', '--'],
		['--', '--', '--', '--', '--', '--', '--', '--'],
		['pW', 'pW1', 'pW2', 'pW3', 'pW4', 'pW5', 'pW6', 'pW7'],
		['rW', 'nW', 'bW', 'kW', 'qW', 'bW2', 'nW2', 'rW2']
	]

	def drawPiece(self, win):
		for r in range(len(self.board)):
			for c in range(len(self.board[0])):

				coX, coY = c * self.tileSize, r * self.tileSize

				if '--' not in self.board[r][c]:
					self.boardWithValid = self.board[r][c]
					if 'v' in self.board[r][c]: self.boardWithValid = self.board[r][c].replace('v', '')
					win.blit(dictionaryOfPics[self.boardWithValid], (coX, coY))
	
	def winnerCheck(self):
		kingWhiteThere = False
		kingBlackThere = False

		for r in range(len(self.board)):
			for c in range(len(self.board[0])):
				if self.board[r][c] == 'kW': kingWhiteThere = True
				if self.board[r][c] == 'kB': kingBlackThere = True
		
		if not kingWhiteThere: return 'Black'
		if not kingBlackThere: return 'White'
	
	def drawValidMoves(self, win):
		for r in range(len(self.board)):
			for c in range(len(self.board[0])):
				try:
					if 'v' in self.board[r][c]:
						if (r, c) in self.blackRectPos: self.validColor = TEALDARK
						else: self.validColor = TEALLIGHT
						rect = pygame.Rect(c * self.tileSize, r * self.tileSize, self.tileSize, self.tileSize)
						pygame.draw.rect(win, self.validColor, rect)

				except: pass

	def drawBoard(self, win):
		cnt = 0
		for x in range(0, 8 + 1):
			for y in range(1, 8 + 1):
				if cnt % 2 == 0:
					pygame.draw.rect(win, self.blackColor, (x * self.tileSize, y * self.tileSize - self.tileSize, self.tileSize, self.tileSize))
					self.blackRectPos.append((x, y - 1))
				else:
					pygame.draw.rect(win, self.whiteColor, (x * self.tileSize, y * self.tileSize - self.tileSize, self.tileSize, self.tileSize))
					self.whiteRectPos.append((x, y - 1))
				cnt += 1

			cnt -= 1

	def move(self, pos, isComputer, piece):
		if not isComputer:
			col, row = pos[0] // 70, pos[1] // 70

			if not self.isSelectedPiece:
				self.selectedPiece = self.board[row][col]
				if self.color in self.selectedPiece:
					self.location = (row, col)
					self.validMoves = findValidMoves(self.selectedPiece, row, col, self.board)
					for move in self.validMoves:
						try: self.board[move[0]][move[1]] += 'v'
						except: pass

					if self.validMoves != []: self.isSelectedPiece = True
					else: self.isSelectedPiece = False
			
			else:
				if [row, col] in self.validMoves:
					self.board[row][col] = self.selectedPiece
					self.board[self.location[0]][self.location[1]] = '--'
					self.isSelectedPiece = False
					self.validMoves = []

					for x in range(len(self.board)):
						for y in range(len(self.board[0])):
							if 'v' in self.board[x][y]:
								self.board[x][y] = self.board[x][y].replace('v', '')

					if self.color == 'B': self.color = 'W'
					elif self.color == 'W': self.color = 'B'
				else:
					self.isSelectedPiece = False

		else:
			for r in range(len(self.board)):
				for c in range(len(self.board[0])):
					if self.board[r][c] == piece: self.board[r][c] = '--'

			self.board[pos[0]][pos[1]] = piece

			if self.color == 'W': self.color = 'B'
			elif self.color == 'B': self.color = 'W'

	
	def update(self, win):
		self.drawBoard(win)
		self.drawValidMoves(win)
		self.drawPiece(win)

		# self.winner = self.winnerCheck()

		# if self.winner != None: print(self.winner)

