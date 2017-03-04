import sys
from time import time
from yahoo_finance import Share, YQLQueryError
from StockDB import StockDB
from datetime import datetime

# A "bot" to check for updates for stocks in the StockBot database and insert new information.
class StockBot:
    
    def __init__(self, stockDatabase: StockDB):
        try:
            self.sd = stockDatabase
            self.stocksToMonitor = []
            self.importStocksToMonitor()
        except:
            print("Unexpected error in StockBot init:", sys.exc_info()[0])
    
    # Actively monitors and updates stock information.
    def run(self):
        self.monitor()
        self.updateAverages()
    
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self):
        keys = self.sd.getKeyValues('stock')
        for key in keys:
            self.stocksToMonitor.append(key)
            
    # Attempt to get current price information for the stocks in the database.
    def monitor(self):
        for stock_id in self.stocksToMonitor:
            yahoo = Share(stock_id)
           
            try:
                self.postStockActivity(stock_id, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in monitor:", sys.exc_info()[0])
    
    # Update the averages for every stock in the database
    def updateAverages(self):
        attributes = self.sd.getAttributeNamesNotKeys('stock')
        for stock_id in self.stocksToMonitor:
            for attr in attributes:
                average = self.sd.avgActivity(stock_id, attr)
                self.sd.updateStockAttribute(stock_id, attr, average)
    
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID, avgOpen, avgDaily, avgClose):
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    # Add a new entry to the StockBot.stock_history table.
    def postStockActivity(self, stockID, price):
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        date = timestamp[:10]
        time = timestamp[11:]
        self.sd.addStockActivity(stockID, date, time, price)
