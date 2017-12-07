import operator

from pymystem3 import Mystem
m = Mystem()
with open('key_phrases.txt', 'r', encoding='utf-8') as key:
    bagofwords = {}
    lines = key.readlines()
    k = ''
    for line in lines[:5]:
        """here goes my test"""
        k += line
    # print('k:', k)
    lemmas = m.lemmatize(k)
    print('lemmas: ',lemmas)
    k_m = (''.join(lemmas))
    print('k_m: ',k_m )


    """here it finishes"""

    #     lemmas = m.lemmatize(line)
    #     line_m = (''.join(lemmas))
    #     print(line_m)
    #     line_split = line_m.strip('\n').split(' ')
    #     for a in line_split:
    #         if a not in bagofwords:
    #             bagofwords[a] = 1
    #         elif a in bagofwords:
    #             bagofwords[a] += 1
    # bag_sorted = sorted(bagofwords.items(), key=operator.itemgetter(1), reverse=True )
    # print(bag_sorted)