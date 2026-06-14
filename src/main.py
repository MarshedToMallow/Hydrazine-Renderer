from alive_progress import alive_bar
from itertools import product
from PIL import Image

from vectors import Vec3
from materials import RGB, Material
from shapes import HitType, Ray3D, Sphere


# Image Constants
ASPECT_RATIO = 16 / 9
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = round(IMAGE_WIDTH / ASPECT_RATIO)

# Camera Constants
VIEWPORT_HEIGHT = 2
VIEWPORT_WIDTH = VIEWPORT_HEIGHT * ASPECT_RATIO
FOCAL_LENGTH = 1

ORIGIN = Vec3(0, 0, 0)
HORIZONTAL = Vec3(VIEWPORT_WIDTH, 0, 0)
VERTICAL = Vec3(0, VIEWPORT_HEIGHT, 0)
LOWER_LEFT_CORNER = ORIGIN - HORIZONTAL / 2 - VERTICAL / 2 - Vec3(0, 0, FOCAL_LENGTH)

SKY_COLOR = RGB(0.5, 0.5, 1.0)
SHAPES = [Sphere(Vec3(0, 0, -4), 0.5, Material(RGB(1.0, 0.0, 0.0)))]



def get_color(ray: Ray3D) -> RGB:
    """
    Takes a given pixel ray and returns the corresponding RGB color

    Parameters:
        ray: Ray3D
    
    Return:
        tuple[
            float, = red channel [0.0,1.0]
            float, = green channel [0.0,1.0]
            float = blue channel [0.0,1.0]
        ] = RGB color
    """

    nearest = None

    for shape in SHAPES:

        hit = shape.get_hit_data(ray)

        if nearest == None or nearest.hit_type == HitType.NO_HIT:
            nearest = hit
        elif nearest.t <= 0 and hit.t > 0:
            nearest = hit
        elif nearest.t > hit.t:
            nearest = hit

    # Hit nothing
    if nearest == None:
        return SKY_COLOR
    # Hit nothing
    elif nearest.hit_type == HitType.NO_HIT:
        return SKY_COLOR
    
    # No material assigned to closest
    elif nearest.material == None:
        return SKY_COLOR
    
    # Hit something and it has a material
    else:
        return nearest.material.color



image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

with alive_bar(IMAGE_WIDTH * IMAGE_HEIGHT) as bar:
    for pixel_x, pixel_y in product(range(IMAGE_WIDTH), range(IMAGE_HEIGHT)):

        u = pixel_x / (IMAGE_WIDTH - 1)
        v = pixel_y / (IMAGE_HEIGHT - 1)

        ray = Ray3D(ORIGIN, LOWER_LEFT_CORNER + u * HORIZONTAL + v * VERTICAL - ORIGIN)

        color = get_color(ray)
        r, g, b = color.r, color.g, color.b
        color = int(r * 255), int(g * 255), int(b * 255)
        image.putpixel((pixel_x, pixel_y), color)
        
        bar() # Must be triggered once per iteration for the progress bar

image.show()