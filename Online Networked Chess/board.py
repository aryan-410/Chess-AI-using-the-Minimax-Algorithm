import pygame
from constants import *
from piece import *
pygame.init()


class Board:
    def __init__(self):
        size = 560
        self.blackColor = blackTileColor
        self.whiteColor = WHITE

        self.validMovesWhiteColor = TEALLIGHT
        self.validMovesBlackColor = TEALDARK

        self.isSelectedPiece = False
        self.moved_piece_for_main = False

        self.width = self.height = size
        self.tileSize = size / 8

        self.color = "W"

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
                    self.boardWithValid = self.boardWithValid.replace('v', '')
                    try: win.blit(dictionaryOfPics[self.boardWithValid], (coX, coY))
                    except Exception: pass
    
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
        for v in self.validMoves: 
            pygame.draw.circle(win, (255, 0, 0), (v[1] * self.tileSize + 35, v[0] * self.tileSize + 35), 12)
            if (v[0], v[1]) in self.blackRectPos: validColor = self.validMovesBlackColor
            else: validColor = self.validMovesWhiteColor
            
            rect = pygame.Rect(v[1] * self.tileSize, v[0] * self.tileSize, self.tileSize, self.tileSize)
            # pygame.draw.rect(win, validColor, rect)

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

                self.moved_piece_for_main = True

        else:
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if self.board[r][c] == piece: self.board[r][c] = '--'

            self.board[pos[0]][pos[1]] = piece
        
        return True
    
    def stringify(self):
        board_string = ""

        for x in range(0, len(self.board)):
            for y in range(0, len(self.board)):
                if x == 7 and y == 7: board_string += f"{self.board[x][y]}"
                else: board_string += f"{self.board[x][y]},"
        
        return board_string
        
    
    def unstringify(self, list_to_unstingify):
        everyPiece = list(list_to_unstingify.split(','))
        
        total = 0
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                try:
                    self.board[x][y] = everyPiece[total]
                    total += 1
                except: pass

    def update(self, win):
        self.drawBoard(win)
        self.drawValidMoves(win)
        self.drawPiece(win)
        win.blit(dictionaryOfPics["rB"], (0, 0))
