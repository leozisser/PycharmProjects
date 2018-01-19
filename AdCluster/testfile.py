import pandas as pd
import numpy as np
df = pd.DataFrame(columns=['A', 'B', 'C '], index=['D', 'E', 'F'], data = np.arange(0, 9, 1).reshape(3,3))
print(df)
