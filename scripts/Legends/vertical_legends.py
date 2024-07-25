import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scripts.map_system_parameters import MEASURE_DICT
from scripts.Legends.insert_linebreaks import insert_linebreak
import matplotlib.patches as patches
import pathlib



def create_vertical_legend_with_images(legend_items, max_items_per_col=4, filepath="legendvertical_legend.png"):
    # Determine the number of rows and columns
    num_items = len(legend_items)
    num_cols = max_items_per_col * 2
    num_rows = np.ceil(num_items / max_items_per_col).astype(int)
    # Create the figure with a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4 * num_cols, 2 * num_rows),
                            # Adjust figure size as needed
                            gridspec_kw={
                                'width_ratios': [1, 3] * min(max_items_per_col,num_items)})  # Adjust for image and text columns
    # Hide all axes
    for ax in axs.flat:
        ax.axis('off')

    for i, item in enumerate(legend_items):
        col = (i % max_items_per_col) * 2  # Calculate column for image based on item index, adjusting for image/text pairing
        row = np.floor(i / max_items_per_col).astype(int)  # Calculate row
        # Load and display the image, scaled and centered
        img = mpimg.imread(item['image_path'])
        if num_rows == 1:
            axs[col].imshow(img)
            text = insert_linebreak((f"{MEASURE_DICT[item['name']]}"))

            # Set the text for the item
            axs[col + 1].text(0, 0.5, text, va='center', ha='left',size=30)  # Adjust text alignment as needed
        else:
            axs[row, col].imshow(img)
            text = insert_linebreak((f"{MEASURE_DICT[item['name']]}"))
            # Set the text for the item
            axs[row, col + 1].text(0, 0.5, text, va='center', ha='left', size=30)  # Adjust text alignment as needed
    # Draw a rectangle around the figure
    rect = patches.Rectangle((0.1, 0), .82, 1.1, linewidth=2, edgecolor='grey', facecolor='none', transform=fig.transFigure,
                             clip_on=False)
    fig.patches.append(rect)
    # Add the 'Legend' annotation in the top left corner
    plt.text(0.11, 1.06, 'Button explanation', transform=fig.transFigure, fontsize=35, va='top', ha='left')


    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight', dpi=600)
    plt.close()