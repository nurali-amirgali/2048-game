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

font = pygame.font.Font(None, 80)
endFont = pygame.font.Font(None, 150)

boardX = WIDTH/2
boardY = HEIGHT/2
board = None
gameOver = False

def setupBoard():
    global board, gameOver
    board = Board(screen, x=boardX, y=boardY, tileSize=90)
    board.placeRandomTile()
    board.placeRandomTile()
    gameOver = False

setupBoard()
i = 0
running = True
while running:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                board.makeMove(3)
            if event.key == pygame.K_d:
                board.makeMove(1)
            if event.key == pygame.K_w:
                board.makeMove(0)
            if event.key == pygame.K_s:
                board.makeMove(2)
            if event.key == pygame.K_r or event.key == pygame.K_2 or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                if gameOver:
                    setupBoard()
            if event.key == pygame.K_p or event.key == pygame.K_o:
                board.makeMove(i)
                i += 1
                i = i % 4

    screen.fill(BG_COLOR)
    board.render()
    
    text = font.render(str(board.score), True, (152, 136, 118))
    width, height = font.size(str(board.score))
    screen.blit(text, ((WIDTH/2) - (width/2), 30))
    
    if board.isGameOver():
        text = endFont.render("GAME OVER!", True, (255,0,0))
        width, height = endFont.size("GAME OVER!")
        screen.blit(text, ((WIDTH/2) - (width/2), (HEIGHT/2) - (height/2)))
        gameOver = True
    
    board.animationTick(dt)
    
    pygame.display.flip() 
    
pygame.quit()
sys.exit()
