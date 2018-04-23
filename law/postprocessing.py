import json
import re
from itertools import chain
from operator import itemgetter
#
# a = [{'article': '283 - 285 и  290', 'source': {'name': 'АПК', 'type': 'codex'}}, {'punkt': '1', 'part': '1', 'article': '287'}]
# b = [{ 'article': '90.3, 90.4', 'source': {'name': 'АПК', 'type': 'codex'}},{'punkt': '1', 'part': '1', 'article': '287'}]
# c = json.loads(json.dumps([
#   {
#     "article": "110, 167-171, 176-177, 180-182",
#     "type": "codex",
#     "name": "АПК"
#   }
# ]))
'''THIS IS A LIBRARY FOR EXTRACT.PY. It provides postprocessing functions.
THE FUNCTION BELOW:'''

'''looks for multiple numbers in object, returns category'''


def multiparser(obj):
    k = ''
    for key, val in obj.items():
        if key !='source' and not re.match('^\s?\d+\.?\d*$', val):
            # print(key, val)
            k = key
    return k

'''adds 'source' to instances in object that do not have it;
 also assigns 'name':'UNKNOWN' to objects where 'code' is not explicitly shown; 'Type: 'codex' is hardcoded'''


def codeadder(obj):
    for number, ins in enumerate(obj):
        if 'source' in ins.keys():
            k = number
            # print (number)
            for mat in obj:
                mat['source'] = obj[k]['source']
        else:
            ins['source'] = {'name': 'UNKNOWN', 'type': 'codex'}
    return obj


'''generates new json objects for multiple numbers'''


def json_generator(obj, position, number, target):
    newobj = {}
    for key, value in obj[position].items():
        newobj[key] = value
    newobj[target] = number
    return newobj
# print(a, json_generator(a,127, 'article'))


'''receives  multiple numbers delimited by comma or dash, returns range'''


def parse_range(rng):
    parts = rng.split('-')
    # print('prarts',parts)
    if 1 > len(parts) > 2:
        raise ValueError("Bad range: '%s'" % (rng,))
    parts = [int(i) for i in parts]  # CAREFUL! WILL CRASH IF PARSING RANGE OF xx.x ITEMS!
    start = parts[0]
    # print(start)
    end = start if len(parts) == 1 else parts[1]
    if start > end:
        end, start = start, end
    return range(start, end + 1)


def parse_range_list(rngs):
    return sorted(set(chain(*[parse_range(rng.lstrip()) for rng in rngs.replace('и',',').split(',')])))\
        if not re.match('\d+\.\d*', rngs)\
        else rngs.replace('и',',').replace(' ','').split(',')


''' combines created jsons '''


def final(array):
    lin = []
    print(array)
    for number, i in enumerate(array):
        k = multiparser(array[number])
        # print ('k', k)
        if k:
            artlist = (parse_range_list(array[number][k]))
            newart = [json_generator(array, number, art, k) for art in artlist]
            lin.append(newart)
        else:
            # print('no multi', i)
            ll = [i]
            # print(ll)
            lin.append(ll)
            # print('lin',lin)
    line = (list(chain(*lin)))
    # line_= sorted(line,key=itemgetter('article'))
    # print('line:',line)
    return line

'''assigns all possible numbers as ints or floats to make sorting possible'''


def intifada(obj):
    for zapis in obj:
        for key, val in zapis.items():
            if key != 'source' and not isinstance(val, int):
                try:
                    zapis[key] = int(val)
                except ValueError:
                    zapis[key] = float(val)
    return obj


'''finalizes, sorts and prettifies object'''


def pretty(line):
    finalize = final(line)
    intified = intifada(finalize)
    withcode = codeadder(intified)
    try:
        theline = (sorted(withcode, key=itemgetter('article'))) #остальное почти не надо сортировать
    except KeyError:
        theline = withcode

    return theline
