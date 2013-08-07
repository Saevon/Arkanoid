import pygame.cursors
# . is black, X is white " " is transparent
#24 * 24 cursor image
cursor = ( 
"           X            ",
"          X.X           ",
"         X...X          ",
"        X.X.X.X         ",
"       X.XX.XX.X        ",
"      X.X X.X X.X       ",
"     X.X  X.X  X.X      ",
"    X.X   X.X   X.X     ",
"   X.X    XXX    X.X    ",
"  X.X             X.X   ",
" X.XXXXX  XXX  XXXXX.X  ",
"X......X  X.X  X......X ",
" X.XXXXX  XXX  XXXXX.X  ",
"  X.X             X.X   ",
"   X.X    XXX    X.X    ",
"    X.X   X.X   X.X     ",
"     X.X  X.X  X.X      ",
"      X.X X.X X.X       ",
"       X.XX.XX.X        ",
"        X.X.X.X         ",
"         X...X          ",
"          X.X           ",
"           X            ",
"                        ")
#creates this cursor
temp = pygame.cursors.compile(cursor)
#adds dimensions used for the pygame.mouse.set_cursor() method
CURSOR = [(24,24)]
#adds the hotspot area
CURSOR.append((12,12))
#adds the two parts given by the compiled cursor (image)
for item in temp:
    CURSOR.append(item)