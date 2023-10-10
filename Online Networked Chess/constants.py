import pygame

WIDTH, HEIGHT = 560, 560

blackTileColor = (90, 90, 90)

WHITE = (255, 255, 255)
TEALDARK = (0, 64, 64)
TEALLIGHT = (0, 128, 128)

listOfPieces = ['rW', 'rB', 'pW', 'pB', 'bB', 'bW', 'nW', 'nB', 'kW', 'kB', 'qB', 'qW', 'rW2', 'nW2', 'bW2', 'nB2', 'bB2', 'rB2', 'pW1', 'pW2', 'pW3', 'pW4', 'pW5', 'pW6', 'pW7', 'pB1', 'pB2', 'pB3', 'pB4', 'pB5', 'pB6', 'pB7']
dictionaryOfPics = {}

for piece in listOfPieces:
	try: dictionaryOfPics[piece] = pygame.image.load(f'Images/{piece}.png')
	except: print(piece)

listOfMovesR = [[1, 0], [0, 1], [-1, 0], [0, -1]]
listOfMovesB = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
listOfMovesQ = [[1, -1], [1, 1], [-1, -1], [-1, 1], [1, 0], [0, 1], [-1, 0], [0, -1]]
listOfMovesPW = [[-1, 0], [-1, 1], [-1, -1]]
listOfMovesPB = [[1, 0], [1, -1], [1, 1]]

pawnsMoved = []
