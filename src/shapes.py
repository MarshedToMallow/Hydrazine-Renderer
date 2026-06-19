from vectors import Vec3
from materials import Material, RGB



class HitInfo:

    def __init__(
        self,
        t: None | float = None,
        normal_vector: None | Vec3 = None,
        material: None | Material = None
    ):

        self.t = t
        self.normal_vector = normal_vector
        self.material = material
    
    def __str__(self):
        return f"HitInfo({self.t},{self.normal_vector},{self.material})"



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
    
    def get_hit_data(self, ray: Ray3D) -> None | HitInfo:
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

        if A == 0:
            if B == 0:
                raise NotImplementedError("If A == B == 0 then either C == 0 and all values of t are valid or C != 0 and no values of t are valid")
            
            if (t := -C / B) < 0:
                return None
            
            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(t, normal, self.material)

        if (discriminant := B*B-4*A*C) < 0:
            return None
        
        elif discriminant == 0:
            t = -B / (2*A)

            if t < 0:
                return None

            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(t, normal, self.material)
        
        root = discriminant ** 0.5

        if (t := (-B - root) / (2*A)) > 0:
            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(t, normal, self.material)
        
        elif (t := (-B + root) / (2*A)) > 0:
            normal = (ray.get_point(t) - self.center).normalize()
            return HitInfo(t, normal, self.material)

        return None