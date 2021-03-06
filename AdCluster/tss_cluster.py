# import pandas as pd
import numpy as np
import morphy_variant
import os
import re
import time
import excel_copy_write
from foldercrawler import path2lines
import statistics
start_time = time.time()


def re_sub(strings):
    good = [re.sub('^y ','', s)for s in strings]
    return good


def loser(dff, listt):
    dic = {}
    for i in listt:
        t = dff['~nfriends'][i]
        dic[i] = t
    a = (min(dic, key=dic.get))
    return a


def TSS(key_filename, my_lines, threshold, xlw):
    res = [i for i in morphy_variant.get_matrix(my_lines, threshold)] #sends threshold to get_matrix where non-sgnificant columns are cut off
    lines = re_sub(res[1])
    df = res[0]
    # print(lines)
    df = df.replace(2, 1)
    template_numbers = res[2]
    # print('TEMPLATE', template_numbers)
    l = np.where(df >= 1, df.columns, 'nan')
    friends_list = []
    nfriends = []
    tss_list = []

    clusters = {}
    done = []
    purgery = []
    loners = []

    print('getting eigen matrices')
    for y,x in enumerate(l):
        print(y)
        # index_list.append(y)
        # print('processing row: ',y)
        # print('this line: ', l[y])
        try:
            eigen_matrix = (df.drop(y)[x[x!='nan']])  # create submatrix
        except ValueError:
            eigen_matrix = df
        eigen_matrix['summa'] = eigen_matrix.sum(axis=1)
        # eigen_list.append(eigen_matrix)  # append sum column
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
            if y not in template_numbers:
                # print('STANDALONE STRING')
                loners.append(lines[y])
            friends_list.append('nan')
            nfriends.append(0)
            done.append(y)


    df['tss'] = tss_list
    df['-friends-'] = friends_list
    df['~nfriends'] = nfriends
    df = df[df['~nfriends'] != 0]
    df = df.sort_values(['tss', '~nfriends'], ascending=[0, 0])

    for indexx, row in df.iterrows():  # better create df where everyone has friends and then iterate over it
        if indexx not in done:
            my_friends = row['-friends-']
            # print(my_friends)
            if my_friends != 'nan':
                print('processing line: ', indexx)
                cluster = [indexx]  # forming head of cluster - the iterated line
                commonfriends = {}
                friends_alive = []  # list of line's friends that are not already clustered
                for i in my_friends:  # iterating over friends of given line
                    # print('current friend',i)
                    # print(df.-friends-[i])
                    if i not in done:
                        friends_alive.append(i)
                        friends_of_friend = df['-friends-'][i]
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
                        # print('my friends are dead')
                        # print('monocluster, goes to purgery', cluster)
                        purgery.append(indexx)
                    else:
                        cluster.append(friends_alive[-1])  # gets friend that is alive and has minimum friends
                        # print('cluster', cluster)

                if len(cluster) > 1:
                    cluster_name = ' '.join([i for i in set(l[cluster[0]]).intersection(l[cluster[1]]) if i != 'nan'])
                    # print(cluster_name)
                    clusters[cluster_name] = cluster
                    done.append(indexx)

                # done.extend([i for i in my_friends if i not in done]) #write L2 clustering.
            # else:
            #     if indexx not in template_numbers:
            #         # print('processing line: ', indexx)
            #         # print('unclustered, goes to loners')
            #         loners.append(indexx)
            #         done.append(indexx)

    # print(len(loners))

    postclustered = []
    for line_number in purgery:
        lemmas = [i for i in l[line_number]if i != 'nan'] #here maybe include non-significant words
        d = {}
        cnt = 0
        for name in clusters:
            k = len(set(lemmas).intersection([i for i in name.split(' ')]))
            d[name] = k
            cnt += 1
        maxk = max(d, key=d.get)
        if d[maxk] >= threshold:
            clusters[maxk].append(line_number)
            postclustered.append(line_number)
        else:
            loners.append(lines[line_number])
            print('why?', line_number, df['-friends-'][line_number], 'friends', ) #try to fix this too

    # clusters['loners'] = loners #appends loners to all clusters
    clusters['шаблоны'] = template_numbers #also appends templates

    print('postclustered', len(postclustered))
    print('loners', len(loners))
    print('clusters ', clusters)
    print('number of clusters', len(clusters))
    print('purgery', purgery)
    filename = os.path.basename(key_filename)
    directory2 = os.path.join('clustered', key_filename.strip('.txls'))  # where loners go
    directory = os.path.join('clustered', key_filename.strip('.txls'), 'clusters')  # where clusters go
    os.makedirs(directory, exist_ok=True)
    lens = []
    for name in clusters:
        lens.append(len(clusters[name]))
        # with open(os.path.join(directory, name + '.txt'), 'w', encoding='utf-8') as file:
    #         for line in clusters[name]:
    #             file.write(lines[line] + "\n")
    with open(os.path.join(directory2, 'loners.txt'), 'w', encoding='utf-8') as lonerfile:
        for i in loners:
            lonerfile.write(i)
    with open(os.path.join(directory2, 'шаблоны.txt'), 'w', encoding='utf-8') as template_file:
        for i in template_numbers:
            template_file.write(lines[i] + '\n')
    m = statistics.mean(lens)
    mm = statistics.median(lens)
    print('mean/median cluster length: ', m, mm)
    if xlw:
        excel_copy_write.xl(clusters, loners, key_filename, lines)
    return 0


def batch_by_batch(key_pathname, threshold, batch_size, xlw):
    key_filename = os.path.basename(key_pathname)
    my_lines = path2lines(key_pathname)
    cnt = 1
    iterno = len(my_lines)// batch_size +1
    print(len(my_lines))
    print('iterno', iterno)
    while cnt <= iterno:
        lines = my_lines[batch_size*(cnt-1): batch_size*cnt]
        TSS(key_pathname + str(cnt), lines, threshold, xlw=xlw)
        cnt += 1


def execute(key_pathname, threshold):
    if os.path.isdir(key_pathname):
        for d in os.listdir(key_pathname):
            key_filename = os.path.basename(key_pathname)
            print('file', d)
            path = os.path.join(key_pathname, d)
            print('path', path)
            my_lines = path2lines(path)
            # TSS(os.path.join(key_filename, d), my_lines, threshold, xlw=1)
            print('len file', len(my_lines))
            if len(my_lines) <= 10000:
                TSS(os.path.join(key_filename, d), my_lines, threshold, xlw=1)
            else:
                print('batching')
                batch_by_batch(os.path.join(key_pathname, d), threshold=threshold, batch_size=10000, xlw=1)
    elif os.path.isfile(key_pathname):
        key_filename = os.path.basename(key_pathname)
        my_lines = path2lines(key_filename)
        TSS(key_filename,my_lines, threshold, xlw=1)



# pathname = 'C:\\Users\\ziswi\\PycharmProjects\\AdCluster\\регистрация в москве купить.txt'
# execute(pathname, threshold=4)



# batch_by_batch(pathname, batch_size=7000, threshold=4, xlw=1)

print("--- %s seconds ---" % (time.time() - start_time))

