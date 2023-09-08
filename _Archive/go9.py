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
bg_bright = (200, 170, 120)

ctext = (0,0,0)

fps = 80

window = pygame.display.set_mode((ww, wh))

pygame.mixer.music.load("stone.wav")


# text fonts
text_title = pygame.font.SysFont(None, r(wh/4))
text_subt  = pygame.font.SysFont(None, r(wh/8))
text_subt2 = pygame.font.SysFont(None, r(ww/24))

text = pygame.font.SysFont(None, 25)


# Main menu text
title = text_title.render("MyGo", True, ctext)

subt1 = text_subt.render("Press [Space] to start.", True, ctext)
subt2 = text_subt.render("[Backspace] for new game.", True, ctext)
subt3 = text_subt.render("Press [Esc] to exit game.", True, ctext)

subt4 = text_subt2.render("Use arrow keys to change.", True, ctext)
subt5 = text_subt.render("Board size:", True, ctext)
subt6 = text_subt2.render("Press [F1] and [F2] to change Fullscreen", True, ctext)
y_fullscreen_text = 550


# constants and basic config
grid = 9 # will be changed in the main menu
offset = ww / 16
adjacent = [(0, -1), (1, 0), (0, 1), (-1, 0)] # left, above, right, below

players = {1:2,         -1:3}
colors  = {2:(0,0,0),   3:(230, 230, 230)}
labels  = {1:"Schwarz", -1:"Weiß"}



# Run Variables for the program
run = 1

run_menu = 1

run_game = 1
paused = 0
# run_end = 1 ???? gebraucht?


clock = pygame.time.Clock()

