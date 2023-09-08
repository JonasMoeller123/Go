import pygame
from pygame.locals import *

def freedoms(board, x, y, old = []):
    free = 0
    stones = [(x, y)]
    
    for vx, vy in ((0, -1), (1, 0), (0, 1), (-1, 0)): # vier durchlaeufe
        cx, cy = (x+vx, y+vy) # compare
        
        if 0 <= cx <= (grid-1) and 0 <= cy <= (grid-1):
            comp = board[cy][cx]
            
            if comp == 0: # Freiheit
                 free += 1
                
            elif comp == spot: # gleicher Stein
                if not (x,y) in old:
                    #print(old, [(x, y)])
                    
                      
                    f, stone = freedoms(board, cx, cy, (old + [(x, y)]))
                    free += f
                    stones += stone
                    # print("Angrenzend: ", stones)
                    # print()
                    
    
    # print((x, y), free, stones)
    return free, stones
    

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
adjacent = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Vektoren von Feld zu benachbarten Feldern


players = {1:2, -1:3}
colors = {2:(0,0,0), 3:(230, 230, 230)}
labels = {1:"Schwarz", -1:"Weiß"}

run = 1
clock = pygame.time.Clock()

while run:
    pygame.display.set_caption("MyGo  -  " + labels[turn] + " am Zug.")
    
    for e in pygame.event.get():
        if e.type == QUIT:
            run -= 1
        if e.type == MOUSEBUTTONDOWN:
            mpress = e.pos
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                turn *= -1
        
    mpos = pygame.mouse.get_pos()
    gx = int((mpos[0]-offset+ 0.5*grid_size) // grid_size)
    gy = int((mpos[1]-offset+ 0.5*grid_size) // grid_size)

    if mpress:
        
        #print(gx, gy)
        if 0 <= gx < grid and 0 <= gy < grid:
            if board[gy][gx] == 0:
                board[gy][gx] = players[turn]
            
                turn *= -1
            
        
    
    
    # calculating stones (after placing stone)

    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            #print(spot)
            
            if spot != 0:
                # pruefe auf Freiheiten und eigene Nachbarn
                free, remove = freedoms(board, x, y)
                

                # Auswertung
                
                if free <= 0: # min: 0...
                    #print(free, remove)
                
                    for spot in remove + [(x, y)]:
                        print("Loeschen")
                        
                        board[spot[1]][spot[0]] = 0
                
                    
    
    mpress = False
    
    
    fenster.fill((170, 120, 80))
    
    # draw cursor
    pygame.draw.circle(fenster, (80, 50, 40), (20+gx*grid_size, 20+gy*grid_size), 2/5*grid_size, 4)
    
    for y in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset, offset+y*grid_size), (offset+(grid-1)*grid_size, offset+y*grid_size), 4)
    for x in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset+x*grid_size, offset), (offset+x*grid_size, offset+(grid-1)*grid_size), 4)
               
    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            if spot != 0:
                pygame.draw.circle(fenster, colors[spot], (offset + x*grid_size, offset + y*grid_size), grid_size*2/5)
        
    
    pygame.display.update()
    clock.tick(10)
    
pygame.quit()
    
    