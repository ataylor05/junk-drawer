import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import talib as ta
import datetime



def cretateDataFrame(date_range, data_file):
    # Create empty dataframe
    df1 = pd.DataFrame(index=date_range)

    # Write CSV data into temporary dataframe
    dfTemp = pd.read_csv(data_file, index_col="OpenTime")

    # Join dataframes
    df1 = df1.join(dfTemp)
    
    return df1

def checkTradingConditions(df1, coefficients, sma, plt, symbol, now):
    price = df1.tail(1)["Close"][0]
    trend = coefficients[1]
    sma_point = sma[-1]
    print("Price Ending Point: " + str(price))
    print("Trend Line Ending Point: " + str(trend))
    print("SMA 50 Point: " + str(sma_point))

    if price > trend and price > sma_point:
        print("Enter trade")
        #plt.savefig("/home/jupyter/crypto/" + symbol + "/" + symbol + "-" + now.strftime("%m-%d-%Y") + ".jpg")
        plt.savefig("D:\\Jupyter_Notebooks\\crypto\\" + symbol + "\\" + symbol + "-" + now.strftime("%m-%d-%Y") + ".jpg")
        # Check if already in the trade
    else:
        print("Exit trade")
        #plt.show()

def main():
    # Define vars
    symbol = 'ETHUSDC'
    #data_file = "/home/jupyter/crypto/" + symbol + "/" + symbol + ".csv"
    data_file = "D:\\Jupyter_Notebooks\\crypto\\" + symbol + "\\" + symbol + ".csv"

    # Set rolling 60 day dates
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=61)
    end_date = now - datetime.timedelta(days=1)
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    date_range = pd.date_range(start, end)
    
    df1 = cretateDataFrame(date_range, data_file)

    # Trend line
    coefficients, residuals, _, _, _ = np.polyfit(range(len(df1.index)), df1['Close'],1, full=True)
    mse = residuals[0]/(len(df1.index))
    nrmse = np.sqrt(mse)/(df1['Close'].max() - df1['Close'].min())

    # SMA
    sma = ta.SMA(df1['Close'].values, timeperiod=50)

    # Plotting
    plt.figure(figsize=(20,10))
    plt.plot(df1['Close'].values, label='Price')
    plt.plot([coefficients[0]*x + coefficients[1] for x in range(len(df1))], label='Trendline')
    plt.plot(sma, label='50 MA')
    title = symbol + ' 50 MA and Trendline'
    plt.title(title)
    plt.legend(loc='best')

    checkTradingConditions(df1, coefficients, sma, plt, symbol, now)
    
if __name__ == "__main__":
    main()
