import pygame
from constants import *
from boardClass import *
from piece import *
from minimaxAI import *

pygame.init()

played = False

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess AI') 	

b = Board(560, blackTileColor, WHITE, 0, 0)

def redrawWindow():
	win.fill((255, 255, 255))
	b.update(win)
	pygame.display.flip()

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False
		
		if event.type == pygame.MOUSEBUTTONDOWN: 
			b.move(event.pos, False, None)
			redrawWindow()
		if b.color == 'B':
			col, value, bP = minimax(b.board, 4, -math.inf, math.inf, True, 'B')
			b.move(col, True, bP)

	redrawWindow()
