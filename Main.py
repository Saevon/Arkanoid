################################################################################
#Import & Initialize
################################################################################
import pygame
import random
from Border import Border
from Vector import Vector
from math import radians
from math import degrees
from Puff import *
from Portal import *
from Text import *
from cursor import CURSOR
from Icon import Icon
from Icon import Pause_Play
import SaveLoad
from Line import Barrier_Lines
from LineSegment import Line_Segment
import os.path
pygame.mixer.init(22500, -16, 2, 512)
pygame.init()

#Display set-up
################################################################################
size = (600, 480)
screen = pygame.display.set_mode(size)
icon = pygame.image.load("images/icon.gif")
pygame.display.set_icon(icon)
pygame.display.set_caption("~Arkanoid")
pygame.mouse.set_cursor(CURSOR[0], CURSOR[1], CURSOR[2], CURSOR[3])
pygame.mouse.set_pos([535,65])

################################################################################

#Classes
################################################################################
class Upgrade(pygame.sprite.Sprite):
    """
    A class which models a falling arkanoid upgrade
    """

    COLORS = "BGORYZ"
    IMAGES = []
    for color in COLORS:
        for num in range(1,4):
            temp = pygame.image.load(os.path.join("images", "Sprites", "Bonus", "Bonus ~ %s - %i.gif" % (color, num)))
            temp.set_colorkey( temp.get_at( (0,0) ) )
            IMAGES.append( temp )

    UP_IMAGES = []
    for num in range(1,8):
        temp = pygame.image.load(os.path.join("images", "Sprites", "Bonus", "Bonus ~ 1UP - %i.gif" % (num)))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        UP_IMAGES.append( temp )

    PATTERN = [3,2,2,1,1,1,0,0,0,0,-1,-1,-1,-2,-2,-3,-1,-1,-1,0,0,0,0,1,1,1,2,2]

    def __init__(self, coord, color):
        """
        Creates a Upgrade object
            coord(list) --> (x,y) the center point of the Upgrade
            color(str)  --> the color of the object from the below list (PRESET: Random)
                B --> Blue: multiball
                G --> Green:rocket
                O --> Orange:fireball
                R --> Red:laser
                Y --> Yellow:bigger paddle
                Z --> Black:small paddle & ball speed change
                1 --> 1UP
        """
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        if self.color == "1":
            self.image = Upgrade.UP_IMAGES[0]
        else:
            self.image = Upgrade.IMAGES[3 * Upgrade.COLORS.find(self.color)  ]

        self.rect = self.image.get_rect()

        self.rect.centerx = coord[0]
        self.rect.centery = coord[1]

        self.hit = [pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Upgrade.ogg")),
                       pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Life-Up.ogg"))]

        self.state = random.randint(0, len(Upgrade.PATTERN))
        self.image_state = 0


    def sound(self, num):
        """
        --> None
        Plays the upgrade gain sounds
            num(int) --> 0 or 1, 0: standard, 1: Special (1UP)
        """
        self.hit[num].play()

    def update(self):
        """
        Method to control sprite behavior, an Upgrade does the following:
            Moves down in a pattern
            Changes image (for rotation)
            Checks if it is touched by a Paddle, and activates upgrade
            Dies if it touches the bottom

        This method is called by Group.update()
        """
        self.state += 1
        self.image_state += 1
        if self.state >= len(Upgrade.PATTERN):
            self.state = 0
        self.rect.centerx += Upgrade.PATTERN[self.state]
        self.rect.centery += 3
        if self.rect.right > border[1]:
            self.rect.right = border[1]
        elif self.rect.left < border[0]:
            self.rect.left = border[0]
        if self.rect.bottom > border[3]:
            self.kill()

        if self.color == "1":
            if self.image_state == len(Upgrade.UP_IMAGES) * 3:
                self.image_state = 0
            if self.image_state % 3 == 0:
                self.image = Upgrade.UP_IMAGES[self.image_state / 3]
        else:
            if self.image_state >= 3 * 3:
                self.image_state = 0
            if self.image_state % 3 == 0:
                self.image = Upgrade.IMAGES[3 * Upgrade.COLORS.find(self.color) + self.image_state / 3 ]

        collisions = pygame.sprite.spritecollide(self, misc, False)
        for other in collisions:
            if type(other) == Paddle:
                self.sound(0)
                self.kill()
                if self.color == "B":
                    #Blue, multiball, 2 balls appear
                    score.add_score(random.randint(500,1000))
                    temp = Ball( (other.rect.left - 2, other.rect.top - 15) )
                    temp.vector.set_angle(radians(225))
                    balls.add(temp)

                    temp = Ball( (other.rect.right + 2, other.rect.top - 15) )
                    temp.vector.set_angle(radians(315))
                    balls.add(temp)

                elif self.color == "G":
                    #Green, Get Rockets
                    score.add_score(1000)
                    portal.reset()
                    rocket_ammo.add_ammo(1)
                elif self.color == "O":
                    #Orange, Fireball for 5 sec
                    score.add_score(random.randint(100, 500))
                    for ball in balls:
                        ball.fire(framerate*5)

                elif self.color == "R":
                    #Red, Laser Paddle
                    score.add_score(750)
                    other.change(5)
                    laser_ammo.add_ammo(25)
                elif self.color == "Y":
                    #Yellow, bigger paddle
                    if other.get_paddle_type() == 1:
                        other.change(2)
                        score.add_score(random.randint(300,500))
                    elif other.get_paddle_type() == 4:
                        score.add_score(random.randint(2500, 5000))
                    elif other.get_paddle_type() >= 3 and other.get_paddle_type() < 4:
                        other.change( other.get_paddle_type() + 0.5 )
                        score.add_score(random.randint(100,1250))
                    else:
                        other.change(3)
                        score.add_score(random.randint(300,500))

                elif self.color == "Z":
                    #black smaller paddle cancels laser and changes ball speed
                    score.add_score(random.randint(500, 1000))
                    other.change(1)
                    for ball in balls:
                        #creates ball speeds of: 1 or 9
                        if random.randint(0,1):
                            ball.vector.set_velocity( 1 )
                        else:
                            ball.vector.set_velocity( 8 )

                elif self.color == "1":
                    #1UP, Life UP
                    self.sound(1)
                    score.add_score(random.randint(2500,10000))
                    life.gain_life(1)

################################################################################
class Laser(pygame.sprite.Sprite):
    """
    A class which models a simple laser projectile
    """

    IMAGE = pygame.image.load(os.path.join("images", "Sprites", "Paddles & Ammunition", "laser.gif"))
    IMAGE.set_colorkey( IMAGE.get_at( (0,0) ) )

    def __init__(self, coord):
        """
        Creates a Laser object
            coor(list) --> (x,y) bottom middle point on the object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = Laser.IMAGE
        self.rect = self.image.get_rect()

        self.rect.bottom = coord[1]
        self.rect.centerx = coord[0]

        self.y_loc = self.rect.centery

        self.velocity = 12

        pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Laser2.ogg")).play()
        pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Laser.ogg")).play()

    def update(self):
        """
        Method to control sprite behavior, a Laser does the following:
            Moves up
            Dies if it hits the top border
            Checks for Block collisions and calls the Block.hit() method

        This method is called by Group.update()
        """
        self.y_loc -= self.velocity
        self.rect.centery = self.y_loc

        if self.rect.top < border[2]:
            self.kill()

        collisions = pygame.sprite.spritecollide(self, blocks, False)
        results = []
        for other in collisions:
            other.hit()
            self.kill()

################################################################################
class Rocket(pygame.sprite.Sprite):
    """
    A rocket projectile object which can be controlled and leaves beahind a trail
    """

    IMAGES = []
    for i in [1,2]:
        temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Missle - %i.gif" % (i))
        IMAGES.append(temp)

    # temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Missle - %i.gif" % (i))
    # temp.set_alpha(0)
    # IMAGES.append(temp)

    def __init__(self, coord):
        """
        Creates a Rocket object
            coord(list) --> (x,y) bottom right point on the object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = Rocket.IMAGES[0].copy()
        self.rect = self.image.get_rect()

        self.rect.bottom = coord[1]
        self.rect.right = coord[0]
        self.coord = [self.rect.centerx, self.rect.centery]

        self.vector = Vector(2, radians(225))
        self.image = pygame.transform.rotate(self.image, -45)

        self.state = 0

        self.sound = pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Missle.ogg"))
        self.sound.play(-1)

        self.blink = framerate

    def boom(self):
        """
        --> None
        Creates an Explosion at its current coordinate
        Calls self.kill()
        """
        misc.add( Explosion( self.coord ) )
        self.kill()

    def kill(self):
        """
        --> None
        Stops music Playback then removes Sprite from all groups that contain it
        """
        self.sound.play()
        self.sound.stop()
        pygame.sprite.Sprite.kill(self)

    def turn_left(self):
        """
        --> None
        Rotates its movement direction left 10 degrees
        """
        self.vector.set_angle( self.vector.get_angle() - radians(10) )

    def turn_right(self):
        """
        --> None
        Rotates its movement direction right 10 degrees
        """
        self.vector.set_angle( self.vector.get_angle() + radians(10) )

    def update(self):
        """
        Method to control sprite behavior, a Rocket does the following:
            Moves in its movement direction
            Creates a Puffs within 3 pixels up and sideways of its previous coordinates
            Calls self.boom() if it hits a border or a Block
                NOTE: the rocket will not collide with Blocks for the first second

        This method is called by Group.update()
        """
        puff_vector = self.vector.copy()
        puff_vector.set_velocity(-15)
        x_puff = int(self.rect.centerx + puff_vector.dx())
        y_puff = int(self.rect.centery + puff_vector.dy())
        trail.add( Puff( (random.randint(x_puff - 3, x_puff + 3),
                              random.randint(y_puff - 3, y_puff + 3)), random.randint(50, 150), random.randint(50, 255)))
        #moving
        self.coord[0] += self.vector.dx()
        self.coord[1] += self.vector.dy()

        self.state += 1
        #hitting the borders
        if self.rect.right > border[1] or self.rect.left < border[0] or self.rect.bottom > border[3] or self.rect.top < border[2]:
            self.boom()
        if not self.blink:
            #collisions with a block
            if pygame.sprite.spritecollideany(self, blocks):
                self.boom()

            if self.state > 1:
                self.state = 0

        else:
            self.blink -= 1
            if self.state >= len(Rocket.IMAGES):
                self.state = 0
        self.image = Rocket.IMAGES[self.state].copy()
        self.image = pygame.transform.rotate(self.image, 360 - degrees(self.vector.get_angle()))

        self.rect = self.image.get_rect()

        self.rect.centerx = int(self.coord[0])
        self.rect.centery = int(self.coord[1])

################################################################################
class Explosion(pygame.sprite.Sprite):
    """
    A class which models an explosion with a specific size
    """

    IMAGES = []
    for num in range(0,10):
        image = pygame.image.load(os.path.join("images", "Sprites", "Paddles & Ammunition", "Blast ~ %i.gif" % (num)))
        image.set_colorkey( image.get_at( (0,0) ) )
        IMAGES.append( image )

    def __init__(self, coord):
        """
        Creates a Explosion object
            coord(list) --> (x,y)center point on the object
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = Explosion.IMAGES[0]

        self.rect = self.image.get_rect()
        self.rect.centerx = coord[0]
        self.rect.centery = coord[1]
        self.radius = 24

        self.counter = 0

        pygame.mixer.Sound(os.path.join("sounds", "In-Game", "Boom.ogg")).play()

    def corners_collide(self, other):
        """
        --> bool
        Return True if other collided with self after taking corners into account
        Should only be used once the two object are known to collide using Rect
        """
        if other.rect.bottom < self.rect.top + 22 or other.rect.top > self.rect.bottom - 22:
            if other.rect.right < self.rect.left + 22 or other.rect.left > self.rect.right - 22:
                return False
        return True

    def update(self):
        """
        Method to control sprite behavior, an Explosion will do the following:
            Change image
            Call self.kill() if explosion finishes
            Check for Block collision and Call Block.hit()
            Check for Ball collision and blast ball away

        This method is called by Group.update()
        """
        self.counter += 1
        rate = framerate / 20
        if self.counter >= (11 * rate):
            self.kill()
        elif self.counter % rate == 0:
            if self.counter / rate == 1:
                self.radius = 30
            elif self.counter / rate == 2:
                self.radius = 44
            else:
                self.radius = 60
            self.image = Explosion.IMAGES[self.counter / rate - 1]
        #collisions with a ball
        collisions = pygame.sprite.spritecollide(self, balls, False)
        for other in collisions:
            if pygame.sprite.collide_circle(other, self):
                other.sound()
                other.vector = Vector()
                other.vector.from_points( (self.rect.centerx, self.rect.centery), (other.rect.centerx, other.rect.centery) )
                other.vector.set_velocity( other.velocity + 10 )
        #collisions with a block
        collisions = pygame.sprite.spritecollide(self, blocks, False)
        results = []
        for other in collisions:
            if self.corners_collide(other):
                other.hit(special = "ROCKET")

################################################################################
class Paddle(pygame.sprite.Sprite):
    """
    A class which models a player controlled paddle class
    """

    IMAGES = []
    LASER_IMAGES = []
    for item in ["0.75", "1.0", "1.5", "2.0"]:
        temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Paddle ~ x%s.gif" % (item))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        IMAGES.append(temp)

        temp = pygame.image.load("images/Sprites/Paddles & Ammunition/Paddle ~ x%s - LASER.gif"  % (item))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        LASER_IMAGES.append(temp)

    def __init__(self, coordinates):
        """
        Creates a Paddle object
            coordinates(list) --> (x,y) the top left corner of the paddle
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = Paddle.IMAGES[1]
        self.paddle_type = 2
        self.rect = self.image.get_rect()

        self.rect.left = coordinates[0]
        self.rect.top = coordinates[1]

        self.no_dir()
        self.laser = False
        self.laser_countdown = 0

        self.ball_vector = Vector(30, radians(270))

    def arrow(self):
        """
        --> Surface
        Returns a surface containing a line pointing in the ball launching direction
        """
        arrow = pygame.Surface((60, 60))
        arrow.fill( [125,125,125] )
        arrow.set_colorkey( arrow.get_at((0,0)) )
        pygame.draw.line(arrow, [255,255,255],
                         (30, 60),
                         (30 + int(self.ball_vector.dx()), 60 + int(self.ball_vector.dy())), 3)
        pygame.draw.line(arrow, [0,0,0],
                         (30, 60),
                         (30 + int(self.ball_vector.dx()), 60 + int(self.ball_vector.dy())), 1)
        return arrow

    def have_ball(self):
        """
        --> bool
        Returns True if the paddle has a ball to launch
        """
        return bool(self.ball_vector)

    def fire_ball(self):
        """
        --> None
        Launches the ball if it is held right now
        """
        if self.have_ball():
            ball = Ball( (self.rect.centerx, self.rect.top - 10))
            ball.vector = self.ball_vector
            ball.vector.set_velocity(ball.velocity)
            balls.add( ball )

        self.ball_vector = None

    def turn_launch_left(self):
        """
        --> None
        Turns the ball_launch direction left 5 degrees, if the paddle has a ball
        """
        if self.have_ball():
            temp = self.ball_vector.get_angle() - radians(5)
            if temp < radians(210):
                temp = radians(210)
            self.ball_vector.set_angle( temp )

    def turn_launch_right(self):
        """
        --> None
        Turns the ball_launch direction right 5 degrees, if the paddle has a ball
        """
        if self.have_ball():
            temp = self.ball_vector.get_angle() + radians(5)
            if temp > radians(330):
                temp = radians(330)
            self.ball_vector.set_angle( temp )

    def right_dir(self):
        """
        --> None
        Makes the paddle start moving right
        """
        self.dx = 1

    def left_dir(self):
        """
        --> None
        Makes the paddle start moving left
        """
        self.dx = -1

    def no_dir(self):
        """
        --> None
        Makes the paddle stop moving
        """
        self.dx = 0

    def set_x(self, x):
        """
        --> None
        Sets the norizontal center position of the paddle
            x(int) --> new position
        """
        self.rect.centerx = int(x)
        if self.rect.right > border[1]:
            self.rect.right = border[1]
        elif self.rect.left < border[0]:
            self.rect.left = border[0]

    def fire_laser(self):
        """
        --> None
        Fires laser if laser is on and there is ammo
        """
        if self.laser and self.laser_countdown <= 0 and laser_ammo.use_ammo():
            misc.add( Laser( (self.rect.centerx, self.rect.top) ) )
            """
            #used for sprites with 2 lasers and 3 lasers (unused for now) too cheap
            if int(self.paddle_type) <= 2:
                misc.add( Laser( (self.rect.centerx, self.rect.top) ) )
            elif int(self.paddle_type) == 3:
                misc.add( Laser( (self.rect.left + 16, self.rect.top) ) )
                misc.add( Laser( (self.rect.right - 16, self.rect.top) ) )
            elif int(self.paddle_type) == 4:
                misc.add( Laser( (self.rect.left + 13, self.rect.top) ) )
                misc.add( Laser( (self.rect.right - 13, self.rect.top) ) )
                misc.add( Laser( (self.rect.centerx, self.rect.top) ) )
            """
            self.laser_countdown = framerate / 8

    def change(self, paddle_type):
        """
        --> None
        Changes the paddle's sprite
            type(int) --> What sprite to use
                1 --> Paddle with x0.75 Size, Laser Disabled
                2 --> Paddle with x1    Size
                3 --> Paddle with x1.5  Size
                4 --> Paddle with x2    Size
                5 --> Paddle with Same  Size, Laser Enabled
        """
        x_cen = self.rect.centerx
        y_cen = self.rect.centery

        if paddle_type == 5:
            self.laser = True
        elif paddle_type == 1:
            self.laser = False
            self.paddle_type = paddle_type
        else:
            self.paddle_type = paddle_type

        if not self.laser:
            self.image = Paddle.IMAGES[int(self.paddle_type - 1)]

        else:
            self.image = Paddle.LASER_IMAGES[int(self.paddle_type - 1)]

        self.rect = self.image.get_rect()
        self.rect.centerx = x_cen
        self.rect.centery = y_cen

    def get_paddle_type(self):
        """
        --> int
        Returns the paddle type
            1 --> Paddle with x0.75 Size
            2 --> Paddle with x1    Size
            3 --> Paddle with x1.5  Size
            4 --> Paddle with x2    Size
        """
        return self.paddle_type

    def update(self):
        """
        Method to control sprite behavior, a Paddle will do the following:
            Move the position of the object
            Countdown laser overheat
            Check for border collisions
            Check if a ball collides with it and change ball direction

        This method is called by Group.update()
        """
        #hitting the borders & movement
        self.set_x(self.dx * 8 + self.rect.centerx)

        self.laser_countdown -= 1

        # ball colliding with it
        collisions = pygame.sprite.spritecollide(self, balls, False)
        for other in collisions:
            other.sound(3)
            temp_vector = Vector()
            temp_vector.from_points( (self.rect.centerx, 0), (other.rect.centerx, 0) )

            #so that reflection angle isnt too extreme only adds 1/4 of the vecotr
            temp_vector.set_velocity( temp_vector.get_velocity() * 0.25)
            other.vector.set_dy(other.vector.dy() * -1)

            velocity = other.vector.get_velocity()
            other.vector = other.vector + temp_vector

            #normalizes velocity, halves the difference between standard and actual velocity
            other.vector.set_velocity( (other.velocity + velocity) / 2.0  )


            other.rect.bottom = self.rect.top
            other.coord[1] = other.rect.centery

################################################################################
class Ball(pygame.sprite.Sprite):
    """
    A class which models a ball
    """

    NORMAL_IMAGE = pygame.image.load("images/Sprites/Balls/Ball ~ Normal.gif")
    NORMAL_IMAGE.set_colorkey( NORMAL_IMAGE.get_at( (0,0) ) )

    FIRE_IMAGES = []

    for image in range(1,5):
        temp = pygame.image.load("images/Sprites/Balls/Ball ~ Fireball %i.gif" % (image))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        FIRE_IMAGES.append(temp)

    def __init__(self, coordinates):
        """
        Creates a Ball object
            coordinates(list) --> (x,y) the top left corner of the ball
        """
        pygame.sprite.Sprite.__init__(self)


        self.image = Ball.NORMAL_IMAGE
        self.rect = self.image.get_rect()

        self.rect.left = coordinates[0]
        self.rect.top = coordinates[1]

        self.coord = [self.rect.centerx, self.rect.centery]
        self.radius = (self.rect.right - self.rect.left) / 2

        self.velocity = 4
        self.vector = Vector( self.velocity,  radians(225))

        self.fire_count = 0
        self.fire_image = 0

        self.bounce = [pygame.mixer.Sound(os.path.join("Sounds", "In-Game", "bounce1.ogg")),
                       pygame.mixer.Sound(os.path.join("Sounds", "In-Game", "bounce2.ogg")),
                       pygame.mixer.Sound(os.path.join("Sounds", "In-Game", "bounce3.ogg")),
                       pygame.mixer.Sound(os.path.join("Sounds", "In-Game", "Wall Bounce.ogg")),
                       pygame.mixer.Sound(os.path.join("Sounds", "In-Game", "Barrier Bounce.ogg"))]

    def sound(self, num = None):
        """
        --> None
        Plays the bounce sound
            num(int) --> between 0,2 the specific sound to play
        """
        if num:
            self.bounce[num].play()
        else:
            self.bounce[random.randint(0,2)].play()

    def undo(self, num):
        """
        --> None
        Moves ball back a certain number of steps, Can also be used to redo by using negative numbers
            num(int) --> Steps to go back, approximately 1 pixel per step
        """
        velocity = self.vector.get_velocity()
        if velocity < 0:
            self.vector.set_velocity( num )
        else:
            self.vector.set_velocity( num * -1 )
        self.coord[0] += self.vector.dx()
        self.coord[1] += self.vector.dy()

        self.rect.centerx = int(self.coord[0])
        self.rect.centery = int(self.coord[1])

        self.vector.set_velocity(velocity)

    def fire(self, frames):
        """
        --> None
        Turns on Fireball for a certain amount more frames
            frames(int) --> frames to have fireball last, adds on to any previous amount
        """
        if frames > 0:
            if self.fire_count == 0:
                self.image = Ball.FIRE_IMAGES[0]
                self.rect = self.image.get_rect()

                self.rect.centerx = self.coord[0]
                self.rect.centery = self.coord[1]
                self.radius = (self.rect.right - self.rect.left) / 2

            self.fire_count += frames

    def __block_hit(self, other):
        """
        --> list
        Returns a list of all the sides bounced for this block
            other(Block) --> Block to check for which side is hit
        """
        #play bounce sound
        self.sound()
        final = []

        #collision with top area
        if self.rect.bottom >= other.rect.top and self.rect.bottom < other.rect.centery:
            final.append( "UP" )
        #if collision with bottom area
        if self.rect.top > other.rect.centery and self.rect.top <= other.rect.bottom:
            final.append( "DOWN" )

        #collision with left area
        if self.rect.right >= other.rect.left and self.rect.right < other.rect.centerx:
            final.append( "LEFT" )
        #if collision with right area
        if self.rect.left > other.rect.centerx and self.rect.left <= other.rect.right:
            final.append( "RIGHT" )

        return final

    def update(self):
        """
        Method to control sprite behavior, a Ball does the following:
            Move location
            Create a Puff that lasts ten frames
            Slowly Change velocity to match required number
            Check for border, and block collisions, and change movement vector accordingly
            Counts down fireball timer

        This method is called by Group.update()
        """
        #used for barrier collisions
        prev_pos = (self.rect.centerx, self.rect.centery)
        prev_vector = self.vector.copy()

        trail.add( Puff( self.coord, 10 , 180, 18, self.image.copy()) )
        #moving
        self.coord[0] += self.vector.dx()
        self.coord[1] += self.vector.dy()

        self.rect.centerx = int(self.coord[0])
        self.rect.centery = int(self.coord[1])

        #slow down
        if self.vector.get_velocity() > self.velocity:
            self.vector.set_velocity( self.vector.get_velocity() - 0.01 )
        #speed up
        elif self.vector.get_velocity() < self.velocity:
            self.vector.set_velocity( self.vector.get_velocity() + 0.01 )
        """
        elif self.vector.get_velocity() > self.velocity * 4:
            self.vector.set_velocity(self.velocity * 4)
        elif self.vector.get_velocity() < self.velocity * -4:
            self.vector.set_velocity(self.velocity * -4)"""

        # Collision with a line
        #if pygame.sprite.spritecollideany(self, barrier_lines):
        prev_vector.set_velocity( prev_vector.get_velocity() * 2 )
        temp = barrier_lines.collide(prev_pos, prev_vector)
        if temp:
            score.add_score(random.randint(50, 100))
            self.coord[0] = temp[0][0]
            self.coord[1] = temp[0][1]
            self.rect.centerx = int(self.coord[0])
            self.rect.centery = int(self.coord[1])
            velo = self.vector.get_velocity()
            self.vector = temp[1]
            self.vector.set_velocity(velo + 0.5)
            self.undo(-3)
            self.sound(4)

        #hitting the borders
        if self.rect.right > border[1]:
            self.vector.set_dx( self.vector.dx() * -1 )
            self.rect.right = border[1]
            self.coord[0] = self.rect.centerx
            self.sound(3)
        elif self.rect.left < border[0]:
            self.vector.set_dx( self.vector.dx() * -1 )
            self.rect.left = border[0]
            self.coord[0] = self.rect.centerx
            self.sound(3)
        if self.rect.bottom > border[3]:
            #technically death
            self.kill()

        elif self.rect.top < border[2]:
            self.vector.set_dy( self.vector.dy() * -1 )
            self.rect.top = border[2]
            self.coord[1] = self.rect.centery
            self.sound(3)

        #counts down fireball timer
        if self.fire_count == 1:
            x_cen = self.rect.centerx
            y_cen = self.rect.centery

            self.image = Ball.NORMAL_IMAGE
            self.rect = self.image.get_rect()

            self.rect.centerx = x_cen
            self.rect.centery = y_cen
            self.radius = (self.rect.right - self.rect.left) / 2

            self.fire_count = 0
        elif self.fire_count > 0:
            self.fire_count -= 1
            self.image = Ball.FIRE_IMAGES[self.fire_image]
            self.fire_image += 1
            if self.fire_image >= len(self.FIRE_IMAGES):
                self.fire_image = 0

        #paddle with ball collision is done in paddle class
        #colliding with a block
        collided = pygame.sprite.Group()
        collided.add( pygame.sprite.spritecollide(self, blocks, False) )
        undone = 0
        while pygame.sprite.spritecollideany(self, collided) and undone <= self.vector.get_velocity():
            self.undo(2)
            undone += 2
        self.undo(-2)

        collisions = pygame.sprite.spritecollide(self, collided, False)
        collided.empty()
        results = []
        for other in collisions:
            if self.fire_count > 0:
                test = other.hit(special = "FIRE")
            else:
                test = other.hit()
            if test:
                for item in self.__block_hit(other):
                    results.append( item )
        #colliding with another ball
        self.ball_collided = [self]
        collisions = pygame.sprite.spritecollide(self, balls, False)
        for other in collisions:
            if other not in self.ball_collided and pygame.sprite.collide_circle(self, other):
                self.ball_collided.append(other)
                self.sound()
                self.undo(2)
                other.undo(2)

                vector = self.vector
                self.vector = other.vector
                other.vector = vector

        #resolves a collision poblem related to one brick above another
        if results.count("RIGHT") > 1:
            results = ["RIGHT"]
        elif results.count("LEFT") > 1:
            results = ["LEFT"]
        if results.count("UP") > 1:
            results = ["UP"]
        elif results.count("DOWN") > 1:
            results = ["DOWN"]


        if "RIGHT" in results and "LEFT" in results:
            pass
        elif "RIGHT" in results:
            self.vector.set_dx(abs(self.vector.dx()))
        elif "LEFT" in results:
            self.vector.set_dx(abs(self.vector.dx()) * -1)

        if "UP" in results and "DOWN" in results:
            pass
        elif "UP" in results:
            self.vector.set_dy(abs(self.vector.dy()) * -1)
        elif "DOWN" in results:
            self.vector.set_dy(abs(self.vector.dy()))

################################################################################

class Block(pygame.sprite.DirtySprite):
    """
    A class which models a Block for arkanoid
    """

    #cover sprites
    COVER = []
    temp = pygame.image.load("images/Sprites/Blocks/Crack.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.Surface((24,16))
    temp.fill([254,234,2])
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Skull.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Barrier.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Group I.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Group II.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Group III.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)

    temp = pygame.image.load("images/Sprites/Blocks/Group ID.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Group IID.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Group IIID.gif")
    temp.set_colorkey( temp.get_at((0,0)) )
    COVER.append(temp)

    #block Sprites
    BLOCK_IMAGES = []
    for color in ["BLUE","GREEN","ORANGE","PURPLE","RED","SKY BLUE","WHITE","YELLOW","ZBLACK"]:
        temp = pygame.image.load("images/Sprites/Blocks/Brick Style 2 ~ %s.jpg" % (color))
        temp.set_colorkey()
        BLOCK_IMAGES.append(temp)

    #normal death image list
    DEATH_IMAGES = []
    for image in range(1,5):
        temp = pygame.image.load("images/Sprites/Blocks/Brick Style Any ~ Death %i.gif" % (image))
        temp.set_colorkey( temp.get_at( (0,0) ) )
        DEATH_IMAGES.append(temp)

    #fireball death image list
    FIRE_DEATH_IMAGES = []
    for part in range(1,4):
        for image in range(1,4):
            temp = pygame.image.load("images/Sprites/Blocks/Brick Style Any ~ Fire Death %i-%i.gif" % (part, image))
            temp.set_colorkey( temp.get_at( (0,0) ) )
            FIRE_DEATH_IMAGES.append(temp)

    temp = pygame.image.load("images/Sprites/Blocks/Brick Style Any ~ Fire Death 4-1.gif")
    temp.set_colorkey( temp.get_at( (0,0) ) )
    FIRE_DEATH_IMAGES.append(temp)
    temp = pygame.image.load("images/Sprites/Blocks/Brick Style Any ~ Fire Death 4-2.gif")
    temp.set_colorkey( temp.get_at( (0,0) ) )
    FIRE_DEATH_IMAGES.append(temp)

    #list of colors used for changing block images
    COLORS = "BGOPRSWYZ"

    Barrier = { "BLOCKS" : [], "LINES": Barrier_Lines()}
    Groups = { 5: [], 6 : [], 7: []}

    def __init__(self, coord, lives = None, color = None ):
        """
        Creates a new Block object with these properties
            coord(tuple) --> (x,y) The sprite coordinates for the block
            lives(int)   --> the type of the block from the below list   (PRESET: 1)
                1 --> 1 Life Block
                2 --> 2 Life Block
                3 --> Skull Block
                4 --> Barrier Brick
                5 --> Group Brick I
                6 --> Group Brick II
                7 --> Group Brick III
            color(str)   --> the color for the Block from the below list (PRESET: Random)
                B --> Blue
                G --> Green
                O --> Orange
                P --> Purple
                R --> Red
                S --> Sky Blue
                W --> White
                Y --> Yellow
                Z --> Black
                ? --> Random
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.color = color
        if self.color == None or color == "?":
            self.color =  Block.COLORS[ random.randint(0,len(Block.COLORS)) - 1 ]
        if lives == None:
            lives = 1
        elif lives == 4:
            Block.Barrier["BLOCKS"].append(self)
        elif lives >= 5 and lives <= 7:
            Block.Groups[lives].append(self)

        self.image = Block.BLOCK_IMAGES[ Block.COLORS.find(self.color)].copy()
        self.image.blit(Block.COVER[lives - 1], (0,0))


        self.health = lives
        self.rect = self.image.get_rect()

        self.rect.left = coord[0]
        self.rect.top = coord[1]

    @staticmethod
    def reset():
        Block.Barrier["LINES"].empty()
        Block.Barrier = { "BLOCKS" : [], "LINES": Barrier_Lines()}
        Block.Groups = { 5: [], 6 : [], 7: []}

    @staticmethod
    def make_lines():
        Block.Barrier["LINES"].empty()
        Block.Barrier["LINES"] = Barrier_Lines()
        for item in range(len(Block.Barrier["BLOCKS"]) - 1):
            for item2 in range(item + 1, len(Block.Barrier["BLOCKS"])):
                point1 = (Block.Barrier["BLOCKS"][item].rect.centerx - 1, Block.Barrier["BLOCKS"][item].rect.centery - 1)
                point2 = (Block.Barrier["BLOCKS"][item2].rect.centerx - 1, Block.Barrier["BLOCKS"][item2].rect.centery - 1)
                Block.Barrier["LINES"].new_line(point1, point2)
        return Block.Barrier["LINES"]

    @staticmethod
    def set_lines(barrier_lines):
        Block.Barrier["LINES"] = barrier_lines


    def alive(self):
        """
        --> bool
        Returns True if the block is alive (not doing death animation)
        """
        if self.health > 0:
            return True
        return False

    def lines(self):
        lines = []
        lines.append( Line_Segment(self.rect.topleft, self.rect.topright) )
        lines.append( Line_Segment(self.rect.bottomleft, self.rect.bottomright) )
        lines.append( Line_Segment(self.rect.topleft, self.rect.bottomleft) )
        lines.append( Line_Segment(self.rect.topright, self.rect.bottomright) )
        return lines

    def create_upgrade(self):
        """
        --> None
        Creates an Upgrade at this Block location, also does randomization for Upgrade color
        """
        percent = random.randint(1,100)
        # matches block color with upgrade color, if no match, randomizes
        if self.color in Upgrade.COLORS:
            upgrade_color = Upgrade.COLORS.find(self.color)
        else:
            upgrade_color = random.randint(0,len(Upgrade.COLORS) - 1)
        #19% chance of same color upgrade
        if percent <= 79:
            upgrade_color = random.randint(0,len(Upgrade.COLORS) - 1)
        #extra 10% chance for multiball
        elif percent <= 18:
            upgrade_color = 1
        #Only 8 % chance of 1UP
        if percent <= 8:
            upgrade_color = "1"
        else:
            upgrade_color = Upgrade.COLORS[upgrade_color]
        upgrades.add( Upgrade((random.randint(self.rect.left, self.rect.right),
                               random.randint(self.rect.top, self.rect.bottom)),
                               upgrade_color ))

    def hit(self, special = None):
        """
        --> bool
        Returns True if the block is killed (if indestructible, doesnt kill it)
        Adds to score decreases lives and spawns Upgrade
            special(str) --> any special hit, currently:
                FIRE --> Fireball Hit (kills destructible)
                ROCKET --> Rocket
        """
        self.dirty = 1
        dead = None
        score_in = []

        if self.health == 1:
            score_in.append(random.randint(100,250))
            self.health = 0
            if special == "FIRE":
                dead = "FIRE"
            else:
                dead = "NORMAL"

        elif self.health == 2:
            score_in.append(random.randint(250,500))
            if special == "FIRE":
                score_in.append(random.randint(100,250))
                dead = "FIRE"
            elif special == "ROCKET":
                dead = "NORMAL"
                score_in.append(random.randint(100,250))
            else:
                self.health = 1
        elif self.health == 3:
            score_in.append(random.randint(50,100))
            if special == "ROCKET":
                score_in.append(random.randint(5000,10000))
                unkilled_needed[0] -= 1
                dead = "NORMAL"
            elif special == "FIRE":
                if random.randint(1,100) <= 10:
                    self.create_upgrade()

        elif self.health == 4:
            score_in.append(random.randint(1000,2000))
            Block.Barrier["LINES"].kill_all((self.rect.centerx - 1, self.rect.centery - 1))
            dead = "NORMAL"
        elif self.health >= 5 and self.health <= 7:
            score_in.append(random.randint(250,750))
            self.health += 3
            kill = True
            for item in Block.Groups[self.health - 3]:
                if item.health != self.health:
                    kill = False
            if kill:
                dead = "GROUP"
        elif self.health >= 8 and self.health <= 10:
            score_in.append(random.randint(250,500))

        for increase in score_in:
            score.add_score(increase)

        if dead:
            if random.randint(1,100) <= 10:
                self.create_upgrade()
            if dead == "GROUP":
                for item in Block.Groups[self.health - 3]:
                    item.kill()
                    dead_blocks.add(item)
                    item.health = 0
                    item.state = 0
                    item.image = Block.DEATH_IMAGES[0]
                self.Groups[self.health - 3] = []
                return True
            elif dead == "FIRE":
                self.kill()
                dead_blocks.add(self)
                self.health = -1
                self.death = 0
                self.state = 0

                x_cen = self.rect.centerx
                y_cen = self.rect.centery

                self.image = Block.FIRE_DEATH_IMAGES[0]
                self.rect = self.image.get_rect()

                self.rect.centerx = x_cen
                self.rect.centery = y_cen
                return False
            elif dead == "NORMAL":
                self.kill()
                dead_blocks.add(self)
                self.health = 0
                self.state = 0
                self.image = Block.DEATH_IMAGES[0]
                return True
        self.image = Block.BLOCK_IMAGES[ Block.COLORS.find(self.color)].copy()
        self.image.blit(Block.COVER[self.health - 1], (0,0))
        return True




        '''
        if self.health == 1 or kill:

            self.state = 0

            self.image = Block.DEATH_IMAGES[0]
            self.kill()
            dead_blocks.add(self)

            if random.randint(1,100) <= 10:
                self.create_upgrade()

            score.add_score(random.randint(100,250))
            if kill and self.health == 2:
                score.add_score(random.randint(250,500))
            if kill and self.health == 3:
                score.add_score(random.randint(5000,10000))
                unkilled_needed[0] -= 1
            self.health = 0

        elif self.health == 2:
            self.health = self.health - 1
            self.image = Block.BLOCK_IMAGES[  7 * (Block.COLORS.find(self.color))]
            score.add_score(random.randint(250,500))

        else:
            score.add_score(random.randint(50,100))



    def fire_hit(self):
        """
        --> bool
        Returns True if the block is killed (if indestructible, doesnt kill it)
        Adds to score, kills the brick and spawns Upgrade
        """
        self.dirty = 1
        if self.health == 1 or self.health == 2:
            self.health = -1
            self.death = 0
            self.state = 0

            x_cen = self.rect.centerx
            y_cen = self.rect.centery

            self.image = Block.FIRE_DEATH_IMAGES[0]
            self.rect = self.image.get_rect()

            self.rect.centerx = x_cen
            self.rect.centery = y_cen

            self.kill()
            dead_blocks.add(self)

            if random.randint(1,100) <= 15:
                self.create_upgrade()

            score.add_score(100 + random.randint(0,150))
            if self.health == 2:
                score.add_score(250 + random.randint(0,250))

        elif self.health == 3:
            score.add_score(random.randint(50,100))
            if random.randint(1,100) <= 10:
                self.create_upgrade()
            return False
        return True
        '''

    def update(self):
        """
        Method to control sprite behavior, a Block does the following:
            Loops death animations if any

        This method is called by Group.update()
        """
        self.dirty = 2
        if self.health == -1:
            self.death += 1
            self.state += 1
            if self.death >= 3:
                self.death = 0
            if self.state >= (framerate * 2 + 2):
                self.kill()
            elif self.state < (framerate * 1):
                self.image = Block.FIRE_DEATH_IMAGES[self.death]
            elif self.state < (framerate * 1.5):
                self.image = Block.FIRE_DEATH_IMAGES[self.death + 3]
            elif self.state < (framerate * 2):
                self.image = Block.FIRE_DEATH_IMAGES[self.death + 6]
            else:
                self.image = Block.FIRE_DEATH_IMAGES[self.death + 9]

        elif self.health == 0:
            self.state += 1
            unit = (framerate / len(Block.DEATH_IMAGES))
            if self.state >= framerate:
                self.kill()
            elif self.state == unit:
                self.image = Block.DEATH_IMAGES[1]
            elif self.state == unit * 2:
                self.image = Block.DEATH_IMAGES[2]
            elif self.state == unit * 3:
                self.image = Block.DEATH_IMAGES[3]

################################################################################
class Life(pygame.sprite.Group):
    """
    A class that models a life bar
    """

    IMAGE = pygame.image.load(os.path.join("images", "Sprites", "Icons", "Life Ball.gif"))
    IMAGE.set_colorkey( IMAGE.get_at( (0,0) ) )

    def __init__(self, lives, coord):
        """
        Creates a Life object
            lives(int)  --> From 1 to 12, number of lives
                            Note: first life is not seen as a ball
            coord(list) --> the center point for the first life ball
        """
        pygame.sprite.Group.__init__(self)
        self.life_balls = []
        if lives > 12:
            lives = 12
        self.coord = coord

        self.last_life = False
        self.gain_life(lives)

    def lose_life(self):
        """
        --> None
        Decreases the number of lives
        """
        if self.alive() and len(self.life_balls) > 0:
            self.life_balls[-1].kill()
            self.life_balls.pop(-1)
        elif self.alive():
            self.last_life = False

    def alive(self):
        """
        --> bool
        Returns True if there are any lives left
        """
        return self.last_life

    def gain_life(self, num):
        """
        --> None
        Adds a certain number of lives up to a limit of 12
            num(int) --> Number of lives to add
        """
        if not self.alive():
            self.last_life = True
            num -= 1
        for i in range(num):
            if len(self.life_balls) >= 12:
                break
            coord = [ self.coord[0] + len(self.life_balls) * Life.IMAGE.get_width() + 1, self.coord[1] ]
            ball = Puff(coord, life = -1, image = Life.IMAGE)
            self.add( ball )
            self.life_balls.append(ball)

################################################################################
class Highscores(pygame.sprite.DirtySprite):
    """
    A class which models a Highscores window
    """

    IMAGE = pygame.image.load(os.path.join("Images", "Backgrounds", "High Scores.jpg"))
    CLOSE = pygame.image.load(os.path.join("Images", "Sprites", "Icons", "High Scores - Close.gif"))
    CLOSE.set_colorkey( CLOSE.get_at((0,0)) )
    IMAGE.blit(CLOSE, (445, 0))
    IMAGE2 = pygame.image.load(os.path.join("Images", "Backgrounds", "High Scores.jpg"))

    def __init__(self, coord):
        """
        Creates a Highscores object
            coord(list) --> (x,y) top left corner of the object
        """
        pygame.sprite.DirtySprite.__init__(self)

        self.image = Highscores.IMAGE.copy()
        self.rect = self.image.get_rect()
        self.rect.top = coord[1]
        self.rect.left = coord[0]

        self.load()

        self.close_rect = pygame.Rect(coord[0] + 445, coord[1], 35, 27)

        self.close_event = pygame.event.Event(pygame.USEREVENT, {"code": "POP-PLAY"})
        self.font = pygame.font.Font("cour.ttf", 18)
        self.font.set_italic(True)
        self.score_font = pygame.font.Font("cour.ttf", 15)
        self.score_font.set_bold(True)

        self.dynamic = 0
        self.dirty = 1

    def load(self):
        """
        --> None
        Loads a specific file into the Highscores object, adding players and highscores
        """
        text = SaveLoad.loadgame(os.path.join("Levels", "Highscore.txt"))
        text = text.split("\n")
        #file1 = open("Levels/Highscore.txt")
        self.players = []
        self.scores = []
        self.padding = 0

        for x in range(10):
            self.players.append( text.pop(0) )
            self.scores.append( int(text.pop(0)) )
            if len(str(self.scores[-1])) > self.padding:
                self.padding = len(str(self.scores[-1]))


    def save(self):
        """
        --> None
        Saves attributes of the Highscores object into a specific file, adding players and highscores
        """
        text = ""
        for item in range(len(self.players)):
            text += self.players[item] + "\n"
            text += str(self.scores[item]) + "\n"
        SaveLoad.savegame("Levels/Highscore.txt", text)

    def display_static(self):
        """
        --> None
        Resets its image to default
        Adds the loaded high score list to its image
        """
        if self.dynamic:
            self.image = Highscores.IMAGE2.copy()
        else:
            self.image = Highscores.IMAGE.copy()
        current_coord = [self.rect.left + 30, self.rect.top + 115]
        for x in range(2):
            for item in range(0,5):
                temp_item = "%i) %s" % (item + 5 * x + 1, self.players[item + 5 * x])
                #aligns the ) for the 2 digit number (10)
                if (item + 5 * x + 1) == 10:
                    current_coord[0] -= self.font.size("1")[0]
                self.image.blit( self.font.render(temp_item, True, [0,0,0]).convert_alpha(), current_coord)
                #Changes the spot for the input name so that #) isnt part of it, but it still aligns
                if self.players[item + 5 * x] == "":
                    self.name_coord = current_coord[:]
                    self.name_coord[0] += self.rect.left + self.font.size("%i) " % (item + 5 * x + 1))[0]
                    self.name_coord[1] += self.rect.top

                current_coord[1] += 17
                current_coord[0] += 35
                temp_item = self.__pad(self.scores[item + 5 * x])
                self.image.blit( self.score_font.render(temp_item, True, [0,0,0]).convert_alpha(), current_coord)
                current_coord [1] += 25
                current_coord[0] -= 35

            current_coord[0] += 210
            current_coord[1] = self.rect.top + 115
        self.dirty = 1

    def check_player(self, score):
        """
        --> Text/None
        Returns Text object of player name if the player has enough score to be added unto the highscore list
        Also enables dynamic display, and changes loaded scores and player names
        """
        score = int(score)
        if score > self.scores[-1]:
            self.dynamic = -1
            while score > self.scores[self.dynamic - 1] and self.dynamic - 1 >  -1 * len(self.scores):
                self.dynamic -= 1
            self.scores = self.scores[:self.dynamic] + [score] + self.scores[self.dynamic:-1]
            self.players = self.players[:self.dynamic] + [""] + self.players[self.dynamic:-1]
            self.display_static()
            self.name = Text(self.name_coord, "", "cour.ttf", 18, rgb = [0,0,0], colorkey = True)
            return self.name
        self.dynamic = 0
        return None

    def pass_event(self, event):
        """
        -->bool
        Returns True if the event is the Enter key, False otherwise
        Checks and updates the name that is being typed
        """
        self.dirty = 1
        char = event.unicode
        #not allowed characters
        if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~ `!@#$%^&*()-_=+,.<>;:'\"/?\\|[]{}" or char == "\x08":
            if char == "\x08":
                if self.players[self.dynamic][-1] == "":
                    self.players[self.dynamic] = self.players[self.dynamic][:-1]
                self.players[self.dynamic] = self.players[self.dynamic][:-1]
            else:
                self.players[self.dynamic] = self.players[self.dynamic][:-1] + char
            if len(self.players[self.dynamic]) < 12:
                self.players[self.dynamic] += ""
            self.name.message = self.players[self.dynamic]
        elif char == "\r":
            if len(self.players[self.dynamic]) == 1:
                self.players[self.dynamic] = "Unknown"
            elif self.players[self.dynamic][-1] == "":
                self.players[self.dynamic] = self.players[self.dynamic][:-1]
            self.save()
            return True
        return False

    def __pad(self,num):
        """
        --> str
        Returns the num on the image to the newest score, padded with spaces
            and with commas every three digits
            num(int) --> number to pad
        """
        num = list(" " * (self.padding - len(str(num))) + str(num))
        num.reverse()
        message = ""
        self.counter = 0
        for char in num:
            if self.counter == 3:
                if char == " ":
                    add = " "
                else:
                    add = ","
                self.counter = 0
                message = add + message
            message = char + message
            self.counter += 1
        return message

    def mouse_click(self, pos):
        """
        --> None
        Call only if mouse is pressed
        Checks if the close button is pressed
        """
        """
        Method to control sprite behavior, a Highscores object does the following:
            Checks if the "x" is pressed, only if the window has an "x" and isn't about to die

        This method is called by Group.update()
        """
        if self.close_rect.collidepoint( pos ) and not self.dynamic:
            pygame.event.post( self.close_event )
            self.dirty = 1

################################################################################
class Instructions(pygame.sprite.DirtySprite):
    """
    An object that is used to flip through a bunch of pages
    """

    PAGES = []
    for page in range(1, 10):
        temp = pygame.image.load(os.path.join("Images", "Instructions", "Instructions Page %i.jpg" % (page)))
        PAGES.append(temp)

    CLOSE = pygame.image.load(os.path.join("Images", "Sprites", "Icons", "High Scores - Close.gif"))
    CLOSE.set_colorkey( CLOSE.get_at((0,0)) )

    LEFT = pygame.image.load(os.path.join("Images", "Sprites", "Icons", "Prev Page.gif"))
    LEFT.set_colorkey( LEFT.get_at((0,0)) )

    RIGHT = pygame.image.load(os.path.join("Images", "Sprites", "Icons", "Next Page.gif"))
    RIGHT.set_colorkey( RIGHT.get_at((0,0)) )

    def __init__(self, coord):
        """
        Creates a Instructions object
            coord(list) --> (x,y) top left corner of the object
        """
        pygame.sprite.DirtySprite.__init__(self)

        self.page = 0
        self.coord = coord
        self.set_image()

        self.close_rect = pygame.Rect(coord[0] + 415, coord[1] + 20, 35, 27)
        self.next_rect = pygame.Rect(coord[0] + 445, coord[1], 39, 55)
        self.prev_rect = pygame.Rect(coord[0] + 373, coord[1], 39, 55)
        self.close_event = pygame.event.Event(pygame.USEREVENT, {"code": "POP-PLAY"})

        self.dirty = 1

    def set_image(self):
        """
        --> None
        Changes the page (image) and adds buttons
        """
        self.image = Instructions.PAGES[self.page]
        if self.page > 0:
            self.image.blit(Instructions.LEFT.copy(), (373,0))
        if self.page < len(Instructions.PAGES) - 1:
            self.image.blit(Instructions.RIGHT.copy(), (445,0))
        self.image.blit(Instructions.CLOSE.copy(), (415,20))
        self.rect = self.image.get_rect()
        self.rect.top = self.coord[1]
        self.rect.left = self.coord[0]

    def mouse_click(self, pos):
        """
        --> None
        Call only if mouse is pressed
        Checks if the close button, next page or previous page are pressed
        """
        if self.close_rect.collidepoint( pos ):
            pygame.event.post( self.close_event )
            self.dirty = 1
        if self.next_rect.collidepoint( pos ) and self.page < len(Instructions.PAGES) - 1:
            self.page += 1
            self.dirty = 1
            self.set_image()
        elif self.prev_rect.collidepoint( pos ) and self.page > 0:
            self.page -= 1
            self.dirty = 1
            self.set_image()

################################################################################
def read_level(border, group, filename):
    """
    --> list [ sr(levelname), str(pic name), str(sound name), blocks(group), indestruct(int)]
    Reads the file and creates the level based on the file, note the file will be deciphered
        INPUT: border(list)    --> [x_min, y_min, x_max, y_max] the playing area for the blocks
               group(Group)    --> Where the Blocks are put into
               filename(str)   --> The file which is loaded, in the /Levels Folder (include EXT)
        OUTPUT:level_name(str) --> What the level is called
               pic_name(str)   --> The picture that should be loaded for the background
               sound_name(str) --> The sound file that should be loaded for background music
               blocks(Group)   --> The Group containing all required Blocks
               indestruct(int) --> Number of indestructible Blocks
    """
    Block.reset()
    count_blocks = 0
    text = SaveLoad.loadgame(os.path.join("Levels", "%s" % (filename)))
    text = text.split("\n")
    final = text[:3]
    text = text[4:]
    x_list = range(border[0], border[1], 24)
    y_list = range(border[2] + 4, border[2] + 20 * 16 + 4, 16)
    for i in range(20):
        line = text.pop(0)
        for x_val in range(20):
            if line[1:3] != "  ":
                lives = int(line[1])
                if lives == 3:
                    count_blocks += 1
                color = line[2].upper()
                group.add( Block((x_list[x_val], y_list[i]), lives, color) )
            line = line[3:]
    text.pop(0)
    temp = Barrier_Lines()
    while len(text):
        line = text.pop(0)
        if len(line) == 11:
            line = line.split(">")
            line[0] = line[0].split(",")
            line[1] = line[1].split(",")
            point1 = (x_list[int(line[0][0]) - 1] + 11, y_list[int(line[0][1]) - 1] +  7)
            point2 = (x_list[int(line[1][0]) - 1] + 11, y_list[int(line[1][1]) - 1] +  7)
            temp.new_line(point1, point2)
    Block.set_lines(temp)
    final.append(group)
    final.append(count_blocks)
    final.append(temp)
    return final

################################################################################
#Python window Setup:
print """
   _____         __                           __     ___
  /  _  \_______|  | _______     ____   ____ |__| __| _/
 /  /_\  \_  __ \  |/ /\__  \   /    \ /  _ \|  |/ __ |
/    |    \  | \/    <  / __ \_|   |  (  <_> )  / /_/ |
\____|__  /__|  |__|_ \(____  /|___|  /\____/|__\____ |
        \/           \/     \/      \/               \/
"""
print """
                                 ______________
  ____             _____ _      /___   ________)
 |  _ \       _   / ____(_)         | |____
 | |_) |_   _(_) | (___  _ _ __     | _____)
 |  _ <| | | |    \___ \| | '__|    | |
 | |_) | |_| |_   ____) | | |  __   | |
 |____/ \__, (_) |_____/|_|_| / /___| |
         __/ |                \______/
        |___/
