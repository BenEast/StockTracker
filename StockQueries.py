
# A wrapper class of MySQL queries for the StockBot database.
class StockQueries:
    
    # Hardcoded inserts for stock and stock_history tables.
    ins_stock = ("INSERT INTO stock (stock_id, avg_open, avg_daily, avg_close) "
                "VALUES (%s, %s, %s, %s)")
    
    ins_stock_history = ("INSERT INTO stock_history (stock_id, stock_history_timestamp, stock_history_price) "
                         "VALUES (%s, %s, %s)")  
              
    # Hardcoded select statements to grab keys from the tables.
    key_stock = ("SELECT stock_id FROM stock")
    
    key_stock_history = ("SELECT stock_id, stock_history_timestamp FROM stock_history")
    
    # Hardcoded update statements to change values in the StockBot.stock table.
    upd_stock_open = ("UPDATE stock SET avg_open = {} WHERE stock_id = '{}'")
    
    upd_stock_daily = ("UPDATE stock SET avg_daily = {} WHERE stock_id = '{}'")
    
    upd_stock_close = ("UPDATE stock SET avg_daily = {} WHERE stock_id = '{}'")
    
    # Hardcoded select statements to get the averages of values from the stock_history table.

    avg_stock_daily = ("SELECT AVG(stock_history_price) AS avg_daily FROM stock_history WHERE stock_id = '{}'")
    
    avg_stock_open = ("SELECT AVG(stock_history_price) AS avg_open FROM stock_history WHERE stock_id = '{}' AND "
                      "stock_history_timestamp < 08:45:00")
    
    avg_stock_close = ("SELECT AVG(stock_history_price) AS avg_close FROM stock_history WHERE stock_id = '{}' AND "
                       "stock_history_timestamp > 14:50:00")
    
    # Hardcoded SQL statement for getting column/attribute names
    attributeNames = ("SELECT 'COLUMN_NAME' FROM 'INFORMATION_SCHEMA'.'COLUMNS' "
                      "WHERE 'TABLE_SCHEMA' = 'StockBot' AND 'TABLE_NAME' = '{}'")
    
    