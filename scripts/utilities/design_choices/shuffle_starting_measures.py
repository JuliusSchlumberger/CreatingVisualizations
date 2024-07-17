import io
import random

from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)



def shuffle_order_starting_measures(filepath):
    with open(filepath, 'r') as file:
        all_lines = file.readlines()

    # Separate 'current' lines from others
    current_lines = [line for line in all_lines if line.strip().startswith('current')]
    other_lines = [line for line in all_lines if not line.strip().startswith('current')]

    # Shuffle 'current' lines
    random.shuffle(current_lines)

    # Merge lists back, assuming the desired order
    merged_lines = current_lines + other_lines

    # Convert merged lines back to a single string
    merged_content = ''.join(merged_lines)

    # Use StringIO to create a stream from the merged content
    stream = io.StringIO(merged_content)

    # Now call your function with this stream
    sequences = read_sequences(stream, actions=None)

    # Don't forget to close the StringIO stream if necessary
    stream.close()

    return sequences
