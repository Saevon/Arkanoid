import pygame

class Pop_Up_Window(pygame.sprite.DirtySprite):
    """
    A pop-up window which displays a message, (with optional Cancel Button)
    which can be moved around
    """
    
    def __init__(self, coord, title = "", body_text = "", icon = None, has_cancel_button = False, cancel_event = None, ok_event = None):
        """
        Creates a Pop_Up_Window object with the following properties,
            coord(tuple)            --> (x,y) the top left corner of the window
            title(str)              --> The Text on the title bar of the window, there must be no
                                        newline character in the string              (PRESET: Nothing)
            body_text(str)          --> The text that is shown in the body window, there can be
                                        newline characters in the string             (PRESET: Nothing)
            icon(Surface)           --> The surface to be used as an icon beside the body_text its size
                                        should be (48 pixels by 48 pixels)           (PRESET: No Icon)
            has_cancel_button(bool) --> Whether the window will have a cancel button (PRESET: False)
            cancel_event(Event)     --> Event that will be sent when the the window is closed,
                                        or the cancel button is clicked              (PRESET: pygame.event.Event(pygame.USEREVENT, {"WINDOW": title, "ACTION": "CLOSED"} )
            cancel_event(Event)     --> Event sent whent the Ok button is clicked    (PRESET: pygame.event.Event(pygame.USEREVENT, {"WINDOW": title, "ACTION": "OK"} )
                                                              
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        
        #events
        if cancel_event:
            self.cancel_event = cancel_event
        else:
            self.cancel_event = pygame.event.Event(pygame.USEREVENT, {"WINDOW": title, "ACTION": "CLOSED"} )
        if ok_event:
            self.ok_event = ok_event
        else:
            self.ok_event = pygame.event.Event(pygame.USEREVENT, {"WINDOW": title, "ACTION": "OK"} )
        
        has_cancel_button
        if icon:
            self.icon = icon
        else:
            self.icon = pygame.Surface((28,28))
            self.icon.fill( (233,233,215) )
            
        self.body_font = pygame.font.Font("Pop-Up/cour.ttf", 10)
        self.title_font = pygame.font.Font("Pop-Up/cour.ttf", 13)
        self.title_font.set_bold(True)
        
        self.body = []
        self.body_width = 0
        for line in body_text.split("\n"):
            temp = self.body_font.render(line, True, [0,0,0]).convert_alpha()
            self.body.append(temp)
            if temp.get_width() > self.body_width:
                self.body_width = temp.get_width()
            
        self.title = self.title_font.render(title, True, [255,255,255]).convert_alpha()
        self.body_height = len(self.body) * self.body[0].get_height()
            
        self.size =[226, 114]
        if self.body_width > 129:
            self.size[0] = self.body_width + 97
        if self.body_height > 30:
            self.size[1] = self.body_height + 84
        if self.size[0] - (self.title.get_width() + 58) <  0:
            self.size[0] = self.title.get_width() + 58
            
        self.image = pygame.Surface(self.size)
        self.image.fill( (233,233,215) )
        
        #borders
        #top left
        self.image.blit( pygame.image.load("Pop-Up/Border ~ Top Left.gif"), (0,0) )
        #top line
        for x in range(6, self.size[0], 10):
            self.image.blit( pygame.image.load("Pop-Up/Border ~ Top.gif"), (x,0) )
        #top right
        self.image.blit( pygame.image.load("Pop-Up/Border ~ Top Right.gif"), (self.size[0] - 28,0) )
        #Left
        for y in range(29, self.size[1], 10):
            self.image.blit( pygame.image.load("Pop-Up/Border ~ Side.gif"), (0,y) )
        #Right
        for y in range(29, self.size[1], 10):
            self.image.blit( pygame.image.load("Pop-Up/Border ~ Side.gif"), (self.size[0] - 3,y) )
        #Bottom
        for x in range(0, self.size[0], 10):
            self.image.blit( pygame.image.load("Pop-Up/Border ~ Bottom.gif"), (x,self.size[1] - 3) )
        
        #icon
        self.image.blit(self.icon, (12,30))
        #Ok button
        temp = pygame.image.load("Pop-Up/Button ~ Ok.gif")
        temp.set_colorkey( temp.get_at( (0,0) ) )
        self.image.blit( temp, (18, self.size[1] - 34))
        if has_cancel_button:
            #Cancel button
            temp = pygame.image.load("Pop-Up/Button ~ Cancel.gif")
            temp.set_colorkey( temp.get_at( (0,0) ) )
            self.image.blit( temp, (105, self.size[1] - 34))
            self.cancel_rect = pygame.Rect(105 + coord[0], self.size[1] - 34 + coord[1], 80, 23)
        else:
            self.cancel_rect = pygame.Rect(-500,-500,0,0)
            
        self.image.blit( self.title, (10, 8) )
        for item in range(len(self.body)):
            self.image.blit( self.body[item], (65, 40 + (item * self.body[item].get_height())) )
            
        self.image.set_colorkey( self.image.get_at( (0,0) ) )
            
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        
        self.close_rect = pygame.Rect(self.size[0] - 26 + coord[0], 6 + coord[1], 20, 20)
        self.ok_rect = pygame.Rect(18 + coord[0], self.size[1] - 34 + coord[1], 80, 23)
        self.title_bar_rect = pygame.Rect(coord[0], coord[1], self.size[0], 29)
        
        self.attached = False
        self.attached_pos = (0,0)
        
    def mouse_click(self, pos):
        """
        --> None
        Call only if there is a MOUSEBUTTONDOWN event (preferably only left button)
        This method must be called for the Window to send events
        Checks if the close button, Ok, or Cancel buttons are pressed and if they are posts an appropriate event and
            kills itself
        """
        if self.close_rect.collidepoint( pos ):
            pygame.event.post( self.cancel_event )
            self.kill()
        elif self.cancel_rect.collidepoint( pos ):
            pygame.event.post( self.cancel_event )
            self.kill()
        elif self.ok_rect.collidepoint( pos ):
            pygame.event.post( self.ok_event )
            self.kill()
        elif self.title_bar_rect.collidepoint( pos ):
            self.attached = True
            self.attached_pos = pos
            
    def mouse_unclick(self):
        """
        --> None
        Call only if there is a MOUSEBUTTONUP event (preferably only left button)
        This method must be called for the Window to stop being attached to the mouse
        """
        self.attached = False
            
    def mouse_motion(self, pos):
        """
        --> None
        Call only if there is a MOUSEMOTION event, This method must be called for the Window to move around
        Will move around the window while the window is attached
        """
        if self.attached:
            movement = [pos[0] - self.attached_pos[0], pos[1] - self.attached_pos[1]]
            self.attached_pos = pos
            self.move(movement)
            
    def move(self, distance):
        """
        --> None
        Moves the window
            distance(tuple) --> (x,y) the distance to move the window by
        """
        if self.close_rect.top != -500:
            self.close_rect.left += distance[0]
            self.close_rect.top += distance[1]
        self.ok_rect.left += distance[0]
        self.ok_rect.top += distance[1]
        self.cancel_rect.left += distance[0]
        self.cancel_rect.top += distance[1]
        self.title_bar_rect.left += distance[0]
        self.title_bar_rect.top += distance[1]
        self.rect.left += distance[0]
        self.rect.top += distance[1]
        
    
if __name__ == "__main__":
    
    size = (600, 480)
    screen = pygame.display.set_mode(size)
    pygame.mixer.init(22500, -16, 2, 512)
    pygame.init()
    
    
    pygame.mouse.set_pos([535,65])
    
    group = pygame.sprite.Group()
    #temp = pygame.image.load("Pop-Up/Pop-Up Icons ~ CD.gif")
    #temp.set_colorkey( temp.get_at( (0,0) ) )
    
    
    group.add( Pop_Up_Window((20,20), title = "Try this out", body_text = """:
This is a Test of the body
I wonder if it will Work
lala


Hey this is cool
WOOWOWOWOWOOWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
long line there ehh
""", icon = None, has_cancel_button = True))

    group.add( Pop_Up_Window((20,20), title = "File Deletion", body_text = """Are you sure you wish to delete this file""", has_cancel_button = True))
    
    framerate = 45
    keep_going = True
    clock = pygame.time.Clock()
    background = pygame.Surface(size)
    background.fill( [255,255,255] )
    screen.blit(background, (0,0))
    
    while keep_going:

        # Timer
        clock.tick(framerate)

        #event Handling
        for ev in pygame.event.get():
            #events which happend regardless of paused state
            if ev.type == pygame.QUIT:
                keep_going = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for item in group:
                        item.mouse_click(ev.pos)
            elif ev.type == pygame.MOUSEBUTTONUP:
                for item in group:
                    item.mouse_unclick()
            elif ev.type == pygame.MOUSEMOTION:
                for item in group:
                    item.mouse_motion(ev.pos)
            elif ev.type == pygame.USEREVENT:
                print ev
                
        group.clear(screen, background)
        group.draw(screen)
        pygame.display.flip()
    