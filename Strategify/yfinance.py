import yfinance as yf
from yfinance import shared
import pandas as pd

def getScripData(scripname,startdate,enddate):
    data = yf.download(scripname + ".NS", start=startdate, end=enddate)
    if shared._ERRORS:
        error_message = shared._ERRORS
    return data

def getScripChartsData(scripname,period):
    status = {}
    data = yf.download( tickers=scripname+".NS",period = period)
    if shared._ERRORS:
        error_message = shared._ERRORS
        status['error'] = error_message
        return status

    df = pd.DataFrame(data, columns = ['Close'], index = data.index)
    df['date'] = df.index.date
    status['success'] = df
    return status
