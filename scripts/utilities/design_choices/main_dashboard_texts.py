from dash import html
#

DASHBOARD_TITLE = 'Dashboard to Evaluate Pathways in a multi-risk system (Sectoral Risk Owner Perspective)'

DASHBOARD_EXPLANATION = {
    'title': 'Introduction',
    'body': [
        "This dashboard is designed to test how different visualizations can be used to for the evaluation of Disaster Risk Management pathways in a multi-risk setting."
        "The dashboard is set in a synthetic case study. In the case study "
        "three sectoral risk owners (farmer, shipping company and a municipality) want to identify pathways to adapt to increasing risk of floods and droughts due to climate change. "
        "One of the main question is what are the most appropriate pathways for these sectoral risk owners, considering "
        "the interactions between pathways of different sectoral risk owners. "
        "The objective is to identify combination of pathways that serve all sectoral risk owners and minimize tradeoffs. ",
        html.Br(),html.Br(),
        "This dashboard is designed to support a sectoral risk owners in the evaluation of their pathway options. Key insights include:",
        html.Br(),
        "1. Identify what alternative pathway options are on the table.",
        html.Br(),
        "2. Assess the performance of different pathways across various scenarios and time horizons.",
        html.Br(),
        "3. Understand the influence of other risk owners' pathways on one's own.",
        html.Br(), html.Br(),
        "As a user, you will take the role of a sectoral risk owner and use the visualizations to extract some information relevant for evaluating pathways. "
        "You can specify time horizons, climate scenarios, performance indicators of interest, and select what interactions with pathways from other risk owners should be explored.",
    ],
    'options_figure': 'This will be the explanation of what a Pathways Map is.',
    'PCP': "A parallel coordinate plot is a way to visualize how each pathway performs across various criteria, "
           "represented by several parallel axes."
           "This plot can uncover relationships between performance criteria and identify clusters of similar pathways. "
           "To read it, follow a line across the axes to see how the variables' values change for a single "
           "data point. Comparing lines can help you spot similarities or differences among data points across "
           "multiple dimensions.",
    'Heatmap': 'A heatmap displays data as a matrix of colored cells, where each color represents a range of values. '
               'The varying shades from light to dark (or through a spectrum of colors) indicate the magnitude of '
               'some variable, such as temperature, frequency, or intensity. This visual representation helps identify '
               'patterns, trends, and outliers at a glance. To read a heatmap, look at the color scale to understand '
               'what each color means, then match the colors in the grid to see how the values change '
               'across two dimensions.',
    'StackedBar': 'A stacked bar chart shows the breakdown of multiple categories stacked on top of each other within'
                  ' bars, where the length of each bar represents the total amount. In this specific chart, a shorter '
                  'total length indicates better performance, allowing you to quickly compare overall performance '
                  'across different pathways options. To interpret this chart, examine the lengths of the bars to '
                  'gauge performance, and look at the segments within each bar to understand the contribution of '
                  'each category to the total.',
    'detailed_explanation_CI': ["The performance of pathways is tested in a wide range of computational experiments. "
                           "Instead of showing the results for all experiments, you can choose between different "
                           "performance indicators, that aggregate the results of each performance criterion into fewer values.",
                            "You selected 'Confidence Intervals' as an performance indicator. Accordingly, "
                           "you can explore the certainty of results within the set of experiments.",
                            html.Br(),html.Br(),
                            "For example: If you want to be 95% certain about the achieved performance, 95% of all " 
                            "experiments are considered and the worst performance across these experiments is shown. " 
                            "It corresponds to the most conservative performance indication of the pathway. " 
                            "Likewise, being 5% certain about the achieved performance, corresponds to an optimistic" 
                            " perspective, where only the best 5% of the experiments are considered and the worst " 
                            "performance across these scenarios is shown."],
'detailed_explanation_otherPerformance': ["The performance of pathways is tested in a wide range of computational experiments. "
                           "Instead of showing the results for all experiments, you can choose between different "
                           "performance indicators, that aggregate the results of each performance criterion into fewer values.",
                          "You selected 'Robustness Indicator' and an performance indicator. Here, "
                          "we compute robustness across the realizations in terms of the mean results "
                          "and the standard deviation across the computational experiments. As such, "
                          "you don't get insights into the factual performance. Instead the values shown"
                          "are indications which pathways have a preferred expected performance and a low variability."],
}

