import matplotlib.pyplot as plt
import pandas as pd

from modules.psar import RealtimePSAR

if __name__ == "__main__":
    name_excel = '../excel/trader_20250526.xlsx'
    df = pd.read_excel(name_excel, sheet_name='tick_7011')

    list_trend = list()
    list_psar = list()

    psar = RealtimePSAR()
    for y in df['Price']:
        ret = psar.add(y)
        list_psar.append(ret.psar)
        list_trend.append(ret.trend)
    
    df['Trend'] = list_trend
    df['PSAR'] = list_psar

    df_bull = df[df['Trend'] == 1][['Time', 'PSAR']]
    df_bear = df[df['Trend'] == -1][['Time', 'PSAR']]

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["Time"], df["Price"], color="black", linewidth=0.5)
    ax.scatter(x=df_bull['Time'], y=df_bull['PSAR'], s=5, c="red")
    ax.scatter(x=df_bear['Time'], y=df_bear['PSAR'], s=5, c="blue")
    ax.grid()
    plt.show()
