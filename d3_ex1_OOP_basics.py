import math


class Vector:
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length

    def __repr__(self):
        return f"Vector({self.angle}, {self.length})"

    def __str__(self):
        return f"<{self.angle}, {self.length}>"


class Segment:
    def __init__(self, start: Point, end: Point):
        for p in start, end:
            if not isinstance(p, Point):
                raise ValueError("give me points!")

        self.start = start
        self.end = end

    def __repr__(self):
        return f"Segment({repr(self.start)}, {repr(self.end)})"

    def __str__(self):
        return f"[{self.start}, {self.end}]"

    def translate(self, dx, dy):
        self.start.translate(dx, dy)
        self.end.translate(dx, dy)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}{self.as_tuple()}"

    def __str__(self):
        return str(self.as_tuple())
    
    def as_tuple(self):
        return (self.x, self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        
        return self.as_tuple() == other.as_tuple()

    def __gt__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Unsuported operation")
        
        return self.as_tuple() > other.as_tuple()
    
    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Unsupported operation")
        
        return Vector(50, self.distance_between(self, other))

    @property
    def distance_from_origin(self):
        return self.distance_between(self, Point(0, 0))

    @staticmethod
    def distance_between(p1, p2):
        return math.sqrt(
            (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2
        )

    @classmethod
    def from_tuple(cls, tup):
        return cls(*tup)
    

class ThreeDPoint(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def as_tuple(self):
        return (self.x, self.y, self.z)

