import pygame

class Portal(pygame.sprite.Sprite):
    """
    A class which models a portal
    """
    
    IMAGES = []
    for i in range(1,4):
        temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Portal ~ Open - %i.gif" % (i))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        IMAGES.append(temp)
        
    OPEN_IMAGES = []
    for i in range(1,13):
        temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Portal - %i.gif" % (i))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        OPEN_IMAGES.append(temp)
    
    def __init__(self, coord, framerate = 45):
        """
        Creates a Portal
            coord(list)    --> (x,y) bottom right of the puff
            framerate(int) --> The framerate(for calculations on how long to do
                                             apppearance animation)
            
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = Portal.IMAGES[0]
        self.rect = self.image.get_rect()
        
        self.rect.right = coord[0]
        self.rect.bottom = coord[1]
        self.countdown = 0
        self.state = 0

        self.framerate = framerate   
    
    def isopen(self):
        """
        --> bool
        Returns True if the Portal has finished the opening animation
        """
        return self.countdown >= 3 * self.framerate
    
    def reset(self):
        """
        --> None
        Resets the counter of the Portal, portal will open again
        """
        self.countdown = 0
        self.state = 0
        
    def update(self):
        """
        Method to control sprite behavior, a Portal will do the following:
            Change its image
            
        This method is called by Group.update()
        """
        self.countdown += 1
        if self.state >= 1:
            if self.countdown % (self.framerate / 10) == 0:
                self.state += 1
            if self.state > len(Portal.OPEN_IMAGES):
                self.state = 1
            self.image = Portal.OPEN_IMAGES[self.state - 1]
        else:
            if self.isopen():
                self.image = Portal.IMAGES[2]
                self.state = 1
            elif self.countdown >= 1.5 * self.framerate:
                self.image = Portal.IMAGES[1]
            else:
                self.image = Portal.IMAGES[0]