while run:  # Main loop

    
    # Menu
    while run_menu:
        for e in pygame.event.get():
            if e.type == QUIT:
                run -= 1
                run_menu = 0
                run_game = 0
                
            if e.type == MOUSEBUTTONDOWN:
                mpress = e.pos

            if e.type == KEYDOWN:
                if not paused:
                    if e.key == K_UP:
                        grid += 1 #* grid < 19

                    if e.key == K_DOWN:
                        grid -= 1 * grid > 3
                    
                if e.key == K_SPACE:
                    run_menu = 0
                    run_game = 1
                
                if e.key == K_BACKSPACE:
                    paused = 0
                    
                if e.key == K_ESCAPE:
                    run = 0
                    run_menu = 0
                    run_game = 0
                    
                if e.key == K_F1:
                    window = pygame.display.set_mode((ww, wh), pygame.FULLSCREEN)
                if e.key == K_F2:
                    window = pygame.display.set_mode((ww, wh))

        
        if paused:
            subt1 = text_subt.render("[Space] to continue game.", True, ctext)
        else:
            subt1 = text_subt.render("Press [Space] to start.", True, ctext)
        
        subt_grid = text_subt.render("{} x {}".format(grid, grid), True, ctext)

        window.fill(bg_bright)

        window.blit(title, (offset, 50))

        
        
        if paused:
            window.blit(subt1, (offset, 380)) # Space bar
            window.blit(subt2, (offset, 430))
            window.blit(subt3, (offset, 480))
            
        else:
            pygame.display.set_caption("MyGo")
            window.blit(subt1, (offset, 400)) # Space bar
            window.blit(subt3, (offset, 475))
        
        window.blit(subt4, (480, 180))        
        window.blit(subt5, (480, offset))#(325, 100))
        window.blit(subt_grid, (480, offset+75))
        window.blit(subt6, (100, 550) )


        # Board icon
        margin = 10
        size = 130
        rect = (480, 220, size+2*margin, size+2*margin)
        x = rect[0]+margin; y = rect[1]+margin

        gap = (rect[2]-2*margin) / (grid-1)

        pygame.draw.rect(window, bg, rect)
        pygame.draw.rect(window, ctext, rect, 2)

        for i in range(grid):
            pygame.draw.line(window, (0,0,0), rund((x, y+i*gap)), rund((x+(grid-1)*gap, y+i*gap)), 1) # horizontal
            
            pygame.draw.line(window, (0,0,0), rund((x+i*gap, y)), rund((x+i*gap, y+(grid-1)*gap)), 1) # vertikal
        
        
        


        pygame.display.update()
        clock.tick(fps)


        
    if not paused:
        
        # Board configuration
        
        grid_size = [(ww // (grid+2)), (wh // (grid+2))]  ;      grid_size.sort()
        #grid_size = [((ww-2*grid_size) // grid), ((wh-grid_size) // grid)]
        grid_size = int(grid_size[0])

        board = [[0 for x in range(grid)] for y in range(grid)]

        st_rad = (grid_size * 4/10)
        line_width = int(round(1/5*st_rad)) or 1

        # Input
        turn = 1 # 1 == black; -1 == white
        turn_counter = 1


        # stone placement
        mpress = 0
        passed = 0
        last_placed = False
        remove      = 0
        captured = [0, 0, 0, 0] # 0 1 2 3
    
        

    # reset menu variable to True
    run_menu = 1
    upper_s = 40
    s = grid_size * 0.5; s = (not (s>20)*s) * 20 + (20 < s <= upper_s) * s + (s > upper_s) * upper_s
    print(s)
    text = pygame.font.SysFont(None, r(s))


    print(grid_size) # war ~61 bei 9x9
    # Game loop
    while run_game:
        
    
        for e in pygame.event.get():
            if e.type == QUIT:
                run -= 1
                run_menu = 0
                run_game = 0
                
            if e.type == MOUSEBUTTONDOWN:
                mpress = e.button
                #mpress = e.pos
            
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    paused = 1
                    run_game = 0
                    run = 1; run_menu = 1
                    
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
            pygame.display.set_caption("MyGo - im Spiel - {} am Zug. - Zug: {}".format(labels[turn], turn_counter))
        
        
        mpos = pygame.mouse.get_pos()
        gx = int((mpos[0]-grid_size+ 0.5*grid_size) // grid_size)
        gy = int((mpos[1]-grid_size+ 0.5*grid_size) // grid_size)

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

                    #if mpress == 1: # right click to easily create scenarios
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
     
        
        window.fill(bg)
        
        # Information for the player
        
        # cursor
        if 0 <= gx < grid and 0 <= gy < grid:
            pygame.draw.circle(window, (80, 50, 40), rund([(gx+1)*grid_size, (gy+1)*grid_size]), r(st_rad), line_width)
        
        # text
        box = [(grid+1)*grid_size, grid_size]
        rx, ry = box
        height = (grid-1)*grid_size
        
        
        text1 = text.render("Geschlagene Steine:", True, (0,0,0))
        text2 = text.render("Am Zug:", True, (0,0,0))
        
        text_b = text.render(str(captured[2]), True, (0,0,0))
        text_w = text.render(str(captured[3]), True, (0,0,0))
        
        # window.blit(text1, (rx, ry)) # Captured stones
        
        # pygame.draw.circle(window, colors[2], rund((1/2*grid_size + rx, ry+grid_size)), r(st_rad)) # +20 < 
        # pygame.draw.circle(window, colors[3], rund((3/2*grid_size + rx, ry+grid_size)), r(st_rad)) # +20 < 3/4*grid_size
        # window.blit(text_b, rund((1/2*grid_size + rx, ry+1.6*grid_size)))#+5/4*grid_size)))
        # window.blit(text_w, rund((3/2*grid_size + rx, ry+1.6*grid_size)))#5/4*grid_size)))
        
        
        # window.blit(text2, (rx, ry+4*grid_size)) # Who's turn
        # pygame.draw.circle(window, colors[players[turn]], rund((1/2*grid_size + rx, ry+5*grid_size)), r(st_rad)) # 
        
        
        window.blit(text1, (rx, ry+0.05*height)) # Captured stones
        
        pygame.draw.circle(window, colors[2], rund((1/2*grid_size + rx, ry+0.05*height+s+st_rad)), r(st_rad)) # +20 < 
        pygame.draw.circle(window, colors[3], rund((3/2*grid_size + rx, ry+0.05*height+s+st_rad)), r(st_rad)) # +20 < 3/4*grid_size
        window.blit(text_b, rund((1/2*grid_size + rx, ry+0.05*height+1.5*s+2*st_rad)))#+5/4*grid_size)))
        window.blit(text_w, rund((3/2*grid_size + rx, ry+0.05*height+1.5*s+2*st_rad)))#5/4*grid_size)))
        
        
        window.blit(text2, (rx, (ry+0.1*height+s+2*st_rad) +0.1*height + grid_size)) # Who's turn
        pygame.draw.circle(window, colors[players[turn]], rund((1/2*grid_size + rx, (ry+0.1*height+s+2*st_rad) + 0.1*height + grid_size +s+st_rad )), r(st_rad)) # 
            
        
        ############## Zeichnen des Spielbrettes ##############
        for y in range(grid): 
            pygame.draw.line(window, (0,0,0), rund((grid_size, (y+1)*grid_size)), rund(( grid*grid_size, (y+1)*grid_size )), line_width)
        for x in range(grid): 
            pygame.draw.line(window, (0,0,0), rund(((x+1)*grid_size, grid_size)), rund(( (1+x)*grid_size, grid*grid_size )), line_width)
                   
        for y, row in enumerate(board):
            for x, spot in enumerate(row):
                if spot != 0:
                    pygame.draw.circle(window, colors[spot], rund(((x+1)*grid_size, (y+1)*grid_size)), r(st_rad))
            
        
        
        pygame.display.update()
        clock.tick(fps)


# Quit game after window cross has been clicked
    
pygame.quit()