GLOSSARY_TERMS={
    'Disaster Risk Management': 'Strategies and practices to reduce vulnerabilities and manage the impacts of natural hazards.',
    'Pathway': 'A sequence of measures that are implemented to adjust to future changes.',
    'Multi-Risk Setting': 'A context in which multiple hazards interact and impacts to and responses by different actors influence each other.',
    'Sectoral Risk Owner': 'Individuals or entities responsible for managing risks in specific sectors, such as a shipping company, farmer, or municipality.',
    'Climate Scenarios': 'Plausible time-series of e.g. precipitation intensity or river discharge for different warming scenarios. '
                         'Multiple time-series per climate scenario to capture uncertainty and natural variability.',
    'Performance': 'Evaluated regarding a set of criteria using indicators to deal with uncertainty in and across climate scenarios.',
    'Trade-offs': 'Compromises made when choosing between two or more competing options.',
    'Interactions': 'Pathways of different sectoral risk owners can interfere with or benefit from each other, leading to changes in performance or available options.'
}

OPTIONS = {
    'title': '1. Pathways Overview',
    'general_introduction': [
        "In the first section of the dashboard you learn about your pathways options as sectoral risk owner to deal with a specific hazard. ",
        html.Br(),
        html.B('(1)'), " Explore what measures are part of the different pathways options.",
        html.Br(),
        html.B('(2)'), " Explore how the sequences of measures are implemented in the selected time horizon and under different climate scenarios.",
        html.Br(),
        html.Br(),
         "Select your role as sectoral risk owner and respective parameters for the evaluation."
    ]
}

PERFORMANCE = {
    'title': '2. Pathways Performance Analysis',
    'general_introduction': [
        "In the second section of the dashboard, you can explore the performance of the pathways in the selected time horizon and under different climate scenarios:",
        html.Br(),
        html.B('(1)'), " Explore the performance of different pathways options across the performance criteria.",
        html.Br(),
        html.B('(2)'), " Explore how the performance evaluation changes for differernt performance indicators. ",
    ],
    'general_explanation': "The performance of pathways is tested in a wide range of computational experiments. "
                           "Instead of showing the results for all experiments, you can choose between different "
                           "performance indicators, that aggregate the results of each performance criterion into fewer values.",
    'detailed_explanation_CI': ["You selected 'Confidence Intervals' as an performance indicator. Accordingly, "
                               "you can explore the certainty of results within the set of experiments.",
                                html.Br(),html.Br(),
                                "For example: If you want to be 95% certain about the achieved performance, 95% of all " 
                                "experiments are considered and the worst performance across these experiments is shown. " 
                                "It corresponds to the most conservative performance indication of the pathway. " 
                                "Likewise, being 5% certain about the achieved performance, corresponds to an optimistic" 
                                " perspective, where only the best 5% of the experiments are considered and the worst " 
                                "performance across these scenarios is shown."],
    'detailed_explanation_otherPerformance': "You selected 'Robustness Indicator' and an performance indicator. Here, " 
                                             "we compute robustness across the realizations in terms of the mean results " 
                                             "and the standard deviation across the computational experiments. As such, " 
                                             "you don't get insights into the factual performance. Instead the values shown" 
                                             "are indications which pathways have a preferred expected performance and a low variability.",
    'nothing_selected': "Choose a performance indicator to guide your analysis."
}

MULTI_RISK = {
    'title': '3. Multi-Risk Interaction Insights',
    'general_introduction': [
        "In the third section, you can explore how your pathways options and performance are affected by other sectoral risk owner pathways:", html.Br(),
        html.B("(1)"), " Observe changes in the pathways options when considering interaction effects.", html.Br(),
        html.B("(2)"), " Observe changes in the performance when considering interaction effects."
    ]
}



TOOLTIP_TEXT = {
    'risk_owner_hazard': 'Choose a sectoral risk owner and their relevant hazards to analyze potential pathways.',
    'timehorizon': 'Select the time horizon for evaluating and comparing pathway outcomes.',
    'scenarios': 'Choose one or more climate scenarios for analysis. Each scenario is treated equally when assessing performance across multiple scenarios.',
    'confidence': 'Consider removing this option.',
    'pathways': 'Enables highlighting of specific pathways in the analysis, enhancing the visibility of their performance and interactions.',
    'which_option': 'Consider removing this option.',
    'performance_metric': 'Select a performance indicator. Indicators aggregate variations under different futures (e.g., climate or interaction scenarios) into confidence intervals. Choose from optimistic (5% CI), expected (50% CI), or pessimistic (95% CI) perceptions.',
    'multi_sectoral_interactions': 'Select other sectoral risk owner to examine their impact on your selected pathways and performance metrics.',
    'interaction_plot_of_interest': 'Do you want to look at the interaction effects regarding the pathways options or the pathways performance?'
}
