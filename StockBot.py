import sys
from time import time, gmtime, strftime
from yahoo_finance import Share, YQLQueryError
from StockDB import StockDB
from datetime import datetime


class StockBot:
    
    def __init__(self, stockDatabase: StockDB):
        try:
            self.sd = stockDatabase
            self.stocksToMonitor = []
            self.importStocksToMonitor()
        except:
            print("Unexpected error in StockBot init:", sys.exc_info()[0])
    
    def monitor(self):
        for stock in self.stocksToMonitor:
            yahoo = Share(stock)
            
            try:
                self.postStockHistory(stock, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in monitor:", sys.exc_info()[0])
            
    def importStocksToMonitor(self):
        keys = self.sd.getKeys('stock')
        for key in keys:
            self.stocksToMonitor.append(key)
    
    def postStock(self, stockID, avgOpen, avgDaily, avgClose):
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    def postStockHistory(self, stockID, price):
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.sd.addStockHistory(stockID, timestamp, price)
