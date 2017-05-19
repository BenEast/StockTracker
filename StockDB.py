import mysql.connector
import sys, logging
from mysql.connector.errors import ProgrammingError as mysql_ProgrammingError

# A class to handle MySQL interactions with the StockBot database.
class StockDB:
    
    # Error message for invalid MySQL queries.
    _mysqlErrorMessage = ("Invalid MySQL query in StockDB.{}().\n"
                          "Unable to execute query '{}'")

    # Error message for unexpected situation.
    _unexpectedErrorMessage = ("Unexpected error in StockDB.{}(): {}")

    # Attempt to initialize a connection with the given parameters.
    # PARAMETERS: username: the username for the database connection;
    #             password: the password for the database connection;
    #             hostIPAddress: the IP address of the database connection;
    #             databaseName: the name of the database to connect to;
    # RETURNS: None
    def __init__(self, username: str, password: str, hostIPAddress: str, databaseName: str):
        try:
            self.databaseName = databaseName
            self.cnx = mysql.connector.connect(user=username, password=password,
                                               host=hostIPAddress, database=databaseName)
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql_ProgrammingError:
            logging.warning("Unable to initialize StockDB connection due to invalid inputs.")
        except:
            logging.warning("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])

    # Closes the active cursor and connection for this object.
    # PARAMETERS: None
    # RETURNS: None
    def close(self) -> None:
        try:
            self.cursor.close()
            self.cnx.close()
        except:
            pass
    
    # Gets the attribute names of a given table in the database.
    # PARAMETERS: query: the MySQL query to be executed in order to get table attributes from the database;
    # RETURNS: Returns a list of attributes resulting from the query.
    def getAttributes(self, query: str) -> list:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getAttributes", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getAttributes", sys.exc_info()[0])
            logging.warning(error)
            
        # Gather the attributes into a list
        attributes = []
        for row in self.cursor:
            attributes.append(row["COLUMN_NAME"])

        return attributes
    
    # Gets the average value given an accurate query.
    # PARAMETERS: query: the MySQL query to be executed in order to get an average value from the database;
    # RETURNS: Returns a float of the average value from the given query.
    def getAverageValue(self, query: str) -> float:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getAverageValue", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getAverageValue", sys.exc_info()[0])
            logging.warning(error)
            
        # Get the average value
        average = 0
        for row in self.cursor:
            average = row["average"]

        return average
    
    # Returns the database name represented by this StockDB
    # PARAMETERS: None
    # RETURNS: Returns the name of the database as a string.
    def getDatabaseName(self) -> str:
        return self.databaseName
    
    # Gets the attributes that are keys in the given table.
    # PARAMETERS: query: the MySQL query to be executed in order to get the key attributes from the database;
    # RETURNS: Returns a list of key attributes resulting from the query.
    def getKeyAttributes(self, query: str) -> list:     
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getKeyAttributes", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getKeyAttributes", sys.exc_info()[0])
            logging.warning(error)
            
        # Gather the keys into a list
        keys = []
        for row in self.cursor:
            keys.append(row["primary_key"])

        return keys
        
    # Gets the keys of the tuples in the given table and returns them.
    # PARAMETERS: query: the MySQL query to be executed in order to get key values from the database;
    # RETURNS: Returns a list of key values resulting from the query.
    def getKeyValues(self, query: str) -> list: 
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getKeyValues", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getKeyValues", sys.exc_info()[0])
            logging.warning(error)
        
        # Gather the key values into a list
        keyValues = []
        for row in self.cursor:
            keyValues.append(row["stock_id"])

        return keyValues
    
    # Gets all of the tables in the database, given the correct query.
    # PARAMETERS: query: the MySQL query to be executed in order to get table names from the database;
    # RETURNS: Returns a list of table names resulting from the query.
    def getTableNames(self, query: str) -> list:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getTables", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getTables", sys.exc_info()[0])
            logging.warning(error)
            
        # Gather the table names into a list
        tableNames = []
        for row in self.cursor:
            tableNames.append(row["table_name"])

        return tableNames
    
    # Attempts to execute the given MySQL query on the StockBot database.
    # PARAMETERS: query: the MySQL query to be run;
    # RETURNS: None
    def runQuery(self, query: str) -> None:
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("runQuery", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("runQuery", sys.exc_info()[0])
            logging.warning(error)
            