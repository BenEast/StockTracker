from builtins import str

# A wrapper class of MySQL queries and getters for the StockBot database.
class StockQueries:
    
    # Hardcoded SQL statement for getting column/attribute names
    _attributeNamesQuery = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                            "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}'")
    
    # Hardcoded select statements to get the averages of values from the stock_history table.
    _averageStockQuery = ("SELECT AVG(stock_activity_price) AS average FROM stock_activity WHERE stock_id = '{}'")
    _averageStockOpenQuery = ("SELECT AVG(stock_history_open) AS average FROM stock_history WHERE stock_id = '{}'")
    _averageStockCloseQuery = ("SELECT AVG(stock_history_close) AS average FROM stock_history WHERE stock_id = '{}'")
    
    _averageStockHistoryQuery = ("SELECT AVG(stock_activity_price) AS stock_history_average FROM stock_activity "
                                 "WHERE stock_id = '{}' AND stock_activity_date = '{}'")
    
    # Hardcoded inserts for stock, stock_activity, and stock_history tables.
    _insStockQuery = ("INSERT INTO stock (stock_id, average_open, average_daily, average_close) "
                      "VALUES (%s, %s, %s, %s)") 
    _insStockActivityQuery = ("INSERT INTO stock_activity (stock_id, stock_activity_date, stock_activity_time, stock_activity_price) "
                              "VALUES (%s, %s, %s, %s)")  
    _insStockHistoryQuery = ("INSERT INTO stock_history (stock_id, stock_history_date, stock_history_open, stock_history_average, "
                             "stock_history_close, stock_history_high, stock_history_low) " 
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    
    # Hardcoded select statements to grab keys from the tables.
    _keyValuesStockQuery = ("SELECT stock_id FROM stock")
    _keyValuesStockActivityQuery = ("SELECT stock_id, stock_activity_date, stock_activity_time FROM stock_activity")
    _keyValuesStockHistoryQuery = ("SELECT stock_id, stock_history_date FROM stock_history")
    
    # Hardcoded select statement to grab primary key column names from the tables.
    _primaryKeyQuery = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}' AND "
                       "COLUMN_KEY = 'PRI'")
     
    # Hardcoded update statements to change values in the StockBot.stock table.
    _updateQuery = ("UPDATE {} SET {} = {} WHERE stock_id = '{}'")
    
    # Returns the attributeNamesQuery.
    @staticmethod
    def getAttributeNamesQuery() -> str:
        return StockQueries._attributeNamesQuery
        
    # Returns the average stock query
    @staticmethod
    def getAverageStockQuery() -> str:
        return StockQueries._averageStockQuery
    
    # Returns the average stock open query
    @staticmethod
    def getAverageStockOpenQuery() -> str:
        return StockQueries._averageStockOpenQuery
    
    #  Returns the average stock close query
    @staticmethod
    def getAverageStockCloseQuery() -> str:
        return StockQueries._averageStockCloseQuery
    
    # Returns a query for the average price for the stock_history table
    @staticmethod
    def getAverageStockHistoryQuery() -> str:
        return StockQueries._averageStockHistoryQuery
        
    # Returns the primaryKeyQuery
    @staticmethod
    def getPrimaryKeyQuery() -> str:
        return StockQueries._primaryKeyQuery
        
    # Returns the correct insert query based on the given table.
    @staticmethod
    def getTableInsertQuery(table: str) -> str:
        table = table.lower()
        
        if table == 'stock':
            return StockQueries._insStockQuery
        elif table == 'stock_activity':
            return StockQueries._insStockActivityQuery
        elif table == 'stock_history':
            return StockQueries._insStockHistoryQuery
        else:
            print("Invalid table input to StockQueries.getTableInsertQuery.")
            return "Invalid"
    
    # Returns the correct table key values query based on the given table.
    @staticmethod
    def getTableKeyValuesQuery(table: str) -> str:
        table = table.lower()
        
        if table == 'stock':
            return StockQueries._keyValuesStockQuery
        elif table == 'stock_activity':
            return StockQueries._keyValuesStockActivityQuery
        elif table == 'stock_history':
            return StockQueries._keyValuesStockHistoryQuery
        else:
            print("Invalid table passed to StockQueries.getTableKeyValuesQuery.")
            return "Invalid"
    
    # Returns the updateQuery
    @staticmethod
    def getUpdateQuery() -> str:
        return StockQueries._updateQuery
    