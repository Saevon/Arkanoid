import math
from Vector import Vector
class Line_Segment(object):
    """
    An object which models a line segment on a cartesian plane
    """
    
    def __init__(self, point1 = (0,0), point2 = (0,0)):
        """
        Creates a Line_Segment
            point1(list)  --> (x,y) The starting point of the line segment
            point2(list)  --> (x,y) The ending point of the line segment
            
            Note: points 1 & 2 are interchangable
        """
        self.point1 = point1
        self.point2 = point2
        
    def points(self):
        """
        --> tuple
        Returns the starting and ending points
        Form: (point1, point2)
        """
        return (self.point1, self.point2)
        
    def y_length(self):
        """
        --> float
        Returns the y length of the line, from point 1 to point 2 (can be negative)
        """
        return float(self.point1[1] - self.point2[1])
    
    def x_length(self):
        """
        --> float
        Returns the x length of the line, from point 1 to point 2 (can be negative)
        """
        return float(self.point1[0] - self.point2[0])
        
    def length(self):
        """
        --> float
        returns the length of the line
        """
        return math.sqrt(self.y_length ** 2.0 + self.x_length **2.0)
    
    def equation(self):
        """
        --> tuple
        Returns the linear equation, in the form ax + by + c
            Returns (a, b ,c)
        """
        if self.y_length() == 0 and self.x_length() == 0:
            return (0,0,0)
        elif self.y_length() == 0:
            return (0, -1, self.point1[1])
        elif self.x_length() == 0:
            return (1, 0, -1 * self.point1[0])
        a = self.y_length()  / self.x_length()
        b = -1
        c = - 1 * (a) * self.point1[0] + self.point1[1]
        return (a,b,c)
    
    def intersect(self, other):
        """
        --> tuple
        Returns the unique point of intersection between two line segments in the form (x,y)
        or Returns None if it doesnt exist (Note: equal lines do not have a unique point of intersection)
        """
        temp1 = self.equation()
        temp2 = other.equation()
        
        bottom = temp1[0] * temp2[1] - temp1[1] * temp2[0]
        if bottom == 0:
            return None
        x = (-1 * temp1[2] * temp2[1] + temp1[1] * temp2[2]) / bottom
        y = (-1 * temp1[0] * temp2[2] + temp1[2] * temp2[0]) / bottom
        
        if (x >= min(self.point1[0], self.point2[0]) and x <= max(self.point1[0], self.point2[0]) and
            y >= min(self.point1[1], self.point2[1]) and y <= max(self.point1[1], self.point2[1]) and
            x >= min(other.point1[0], other.point2[0]) and x <= max(other.point1[0], other.point2[0]) and
            y >= min(other.point1[1], other.point2[1]) and y <= max(other.point1[1], other.point2[1])):
            return (x,y)
        
    def hit(self, pos, vector):
        """
        --> tuple
        Returns the position and reflection vector as a tuple (pos, vector),
         or if there is no unique point of intersection returns None
            pos(tuple)     --> The origin of the object before movement
            vector(Vector) --> The movement vector of the object
        """
            
        new_vector = vector.copy()
        other = Line_Segment( pos, (pos[0] + new_vector.dx(), pos[1] + new_vector.dy()) )
        if other.intersect(self):
            self_vector = Vector()
            self_vector.from_points(self.points()[0], self.points()[1])
            angle = self_vector.get_angle()
            new_vector.set_angle( new_vector.get_angle() - angle)
            new_vector.set_dy( new_vector.dy() * -1 )
            new_vector.set_angle( angle + new_vector.get_angle())
            new_vector.set_velocity( vector.get_velocity() )
            return (other.intersect(self), new_vector)
        
        
if __name__ == "__main__":
    x1 = Line_Segment((-5,0), (0,5))
    print x1.equation()
    
    x2 = Line_Segment((2,-2.77777777), (-5,3.444444))
    print x2.equation()
    
    print x1.intersect(x2)
    
    x1 = Line_Segment((-5,5), (0,0))
    
    x2 = Line_Segment((2,-2), (-2,2))
    
    print x1.intersect(x2)