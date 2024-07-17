from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import MEASURE_COLORS

def get_tp_positions(ax, tipping_points):
    ytick_labels = ax.get_yticklabels()

    y_positions_dict = {}
    x_positions_dict = {}
    for ytick in ytick_labels:
        _, y_pos = ytick.get_position()
        measure_name = ytick.get_text()
        y_positions_dict[measure_name] = y_pos

    for key_i, key in enumerate(tipping_points):
        x_positions_dict[str(key)] = tipping_points[key]

    y_positions = []
    x_positions_tp = []
    # print(y_positions_dict)
    # print(x_positions_dict)

    for x_posi in x_positions_dict.keys():
        # if 'current[' in str(x_posi):
        #     measure_name = 'current'
        # else:
        #     print(x_posi[:-3], str(x_posi))
        measure_name = str(x_posi).split('[')[0]
        y_positions.append(y_positions_dict[measure_name])
        x_positions_tp.append(x_positions_dict[x_posi] + 1)

    return y_positions_dict, x_positions_dict,y_positions, x_positions_tp
