# -*- coding: utf-8 -*-
import xlwt, xlrd
from xlutils.copy import copy
import xlutils
from unidecode import unidecode
import os


def xl(clusters, loners, filename, lines):
    print('filename', filename)
    basename = os.path.basename(filename)
    template_name = "direct_example"
    # name = 'временная регистрация московская область'
    uniname = unidecode(filename).strip('txls').strip('.').replace(' ', '_')
    savename = filename.strip('txls').strip('.')
    link = 'http://ooo-777.moscow/?utm_source=yandex_poisk&utm_medium=cpc&utm_term={keyword}&utm_content={position}/{position_type}&utm_campaign='+ uniname +'&type={source_type}&source={source}'
    # print(len(loners))
    totalgroups = len(clusters) + len(loners)
    campname = basename.strip('txtlscsv').strip('.')
    print('campname', campname)
    rb = xlrd.open_workbook(template_name + '.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    wb = xlutils.copy.copy(rb)
    s = wb.get_sheet(0)
    data = [sheet.cell_value(12, col) for col in range(sheet.ncols)]
    for i in range(totalgroups):
        for index, value in enumerate(data):
            s.write(12 + i, index, value)
    counter = 0
    groupid = 0
    s.write(11 + counter, 4, 'шаблоны')
    s.write(11 + counter, 5, str(groupid))
    s.write(11 + counter, 11, '#' + campname + '#')
    counter += 1
    groupid +=1
    for a in sorted(clusters):
        if a != 'шаблоны':
            for line_no in clusters[a]:
                s.write(11 + counter, 4, a)
                s.write(11 + counter, 5, str(groupid))
                s.write(11 + counter, 8, lines[line_no])
                s.write(11+counter, 17, link)
                counter += 1
            groupid += 1
    for b in loners:
        s.write(11 + counter, 8, b)
        s.write(11 + counter, 17, link)
        counter += 1
    savepath = 'clustered//'+savename + '//кампания ' + campname + '.xls'
    wb.save(savepath)
    print('xl created at ', savepath )
    return 0
