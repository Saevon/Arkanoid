import pygame
from random import randint

class Text(pygame.sprite.DirtySprite):
    """
    A class which models a Text sprite, used as a base class for text objects
    """
    
    def __init__(self, coord, message, font, size = 10, rgb = [255,255,255], colorkey = False):
        """
        Creates a Text object,
            coord(list)    --> (x,y) the top left corner of the Text object
            message(str)   --> The message that will be displayed
            font(Font)     --> loaded pygame font that will be used
            size(int)      --> font size                                 (PRESET: 10 point)
            rgb(list)      --> [R,G,B] the color of the text in RGB form (PRESET: Pure White)
            colorkey(bool) --> True: sets colorkey at (0,0)              (PRESET: False)
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.message = message
        self.font = pygame.font.Font(font, size)
        self.rgb = rgb
        
        self.image = self.font.render(self.message, True, self.rgb).convert_alpha()
        self.colorkey = colorkey
        if self.colorkey:
            self.image.set_colorkey( self.image.get_at((0,0)) ) 
        self.rect = self.image.get_rect()
        
        self.coord = coord
        self.rect.left = self.coord[0]
        self.rect.top = self.coord[1]
	self.dirty = 2
        
    def update(self):
        """
        Text.update() --> None
        Method to control sprite behavior, a Text object will do the following:
            Re-render the image
        
        This method is called by Group.update()
        """
        self.image = self.font.render(self.message, True, self.rgb).convert_alpha()
        if self.colorkey:
            self.image.set_colorkey( self.image.get_at((0,0)) ) 
        
        self.rect = self.image.get_rect()
        self.rect.left = self.coord[0]
        self.rect.top = self.coord[1]
        
################################################################################      
class Ammo(Text):
    """
    An object which models an ammunition counter
    """
    
    def __init__(self, coord, font, padding = 3, size = 10, rgb = [255,255,255]):
        """
        Creates a Ammo object, with a munition count of 0
            coord(list)  --> (x,y) the top left corner of the Text object
            font(Font)   --> loaded pygame font that will be used
            padding(int) --> Number of digits shown, with commas       (PRESET: 3 Digits)
            size(int)    --> font size                                 (PRESET: 10 point)
            rgb(list)    --> [R,G,B] the color of the text in RGB form (PRESET: Pure White)
        """
        Text.__init__(self, coord, "", font, size, rgb)
        
        self.amount = 0
        self.padding = padding
        
        self.pad_ammo()
        self.dirty = 1
        
    def ammunition(self):
        """
        --> int
        Returns the amount of ammo there is
        """
        return self.amount

    def pad_ammo(self):
        """
        --> str
        Changes the message on the image padding it with zeros
        Returns the padded message
        """
        self.message = "0" * (self.padding - len(str(self.amount))) + str(self.amount)
        if len(self.message) > self.padding:
            self.message = "9" * self.padding

        return self.message
    
    def use_ammo(self):
        """
        --> bool
        Returns True if there is ammo to use
        Also decreases the ammo count
        """
        if self.amount > 0:
            self.amount -= 1
            self.dirty = 1
            return True
        return False
        
    def add_ammo(self, num):
        """
        --> None
        Increases ammo count
            num(int) --> Increase of ammo count
        """
        self.amount += num
        self.dirty = 1
    
    def update(self):
        """
        Method to control sprite behavior, an Ammo object does the following:
            Calls the self.pad_ammo() method
            Calls the Text.update() method
            
        This method is called by Group.update()
        """
        self.pad_ammo()
        Text.update(self)
        
################################################################################        
class Score(Text):
    """
    A class which models a score board
    Maintains a value and adds on to it, Can only be used with a Combo object
    """
    
    def __init__(self, coord, font, padding = 7, size = 10, rgb = [255,255,255]):
        """
        Creates a Score object, with a score of 0
            coord(list)  --> (x,y) the top left corner of the Text object
            font(Font)   --> loaded pygame font that will be used
            padding(int) --> Number of digits shown, with commas       (PRESET: 7 Digits)
            size(int)    --> font size                                 (PRESET: 10 point)
            rgb(list)    --> [R,G,B] the color of the text in RGB form (PRESET: Pure White)
        """
        Text.__init__(self, coord, "", font, size, rgb)
        
        self.score = 0
        self.padding = padding
        
        self.pad_score()
        self.dirty = 1
        
        
    def allow_combos(self, coord):
        """
        --> Combo
        Must be done before using a Score object,
        Creates and Returns a Combo object
        """
        self.combo = Combo(coord)
        return self.combo
        
    def pad_score(self):
        """
        --> str
        Changes the message on the image to the newest score, padded with zeros
            and with commas every three digits
        Returns the message
        """
        self.score = int(self.score)
        temp = list("0" * (self.padding - len(str(self.score))) + str(self.score))
        if len(temp) > self.padding:
            temp = list("9" * self.padding)
        temp.reverse()
        self.message = ""
        self.counter = 0
        for char in temp:
            if self.counter == 3:
                self.counter = 0
                self.message = "," + self.message
            self.message = char + self.message
            self.counter += 1
        return self.message

    def add_score(self, num):
        """
        --> None
        Increases the score (adding on the multiplier from the Combo object)
        Adds 1 combo to the combo object
        """
        self.dirty = 1
        self.score += self.combo.multiplier(num)
        self.combo.add()
        
    def update(self):
        """
        Method to control sprite behavior, a Score object will do the following:
            Calls the self.pad_score() method
            Calls the Text.update() method
        
        This method is called by Group.update()
        """
        self.pad_score()
        Text.update(self)
        
################################################################################
class Combo_Counter(Text):
    """
    A class which models a combo counter
    Can only be used with a Combo object
    """
    
    def __init__(self, coord, font, padding = 2, size = 10, rgb = [255,255,255]):
        """
        Creates a Combo_Counter object, with a combo count of 0
            coord(list)  --> (x,y) the top left corner of the Text object
            font(Font)   --> loaded pygame font that will be used
            padding(int) --> Number of digits shown, with commas       (PRESET: 2 Digits)
            size(int)    --> font size                                 (PRESET: 10 point)
            rgb(list)    --> [R,G,B] the color of the text in RGB form (PRESET: Pure White)
        """
        Text.__init__(self, coord, 0, font, size, rgb)
        self.size = size
        self.flash = 0
        self.padding = padding
        
        self.fonts = []
        for x in range(11):
            self.fonts.append( pygame.font.Font(font, size + x) )
            
        self.pad_combo()
        self.dirty = 1
        
    def __add__(self, other):
        """
        self + other
        --> Combo_Counter
        Adds a Combo_Counter with an int or a float, increasing the combo count
        Starts Text 'Flash' aka. the text grows big and red then shrinks back to normal
        """
        self.message = int(self.message) + other
        self.flash = 5
        self.dirty = 2
        return self
    
    def __le__(self, other):
        """
        self <= other
        --> bool
        Returns True if the combo count is less than or equal to other(int, float)
        """
        return int(self.message) <= other
    
    def __gt__(self, other):
        """
        self > other
        --> bool
        Returns True if the combo count is greater than other(int, float)
        """
        return int(self.message) > other
        
    def pad_combo(self):
        """
        --> str
        Changes the message on the image, padded with zeros
        Returns the padded message
        """
        self.message = "0" * (self.padding - len(str(self.message))) + str(self.message)
        if len(self.message) > self.padding:
            self.message = "9" * self.padding

        return self.message
        
    def reset(self):
        """
        --> None
        Resets the combo counter to 0, and resets font style
        """
        self.message = 0
        self.flash = 0
        self.dirty = 1

        
    def update(self):
        """
        Method to control sprite behavior, a Combo_counter object does the following:
            Calls the self.pad_combo() method
            Calls the Text.update() method
            Reduces 'Flash'
            Changes Font based on 'Flash'
            
        This method is called by Group.update()
        """
        self.pad_combo()
        if self.flash < 0:
            self.flash = 0
            self.dirty = 1
        self.font = self.fonts[self.flash]
        self.rgb = [255,(9 - self.flash) * 25 + 30,(9 - self.flash) * 25 + 30]
        Text.update(self)
        
        self.rect.centery = self.coord[1]
        
################################################################################        
class Combo(pygame.sprite.DirtySprite):
    """
    An object which models a combo timer which resets every 5/3 of a second
    Must be used with a Combo_Counter object
    """
    
    IMAGES = []
    for i in range(0,10):
        temp = pygame.image.load("images/Sprites/Icons/Combo - %i.gif" % (i))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        IMAGES.append(temp)
        
    def __init__(self, coord, framerate = 45):
        """
        Creates a Combo object
            coord(list)    --> (x,y) the top left coorinate of the object
            framerate(int) --> The framerate(for calculations on how long combos last)
        """
        pygame.sprite.DirtySprite.__init__(self)
        
        self.image = self.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.top = coord[1]
        self.rect.left = coord[0]

        self.counter = 0
        self.rate = framerate / 6
        self.dirty = 1
        
    def add(self):
        """
        --> None
        Increases Combo by 1, and restarts combo timer
        """
        self.combos += 1
        self.counter = self.rate * 10
        self.dirty = 2
        
    def reset(self):
        """
        --> None
        Resets the Combo timer and Combo num
        """
        self.counter = 0
        self.combos.reset()
        self.dirty = 1
        
    def multiplier(self, score):
        """
        --> float
        Returns the new score, based on combo num (if score is zero, zero is returned)
            MULTIPLIERS:
                x2  - x4  --> + 250
                x5  - x9  --> x 1.5
                x10 - x24 --> x 2
                x25 - x49 --> x 4
                x50 - x99 --> x4  + (500 or more)
            score(float, int) --> score to modify
        """
	if score != 0:
	    if self.combos <= 2:
		return score
	    elif self.combos <= 4:
		return score + 250
	    elif self.combos <= 9:
		return int(score * 1.5)
	    elif self.combos <= 24:
		return score * 2
	    elif self.combos <= 49:
		return score * 4
	    return score * 4 + randint(500, 1500)
	return 0
        
    def allow_combo_counter(self, coord, font, padding = 2, size = 10, rgb = [255,255,255]):
        """
        --> Combo_Counter
        Must be done before using a Combo object,
        Creates and Returns a Combo_Counter object
        """
        self.combos = Combo_Counter(coord, font, padding, size, rgb)
        return self.combos
        
    def update(self):
        """
        Method to control sprite behavior, a Combo Object does the following:
            Counts timer
            Resets combo num if time runs out
            Changes Image
            
        This method is called by Group.update()
        """
        self.counter -= 1
        if self.counter <= 0:
            self.counter = 0
        elif int(self.counter / self.rate) == 1:
            self.combos.reset()

        self.image = Combo.IMAGES[ int(self.counter / self.rate) ]
        self.combos.flash = self.counter - self.rate * 10 + 10
        