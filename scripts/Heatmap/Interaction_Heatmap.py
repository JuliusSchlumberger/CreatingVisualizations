
import matplotlib.pyplot as plt
from Paper3_v1.main_central_path_directions import ROH_LIST
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import COLORSCALE_HEATMAP
import base64
from io import BytesIO

import pandas as pd
import plotly.express as px
# from Paper3_helperfunctions import create_subfolder, multiply_with_factor, calculate_ratio, generate_hover_info,get_sorted_data, create_buttons
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.tri import Triangulation
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.gridspec as gridspec
import numpy as np


def Interaction_Heatmap(baseline_df, interaction_dict,risk_owner_hazard):

    fig, ax = plt.subplots(ncols=3, sharey=True,figsize=(30,10), layout="constrained")
    plt.subplots_adjust(wspace=0.1)
    axes = ax.ravel()

    baseline_df.set_index(risk_owner_hazard, inplace=True)

    for i, interaction in enumerate(interaction_dict.keys()):
        interaction_df = interaction_dict[interaction]

        # print(interaction_dict[interaction].nunique())
        interaction_df[ROH_LIST] = interaction_df.pw_combi.str.split('_', expand=True).copy()
        interaction_pivot = interaction_df.pivot_table(
            index=risk_owner_hazard,
            columns=interaction.split('&')[1],
            values='Value',
            aggfunc='sum'  # or 'mean', 'max', etc., depending on the required aggregation
        )
        interaction_pivot.reset_index()

        arr1to2 = np.round(baseline_df['Value'].values[1:] / interaction_pivot.values, 2)
        arr1to2[np.isinf(arr1to2)] = 2
        arr1to2 = np.append(arr1to2, -np.ones((len(arr1to2[:, 1]), 1)), axis=1)
        arr1to2 = np.append(arr1to2, -np.ones((1, len(arr1to2[1, :]))), axis=0)
        zh1 = arr1to2
        zh1 = zh1[:-1, :-1].ravel()

        M = len(arr1to2[0, :]) - 1
        N = len(arr1to2[:, 1]) - 1
        x = np.arange(M + 1)
        y = np.arange(N + 1)
        xs, ys = np.meshgrid(x, y)

        triangles1 = [(i + 1 + j * (M + 1) - 1, i + 1 + (j + 1) * (M + 1), i + (j + 1) * (M + 1)) for j
                      in range(N) for i in range(M)]

        triang1 = Triangulation(xs.ravel(), ys.ravel(), triangles1)

        # # Define the continuous colormap to use
        # base_cmap = plt.get_cmap('RdYlGn')
        # # Create a list of 5 colors from the continuous colormap
        # colors = base_cmap(np.linspace(0, 1, 5))
        #
        # # Create a new ListedColormap object from these colors
        # cmap = ListedColormap(colors)

        # Extract unique color values from the colorscale (ignoring the positions)
        colors = [color for position, color in COLORSCALE_HEATMAP if position in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]]

        # Create a new ListedColormap object from these colors
        cmap = ListedColormap(colors)
        #
        # print(cmap)
        # print(error)

        # define the string labels for x and y axis
        xlabels = interaction_pivot.columns.tolist()
        ylabels = interaction_pivot.index.tolist()

        # set tick locations to be the middle point between each pair of adjacent x or y values
        xticks = np.insert(np.diff(x) / 2 + x[:-1], 0, x[0] - 0.5)
        yticks = np.insert(np.diff(y) / 2 + y[:-1], 0, y[0] - 0.5)

        # plot heatmap with centered axis labels and string labels
        # bottom triangles for arr1to2 (for stage 2: combined of drought_agr & flood_agr effects relative to flood_agr)
        img1 = axes[i].tripcolor(triang1, zh1, cmap=cmap, vmax=2, vmin=0, edgecolors='w',
                                    linewidths=1.2)
        if i == len(interaction_dict.keys())-1:
            cbar = fig.colorbar(img1, ax=axes[i],ticks=[.2,.6,1.,1.4,1.8], label='Interaction effect factor', spacing='proportional')
            cbar.set_ticklabels(['Strong trade-off', 'medium trade-off', 'no interaction', 'medium synergy', 'strong synergy'],
                                fontsize=12)
            cbar.set_label('Interaction effect', fontsize=14)

        # axes[i].tick_params(axis='x', which='both', labelbottom=False, labeltop=True)
        axes[i].set_xticks(xticks[1:], xlabels, fontsize=12)
        axes[i].set_yticks(yticks[1:], ylabels, fontsize=12)
        if i == 0:
            axes[i].set_ylabel(risk_owner_hazard, fontsize=14)
        else:
            axes[i].set_ylabel(f'')
        axes[i].set_xlabel(interaction.split('&')[1], fontsize=14)
        axes[i].set_xlim(x[0], x[-1])
        axes[i].set_ylim(y[0], y[-1])
        axes[i].set_title(interaction)

        # axes[i].colorbar(img2)
        # axes[i].xtickis(rotation=45)  # Rotates X-Axis is by 45-degrees
        # axes[i].show()
        # Convert the Matplotlib figure to a PNG image and encode it in base64

    # Function to check if an axes is empty
    def is_axes_empty(ax):
        # Check for the presence of lines, collections, patches, or text
        if (len(ax.lines) == 0 and len(ax.collections) == 0 and
                len(ax.patches) == 0 and len(ax.texts) == 0):
            # Additionally check for the presence of images if necessary
            if not ax.has_data():
                return True
        return False

    # Iterate through axes and hide if empty
    for a in ax:
        if is_axes_empty(a):
            a.set_visible(False)


    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)  # Close the figure to free memory
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return f'data:image/png;base64,{image_base64}'
