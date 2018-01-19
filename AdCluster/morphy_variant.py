# -*- coding: utf-8 -*-
import pymorphy2
import re
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
morph = pymorphy2.MorphAnalyzer()


def word_doc_matrix(lemlines, threshold):
    vec = CountVectorizer(token_pattern=u"(?u)\\b\\w+\\b")
    try:
        X = vec.fit_transform(lemlines)
        df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        df = df[df.columns[df.sum() >= threshold]]
    except ValueError:
        # threshold = 0
        # word_doc_matrix(lemlines, threshold)
        df = pd.DataFrame(data=[i for i in lemlines[0]], index=[''], columns=[''])#.fillna(0)
        print(df)
    return df


def tokenize(text):
    tokenized = [word for word in text.split(' ')]
    return tokenized


def lemmatize(lines):
    keys_tokenized = []
    templates = []

    for i, line in enumerate(lines):#[:219]:
        line = re.sub('^y ','', line)  # delete parasytic 'y ' at the beginning of lines.

        if len(line) < 36:  # grouping all TEMPLATE-fitting key phrases and dumping them into a file
            keys_tokenized.append('')
            templates.append(i)
        else:
            line_split = line.strip('\n').split(' ')
            tokens = []
            lemmaline = ''   # lemmatized key phrase
            for word in line_split:
                # print(word)
                if len(word) > 2:
                    p = morph.parse(word)[0]
                    lemma = p.normal_form
                    lemmaline += lemma + ' '
                else:
                    lemma = word
                    lemmaline += lemma + ' '

                tokens.append(lemma)
            lemmaline = lemmaline.strip(' ')
            keys_tokenized.append(lemmaline)
    return keys_tokenized, templates


def get_matrix(my_lines, threshold):
    k = lemmatize(my_lines)
    matrix = word_doc_matrix(k[0], threshold)
    templates = k[1]
    return [matrix, my_lines, templates]

# a= ['камаз полуприцеп термос москва','камаз с полуприцепом с фото москва']
# print(lemmatize(a))