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
    
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self) -> None:
        keys = self.sd.getKeyValues('stock')
        for key in keys:
            self.stocksToMonitor.append(key)
            
    # Attempt to get current price information for the stocks in the database.
    def monitor(self) -> None:
        for stockID in self.stocksToMonitor:
            yahoo = Share(stockID)
            try:
                self.postStockActivity(stockID, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in monitor:", sys.exc_info()[0])
            
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID: str, avgOpen: float, avgDaily: float, avgClose: float) -> None:
        self.sd.addStock(stockID, avgOpen, avgDaily, avgClose)
        
    # Add a new entry to the StockBot.stock_activity table.
    def postStockActivity(self, stockID: str, price: float) -> None:
        timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        self.sd.addStockActivity(stockID, currentDate, currentTime, price)

    # Updates the stock_history table for the current date. 
    # Only meant to be used after trading is closed.
    def postStockHistory(self) -> None:
        for stockID in self.stocksToMonitor:
            currentDate = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')[:10]
            yahoo = Share(stockID)
            average = self.sd.getStockHistoryAverageValue(stockID, currentDate)
            
            self.sd.addStockHistory(stockID, currentDate, yahoo.get_open(), average, 
                                    yahoo.get_price(), yahoo.get_days_high(), yahoo.get_days_low())

    # Actively monitors and updates stock information.
    def run(self) -> None:
        self.monitor()
        self.updateStockAverages()

    # Update the averages for every stock in the database
    def updateStockAverages(self) -> None:
        attributes = self.sd.getAttributeNamesNotKeys('stock')
        for stockID in self.stocksToMonitor:
            for attr in attributes:
                averageDaily = self.sd.getAverageStock(attr, stockID)
                self.sd.updateTableAttribute('stock', stockID, attr, averageDaily)
                