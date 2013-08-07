import pygame
from Vector import *
from LineSegment import *

class Barrier_Lines(pygame.sprite.Group):
    
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.lines = []
        
    def new_line(self, pos1, pos2):
        line = Line(pos1, pos2)
        self.lines.append(line)
        self.add(line)
    
    def collide(self, point, vector):
        closest = None
        for line in self.lines:
            if line in self:
                temp = line.hit(point, vector)
                if temp:
                    if not closest:
                        closest = temp
                    elif abs(temp[0][0] - point[0]) + abs(temp[0][1] - point[1]) < abs(closest[0][0] - point[0]) + abs(closest[0][1] - point[1]):
                        closest = temp
                    elif int(abs(temp[0][0] - point[0]) + abs(temp[0][1]) - point[1]) == int(abs(closest[0][0] - point[0]) + abs(closest[0][1] - point[1])):
                        temp = (temp[0], temp[1] + closest[1])
                        closest = temp
            else:
                self.lines.remove(line)
        return closest
        
    def kill_all(self, point):
        for line in self.lines[:]:
            if line.points()[0] == point or line.points()[1] == point:
                line.kill()
                self.lines.remove(line)
                
                
class Line(pygame.sprite.DirtySprite):
    
    def __init__(self, pos1, pos2):
        pygame.sprite.DirtySprite.__init__(self)
        
        if pos1[1] > pos2[1]:
            temp = pos1
            pos1 = pos2
            pos2 = temp
        
        self.line_seg = Line_Segment(pos1,pos2)
        #vertical line
        if pos1[0] == pos2[0]:
            self.image = pygame.Surface( (3, abs(self.line_seg.y_length())) )
            self.image.fill( [125,125,125] )
            self.rect = self.image.get_rect()
            
            pygame.draw.line(self.image, [0,0,175],
                            (1,0),
                            (1, self.rect.bottom), 3)
            pygame.draw.line(self.image, [0,255,255],
                             (1,0),
                             (1, self.rect.bottom), 1)
            self.rect.left = min(pos1[0], pos2[0])
            self.rect.top = pos1[1] - 1
        #horizontal line
        elif pos1[1] == pos2[1]:
            self.image = pygame.Surface( (abs(self.line_seg.x_length()), 5 ) )
            self.image.fill( [125,125,125] )
            self.rect = self.image.get_rect()
            
            pygame.draw.line(self.image, [0,0,175],
                            (0,1),
                            (self.rect.right, 1), 3)
            pygame.draw.line(self.image, [0,255,255],
                             (0,1),
                             (self.rect.right, 1), 1)
            self.rect.left = pos1[0] - 1
            self.rect.top = min(pos1[1], pos2[1])
            
        else:
            self.image = pygame.Surface( (abs(self.line_seg.x_length()), abs(self.line_seg.y_length())) )
            self.image.fill( [125,125,125] )
            self.rect = self.image.get_rect()
            
            if pos1[0] < pos2[0]:
                pygame.draw.line(self.image, [0,0,175],
                                 (0,0),
                                 (self.rect.right, self.rect.bottom), 4)
                pygame.draw.line(self.image, [0,255,255],
                                 (0,0),
                                 (self.rect.right, self.rect.bottom), 2)
                self.rect.top = pos1[1]
                self.rect.left = pos1[0]
            else:
                pygame.draw.line(self.image, [0,0,175],
                                 (self.rect.right,0),
                                 (0, self.rect.bottom), 4)
                pygame.draw.line(self.image, [0,255,255],
                             (self.rect.right,0),
                             (0, self.rect.bottom), 2)
                self.rect.top = pos1[1]
                self.rect.left = pos2[0]
        self.image.set_colorkey( [125,125,125] )
        self.dirty = 1
        
    def points(self):
        return self.line_seg.points()
        
    def hit(self, pos, vector):
        """
        --> tuple
        Returns the position and reflection vector as a tuple (pos, vector),
         or if there is no unique point of intersection returns None
            pos(tuple)     --> The origin of the object before movement
            vector(Vector) --> The movement vector of the object
        """
        return self.line_seg.hit(pos, vector)
        
        
        
if __name__ == "__main__":
    from math import degrees
    x = Line( (0,0), (4.6025242672622015, 1.9536556424463689) )
    yx = Vector()
    yx.from_points( (0,0), (4.6025242672622015, 1.9536556424463689) )
    print degrees(yx.get_angle())
    y = Vector()
    y.from_points( (- 2,-2 ), (.5881904510252074,7.6592582628906829) )
    print degrees(y.get_angle())
    print "expected 331"
    print degrees(x.hit( (0,-2), y )[1].get_angle())
            