import mysql.connector
import sys, logging
from StockQueries import *
from mysql.connector.errors import IntegrityError as mysql_IntegrityError
from mysql.connector.errors import DataError as mysql_DataError
from mysql.connector.errors import ProgrammingError as mysql_ProgrammingError

# A class to handle MySQL interactions with the StockBot database.
class StockDB:
    
    # Attempt to initialize a connection with the given parameters.
    def __init__(self, user, password, hostIP, database):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                               host=hostIP, database=database)
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysql_ProgrammingError:
            print("Unable to initialize StockDB connection due to invalid inputs.")
        except:
            print("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])
        
    # Closes the active cursor and connection for this object.
    # Effectively disables the object.
    def close(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except:
            pass
    
    # Adds a stock with the given parameters to the StockBot.stock table in the MySQL database.
    def addStock(self, stockID, avgOpen, avgDaily, avgClose):
        try:
            self.cursor.execute(StockQueries.insStock, (stockID, avgOpen, avgDaily, avgClose))
            self.cnx.commit()
        except mysql_IntegrityError:
            print("Key {} already exists in table stock!".format(stockID))
        except mysql_DataError:
            print("Invalid inputs for stock MySQL query.")
        except TypeError:
            print("Incorrect number of arguments for stock query.")
        except:
            print("Unexpected error in addStock:", sys.exc_info()[0])
            
    # Adds a stock activity entry with the given parameters to the StockBot.stock_activity table.
    def addStockActivity(self, stockID, date, time, price):
        try:
            self.cursor.execute(StockQueries.insStockActivity, (stockID, date, time, price))
            self.cnx.commit()     
        except mysql_IntegrityError:
            print("Key ({}, {}, {}) already exists in table stock_activity!".format(stockID, date, time))
        except mysql_DataError:
            print("Invalid inputs for stock_activity MySQL query.")
        except TypeError:
            print("Incorrect number of arguments for stock_activity query.")
        except:
            print("Unexpected error in addStockActivity:", sys.exc_info()[0])
            
    # Adds a stock history entry with the given parameters to the StockBot.stock_history table.
    def addStockHistory(self, stockID, currentDate, stockOpen, stockAvg, stockClose):
        try:
            self.cursor.execute(StockQueries.insStockHistory, 
                                (stockID, currentDate, stockOpen, stockAvg, stockClose))
            self.cnx.commit()
        except mysql_IntegrityError:
            print("Key ({}, {}, {}) already exists in table stock_activity!".format(stockID, currentDate))
        except mysql_DataError:
            print("Invalid inputs for stock_history MySQL query.")
        except TypeError:
            print("Incorrect number of arguments for stock_activity query.")
        except:
            print("Unexpected error in addStockHistory:", sys.exc_info()[0])
    
    # Attempts to execute the database query parameters and outputs the results to the console.
    def queryDB(self, query):
        try:
            result = self.cursor.execute(query, multi=True)
        except mysql_ProgrammingError:
            print("Invalid MySQL syntax! \nUnable to execute query '{}'".format(query))
            result = []
        except:
            print("Unexpected error in queryDB:", sys.exc_info()[0])
            result = []
            
        if result:
            for r in result:
                if r.with_rows:
                    print("Rows produced by statement '{}':".format(r.statement))
                    print(r.fetchall())
                else:
                    print("Number of rows affected by statement '{}': {}".format(r.statement, r.rowcount))
    
        return result
    
    # Gets the attributes that are keys in the given table.
    def getKeyAttributes(self, table):
        table = table.lower()   
        query = StockQueries.getQueryKeyAttributes(table)       
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getKeyAttributes. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getKeyValues:", sys.exc_info()[0]) 
            
        keys = []
        for row in self.cursor:
            keys.append(row['primary_key'])
            
        return keys
    
    # Gets the keys of the tuples in the given table and returns them.
    def getKeyValues(self, table):
        table = table.lower()

        query = StockQueries.getTableKeyValues(table)
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getKeyValues. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getKeyValues:", sys.exc_info()[0])
        
        result = []
        for row in self.cursor:
            result.append(row['stock_id'])
        
        return result
    
    # Averages the history of the stock.
    def avgActivity(self, stock_id, attribute):
        attribute = attribute.lower()
        query = StockQueries.getAvgStockQuery(attribute, stock_id)
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in avgActivity. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in avgActivity:", sys.exc_info()[0])
            
        for row in self.cursor:
            return (row[attribute])
            
    # Gets the attribute names of a given table in the database.
    def getAttributeNames(self, table):
        table = table.lower()
        query = StockQueries.attributeNames.format(table)
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getAttributeNames. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getAttributeNames:", sys.exc_info()[0])
            
        attributes = []
        for row in self.cursor:
            attributes.append(row['COLUMN_NAME'])
        return attributes
    
    # Gets the names of the attributes that aren't keys for the given table.
    def getAttributeNamesNotKeys(self, table):
        table = table.lower()
        attributes = self.getAttributeNames(table)
        keys = self.getKeyAttributes(table)
        
        for key in keys:
            if key in attributes:
                attributes.remove(key)
    
        return attributes
    
    # Updates a given attribute of a given stock with the given value.
    def updateStockAttribute(self, stockID, attribute, value): 
        attribute = attribute.lower()
        if value == None:
            value = -1
            
        query = StockQueries.getStockUpdateQuery(attribute, value, stockID)
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql_ProgrammingError:
            print("Invalid MySQL query in updateStockAttribute. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in updateStockAttribute:", sys.exc_info()[0])   
    
    # Updates a given attribute of a given stock with the given value.
    def updateStockHistoryAttribute(self, stockID, attribute, value): 
        attribute = attribute.lower()
        if value == None:
            value = -1
        
        query = StockQueries.getStockHistoryUpdateQuery(attribute, value, stockID)
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql_ProgrammingError:
            print("Invalid MySQL query in updateStockAttribute. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in updateStockAttribute:", sys.exc_info()[0])   
    
    # Gets the average value of the stock for a given date
    def getStockHistoryAverageValue(self, stockID, date):
        query = StockQueries.getAvgStockHistoryQuery(stockID, date)
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getStockHistoryAverageValue. \nUnable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getStockHistoryAverageValue:", sys.exc_info()[0])  
        
        result = []
        for row in self.cursor:
            result.append(row['stock_history_average'])
        
        return result[0]    # Result will always be 1 value, since its a MySQL AVG call.
    