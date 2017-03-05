import mysql.connector
import sys, logging
from StockQueries import *
from mysql.connector.errors import IntegrityError as mysql_IntegrityError
from mysql.connector.errors import DataError as mysql_DataError
from mysql.connector.errors import ProgrammingError as mysql_ProgrammingError

# A class to handle MySQL interactions with the StockBot database.
class StockDB:
    
    # Attempt to initialize a connection with the given parameters.
    def __init__(self, user: str, password: str, hostIP: str, database: str):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                               host=hostIP, database=database)
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql_ProgrammingError:
            print("Unable to initialize StockDB connection due to invalid inputs.")
            logging.warning("Unable to initialize StockDB connection due to invalid inputs.")
        except:
            print("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])
            logging.warning("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])

        logging.info("StockDB initialized.\n")

    # Adds a stock with the given parameters to the StockBot.stock table in the MySQL database.
    def addStock(self, stockID: str, avgOpen: float, avgDaily: float, avgClose: float) -> None:
        logging.info("StockDB.addStock() called.")
        
        try:
            self.cursor.execute(StockQueries.getTableInsertQuery("stock"), (stockID, avgOpen, avgDaily, avgClose))
            self.cnx.commit()
        except mysql_IntegrityError:
            print("Key {} already exists in table stock!".format(stockID))
            logging.warning("Key {} already exists in table stock!".format(stockID))
        except mysql_DataError:
            print("Invalid inputs for query in StockDB.addStock().")
            logging.warning("Invalid inputs for query in StockDB.addStock().")
        except TypeError:
            print("Incorrect number of arguments for query in StockDB.addStock().")
            logging.warning("Invalid inputs for query in StockDB.addStock().")
        except:
            print("Unexpected error in StockDB.addStock():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.addStock():", sys.exc_info()[0])
            
        logging.info("StockDB.addStock() completed.\n")
            
    # Adds a stock activity entry with the given parameters to the StockBot.stock_activity table.
    def addStockActivity(self, stockID: str, date, time, price: float) -> None:
        logging.info("StockDB.addStockActivity() called.")
        
        try:
            self.cursor.execute(StockQueries.getTableInsertQuery("stock_activity"), (stockID, date, time, price))
            self.cnx.commit()     
        except mysql_IntegrityError:
            print("Key ({}, {}, {}) already exists in table stock_activity!".format(stockID, date, time))
            logging.warning("Key ({}, {}, {}) already exists in table stock_activity!".format(stockID, date, time))
        except mysql_DataError:
            print("Invalid inputs for query in StockDB.addStockActivity().")
            logging.warning("Invalid inputs for query in StockDB.addStockActivity().")
        except TypeError:
            print("Incorrect number of arguments for query in StockDB.addStockActivity().")
            logging.warning("Incorrect number of arguments for query in StockDB.addStockActivity().")
        except:
            print("Unexpected error in StockDB.addStockActivity():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.addStockActivity():", sys.exc_info()[0])
            
        logging.info("StockDB.addStockActivity() completed.\n")    
        
    # Adds a stock history entry with the given parameters to the StockBot.stock_history table.
    def addStockHistory(self, stockID: str, currentDate, stockOpen: float, stockAvg: float, 
                        stockClose: float, stockHigh: float, stockLow: float) -> None:
        logging.info("StockDB.addStockHistory() called.")
        
        try:
            self.cursor.execute(StockQueries.getTableInsertQuery('stock_history'), 
                                (stockID, currentDate, stockOpen, stockAvg, stockClose, stockHigh, stockLow))
            self.cnx.commit()
        except mysql_IntegrityError:
            print("Key ({}, {}) already exists in table stock_history!".format(stockID, currentDate))
            logging.warning("Key ({}, {}) already exists in table stock_history!".format(stockID, currentDate))
        except mysql_DataError:
            print("Invalid inputs for query in StockDB.addStockHistory().")
            logging.warning("Invalid inputs for query in StockDB.addStockHistory().")
        except TypeError:
            print("Incorrect number of arguments for query in StockDB.addStockHistory().")
            logging.warning("Incorrect number of arguments for query in StockDB.addStockHistory().")
        except:
            print("Unexpected error in StockDB.addStockHistory():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.addStockHistory():", sys.exc_info()[0])
        
        logging.info("StockDB.addStockHistory() completed.\n")
        
    # Closes the active cursor and connection for this object.
    # Effectively disables the object.
    def close(self) -> None:
        try:
            self.cursor.close()
            self.cnx.close()
        except:
            pass
    
    # Averages the history of the stock.
    def getAverageStock(self, attribute: str, stockID: str) -> float:
        logging.info("StockDB.getAverageStock() called.")
        
        if attribute == "average_daily":
            query = StockQueries.getAverageStockQuery().format(stockID)
        elif attribute == "average_open":
            query = StockQueries.getAverageStockOpenQuery().format(stockID)
        elif attribute == "average_close":
            query = StockQueries.getAverageStockCloseQuery().format(stockID)
        else:
            query = "Invalid"

        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.getAverageStock().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.getAverageStock().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.getAverageStock():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.getAverageStock():", sys.exc_info()[0])
            
        average = 0
        for row in self.cursor:
            average = row["average"]
            
        logging.info("StockDB.getAverageStock() completed.\n")
        return average
            
    # Gets the attribute names of a given table in the database.
    def getAttributeNames(self, table: str):
        logging.info("StockDB.getAttributeNames() called.")
        
        table = table.lower()
        query = StockQueries.getAttributeNamesQuery().format(table)  
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.getAttributeNames().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.getAttributeNames().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.getAttributeNames():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.getAttributeNames():", sys.exc_info()[0])
            
        attributes = []
        for row in self.cursor:
            attributes.append(row["COLUMN_NAME"])
            
        logging.info("StockDB.getAttributeNames() completed.\n")
        return attributes
    
    # Gets the names of the attributes that aren't keys for the given table.
    def getAttributeNamesNotKeys(self, table: str):
        logging.info("StockDB.getAttributeNamesNotKeys() called.")
        
        table = table.lower()
        attributes = self.getAttributeNames(table)
        keys = self.getKeyAttributes(table)
        
        for key in keys:
            if key in attributes:
                attributes.remove(key)
    
        logging.info("StockDB.getAttributeNamesNotKeys() completed.\n")
        return attributes 
    
    # Gets the attributes that are keys in the given table.
    def getKeyAttributes(self, table: str):
        logging.info("StockDB.getKeyAttributes() called.")
        
        table = table.lower()   
        query = StockQueries.getPrimaryKeyQuery().format(table)       
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.getKeyAttributes().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.getKeyAttributes().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.getKeyAttributes():", sys.exc_info()[0]) 
            logging.warning("Unexpected error in StockDB.getKeyAttributes():", sys.exc_info()[0])
            
        keys = []
        for row in self.cursor:
            keys.append(row["primary_key"])
            
        logging.info("StockDB.getKeyAttributes() completed.\n")
        return keys
    
    # Gets the keys of the tuples in the given table and returns them.
    def getKeyValues(self, table: str):
        logging.info("StockDB.getKeyValues() called.")
        
        table = table.lower()
        query = StockQueries.getTableKeyValuesQuery(table)
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.getKeyValues().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.getKeyValues().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.getKeyValues():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.getKeyValues():", sys.exc_info()[0])
        
        result = []
        for row in self.cursor:
            result.append(row["stock_id"])
        
        logging.info("StockDB.getKeyValues() completed.\n")
        return result
    
    # Gets the average value of the stock for a given date
    def getStockHistoryAverageValue(self, stockID: str, date) -> float:
        logging.info("StockDB.getStockHistoryAverageValue() called.")
        
        query = StockQueries.getAverageStockHistoryQuery().format(stockID, date)
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.getStockHistoryAverageValue().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.getStockHistoryAverageValue().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.getStockHistoryAverageValue():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.getStockHistoryAverageValue():", sys.exc_info()[0])  
        
        result = []
        for row in self.cursor:
            result.append(row["stock_history_average"])
        
        logging.info("StockDB.getStockHistoryAverageValue() completed.\n")
        return result[0]    # Result will always be a singleton, since its a MySQL AVG call.
    
    # Attempts to execute the database query parameters and outputs the results to the console.
    def queryDB(self, query: str) -> None:
        logging.info("StockDB.queryDB() called.")
        
        try:
            result = self.cursor.execute(query, multi=True)
        except mysql_ProgrammingError:
            print("Invalid MySQL syntax in StockDB.queryDB().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL syntax in StockDB.queryDB()."
                            "\nUnable to execute query '{}'".format(query))
            result = []
        except:
            print("Unexpected error in StockDB.queryDB():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.queryDB():", sys.exc_info()[0])
            result = []
            
        if result:
            for r in result:
                if r.with_rows:
                    print("Rows produced by statement '{}':".format(r.statement))
                    print(r.fetchall())
                else:
                    print("Number of rows affected by statement '{}': {}".format(r.statement, r.rowcount))
    
        logging.info("StockDB.queryDB() completed.\n")
        return result
    
    # Updates a given table and attribute with a given value.
    def updateTableAttribute(self, table: str, attribute: str, value, stockID: str) -> None:
        logging.info("StockDB.updateTableAttribute() called.")
        
        table = table.lower()
        attribute = attribute.lower()
        if value == None:
            value = -1
            
        query = StockQueries.getUpdateQuery().format(table, attribute, value, stockID)
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql_ProgrammingError:
            print("Invalid MySQL query in StockDB.updateTableAttribute().\n"
                  "Unable to execute query '{}'".format(query))
            logging.warning("Invalid MySQL query in StockDB.updateTableAttribute().\n"
                            "Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in StockDB.updateTableAttribute():", sys.exc_info()[0])
            logging.warning("Unexpected error in StockDB.updateTableAttribute():", sys.exc_info()[0])
            
        logging.info("StockDB.updateTableAttribute() completed.\n")
            