import xlrd
import os
import itertools
import tss_cluster


def create(file):
    # basename = os.path.basename(file)
    rb = xlrd.open_workbook(file)
    sheet = rb.sheet_by_index(0)
    data1 = [sheet.cell_value(row, 0) for row in range(sheet.nrows)][1:]
    data2 = [i for i in[sheet.cell_value(0,col) for col in range(sheet.ncols)][1:] if i != 'частотность']
    combinations = list(itertools.product(data1, data2))
    k = [(i[0] + ' ' + i[1].strip(' ')) for i in combinations]
    # print(data1)
    # print(data2)
    print(k)
    return k

xl = 'C:\\Users\\ziswi\\PycharmProjects\\AdCluster\\parse'
for f in os.listdir(xl):
    print(f)
    kk = create(os.path.join(xl,f))
    tss_cluster.TSS(f, my_lines=kk, threshold=3, xlw=1)


# print(create(xl))
