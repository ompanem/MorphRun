from game_platform import Platform
from enemy import Enemy
from form import Form
#colors
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
ORANGE = (255,165,0)   
YELLOW = (255,255,0)
def load_level(file_path: str):
    platforms = []
    enemies = []
    player_x = 0
    player_y = 0
    file = open(file_path)
    lines = file.readlines()
    file.close()

    for row, line in enumerate(lines):
        start_f = -1
        start_o = -1
        for col, char in enumerate(line):
            #40 is the multiplier bc its a 20x15 txt
            x = col*40 
            y = row*40

            match(char):
                #Player
                case 'P':
                    player_x = x
                    player_y = y
                #Breakable Block
                case 'O':
                     if(start_f!=-1):
                        width = (col-start_f)*40
                        platforms.append(Platform(start_f*40, y, width, 40, GREEN, False))
                        start_f = -1
                     if(start_o == -1):
                        start_o = col
                #Floor
                case 'F':
                    if(start_o!=-1):
                        width = (col-start_o)*40
                        platforms.append(Platform(start_o*40, y, width, 40, ORANGE, True))
                        start_o = -1
                    if(start_f == -1):
                        start_f = col
                case 'W':
                    if(start_f!=-1):
                        width = (col-start_f)*40
                        platforms.append(Platform(start_f*40, y, width, 40, GREEN, False))
                        start_f = -1
                    if(start_o!=-1):
                        width = (col-start_o)*40
                        platforms.append(Platform(start_o*40, y, width, 40, ORANGE, True))
                        start_o = -1
                    
                    platform = Platform(x,y,40,40,YELLOW, False)
                    platform.goal = True
                    platforms.append(platform)
                    platforms[-1].goal = True
                #If its divided by empty space aka (.) then stop the floor there
                case _:
                    if(start_f!=-1):
                        width = (col-start_f)*40
                        platforms.append(Platform(start_f*40, y, width, 40, GREEN, False))
                        start_f = -1
                    
                    if(start_o!=-1):
                        width = (col-start_o)*40
                        platforms.append(Platform(start_o*40, y, width, 40, ORANGE, True))
                        start_o = -1
                
        
        #check for when F takes up the whole floor
        if(start_f!=-1):
            width = (len(line.strip())-start_f)*40
            platforms.append(Platform(start_f*40,y, width, 40, GREEN, False))
        if(start_o!=-1):
            width = (len(line.strip())-start_o)*40
            platforms.append(Platform(start_o*40, y, width, 40, ORANGE, True))
        
        start_f = -1
        start_o = -1

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            x = col*40
            y = row*40
            match(char):
                case 'B':
                    for p in platforms:

                        if(p.x<=x and x< p.x + p.width and p.y == y+40):
                            enemies.append(Enemy(x, Form.BRUTE, p))
                            break
                case 'S':
                    for p in platforms:
                        if(p.x<=x and x< p.x + p.width and p.y == y+40):
                            enemies.append(Enemy(x,Form.SHRINKER, p))
                            break

    return platforms, enemies, player_x, player_y
                   


