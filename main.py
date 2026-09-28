import pygame
import sys
from board import Board

WIDTH = 800
HEIGHT = 600
FPS = 60

BG_COLOR = (250, 248, 240)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True)
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

boardX = WIDTH/2
boardY = HEIGHT/2
board = Board(screen, x=boardX, y=boardY, tileSize=90)
board.placeRandomTile()
board.placeRandomTile()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                board.makeMove(3)
                board.placeRandomTile()
            if event.key == pygame.K_d:
                board.makeMove(1)
                board.placeRandomTile()
            if event.key == pygame.K_w:
                board.makeMove(0)
                board.placeRandomTile()
            if event.key == pygame.K_s:
                board.makeMove(2)
                board.placeRandomTile()
            
    screen.fill(BG_COLOR)
    board.render()
    
    pygame.display.flip() 
    
    clock.tick(FPS) 
    
pygame.quit()
sys.exit()
