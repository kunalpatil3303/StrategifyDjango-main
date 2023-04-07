import pandas as pd
from .views import *


def ProfitLossCalculationWithoutExit(data, username, scrip, target, steploss, quantity):
    a = 0
    status = 0
    WinsCount = LossCount = 0               # TOTAL NO OF WINS AND LOSS
    totalProfit = totalLoss = 0             # TOTAL PROFIT AND LOSS
    balance = 0                             # NET BALANCE
    enter = 0                               # VARIABLE FOR TO CHECK
    PS = PL = 0                             # VARIABLE FOR CALCULATING NO OF STREAK
    streakProfit = streakLoss = 0           # NO OF PROFIT AND LOSS STREAK
    graphdata = []                          # STORING BUY/SELL DATA
    alllist = []                            # LIST TO STORE ALL GATHERED DATA

    for i in range(0, len(data['Position'])):
        x = []
        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            alllist.append({'date': data.index[i], 'price': data['Close'][i], 'buysell': "buy", 'balance': balance, })
            x.append(str(data.index[i]))
            x.append("{:.2f}".format(data['Close'][i]))
            graphdata.append(x)
            print("Buy:    Date: ", data.index[i], " Price: ", a)
        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                          data['Close'][i] - a)
                    WinsCount += 1
                    totalProfit += data['Close'][i] - a
                    alllist.append(
                        {'date': data.index[i], 'price': data['Close'][i], 'buysell': "sell", 'balance': balance})
                    PS += 1
                    PL = 0
                    if PS > streakProfit:
                        streakProfit = PS
                    a = 0
                    enter = 0
                    x.append(str(data.index[i]))
                    x.append("{:.2f}".format(data['Close'][i]))
                    graphdata.append(x)
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                          data['Close'][i] - a)
                    LossCount += 1
                    totalLoss += data['Close'][i] - a
                    alllist.append(
                        {'date': data.index[i], 'price': data['Close'][i], 'buysell': "sell", 'balance': balance, })
                    PL += 1
                    PS = 0
                    if PL > streakLoss:
                        streakLoss = PL
                    a = 0
                    enter = 0
                    x.append(str(data.index[i]))
                    x.append("{:.2f}".format(data['Close'][i]))
                    graphdata.append(x)

    print("Balance: ", balance, " Total Wins: ", WinsCount, " Total Loss: ", LossCount, " Total Profit:  ", totalProfit,
          " Total Loss: ", totalLoss)

    if totalProfit + totalLoss > 0:
        status = 1


    LTP = 0.0
    if len(data['Close']) > 0:
        LTP = data['Close'][-1]  # LAST TRADE PRICE

    pd.DataFrame(alllist).to_csv('static/GeneratedFile/' + '' + username + '' + scrip.replace('.NS', '') + '.csv')
    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totalProfit = "{:.2f}".format(totalProfit)
    totalLoss = "{:.2f}".format(-totalLoss)
    LTP = "{:.2f}".format(float(LTP))

    if WinsCount != 0 and LossCount != 0:
        AvgGain = "{:.2f}".format(float(totalProfit) * int(quantity) / WinsCount)
        AvgLoss = "{:.2f}".format(float(totalLoss) * int(quantity) / LossCount)
    elif WinsCount == 0 and LossCount != 0:
        AvgGain = 0
        AvgLoss = "{:.2f}".format(float(totalLoss) * int(quantity) / LossCount)
    elif WinsCount != 0 and LossCount != 0 and totalProfit != 0.0 and totalLoss != 0.0:
        AvgGain = "{:.2f}".format(float(totalProfit) * int(quantity) / WinsCount)
        AvgLoss = "{:.2f}".format(float(totalLoss) * int(quantity) / LossCount)
    else:
        AvgLoss = 0
        AvgGain = 0

    if float(totalProfit) == 0.00 and float(totalLoss) == 0.00:
        percentBar = 0
    else:
        percentBar = (float(totalProfit) / (float(totalProfit) + float(totalLoss))) * 100
    alldata = {
        'username': username,
        'ScripName': scrip.replace('.NS', ''),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Quantity': quantity,
        'Status': status,
        'LTP': LTP,
        'Signal': WinsCount + LossCount,
        'WinStreak': streakProfit,
        'LossStreak': streakLoss,
        'Wins': WinsCount,
        'Loss': LossCount,
        'MaxGain': "{:.2f}".format(float(totalProfit) * int(quantity)),
        'MaxLoss': "{:.2f}".format(float(totalLoss) * int(quantity)),
        'PeriodHigh': periodHigh,
        'PeriodLow': periodLow,
        'AvgGain': AvgGain,
        'AvgLoss': AvgLoss,
        'PercentBar': percentBar,
        'graphdata': graphdata,
    }
    return alldata


