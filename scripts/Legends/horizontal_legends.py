import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scripts.map_system_parameters import MEASURE_DICT
from scripts.Legends.insert_linebreaks import insert_linebreak
import matplotlib.patches as patches


def create_horizontal_legend_with_images(legend_items, max_items_per_col=2, filepath="horizontal_legend.png"):
    num_items = len(legend_items)
    num_cols = 2
    num_rows = num_items
    # Create the figure with a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 2*6),
                            # Adjust figure size as needed
                            gridspec_kw={
                                'width_ratios': [1, 4]})  # Adjust for image and text columns
    # Hide all axes
    for ax in axs.flat:
        ax.axis('off')

    for i, item in enumerate(legend_items):
        # Load and display the image, scaled and centered
        img = mpimg.imread(item['image_path'])

        axs[i, 0].imshow(img)
        text = insert_linebreak((f"{MEASURE_DICT[item['name']]}"))

        # Set the text for the item
        axs[i, 1].text(0, 0.5, text, va='center', ha='left', size=30)  # Adjust text alignment as needed
    # Draw a rectangle around the figure
    rect = patches.Rectangle((0.1, 0.1), .8, .87, linewidth=2, edgecolor='grey', facecolor='none', transform=fig.transFigure,
                             clip_on=False)
    fig.patches.append(rect)
    # Add the 'Legend' annotation in the top left corner
    plt.text(0.15, .95, 'Button explanation', transform=fig.transFigure, fontsize=35, va='top', ha='left')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight', dpi=600)

    plt.close()