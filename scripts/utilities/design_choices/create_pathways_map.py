from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)


def create_pathways_map(sequence_txt, tipping_point_txt):
    print(sequence_txt)
    with open(sequence_txt, 'r') as file:
        print(sequence_txt)
        sequences = read_sequences(file)

    sequence_graph = sequences_to_sequence_graph(sequences)
    level_by_action = action_level_by_first_occurrence(sequences)

    pathway_map = sequence_graph_to_pathway_map(sequence_graph)

    with open(tipping_point_txt, 'r') as file:
        tipping_points = read_tipping_points(file, pathway_map.actions(),)

    pathway_map.assign_tipping_points(tipping_points)
    pathway_map.set_attribute("level", level_by_action)

    return pathway_map, tipping_points, sequence_graph
