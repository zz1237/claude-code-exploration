"""Module for creating dataframes with random data."""

import pandas as pd
import numpy as np


def create_random_dataframe(rows: int = 5, cols: int = 3) -> pd.DataFrame:
    """
    Create a pandas DataFrame with random data.

    Args:
        rows: Number of rows in the dataframe. Defaults to 5.
        cols: Number of columns in the dataframe. Defaults to 3.

    Returns:
        A pandas DataFrame with random float values between 0 and 1.
    """
    column_names = [f'column{i+1}' for i in range(cols)]
    return pd.DataFrame(
        np.random.rand(rows, cols),
        columns=column_names
    )


if __name__ == '__main__':
    df = create_random_dataframe()
    print(df)
