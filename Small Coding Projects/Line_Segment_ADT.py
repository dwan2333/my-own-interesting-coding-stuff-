class LineSeg:

    import math

    # construct two endpoint of the line 
    def __init__(self, ptA, ptB):
        self._ptA = ptA
        self._ptB = ptB

    # return Cartesian coordinate of point A 
    def endPointA(self):
        return self._ptA

    # return Cartesian coordinate of point B 
    def endPointB(self):
        return self._ptB

    # return the length of the line segement given by two endpoint 
    def length(self):
        math = self.math
        return math.sqrt((self._ptB[0] - self._ptA[0])**2 + (self._ptB[1] - self._ptA[0])**2)

    # return string representation of the line segment 
    def toString(self):
        return f'({self._ptA[0]}, {self._ptA[1]})#({self._ptB[0], self._ptA[1]})'

    # return Bool to determine if the line segment is vertical 
    def isVertical(self): 
        if self._ptA[0] == self._ptB[0]:
            return True
        else:
            return False 

    # return Bool to determine if the line is horizontal
    def isHorizontal(self):
        if self._ptA[1] == self._ptB[1]:
            return True
        else:
            return False 

    # return the slope of the line 
    def slope(self):
        math = self.math 
        if self.isVertical():
            return None 
        else:
            return (self._ptB[1] - self._ptA[1]) / \
                (self._ptB[0] - self._ptA[0])

    # return Bool for if the otherline is parallel 
    def isParallel(self,otherline):
        if self.slope ==  otherline.slope: 
            return True 
        else:
            return False 

    # return Bool for if it is perpendicular 
    def isPerpendicular(self, otherline):
        if -1 / self.slope == otherline:
            return True
        else:
            return False 

    # return Bool if line intersect with otherline
    def midpoint(self):
        midx = (self._ptB[0] - self._ptA[0]) / 2
        midy = (self._ptB[1] - self._ptA[0]) / 2
        return tuple((midx, midy))

    # return Bool if otherline bisects bisects the line 
    def bisects(self, otherLine):
        if self.isPerpendicular(otherLine) and self.midpoint() == otherLine.midpoint():
            return True
        else:
            return False 

    # return Bool if the line intersects with otherline
    def intersects(self, otherline):

        # if two line are parallel then they 100 percent not intersect with each other 
        if self.isParallel(otherline):
            return False

        # Find the intersection point (intersect_x, intersect_y)
        if self.isVertical():
            # self is vertical, otherline is not
            m2 = otherline.slope()
            b2 = otherline._ptA[1] - (m2 * otherline._ptA[0])
            
            intersect_x = self._ptA[0]
            intersect_y = (m2 * intersect_x) + b2

        elif otherline.isVertical():
            # otherline is vertical, self is not
            m1 = self.slope()
            b1 = self._ptA[1] - (m1 * self._ptA[0])
            
            intersect_x = otherline._ptA[0]
            intersect_y = (m1 * intersect_x) + b1

        else:
            # Neither is vertical, safe to use y = mx + b for both
            m1 = self.slope()
            m2 = otherline.slope() 
            # Note: b = y - mx. You accidentally used ptA for y and ptB for x previously!
            b1 = self._ptA[1] - (m1 * self._ptA[0])
            b2 = otherline._ptA[1] - (m2 * otherline._ptA[0])
            
            intersect_x = (b2 - b1) / (m1 - m2)
            intersect_y = (m1 * intersect_x) + b1

        # Now we check if the intersection point lies within the bounding box of BOTH segments
        self_min_x = min(self._ptA[0], self._ptB[0])
        self_max_x = max(self._ptA[0], self._ptB[0])
        self_min_y = min(self._ptA[1], self._ptB[1])
        self_max_y = max(self._ptA[1], self._ptB[1])

        other_min_x = min(otherline._ptA[0], otherline._ptB[0])
        other_max_x = max(otherline._ptA[0], otherline._ptB[0])
        other_min_y = min(otherline._ptA[1], otherline._ptB[1])
        other_max_y = max(otherline._ptA[1], otherline._ptB[1])

        # Check if intersect_x is within both X ranges and Y ranges
        in_x_bounds = (self_min_x <= intersect_x <= self_max_x) and (other_min_x <= intersect_x <= other_max_x)
        in_y_bounds = (self_min_y <= intersect_y <= self_max_y) and (other_min_y <= intersect_y <= other_max_y)

        # To intersect, the point must be within the bounds for both x and y
        return in_x_bounds and in_y_bounds

        


        
