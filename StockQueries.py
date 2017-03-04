
# A wrapper class of MySQL queries and getters for the StockBot database.
class StockQueries:
    
    # Hardcoded SQL statement for getting column/attribute names
    attributeNames = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                      "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}'")
    
    # Hardcoded inserts for stock, stock_activity, and stock_history tables.
    insStock = ("INSERT INTO stock (stock_id, avg_open, avg_daily, avg_close) "
                "VALUES (%s, %s, %s, %s)") 
    insStockActivity = ("INSERT INTO stock_activity (stock_id, stock_activity_date, stock_activity_time, stock_activity_price) "
                         "VALUES (%s, %s, %s, %s)")  
    insStockHistory = ("INSERT INTO stock_history (stock_id, stock_history_date, stock_history_open, stock_history_average, stock_history_close) " 
                       "VALUES (%s, %s, %s, %s, %s)")
    
    # Returns the correct insert query based on the given table.
    @staticmethod
    def getInsertQuery(table):
        table = table.lower()
        
        if table == 'stock':
            return StockQueries.insStock
        elif table == 'stock_activity':
            return StockQueries.insStockActivity
        elif table == 'stock_history':
            return StockQueries.insStockHistory
        else:
            print("Invalid table input to StockQueries.getInsertQuery.")
            return "Invalid"
        
    # Hardcoded select statement to grab primary key column names from the tables.
    primaryKey = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                  "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}' AND "
                  "COLUMN_KEY = 'PRI'")
     
    # Returns the correct primary keys query for the given table.
    @staticmethod
    def getQueryKeyAttributes(table):
        table = table.lower()
        return StockQueries.primaryKey.format(table)
    
    # Hardcoded select statements to grab keys from the tables.
    keyValuesStock = ("SELECT stock_id FROM stock")
    keyValuesStockActivity = ("SELECT stock_id, stock_activity_date, stock_activity_time FROM stock_activity")
    keyValuesStockHistory = ("SELECT stock_id, stock_history_date FROM stock_history")
    
    # Returns the correct table key values query based on the given table.
    @staticmethod
    def getTableKeyValues(table):
        table = table.lower()
        
        if table == 'stock':
            return StockQueries.keyValuesStock
        elif table == 'stock_activity':
            return StockQueries.keyValuesStockActivity
        elif table == 'stock_history':
            return StockQueries.keyValuesStockHistory
        else:
            print("Invalid table passed to StockQueries.getTableKeys.")
            return "Invalid"
        
    # Hardcoded update statements to change values in the StockBot.stock table.
    updStock = ("UPDATE stock SET {} = {} WHERE stock_id = '{}'")
    
    # Returns the correct update stock query based on the given attribute.
    @staticmethod
    def getStockUpdateQuery(attribute, value, stockID):
        attribute = attribute.lower()
        return StockQueries.updStock.format(attribute, value, stockID)
    
    # Hardcoded update statements to update values in the stock_history table.
    updStockHistory = ("UPDATE stock_history SET {} = {} WHERE stock_id = '{}'")
    
    # Returns the correct update stock history query based on the given attribute.
    @staticmethod
    def getStockHistoryUpdateQuery(attribute, value, stockID):
        attribute = attribute.lower()
        return StockQueries.updStockHistory.format(attribute, value, stockID)
    
    # Hardcoded select statements to get the averages of values from the stock_activity table.
    avgStock = ("SELECT AVG(stock_history_open) AS {} FROM stock_history WHERE stock_id = '{}'")
    
    # Returns the correct avg stock query based on the given attribute.
    @staticmethod
    def getAvgStockQuery(attribute, stockID):
        attribute = attribute.lower()
        return StockQueries.avgStock.format(attribute, stockID)
    
    avgStockHistory = ("SELECT AVG(stock_activity_price) AS stock_history_average FROM stock_activity "
                       "WHERE stock_id = '{}' AND stock_activity_date = '{}'")
    
    # Returns a query for the average price for the given date; for use with stock_history table.
    @staticmethod
    def getAvgStockHistoryQuery(stockID, date):
        return StockQueries.avgStockHistory.format(stockID, date)
    