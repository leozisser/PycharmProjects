# -*- coding: utf-8 -*-
import pymorphy2
import re
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
morph = pymorphy2.MorphAnalyzer()


def word_doc_matrix(lemlines, threshold):
    vec = CountVectorizer(token_pattern=u"(?u)\\b\\w+\\b")
    X = vec.fit_transform(lemlines)
    # x = vec.inverse_transform(X)
    df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    df = df[df.columns[df.sum() >= threshold]]
    # print(df)
    # print(x)
    return df


def tokenize(text):
    tokenized = [word for word in text.split(' ')]
    return tokenized


def lemmatize(lines):
    # template_file = open('template.txt', 'w', encoding='utf-8')
    keys_tokenized = []
    templates = []

    for i, line in enumerate(lines):#[:219]:
        line = re.sub('^y ','', line)  # delete parasytic 'y ' at the beginning of lines.
        # without.append(line)

        if len(line) < 36:  # grouping all TEMPLATE-fitting key phrases and dumping them into a file
            # template_file.write(line)
            keys_tokenized.append('')
            templates.append(i)
        else:
            line_split = line.strip('\n').split(' ')
            tokens = []
            lemmaline = ''   # lemmatized key phrase
            for word in line_split:
                if len(word) > 2:
                    p = morph.parse(word)[0]
                    lemma = p.normal_form
                    lemmaline += lemma + ' '
                else:
                    lemma = word
                    lemmaline += lemma + ' '

                tokens.append(lemma)
            lemmaline = lemmaline.strip(' ')
            # print(lemmaline)
            keys_tokenized.append(lemmaline)

    # template_file.close()
    return keys_tokenized, templates


def get_matrix(my_lines, threshold):
    # with open(filename, 'r', encoding='utf-8') as key:
    #     my_lines = key.readlines()
    k = lemmatize(my_lines)
    matrix = word_doc_matrix(k[0], threshold)
    templates = k[1]
    # print(matrix.head(3))
    return [matrix, my_lines, templates]
#
# key_filename = 'million_lines.txt'
# threshold = 3
#
# res = get_matrix(key_filename, threshold)[0]
#
# print(res)
