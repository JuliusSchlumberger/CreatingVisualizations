import numpy as np

def calculate_performance_metrics(df, group, metric, column_to_aggregate):
    if metric == '5%':
        return df.groupby(group)['Value'].quantile(0.05)
    elif metric == '50%':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])[column_to_aggregate].quantile(0.50)
    elif metric == '95%':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])[column_to_aggregate].quantile(0.95)
    elif metric == 'average':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])[column_to_aggregate].mean() * (1 + df.groupby(['year', 'objective_parameter', 'pw_combi'])[column_to_aggregate].std())

def custom_percentile_agg(column, percentile):
    return np.percentile(column, percentile)

def custom_agg(series, metric):
    if metric == 'average':
        return series.mean()
    else:
        # Extract the numeric value from the performance_metric string
        percentile = float(metric.replace('%', ''))
        return custom_percentile_agg(series, percentile)

def calculate_performance_metrics_old(df, metric):
    if metric == '5%':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])['Value'].quantile(0.05)
    elif metric == '50%':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])['Value'].quantile(0.50)
    elif metric == '95%':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])['Value'].quantile(0.95)
    elif metric == 'average':
        return df.groupby(['year', 'objective_parameter', 'pw_combi'])['Value'].mean()
