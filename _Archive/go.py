import pygame
from pygame.locals import *

ww, wh = (800, 600)

fenster = pygame.display.set_mode((ww, wh))


offset = 20

grid = 9
grid_size = [((ww-offset) // grid), ((wh-offset) // grid)]
grid_size.sort()
grid_size = grid_size[0]

print(grid_size)

board = [[0 for x in range(grid)] for y in range(grid)]
print(board)

# eingabe
turn = 1 # 1 == black; -1 == white
mpress = 0


run = 1
players = {1:2, -1:3}
colors = {2:(0,0,0), 3:(230, 230, 230)}
labels = {1:"Schwarz", -1:"Weiß"}

while run:
    pygame.display.set_caption("MyGo  -  " + labels[turn] + " am Zug.")
    
    for e in pygame.event.get():
        if e.type == QUIT:
            run -= 1
        if e.type == MOUSEBUTTONDOWN:
            mpress = e.pos
        

    if mpress:
        x = (mpress[0]-offset) // grid_size
        y = (mpress[1]-offset) // grid_size
        print(x, y)
        
        if board[y][x] == 0:
            board[y][x] = players[turn]
            
            turn *= -1
            
        mpress = False
    
    
    
    fenster.fill((170, 120, 80))
    
    for y in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset, offset+y*grid_size), (offset+(grid-1)*grid_size, offset+y*grid_size), 4)
    for x in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset+x*grid_size, offset), (offset+x*grid_size, offset+(grid-1)*grid_size), 4)
               
    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            if spot != 0:
                pygame.draw.circle(fenster, colors[spot], (offset + x*grid_size, offset + y*grid_size), grid_size*2/5)
        
    
    pygame.display.update()
    
pygame.quit()
    
    