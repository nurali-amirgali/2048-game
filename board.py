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

def multiply_tuple(pos, n):
    return tuple(x * n for x in pos)

def lerp_position(pos, target, current_time, arrival_time):
    t = min(current_time / arrival_time, 1)

    t = t * t * (3 - 2 * t)

    x = pos[0] + (target[0] - pos[0]) * t
    y = pos[1] + (target[1] - pos[1]) * t

    return x, y

def overshoot(t, amount=0.2):
    return 1 + amount * math.sin(math.pi * t)

@dataclass
class MoveInfo:
    fromSquare: tuple[int, int]
    toSquare: tuple[int, int]
    merge: bool
    newValue: int
    currentValue: int

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
        self.newTileCoord = (-1,-1)
        self.score = 0
        
        self.mergePercent = 0.5 #means it will start the animation at the 80% point
        self.currentMovement = []
        self.lastMovedTime = 0
        self.moveSpeed = 0.2
        self.oldTiles = deepcopy(self.tiles)
        
    def center(self, row, col, x, y, gapSize):
        return ((col * self.tileSize) + x + (self.tileSize/2) + (gapSize/2),
                (row * self.tileSize) + y + (self.tileSize/2) + (gapSize/2))
    
    def animationTick(self, dt):
        self.lastMovedTime += dt
    
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
                    move = MoveInfo((i, 0), (currentIndex, 0), True, value * 2, value)
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
                        move = MoveInfo((i, 0), (newIndex, 0), False, 0, value)
                        moveReport.append(move)
            i += 1
        return array, moveReport
        
    def makeMove(self, move):
        self.oldTiles = deepcopy(self.tiles)
        moveInfoList = []
        if move == LEFT or move == RIGHT:
            for row in range(self.numTilesY):
                if move == LEFT:
                    self.tiles[row], rawMoveInfo = self.moveLeft(self.tiles[row])
                    newInfoList = []
                    for info in rawMoveInfo:
                        if info:
                            newInfoList.append(MoveInfo((row, info.fromSquare[0]), (row, info.toSquare[0]), info.merge, info.newValue, info.currentValue))
                    moveInfoList.extend(newInfoList)
                else:
                    newRow, rawMoveInfo = self.moveLeft(self.tiles[row][::-1]) #[::-1] reverses an array
                    self.tiles[row] = newRow[::-1]
                    
                    newInfoList = []
                    for info in rawMoveInfo:
                        if info:
                            newInfoList.append(MoveInfo((row, len(self.tiles[row]) - 1 - info.fromSquare[0]), (row, len(self.tiles[row]) - 1 - info.toSquare[0]), 
                                                        info.merge, info.newValue, info.currentValue))
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
                        newInfoList.append(MoveInfo((newFrom, col), (newTo, col), info.merge, info.newValue, info.currentValue))
                moveInfoList.extend(newInfoList)
                if move == DOWN:
                    newCol = newCol[::-1]
                    
                for row in range(self.numTilesY):
                    self.tiles[row][col] = newCol[row]

        for move in moveInfoList:
            if move.merge:
                self.score += move.newValue
        
        self.lastMovedTime = 0
        self.currentMovement = moveInfoList
        self.placeRandomTile()
    
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
            self.newTileCoord = (randomTile[0], randomTile[1])
        else:
            self.newTileCoord = (-1, -1)
    
    def isGameOver(self):
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                if self.tiles[row][col] == 0:
                    return False
                
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] 
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                value = self.tiles[row][col]
                for dRow, dCol in directions:
                    newRow = row + dRow
                    newCol = col + dCol
                    if 0 <= newRow < self.numTilesY and 0 <= newCol < self.numTilesX:
                        if self.tiles[newRow][newCol] == value:
                            return False 

        return True
    
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
        
    def renderTile(self, drawSurface, x, y, value, gapSize = 8, scale = 1):
        if scale <= 0:
            return
        
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
                
        drawWidth = (self.tileSize - gapSize) * scale
        drawHeight = (self.tileSize - gapSize) * scale
        x = x - (drawWidth/2)
        y = y - (drawHeight/2)
        pygame.draw.rect(drawSurface, color, (x, y, drawWidth, drawHeight), border_radius=max(0, round(9 * scale)))
        
        if value:
            sizeIndex = int(math.log2(value)-1)
            try:
                font = self.fonts[sizeIndex]
            except IndexError:
                font = self.defaultFont
            valueText = str(value)

            surface = font.render(valueText, True, textColor)
            if scale < 1:                                             
                w, h = surface.get_size()                              
                surface = pygame.transform.smoothscale(               
                    surface, (max(1, round(w * scale)), max(1, round(h * scale))))
            
            textX = round(x + (drawWidth/2) - (surface.get_width()/2))
            textY = round(y + (drawHeight/2) - (surface.get_height()/2))
            drawSurface.blit(surface, (textX, textY))
    
    def render(self):
        gapSize = 8
        boardWidth = self.numTilesX * self.tileSize + gapSize
        boardHeight = self.numTilesY * self.tileSize + gapSize
        x = self.x - (boardWidth/2) - (gapSize/2)
        y = self.y - (boardHeight/2) - (gapSize/2)
        pygame.draw.rect(self.screen, (155, 137, 122), (x, y, boardWidth, boardHeight), border_radius=13)
        
        progress = max(0, min(1, self.lastMovedTime / self.moveSpeed))
        if progress == 1:
            for row in range(self.numTilesY):
                for col in range(self.numTilesX):
                    drawX, drawY = self.center(row, col, x, y, gapSize)
                    value = self.tiles[row][col]
                    self.renderTile(self.screen, drawX, drawY, value, gapSize)
                
        else:
            movingFrom = {move.fromSquare for move in self.currentMovement}
                
            for row in range(self.numTilesY):
                for col in range(self.numTilesX):
                    drawX, drawY = self.center(row, col, x, y, gapSize)
                    value = self.tiles[row][col]
                    if (row, col) not in movingFrom:
                        if (row, col) != self.newTileCoord:
                            self.renderTile(self.screen, drawX, drawY, self.oldTiles[row][col], gapSize)
                        else:
                            self.renderTile(self.screen, drawX, drawY, 0, gapSize)
                            self.renderTile(self.screen, drawX, drawY, self.tiles[row][col], gapSize, scale=progress)
                    else:
                        self.renderTile(self.screen, drawX, drawY, 0, gapSize)
            
            for move in self.currentMovement:
                fromSquare = multiply_tuple(move.fromSquare, self.tileSize)
                toSquare = multiply_tuple(move.toSquare, self.tileSize)
                
                fromX = fromSquare[1] + x + (self.tileSize/2) + (gapSize/2)
                fromY = fromSquare[0] + y + (self.tileSize/2) + (gapSize/2)
                toX = toSquare[1] + x + (self.tileSize/2) + (gapSize/2)
                toY = toSquare[0] + y + (self.tileSize/2) + (gapSize/2)
                
                fromSquare = (fromX, fromY)
                toSquare = (toX, toY)
                
                moveTimeEnd = self.moveSpeed * self.mergePercent
                drawPos = lerp_position(fromSquare, toSquare, self.lastMovedTime, moveTimeEnd)
                if moveTimeEnd > self.lastMovedTime or not move.merge:
                    moveTimeEnd = self.moveSpeed
                    self.renderTile(self.screen, drawPos[0], drawPos[1], move.currentValue, gapSize)
                else:
                    scaleProgress = 1 - (1 - progress) * (1/(1-self.mergePercent))
                    self.renderTile(self.screen, drawPos[0], drawPos[1], move.newValue, gapSize, scale=overshoot(scaleProgress))