# Import required libraries
from dash import dcc, html
# from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from Paper3_v1.scripts.utilities.design_choices.main_dashboard_design_choices import PANEL_BACKGROUND,DASHBOARD_BACKGROUND, DASHBOARD_DIMENSIONS
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_texts import *
from Paper3_v1.scripts.utilities.design_choices.main_dashboard_dropdowns import ROH_DICT, TIMEHORIZONS, SCENARIOS, CONFIDENCE, WHICH_OPTIONS, PERFORMANCE_METRICS, INTERACTION_VIZ
from Paper3_v1.main_central_path_directions import DIRECTORY_MEASURE_LOGOS_GITHUB


def create_main_dashboard_structure(app):
    app.layout = html.Div([
        html.H1(DASHBOARD_TITLE, style={'textAlign': 'center'}),

        # # New panel for General Comments
        # html.Div([
        #     html.H2(DASHBOARD_EXPLANATION['title']),
        #     # *[html.P(paragraph) for paragraph in DASHBOARD_EXPLANATION['body']]
        #     html.P(DASHBOARD_EXPLANATION['body']
        #         ),
        # ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
        #           'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '100%'}),
        # Flex container for the introduction and glossary
        # html.Div([
        #     # Introduction panel
        #     html.Div([
        #         html.H2(DASHBOARD_EXPLANATION['title']),
        #         html.P(DASHBOARD_EXPLANATION['body']),
        #     ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
        #               'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '70%', 'marginRight': '1%'}),
        #
        #     # Glossary panel
        #     html.Div([
        #         html.H2('Glossary'),
        #         html.Ul([html.Li([html.B(f"{term}"), f": {definition}"]) for term, definition in GLOSSARY_TERMS.items()])
        #     ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
        #               'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '29%'}),
        #
        # ], style={'display': 'flex', 'flexDirection': 'row'}),  # Flex container style
        # Flex container for the three panels: introduction text, image, and glossary
        html.Div([

            # Introduction text panel
            html.Div([
                html.H2(DASHBOARD_EXPLANATION['title']),
                html.P(DASHBOARD_EXPLANATION['body']),
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '40%', 'marginRight': '1%'}),

            # Image panel
            html.Div([
                html.Img(src=f'{DIRECTORY_MEASURE_LOGOS_GITHUB}/Waasmodel.png', style={'width': '100%', 'marginBottom': DASHBOARD_DIMENSIONS['margin']}),  # Adjust src and style as needed
                html.P("Visualization of the case study area as published in Haasnoot et al. (2012).", style={'textAlign': 'center'})
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '29%', 'marginRight': '1%'}),

            # Adjusted for two columns inside

            # Glossary panel
            html.Div([
                html.H2('Glossary'),
                html.Ul(
                    [html.Li([html.B(f"{term}"), f": {definition}"]) for term, definition in GLOSSARY_TERMS.items()])
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'width': '29%'}),

        ], style={'display': 'flex', 'flexDirection': 'row'}),  # Flex container style


        # Div for the left panel (Explanation and Interaction Buttons)
        html.Div([
            # Showing Options
            html.Div([
                html.H3(OPTIONS['title']),
                html.Div(OPTIONS['general_introduction'],style={'marginBottom': '5vh'}),
                dbc.Row([
                    dbc.Col([
                        html.Label('a) Select Risk Owner - Hazard', className='mb-1')], width=6,),
                    dbc.Col([
                        html.Label('b) Timehorizon for Evaluation', className='mb-1')], width=6,)]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id='risk_owner_hazard',
                                     options=[{'label': option, 'value': ROH_DICT[option]} for option in ROH_DICT],
                                     value = ROH_DICT[list(ROH_DICT.keys())[0]]
                                     ),
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-risk_owner_hazard"), width=1),

                    dbc.Col([
                        dcc.Dropdown(id='timehorizon',
                                     options=[{'label': option, 'value': TIMEHORIZONS[option]} for option in TIMEHORIZONS],
                                     value = TIMEHORIZONS[list(TIMEHORIZONS.keys())[-1]]
                                     ),
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-timehorizon"), width=1),

                ], style={'marginBottom': '2vh'}),

                dbc.Row([
                    dbc.Col([
                        html.Label('c) Climate Scenarios', className='mb-1')], width=6, ),
                    dbc.Col([
                        html.Label('d) Highlight Pathway Alternative', className='mb-1')], width=6, )]),
                dbc.Row([
                    dbc.Col([
                        dcc.Checklist(id='scenarios',
                                     options=[{'label': option, 'value': SCENARIOS[option]} for option in SCENARIOS],
                                     inline=True, inputStyle={"marginRight": "1vh","marginLeft": "2vh"},
                                    value=[SCENARIOS[list(SCENARIOS.keys())[0]]]
                                      ),
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-scenarios"), width=1),

                    dbc.Col([
                        dcc.Dropdown(id='highlight_pathway',
                                     ),
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-pathways"), width=1),

                ], style={'marginBottom': '2vh'}),

                # Button to open the modal
                dbc.Row([
                    dbc.Button("Show Explanation Options Figure Type", id="open-modal-options_figure", className="mb-3"),

                    # The Modal
                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Figure Explanation")),
                        dbc.ModalBody(DASHBOARD_EXPLANATION['options_figure']),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-modal-options_figure", className="ms-auto", n_clicks=0)
                        ),
                    ], id="options_figure-modal", is_open=False),  # Modal starts hidden
                ], style={'marginBottom': '2vh'}),
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'], 'marginBottom': DASHBOARD_DIMENSIONS['margin'],
                      'width': '100%', 'height': DASHBOARD_DIMENSIONS['options_panel'] }),

            # Tooltips for the buttons
            dbc.Tooltip(TOOLTIP_TEXT['risk_owner_hazard'], target="tooltip-risk_owner_hazard"),
            dbc.Tooltip(TOOLTIP_TEXT['timehorizon'], target="tooltip-timehorizon"),
            dbc.Tooltip(TOOLTIP_TEXT['scenarios'], target="tooltip-scenarios"),
            dbc.Tooltip(TOOLTIP_TEXT['pathways'], target="tooltip-pathways"),

            # Showing Performance
            html.Div([
                html.H3(PERFORMANCE['title']),
                html.Div(PERFORMANCE['general_introduction'], style={'marginBottom': '5vh'}),
                dbc.Row([
                    dbc.Col([
                        html.Label('a) dev: Plot Alternatives', className='mb-1')], width=6, ),
                    dbc.Col([
                        html.Label('b) Performance Indicator', className='mb-1')], width=6, )]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id='options',
                                     options=[{'label': option, 'value': WHICH_OPTIONS[option]} for option in
                                              WHICH_OPTIONS],
                                     value=WHICH_OPTIONS[list(WHICH_OPTIONS.keys())[0]],
                                     ),
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-which_option"), width=1),

                    dbc.Col([
                        dcc.Dropdown(id='performance_metric',
                                     options=[{'label': option, 'value': PERFORMANCE_METRICS[option]} for option in
                                              PERFORMANCE_METRICS],
                                     value=PERFORMANCE_METRICS[list(PERFORMANCE_METRICS.keys())[0]],
                                     )
                    ], style={'marginRight': '-1vw'}, width=5),

                    dbc.Col(dbc.Button("?", id="tooltip-performance_metric"), width=1),

                ], style={'marginBottom': '2vh'}),
            # html.Div(id='performance_explanation', style={'marginBottom': '5vh'}),
                dbc.Row([
                    dbc.Button("Show Explanation Performance Analysis", id="open-modal-performance_analysis", className="me-2",
                               n_clicks=0),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Performance Analysis Explanation")),
                        dbc.ModalBody(id="modal-body-performance_analysis"),  # Content will be set dynamically
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-modal-performance_analysis", className="ms-auto", n_clicks=0)
                        ),
                    ], id="performance_analysis-modal", is_open=False),
                ], style={'marginBottom': '2vh'}),
                dbc.Row([
                    dbc.Button("Show Explanation Performance Figure", id="open-modal-performance_figure", className="me-2", n_clicks=0),

                    dbc.Modal([
                        dbc.ModalHeader(dbc.ModalTitle("Figure Explanation")),
                        dbc.ModalBody(id="modal-body-performance_figure"),  # Content will be set dynamically
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-modal-performance_figure", className="ms-auto", n_clicks=0)
                        ),
                    ], id="performance_figure-modal", is_open=False),
                ], style={'marginBottom': '2vh'}),
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'],
                      'width': '100%', 'height': DASHBOARD_DIMENSIONS['performance_panel']}),

            # Tooltips for the buttons
            dbc.Tooltip(TOOLTIP_TEXT['which_option'], target="tooltip-which_option"),
            dbc.Tooltip(TOOLTIP_TEXT['performance_metric'], target="tooltip-performance_metric"),

            # Exploring Multi-risk Interactions
            html.Div([
                html.H3(MULTI_RISK['title']),
                html.Div(MULTI_RISK['general_introduction'], style={'marginBottom': '5vh'}),
                dbc.Row([
                    dbc.Col([
                        html.Label('a) Multi-sectoral interactions (multiple-choice)', className='mb-1')], width=8, ),
                    ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Checklist(id='multi_sectoral_interactions',),
                    ], style={'marginRight': '-1vw'}, width=8),

                    dbc.Col(dbc.Button("?", id="tooltip-multi_sectoral_interactions"), width=1),

                    ], style={'marginBottom': '2vh'}),
                dbc.Row([
                    dbc.Col([
                        html.Label('b) Explore interaction effects on...', className='mb-1')], width=8, ),
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id='interaction_plot_options',
                                     options=[{'label': option, 'value': INTERACTION_VIZ[option]} for option in
                                              INTERACTION_VIZ],
                                     ),
                    ], style={'marginRight': '-1vw'}, width=8),

                    dbc.Col(dbc.Button("?", id="tooltip-interaction_plot_of_interest"), width=1),

                ], style={'marginBottom': '2vh'}),

            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'],
                      'width': '100%', 'height': DASHBOARD_DIMENSIONS['multi_risk_panel']}),

            # Tooltips for the buttons
            dbc.Tooltip(TOOLTIP_TEXT['multi_sectoral_interactions'], target="tooltip-multi_sectoral_interactions"),
            dbc.Tooltip(TOOLTIP_TEXT['interaction_plot_of_interest'], target="tooltip-interaction_plot_of_interest"),

        ], style={'width': DASHBOARD_DIMENSIONS['left_panel_width'], 'display': 'inline-block',
                  'verticalAlign': 'top'}),

        # Div for the right panels (Figures)
        html.Div([
            # Panel for Showing Options with figure
            html.Div([
                # html.H2('Showing Options'),
                # html.Iframe(src=f'https://raw.githubusercontent.com/JuliusSchlumberger/5_code/master/Paper3_v1/figures/decision_tree/stage3_portfolios_flood_agr.html', width='100%', height='600'),  # Adjust width and height as needed
                # html.Img(id='options-graph', style={'width': DASHBOARD_DIMENSIONS['figure_options']}),
                dcc.Graph(id='options-graph',
                          style={'height': DASHBOARD_DIMENSIONS['figure_options'], 'maxHeight': '550px'}),
                html.Img(id='pathways_legend-image', src='',
                         style={'height': DASHBOARD_DIMENSIONS['figure_legend']})
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'height': DASHBOARD_DIMENSIONS['options_panel'],
                      'display': 'flex',  # This will enable flexbox for this container
                      'flex-direction': 'column',  # This stacks the children vertically
                      'align-items': 'center',  # This centers the children horizontally in the container
                      'justify-content': 'center'
                      # This centers the children vertically in the container, if you want equal spacing around them
                      }),

            # Panel for Performance with figure
            html.Div([
                # html.H2('Performance'),
                dcc.Graph(id='performance-graph', style={'height': DASHBOARD_DIMENSIONS['figure_options'], 'maxHeight': '550px'}),
                html.Img(id='performance_legend-image', src='',
                         style={'height': DASHBOARD_DIMENSIONS['figure_legend'],

                                })
            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'],
                      'marginBottom': DASHBOARD_DIMENSIONS['margin'], 'height': DASHBOARD_DIMENSIONS['performance_panel'],
                      # 'display': 'flex',  # This will enable flexbox for this container
                      # 'flex-direction': 'column',  # This stacks the children vertically
                      # 'align-items': 'center',  # This centers the children horizontally in the container
                      # 'justify-content': 'center'
                      }),

            # Panel for Multi-risk interactions with figure
            html.Div([
                # html.H2('Multi-risk interactions'),
                dcc.Graph(id='interactions-graph', style={'height': DASHBOARD_DIMENSIONS['figure_options'], 'maxHeight': '550px', 'display': 'none'}),  # Initially hidden
                html.Img(id='interactions-image', src='', style={'height': DASHBOARD_DIMENSIONS['figure_options'], 'display': 'none'})  # Initially hidden

            ], style={'backgroundColor': PANEL_BACKGROUND, 'padding': DASHBOARD_DIMENSIONS['padding'], 'height': DASHBOARD_DIMENSIONS['multi_risk_panel']})
        ], style={'width': DASHBOARD_DIMENSIONS['right_panel_width'], 'display': 'inline-block', 'verticalAlign': 'top',
                  'marginLeft': DASHBOARD_DIMENSIONS['button_vdistance']}),
    ], style={'padding': DASHBOARD_DIMENSIONS['padding_dashboard'], 'backgroundColor': DASHBOARD_BACKGROUND})




    return app



