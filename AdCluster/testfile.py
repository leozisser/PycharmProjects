# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
# df = pd.DataFrame({'A': '0 1 0 1 0 1 0 1'.split(),
#                    'B': '1 1 0 1 0 0 1 0'.split(),
#                    'C': '0 0 0 1 0 0 1 0 '.split(),
#                    'D': '0 0 1 0 0 0 0 0'.split()})
#
# l=np.where(df.eq(1), df.columns, 'nan')


k = ['a','s','d','f']

line = ''
for i in k:
    line += i
print(line)
