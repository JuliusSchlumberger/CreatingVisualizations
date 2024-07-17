import matplotlib.pyplot as plt

# Function to create a custom colorscale
def create_custom_colorscale(df):
    unique_values = df['Color'].unique()
    real_numbers = [0] + [val for val in unique_values if val < 1000]
    real_numbers = sorted(set(real_numbers))
    max_value = max(real_numbers)

    viridis = plt.get_cmap('viridis', len(real_numbers))

    custom_colorscale = []
    custom_colorscale.append([0.0, 'grey'])

    for i, val in enumerate(real_numbers):
        color = viridis(i / (len(real_numbers)))
        custom_colorscale.append(
            [(val + 3) / (max_value + 3), f'rgb({color[0] * 255}, {color[1] * 255}, {color[2] * 255})'])
    # if 1000 in unique_values:
    #     custom_colorscale.append([0.0, 'pink'])
    color_values = df['Color'].apply(lambda x: 0.0 if x == 1000 else (x + 3) / (max_value + 3))
    return color_values, custom_colorscale