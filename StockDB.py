import mysql.connector
import sys
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
        # Throw errors if the connection cannot be initialized.
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
            self.cursor.execute(StockQueries.ins_stock, (stockID, avgOpen, avgDaily, avgClose))
            self.cnx.commit()
            
        except mysql_IntegrityError:
            print("Key {} already exists in table stock!".format(stockID))
        except mysql_DataError:
            print("Invalid inputs for stock MySQL query.")
        except TypeError:
            print("Incorrect number of arguments for stock query.")
        except:
            print("Unexpected error in addStock:", sys.exc_info()[0])
            
    # Adds a stock history entry with the given parameters to the StockBot.stock_history table
    # in the MySQL database.
    def addStockHistory(self, stockID, timestamp, price):
        try:
            self.cursor.execute(StockQueries.ins_stock_history, 
                                   (stockID, timestamp, price))
            self.cnx.commit()
            
        except mysql_IntegrityError:
            print("Key ({}, {}) already exists in table stock_history!".format(stockID, timestamp))
        except mysql_DataError:
            print("Invalid inputs for stock_history MySQL query.")
        except TypeError:
            print("Incorrect number of arguments for stock_history query.")
        except:
            print("Unexpected error in addStockHistory:", sys.exc_info()[0])
    
    # Attempts to execute the database query parameters and outputs the results to the console.
    def queryDB(self, dbQuery):
        try:
            result = self.cursor.execute(dbQuery, multi=True)
        except mysql_ProgrammingError:
            print("Invalid MySQL syntax! Unable to execute query '{}'".format(dbQuery))
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
    
    # Gets the keys of the tuples in the given table and returns them.
    def getKeys(self, table):
        if table == 'stock':
            query = StockQueries.key_stock
        elif table == 'stock_history':
            query = StockQueries.key_stock_history
        else:
            print("Invalid table passed to getKeys.")
            return
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getKeys. Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getKeys:", sys.exc_info()[0])
        
        result = []
        for row in self.cursor:
            result.append(row['stock_id'])
        
        return result
    
    # Averages the history of the stock.
    def avgHistory(self, stock_id, attribute):
        if attribute == 'daily':
            query = StockQueries.avg_stock_daily.format(stock_id)
        elif attribute == 'open':
            query = StockQueries.avg_stock_open.format(stock_id)
        elif attribute == 'close':
            query = StockQueries.avg_stock_close.format(stock_id)
        else:
            print("Invalid attribute passed to avgHistory.")
            return
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in avgHistory. Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in avgHistory:", sys.exc_info()[0])
            
        average = []
        for row in self.cursor:
            average.append(row['avg_' + attribute])
        
        return average
            
    # Gets the attribute names of a given table in the database.
    def getAttributeNames(self, table):
        query = StockQueries.attributeNames.format(table)
        
        try:
            self.cursor.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getAttributeNames. Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getAttributeNames:", sys.exc_info()[0])
            
        attributes = []
        for row in self.cursor:
            attributes.append(row)
        return attributes
    
    # Updates a given attribute of a given stock with the given value.
    def updateStockAttribute(self, stock_id, attribute, value): 
        if attribute == 'daily':
            query = StockQueries.upd_stock_daily.format(value, stock_id)
        elif attribute == 'open':
            query = StockQueries.upd_stock_open.format(value, stock_id)
        elif attribute == 'close':
            query = StockQueries.upd_stock_close.format(value, stock_id)
        else:
            print("Invalid attribute input to updateStockAttribute.")
            return
        
        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql_ProgrammingError:
            print("Invalid MySQL query in updateStockAttribute. Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in updateStockAttribute:", sys.exc_info()[0])   
            