import pygame
from pygame.locals import *

def freedoms(board, x, y, old = []):
    free = 0
    stones = [(x, y)]
    spot = board[y][x]
    
    for vx, vy in ((0, -1), (1, 0), (0, 1), (-1, 0)): # vier durchlaeufe
        cx, cy = (x+vx, y+vy) # compare
##        if x == 0 and y == 0:
##            print(cx, cy)
        
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
bg = (200, 150, 80)
fenster = pygame.display.set_mode((ww, wh))


offset = 50

grid = 9
grid_size = [((ww-offset) // grid), ((wh-offset) // grid)]  ;      grid_size.sort()
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

passed = 0
last_placed = False

run = 1
clock = pygame.time.Clock()

while run:
    
    
    for e in pygame.event.get():
        if e.type == QUIT:
            run -= 1
        if e.type == MOUSEBUTTONDOWN:
            mpress = e.pos
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                turn *= -1
                #passed += 1

    if passed > 1:
        pygame.display.set_caption("MyGo  -  Spielende")
    else:
        pygame.display.set_caption("MyGo  -  " + labels[turn] + " am Zug.")

    mpos = pygame.mouse.get_pos()
    gx = int((mpos[0]-offset+ 0.5*grid_size) // grid_size)
    gy = int((mpos[1]-offset+ 0.5*grid_size) // grid_size)

    # placing stones
    if mpress and passed < 2:

        if 0 <= gx < grid and 0 <= gy < grid:
            if board[gy][gx] == 0:
                
                
                board[gy][gx] = players[turn] # just place this stone first (suicide check comes later)

                last_placed = (gx, gy)
                
                turn *= -1
                passed = 0
            
    
    # calculating stones (after placing stone)

    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            #print(spot)
            
            if spot != 0:
                # pruefe auf Freiheiten und eigene Nachbarn
                if (x, y) != last_placed:
                    free, chain = freedoms(board, x, y)
                    #print(free, chain)
                    
                    
                    # Auswertung
                    if free <= 0: # min: 0...
                    
                        for spot in chain:# + [(x, y)]: # Alle Steine der Kette loeschen                     
                            board[spot[1]][spot[0]] = 0
                                 
    # then remove suicidal stones
    if last_placed:
        print(freedoms(board, last_placed[0], last_placed[1]))
        
        if freedoms(board, last_placed[0], last_placed[1])[0] <= 0:
            
          
            board[last_placed[1]][last_placed[0]] = 0
          
            last_placed = False
            turn *= -1
    
    if board[0][0] != 0:
        print(board[0][0], freedoms(board, 0, 0))

    #last_placed = False
    mpress = False
    
    fenster.fill(bg)
    
    # draw cursor
    pygame.draw.circle(fenster, (80, 50, 40), (offset+gx*grid_size, offset+gy*grid_size), 2/5*grid_size, 4)
    
    for y in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset, offset+y*grid_size), (offset+(grid-1)*grid_size, offset+y*grid_size), 4)
    for x in range(grid): 
        pygame.draw.line(fenster, (0,0,0), (offset+x*grid_size, offset), (offset+x*grid_size, offset+(grid-1)*grid_size), 4)
               
    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            if spot != 0:
                pygame.draw.circle(fenster, colors[spot], (offset + x*grid_size, offset + y*grid_size), grid_size*2/5)
        
    # Weitere Anzeigen
    pygame.draw.circle(fenster, colors[players[turn]], (offset + (grid+1)*grid_size, offset+grid_size), grid_size*2/5)
    
    pygame.display.update()
    clock.tick(80)
    
pygame.quit()






