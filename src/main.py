from alive_progress import alive_bar
from itertools import product
from PIL import Image



WIDTH, HEIGHT = 1920, 1080
RATIO = WIDTH / HEIGHT

NEAR_PLANE = 0.01
FAR_PLANE = 100



def get_color(viewport_x: float, viewport_y: float) -> tuple[float, float, float]:
    """
    Takes a given viewport position and returns the corresponding RGB color

    Parameters:
        viewport_x: float
        viewport_y: float
    
    Return:
        tuple[
            float, = red channel [0.0,1.0]
            float, = green channel [0.0,1.0]
            float = blue channel [0.0,1.0]
        ] = RGB color
    """

    # Red Circle (Trivial logic to simulate an unshaded red sphere)
    if viewport_x ** 2 + viewport_y ** 2 <= 0.1:
        return (1.0, 0.0, 0.0)

    # Sky color (Default, blue)
    return (0.5, 0.5, 1.0)



image = Image.new("RGB", (WIDTH, HEIGHT))

with alive_bar(WIDTH * HEIGHT) as bar:
    for pixel_x, pixel_y in product(range(WIDTH), range(HEIGHT)):

        viewport_x = pixel_x / HEIGHT - (RATIO / 2)
        viewport_y = pixel_y / HEIGHT - 0.5

        color = get_color(viewport_x, viewport_y)
        image.putpixel((pixel_x, pixel_y), tuple([int(channel * 255) for channel in color]))
        
        bar() # Must be triggered once per iteration for the progress bar

image.show()