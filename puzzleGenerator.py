import puzzle as pz
import numpy as np
import random
import math

"""Create a small library of 'normal' pieces, just tetronimoes for now. Not used yet"""
standardPieces = []
standardPieces.append(pz.Block([[1,1],[1,1]]))  # 2x2 square
standardPieces.append(pz.Block([[1,1,1],[0,1,0]]))  # Small T
standardPieces.append(pz.Block([[1,0,0],[1,1,1]]))  # Small L
standardPieces.append(pz.Block([[0,0,1],[1,1,1]]))  # Small L
standardPieces.append(pz.Block([[0,1,1],[1,1,0]]))  # Small Z
standardPieces.append(pz.Block([[1,1,0],[0,1,1]]))  # Small Z
standardPieces.append(pz.Block([[1,1,1,1]]))  # Small straight

class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

def generatePuzzle(row,col,avgSize):
    """Generate a puzzle with pieces around avgSize (in fact, this is just max size)"""
    tol = 100  # Number of attempts to make for each piece
    pieces = set([])
    board = np.zeros((row, col))  # Will fill this with +ve integers as the algorithm progresses
    nextSquare = Point(0,0)
    completed = False
    pieceNumber = 1 # Identifier for each piece, so boards are not just a matrix of ones
    while not completed:
        """We try to add a block starting in 'next' position. Always connected, unlikely to be not simply connected.
        During construction represent a piece by using a list of coordinates for the squares present"""

        tempBlock = [nextSquare]
        board[nextSquare.x,nextSquare.y] = pieceNumber
        numSquares = 1
        for i in range (0,avgSize-1):
            viable = False
            attempts = 0
            while attempts < tol and (not viable):
                attempts +=1
                # First pick a piece to grow from
                piece = tempBlock[math.floor(random.random()*numSquares)]
                # Now a direction to grow in
                rand = math.floor(random.random()*4)
                if (rand == 0) and (piece.x+1<=row-1):
                    new = Point(piece.x + 1,piece.y)
                    if board[new.x,new.y] == 0:
                        viable = True
                        tempBlock.append(new)
                        numSquares += 1
                        board[new.x,new.y] = pieceNumber

                elif (rand == 1) and (piece.x - 1 >= 0):
                    new = Point(piece.x - 1,piece.y)
                    if board[new.x,new.y] == 0:
                        viable = True
                        tempBlock.append(new)
                        numSquares += 1
                        board[new.x,new.y] = pieceNumber

                elif (rand == 2) and (piece.y + 1 <= col-1):
                    new = Point(piece.x,piece.y + 1)
                    if board[new.x,new.y] == 0:
                        viable = True
                        tempBlock.append(new)
                        numSquares += 1
                        board[new.x,new.y] = pieceNumber

                elif (rand == 3) and (piece.y - 1 >= 0):
                    new = Point(piece.x, piece.y - 1)
                    if board[new.x,new.y] == 0:
                        viable = True
                        tempBlock.append(new)
                        numSquares += 1
                        board[new.x,new.y] = pieceNumber

        #Construct the block with its regular representation
        minX = float('inf')
        maxX = -float('inf')
        minY = float('inf')
        maxY = -float('inf')
        for square in tempBlock:
            minX = min(minX,square.x)
            maxX = max(maxX,square.x)
            minY = min(minY,square.y)
            maxY = max(maxY,square.y)

        config = np.zeros((maxX-minX+1,maxY-minY+1))

        for square in tempBlock:
            config[square.x-minX,square.y-minY] = pieceNumber

        pieces.add(pz.Block(config))

        # Prepare for the next pass
        pieceNumber +=1
        # Find the next square we need to fill, if any
        completed = True
        flag = 0
        for i in range(0,row):
            for j in range(0,col):
                if board[i,j] == 0:
                    completed = False
                    nextSquare = Point(i,j)
                    flag = 1
                    break

            if flag:
                break

    # Print here to show a completed board
    #print(board)

    return pz.Puzzle(row,col,frozenset(pieces))
