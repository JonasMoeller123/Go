import pygame, random, math
from pygame.locals import *

from module import *


pygame.init()


ww, wh = (800, 600)
bg = (200, 150, 80)
bg_bright = (200, 170, 120)

black = (0,0,0)
black_edge = (20, 20, 20)
white = (230, 230, 230)
white_edge = (200, 200, 200)

wood1 = (120, 50, 20)
wood2 = (80, 20, 10)

ctext = (0,0,0)
clines = (0,0,0)

fps = 80

window = pygame.display.set_mode((ww, wh))

pygame.mixer.music.load("stone.wav")


# game replay config
frame_cut = "---\n"
replay_name = "last_replay.txt"


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
#adjacent = [(0, -1), (1, 0), (0, 1), (-1, 0)] # above, right, below, left
adjacent = [(1, 0), (0, 1)]

players = {1:2,         -1:3}
colors  = {2:black,   3:white, 4:black_edge, 5:white_edge}
labels  = {1:"black", -1:"white"}

stones = {2:None, 3:None} # stone list


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


    # after menu
    
    if not paused: # initializing new board
        stones[2] = []; stones[3] = []
        
        for i in range(r(grid*0.75*grid)):
            stones[2].append( [random.randint(20, 100)/100, random.randint(0, 100)/100] ) # [dist, angle]
            stones[3].append( [random.randint(20, 100)/100, random.randint(0, 100)/100] )
        
        
        # Board configuration
        
        grid_size = [(ww // (grid+2)), (wh // (grid+2))]  ;      grid_size.sort()
        #grid_size = [((ww-2*grid_size) // grid), ((wh-grid_size) // grid)]
        grid_size = int(grid_size[0])

        board = [[0 for x in range(grid)] for y in range(grid)]

        st_rad = r(grid_size * 4/10)
        line_width = int(round(1/5*st_rad)) or 1

        # Input
        turn = 1 # 1 == black; -1 == white
        turn_counter = 1

        # game replay save
        # replay = open(replay_name, "w")
        gamesave = save()

        # stone pits
        #size = r(2*grid_size); size = r(0.25*((grid-1)*grid_size))
        size = 2.9*grid_size#; size = size

        surface_black = pygame.Surface((size, size))
        surface_white = pygame.Surface((size, size))

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
    #print(s)
    text = pygame.font.SysFont(None, r(s))

    #print(grid_size) # war ~61 bei 9x9
    
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
            pygame.display.set_caption("MyGo - Spielende")
        else:
            pygame.display.set_caption("MyGo - in match - {}'s turn. - turn: {}".format(labels[turn], turn_counter))

        
        mpos = pygame.mouse.get_pos()
        gx = int((mpos[0]-grid_size+ 0.5*grid_size) // grid_size)
        gy = int((mpos[1]-grid_size+ 0.5*grid_size) // grid_size)

        # remove stone with force remove key (-)
        if remove:
            board[gy][gx] = 0

        placed_stone = False
        
        # placing stones
        if mpress and passed < 2:
            if 0 <= gx < grid and 0 <= gy < grid:
                if board[gy][gx] == 0:
                    
                    board[gy][gx] = players[turn] # just place this stone first (suicide check comes later)
                    pygame.mixer.music.play()
                    last_placed = (gx, gy)
                    placed_stone = True
                    
                    #if mpress == 1: # right click to easily create scenarios
                    turn_counter += 1
                    turn *= -1
                        
                    passed = 0

        
        # calculating stone freedoms (after placing stone)
        for y, row in enumerate(board):
            for x, spot in enumerate(row):
                #print(spot)
                
                if spot != 0:
                    # pruefe auf Freiheiten und eigene Nachbarn
                    if (x, y) != last_placed:
                        free, chain = freedoms(board, grid, x, y)   
                        
                        # Auswertung
                        if free <= 0 and spot != players[-turn]: # min: 0...
                        
                            for spot in chain:# + [(x, y)]: # Alle Steine der Kette loeschen                     
                                captured[board[spot[1]][spot[0]]] += 1    
                                board[spot[1]][spot[0]] = 0
                                
                                     
        # ...then remove potentially suicidal stones
        if last_placed:        
            if freedoms(board, grid, last_placed[0], last_placed[1])[0] <= 0:
              
                board[last_placed[1]][last_placed[0]] = 0
              
                last_placed = False
                turn_counter -= 1
                turn *= -1

            elif mpress:
                if len(stones[players[-turn]]) > 0 and placed_stone:
                        del stones[players[-turn]][-1]
     
        
        if mpress:   # save board frame in replay file when a stone got placed
            gamesave.capture(board)
##            replay.write(frame_cut) # includes "\n"
##            
##            for y, row in enumerate(board):
##                string = ""
##                
##                for x, spot in enumerate(row):    
##                    string += str(spot)
##
##                replay.write(string + "\n")
##
##            replay.close()
##            replay = open(replay_name, "a+")

        mpress = False
        


        # RENDERING - Start
        window.fill(bg)
        
        # draw cursor
        if 0 <= gx < grid and 0 <= gy < grid:
            pygame.draw.circle(window, (80, 50, 40), rund([(gx+1)*grid_size, (gy+1)*grid_size]), r(st_rad), line_width)
        
        # draw text
        box = [(grid+1)*grid_size, grid_size]
        rx, ry = box
        height = (grid-1)*grid_size
        
        
        text1 = text.render("Captured stones:", True, (0,0,0))
        #text2 = text.render("Am Zug:", True, (0,0,0))
        
        text_b = text.render(str(captured[2]), True, (0,0,0))
        text_w = text.render(str(captured[3]), True, (0,0,0))
        
        
        # draw Captured stones
        window.blit(text1, (rx, ry+0.025*height)) 
        
        pygame.draw.circle(window, colors[2], rund((1/2*grid_size + rx, ry+0.025*height+s+st_rad)), r(st_rad)) # +20 < 
        pygame.draw.circle(window, colors[3], rund((3/2*grid_size + rx, ry+0.025*height+s+st_rad)), r(st_rad)) # +20 < 3/4*grid_size
        window.blit(text_b, rund((1/2*grid_size + rx, ry+0.025*height+1.25*s+2*st_rad)))#+5/4*grid_size)))
        window.blit(text_w, rund((3/2*grid_size + rx, ry+0.025*height+1.25*s+2*st_rad)))#5/4*grid_size)))
        

        render_pit(window, (rx, ry + 1/3*height), 1/3*height-2, stones[2], [bg, black, black_edge, wood1, wood2], st_rad) # black
        render_pit(window, (rx, ry + 2/3*height), 1/3*height-2, stones[3], [bg, white, white_edge, wood1, wood2], st_rad) # white


        ############## Zeichnen des Spielbrettes ##############
        
        # lines of the board    
        for y in range(grid): 
            pygame.draw.line(window, clines, rund((grid_size, (y+1)*grid_size)), rund(( grid*grid_size, (y+1)*grid_size )), line_width)
        for x in range(grid): 
            pygame.draw.line(window, clines, rund(((x+1)*grid_size, grid_size)), rund(( (1+x)*grid_size, grid*grid_size )), line_width)


        gap = grid//7 +1 # from the edge
        gap = (gap * (gap >= 2)) or 2
        cords = []
        rad = 2*line_width; rad = rad * (rad >=5) or 5
        #if grid % 2 == 1: # odd
        #    if (grid-1-2*gap) >= 2*gap:
        #        cords = cords + [(0.5, 0), (0, 0.5), (1, 0.5), (0.5, 1)] # relative edge center points        
    
            #center = (grid//2 +1) * grid_size
            
        #    cords += [0.5, 0.5]
            #pygame.draw.circle(window, clines, rund((center, center)), r(line_width*2.5))

        
            
        if grid % 2 == 1:
            cords += [(0.5, 0.5)] # center point
            
            
            if (grid-1-2*gap) >= 2*gap: # corner points (when enought offset is granted)
                cords = cords + [(0.5, 0), (0, 0.5), (1, 0.5), (0.5, 1)] # edge center points

        if grid > 7: # add corner points
            cords += [(0, 0), (1, 0), (0, 1), (1, 1)]


        for i, j in cords: # draws 4 points in the corners of the board (with gap offset)
            dot_x = i*grid_size*(grid-1-2*gap) + (gap+1)*grid_size
            dot_y = j*grid_size*(grid-1-2*gap) + (gap+1)*grid_size
            
            pygame.draw.circle(window, clines, rund((dot_x, dot_y)), rad)

        
        # render Stones      
        for y, row in enumerate(board):
            for x, spot in enumerate(row):
                if spot != 0:
                    pygame.draw.circle(window, colors[spot], rund(((x+1)*grid_size, (y+1)*grid_size)), r(st_rad))
                    
                    

        
        
        pygame.display.update()
        clock.tick(fps)


# Quit game after window cross has been clicked

#replay.close()
gamesave.close()
pygame.quit()




########################################################################################################################

        # Ersetzt durch Schuesseln
        # window.blit(text2, (rx, (ry+0.1*height+s+2*st_rad) +0.1*height + grid_size)) # Who's turn
        # pygame.draw.circle(window, colors[players[turn]], rund((1/2*grid_size + rx, (ry+0.1*height+s+2*st_rad) + 0.1*height + grid_size +s+st_rad )), r(st_rad)) # 
        
        # pygame.draw.circle(window, wood1, (rx+grid_size, ry+0.55*height), 0.15*height) # schnitt bei 0.125*height == 
        # pygame.draw.circle(window, wood2, (rx+grid_size, ry+0.55*height), 0.15*height, 4)
        
        # pygame.draw.circle(window, wood1, (rx+grid_size, ry+0.85*height), 0.15*height)
        # pygame.draw.circle(window, wood2, (rx+grid_size, ry+0.85*height), 0.15*height, 4)



"""

p = 0
        mingap = 3
        
        if grid % 2 == 1:
            range_ = list(range(mingap, grid//2 + 1))
            range_.reverse()
            
            for c in range_:
                if (grid-1) % c == 0:
                    
                    p = c

        print(p)

        # render points
        if p != 0:
            for i in range(1, grid//p):
                for j in range(1, grid//p):
                    pygame.draw.circle(window, clines,
                                       rund(((1+ i*p) * grid_size,(1+ j*p) * grid_size)), line_width*2)
                



"""



"""

        # orientation points
##        mode = grid
##        pts = []
##        while mode % 2 == 1 and (mode // 2) > 1:
##            spot = mode // 2
##
##            pts.append([spot, spot])
##            pts.append([spot, grid-1-spot])
##            pts.append([grid-1-spot, spot])
##            pts.append([grid-1-spot, grid-1-spot])
##            
##            mode = mode // 2 +1
##
##        print(pts)
##        for p in pts:
##            pygame.draw.circle(window, (0,0,0), rund(((p[0]+1) * grid_size, (p[1]+1)*grid_size)), 10)
        

"""




