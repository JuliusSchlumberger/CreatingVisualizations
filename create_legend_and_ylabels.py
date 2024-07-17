from scripts.main_central_path_directions import ALL_PATHWAYS, ROH_LIST
from scripts.Legends.vertical_legends import create_vertical_legend_with_images
from scripts.Legends.horizontal_legends import create_horizontal_legend_with_images
from scripts.Legends.create_ylabels import create_ylabels


for risk_owner_hazard in ROH_LIST:
    legend_items = []
    name_list = []

    for y_tick in range(0,len(ALL_PATHWAYS[risk_owner_hazard])):
        # Identify specific set of measures
        row = ALL_PATHWAYS[risk_owner_hazard].loc[int(y_tick), :].values
        row_items = []
        for i, measure in enumerate(row):
            # if measure not in ['no_measure', np.nan, 'nan', np.NaN, '']:
            button_path = 'logos/colorized'
            # Get the logo filename for the current column from the dictionary
            img_path = f'{button_path}/{measure}.png'

            row_items.append({'name': measure, 'image_path': img_path})

            if measure not in name_list:
                legend_items.append({'name': measure, 'image_path': img_path})
                name_list.append(measure)
                print(name_list)
        create_ylabels(row_items, max_items_per_col=4, filepath=f"legends/{risk_owner_hazard}_pathway_{y_tick}_ylabel.png")
    create_vertical_legend_with_images(legend_items,filepath=f"legends/{risk_owner_hazard}_full_legend.png")
    create_horizontal_legend_with_images(legend_items, filepath=f"legends/vertical_{risk_owner_hazard}_full_legend.png")
# print(legend_items)
