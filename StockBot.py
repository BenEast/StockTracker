import sys, logging
from yahoo_finance import Share, YQLQueryError
from StockQueries import *
from StockDB import StockDB
from datetime import datetime

# A "bot" to check for updates for stocks in the StockBot database and insert new information.
class StockBot:
    
    # Initialize the class object.
    # PARAMETERS: stockDatabase: A StockDB object to update data to;
    # RETURNS: None; Intializes the class.
    def __init__(self, stockDatabase: StockDB):
        try:
            self.sd = stockDatabase
            self.stocksToMonitor = []
            self.tableDict = dict()
            self.importTableAttributes()
            self.importStocksToMonitor()
        except:
            logging.warning("Unexpected error in StockBot init:", sys.exc_info()[0])
        
    # Converts a list of attributes to a comma delimted string.
    # PARAMETERS: attrs: a list of attributes to iterate through;
    # RETURNS: Returns a comma delimited string of attributes
    def _attrsToCommaDeliminatedString(self, attributes: list) -> str:
        commaString = ""
        for attribute in attributes:
            if attribute == None:
                commaString = commaString + "0, "
            else:
                commaString = commaString + ("{}, ".format(attribute))
        
        # Cut off the last comma in the string
        return commaString[:len(commaString) - 2]
    
    _stockNamesFilePath = "C:/Users/Ben/Documents/Rainmeter/Skins/illustro/Stock Monitor/StockNames.txt"
    _stockPricesFilePath = "C:/Users/Ben/Documents/Rainmeter/Skins/illustro/Stock Monitor/StockPrices.txt"
    
    # Opens the stock names and stock prices files in write mode to clear all contents from them.
    # PARAMETERS: None
    # RETURNS: None
    def _clearRainmeterFiles(self) -> None:
        open(self._stockNamesFilePath, 'w').close()
        open(self._stockPricesFilePath, 'w').close()
            
    # Updates the stock names and stock prices files for use with the rainmeter skin
    # PARAMETERS: stockID: the stock symbol to be added to StockNames.txt;
    #             currentPrice: the current price of the stock symbol to be added to StockPrices.txt;
    # RETURNS: None
    def _updateRainmeterFiles(self, stockID: str, currentPrice: float) -> None:
        nameFile = open(self._stockNamesFilePath, 'a')
        nameFile.write(stockID + "\n\n")
        nameFile.close()
        
        priceFile = open(self._stockPricesFilePath, 'a')
        priceFile.write(currentPrice + "\n\n")
        priceFile.close()
    
    # Import the stock_id keys from the StockBot.stock table.
    # PARAMETERS: None
    # RETURNS: None
    def importStocksToMonitor(self) -> None:
        self.stocksToMonitor.clear()
        keyValuesQuery = StockQueries.getKeyValuesQuery("stock_id", "stock")
        self.stocksToMonitor = self.sd.getKeyValues(keyValuesQuery)
    
    # Imports the tables, keys, and attributes for the database represented by sd.
    # PARAMETERS: None
    # RETURNS: None
    def importTableAttributes(self) -> None:
        # Get the table names in the database
        tableNamesQuery = StockQueries.getTableNamesQuery(self.sd.getDatabaseName())
        tables = self.sd.getTableNames(tableNamesQuery)
        
        for table in tables:
            # Get attributes
            tableAttributesQuery = StockQueries.getAttributeQuery(table)
            attributes = self.sd.getAttributes(tableAttributesQuery)
            
            self.tableDict[table] = attributes
        
    # Monitors the stocks that are contained in the database.
    # PARAMETERS: None
    # RETURNS: None
    def monitor(self) -> None:
        self._clearRainmeterFiles()
        for stockID in self.stocksToMonitor:
            try:
                yahoo = Share(stockID)
                currentPrice = yahoo.get_price()
                self.postStockActivity(stockID, currentPrice)
                self._updateRainmeterFiles(stockID, currentPrice)
            except YQLQueryError:
                logging.warning("Yahoo finance is currently unavailable.")
            except:
                logging.warning("Unexpected error in StockBot.monitor():", sys.exc_info()[0])
        
    # Add a new entry to the StockBot.stock table.
    # PARAMETERS: stockID: the stock symbol to be posted;
    # RETURNS: None
    def postStock(self, stockID: str) -> None:
        # Get the schema of the stock table and format it as a comma delimited
        # string for use in the MySQL query.
        stockAttributes = self.tableDict.get("stock")
        attributesString = self._attrsToCommaDeliminatedString(stockAttributes)
        
        # Format as a comma delimted string for use in the SQL query
        attributesToInsert = '"{}", {}, {}, {}'.format(stockID, 0, 0, 0)
        query = StockQueries.getInsertQuery("stock", attributesString, attributesToInsert)
        self.sd.runQuery(query)
        
    # Add a new entry to the StockBot.stock_activity table.
    # PARAMETERS: stockID: the stock symbol to be posted;
    #             price: the price value to post;
    # RETURNS: None
    def postStockActivity(self, stockID: str, price: float) -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        
        # Get the schema of the stock_activity table and format it as a comma delimited
        # string for use in the MySQL query.
        stockActivityAttributes = self.tableDict.get("stock_activity")
        attributesString = self._attrsToCommaDeliminatedString(stockActivityAttributes)
        
        # Format as a comma delimted string for use in the SQL query
        attributesToInsert = "{}, {}, {}, {}".format('"' + stockID + '"', '"' + currentDate + '"', 
                                         '"' + currentTime + '"', price)
        query = StockQueries.getInsertQuery("stock_activity", attributesString, attributesToInsert)
        self.sd.runQuery(query)
        
    # Updates the stock_history table for the current date. 
    # Only meant to be used after trading is closed.
    # PARAMETERS: None
    # RETURNS: None
    def postStockHistory(self) -> None:
        for stockID in self.stocksToMonitor:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            currentDate = timestamp[:10]
            
            # Get the average MySQL query
            avgQuery = StockQueries.getAverageQuery("stock_activity_price", "stock_activity", 
                                                             "stock_activity_date", currentDate)
            # Get the average value
            average = self.sd.getAverageValue(avgQuery)
            if average == None:
                average = -1
            yahoo = Share(stockID)
            
            # Get the schema of the stock_history table and format it as a comma delimited
            # string for use in the MySQL query.
            stockHistoryAttributes = self.tableDict.get("stock_history")
            attributesString = self._attrsToCommaDeliminatedString(stockHistoryAttributes)
            
            try:
                # Format as a comma delimted string for use in the SQL query
                attributesToInsert = self._attrsToCommaDeliminatedString(['"'+stockID+'"', 
                                              '"'+currentDate+'"', 
                                              yahoo.get_open(), 
                                              average, 
                                              yahoo.get_price(), 
                                              yahoo.get_days_high(), 
                                              yahoo.get_days_low()])
            except YQLQueryError:
                logging.warning("Yahoo finance is currently unavailable.")
                
            insQuery = StockQueries.getInsertQuery("stock_history", attributesString, attributesToInsert)
            self.sd.runQuery(insQuery)
    
    # Removes the given stockID from all tables, or just the stock table based on allTables.
    # PARAMETERS: stockID: the stock symbol to remove from the database;
    #             allTables: True if removing from all tables, False if removing only from stock table;
    # RETURNS: None
    def removeStock(self, stockID: str, allTables: bool) -> None:   
        # Delete from all tables
        if allTables:
            for table in self.tableDict.keys():
                deleteQuery = StockQueries.getDeleteQuery(table, "stock_id", stockID)
                self.sd.runQuery(deleteQuery)
        # Delete from only the stock table
        else: 
            deleteQuery = StockQueries.getDeleteQuery().format("stock", "stock_id", stockID)
            self.sd.runQuery(deleteQuery)
        
    # Actively monitors and updates stock information.
    # PARAMETERS: None
    # RETURNS: None
    def run(self) -> None:
        self.monitor()
        self.updateStockAverages()

    # Update the averages for every stock in the database.
    # PARAMETERS: None
    # RETURNS: None
    def updateStockAverages(self) -> None:
        for stockID in self.stocksToMonitor:
            # Get averageOpenQuery, averageQuery, averageCloseQuery
            avgOpenQuery = StockQueries.getAverageQuery("stock_history_open" , "stock_history", 
                                                                 "stock_id", stockID)
            avgDayQuery = StockQueries.getAverageQuery("stock_history_average" , "stock_history", 
                                                                "stock_id", stockID)
            avgCloseQuery = StockQueries.getAverageQuery("stock_history_close" , "stock_history", 
                                                                  "stock_id", stockID)
            
            # Replace None with -1, to prevent udpate errors;.
            avgOpen = self.sd.getAverageValue(avgOpenQuery)
            if avgOpen == None:
                avgOpen = -1
            avgDay = self.sd.getAverageValue(avgDayQuery)
            if avgDay == None:
                avgDay = -1
            avgClose = self.sd.getAverageValue(avgCloseQuery)
            if avgClose == None:
                avgClose = -1
            
            # Update the values in the database
            openUpdate = StockQueries.getUpdateQuery("stock", "stock_average_open", avgOpen, stockID)
            self.sd.runQuery(openUpdate)
            dayUpdate = StockQueries.getUpdateQuery("stock", "stock_average_daily", avgDay, stockID)
            self.sd.runQuery(dayUpdate)
            closeUpdate = StockQueries.getUpdateQuery("stock", "stock_average_close", avgClose, stockID)
            self.sd.runQuery(closeUpdate)
    