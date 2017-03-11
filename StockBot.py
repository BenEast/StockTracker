import sys, logging
from yahoo_finance import Share, YQLQueryError
from StockQueries import *
from StockDB import StockDB
from datetime import datetime

# Helper data structure to store keys and attributes of a table.
class tableAttributes:
    def __init__(self, keys, attrs):
        self.keys = keys
        self.attributes = attrs

    def getAttributes(self):
        return self.attributes

    def getKeys(self):
        return self.keys

# A "bot" to check for updates for stocks in the StockBot database and insert new information.
class StockBot:
    
    def __init__(self, stockDatabase: StockDB):
        try:
            self.sd = stockDatabase
            self.stocksToMonitor = []
            self.tableDict = dict()
            self.importTableAttributes()
            self.importStocksToMonitor()
        except:
            logging.warning("Unexpected error in StockBot init:", sys.exc_info()[0])
        
    # Converts a list of attributes to a comma delimted string
    def _attrsToString(self, attrs: list) -> str:
        out = ""
        for a in attrs:
            out = out + a + ", "
        
        return out[:len(out) - 2]
    
    # Import the stock_id keys from the StockBot.stock table.
    def importStocksToMonitor(self) -> None:
        self.stocksToMonitor.clear()
        query = StockQueries.getKeyValuesQuery().format("stock_id", "stock")
        self.stocksToMonitor = self.sd.getKeyValues(query)
    
    # Imports the tables, keys, and attributes for the database represented by sd.
    def importTableAttributes(self) -> None:
        query = StockQueries.getTablesQuery().format(self.sd.getDatabaseName())
        tables = self.sd.getTables(query)
        for t in tables:
            # Get key attributes
            keyQuery = StockQueries.getPrimaryKeyQuery().format(self.sd.getDatabaseName(), t)
            keys = self.sd.getKeyAttributes(keyQuery)
            # Get non-key attributes
            attrQuery = StockQueries.getAttributeQuery().format(t)
            attr = self.sd.getAttributes(attrQuery) #Includes keys
            
            self.tableDict[t] = tableAttributes(keys, attr)
            
    # Attempt to get current price information for the stocks in the database.
    def monitor(self) -> None:
        for stockID in self.stocksToMonitor:
            try:
                yahoo = Share(stockID)
                self.postStockActivity(stockID, yahoo.get_price())
            except YQLQueryError:
                logging.warning("Yahoo finance is currently unavailable.")
            except:
                logging.warning("Unexpected error in StockBot.monitor():", sys.exc_info()[0])
        
    # Add a new entry to the StockBot.stock table.
    def postStock(self, stockID: str) -> None:
        attrs = self._attrsToString((self.tableDict.get("stock")).getAttributes())
        attrIn = "{}, {}, {}, {}".format('"' + stockID + '"', 0, 0, 0)
        query = StockQueries.getInsertQuery().format("stock", attrs, attrIn)
        self.sd.runQuery(query)
        
    # Add a new entry to the StockBot.stock_activity table.
    def postStockActivity(self, stockID: str, price: float) -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        
        attrs = self._attrsToString((self.tableDict.get("stock_activity")).getAttributes())
        attrIn = "{}, {}, {}, {}".format('"' + stockID + '"', '"' + currentDate + '"', 
                                         '"' + currentTime + '"', price)
        query = StockQueries.getInsertQuery().format("stock_activity", attrs, attrIn)
        self.sd.runQuery(query)
        
    # Updates the stock_history table for the current date. 
    # Only meant to be used after trading is closed.
    def postStockHistory(self) -> None:
        for stockID in self.stocksToMonitor:
            currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
            avgQuery = StockQueries.getAverageQuery().format("stock_activity_price", "stock_activity", 
                                                             "stock_activity_date", currentDate)
            average = self.sd.getAverageValue(avgQuery)
            if average == None:
                average = -1
            yahoo = Share(stockID)
            attrs = self._attrsToString((self.tableDict.get("stock_history")).getAttributes())
            attrIn = "{}, {}, {}, {}, {}, {}, {}".format('"' + stockID + '"', '"' + currentDate + '"', 
                                                         yahoo.get_open(), average, yahoo.get_price(), 
                                                         yahoo.get_days_high(), yahoo.get_days_low())
            insQuery = StockQueries.getInsertQuery().format("stock_history", attrs, attrIn)
            self.sd.runQuery(insQuery)
    
    # Removes the given stockID from all tables, or just the stock table based on allTables.
    def removeStock(self, stockID: str, allTables: bool) -> None:   
        if allTables:
            for table in self.tableDict.keys():
                delQuery = StockQueries.getDeleteQuery().format(table, stockID)
                self.sd.runQuery(delQuery)
        else:
            delQuery = StockQueries.getDeleteQuery().format("stock", stockID)
            self.sd.runQuery(delQuery)
        
    # Actively monitors and updates stock information.
    def run(self) -> None:
        self.monitor()
        self.updateStockAverages()

    # Update the averages for every stock in the database.
    # This one takes a ton of "insider information" for now
    def updateStockAverages(self) -> None:
        for stockID in self.stocksToMonitor:
            avgOpenQuery = StockQueries.getAverageQuery().format("stock_history_open" , "stock_history", 
                                                                 "stock_id", stockID)
            avgDayQuery = StockQueries.getAverageQuery().format("stock_history_average" , "stock_history", 
                                                                "stock_id", stockID)
            avgCloseQuery = StockQueries.getAverageQuery().format("stock_history_close" , "stock_history", 
                                                                  "stock_id", stockID)
            avgOpen = self.sd.getAverageValue(avgOpenQuery)
            avgDay = self.sd.getAverageValue(avgDayQuery)
            avgClose = self.sd.getAverageValue(avgCloseQuery)
            
            # Replace none with -1, in case data doesn't exist
            if avgOpen == None:
                avgOpen = -1
            if avgDay == None:
                avgDay = -1
            if avgClose == None:
                avgClose = -1
            
            openUpdate = StockQueries.getUpdateQuery().format("stock", "stock_average_open", avgOpen, stockID)
            dayUpdate = StockQueries.getUpdateQuery().format("stock", "stock_average_daily", avgDay, stockID)
            closeUpdate = StockQueries.getUpdateQuery().format("stock", "stock_average_close", avgClose, stockID)
            self.sd.runQuery(openUpdate)
            self.sd.runQuery(dayUpdate)
            self.sd.runQuery(closeUpdate)
    