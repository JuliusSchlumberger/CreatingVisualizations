

def get_implementation_timings(sequence_graph, current_node, depth, y_positions_dict, x_positions_dict, marker_x, marker_y,
                   marker_c, MEASURE_COLORS):
    if depth == 0:
        return

    # Retrieve nodes from which there are sequences to the current node
    previous_nodes = sequence_graph.from_nodes(current_node)
    try:
        for i, previous_node in enumerate(previous_nodes):
            # Process each previous_node
            for_markers = str(previous_nodes).split(', ')[i]
            # print(for_markers.split('(')[1])
            x_posi = for_markers.split('(')[1].replace(')]', '')
            x_posi = x_posi.replace(')', '')
            # print(x_positions_dict)
            # Update marker sizes and colors based on the current node
            try:
                marker_x.append(x_positions_dict[x_posi])
                marker_y.append(y_positions_dict[str(current_node)])
                # print(str(current_node), current_node)
                marker_c.append(MEASURE_COLORS[str(current_node)])
            except KeyError:
                print('missing', x_posi)

            # Recursively call this function for each previous node, decreasing the depth
            get_implementation_timings(sequence_graph, previous_node, depth - 1, y_positions_dict, x_positions_dict, marker_x,
                           marker_y, marker_c, MEASURE_COLORS)
    except ValueError:
        pass