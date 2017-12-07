from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
# noinspection PyUnresolvedReferences
import numpy as np


def word_doc_matrix(lines):
    vec = CountVectorizer()
    X = vec.fit_transform(lines)
    df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    df = df[df.columns[df.sum() > 1]]
    # df['sum'] = df.sum(axis=1)
    # print(df)
    # idx = df.sort_values(['sum'], ascending=False)
    # l = np.where(df.eq(1), df.columns, 'nan')
    return df


def word_doc():
    with open('key_phrases.txt', 'r', encoding='utf-8') as keys:
        lines = keys.readlines()
        dff = word_doc_matrix(lines)
        # print(dff.head(3))
        return dff
        # print(submatrix(dff))
# print(word_doc().head(5))