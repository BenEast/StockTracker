import sys, logging
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
            logging.warning("Unexpected error in StockBot init:", sys.exc_info()[0])
            
        logging.info("StockBot initialized.\n")
        
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self) -> None:
        keys = self.sd.getKeyValues("stock")
        for key in keys:
            self.stocksToMonitor.append(key)
            
    # Attempt to get current price information for the stocks in the database.
    def monitor(self) -> None:
        logging.info("StockBot.monitor() called.")
        
        for stockID in self.stocksToMonitor:
            try:
                yahoo = Share(stockID)
                self.postStockActivity(stockID, yahoo.get_price())
            except YQLQueryError:
                print("Yahoo finance is currently unavailable.")
                logging.warning("Yahoo finance is currently unavailable.")
            except:
                print("Unexpected error in StockBot.monitor():", sys.exc_info()[0])
                logging.warning("Unexpected error in StockBot.monitor():", sys.exc_info()[0])
                
        logging.info("StockBot.monitor() completed.\n")
        
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID: str) -> None:
        logging.info("StockBot.postStock() called.")
        self.sd.addStock(stockID, 0, 0, 0)
        logging.info("StockBot.postStock() completed.\n")
        
    # Add a new entry to the StockBot.stock_activity table.
    def postStockActivity(self, stockID: str, price: float) -> None:
        logging.info("StockBot.postStockActivity() called.")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        self.sd.addStockActivity(stockID, currentDate, currentTime, price)

        logging.info("StockBot.postStockActivity() completed.\n")
        
    # Updates the stock_history table for the current date. 
    # Only meant to be used after trading is closed.
    def postStockHistory(self) -> None:
        logging.info("StockBot.postStockHistory() called.")
        
        for stockID in self.stocksToMonitor:
            currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
            average = self.sd.getStockHistoryAverageValue(stockID, currentDate)
            yahoo = Share(stockID)
            
            self.sd.addStockHistory(stockID, currentDate, yahoo.get_open(), average, 
                                    yahoo.get_price(), yahoo.get_days_high(), yahoo.get_days_low())

        logging.info("StockBot.postStockHistory() completed.\n")
    
    # Removes the given stockID from all tables, or just the stock table based on allTables.
    def removeStock(self, stockID: str, allTables: bool) -> None:   
        logging.info("StockBot.removeStock() called.")
         
        if allTables:
            for table in self.sd.getTablesWithAttribute('stock_id'):
                self.sd.deleteFromTable(table, stockID)
        else:
            self.sd.deleteFromTable("stock", stockID)
            
        logging.info("StockBot.removeStock() completed.\n")
        
    # Actively monitors and updates stock information.
    def run(self) -> None:
        self.monitor()
        self.updateStockAverages()

    # Update the averages for every stock in the database
    def updateStockAverages(self) -> None:
        logging.info("StockBot.updateStockAverages() called.")
        
        attributes = self.sd.getAttributeNamesNotKeys("stock")
        for stockID in self.stocksToMonitor:
            for attr in attributes:
                averageDaily = self.sd.getAverageStock(attr, stockID)
                self.sd.updateTableAttribute('stock', attr, averageDaily, stockID)
                
        logging.info("StockBot.updateStockAverages() completed.\n")
