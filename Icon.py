import pygame

class Icon(pygame.sprite.DirtySprite):
    
    def __init__(self, coord, event_code, up_image, down_image):
        """
        Creates a new Icon object with the attributes:
            coord(list[int])  --> (x,y) top left corner of the icon
            event_code(?)     --> Event code that will be sent to the event que
                                      when icon is clicked. The Event will then
                                      have this property at (event1.code)
            up_image(str)     --> relative file path for the image of the unclicked icon
            down_image(str)   --> relative fiel path fot the image of the clicked icon
        """
        pygame.sprite.Sprite.__init__(self)
        self.event = pygame.event.Event(pygame.USEREVENT, {"code": event_code})
        self.IMAGES = [pygame.image.load(up_image), pygame.image.load(down_image)]
        self.image = self.IMAGES[0]
        
        self.rect = self.image.get_rect()
        self.rect.top = coord[1]
        self.rect.left = coord[0]
        
        self.clicked = False
        self.dirty = 1
        
    def change_state(self, clicked):
        """
        --> None
        Changes image number (does not change image, that is done in update)
        Posts the event unto the event que
            clicked(bool) --> True: icon was just clicked       
        """
        self.dirty = 1
        if clicked:
            self.clicked = True
            pygame.event.post( self.event )
        else:
            self.clicked = False
        self.image = self.IMAGES[int(self.clicked)]
    
    def update(self):
        """
        Method to control sprite behavior, an Icon will do the following:
            Check if it is being clicked at the moment OR if mouse button was released after it was clicked
            Calls Icon.change_state() method
            Changes Icon Image
        
        This method is called by Group.update()
        """
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint( pygame.mouse.get_pos() ) and not self.clicked:
            self.change_state(1)
        elif self.clicked and not pygame.mouse.get_pressed()[0]:
            self.change_state(0)
        
class Pause_Play(Icon):
    
    def __init__(self, coord, play_event, pause_event, play_up, play_down, pause_up, pause_down):
        """
        icon1 = Pause_Play(...)
        Creates a new Icon object with the attributes:
            coord(list[int])  --> (x,y) top left corner of the icon
            play_event(?)     --> Event code that will be sent to the event que
                                      when icon is clicked. The Event will then
                                      have this property at (event1.code)
            pause_event(?)    --> Same as play_event, but for pausing
            play_up(str)      --> relative file path for the image of the unclicked play icon
            play_down(str)    --> relative fiel path fot the image of the clicked play icon
            pause_up(str)     --> relative file path for the image of the unclicked pause icon
            pause_down(str)   --> relative fiel path fot the image of the clicked pause icon
        """
        Icon.__init__(self, coord, pause_event, pause_up, pause_down)
        self.PAUSE_IMAGES = [pygame.image.load(pause_up), pygame.image.load(pause_down)]
        self.PLAY_IMAGES = [pygame.image.load(play_up), pygame.image.load(play_down)]
        self.pause_event = pygame.event.Event(pygame.USEREVENT, {"code": pause_event})
        self.play_event = pygame.event.Event(pygame.USEREVENT, {"code": play_event})
        
        self.paused = False
        
    def pause(self):
        """
        --> None
        Changes the state of the icon to paused (does not change image, that is done in update)
        Posts the event unto the event que
        """
        self.paused = True
        self.IMAGES = self.PLAY_IMAGES
        self.event = self.pause_event
        Icon.change_state(self, 1)
        
    def play(self):
        """
        --> None
        Changes the state of the icon to playing (does not change image, that is done in update)
        Posts the event unto the event que
        """
        self.paused = False
        self.IMAGES = self.PAUSE_IMAGES
        self.event = self.play_event
        Icon.change_state(self, 1)
        
    def change_state(self, clicked):
        """
        --> None
        Changes image number (does not change image, that is done in update)
        Posts the event unto the event que
        Calls either Pause_Play.play() or Pause_Play.Pause() method
            clicked(bool) --> True: icon was just clicked       
        """
        if clicked:
            if self.paused:
                self.play()
            else:
                self.pause()
        else:
            Icon.change_state(self, 0)
        