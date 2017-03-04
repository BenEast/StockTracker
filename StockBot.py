import sys, logging
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
        self.updateStockAverages()
    
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self):
        keys = self.sd.getKeyValues('stock')
        for key in keys:
            self.stocksToMonitor.append(key)
            
    # Attempt to get current price information for the stocks in the database.
    def monitor(self):
        for stockID in self.stocksToMonitor:
            yahoo = Share(stockID)
            try:
                self.postStockActivity(stockID, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in monitor:", sys.exc_info()[0])
    
    # Update the averages for every stock in the database
    def updateStockAverages(self):
        attributes = self.sd.getAttributeNamesNotKeys('stock')
        for stock_id in self.stocksToMonitor:
            for attr in attributes:
                average = self.sd.avgActivity(stock_id, attr)
                self.sd.updateStockAttribute(stock_id, attr, average)
    
    # Updates the stock_history table for the current date. 
    # Only meant to be used after trading is closed.
    def updateStockHistory(self):
        for stockID in self.stocksToMonitor:
            currentDate = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')[:10]
            yahoo = Share(stockID)
            avg = self.sd.getStockHistoryAverageValue(stockID, currentDate)
            
            self.postStockHistory(stockID, currentDate, yahoo.get_open(), avg, yahoo.get_price())
            
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID, avgOpen, avgDaily, avgClose):
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    # Add a new entry to the StockBot.stock_activity table.
    def postStockActivity(self, stockID, price):
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        self.sd.addStockActivity(stockID, currentDate, currentTime, price)

    # Add a new entry to the StockBot.stock_history table.
    # Only for use after trading hours; when the history table will be updated.
    def postStockHistory(self, stockID, currentDate, stockOpen, stockAvg, stockClose):
        self.sd.addStockHistory(stockID, currentDate, stockOpen, stockAvg, stockClose)
        