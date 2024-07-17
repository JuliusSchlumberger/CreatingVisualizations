

# Function to define the color and pattern based on value
def get_bar_style(value, color):
    if value > 0:
        return dict(color=color, pattern_shape="-")
    elif value < 0:
        return dict(color=color, pattern_shape="/")
    else:
        return dict(color='grey')