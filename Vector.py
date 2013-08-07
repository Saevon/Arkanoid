import math
class Vector(object):
    """
    A class that models a 2D vector, with a velocity and angle
    """
    
    def __init__(self, velocity = 0, angle = 0):
        """
        --> None
        Creates a new Vector object, with a velocity and angle
            velocity(float) --> the length of the Vector
            angle(float)    --> The angle in radians from the point (1,0) rotating CounterClockwise
        """
        self.velocity = float(velocity)
        self.angle = float(angle)
        
    def __add__(self, other):
        """
        self + other
        --> Vector
        Adds the two Vectors together
        """
        
        dx = self.dx() + other.dx()
        dy = self.dy() + other.dy()
        new = Vector()
        new.__set_dx_dy(dx,dy)
        return new
    
    def __iadd__(self, other):
        """
        self += other
        Changes self to be the sum of the two Vectors
        """
        dx = self.dx() + other.dx()
        dy = self.dy() + other.dy()
        self.__set_dx_dy(dx,dy)
    
    def __mul__(self, other):
        """
        self * other
        --> Vector
        Multiplies the vector by a float or int value
        """
        new = Vector(self.velocity * other, self.angle)
        return new
    
    def __str__(self):
        """
        str(Vector)
        --> str
        Returns the str representation of a Vector in the form length[angle]
        """
        return "%.2f[%.2f]" % (self.velocity, self.angle)
        
    def dx(self):
        """
        --> float
        Returns the horizontal component of the Vector as a float
        """
        return self.velocity * math.cos(self.angle)
    
    def dy(self):
        """
        --> float
        Returns the vertical component of the Vector as a float
        """
        return self.velocity * math.sin(self.angle)
    
    def set_dx(self, dx):
        """
        --> None
        Sets the Horizontal component of the Vector
            dx(float) --> new x component of the Vector
        """
        x_velo = dx
        y_velo = self.dy()
        self.__set_dx_dy(x_velo,y_velo)
        
    def set_dy(self, dy):
        """
        --> None
        Sets the vertical component of the Vector
            dx(float) --> new x component of the Vector
        """
        x_velo = self.dx()
        y_velo = dy
        self.__set_dx_dy(x_velo,y_velo)
        
    def __set_dx_dy(self, dx, dy):
        """
        --> None
        Changes the Vector according to components
            dx(float) --> new x component of the Vector
            dy(float) --> new y component of the Vector
        """
        self.velocity = math.sqrt(dx ** 2.0 + dy ** 2.0)
        if self.velocity == 0.0:
            self.angle = 0.0
        else:
            self.angle = math.acos(dx / self.velocity)
        if dy < 0:
            self.angle = math.radians(360) - self.angle        
       
    def get_velocity(self):
        """
        --> float
        Returns the velocity of the Vector as a float
        """
        return self.velocity
    
    def set_velocity(self, velocity):
        """
        --> None
        Changes the velocity or length of the Vector
            velocity(float) --> New Vector length
        """
        self.velocity = velocity
        
    def get_angle(self):
        """
        --> float
        Returns the angle of the Vector as a float in radians
        """
        return self.angle
    
    def set_angle(self, angle):
        """
        --> None
        Changes the angle of the Vector
            angle(float) --> New Vector angle in radians
        """
        self.angle = angle
    
    def from_points(self, point1, point2):
        """
        --> None
        Changes the Vector to a Vector going from point A to point B
            point1(list) --> (x,y) Point A
            point2(list) --> (x,y) Point B
        """
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        self.__set_dx_dy(dx,dy)
    
    def copy(self):
        """
        --> Vector
        Creates a copy of the vector and returns a reference to it
        """
        return Vector(self.velocity, self.angle)
        
if __name__ == "__main__":
    vector1 = Vector(100, math.radians(180))
    print vector1.dx(), vector1.dy()
    
    vector2 = Vector(100, math.radians(0))
    vector2.set_dy(20)
    print vector2.dx(), vector2.dy()
    
    vector3 = vector1 + vector2
    print vector3.dx(), vector3.dy()
    
    vector4 = Vector()
    vector4.from_points( (0,0), (-4,4) )
    print math.degrees(vector4.angle)
    vector4.from_points( (0,0), (0,-4) )
    print vector4.velocity
