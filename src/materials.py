from vectors import Vec3



class RGB(Vec3):
    def __init__(self, r: float, g: float, b: float):
        super().__init__(r, g, b)
        self.r = r
        self.g = g
        self.b = b

class Material:
    
    def __init__(self, color:  RGB):
        
        self.color = color