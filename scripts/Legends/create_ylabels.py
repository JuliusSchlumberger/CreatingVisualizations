import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pathlib



def create_ylabels(ylabel_items, max_items_per_col=4, filepath="legends/vertical_legend.png"):
    num_cols = max_items_per_col
    num_rows = 1
    # Create the figure with a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(1.5 * num_cols, 2 * num_rows),)  # Adjust for image and text columns

    fig.patch.set_alpha(0.0)

    # Hide all axes
    for ax in axs.flat:
        ax.axis('off')

    for i, item in enumerate(ylabel_items):
        col = (i % max_items_per_col)  # Calculate column for image based on item index, adjusting for image/text pairing

        # Load and display the image, scaled and centered
        img = mpimg.imread(item['image_path'])
        axs[col].imshow(img)
        # Set the axes background to be transparent
        axs[col].patch.set_alpha(0.0)

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight',transparent=True, dpi=300)
    plt.close()