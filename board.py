import random
import pygame
import math
from copy import deepcopy
from dataclasses import dataclass

BLACK_TEXT = (119, 110, 101)
WHITE_TEXT = (255, 255, 255)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

colors = [
    ((238, 228, 218),BLACK_TEXT),
    ((235, 215, 183),BLACK_TEXT),
    ((242, 175, 117),WHITE_TEXT),
    ((246, 145, 94),WHITE_TEXT),
    ((248, 128, 100),WHITE_TEXT),
    ((246, 100, 67), WHITE_TEXT),
    ((240, 210, 105),WHITE_TEXT),
    ((238, 204, 97),WHITE_TEXT),
    ((238, 201, 80),WHITE_TEXT),
    ((238, 196, 63),WHITE_TEXT),
    ((237, 193, 46),WHITE_TEXT),
    ((181, 134, 180),WHITE_TEXT),
    ((168, 97, 171),WHITE_TEXT),
    ((160, 72, 162),WHITE_TEXT),
    ((128, 0, 128),WHITE_TEXT),
    ((96, 0, 70),WHITE_TEXT),
    ((139, 134, 227),WHITE_TEXT)
]

class AnimTile:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 40
        self.targetX = 0
        self.targetY = 0
        self.time = 0
        self.arrivalTime = 0

@dataclass
class MoveInfo:
    fromSquare: tuple[int, int]
    toSquare: tuple[int, int]
    merge: bool
    newValue: int

class Board:
    def __init__(self, screen, x=0, y=0, tileSize=50, numTilesX=4,numTilesY=4):
        self.screen = screen
        self.numTilesX = numTilesX
        self.numTilesY = numTilesY
        self.x = x
        self.y = y
        self.maxTextWidth = 0.7
        self.maxTextHeight = 0.35
        self.tileSize = tileSize
        self.defaultFont = pygame.font.SysFont(None, 36)
        self.fonts = []
        self.tiles = [[0] * numTilesX for _ in range(numTilesY)]
        self.initFontSizes()
        
        self.moveSpeed = 0.1
        self.lastTiles = deepcopy(self.tiles)
        self.renderSquares = 0
    
    def animationTick(self, dt):
        pass
    
    def moveLeft(self, array):
        moveReport = []
        array = array.copy()
        i = 0
        currentValue = 0
        currentIndex = 0
        while i < len(array):
            value = array[i]
            if value != 0:
                if value == currentValue:
                    move = MoveInfo((i, 0), (currentIndex, 0), True, value * 2)
                    moveReport.append(move)
                    
                    array[i] = 0
                    array[currentIndex] = value * 2
                    i = currentIndex + 1
                    currentValue = value * 2
                else:
                    newIndex = currentIndex if currentValue == 0 else currentIndex + 1
                    array[i] = 0
                    array[newIndex] = value
                    currentValue = value
                    currentIndex = newIndex
                    
                    if i != newIndex:
                        move = MoveInfo((i, 0), (newIndex, 0), False, 0)
                        moveReport.append(move)
            i += 1
        return array, moveReport
        
    def makeMove(self, move):
        moveInfoList = []
        if move == LEFT or move == RIGHT:
            for row in range(self.numTilesY):
                if move == LEFT:
                    self.tiles[row], rawMoveInfo = self.moveLeft(self.tiles[row])
                    newInfoList = []
                    for info in rawMoveInfo:
                        if info:
                            newInfoList.append(MoveInfo((row, info.fromSquare[0]), (row, info.toSquare[0]), info.merge, info.newValue))
                    moveInfoList.extend(newInfoList)
                else:
                    newRow, rawMoveInfo = self.moveLeft(self.tiles[row][::-1]) #[::-1] reverses an array
                    self.tiles[row] = newRow[::-1]
                    
                    newInfoList = []
                    for info in rawMoveInfo:
                        if info:
                            newInfoList.append(MoveInfo((row, len(self.tiles[row]) - 1 - info.fromSquare[0]), (row, len(self.tiles[row]) - 1 - info.toSquare[0]), 
                                                        info.merge, info.newValue))
                    moveInfoList.extend(newInfoList)
        else:
            for col in range(self.numTilesX):
                currentCol = []
                for row in range(self.numTilesY):
                    currentCol.append(self.tiles[row][col])       
                
                if move == DOWN:
                    currentCol = currentCol[::-1]
                    
                newCol, rawMoveInfo = self.moveLeft(currentCol)
                newInfoList = []
                for info in rawMoveInfo:
                    if info:
                        newFrom = info.fromSquare[0]
                        newTo = info.toSquare[0]
                        if move == DOWN:
                            newFrom = len(currentCol) - 1 - newFrom
                            newTo = len(currentCol) - 1 - newTo
                        newInfoList.append(MoveInfo((newFrom, col), (newTo, col), info.merge, info.newValue))
                moveInfoList.extend(newInfoList)
                if move == DOWN:
                    newCol = newCol[::-1]
                    
                for row in range(self.numTilesY):
                    self.tiles[row][col] = newCol[row]
        print(moveInfoList)
    
    def placeRandomTile(self, newValue=2):
        availableTiles = []
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                value = self.tiles[row][col]
                if value == 0:
                    availableTiles.append((row,col))
        if availableTiles:
            randomTile = random.choice(availableTiles)
            self.tiles[randomTile[0]][randomTile[1]] = newValue
    
    def initFontSizes(self):
        font = pygame.font.SysFont(None, 36)
        for i in range(1, len(colors)):
            value = int(2**i)
            width, height = font.size(str(value))
            diffX = (self.tileSize*self.maxTextWidth) - width 
            diffY = (self.tileSize*self.maxTextHeight) - height
            change = 0
            if diffX < diffY:
                change = (self.tileSize*self.maxTextWidth)/width
            else:
                change = (self.tileSize*self.maxTextHeight)/height
            newFont = pygame.font.SysFont(None, round(36 * change))
            self.fonts.append(newFont)
        
    def render(self):
        gapSize = 8
        boardWidth = self.numTilesX * self.tileSize + gapSize
        boardHeight = self.numTilesY * self.tileSize + gapSize
        x = self.x - (boardWidth/2) - (gapSize/2)
        y = self.y - (boardHeight/2) - (gapSize/2)
        pygame.draw.rect(self.screen, (155, 137, 122), (x, y, boardWidth, boardHeight), border_radius=13)
        
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                drawX = (col * self.tileSize) + x + gapSize
                drawY = (row * self.tileSize) + y + gapSize
                value = self.tiles[row][col]
                color = (189, 172, 151)
                textColor = (255,255,255)
                colorIndex = None
                if value:
                    colorIndex = int(math.log2(value)-1)
                    try:
                        color, textColor = colors[colorIndex]
                    except IndexError:
                        colorIndex = None
                        color = (255,0,0)
                drawWidth = self.tileSize - gapSize
                drawHeight = self.tileSize - gapSize
                pygame.draw.rect(self.screen, color, (drawX, drawY, drawWidth, drawHeight), border_radius=9)

                if value:
                    sizeIndex = int(math.log2(value)-1)
                    try:
                        font = self.fonts[sizeIndex]
                    except IndexError:
                        font = self.defaultFont
                    valueText = str(value)
                    width, height = font.size(valueText)
                    surface = font.render(valueText, True, textColor)

                    textX = round(drawX + (drawWidth/2) - (width/2))
                    textY = round(drawY + (drawHeight/2) - (height/2))
                    self.screen.blit(surface, (textX, textY))