from PIL import Image, ImageOps
from scripts.design_choices.main_dashboard_design_choices import MEASURE_COLORS, MEASURE_NUMBERS
import pathlib

def hex_to_rgb(hex_color):
    # Remove the '#' character and convert to integer from base 16
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def convert_to_black_and_white(input_path, output_path, hex_color):
    # Load the image
    img = Image.open(input_path)

    # Convert the image to grayscale
    img_gray = img.convert("L")

    # Convert the grayscale image to binary (black and white)
    # 128 is the threshold value; adjust it if necessary
    img_bw = img_gray.point(lambda x: 0 if x < 128 else 255, '1')

    # Save the black and white image
    img_bw.save(output_path)


def colorize_logos(logo_path,colour, new_logo_path):
    # Load the image
    original_image = Image.open(logo_path)

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(original_image)

    # Colorize the image - the example here colorizes the image to light blue
    # The first tuple defines the original color (black in grayscale),
    # and the second tuple defines the target color in (R, G, B) format.
    colorized_image = ImageOps.colorize(gray_image, black='white', white=colour)

    # Now you can save the colorized image or use it directly in Plotly
    colorized_image.save(new_logo_path)

# Continue to add this colorized image to your Plotly figure

for measure in MEASURE_NUMBERS:
    image_path = f'logos/{measure}.png'
    colour = MEASURE_COLORS[str(MEASURE_NUMBERS[measure])]
    # Example usage
    pathlib.Path('logos/black_white').mkdir(parents=True, exist_ok=True)
    convert_to_black_and_white(image_path,f'logos/black_white/{measure}.png', colour)
    pathlib.Path('logos/colorized').mkdir(parents=True, exist_ok=True)
    colorize_logos(f'logos/black_white/{measure}.png', colour, f'logos/colorized/{measure}.png')
