import pygame
class Puff(pygame.sprite.Sprite):
    """
    A class which acts as temporary image, it has a life, and Surface as well as a location
    The class can be given an alpha value, which can be made to change at a specified rate
    The object will automatically kill itself after its life runs out
    """

    #standard smoke puff image
    IMAGE = pygame.image.load("images/Sprites/Paddles & Ammunition/Smoke Puff.gif")
    IMAGE.set_colorkey( IMAGE.get_at( (0,0) ) )

    def __init__(self, coord, life = 60, alpha = None, alpha_decrease = None, image = None):
        """
        Creates a puff of smoke
            coord(list)    --> (x,y) center point of the puff
            life(int)      --> frames before dissapearing (PRESET: 60 frames)(-1 = infinite)
            alpha(int)     --> Alpha value of the surface (PRESET: fully opaque)
            alpha_decrease --> Alpha decrease per frame   (PRESET: No decrease)
            image(Surface) --> Image to be used           (PRESET standard puff)
        """
        pygame.sprite.Sprite.__init__(self)
        if image:
            self.image = image
        else:
            self.image = Puff.IMAGE.copy()
        self.rect = self.image.get_rect()

        if alpha:
            self.image.set_alpha(int(alpha))
        else:
            self.image.set_alpha(255)

        self.rect.centerx = coord[0]
        self.rect.centery = coord[1]

        self.countdown = life

        self.dec = alpha_decrease

    def update(self):
        """
        Method to control sprite behavior, a Puff will do the following:
            Decrease life by one
            Change alpha if alpha_decrease was given during intitialization
            Run the Sprite method kill() if life runs out

        This method is called by Group.update()
        """
        self.countdown -= 1
        if self.countdown == 0:
            self.kill()
        if self.dec:
            temp = self.image.get_alpha() - self.dec
            if temp <= 0:
                temp = 0
            self.image.set_alpha(temp)
