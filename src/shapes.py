from vectors import Vec3
from materials import Material, RGB



class HitType:

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
    
    def __str__(self):

        return f"Ray3D(origin={self.origin},direction={self.direction})"



class Sphere:
    
    def __init__(self, center: Vec3, radius: float, material: Material):

        self.center = center
        self.radius = radius
        self.radius_squared = radius * radius

        self.material = material
    
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

        A = ray.direction.magnitude_squared

        B = 2 * (
            ray.direction.x * (ray.origin.x - self.center.x)
            + ray.direction.y * (ray.origin.y - self.center.y)
            + ray.direction.z * (ray.origin.z - self.center.z)
        )

        C = (ray.origin - self.center).magnitude_squared - self.radius_squared

        discriminant = B*B - 4*A*C

        if discriminant < 0:
            return HitInfo(HitType.NO_HIT)
        
        elif discriminant == 0:
            t = -B / (2*A)

            if t < 0:
                return HitInfo(HitType.NO_HIT)

            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(HitType.OUTSIDE_AHEAD, t, normal, self.material)
        
        root = discriminant ** 0.5

        if (t := (-B - root) / (2*A)) > 0:
            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(HitType.OUTSIDE_AHEAD, t, normal, self.material)
        
        elif (t := (-B + root) / (2*A)) > 0:
            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(HitType.OUTSIDE_AHEAD, t, normal, self.material)

        return HitInfo(HitType.NO_HIT)