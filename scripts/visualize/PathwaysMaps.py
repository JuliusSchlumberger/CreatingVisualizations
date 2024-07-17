# from io import StringIO
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import matplotlib.pyplot as plt
# import base64
# from io import BytesIO
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#
# from Paper3_v1.scripts.utilities.design_choices.add_logos import add_logos
# import plotly.graph_objects as go
# from Paper3_v1.scripts.utilities.design_choices.create_pathways_map import create_pathways_map
# from Paper3_v1.scripts.utilities.design_choices.create_grey_colorscheme import create_grey_plot_colours
# from Paper3_v1.scripts.utilities.design_choices.add_interaction_changes import add_interaction_changes
# from adaptation_pathways.graph import (
#     action_level_by_first_occurrence,
#     read_sequences,
#     read_tipping_points,
#     sequence_graph_to_pathway_map,
#     sequences_to_sequence_graph,
# )
# from adaptation_pathways.plot import init_axes
# from adaptation_pathways.plot import plot_classic_pathway_map as plot
# from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import FIGSIZES
#
#
# def PathwaysMaps(sequences_no_interaction, tipping_points_no_interaction, interactions_of_interest=None,sequences_interaction_other=None, tipping_points_interaction_other=None,  sequences_interaction=None, tipping_points_interaction=None):
#
#     pathways_map, tipping_points = create_pathways_map(sequences_no_interaction, tipping_points_no_interaction)
#
#
#
#     if interactions_of_interest is None:
#         fig1, axes1 = plt.subplots(layout="constrained", figsize=FIGSIZES['options_figure'])
#
#         fig, axes = create_classic_pathways(axes1)
#         plot(axes1, pathways_map)
#         # axes1 = add_logos(axes1)
#
#         buf = BytesIO()
#         fig1.savefig(buf, format='png')
#         plt.close(fig1)  # Close the figure to free memory
#         buf.seek(0)
#         image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         return f'data:image/png;base64,{image_base64}'
#     else:
#
#         pathways_map_interaction, tipping_points_interaction = create_pathways_map(sequences_interaction,
#                                                                                    tipping_points_interaction)
#         pathways_map_interaction_other_dict = {}
#         tipping_points_interaction_other_dict = {}
#         for interaction in interactions_of_interest:
#             pathways_map_interaction_other_dict[interaction], tipping_points_interaction_other_dict[
#                 interaction] = create_pathways_map(sequences_interaction_other[interaction],
#                                                    tipping_points_interaction_other[interaction])
#
#         plot_colours_old = create_grey_plot_colours(0.8)  # Mid-grey
#         fig1, axes = plt.subplots(ncols=1,nrows=len(interactions_of_interest), layout="constrained")
#         ax = axes.ravel()
#         plot(ax[0], pathways_map, plot_colours=plot_colours_old)
#         plot(ax[0], pathways_map_interaction)
#         # ax[0] = add_logos(ax[0])
#
#         ax[0] = add_interaction_changes(tipping_points, tipping_points_interaction, ax[0])
#
#         for i, interaction in enumerate(interactions_of_interest):
#             plot(ax[i+1],pathways_map_interaction_other_dict[interaction])
#             ax[i+1] = add_logos(ax[+1])
#
#         buf = BytesIO()
#         fig1.savefig(buf, format='png')
#         plt.close(fig1)  # Close the figure to free memory
#         buf.seek(0)
#         image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         return f'data:image/png;base64,{image_base64}'