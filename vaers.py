import pandas as pd
import numpy as np


def create_dataframe(filename):
    """Takes the filename as a parameter and loads the data and returns its DataFrame.

    param filename: Name of the file for which the DataFrame will be created.
    :return: The DataFrame with all its rows and columns.

    """
    df = pd.read_csv(filename, engine='python')
    # print(df.head(250))
    return df

