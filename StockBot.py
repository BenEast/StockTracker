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
    
    # Attempt to get current price information for the stocks in the database.
    def monitor(self):
        for stock in self.stocksToMonitor:
            yahoo = Share(stock)
            
            try:
                self.postStockHistory(stock, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in monitor:", sys.exc_info()[0])
            
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self):
        keys = self.sd.getKeys('stock')
        for key in keys:
            self.stocksToMonitor.append(key)
    
    def updateAverages(self):
        for stock_id in self.stocksToMonitor:
            average = self.sd.avgHistory(stock_id, 'daily')[0]
            self.sd.updateStockAttribute(stock_id, 'daily', average)
        
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID, avgOpen, avgDaily, avgClose):
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    # Add a new entry to the StockBot.stock_history table.
    def postStockHistory(self, stockID, price):
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.sd.addStockHistory(stockID, timestamp, price)