"""
print """
Please do not Close this window.
If you Close this window the game ends.
If you Close Game window this window is closed too.
"""


################################################################################

#Entities
################################################################################
# all permanent values
#Background area
BACK = pygame.image.load(os.path.join("images", "Backgrounds", "Background.jpg"))
BACK = BACK.convert()
#creates borders of the play area
border = (22, 502, 22, 422)
#border group which looks like vines
border_group = pygame.sprite.Group()

border_group.add( Border( (1, 1), os.path.join("Images", "Backgrounds", "Border", "TL.gif")) )
border_group.add( Border( (41, 1), os.path.join("Images", "Backgrounds", "Border", "T.gif")) )
border_group.add( Border( (483, 1), os.path.join("Images", "Backgrounds", "Border", "TR.gif")) )
border_group.add( Border( (1, 41), os.path.join("Images", "Backgrounds", "Border", "L.gif")) )
border_group.add( Border( (483, 41), os.path.join("Images", "Backgrounds", "Border", "R.gif")) )
border_group.add( Border( (1, 390), os.path.join("Images", "Backgrounds", "Border", "BL.gif")) )
border_group.add( Border( (41, 403), os.path.join("Images", "Backgrounds", "Border", "B.gif")) )
border_group.add( Border( (470, 395), os.path.join("Images", "Backgrounds", "Border", "BR.gif")) )

# Menu group containing all non play area sprites (gets the icons)
menu_group = pygame.sprite.Group()
pause_icon = Pause_Play([523, 105], "PLAY", "PAUSE", os.path.join("Images", "Sprites", "Icons", "Play - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "Play - 1.gif"), os.path.join("Images", "Sprites", "Icons", "Pause - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "Pause - 1.gif"))
menu_group.add(Icon([523, 79], "HIGHSCORES", os.path.join("Images", "Sprites", "Icons", "High Score - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "High Score - 1.gif")),
                Icon([523, 53], "NEW GAME", os.path.join("Images", "Sprites", "Icons", "New - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "New - 1.gif")),
                Icon([523, 157], "QUIT", os.path.join("Images", "Sprites", "Icons", "Quit - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "Quit - 1.gif")),
                Icon([523, 131], "HELP", os.path.join("Images", "Sprites", "Icons", "Help - 1.gif"),
                    os.path.join("Images", "Sprites", "Icons", "Help - 1.gif")), pause_icon
                )

# image which appear on screen during pause
PAUSE_IMAGE = pygame.image.load(os.path.join("Images", "Sprites", "Icons", "Pause On-Screen.gif"))
PAUSE_IMAGE.set_colorkey( PAUSE_IMAGE.get_at( (0,0) ) )
# paused state of screen
pause = None
# pygame clock for  framerate
clock = pygame.time.Clock()
# framerate
framerate = 45

# Group which contrains the Paddle and misc stuff
misc = pygame.sprite.Group()
# Group which contrains the Blocks, as well as the one with dead blocks
blocks = pygame.sprite.Group()
dead_blocks = pygame.sprite.Group()
#Group which contains the balls
balls = pygame.sprite.Group()
#Group which contains upgrades
upgrades = pygame.sprite.Group()
#Group which contains the ball trails
trail = pygame.sprite.OrderedUpdates()
#Group Which contains the Barriers
barrier_lines = Barrier_Lines()

################################################################################

#Action
################################################################################

# Assign Values
keep_going = True
# used so that the first time these sprites can be killed and remade, so that the same thing can happen every time before game starts
score = pygame.sprite.Sprite()
combos = pygame.sprite.Sprite()
combo_counter  = pygame.sprite.Sprite()
rocket_ammo = pygame.sprite.Sprite()
laser_ammo = pygame.sprite.Sprite()

#loop for entire program
while keep_going:
    #new game code: creates a new score, combo items, ammunition, and Icons and life
    #group which contains your lives
    life = Life(3, [87, 459])
    #score and combo stuff
    score.kill()
    score = Score((416,445), "cour.ttf", padding = 9, size = 25)
    combos.kill()
    combos = score.allow_combos( [527, 217] )
    combo_counter.kill()
    combo_counter  = combos.allow_combo_counter( [548, 304], "cour.ttf", 2, 30)
    #ammunition
    rocket_ammo.kill()
    laser_ammo.kill()
    rocket_ammo = Ammo((566,380), "cour.ttf", 2, 20, [0,0,0])
    rocket_ammo.add_ammo(1)
    laser_ammo = Ammo((555,411), "cour.ttf", 3, 20, [0,0,0])

    menu_group.add( score, rocket_ammo, laser_ammo)

    #restarts the game and level loops as well as level num
    game = True
    level = True
    level_num = 1

    #loop for this game
    while game:
        #New Level code: paddle creation, music, blocks, background image
        # loads level
        for item in blocks:
            item.kill()
        for item in dead_blocks:
            item.kill()
        temp = read_level(border, blocks.copy(), "%s.txt" % (str(level_num)))
        blocks = temp[3]
        unkilled_needed = [temp[4]]
        barrier_lines = temp[5]

        # clears extra groups
        for item in misc:
            item.kill()
        for item in balls:
            item.kill()
        for item in trail:
            item.kill()
        for item in upgrades:
            item.kill()
        #replaces combo stuff
        combos.reset()
        menu_group.add( combos, combo_counter )
        # creation of portal
        portal = Portal( (border[1]- 20, border[3] - 40), framerate )
        misc.add( portal )
        #Background Music
        pygame.mixer.music.load(os.path.join("Sounds", "Background", "%s" % (temp[2])).strip())
        pygame.mixer.music.play(-1)
        #background image
        temp = pygame.image.load(os.path.join("images", "Backgrounds", "%s" % (temp[1])).strip())
        temp.convert()
        background = BACK.copy()
        background.blit(temp, (border[0], border[2]))
        screen.blit(background, (0,0))
        #paddle creation
        paddle = Paddle(((border[1] + border[0]) / 2, border[3] - 30))
        line = Puff( (paddle.rect.centerx, paddle.rect.top), image = paddle.arrow() )
        misc.add( paddle )
        #Resets rocket
        rocket = None

        level = True

        # Loop for a level
        while level:



            # Timer
            clock.tick(framerate)

            #event Handling
            for ev in pygame.event.get():
                #events which happend regardless of paused state
                if ev.type == pygame.QUIT:
                    keep_going = False
                    game = False
                    level = False
                    #causes it to ignore the rest of the events
                    break
                #sends mousedown events to any pause icons which need it
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if type(pause) == Instructions:
                        pause.mouse_click(ev.pos)
                    elif type(pause) == Highscores:
                        pause.mouse_click(ev.pos)
                #events created by the icon class
                elif ev.type == pygame.USEREVENT:
                    if ev.code == "PAUSE":
                        #creates the on screen symbol telling you the game is paused
                        if not pause:
                            pause = Puff( [(border[1] - border[0]) / 2 + border[0],(border[3] - border[2]) / 2 + border[2]],
                                          life = -1, image = PAUSE_IMAGE.copy())
                        pause.kill()
                        menu_group.add(pause)
                    elif ev.code == "PLAY":
                        #removes the in game symbol
                        if pause:
                            pause.kill()
                        pause = None
                    elif ev.code == "HIGHSCORES":
                        #Creates the on screen highcores sheet
                        if not pause:
                            pause = Highscores( (border[0], border[2]) )
                        else:
                            if type(pause) != Highscores:
                                pause.kill()
                                pause = Highscores( (border[0], border[2]) )
                        pause.load()
                        pause.display_static()
                        pause_icon.pause()
                    elif ev.code == "HELP":
                        #Creates the on screen highcores sheet
                        if not pause:
                            pause = Instructions( (border[0], border[2]) )
                        else:
                            if type(pause) != Instructions:
                                pause.kill()
                                pause = Instructions( (border[0], border[2]) )
                        pause_icon.pause()
                    elif ev.code == "POP-PLAY":
                        #removes the HighScores and unpauses(send the play event)
                        pause_icon.play()
                    elif ev.code == "NEW GAME":
                        #breaks out 2 while loops but not the last, restarting game and reseting level number
                        if pause:
                            pause.kill()
                            pause = None
                        game = False
                        level = False
                        level_num = 1
                        #causes it to ignore the rest of the events
                        break
                    elif ev.code  == "QUIT":
                        if pause:
                            pause.kill()
                            pause = None
                        keep_going = False
                        game = False
                        level = False
                        #causes it to ignore the rest of the events
                        break
                #checks for unpausing or pausing
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_p:
                        if pause:
                            #the icon changes and then send the play event
                            pause_icon.play()
                        else:
                            #the icon changes and then send the pause event
                            pause_icon.pause()
                # events which only happen when game is playing
                if not pause:
                    if ev.type == pygame.KEYDOWN:
                        #spawns a rocket if there is enough ammo
                        if ev.key == pygame.K_w:
                            if not rocket in misc and portal.isopen() and rocket_ammo.use_ammo():
                                rocket = Rocket( (border[1] - 35, border[3] - 65) )
                                misc.add( rocket )
                        #explodes a rocket if it exists
                        elif ev.key == pygame.K_s:
                            if rocket:
                                rocket = rocket.boom()
                    """
                    #mouse laser fire, off since mouse control is disabled
                    elif ev.type == pygame.MOUSEBUTTONDOWN:
                        paddle.fire_laser()
                    #mouse paddle movement, DISABLED
                    elif ev.type == pygame.MOUSEMOTION:
                        paddle.set_x(ev.pos[0])
                    """
            # for buttons which can be held for continuous events but cannot happen during paused state
            if not pause:
                #continuous laser fire if there is ammo or if the ball has yet to be launched it is launched
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if paddle.have_ball():
                        paddle.fire_ball()
                        if line:
                            line.kill()
                        line = None
                    else:
                        paddle.fire_laser()
                #turns rocket left, if it exists
                if pygame.key.get_pressed()[pygame.K_a]:
                    if rocket:
                        rocket.turn_left()
                #turns rocket right, if it exists
                if pygame.key.get_pressed()[pygame.K_d]:
                    if rocket:
                        rocket.turn_right()
                #stopps paddle movement if both are pressed
                if pygame.key.get_pressed()[pygame.K_LEFT] and pygame.key.get_pressed()[pygame.K_RIGHT]:
                    paddle.no_dir()
                #moves paddle left
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    paddle.left_dir()
                #moves paddle right
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    paddle.right_dir()
                #stops movement if none are pressed
                else:
                    paddle.no_dir()
                #turns ball launch direction left, if the ball needs to be launched
                if pygame.key.get_pressed()[pygame.K_UP]:
                    if paddle.have_ball():
                        paddle.turn_launch_left()
                #turns ball launch direction right, if the ball needs to be launched
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    if paddle.have_ball():
                        paddle.turn_launch_right()

                #cheap mouse gravity - only if Left ctrl & Left alt are pressed (FOR TESTING)
                if (pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_LCTRL]):
                    for ball in balls:
                        ball.vector.from_points( (ball.rect.centerx, ball.rect.centery), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) )
                        ball.vector.set_velocity( ball.velocity )

                #check for life_loss
                if len(balls) <= 0 and not paddle.have_ball():
                    #reset actions in case of life loss:
                    life.lose_life()
                    #resets paddle type and location
                    paddle = Paddle(((border[1] + border[0]) / 2, border[3] - 30))
                    #if there is a rocket on screen you get refunded
                    if rocket:
                        rocket_ammo.add_ammo(1)
                    #removes the rocket
                    rocket = None
                    for item in misc:
                        item.kill()
                    misc.add(portal, paddle)
                    portal.reset()
                    #remsets combo stuff
                    combo_counter.reset()
                    combos.reset()
                    #empties previous sprites
                    for item in upgrades:
                        item.kill()
                    for item in trail:
                        item.kill()

                #checks if the level is over: unkilled will tell you max blocks on the screen for level end
                if unkilled_needed[0] >= len(blocks):
                    level = False
                    # Level End Bonus
                    score.add_score(25000)
                    #if there is a rocket on screen you get refunded
                    if rocket:
                        rocket_ammo.add_ammo(1)
                    # level limit is 15 so far
                    if level_num < 15:
                        level_num += 1
                    # if the game is over aka finished level 15 then you lose all lives effectively clicking new game
                    else:
                        # game Finish Bonus
                        score.add_score(250000)
                        for x in range(13):
                            if life.alive():
                                # every extra life you have gives you points
                                #NOTE: if you end with a high combo the point add to it and are affected by it
                                score.add_score(50000)
                                life.lose_life()
                        for x in range(rocket_ammo.ammunition()):
                            # every extra Rocket you have gives you points
                            score.add_score(25000)
                        for x in range(laser_ammo.ammunition()):
                            # every extra laser you have gives you points
                            score.add_score(500)
                # if you juse lost the game
                if not life.alive():
                    #NOTE: "check for life loss" will still have occurred
                    level = False
                    game = False

            # clears all the groups
            trail.clear(screen, background)
            barrier_lines.clear(screen, background)
            blocks.clear(screen, background)
            dead_blocks.clear(screen, background)
            upgrades.clear(screen, background)
            misc.clear(screen, background)
            balls.clear(screen, background)
            menu_group.clear(screen, background)
            border_group.clear(screen, background)
            # updates the groups only if the game is not paused (therefore it seems like it is paused
            if not pause:
                trail.update()
                balls.update()
                upgrades.update()
                dead_blocks.update()
                misc.update()
                #if the rocket collided and exploded it kills itself
                if rocket:
                    if not rocket.alive():
                        rocket = None
                #checks if you are in progress of launching the ball and adds the line AFTER paddle moves
                if paddle.have_ball():
                    #kills the previous line
                    if line:
                        line.kill()
                    # resets the portal and makes a new line
                    portal.reset()
                    line = Puff( (paddle.rect.centerx, paddle.rect.top - 30), image = paddle.arrow() )
                    misc.add( line )
            #draws the groups in specific order
            blocks.draw(screen)
            dead_blocks.draw(screen)
            upgrades.draw(screen)
            trail.draw(screen)
            barrier_lines.draw(screen)
            misc.draw(screen)
            balls.draw(screen)

            # menu and border groups (update and draw)
            menu_group.update()
            menu_group.draw(screen)
            border_group.draw(screen)
            life.clear(screen, background)
            life.draw(screen)


            pygame.display.flip()

    #add to high scores list
    high = Highscores( (border[0], border[2]) )
    high.load()
    menu_group.add(high)
    name = high.check_player(score.score)
    if name:
        #dynamic highscores
        name_input = pygame.sprite.GroupSingle()
        name_input.add( name )
        typing = True
        while typing:
            # Timer
            clock.tick(10)
            #event Handling
            for ev in pygame.event.get():
                #events which happend regardless of paused state
                if ev.type == pygame.QUIT:
                    keep_going = False
                    game = False
                    level = False
                    typing = False
                elif ev.type == pygame.KEYDOWN:
                    if high.pass_event(ev):
                        typing = False
                elif ev.type == pygame.USEREVENT:
                    if ev.code  == "QUIT":
                            keep_going = False
                            game = False
                            level = False
                            typing = False
            #leaves the other groups since they do not affect screen
            menu_group.clear(screen, background)
            name_input.clear(screen, background)
            border_group.clear(screen, background)

            menu_group.update()
            name_input.update()

            menu_group.draw(screen)
            name_input.draw(screen)
            border_group.draw(screen)

            pygame.display.flip()

        name.kill()
    high.kill()

