import sys
from StockDB import StockDB
from datetime import datetime
from time import time

class StockBot:
    
    def __init__(self, stockDatabase):
        try:
            self.sd = stockDatabase
            self.stocksToMonitor = []
            self.getStocksToMonitor()
        except:
            print("Unexpected error in StockBot init:", sys.exc_info()[0])
    
    def monitor(self):
        self.getStocksToMonitor()
        # monitor and upload data as necessary
        
    def getStocksToMonitor(self):
        for stockID in self.sd.getKeys():
            self.stocksToMonitor.append(stockID)
    
    def postStock(self, stockID, avgOpen, avgDaily, avgClose):
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    def postStockHistory(self, stockID, dayOpen, dayMid, dayClose):
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.sd.addStockHistory(stockID, dayOpen, dayMid, dayClose, timestamp)

sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
sb = StockBot(sd)
print(sb.stocksToMonitor)