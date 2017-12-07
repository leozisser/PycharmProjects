listt = ['a','b','c','d']


b = [a for a in range(len(listt))]
# print(b)
k = zip(listt, b)
print([f for f in k])
# a = dict(enumerate(listt))
# print(a)
def nexxt(list, elem):
    for elemm in list:
        print (elemm)
        print (elemm[0])

nexxt(k,'c' )