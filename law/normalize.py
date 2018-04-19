# -*- coding: utf-8 -*-
import json
import re
import operator
import pymorphy2
d = {}
d['nothing'] = 0
with open('test/test.txt', encoding='utf-8') as text:
    a = text.readlines()
    for line in a:
        codex = re.search('(?<=\d[\s\.])\D*?([Фф]едерации|РФ|России)', line)

        if codex:
            # print(line)
            a = codex.group(0).lower().lstrip().replace('  ', ' ')
            if a not in d:
                d[a] = 1
            else:
                d[a] += 1
        else:
            print(line)
            print('NOTHING FOUND')
            d['nothing']+=1
print(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
#get position in line with Match object: span

