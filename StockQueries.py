
# A wrapper class of MySQL queries and getters for the StockBot database.
class StockQueries:

    # Hardcoded SQL statement for getting column/attribute names
    _attributesQuery = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                            "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}'")
    
    # Hardcoded select statements to get the averages of values from the stock_history table.
    _averageQuery = ("SELECT AVG({}) AS average FROM {} WHERE {} = '{}'")
    
    # Hardcoded remove statements to remove a value from stock, or from all tables.
    _deleteQuery = ("DELETE FROM {} WHERE stock_id = '{}'")
    
    # General insert query for use with a database.
    _insQuery = ("INSERT INTO {} ({}) VALUES ({})")  
    
    # General query to select values from a database.
    _keyValuesQuery = ("SELECT {} FROM {}")

    # Hardcoded select statement to grab primary key column names from the tables.
    _primaryKeyQuery = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}' AND "
                       "COLUMN_KEY = 'PRI'")
     
    # Hardcoded update statements to update values
    _updateQuery = ("UPDATE {} SET {} = {} WHERE stock_id = '{}'")
    
    # Hardcoded query for all of the tables in a database.
    _tableNamesQuery = ("SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema='{}'")
    
    # Returns the attributeNamesQuery.
    @staticmethod
    def getAttributeQuery() -> str:
        return StockQueries._attributesQuery
        
    # Returns the averageAttributeQuery
    @staticmethod
    def getAverageQuery() -> str:
        return StockQueries._averageQuery
    
    # Returns deleteQuery
    @staticmethod
    def getDeleteQuery() -> str:
        return StockQueries._deleteQuery    
        
    # Returns the primaryKeyQuery
    @staticmethod
    def getPrimaryKeyQuery() -> str:
        return StockQueries._primaryKeyQuery
    
    # Returns the insQuery
    @staticmethod
    def getInsertQuery() -> str:
        return StockQueries._insQuery
    
    # Returns the keyValuesQuery
    @staticmethod
    def getKeyValuesQuery() -> str:
        return StockQueries._keyValuesQuery
        
    # Returns the updateQuery
    @staticmethod
    def getUpdateQuery() -> str:
        return StockQueries._updateQuery
    
    @staticmethod
    def getTablesQuery() -> str:
        return StockQueries._tableNamesQuery
    