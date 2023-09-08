import pygame, math


pygame.init()


def rund(pos):
    return [int(round(i)) for i in pos]

def r(i):
    return int(round(i))


# game replay and save
class save:
    def __init__(self, name=""): # Create / Read Savegame file

        self.cut = "---\n"
        
        if name != "":

            self.name = inp
            self.file = open(inp, "a+")

            #self.content = file.readlines()
            #file.close()

        else:
            
            #self.content = name
            self.name = "last_replay.txt"
            self.file = open(self.name, "w")
            
        
    def capture(self, board):

        self.file.write(self.cut) # includes "\n"
            
        for y, row in enumerate(board):
            string = ""
                
            for x, spot in enumerate(row):    
                string += str(spot)

            self.file.write(string + "\n")

        self.file.close()
        self.file = open(self.name, "a+")
            

    def close(self):
        self.file.close()




# game logic

def freedoms(board, grid, x, y, old = []):
    free = 0
    stones = [(x, y)]
    spot = board[y][x]
    
    for vx, vy in ((0, -1), (1, 0), (0, 1), (-1, 0)): # vier durchlaeufe
        cx, cy = (x+vx, y+vy) # compare
        
        if 0 <= cx <= (grid-1) and 0 <= cy <= (grid-1):
            comp = board[cy][cx]
            
            if comp == 0: # Freiheit
                 free += 1
                
            elif comp == spot: # gleicher Stein
                if not (cx, cy) in old:
                                          
                    f, stone = freedoms(board, grid, cx, cy, (old + [(x, y)]))
                    free += f
                    stones += stone

    
    # print((x, y), free, stones)
    
    return free, stones


def render_pit(surface, position, size, stones, colors, st_rad): # colors == [background, stone, stone_edge, pit, pit_edge]
    x, y = position
    
    #surface.fill(colors[0])
    pygame.draw.circle(surface, colors[3], rund((x+ 0.5*size, y+ 0.5*size)), r(0.5*size)) # schnitt bei 0.125*height == 


    # render stones
    for s in stones: # Black (upper pit) # b = [len, angle] # 0 << 1
        stone_x = x + 0.5*size + math.cos(math.radians(s[1]*360)) * ((s[0] * 0.5*size)-st_rad)
        stone_y = y + 0.5*size + math.sin(math.radians(s[1]*360)) * ((s[0] * 0.5*size)-st_rad)
        #stone_x = size * b[0]
        #stone_y = size * b[1]
        pygame.draw.circle(surface, colors[1], rund((stone_x, stone_y)), st_rad) # draw stone into the pit
        pygame.draw.circle(surface, colors[2], rund((stone_x, stone_y)), st_rad, 2)
        


    # draw edges of the pit        
    pygame.draw.circle(surface, colors[4], rund((x+ 0.5*size, y+ 0.5*size)), r(0.5*size), r(0.05*size)) # schnitt bei 0.125*height == 
    

##
##def anim_update(anims, speed=1):
##    dellist = []
##
##    for i, anim in enumerate(anims): # anim == [(r,g,b), startpos, endpos, counter] # counter: 0 -> 100
##
##        if anim[3] >= 100:
##            dellist.append(i)
##        else:
##            anim[3] += speed
##
##    dellist.reverse()
##
##    for d in dellist:
##        del anims[d]
##
##    dellist.reverse()
##    return dellist
##        
##
##def anim_render(window, anims, circle_rad):
##
##    for anim in anims:
##        #pos = anim[1]
##
##        # absolute vector
##        dx = anim[2][0] - anim[1][0]
##        dy = anim[2][1] - anim[1][1]
##
##        x = anim[3] / 100
##        f = math.sin(math.pi * (x - 0.5)) / 2 + 0.5
##        pos = [anim[1][0] + f * dx , anim[1][1] + f * dy ]
##        
##        pygame.draw.circle(window, anim[0], rund(pos), circle_rad)
##    






