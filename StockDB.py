import mysql.connector
import sys, logging
from mysql.connector.errors import ProgrammingError as mysql_ProgrammingError

# A class to handle MySQL interactions with the StockBot database.
class StockDB:
    
    # Standard error messages
    _mysqlErrorMessage = ("Invalid MySQL query in StockDB.{}().\n"
                          "Unable to execute query '{}'")

    _unexpectedErrorMessage = ("Unexpected error in StockDB.{}(): {}")

    # Attempt to initialize a connection with the given parameters.
    def __init__(self, user: str, password: str, hostIP: str, db: str):
        try:
            self.databaseName = db
            self.cnx = mysql.connector.connect(user=user, password=password,
                                               host=hostIP, database=db)
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql_ProgrammingError:
            logging.warning("Unable to initialize StockDB connection due to invalid inputs.")
        except:
            logging.warning("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])

    # Closes the active cursor and connection for this object.
    # Effectively disables the object.
    def close(self) -> None:
        try:
            self.cursor.close()
            self.cnx.close()
        except:
            pass
    
    # Gets the attribute names of a given table in the database.
    def getAttributes(self, query: str) -> list:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getAttributes", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getAttributes", sys.exc_info()[0])
            logging.warning(error)
            
        attributes = []
        for row in self.cursor:
            attributes.append(row["COLUMN_NAME"])

        return attributes
    
    # Gets the average value given an accurate query.
    def getAverageValue(self, query: str) -> float:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getAverageValue", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getAverageValue", sys.exc_info()[0])
            logging.warning(error)
            
        average = 0
        for row in self.cursor:
            average = row["average"]

        return average
    
    # Returns the database name represented by this StockDB
    def getDatabaseName(self) -> str:
        return self.databaseName
    
    # Gets the attributes that are keys in the given table.
    def getKeyAttributes(self, query: str) -> list:     
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getKeyAttributes", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getKeyAttributes", sys.exc_info()[0])
            logging.warning(error)
            
        keys = []
        for row in self.cursor:
            keys.append(row["primary_key"])

        return keys
        
    # Gets the keys of the tuples in the given table and returns them.
    def getKeyValues(self, query: str) -> list: 
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getKeyValues", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getKeyValues", sys.exc_info()[0])
            logging.warning(error)
        
        result = []
        for row in self.cursor:
            result.append(row["stock_id"])

        return result
    
    # Gets all of the tables in the database, given the correct query.
    def getTables(self, query: str) -> list:
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            error = self._mysqlErrorMessage.format("getTables", query)
            logging.warning(error)
        except:
            error = self._unexpectedErrorMessage.format("getTables", sys.exc_info()[0])
            logging.warning(error)
        
        result = []
        for row in self.cursor:
            result.append(row["table_name"])

        return result
    
    # Attempts to execute the database query parameters and outputs the results to the console.
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
            