import pygame
import random
from piece import *
import math
from copy import deepcopy

transpositionTable = {}

def evaluation(board):
    score = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if 'pW' in board[r][c]: score -= 10
            if 'nW' in board[r][c] or 'bW' in board[r][c]: score -= 30
            if 'rW' in board[r][c]: score -= 50
            if 'qW' in board[r][c]: score -= 90

            if board[r][c] == 'kW': score -= 10000

            if 'pB' in board[r][c]: score += 10
            if 'nB' in board[r][c] or 'bB' in board[r][c]: score += 30
            if 'rB' in board[r][c]: score += 50
            if 'qB' in board[r][c]: score += 90

            if board[r][c] == 'kB': score += 10000

    return score
def findPossibleMoves(board, color):
    validMoves = {}
    for row in range(len(board)):
        for col in range(len(board)):
            if color in board[row][col]:
                validMoves[board[row][col]] = findValidMoves(board[row][col], row, col, board)

    # for piece in validMoves:
    #     for move in validMoves[piece]:
    #         if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0: validMoves[piece].remove(move)

    # print(validMoves)
    return validMoves

def isWon(board, king):
    for x in board:
        if king in x: return False

    return True

def simulateMove(board, piece, move):
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == piece: board[r][c] = '--'

    board[move[0]][move[1]] = piece

    return board

def minimax(board, depth , alpha, beta, maximizingPlayer, color):

    if depth == 0 or isWon(board, 'kW') or isWon(board, 'kB'):
        if isWon(board, 'kB'):
            return (None, -10000000000000000000000000, None)
        elif isWon(board, 'kW'):
            return (None, 1000000000000000000000, None)
        else:
            return (None, evaluation(board), None)


    validMoves = findPossibleMoves(board, color)

    if maximizingPlayer:
        value = -math.inf
        column = None
        for piece in validMoves:
            breakNow = False
            for move in validMoves[piece]:
                bCopy = deepcopy(board)
                bCopy = simulateMove(bCopy, piece, move)
                newScore = (minimax(bCopy, depth - 1, alpha, beta, False, 'W'))[1]
                if newScore > value:
                    value = newScore
                    column = move
                    bestPiece = piece
                alpha = max(alpha, value)       
                if alpha >= beta:
                    breakNow = True
                    break

                if value > 9000:
                    breakNow = True
                    break

            if breakNow == True: break

        return (column, value, bestPiece)
    
    else:
        value = math.inf
        column = None
        for piece in validMoves:
            breakNow = False
            for move in validMoves[piece]:
                bCopy = deepcopy(board)
                bCopy = simulateMove(bCopy, piece, move)
                newScore = (minimax(bCopy, depth - 1, alpha, beta, True, 'B'))[1]
                if newScore < value:
                    value = newScore
                    column = move
                    bestPiece = piece
                beta = min(beta, value)
                if alpha >= beta:
                    breakNow = True
                    break

            if breakNow == True: break

        return (column, value, bestPiece)
