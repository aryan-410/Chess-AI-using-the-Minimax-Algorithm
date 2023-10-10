from constants import *

pawnsMoved = []

def findValidMoves(piece, row, col, board):
    if 'W' in piece:
        oppColor = 'B'
        selfColor = 'W'
    else:
        oppColor = 'W'
        selfColor = 'B'

    if 'k' in piece: validMoves = getKNMoves(row, col, selfColor, board, 'k')
    if 'n' in piece: validMoves = getKNMoves(row, col, selfColor, board, 'n')

    if 'r' in piece: validMoves = getBRQMoves(row, col, selfColor, oppColor, board, listOfMovesR)
    if 'b' in piece: validMoves = getBRQMoves(row, col, selfColor, oppColor, board, listOfMovesB)
    if 'q' in piece: validMoves = getBRQMoves(row, col, selfColor, oppColor, board, listOfMovesQ)

    if 'p' in piece: validMoves = getPawnMoves(row, col, selfColor, oppColor, board, piece)

    for x in validMoves:
        for y in x:
            if y < 0 or y > 7:
                validMoves = [i for i in validMoves if i != x]

    return validMoves

def getKNMoves(row, col, selfColor, board, kORn):
    if kORn == 'k': validMoves = [[row + 1, col + 1], [row, col + 1], [row, col - 1], [row + 1, col - 1], [row - 1, col - 1], [row - 1, col + 1], [row + 1, col], [row - 1, col]]
    elif kORn == 'n': validMoves = [[row + 2, col - 1], [row + 2, col + 1], [row + 1, col - 2], [row + 1, col + 2], [row - 2, col - 1], [row - 2, col + 1], [row - 1, col - 2], [row - 1, col + 2]]
    
    for [row, col] in validMoves:
        try:
            if selfColor in board[row][col]: validMoves = [i for i in validMoves if i != [row, col]]
        except: pass

    return validMoves

def getBRQMoves(row, col, selfColor, oppColor, board, listOfMoves):
    validMoves = []

    for move in listOfMoves:
        added = True
        for i in range(1, 9):
            try:
                if board[row + move[0] * i][col + move[1] * i] == '--' and added == True: validMoves.append([row + move[0] * i, col + move[1] * i])
                else:
                    if oppColor in board[row + move[0] * i][col + move[1] * i] and added == True: validMoves.append([row + move[0] * i, col + move[1] * i])
                    added = False
            except: pass

    return validMoves

def getPawnMoves(row, col, selfColor, oppColor, board, pawn):
    if selfColor == 'W': validMoves = [[row - 1, col], [row - 1, col - 1], [row - 1, col + 1]]
    if selfColor == 'B': validMoves = [[row + 1, col], [row + 1, col - 1], [row + 1, col + 1]]

    if pawn not in pawnsMoved:
        if selfColor == 'W': validMoves.append([row - 2, col])
        else: validMoves.append([row + 2, col])
        pawnsMoved.append(pawn)

    added = True
    for [rowL, colL] in validMoves:
        try:
            if colL != col:
                if oppColor not in board[rowL][colL]: validMoves = [i for i in validMoves if i != [rowL, colL]]
            else:
                if '--' not in board[rowL][colL]: validMoves = [i for i in validMoves if i != [rowL, colL]]
        except: pass

    return validMoves