import pandas as pd
import numpy as np

# Create a dataframe with 3 columns and 5 rows of random data
df = pd.DataFrame(
    np.random.rand(5, 3),
    columns=['column1', 'column2', 'column3']
)

print(df)
