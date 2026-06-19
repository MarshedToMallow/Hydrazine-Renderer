from alive_progress import alive_bar
from itertools import product
from PIL import Image
from random import random, seed
from colorsys import hls_to_rgb

from vectors import Vec3
from materials import RGB, Material
from shapes import Ray3D, Sphere

seed(0)



# Image Constants
ASPECT_RATIO = 16 / 9
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = round(IMAGE_WIDTH / ASPECT_RATIO)

ORIGIN = Vec3(0, 0, 0)

PIXEL_WIDTH = 1 / (IMAGE_WIDTH - 1)
PIXEL_HEIGHT = 1 / (IMAGE_HEIGHT - 1)

# Ray Constants
SAMPLES = 10**2
BOUNCES = 5

SKY_COLOR = RGB(0.5, 0.5, 1.0)
DEBUG_COLOR = RGB(1.0, 0.0, 1.0) * SAMPLES

# Scene Shapes
#SHAPES = [
#    Sphere(Vec3(0, 0, -4), 0.5, Material(RGB(1.0, 0.0, 0.0), 0.5)),
#    Sphere(Vec3(2, 0.5, -3), 1.2, Material(RGB(0.0, 1.0, 0.5), 0.2)),
#    Sphere(Vec3(0.1, 1.5, -2), 0.4, Material(RGB(1.0, 1.0, 1.0), 0.7)),
#    Sphere(Vec3(0, 50, -10), 10, Material(RGB(100.0, 100.0, 100.0), 0.0))
#]

#SHAPES = []
#
#for i in range(5):
#
#    x = 2 * i - 4
#    r = 0.2 * i
#
#    color = [0.75, 0.75, 0.75]
#
#    position = Vec3(x, 0, -5)
#    radius = 0.75
#    material = Material(RGB(*color), r)
#
#    SHAPES.append(Sphere(position, radius, material))

#SHAPES = [
#    Sphere(Vec3(1, 0, -2), 1, Material(RGB(1, 1, 1), 0.5)),
#    Sphere(Vec3(-2, 0, -3), 1, Material(RGB(1, 1, 1), 0))
#]

SHAPES = [
    Sphere(Vec3(0, 0, -10), 1, Material(RGB(1, 0, 0), 0.5)),
    Sphere(Vec3(0, 20, -10), 15, Material(RGB(1, 1, 1), 0))
]



def get_sky_color(ray: Ray3D) -> RGB:
    return SKY_COLOR



def get_color(ray: Ray3D, bounces: int = BOUNCES, default_color: RGB = SKY_COLOR, previous_shape: None | Sphere = None) -> RGB:
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

    if bounces == 0:
        return default_color

    nearest = None
    nearest_shape = None

    for shape in SHAPES:

        if type(shape) in [Sphere] and shape == nearest_shape:
            continue

        if (hit := shape.get_hit_data(ray)) == None:
            continue

        elif nearest == None or nearest.t > hit.t:
            nearest = hit
            nearest_shape = shape

    # Hit nothing
    if nearest == None:
        return get_sky_color(ray)
    
    # Hit something
    else:

        multiplier = nearest.material.reflect_proportion

        reflect_origin = ray.get_point(nearest.t)
        reflect_direction = nearest.normal_vector.reflect(ray.direction)
        reflected_ray = Ray3D(reflect_origin, reflect_direction)

        if nearest.material.reflect_proportion != 0:
            reflected_color = get_color(reflected_ray, bounces - 1, previous_shape=nearest_shape)
        else:
            reflected_color = RGB(0, 0, 0)

        return reflected_color * multiplier + nearest.material.color * (1 - multiplier)



print(f"Scene Stats:")
print(f"\tResolution: {IMAGE_WIDTH:,}x{IMAGE_HEIGHT:,} ({IMAGE_WIDTH * IMAGE_HEIGHT:,} Total Pixels)")
print(f"\tSamples per Pixel: {SAMPLES:,}")
print(f"\tMaximum Bounces per Sample: {BOUNCES:,}")
print(f"\tScene Objects: {len(SHAPES):,}")

if input("Start rendering? [Y/n] ").lower() not in ["", "y"]:
    print("Cancelling...")
    exit()

image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

with alive_bar(IMAGE_WIDTH * IMAGE_HEIGHT) as bar:
    for pixel_x, pixel_y in product(range(IMAGE_WIDTH), range(IMAGE_HEIGHT)):

        u = pixel_x / (IMAGE_HEIGHT - 1) - (IMAGE_WIDTH / (2 * IMAGE_HEIGHT))
        v = (IMAGE_HEIGHT - pixel_y - 1) / (IMAGE_HEIGHT - 1) - 0.5

        color = RGB(0.0, 0.0, 0.0)

        for _ in range(SAMPLES):

            ray = Ray3D(
                ORIGIN,
                Vec3(
                    u + PIXEL_WIDTH * (random() - 0.5),
                    v + PIXEL_HEIGHT * (random() - 0.5),
                    -1
                ).normalize()
            )

            #ray = Ray3D(
            #    ORIGIN,
            #    LOWER_LEFT_CORNER
            #    + (u + (PIXEL_WIDTH * (random() - 0.5))) * HORIZONTAL
            #    + (v + (PIXEL_HEIGHT * (random() - 0.5))) * VERTICAL
            #    - ORIGIN
            #)

            sample_color = get_color(ray)
            color += sample_color

        color /= SAMPLES
        r, g, b = color.r, color.g, color.b
        color = int(r * 255), int(g * 255), int(b * 255)

        image.putpixel((pixel_x, pixel_y), color)
        
        bar() # Must be triggered once per iteration for the progress bar

print("Rendering Complete!")

image.show()