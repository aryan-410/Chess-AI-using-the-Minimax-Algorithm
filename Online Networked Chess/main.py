import pygame
import time

from constants import *
from board import *
from piece import *
from client import *

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Online Multiplayer Chess') 

c = client()
b = Board()

color = None
color_turn = None
prevBoardChange = None

nothing_sent = True
board_sent = False
run = True
playing = False

circles = []

clicks = 0

clock = pygame.time.Clock()

def unstringifyChangeList(list_to_unstringify):
    board = [
        ['rB', 'nB', 'bB', 'qB', 'kB', 'bB2', 'nB2', 'rB2'],
        ['pB', 'pB1', 'pB2', 'pB3', 'pB4', 'pB5', 'pB6', 'pB7'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['pW', 'pW1', 'pW2', 'pW3', 'pW4', 'pW5', 'pW6', 'pW7'],
        ['rW', 'nW', 'bW', 'kW', 'qW', 'bW2', 'nW2', 'rW2']
    ]

    everyPiece = list(list_to_unstringify.split(','))

    total = 0
    for x in range(len(board)):
        for y in range(len(board)):
            try:
                board[x][y] = everyPiece[total]
                total += 1
            except: pass
    
    return board

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not board_sent: c.send("Hello")
    else: board_sent = False
    
    if color == None: 
        color = c.recieved_message
        if color == "white": b.color = "W"
        if color == "black": b.color = "B"
    
    else:
        color_and_board = c.recieved_message.split(".")
        color_turn = color_and_board[0]
        board = color_and_board[1]
        if color == "white": b.color = "W"
        if color_turn == color:
            prevBoard = b.stringify()
            if event.type == pygame.MOUSEBUTTONDOWN: b.move(event.pos, False, None)
            
            if (b.moved_piece_for_main):
                if b.stringify() != prevBoard:
                    c.send(b.stringify())
                    board_sent = True
                    b.moved_piece_for_main = False

            if not prevBoardChange: prevBoardChange = b.board
            moveChangeBoard = unstringifyChangeList(board)

            for row in range(len(prevBoardChange)):
                for col in range(len(prevBoardChange)):

                    if prevBoardChange[row][col] != moveChangeBoard[row][col]:
                        circles.append((col * 70 + 35, row * 70 + 35))                

        b.unstringify(board)
        prevBoardChange = None

    win.fill((255, 255, 255))
    b.update(win)
    # if color_turn == color:
    #     for pos in circles: pygame.draw.circle(win, (0, 0, 255), pos, 35, 2)
    pygame.display.flip()


c.send(c.DISCONNECT_MESSAGE)
