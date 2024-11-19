from PIL import Image

def get_rgb_values(image_path):
    """Gets RGB values for each pixel in an image.

    Args:
        image_path: Path to the image file.

    Returns:
        A list of tuples, where each tuple contains the RGB values (R, G, B) of a pixel.
    """

    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure the image is in RGB mode
    pixels = img.getdata()

    return list(pixels)

# Example usage
image_path = "/Users/vidursanghi/Desktop/colorBlindTransform/rubberduck112.jpg"
rgb_values = get_rgb_values(image_path)
print(rgb_values) 