import pygame
class Border(pygame.sprite.Sprite):
    """
    A class which models a Border, with a location, and Surface
    Note the top left corner pixel becomes the transparent color
    """
    def __init__(self, coord, image):
        """
        Creates a new Border object, transparent color is taken at pixel (0,0)
            coord(list)    --> (x,y) top left corner
            image(Surface) --> The Surface for that will be displayed
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at( (0,0) ) )
        
        self.rect = self.image.get_rect()
        self.rect.top = coord[1]
        self.rect.left = coord[0]