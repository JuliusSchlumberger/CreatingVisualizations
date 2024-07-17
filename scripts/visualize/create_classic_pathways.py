from Paper3_v1.scripts.utilities.design_choices.create_grey_colorscheme import create_grey_plot_colours
from Paper3_v1.scripts.utilities.design_choices.get_tp_positions import get_tp_positions
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import MEASURE_COLORS
from Paper3_v1.scripts.utilities.design_choices.get_implementation_timings import get_implementation_timings
from Paper3_v1.scripts.utilities.design_choices.add_logos import add_logos
from Paper3_v1.scripts.utilities.design_choices.pathways_calculate_vertical_distance import pathways_calculate_vertical_distance
from Paper3_v1.scripts.utilities.design_choices.shuffle_starting_measures import shuffle_order_starting_measures
import matplotlib.pyplot as plt
from adaptation_pathways.plot import plot_classic_pathway_map as plot


def create_classic_pathways(ax, tipping_points, pathway_map, sequence_graph):

    plot_colours = create_grey_plot_colours(ax, grey_value=0.8)

    y_positions_dict, x_positions_dict, y_positions, x_positions_tp = get_tp_positions(ax, tipping_points)
    print(x_positions_dict)
    print(y_positions_dict)
    pathways_calculate_vertical_distance(x_positions_dict,y_positions_dict)

    print(error)
    fig, axes = plt.subplots(layout="constrained", figsize=(12,4))
    plot(axes, pathway_map, plot_colours=plot_colours)

    axes.scatter(x=x_positions_tp, y=y_positions, marker="|", c='grey', s=200, linewidths=3)
    axes.scatter(x=[xposi - 2 for xposi in x_positions_tp], y=y_positions,c='lightgrey', marker='_', linewidths=1, s=300, zorder=4)

    marker_x = []
    marker_y = []
    marker_c = []

    # Initial call to the recursive function for each leaf node, specifying the iteration depth (e.g., 5)
    end_leaves = sequence_graph.leaf_nodes()
    for end_leaf in end_leaves:
        get_implementation_timings(sequence_graph, end_leaf, 6, y_positions_dict, x_positions_dict, marker_x, marker_y,
                       marker_c, MEASURE_COLORS)

    axes.scatter(x=marker_x, y=marker_y, s=200, zorder=5, c=marker_c)

    axes = add_logos(axes)
    return fig, axes



