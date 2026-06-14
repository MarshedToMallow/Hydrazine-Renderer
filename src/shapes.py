from enum import Enum

from vectors import Vec3
from materials import Material



class HitType(Enum):

    NO_HIT = 0          # No Intersections
    OUTSIDE_BEHIND = 1  # Intersection behind camera
    INSIDE = 2          # Camera inside object
    OUTSIDE_AHEAD = 3   # Intersection in front of camera

class HitInfo:

    def __init__(self, hit_type: HitType, t: None | float = None, normal_vector: None | Vec3 = None, material: None | Material = None):

        self.hit_type = hit_type
        self.t = t
        self.normal_vector = normal_vector

        self.material = material
    
    def __str__(self):
        match self.hit_type:
            case HitType.NO_HIT:
                return f"HitInfo({self.hit_type})"
            case _:
                return f"HitInfo({self.hit_type},{self.t},{self.normal_vector},{self.material})"



class Ray3D:

    def __init__(self, origin: Vec3, direction: Vec3):

        self.origin = origin
        self.direction = direction
    
    def get_point(self, t: float) -> Vec3:

        return self.origin + self.direction * t



class Sphere:
    
    def __init__(self, center: Vec3, radius: float, material: Material):

        self.center = center
        self.radius = radius
        self.radius_squared = radius * radius

        self.material = material
    
    # Sphere-Line intersection code from:
    #   https://stackoverflow.com/questions/5883169/intersection-between-a-line-and-a-sphere
    def get_hit_data(self, ray: Ray3D) -> HitInfo:
        """
        Returns the nearest distance t along the ray that the given ray intersects the sphere.

        Parameters:
            ray: Ray3D          - The ray to check intersection against
        
        Returns:
            HitInfo             - The information about the intersection
        
        Details:
            Todo
        """

        p0 = ray.origin
        p1 = ray.origin + ray.direction

        offset_a = p0 - self.center
        offset_b = p1 - self.center
        offset_c = p0 - p1

        # Solving a quadratic to find the intersection point
        #   x = (-b ± sqrt(b^2 - 4ac)) / (2a)

        A = offset_a.magnitude_squared - self.radius_squared

        # This would make it a linear equation, so maybe it's fine to just fallback on solving linear equations?  I'm not sure (also falling back on constants if B == 0)
        if A == 0:
            raise NotImplementedError("Can't solve sphere-ray intersections resulting in a quadratic where A == 0")

        C = offset_c.magnitude_squared
        B = offset_b.magnitude_squared - self.radius_squared - A - C

        # The part in the square root of the quadratic formula
        #   b^2 - 4ac
        discriminant = B*B - 4*A*C

        # No Real Solutions
        if discriminant < 0:
            return HitInfo(HitType.NO_HIT)
        
        # One Real Solution (Square Root is 0, so + and - give the same answer)
        elif discriminant == 0:

            # Solution is positive
            #   The camera faces towards the point (facing sphere)
            if -B > 0:
                return HitInfo(HitType.OUTSIDE_AHEAD, -B / (2*A), None, self.material)
            # Solution is negative
            #   The camera faces away from the point (facing away from sphere)
            else:
                return HitInfo(HitType.OUTSIDE_BEHIND, -B / (2*A), None, self.material)
        
        # Two Real Solutions
        else:
            # Smaller solution is positive
            #   The camera faces towards both points (facing sphere)
            if -B - (root := discriminant**0.5) > 0:
                return HitInfo(HitType.OUTSIDE_AHEAD, (-B - root) / (2*A), None, self.material)
            
            # Only the larger solution is positive
            #   The camera faces towards one point and away from the other (inside sphere)
            elif -B + root > 0:
                return HitInfo(HitType.INSIDE, (-B + root) / (2*A), None, self.material)
            
            # Two Negative Solutions
            #   The camera faces away from both points (facing away from sphere)
            else:
                return HitInfo(HitType.OUTSIDE_BEHIND, (-B + root) / (2*A), None, self.material)