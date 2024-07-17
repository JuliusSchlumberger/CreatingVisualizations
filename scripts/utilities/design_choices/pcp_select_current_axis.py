
# Functions
def select_current_axis(selected_axes, selected_objective):
    if selected_objective == 'aggregated':
        set_objectives = objectives_agg
    else:
        set_objectives = objectives
    dimensions = []
    for sector in selected_axes:
        if selected_objective == 'aggregated':
            sector_objective = set_objectives[sector]
            dimensions.append(sector_objective[0])
        else:
            sector_objective = set_objectives[sector]
            dimensions = dimensions + [obj for obj in sector_objective]
    dimensions = ['Shipping_Strategy', 'Urban_Strategy', 'Agriculture_Strategy',*dimensions]
    return dimensions