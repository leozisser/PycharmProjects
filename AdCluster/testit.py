# from sklearn.feature_extraction.text import CountVectorizer
# import pandas as pd
#
#
# def word_doc_matrix(lines, threshold):
#     vec = CountVectorizer()
#     X = vec.fit_transform(lines)
#     df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
#     df = df[df.columns[df.sum() >= threshold]]
#     return df


# threshold = 3
filename = open('million_lines.txt', 'r', encoding='utf-8')
key = filename.readlines()[:20000]

# r = word_doc_matrix(filename, threshold)
k = {}
for line in key:
    line = line.split(' ')
    for word in line:
        if word not in key:
            k[word] = 1
        else:
            k[word]+=1
out = open('million_lines_freqdict.txt', 'w', encoding='utf-8')
for i in k:
    out.write(k)
print(k)