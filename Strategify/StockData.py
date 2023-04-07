import requests

class NSE:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/97.0.4692.99 Safari/537.36'}
        self.session = requests.Session()
        self.session.get('http://nseindia.com', headers=self.header)

    def marketstatus(self):
        return self.session.get(f"https://www1.nseindia.com//emerge/homepage/smeNormalMktStatus.json",
                                   headers=self.header).json()


    def allscrip(self):
        data = self.session.get(f"https://www1.nseindia.com/homepage/peDetails.json",
                                   headers=self.header).json()
        allscrip = []

        # for key in data.keys():
        #     allscrip.append(str(key)+".NS")

        for key in data.keys():
            allscrip.append(str(key))
            
        return allscrip

    def topgainers(self):
        data = self.session.get(f"https://www1.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json",
                                    headers=self.header).json()
        return data

    def toplosers(self):
        data = self.session.get(f"https://www1.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json",
                                    headers=self.header).json()
        return data

    def allindex(self):
        data = self.session.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/liveIndexWatchData.json",
                                    headers=self.header).json()
        return data

    def getscripdata(self,symbol,start,end):
        print(start,end)
        data = self.session.get(f" https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22EQ%22]&from="+start+"&to="+end,
                                    headers=self.header).json()
        return data