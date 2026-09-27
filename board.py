import random
import pygame
import math

BLACK_TEXT = (119, 110, 101)
WHITE_TEXT = (255, 255, 255)

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
        self.tiles = [[0] * 5 for _ in range(5)]
        print(self.tiles)
        self.initFontSizes()
    
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