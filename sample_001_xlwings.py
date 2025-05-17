import xlwings as xw

if __name__ == '__main__':
    name_excel = 'daytrader.xlsx'
    wb = xw.Book(name_excel)
    sheet = wb.sheets['Sheet1']
    print(sheet[0, 0].value)
    print(sheet[0, 1].value)
    print(sheet[0, 2].value)
    print(sheet[0, 3].value)