import numpy as np

def generate_ticks(start, end, num, label_interval):
    tickvals = np.linspace(start, end, num)
    ticktext = [str(int(val)) if i % label_interval == 0 else i*f" " for i, val in enumerate(tickvals)]
    return tickvals, ticktext