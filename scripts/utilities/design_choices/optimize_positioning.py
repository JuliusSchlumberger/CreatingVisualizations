import matplotlib.pyplot as plt

from Paper3_v1.scripts.utilities.design_choices.get_tp_positions import get_tp_positions
from Paper3_v1.scripts.utilities.design_choices.pathways_calculate_vertical_distance import pathways_calculate_vertical_distance
from Paper3_v1.scripts.utilities.design_choices.shuffle_starting_measures import shuffle_order_starting_measures

from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from adaptation_pathways.plot import plot_classic_pathway_map as plot

def optimize_positioning(sequences_txt, tipping_points_txt, num_iterations):
    best_sequence = None
    best_length = 100000

    for shuffles in range(num_iterations):
        shuffeld_starters = shuffle_order_starting_measures(sequences_txt)
        # read_sequences(file)

        sequence_graph = sequences_to_sequence_graph(shuffeld_starters)
        level_by_action = action_level_by_first_occurrence(shuffeld_starters)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)

        with open(tipping_points_txt, 'r') as file:
            tipping_points = read_tipping_points(file, pathway_map.actions(), )

        pathway_map.assign_tipping_points(tipping_points)
        pathway_map.set_attribute("level", level_by_action)
        fig, ax = plt.subplots()
        plot(ax, pathway_map)

        y_positions_dict, x_positions_dict, y_positions, x_positions_tp = get_tp_positions(ax,
                                                                                           tipping_points)
        vertical_distance = pathways_calculate_vertical_distance(x_positions_dict, y_positions_dict)

        if vertical_distance < best_length:
            print(vertical_distance)
            best_length = vertical_distance
            best_sequence = shuffeld_starters
        return best_sequence