from PIL import Image, ImageDraw

def hex_to_rgb(hex_color):
    """ Convert hex color to RGB tuple """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def lighten_color(color, factor=0.7):
    """ Lighten the given color by blending it with white """
    r, g, b = hex_to_rgb(color)
    return (int(r + (255 - r) * factor), int(g + (255 - g) * factor), int(b + (255 - b) * factor), 255)


# Function to create pattern image
def create_pattern_image(color, pattern, size=(50, 50)):
    img = Image.new('RGB', size, color)
    light_color = lighten_color(color)
    draw = ImageDraw.Draw(img)
    if pattern == '/':
        for i in range(-size[0], size[0] + size[1], 15):
            draw.line((i, size[1], i + size[0], 0), fill=light_color, width=2)
    elif pattern == '.':
        for i in range(3, size[0], 10):
            for j in range(3, size[1], 10):
                draw.ellipse((i, j, i + 3, j + 3), fill=light_color, )
    return img