# import pandas as pd
import numpy as np
import os
import re, statistics
import pymorphy2
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
morph = pymorphy2.MorphAnalyzer()

def word_doc_matrix(lemlines, threshold):
    vec = CountVectorizer(token_pattern=u"(?u)\\b\\w+\\b")
    X = vec.fit_transform(lemlines)
    df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    df = df[df.columns[df.sum() >= threshold]]
    return df


def tokenize(text):
    tokenized = [word for word in text.split(' ')]
    return tokenized


def lemmatize(lines):
    template_file = open('template.txt', 'w', encoding='utf-8')
    keys_tokenized = []
    templates = []

    for i, line in enumerate(lines):#[:219]:
        line = re.sub('^y ','', line)  # delete parasytic 'y ' at the beginning of lines.
        # without.append(line)

        if len(line) < 36:  # grouping all TEMPLATE-fitting key phrases and dumping them into a file
            template_file.write(line)
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

    template_file.close()
    return keys_tokenized, templates


def get_matrix(filename, threshold):
    with open(filename, 'r', encoding='utf-8') as key:
        my_lines = key.readlines()
        k = lemmatize(my_lines)
        matrix = word_doc_matrix(k[0], threshold)
        templates = k[1]
        # print(matrix.head(3))
        return [matrix, my_lines, templates]




def re_sub(strings):
    good = [re.sub('^y ','', s)for s in strings]
    return good


def loser(dff, listt):
    dic = {}
    for i in listt:
        t = dff.nfriends[i]
        dic[i] = t
    a = (min(dic, key=dic.get))
    return a

threshold = 4
key_filename = 'key_phrases.txt'


res = [i for i in get_matrix(key_filename, threshold)] #sends threshold to get_matrix where non-sgnificant columns are cut off
lines = re_sub(res[1])
df = res[0]
print(lines)
df = df.replace(2, 1)
template_numbers = res[2]
print('TEMPLATE', template_numbers)


l = np.where(df >= 1, df.columns, 'nan')
# print(l)
index_list = []
eigen_list = []
friends_list = []
nfriends = []
tss_list = []
print('getting eigen matrices')
for y,x in enumerate(l):
    # print(x)
    index_list.append(y)
    # print('processing row: ',y)
    # print('this line: ', l[y])
    eigen_matrix = (df.drop(y)[x[x!='nan']])  # create submatrix
    eigen_matrix['summa'] = eigen_matrix.sum(axis=1)
    eigen_list.append(eigen_matrix)  # append sum column
    # print(eigen_matrix)
    tss = eigen_matrix['summa'].max()  # collect TSS for line
    tss_list.append(tss)
    # print(y, 'line', x, 'tss', tss)

    """when calculating TSS ot FRIENDS, we need to get:
     a) either a list of column headers for every friend, so that later we could make a dict{friend:[headers]}
      and then ' '.join([headers]) and thus get a name for our cluster (not preferable),
     b) or a list of all headers of the submatrix, to be later mapped to all levels of SS."""

    if tss >= threshold:
        friends = eigen_matrix.index[eigen_matrix['summa'] == tss].tolist()
        friends_list.append(friends)
        nfriends.append(len(friends))
        '''We need to make this into a function. 
        write code to add friends for tss-1, tss-2, etc.
            maybe return a dict {tss:[friends], tss-1:[friends], tss-2:[friends]...}'''
    else:
        # print('STANDALONE STRING')
        friends_list.append('nan')
        nfriends.append(0)


df['tss'] = tss_list
df['friends'] = friends_list
df['nfriends'] = nfriends
df = df.sort_values(['tss', 'nfriends'], ascending=[0, 0])
# df['friends'] = friends_list
# print(df)
clusters = {}
done = []
purgery = []
loners = []

for indexx, row in df.iterrows():  # better create df where everyone has friends and then iterate over it
    if indexx not in done:
        my_friends = row['friends']
        # print(my_friends)
        if my_friends != 'nan':
            print('processing line: ', indexx)
            cluster = [indexx]  # forming head of cluster - the iterated line
            commonfriends = {}
            friends_alive = []  # list of line's friends that are not already clustered
            for i in my_friends:  # iterating over friends of given line
                # print('current friend',i)
                # print(df.friends[i])
                if i not in done:
                    # print('done', done)
                    # print('i', i)
                    friends_alive.append(i)
                    friends_of_friend = df.friends[i]
                    # print('i`s friends ', friends_of_friend)
                    common = set(my_friends).intersection(friends_of_friend)
                    # print('common', common)  # intersect line's friends with his friend's friends and add it to dictionary
                    commonfriends[i] = [f for f in common if f not in done]  # adds the intersection to dictionary {friend: common friends} if not done
            # print('commonfriends', commonfriends)
            # print('friends_alive', friends_alive)

            if commonfriends:
                best = max(commonfriends, key=lambda key: len(commonfriends[key]))
                cluster.append(best)
                done.append(best)
                cluster.extend([i for i in commonfriends[best]])  # get all of common friends in cluster
                done.extend([j for j in commonfriends[best]])
                # print('cluster', cluster)
            else:
                if not friends_alive:  # line has no unclustered friends
                    print('my friends are dead')
                    print('monocluster, goes to purgery', cluster)
                    purgery.append(indexx)
                else:
                    cluster.append(friends_alive[-1])  # gets friend that is alive and has minimum friends
                    print('cluster', cluster)

            if len(cluster) > 1:
                cluster_name = ' '.join([i for i in set(l[cluster[0]]).intersection(l[cluster[1]]) if i != 'nan'])
                print(cluster_name)
                clusters[cluster_name] = cluster
                done.append(indexx)

            # done.extend([i for i in my_friends if i not in done]) #write L2 clustering.
        else:
            if indexx not in template_numbers:
                # print('processing line: ', indexx)
                # print('unclustered, goes to loners')
                loners.append(indexx)
                done.append(indexx)

print(len(loners))

postclustered = []
for line_number in purgery:
    lemmas = [i for i in l[line_number]if i != 'nan'] #here maybe include non-significant words
    d = {}
    for name in clusters:
        k = len(set(lemmas).intersection([i for i in name.split(' ')]))
        d[name] = k
    maxk = max(d, key=d.get)
    if d[maxk] >= threshold:
        clusters[maxk].append(line_number)
        postclustered.append(line_number)
    else:
        loners.append(line_number)
        print('why?', line_number, df['friends'][line_number], 'friends', ) #try to fix this too

print('postclustered', len(postclustered))
print('loners', len(loners))
print('clusters ', clusters)
print('number of clusters', len(clusters))
print('purgery', purgery)

directory = os.path.join('clusters', key_filename.strip('.txt'))
os.makedirs(directory, exist_ok=True)
for name in clusters:
    with open(os.path.join(directory,name + '.txt'), 'w', encoding='utf-8') as file:
        for line in clusters[name]:
            file.write(lines[line])
with open(os.path.join(directory, 'loners.txt'), 'w', encoding='utf-8') as lonerfile:
    for i in loners:
        lonerfile.write(lines[i])
