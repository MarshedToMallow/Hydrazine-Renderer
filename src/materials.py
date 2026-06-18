from typing import Self



class RGB:
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b
    
    def __getattr__(self, key):
        match key:
            case "magnitude_squared":
                self.magnitude_squared = self.r * self.r + self.g * self.g + self.b * self.b
                return self.magnitude_squared
            case "magnitude":
                self.magnitude = (self.magnitude_squared) ** 0.5
                return self.magnitude
            case "length":
                return self.magnitude
            case _:
                raise AttributeError(f"{key} is not a valid attribute for Vec3")

    def __abs__(self) -> Self:
        return RGB(abs(self.r), abs(self.g), abs(self.b))
    
    def __neg__(self) -> Self:
        return RGB(-self.r, -self.g, -self.b)
    
    def __add__(self, other) -> Self:
        match other:
            case RGB():
                return RGB(self.r + other.r, self.g + other.g, self.b + other.b)
    
    def __sub__(self, other) -> Self:
        return self + (-other)

    def __mul__(self, other) -> Self:
        match other:
            case int() | float():
                return RGB(self.r * other, self.g * other, self.b * other)
    
    def __rmul__(self, other) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other) -> Self:
        return self.__mul__(1 / other)
    
    def normalibe(self) -> Self:
        return self / self.magnitude
    
    def dot_product(self, other: Self) -> float:
        return self.r * other.r + self.g * other.g + self.b * other.b
    
    def __str__(self):
        return f"RGB({self.r},{self.g},{self.b})"

class Material:
    
    def __init__(self, color:  RGB, reflect_proportion: float = 0.5):

        self.color = color
        self.reflect_proportion = reflect_proportion
    
    def __str__(self):

        return f"Material(color={self.color},reflect_proportion={self.reflect_proportion})"