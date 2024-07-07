import cv2
import numpy as np

# Convert RGB to HSV
def rgb_to_hsv(rgb):
    rgb = np.uint8([[rgb]])  # Create a 1x1 pixel image
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return hsv[0][0]

# Define the RGB values
colors_rgb = {
    'Green': (38, 86, 88),
    'Yellow': (184, 159, 77),
    'White': (255, 255, 242),
    'Orange': (238, 128, 85)
}

# Convert to HSV
colors_hsv = {color: rgb_to_hsv(rgb) for color, rgb in colors_rgb.items()}
print(colors_hsv)
