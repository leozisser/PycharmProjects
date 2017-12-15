import os
import xlrd


def file_or_folder(name):
    abspaths = []
    if os.path.isdir(name):
        for i in os.listdir(name):
            file_or_folder(os.path.join(name,i))
    elif os.path.isfile(name):
        abspaths.append(os.path.abspath())
    return 0


def xl2lines(file):
    rb = xlrd.open_workbook(file)
    worksheet = rb.sheet_by_index(0)
    column_generator = (worksheet.row_values(i)[1] for i in range(worksheet.nrows))
    lines = list(column_generator)
    lines = [i for i in lines if i != '']
    return lines


def file2lines(path, lines):
    if path.endswith('.txt'):
        with open(path, 'r', encoding='utf-8')as file:
            templines = file.readlines()
            lines.extend(templines)
    elif path.endswith('.xls') or path.endswith('.xlsx'):
        templines = xl2lines(path)
        lines.extend(templines)
    else:
        print('unknown extension of file: ', path)


def path2lines(folder):
    lines = []
    if os.path.isdir(folder):
        for i in os.listdir(folder):
            # print(i)
            if os.path.isfile(os.path.join(folder, i)):
                path = os.path.join(folder, i)
                file2lines(path, lines)
    elif os.path.isfile(folder):
        file2lines(folder, lines)

    return lines
# print(len(path2lines('временная регистрация')))




