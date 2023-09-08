import pygame
from pygame.locals import *


def rund(pos):
    return [int(round(i)) for i in pos]

def r(i):
    return int(round(i))

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
                if not (cx, cy) in old:
                    #print(old, [(x, y)])
                    
                      
                    f, stone = freedoms(board, cx, cy, (old + [(x, y)]))
                    free += f
                    stones += stone
                    #stones = list(set(stones))
                    # print("Angrenzend: ", stones)
                    # print()
                    
    
    # print((x, y), free, stones)
    return free, stones


pygame.init()


ww, wh = (800, 600)
bg = (200, 150, 80)
fenster = pygame.display.set_mode((ww, wh))

pygame.mixer.music.load("stone.wav")

# text
text = pygame.font.SysFont(None, 25)


 # Board configuration
offset = ww / 16

grid = 7
grid_size = [((ww-2*offset) // grid), ((wh-offset) // grid)]  ;      grid_size.sort()
grid_size = int(grid_size[0])

board = [[0 for x in range(grid)] for y in range(grid)]

st_rad = grid_size * 7/20


# Input
turn = 1 # 1 == black; -1 == white
mpress = 0
adjacent = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Vektoren von Feld zu benachbarten Feldern


players = {1:2,         -1:3}
colors  = {2:(0,0,0),   3:(230, 230, 230)}
labels  = {1:"Schwarz", -1:"Weiß   "}

captured = [0, 0, 0, 0] # 0 1 2 3

turn_counter = 1

passed = 0
last_placed = False
remove      = 0

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
                turn_counter += 1
                #passed += 1
            if e.key == K_MINUS:
                remove = 1

        if e.type == KEYUP:
            if e.key == K_MINUS:
                remove = 0

    if passed > 1:
        pygame.display.set_caption("MyGo  -  Spielende")
    else:
        pygame.display.set_caption("MyGo  -  {} am Zug. - Zug {}".format(labels[turn], turn_counter))
    
    
    mpos = pygame.mouse.get_pos()
    gx = int((mpos[0]-offset+ 0.5*grid_size) // grid_size)
    gy = int((mpos[1]-offset+ 0.5*grid_size) // grid_size)

    # remove stone with force remove key (-)
    if remove:
        board[gy][gx] = 0
        

    # placing stones
    if mpress and passed < 2:
        if 0 <= gx < grid and 0 <= gy < grid:
            if board[gy][gx] == 0:
                
                board[gy][gx] = players[turn] # just place this stone first (suicide check comes later)
                pygame.mixer.music.play()
                last_placed = (gx, gy)

                turn_counter += 1
                turn *= -1
                passed = 0
        
        mpress = False
    
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
                    if free <= 0 and spot != players[-turn]: # min: 0...
                    
                        for spot in set(chain):# + [(x, y)]: # Alle Steine der Kette loeschen                     
                            captured[board[spot[1]][spot[0]]] += 1    
                            board[spot[1]][spot[0]] = 0
                            
                                 
    # then remove suicidal stones
    if last_placed:        
        if freedoms(board, last_placed[0], last_placed[1])[0] <= 0:
          
            board[last_placed[1]][last_placed[0]] = 0
          
            last_placed = False
            turn_counter -= 1
            turn *= -1
 
    
    fenster.fill(bg)
    
    # Information for the player
    
    # cursor
    pygame.draw.circle(fenster, (80, 50, 40), rund((offset+gx*grid_size, offset+gy*grid_size)), r(st_rad), 4)
    
    # text
    box = [grid*grid_size, offset]
    rx, ry = box
    
    text1 = text.render("Geschlagene Steine:", True, (0,0,0), bg)
    text2 = text.render("Am Zug:", True, (0,0,0), bg)
    
    text_b = text.render(str(captured[2]), True, (0,0,0), bg)
    text_w = text.render(str(captured[3]), True, (0,0,0), bg)
    
    fenster.blit(text1, (rx, ry))
    pygame.draw.circle(fenster, colors[2], rund((1/2*grid_size + rx, ry+3/4*grid_size)), r(st_rad))
    pygame.draw.circle(fenster, colors[3], rund((3/2*grid_size + rx, ry+3/4*grid_size)), r(st_rad))
    fenster.blit(text_b, rund((1/2*grid_size + rx, ry+5/4*grid_size)))
    fenster.blit(text_w, rund((3/2*grid_size + rx, ry+5/4*grid_size)))
    
    
    fenster.blit(text2, (rx, ry+3*grid_size))
    pygame.draw.circle(fenster, colors[players[turn]], rund((1/2*grid_size + rx, ry+3.75*grid_size)), r(st_rad))
        
    
    ############## Zeichnen des Spielbrettes ##############
    for y in range(grid): 
        pygame.draw.line(fenster, (0,0,0), rund((offset, offset+y*grid_size)), rund((offset+(grid-1)*grid_size, offset+y*grid_size)), 4)
    for x in range(grid): 
        pygame.draw.line(fenster, (0,0,0), rund((offset+x*grid_size, offset)), rund((offset+x*grid_size, offset+(grid-1)*grid_size)), 4)
               
    for y, row in enumerate(board):
        for x, spot in enumerate(row):
            if spot != 0:
                pygame.draw.circle(fenster, colors[spot], rund((offset + x*grid_size, offset + y*grid_size)), r(st_rad))
        
    
    
    pygame.display.update()
    clock.tick(80)
    
pygame.quit()






