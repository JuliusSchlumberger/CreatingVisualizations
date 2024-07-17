from scripts.StackedBar.create_pattern_image import create_pattern_image
from scripts.main_central_path_directions import LEGENDS_LOCATION_GITHUB

def add_custom_legend(fig, marker_dict, risk_owner_hazard):
    # Create and save images for each entry in marker_dict
    for name, (color, pattern) in marker_dict.items():
        if color is None and pattern is None:
            pass
        elif pattern is None:
            img = create_pattern_image(color, pattern)
            img.save(f"markers_for_github/markers_{name}_{risk_owner_hazard}.png")
        else:
            pattern = pattern['shape']
            # print(color)
            # print('e', pattern)
            img = create_pattern_image(color, pattern)
            # img.show()
            img.save(f"markers_for_github/markers_{name}_{risk_owner_hazard}.png")
    # Position for the custom legend
    x_start = 1.015
    y_start = .9
    y_step = -0.04

    # Add custom markers and text
    # Add custom markers and text using the saved images
    for i, name in enumerate(marker_dict.keys()):
        y_position = y_start + i * y_step
        fig.add_layout_image(
            dict(
                source=f"{LEGENDS_LOCATION_GITHUB}/markers_{name}_{risk_owner_hazard}.png",
                xref="paper", yref="paper",
                x=x_start, y=y_position,
                sizex=0.03, sizey=0.03,
                xanchor="left", yanchor="top"
            )
        )
        fig.add_annotation(
            x=x_start + 0.02, y=y_position - 0.015,
            text=name,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            xref="paper", yref="paper",
            font=dict(color="black", size=10)
        )
    return fig