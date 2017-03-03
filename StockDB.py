import mysql.connector
import sys
from mysql.connector.errors import IntegrityError as mysql_IntegrityError
from mysql.connector.errors import DataError as mysql_DataError
from mysql.connector.errors import ProgrammingError as mysql_ProgrammingError

# A class to handle MySQL interactions with the StockBot database.
class StockDB:
    # Hardcoded inserts for stock and stock_history tables.
    inserts = {'ins_stock' : ("INSERT INTO stock (stock_id, avg_open, avg_daily, avg_close) "
                              "VALUES (%s, %s, %s, %s)"),
                'ins_stock_history' : ("INSERT INTO stock_history (stock_id, stock_history_timestamp, stock_history_price) "
                "VALUES (%s, %s, %s)")}
    # Hardcoded select statements to grab keys from the tables.
    keys = {'key_stock' : ("SELECT stock_id FROM stock"),
            'key_stock_history' : ("SELECT stock_id, stock_history_timestamp FROM stock_history")}
    
    # TODO: Make a dictionary of common queries based on information in the database for updating purposes.
    
    # Attempt to initialize a connection with the given parameters.
    def __init__(self, user, password, hostIP, database):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                      host=hostIP, database=database)
            self.cursor = self.cnx.cursor()
        # Throw errors if the connection cannot be initialized.
        except mysql_ProgrammingError:
            print("Unable to initialize StockDB connection due to invalid inputs.")
        except:
            print("Unable to initialize StockDB connection. Unexpected error:", sys.exc_info()[0])
        
    # Closes the active cursor and connection for this object.
    # Effecitvely disables the object.
    def close(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except:
            pass
    
    # Adds a stock with the given parameters to the StockBot.stock table in the MySQL database.
    def addStock(self, stockID, avgOpen, avgDaily, avgClose):
        try:
            self.cursor.execute(StockDB.inserts['ins_stock'], (stockID, avgOpen, avgDaily, avgClose))
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
            self.cursor.execute(StockDB.inserts['ins_stock_history'], 
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
        dictCurs = self.cnx.cursor(dictionary=True)
        query = StockDB.keys['key_' + table]
        
        try:
            dictCurs.execute(query)
        except mysql_ProgrammingError:
            print("Invalid MySQL query in getKeys. Unable to execute query '{}'".format(query))
        except:
            print("Unexpected error in getKeys:", sys.exc_info()[0])
        
        result = []
        for row in dictCurs:
            result.append(row['stock_id'])
        
        dictCurs.close()
        return result
    