def ProfitLossCalculationWithExit(data, username, scrip, target, steploss, quantity):
    a = 0
    status = 0
    WinsCount = LossCount = 0  # TOTAL NO OF WINS AND LOSS
    totalProfit = totalLoss = 0  # TOTAL PROFIT AND LOSS
    balance = 0  # NET BALANCE
    enter = 0  # VARIABLE FOR TO CHECK
    PS = PL = 0  # VARIABLE FOR CALCULATING NO OF STREAK
    streakProfit = streakLoss = 0  # NO OF PROFIT AND LOSS STREAK
    graphdata = []  # STORING BUY/SELL DATA
    alllist = []  # LIST TO STORE ALL GATHERED DATA

    for i in range(0, len(data['Position'])):
        x = []

        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            alllist.append({
                'date': data.index[i],
                'price': data['Close'][i],
                'buysell': "buy",
                'balance': balance,
            })
            x.append(str(data.index[i]))
            x.append("{:.2f}".format(data['Close'][i]))
            graphdata.append(x)
            print("Buy:    Date: ", data.index[i], " Price: ", a)
        elif data['Position'][i] == -1.0 and enter == 1:
            balance += data['Close'][i] - a
            if data['Close'][i] - a >= 0:
                print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                      data['Close'][i] - a)
                WinsCount += 1
                totalProfit += data['Close'][i] - a
                alllist.append({
                    'date': data.index[i],
                    'price': data['Close'][i],
                    'buysell': "sell",
                    'balance': balance
                })
                x.append(str(data.index[i]))
                x.append("{:.2f}".format(data['Close'][i]))
                graphdata.append(x)
                PS += 1
                PL = 0
                if PS > streakProfit:
                    streakP = PS
                a = 0
                enter = 0
            else:
                print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                      data['Close'][i] - a)
                LossCount += 1
                totalLoss += data['Close'][i] - a
                alllist.append({
                    'date': data.index[i],
                    'price': data['Close'][i],
                    'buysell': "sell",
                    'balance': balance
                })
                x.append(str(data.index[i]))
                x.append("{:.2f}".format(data['Close'][i]))
                graphdata.append(x)
                PL += 1
                PS = 0
                if PL > streakLoss:
                    streakLoss = PL
                a = 0
                enter = 0
        else:
            if a > 0 and enter == 1:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                          data['Close'][i] - a)
                    WinsCount += 1
                    totalProfit += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i],
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    x.append(str(data.index[i]))
                    x.append("{:.2f}".format(data['Close'][i]))
                    graphdata.append(x)
                    PS += 1
                    PL = 0
                    if PS > streakProfit:
                        streakProfit = PS
                    a = 0
                    enter = 0
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                          data['Close'][i] - a)
                    LossCount += 1
                    totalLoss += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i],
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    x.append(str(data.index[i]))
                    x.append("{:.2f}".format(data['Close'][i]))
                    graphdata.append(x)
                    PL += 1
                    PS = 0
                    if PL > streakLoss:
                        streakLoss = PL
                    a = 0
                    enter = 0

    print("Balance: ", balance, " Total Wins: ", WinsCount, " Total Loss: ", LossCount, " Total Profit:  ", totalProfit,
          " Total Loss: ", totalLoss)

    if totalProfit + totalLoss > 0:
        status = 1

    LTP = 0.0
    if len(data['Close']) > 0:
        LTP = data['Close'][-1]  # LAST TRADE PRICE

    pd.DataFrame(alllist).to_csv('static/GeneratedFile/' + '' + username + '' + scrip.replace('.NS', '') + '.csv')
    periodHigh = "{:.2f}".format(data['Close'].max())
    periodLow = "{:.2f}".format(data['Close'].min())
    balance = "{:.2f}".format(balance)
    totalProfit = "{:.2f}".format(totalProfit)
    totalLoss = "{:.2f}".format(-totalLoss)
    LTP = "{:.2f}".format(float(LTP))

    if WinsCount == 0:
        AvgGain = 0
        AvgLoss = "{:.2f}".format(float(totalLoss) * int(quantity) / LossCount)
    elif LossCount == 0:
        AvgLoss = 0
        AvgGain = "{:.2f}".format(float(totalProfit) * int(quantity) / WinsCount)
    elif WinsCount != 0 and LossCount != 0 and totalProfit != 0.0 and totalLoss != 0.0:
        AvgGain = "{:.2f}".format(float(totalProfit) * int(quantity) / WinsCount)
        AvgLoss = "{:.2f}".format(float(totalLoss) * int(quantity) / LossCount)
    else:
        AvgLoss = 0
        AvgGain = 0


    percentBar = (float(totalProfit) / (float(totalProfit) + float(totalLoss))) * 100
    alldata = {
        'username': username,
        'ScripName': scrip.replace('.NS', ''),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Quantity': quantity,
        'Status': status,
        'Signal': WinsCount + LossCount,
        'LTP': LTP,
        'WinStreak': streakProfit,
        'LossStreak': streakLoss,
        'Wins': WinsCount,
        'Loss': LossCount,
        'MaxGain': "{:.2f}".format(float(totalProfit) * int(quantity)),
        'MaxLoss': "{:.2f}".format(float(totalLoss) * int(quantity)),
        'PeriodHigh': periodHigh,
        'PeriodLow': periodLow,
        'AvgGain': AvgGain,
        'AvgLoss': AvgLoss,
        'PercentBar': percentBar,
        'graphdata': graphdata,
    }
    return alldata
