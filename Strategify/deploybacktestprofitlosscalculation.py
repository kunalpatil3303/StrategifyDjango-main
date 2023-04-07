from .views import *

def deployprofitLossCalculationWithoutExit(data, strategyname, scrip, target, steploss, quantity, algocycles, deploydate):
    a = 0
    status = 0                              # TOTAL NO OF WINS AND LOSS
    totalProfit = totalLoss = 0             # TOTAL PROFIT AND LOSS
    balance = 0                             # NET BALANCE
    enter = 0                               # VARIABLE FOR TO CHECK
    alllist = []                            # LIST TO STORE ALL GATHERED DATA
    waitenter = "WAIT"                      # CHECK WHETHER WAIT/ENTERED STATE
    cyclescount = 0                         # CHECK ALGOCYCLES

    for i in range(0, len(data['Position'])):
        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            waitenter = "ENTER"
            alllist.append({'date': data.index[i].strftime('%d%b%Y'), 'price': data['Close'][i], 'buysell': "buy", 'balance': balance, })
            print("Buy:    Date: ", data.index[i], " Price: ", a)
        else:
            if a > 0:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    waitenter = "WAIT"
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                          data['Close'][i] - a)
                    totalProfit += data['Close'][i] - a
                    alllist.append(
                        {'date': data.index[i].strftime('%d%b%Y'), 'price': data['Close'][i], 'buysell': "sell", 'balance': balance})
                    a = enter = 0
                    cyclescount += 1
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    waitenter = "WAIT"
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                          data['Close'][i] - a)
                    totalLoss += data['Close'][i] - a
                    alllist.append(
                        {'date': data.index[i].strftime('%d%b%Y'), 'price': data['Close'][i], 'buysell': "sell", 'balance': balance, })
                    a = enter = 0
                    cyclescount += 1
        if cyclescount == int(algocycles):
            waitenter = "STOP"
            break

    print("Balance: ", balance, " Total Profit:  ", totalProfit, " Total Loss: ", totalLoss)

    if balance > 0:
        status = 1

    LTP = 0.0
    if len(data['Close'])!=0:
        LTP = data['Close'][-1]  # LAST TRADE PRICE

    balance = "{:.2f}".format(balance)
    LTP = "{:.2f}".format(float(LTP))

    alldata = {
        'strategyname': strategyname,
        'ScripName': scrip.replace('.NS', ''),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Status': status,
        'LTP': LTP,
        'target':target,
        'waitenter':waitenter,
        'deploydate':deploydate,
        'graphdata': alllist,
        'cyclescount':str(cyclescount),
        'quantity':str(quantity),
        'algocycles':str(algocycles),
    }
    return alldata

def deployprofitLossCalculationWithExit(data, strategyname, scrip, target, steploss, quantity, algocycles, deploydate):
    a = 0
    status = 0
    totalProfit = totalLoss = 0     # TOTAL PROFIT AND LOSS
    balance = 0                     # NET BALANCE
    enter = 0                       # VARIABLE FOR TO CHECK
    alllist = []                    # LIST TO STORE ALL GATHERED DATA
    waitenter = "WAIT"
    cyclescount = 0

    for i in range(0, len(data['Position'])):
        if data['Position'][i] == 1.0 and enter == 0:
            a = data['Close'][i]
            enter = 1
            alllist.append({
                'date': data.index[i].strftime('%d%b%Y'),
                'price': data['Close'][i],
                'buysell': "buy",
                'balance': balance,
            })
            waitenter = "ENTER"
            print("Buy:    Date: ", data.index[i], " Price: ", a)
            print("TimeStamp Date: ",data.index[i].strftime('%d%b%Y'))
        elif data['Position'][i] == -1.0 and enter == 1:
            balance += data['Close'][i] - a
            if data['Close'][i] - a >= 0:
                print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                      data['Close'][i] - a)
                totalProfit += data['Close'][i] - a
                alllist.append({
                    'date': data.index[i].strftime('%d%b%Y'),
                    'price': data['Close'][i],
                    'buysell': "sell",
                    'balance': balance
                })
                waitenter = "WAIT"
                a = enter = 0
                cyclescount += 1
            else:
                print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                      data['Close'][i] - a)
                totalLoss += data['Close'][i] - a
                alllist.append({
                    'date': data.index[i].strftime('%d%b%Y'),
                    'price': data['Close'][i],
                    'buysell': "sell",
                    'balance': balance
                })
                waitenter = "WAIT"
                a = enter = 0
                cyclescount += 1
        else:
            if a > 0 and enter == 1:
                if ((data['Close'][i] - a) / a) * 100 >= int(target):
                    balance += data['Close'][i] - a
                    print("Sell:   Profit  Price: ", data['Close'][i], " Date: ", data.index[i], " Net Profit: ",
                          data['Close'][i] - a)
                    totalProfit += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i].strftime('%d%b%Y'),
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    cyclescount += 1
                    waitenter = "WAIT"
                    a = enter = 0
                elif ((a - data['Close'][i]) / a) * 100 >= int(steploss):
                    balance += data['Close'][i] - a
                    print("Sell:   Loss   Price: ", data['Close'][i], " Date: ", data.index[i], " Net Loss: ",
                          data['Close'][i] - a)
                    totalLoss += data['Close'][i] - a
                    alllist.append({
                        'date': data.index[i].strftime('%d%b%Y'),
                        'price': data['Close'][i],
                        'buysell': "sell",
                        'balance': balance
                    })
                    waitenter = "WAIT"
                    a = enter = 0
                    cyclescount += 1

        if cyclescount == int(algocycles):
            waitenter = "STOP"
            break

    print("Balance: ", balance, " Total Profit:  ", totalProfit," Total Loss: ", totalLoss)

    if balance > 0:
        status = 1
    elif balance < 0:
        status = -1

    LTP = 0.0
    if len(data['Close'])!=0:
        LTP = data['Close'][-1]  # LAST TRADE PRICE

    balance = "{:.2f}".format(balance)
    LTP = "{:.2f}".format(float(LTP))


    alldata = {
        'strategyname': strategyname,
        'ScripName': scrip.replace('.NS', ''),
        'PL': "{:.2f}".format(float(balance) * int(quantity)),
        'Status': status,
        'LTP': LTP,
        'target':target,
        'waitenter':waitenter,
        'deploydate': deploydate,
        'graphdata': alllist,
        'cyclescount':str(cyclescount),
        'quantity':str(quantity),
        'algocycles':str(algocycles)
    }
    return alldata
