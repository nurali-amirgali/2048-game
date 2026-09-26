import random
import pygame

class Board:
    def __init__(self, screen, x=0, y=0, tileSize=50, numTilesX=5,numTilesY=5):
        self.screen = screen
        self.numTilesX = numTilesX
        self.numTilesY = numTilesY
        self.x = x
        self.y = y
        self.tileSize = tileSize
        self.tiles = [[0] * 5 for _ in range(5)]
        
    def render(self):
        gapSize = 6
        boardWidth = self.numTilesX * self.tileSize + gapSize
        boardHeight = self.numTilesY * self.tileSize + gapSize
        x = self.x - (boardWidth/2) - (gapSize/2)
        y = self.y - (boardHeight/2) - (gapSize/2)
        pygame.draw.rect(self.screen, (155, 137, 122), (x, y, boardWidth, boardHeight), border_radius=13)
        
        for row in range(self.numTilesY):
            for col in range(self.numTilesX):
                drawX = (col * self.tileSize) + x + gapSize
                drawY = (row * self.tileSize) + y + gapSize
                pygame.draw.rect(self.screen, (238, 228, 218), (drawX, drawY, self.tileSize - gapSize, self.tileSize - gapSize), border_radius=9)