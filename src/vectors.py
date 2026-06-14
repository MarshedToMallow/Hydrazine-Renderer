class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __getattr__(self, key):
        match key:
            case "magnitude_squared":
                self.magnitude_squared = self.x * self.x + self.y * self.y + self.z * self.z
                return self.magnitude_squared
            case "magnitude":
                self.magnitude = (self.magnitude_squared) ** 0.5
                return self.magnitude
            case "length":
                return self.magnitude

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))
    
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    
    def __add__(self, other):
        match other:
            case Vec3():
                return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        match other:
            case int() | float():
                return Vec3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        return self.__mul__(1 / other)