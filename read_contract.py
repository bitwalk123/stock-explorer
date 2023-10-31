from functions.read_csv import read_csv_contract_from_shiftjis

if __name__ == '__main__':
    csvname = '/home/bitwalk/ダウンロード/stockorder(JP)_20231030.csv'
    read_csv_contract_from_shiftjis(csvname)
