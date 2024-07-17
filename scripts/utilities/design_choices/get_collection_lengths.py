import matplotlib as mpl


def get_collection_lengths(ax):
    node_colours_length = 0
    edge_colours_length = 0

    for child in ax.get_children():
        if isinstance(child, mpl.collections.PathCollection):
            # Assuming each path in the collection represents one node
            node_colours_length += len(child.get_offsets())
        elif isinstance(child, mpl.collections.LineCollection):
            # Assuming each line in the collection represents one edge
            # This might need adjustment based on how edges are represented in your plot
            edge_colours_length += len(child.get_segments())

    return node_colours_length, edge_colours_length
