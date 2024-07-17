import pandas as pd
import gzip

def convert_gzip_to_df(file):
    # read the compressed file back into a DataFrame
    with gzip.open(file, 'rb') as f:
        df = pd.read_csv(f)
    return df