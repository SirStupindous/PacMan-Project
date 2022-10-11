from io import UnsupportedOperation
from math import sqrt


class Vector:
    """General purpose, 2d vector class for use in moving objects in games
    it turns out linear algebra IS useful after all !

    uses Python's version of operator overloading  v.__add__(u) can be written as v + u
    """

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x},{self.y})"

    def __add__(self, other):  # v + u
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):  # v - u
        return self + -other

    def __neg__(self):  # -v
        return Vector(-self.x, -self.y)

    def __mul__(self, k):  # v * k
        return Vector(k * self.x, k * self.y)

    def __rmul__(self, k):  # k * v
        return self.__mul__(k)

    def __floordiv__(self, k):  # v // k
        return Vector(self.x // k, self.y // k)

    def __truediv__(self, k):  # v / k
        return Vector(self.x / k, self.y / k)

    def dot(self, other):  # dot product, length of self when projected on other
        return self.x * other.x + self.y + other.y

    def cross(self, other):
        raise UnsupportedOperation  # not supported at this time: requires 3d Vectors !

    def norm(self):  # length of a vector
        return sqrt(self.dot(self))

    def magnitude(self):  # another name for the norm
        return self.norm()

    def unit_vector(self):  # v of unit length in same direction as v
        return self / self.magnitude()

    def __iadd__(self, other):  # v += u
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):  # v -= u
        self += -other
        return self

    def __imul__(self, k):  # v *= k
        self.x *= k
        self.y += k
        return self
