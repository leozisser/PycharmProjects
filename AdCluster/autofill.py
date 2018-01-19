import os
import xlrd
import re
import numpy as np
import itertools
import pandas as pd
import operator

def freqdict(array):
    dic = {}
    for i in array:
        if i not in dic:
            dic[i] = 1
        else:
            dic[i] += 1
    # print(dic)
    unique_list = [i for i in dic if '#' not in i]
    return unique_list

# link = input('input link: ')
# group = input('group name: ')
link = 'C:\\Users\ziswi\PycharmProjects\AdCluster\campaigns'
group = 'registracii'
regex = re.compile('[А-Я].+?(?=\s[А-Я]|$)')
o2 = []
o3 = []
for file in os.listdir(link):
    if file.endswith('.xls') or file.endswith('.xlsx'):
        rb = xlrd.open_workbook(os.path.join(link, file))
        sheet = rb.sheet_by_index(0)
        objav2 = [sheet.cell_value(row, 12) for row in range(sheet.nrows)][11:]
        for i in objav2:
            k = re.findall(pattern=regex, string=i)
            o2.extend(k)
        objav3 = [sheet.cell_value(row, 13) for row in range(sheet.nrows)][11:]
        for j in objav3:
            k = re.findall(pattern=regex, string=j)
            o3.extend(k)

o2_ = freqdict(o2)
o3_ = freqdict(o3)
# print(o2_)
# print(o3_)
# print('o3_: ', len(o3_), ' o2_: ', len(o2_))
os.makedirs(os.path.join('campaigns', 'results'), exist_ok=True)
with open('campaigns\\results\\' + group + '.txt', 'w', encoding='utf-8') as examples:
    examples.write('\t'.join(o2_) + '\n')
    examples.write('\t'.join(o3_))

# xlrd.open_workbook
# C:\Users\ziswi\PycharmProjects\AdCluster\campaigns
'''uncomment block if we want punctuation gone'''
# for index, el in enumerate(o2_):
#     if el.endswith('!') or el.endswith('?'):
#         # print(el)
#         o2_[index] = el.strip('?!')
# print(o2_)
# print(len(o2_))
combinations = list(itertools.product(o2_, o2_))
print(len(combinations))

# for n, a in enumerate(combinations):
#     if a[0] == a[1]:
#         combinations.pop(n)
# print(len(combinations))
# print(combinations)
# liss = [e[0] +' '+ e[1] for e in combinations]
# dicc = {a:len(a) for a in liss}
# print(dicc)


# print(len(combinations))
comb = [len(a[0]) + len(a[1]) + 1  for a in combinations]
numdata = np.array(comb).reshape(len(o2_), len(o2_))
df2 = pd.DataFrame(index=o2_, columns=o2_, data=numdata)
# print(df2)
for y,x in enumerate(df2):
    # print('y',y)
    for i in range (y+1):
        df2.iloc[y][i] = 100

# print(df2.T)
size = 10
testframe = pd.DataFrame(columns=['phrase', 'adv2', 'adv3 ', 'sum'], index=range(size))
testframe['phrase'] = np.random.randint(low=25, high=35, size=size)
# testframe['adv2'] = 55 - testframe['phrase']
print(testframe)
# filtered = (df2[df2 < 27 ])
# print('filtered',filtered)

def findbest(i):
    n = 55 - i
    print('.N',n)
    a = df2.where(df2 < n).stack().to_dict()
    phrase = max(a.items(), key=operator.itemgetter(1))[0]
    text = phrase[0] + ' ' + phrase[1]
    return text

for index, i in enumerate(testframe['phrase']):
    print(i)
    print(index)
    testframe["adv2"].iloc[index] = findbest(i)
print(testframe)
