from scripts.main_central_path_directions import MEASURE_LOGOS_GITHUB, ALL_PATHWAYS, LEGENDS_LOCATION_GITHUB

def add_measure_buttons(fig, y_ticks, risk_owner_hazard):
    for tick, y_tick in enumerate(y_ticks.values):
        img_path = f'{LEGENDS_LOCATION_GITHUB}/{risk_owner_hazard}_pathway_{y_tick}_ylabel.png'

        fig.add_layout_image(
            dict(
                source=img_path,
                xref="paper",  # Use "paper" for relative positioning
                yref="y",  # Use axis ID for aligning with specific ticks
                x=.23,  # Adjust this value to position the image on the x-axis
                y=tick,  # Align with a specific y-axis tick label
                sizex=.7,
                sizey=.7,
                xanchor="right",
                yanchor="middle",
            ),
        )
    return fig

