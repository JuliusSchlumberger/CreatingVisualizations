from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from Paper3_v1.main_central_path_directions import FILE_PATH_ALL_PATHWAYS_SECTORS, MEASURE_LOGOS
from Paper3_v1.scripts.utilities.map_system_parameters import INVERTED_MEASURE_NUMBERS
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def getImage(local_path):
    img = Image.open(local_path)
    return OffsetImage(np.array(img), zoom=0.03)

def add_logos(axes):

    ytick_labels = axes.get_yticklabels()
    print('test', ytick_labels)
    for ytick in ytick_labels:
        _, y_pos = ytick.get_position()
        ylabel = ytick.get_text()
        if ylabel == 'current':
            pass
        else:
            # image_positions = axes1.get_ylabelticks()
            img_path = MEASURE_LOGOS[INVERTED_MEASURE_NUMBERS[int(ylabel)]]
            imagebox = getImage(img_path)
            ab = AnnotationBbox(imagebox, (-0.1, y_pos),
                                xybox=(0, 0),
                                xycoords=("axes fraction", "data"),
                                boxcoords="offset points",
                                box_alignment=(0, .5),  # Align logos to the bottom
                                bboxprops={"edgecolor": "none"}, frameon=False)
            axes.add_artist(ab)
    # Set new labels, keeping 'current' and replacing others with ''
    current_labels = [label.get_text() for label in axes.get_yticklabels()]
    new_labels = ['' if label != 'current' else 'current' for label in current_labels]

    # Apply the new labels
    axes.set_yticklabels(new_labels)

    return axes