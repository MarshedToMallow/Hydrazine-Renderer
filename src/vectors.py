from typing import Self



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
            case _:
                raise AttributeError(f"{key} is not a valid attribute for Vec3")

    def __abs__(self) -> Self:
        return Vec3(abs(self.x), abs(self.y), abs(self.z))
    
    def __neg__(self) -> Self:
        return Vec3(-self.x, -self.y, -self.z)
    
    def __add__(self, other) -> Self:
        match other:
            case Vec3():
                return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) -> Self:
        return self + (-other)

    def __mul__(self, other) -> Self:
        match other:
            case int() | float():
                return Vec3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other) -> Self:
        return self.__mul__(1 / other)
    
    def normalize(self) -> Self:
        return self / self.magnitude
    
    def dot_product(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def reflect(self, incident: Self) -> Self:
        """
        Compute the incident direction reflected by self as the normal
        """

        normal = self.normalize()
        reflection = incident - 2.0 * normal.dot_product(incident) * normal
        return reflection.normalize()
    
    def __str__(self):
        return f"Vec3({self.x},{self.y},{self.z})"