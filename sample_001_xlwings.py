import xlwings as xw

terminator = '------'

if __name__ == '__main__':
    name_excel = 'daytrader.xlsx'
    wb = xw.Book(name_excel)
    sheet = wb.sheets['Sheet1']

    col_code = 0
    col_name = 1
    col_date = 2
    col_time = 3
    col_price = 4
    col_price_prev = 5

    r = 0
    print(sheet[r, col_code].value)
    print(sheet[r, col_name].value)
    print(sheet[r, col_date].value)
    print(sheet[r, col_time].value)
    print(sheet[r, col_price].value)
    print(sheet[r, col_price_prev].value)

    while True:
        r += 1
        val_code = sheet[r, col_code].value
        val_price = sheet[r, col_price].value
        if val_code == terminator:
            break
        else:
            print(val_code, val_price)

    n = r
    print('terminator row', n)