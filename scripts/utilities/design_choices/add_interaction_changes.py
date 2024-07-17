def add_interaction_changes(old_tp_dict, new_tp_dict, axes):
    new_dict = {}
    print(new_tp_dict)
    print(old_tp_dict)
    for key_i, key in enumerate(old_tp_dict):
        print(str(key), old_tp_dict[key], list(new_tp_dict.keys())[0])
        if old_tp_dict[key] != list(new_tp_dict.keys())[key_i]:
            new_dict[key] = [old_tp_dict[key], new_tp_dict[list(new_tp_dict.keys())[key_i]]]

    for i, (key, values) in enumerate(new_dict.items()):
        # Now that the y-tick labels are set, retrieve them for position lookup
        ytick_labels = axes.get_yticklabels()
        # print(ytick_labels)
        # print(axes.get_yticklabels())
        for label_option in ytick_labels:
            print(str(key)[:-3], label_option.get_text())
            if str(key)[:-3] == label_option.get_text():
                _, y_pos = label_option.get_position()
                continue

        # Plotting each line
        axes.plot(values, [y_pos, y_pos], linestyle='dotted', color='white', label=key,linewidth=4.0)
    return axes

