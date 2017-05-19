
# A class to generate MySQL queries to work with the Stockbot databse.
class StockQueries:

    # SQL statement for getting column/attribute names
    _attributesQuery = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                            "WHERE TABLE_SCHEMA = 'StockBot' AND TABLE_NAME = '{}'")

    # PARAMETERS: table: the table to get attributes from;
    # RETURNS: Returns a complete SQL Attribute query.
    @staticmethod
    def getAttributeQuery(tableName: str) -> str:
        return StockQueries._attributesQuery.format(tableName)
        
    # SQL Select statements to get the averages of values from the stock_history table.
    _averageQuery = ("SELECT AVG({}) AS average FROM {} WHERE {} = '{}'")        
        
    # PARAMETERS: avgAttr: the attribute to average; 
    #             fromVal: the table the attribute is found in;
    #             whereKey: the first value in the SQL where condition; 
    #             whereVal: the second value in the SQL where condition;
    # RETURNS: Returns a complete SQL Average query.
    @staticmethod
    def getAverageQuery(avgAttr: str, fromVal: str, whereKey: str, whereVal: str) -> str:
        return StockQueries._averageQuery.format(avgAttr, fromVal, whereKey, whereVal)
    
    # SQL Remove statements to remove a value from stock, or from all tables.
    _deleteQuery = ("DELETE FROM {} WHERE {} = '{}'")
    
    # PARAMETERS: fromVal: the table the attribute is found in; 
    #             whereKey: the first value in the SQL where condition; 
    #             whereVal: the second value in the SQL where condition;
    # RETURNS: Returns a complete SQL Delete query.
    @staticmethod
    def getDeleteQuery(fromVal: str, whereKey: str, whereVal: str) -> str:
        return StockQueries._deleteQuery.format(fromVal, whereKey, whereVal)    
     
    # SQL select statement to grab primary key column names from the tables.
    _primaryKeyQuery = ("SELECT COLUMN_NAME AS primary_key FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}' AND "
                       "COLUMN_KEY = 'PRI'")
      
    # PARAMETERS: databaseName: the name of the database.
    #             tableName: the name of the table in the database
    # RETURNS: Returns the primaryKeyQuery
    @staticmethod
    def getPrimaryKeyQuery(databaseName: str, tableName: str) -> str:
        return StockQueries._primaryKeyQuery.format(databaseName, tableName)
    
    # General SQL insert query for use with a database.
    _insQuery = ("INSERT INTO {} ({}) VALUES ({})")  
    
    # PARAMETERS: insTable: the table to insert into;; 
    #             insAttr: the attributes in the table;
    #             values: the values being inserted into the table;
    # RETURNS: Returns a complete SQL Insert query.
    @staticmethod
    def getInsertQuery(insTable: str, insAttr: str, values: str) -> str:
        return StockQueries._insQuery.format(insTable, insAttr, values)
    
    # General SQL query to select values from a database.
    _keyValuesQuery = ("SELECT {} FROM {}")
    
    # PARAMETERS: selVal: the attribute to select; 
    #             fromVal: the table the attribute is found in;
    # RETURNS: Returns a complete SQL Select query.
    @staticmethod
    def getKeyValuesQuery(selVal: str, fromVal: str) -> str:
        return StockQueries._keyValuesQuery.format(selVal, fromVal)
    
    # SQL Update statements to update values
    _updateQuery = ("UPDATE {} SET {} = {} WHERE stock_id = '{}'")
    
    # PARAMETERS: updateVal: the table to be updated; 
    #             setKeyVal: the table attribute to be set;
    #             setValue: the value that is being set to the table attribute;
    #             stockID: the stockID (database key) to update;
    # RETURNS: Returns a complete SQL Average query.
    @staticmethod
    def getUpdateQuery(updateVal: str, setKeyVal: str, setValue: str, stockID: str) -> str:
        return StockQueries._updateQuery.format(updateVal, setKeyVal, setValue, stockID)
    
    # SQL query for all of the tables in a database.
    _tableNamesQuery = ("SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema='{}'")
    
    # PARAMETERS: databaseName: the name of the database;
    # RETURNS: Returns a complete SQL Table names query.
    @staticmethod
    def getTableNamesQuery(databaseName: str) -> str:
        return StockQueries._tableNamesQuery.format(databaseName)
    