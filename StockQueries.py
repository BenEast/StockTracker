
# A wrapper class of MySQL queries and getters for the StockBot database.
class StockQueries:
    
    # Hardcoded inserts for stock, stock_activity, and stock_history tables.
    insStock = ("INSERT INTO stock (stock_id, avg_open, avg_daily, avg_close) "
                "VALUES (%s, %s, %s, %s)")
    
    insStockActivity = ("INSERT INTO stock_activity (stock_id, stock_activity_date, stock_activity_time, stock_activity_price) "
                         "VALUES (%s, %s, %s, %s)")  
    
    insStockHistory = ("INSERT INTO stock_history (stock_id, stock_history_date, stock_history_open, stock_history_average, "
                       "stock_history_close) VALUES (%s, %s, %s, %s, %s)")
    
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
        
    # Hardcoded select statements to grab primary key column names from the tables.
    primaryKeyStock = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = 'stock' AND "
                       "COLUMN_KEY = 'PRI'")
    
    primaryKeyStockActivity = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                               "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = 'stock_activity' AND "
                               "COLUMN_KEY = 'PRI'")
    
    primaryKeyStockHistory = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                              "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = 'stock_history' AND "
                              "COLUMN_KEY = 'PRI'")
    
    # Returns the correct primary keys query for the given table.
    @staticmethod
    def getQueryKeyAttributes(table):
        table = table.lower()
        
        if table == 'stock':
            return StockQueries.primaryKeyStock
        elif table == 'stock_activity':
            return StockQueries.primaryKeyStockActivity
        elif table == 'stock_history':
            return StockQueries.primaryKeyStockHistory
        else:
            print("Invalid table passed to StockQueries.getTableKeyAttributes.")
            return "Invalid"
    
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
    updStockOpen = ("UPDATE stock SET avg_open = {} WHERE stock_id = '{}'")
    
    updStockDaily = ("UPDATE stock SET avg_daily = {} WHERE stock_id = '{}'")
    
    updStockClose = ("UPDATE stock SET avg_close = {} WHERE stock_id = '{}'")
    
    # Returns the correct update stock query based on the given attribute.
    @staticmethod
    def getStockUpdateQuery(attribute, value, stock_id):
        attribute = attribute.lower()
        
        if attribute == 'avg_open':
            return StockQueries.updStockOpen.format(value, stock_id)
        elif attribute == 'avg_daily':
            return StockQueries.updStockDaily.format(value, stock_id)
        elif attribute == 'avg_close':
            return StockQueries.updStockClose.format(value, stock_id)
        else:
            print('Invalid attribute passed to StockQueries.getStockUpdateQuery.')
            return "Invalid"
    
    # Hardcoded update statements to update values in the stock_history table.
    updStockHistoryOpen = ("UPDATE stock_history SET stock_history_open = {} WHERE stock_id = '{}'")
    
    updStockHistoryAverage = ("UPDATE stock_history SET stock_history_average = {} WHERE stock_id = '{}'")
    
    updStockHistoryClose = ("UPDATE stock_history SET stock_history_close = {} WHERE stock_id = '{}'")
    
    # Returns the correct update stock history query based on the given attribute.
    @staticmethod
    def getStockHistoryUpdateQuery(attribute, value, stock_id):
        attribute = attribute.lower()
        
        if attribute == 'stock_history_open':
            return StockQueries.updStockHistoryOpen.format(value, stock_id)
        elif attribute == 'stock_history_average':
            return StockQueries.updStockHistoryAverage.format(value, stock_id)
        elif attribute == 'stock_history_close':
            return StockQueries.updStockHistoryClose.format(value, stock_id)
        else:
            print('Invalid attribute passed to StockQueries.getStockHistoryUpdateQuery.')
            return "Invalid"
    
    # Hardcoded select statements to get the averages of values from the stock_activity table.
    avgStockDaily = ("SELECT AVG(stock_activity_price) AS avg_daily FROM stock_activity WHERE stock_id = '{}'")
    
    avgStockOpen = ("SELECT AVG(stock_activity_price) AS avg_open FROM stock_activity WHERE stock_id = '{}'")
    
    avgStockClose = ("SELECT AVG(stock_activity_price) AS avg_close FROM stock_activity WHERE stock_id = '{}'")
    
    avgStockHistoryDate = ("SELECT AVG(stock_activity_price) AS stock_history_average FROM stock_activity "
                           "WHERE stock_id = '{}' AND stock_activity_date = {}")
    
    # Returns a query for the average price for the given date; for use with stock_history table.
    @staticmethod
    def getAvgStockHistoryQuery(stock_id, date):
        return StockQueries.avgStockHistoryDate.format(stock_id, date)
    
    # Returns the correct avg stock query based on the given attribute.
    @staticmethod
    def getAvgStockQuery(attribute, stock_id):
        attribute = attribute.lower()
        
        if attribute == 'avg_open':
            return StockQueries.avgStockOpen.format(stock_id)
        elif attribute == 'avg_daily':
            return StockQueries.avgStockDaily.format(stock_id)
        elif attribute == 'avg_close':
            return StockQueries.avgStockClose.format(stock_id)
        else:
            print('Invalid attribute passed to StockQueries.getAvgStockQuery.')
            return "Invalid"
        
    # Hardcoded SQL statement for getting column/attribute names
    attributeNames = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                      "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}'")
    